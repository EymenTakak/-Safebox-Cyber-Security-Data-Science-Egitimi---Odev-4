import sys
try:
    import pymongo
    from columnar import columnar
except:
    print("pymongo ve columlar kütüphanlerini yükleyiniz...")
    sys.exit()

dbusername = "<MONGODB KULLANICI ADI>"
dbpassword = "<MONGODB SIFRE>"
dbipadres = "<MONGODB IPADRESS>"

try:
    md = pymongo.MongoClient(f"mongodb+srv://{dbusername}:{dbpassword}@{dbipadres}/?retryWrites=true&w=majority")
except:
    print("mongo db client bağlantısı başarısız")
    sys.exit()

db = md["flaskmongodb"]
col = db["Users"]


def getAll():
    li = []
    data = col.find()

    for one in data:
        li.append(list(one.values()))

    print(columnar(li, ["ID","Name","Age","Job","Description"], no_borders=True))

def getFilteredUser(name):
    li = []
    data = col.find({"Name" : name})

    for one in data:
        li.append(list(one.values()))
    print(columnar(li, ["ID", "Name", "Age", "Job", "Description"], no_borders=True))


def getFilteredAge(age):
    li = []
    data = col.find({"Age": {"$gt": age}})

    for one in data:
        li.append(list(one.values()))
    print(columnar(li, ["ID", "Name", "Age", "Job", "Description"], no_borders=True))

def filteredAgeM(age):
    stat = {"Age": {"$gt": age}}
    upd = {"$set": {"Description": "0"}}

    try:
        col.update_many(stat, upd)
        getFilteredAge(age)
        print("Güncelleme İşlemi Başarılı")

    except:
        print("Güncelleme İşlemi Başarısız")


def filteredDelete(fAge, sAge):
    stat =  {"Age": {"$gt": fAge, "$lt": sAge}}
    try:
        col.delete_many(stat)
        getAll()
        print(f"Silme İşlemi Başarılı.")
    except Exception:
        print("Silme İşlemi Başarısız")


try:
    filteredDelete(0,80)
except Exception as e:
    print(e)