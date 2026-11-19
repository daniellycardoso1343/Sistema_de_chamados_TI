"""Compara os models SQLAlchemy com o docs/banco.dbml e lista as divergências.

Uso (na raiz do projeto, com o venv ativo):
    python scripts/conferir_models.py
"""
import re
import sys
from pathlib import Path

from sqlalchemy import BigInteger, CheckConstraint, UniqueConstraint

RAIZ = Path(__file__).resolve().parent.parent
DBML = RAIZ / "docs" / "banco.dbml"

# Colunas que estão no .dbml, mas que de propósito ainda não existem nos models.
IGNORAR = {
    ("chamados", "solucao_usada_id"),  # volta na Fase 2, junto com a tabela solucoes
}


# ---------------------------------------------------------------- leitura do .dbml
def ler_dbml(texto):
    enums = {}
    for m in re.finditer(r"^Enum\s+(\w+)\s*\{(.*?)^\}", texto, re.S | re.M):
        enums[m.group(1)] = set(re.findall(r"^\s*(\w+)\s*$", m.group(2), re.M))

    tabelas = {}
    for m in re.finditer(r"^Table\s+(\w+)\s*\{(.*?)^\}", texto, re.S | re.M):
        tabelas[m.group(1)] = _ler_tabela(m.group(2))
    return enums, tabelas


def _ler_tabela(corpo):
    colunas, indices, checks_note = {}, [], 0
    modo = None
    for linha in corpo.splitlines():
        s = linha.strip()
        if modo == "indexes":
            if s == "}":
                modo = None
            elif s:
                indices.append(tuple(re.findall(r"\w+", s)))
            continue
        if modo == "note":
            if "'''" in s:
                modo = None
            elif s.upper().startswith("CHECK"):
                checks_note += 1
            continue
        if s.startswith("Indexes"):
            modo = "indexes"
            continue
        if s.startswith("Note:"):
            if s.count("'''") == 1:
                modo = "note"
            continue
        m = re.match(r"^(\w+)\s+(\w+(?:\(\d+\))?)\s*(?:\[(.*)\])?\s*$", s)
        if not m:
            continue
        nome, tipo, attrs = m.group(1), m.group(2), m.group(3) or ""
        attrs = re.sub(r"note:\s*'[^']*'", "", attrs)
        ref = re.search(r"ref:\s*[<>-]\s*(\w+)\.(\w+)", attrs)
        padrao = re.search(r"default:\s*(`[^`]*`|'[^']*'|[\w.]+)", attrs)
        colunas[nome] = {
            "tipo": tipo,
            "pk": bool(re.search(r"\bpk\b", attrs)),
            "not_null": "not null" in attrs,
            "unique": bool(re.search(r"\bunique\b", attrs)),
            "ref": f"{ref.group(1)}.{ref.group(2)}" if ref else None,
            "default": padrao.group(1) if padrao else None,
        }
    return {"colunas": colunas, "indices": indices, "checks_note": checks_note}


# --------------------------------------------------------------------- comparação
def _valor_default(texto):
    if texto.startswith("`"):
        return "now()" if "now" in texto else texto
    if texto.startswith("'"):
        return texto.strip("'")
    if texto in ("true", "false"):
        return texto == "true"
    return int(texto) if texto.lstrip("-").isdigit() else texto


