import requests, zipfile, os, shutil

# 1️⃣ Baixar o ZIP do GitHub
url = "https://github.com/magazord-plataforma/data_engineer_test/archive/refs/heads/master.zip"
zip_path = "master.zip"

with open(zip_path, "wb") as f:
    f.write(requests.get(url).content)

# 2️⃣ Extrair o ZIP principal
with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(".")

# 3️⃣ Definir caminhos
folder = "data_engineer_test-master"  # Pasta extraída
raw_path = "data/raw"  # Caminho para a pasta raw
os.makedirs(raw_path, exist_ok=True)  # Garante que a pasta exista

# 4️⃣ Mover os arquivos CSV soltos (clientes.csv e produtos.csv) para raw
for file in ["cliente.csv", "produtos.csv"]:
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):  # Verifica se o arquivo existe antes de mover
        shutil.move(file_path, os.path.join(raw_path, file))
        print(f"✅ {file} movido para {raw_path}")

# 5️⃣ Encontrar e extrair os ZIPs internos (transacoes_1.zip, transacoes_2.zip, etc.)
for file in os.listdir(folder):
    if file.endswith(".zip"):
        with zipfile.ZipFile(os.path.join(folder, file), "r") as z:
            z.extractall(raw_path)  # Extrai diretamente para data/raw

# 6️⃣ Limpeza
os.remove(zip_path)
shutil.rmtree(folder)

print("🎉 Todos os arquivos foram movidos para 'data/raw/'")
