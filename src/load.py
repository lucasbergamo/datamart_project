import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text, Integer, String, Float, Date, DECIMAL

load_dotenv()
db_url = os.getenv('DB_URL')

if db_url is None:
    raise ValueError("A variável de ambiente 'DB_URL' não está definida no arquivo .env.")

engine = create_engine(db_url)

with engine.begin() as conn:
    print("✅ Conectado ao banco de dados PostgreSQL com sucesso!")
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS meu_schema"))
    print("✅ Schema 'meu_schema' criado/verificado com sucesso!")

trusted_path = '/app/data/trusted'
refined_path = '/app/data/refined'

os.makedirs(refined_path, exist_ok=True)

if not os.path.exists(trusted_path):
    raise FileNotFoundError(f"❌ O diretório '{trusted_path}' não foi encontrado!")

parquet_files = [f for f in os.listdir(trusted_path) if f.endswith('.parquet')]

if not parquet_files:
    print("⚠️ Nenhum arquivo Parquet encontrado na pasta 'trusted'. Nada para processar.")
else:
    print(f"📂 {len(parquet_files)} arquivos Parquet encontrados. Iniciando o processamento...")

schemas = {
    "clientes": {
        "id_cliente": Integer,
        "nome_cliente": String(100),
        "email": String(100),
        "telefone": String(15)
    },
    "produtos": {
        "id_produto": Integer,
        "nome_produto": String(100),
        "categoria": String(120),
        "preco": DECIMAL(10, 2)
    },
    "transacoes": {
        "id_transacao": Integer,
        "id_cliente": Integer,
        "id_produto": Integer,
        "quantidade": Integer,
        "data_transacao": Date
    }
}

for parquet_file in parquet_files:
    file_path = os.path.join(trusted_path, parquet_file)
    table_name = os.path.splitext(parquet_file)[0]

    try:
        df = pd.read_parquet(file_path)

        if table_name in schemas:
            for col, dtype in schemas[table_name].items():
                if col in df.columns:
                    if dtype == Date:  
                        df[col] = pd.to_datetime(df[col])
                    elif dtype == Integer:
                        df[col] = df[col].astype("int")
                    elif dtype == Float or dtype == DECIMAL:
                        df[col] = df[col].astype("float")
                    elif isinstance(dtype, String):
                        df[col] = df[col].astype(str)

        refined_file_path = os.path.join(refined_path, parquet_file)
        df.to_parquet(refined_file_path, index=False)
        print(f"✅ Arquivo refinado salvo: {refined_file_path}")

        df.to_sql(table_name, engine, schema="meu_schema", if_exists="replace", index=False, dtype=schemas.get(table_name, {}))
        print(f"✅ Dados do arquivo {parquet_file} carregados na tabela '{table_name}' com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao processar o arquivo {parquet_file}: {e}")

print("🎉 Todos os dados foram processados, refinados e carregados no banco de dados com sucesso!")