def comparar(metadata, texto_dbml):
    enums, tabelas = ler_dbml(texto_dbml)
    erros = []

    for nome in sorted(set(tabelas) - set(metadata.tables)):
        erros.append(f"[{nome}] tabela do .dbml não existe nos models (nome errado ou model não registrado?)")
    for nome in sorted(set(metadata.tables) - set(tabelas)):
        erros.append(f"[{nome}] tabela dos models não existe no .dbml (nome errado?)")

    for nome, esp in tabelas.items():
        t = metadata.tables.get(nome)
        if t is None:
            continue
        e = lambda msg: erros.append(f"[{nome}] {msg}")

        esperadas = {c for c in esp["colunas"] if (nome, c) not in IGNORAR}
        for c in sorted(esperadas - set(t.columns.keys())):
            e(f"coluna '{c}' falta no model")
        for c in sorted(set(t.columns.keys()) - set(esp["colunas"])):
            e(f"coluna '{c}' existe no model mas não no .dbml (nome errado?)")

        n_enum = 0
        for cnome in sorted(esperadas & set(t.columns.keys())):
            d, col = esp["colunas"][cnome], t.columns[cnome]

            obrigatoria = d["pk"] or d["not_null"]
            if col.nullable == obrigatoria:
                e(f"'{cnome}': {'deveria ser obrigatória' if obrigatoria else 'deveria aceitar vazio (| None)'}")

            unica = bool(col.unique) or any(
                isinstance(c, UniqueConstraint) and list(c.columns) == [col] for c in t.constraints
            )
            if d["unique"] and not unica:
                e(f"'{cnome}': falta unique=True")
            if unica and not d["unique"]:
                e(f"'{cnome}': tem unique=True, mas o .dbml não pede")

            m = re.match(r"varchar\((\d+)\)", d["tipo"])
            if m and getattr(col.type, "length", None) != int(m.group(1)):
                e(f"'{cnome}': tamanho deveria ser String({m.group(1)}), está {getattr(col.type, 'length', None)}")
            if d["tipo"] == "bigint" and not isinstance(col.type, BigInteger):
                e(f"'{cnome}': deveria ser db.BigInteger")

            alvos = {fk.target_fullname for fk in col.foreign_keys}
            if d["ref"] and d["ref"] not in alvos:
                e(f"'{cnome}': deveria ter ForeignKey('{d['ref']}')")
            if alvos and not d["ref"]:
                e(f"'{cnome}': tem ForeignKey, mas o .dbml não pede")

            padrao = _valor_default(d["default"]) if d["default"] else None
            if padrao == "now()":
                if col.server_default is None:
                    e(f"'{cnome}': falta server_default=db.func.now()")
            else:
                if col.server_default is not None:
                    e(f"'{cnome}': tem server_default, mas o .dbml não pede (nasce preenchida?)")
                if padrao is not None:
                    atual = col.default.arg if col.default is not None else None
                    if atual != padrao:
                        e(f"'{cnome}': deveria ter default={padrao!r}, está {atual!r}")

            if d["tipo"] in enums:
                n_enum += 1
                valores = enums[d["tipo"]]
                achou = None
                for c in t.constraints:
                    if isinstance(c, CheckConstraint):
                        mm = re.search(rf"\b{cnome}\s+IN\s*\(([^)]*)\)", str(c.sqltext))
                        if mm:
                            achou = set(re.findall(r"'([^']*)'", mm.group(1)))
                if achou is None:
                    e(f"'{cnome}': falta o CheckConstraint com os valores {sorted(valores)}")
                elif achou != valores:
                    e(f"'{cnome}': CHECK com valores diferentes do .dbml "
                      f"(sobra {sorted(achou - valores)}, falta {sorted(valores - achou)})")

        n_checks = sum(isinstance(c, CheckConstraint) for c in t.constraints)
        esperado_checks = n_enum + esp["checks_note"]
        if n_checks != esperado_checks:
            e(f"deveria ter {esperado_checks} CheckConstraint, tem {n_checks} (__table_args__ com nome errado?)")

        esp_idx = {tuple(i) for i in esp["indices"]}
        got_idx = [tuple(c.name for c in i.columns) for i in t.indexes]
        for i in sorted(esp_idx - set(got_idx)):
            e(f"falta o índice em {i}")
        for i in sorted(set(got_idx) - esp_idx):
            e(f"índice {i} não está no .dbml")
        if len(got_idx) != len(set(got_idx)):
            e("há índices repetidos nas mesmas colunas")
    return erros


# ------------------------------------------------------------------------ execução
def main():
    sys.path.insert(0, str(RAIZ))
    from app import create_app
    from app.extensions import db

    app = create_app()
    with app.app_context():
        erros = comparar(db.metadata, DBML.read_text(encoding="utf-8"))
        total = len(db.metadata.tables)

    print(f"Tabelas nos models: {total} (esperado: 18)")
    if erros:
        print(f"\n{len(erros)} divergência(s):\n")
        for erro in erros:
            print(" -", erro)
        sys.exit(1)
    print("Tudo confere com o banco.dbml.")


if __name__ == "__main__":
    main()