"""
Script para extrair toda a estrutura do banco de dados em formato JSON.
Extrai informações sobre tabelas, colunas, tipos, constraints, foreign keys, etc.
"""
import json
from datetime import datetime
from sqlalchemy import inspect
from resource.database import engine


def extract_database_structure():
    """Extrai a estrutura completa do banco de dados."""
    inspector = inspect(engine)

    database_structure = {
        "database_url": str(engine.url).replace(engine.url.password or "", "****"),
        "extraction_date": datetime.now().isoformat(),
        "tables": []
    }

    # Obtém todos os nomes das tabelas
    table_names = inspector.get_table_names()

    for table_name in table_names:
        table_info = {
            "name": table_name,
            "columns": [],
            "primary_keys": [],
            "foreign_keys": [],
            "indexes": [],
            "constraints": []
        }

        # Extrair informações das colunas
        columns = inspector.get_columns(table_name)
        for column in columns:
            column_info = {
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "default": str(column["default"]) if column["default"] is not None else None,
                "autoincrement": column.get("autoincrement", False),
                "comment": column.get("comment", None)
            }
            table_info["columns"].append(column_info)

        # Extrair primary keys
        pk_constraint = inspector.get_pk_constraint(table_name)
        if pk_constraint:
            table_info["primary_keys"] = pk_constraint.get("constrained_columns", [])
            table_info["primary_key_name"] = pk_constraint.get("name", None)

        # Extrair foreign keys
        foreign_keys = inspector.get_foreign_keys(table_name)
        for fk in foreign_keys:
            fk_info = {
                "name": fk.get("name", None),
                "constrained_columns": fk.get("constrained_columns", []),
                "referred_table": fk.get("referred_table", None),
                "referred_columns": fk.get("referred_columns", []),
                "on_delete": fk.get("ondelete", None),
                "on_update": fk.get("onupdate", None)
            }
            table_info["foreign_keys"].append(fk_info)

        # Extrair índices
        indexes = inspector.get_indexes(table_name)
        for index in indexes:
            index_info = {
                "name": index.get("name", None),
                "columns": index.get("column_names", []),
                "unique": index.get("unique", False)
            }
            table_info["indexes"].append(index_info)

        # Extrair outras constraints (unique, check, etc)
        try:
            unique_constraints = inspector.get_unique_constraints(table_name)
            for constraint in unique_constraints:
                constraint_info = {
                    "type": "unique",
                    "name": constraint.get("name", None),
                    "columns": constraint.get("column_names", [])
                }
                table_info["constraints"].append(constraint_info)
        except NotImplementedError:
            pass

        try:
            check_constraints = inspector.get_check_constraints(table_name)
            for constraint in check_constraints:
                constraint_info = {
                    "type": "check",
                    "name": constraint.get("name", None),
                    "sqltext": str(constraint.get("sqltext", None))
                }
                table_info["constraints"].append(constraint_info)
        except NotImplementedError:
            pass

        database_structure["tables"].append(table_info)

    return database_structure


def save_to_json(data, filename="database_structure.json"):
    """Salva a estrutura em arquivo JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Estrutura do banco de dados salva em: {filename}")


def print_summary(data):
    """Imprime um resumo da estrutura extraída."""
    print("\n" + "="*60)
    print("RESUMO DA ESTRUTURA DO BANCO DE DADOS")
    print("="*60)
    print(f"\nData de extração: {data['extraction_date']}")
    print(f"Total de tabelas: {len(data['tables'])}\n")

    for table in data["tables"]:
        print(f"\n📋 Tabela: {table['name']}")
        print(f"   └─ Colunas: {len(table['columns'])}")
        print(f"   └─ Primary Keys: {', '.join(table['primary_keys']) if table['primary_keys'] else 'Nenhuma'}")
        print(f"   └─ Foreign Keys: {len(table['foreign_keys'])}")
        print(f"   └─ Índices: {len(table['indexes'])}")
        print(f"   └─ Constraints: {len(table['constraints'])}")

        if table['columns']:
            print(f"\n   Colunas:")
            for col in table['columns']:
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                default = f" DEFAULT {col['default']}" if col['default'] else ""
                print(f"      • {col['name']}: {col['type']} {nullable}{default}")

        if table['foreign_keys']:
            print(f"\n   Foreign Keys:")
            for fk in table['foreign_keys']:
                cols = ', '.join(fk['constrained_columns'])
                ref_cols = ', '.join(fk['referred_columns'])
                print(f"      • {cols} → {fk['referred_table']}.{ref_cols}")


if __name__ == "__main__":
    try:
        print("Conectando ao banco de dados...")
        print(f"URL: {str(engine.url).replace(str(engine.url.password) if engine.url.password else '', '****')}")

        print("\nExtraindo estrutura do banco de dados...")
        structure = extract_database_structure()

        # Salvar em JSON
        save_to_json(structure)

        # Imprimir resumo
        print_summary(structure)

        print("\n" + "="*60)
        print("✓ Extração concluída com sucesso!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Erro ao extrair estrutura: {str(e)}")
        import traceback
        traceback.print_exc()
