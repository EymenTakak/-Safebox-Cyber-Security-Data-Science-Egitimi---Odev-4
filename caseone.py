import sys
import random
try:
    from faker import Faker
    import pymongo
except:
    print("pymongo ve Faker kütüphanelerini yükleyiniz...")
    sys.exit()

dbusername = "<MONGODB KULLANICI ADI>"
dbpassword = "<MONGODB SIFRE>"
dbipadres = "<MONGODB IPADRESS>"

info = Faker('tr_TR')

try:
    md = pymongo.MongoClient(f"mongodb+srv://{dbusername}:{dbpassword}@{dbipadres}/?retryWrites=true&w=majority")
except:
    print("mongo db client bağlantısı başarısız")
    sys.exit()


db = md["flaskmongodb"]
col = db["Users"]


try:
    for _ in range(50):
        name = info.name().split()[0]
        age = random.randint(18,70)
        job = info.job()

        pers = {"Name": name, "Age":age, "Job": job, "Description": "1"}
        # pers = {"Name": info.name().split()[0], "Age":random.randint(18,70), "Job": info.job(), "Description": "1"}

        col.insert_one(pers)

    print("Veri Ekleme Başarılı.")
except Exception as e:
    print("Veri Ekleme Başarısız! \n",e)