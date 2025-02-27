import requests, zipfile, os, shutil

url = "https://github.com/magazord-plataforma/data_engineer_test/archive/refs/heads/master.zip"
zip_path = "master.zip"

with open(zip_path, "wb") as f:
    f.write(requests.get(url).content)

with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(".")

folder = "data_engineer_test-master"
raw_path = "data/raw"
os.makedirs(raw_path, exist_ok=True)

for file in ["cliente.csv", "produtos.csv"]:
    file_path = os.path.join(folder, file)
    if os.path.exists(file_path):
        shutil.move(file_path, os.path.join(raw_path, file))
        print(f"✅ {file} movido para {raw_path}")

for file in os.listdir(folder):
    if file.endswith(".zip"):
        with zipfile.ZipFile(os.path.join(folder, file), "r") as z:
            z.extractall(raw_path)

os.remove(zip_path)
shutil.rmtree(folder)

print("🎉 Todos os arquivos foram movidos para 'data/raw/'")
