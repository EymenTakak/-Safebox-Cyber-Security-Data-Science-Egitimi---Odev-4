import sys
try:
    import pymongo
    from flask import Flask, render_template, request, jsonify
    import json
    import pandas as pd
except:
    print("pymongo , flask ve pandas kütüphanlerini yükleyiniz...")
    sys.exit()

dbusername = "<MONGODB KULLANICI ADI>"
dbpassword = "<MONGODB SIFRE>"
dbipadres = "<MONGODB IPADRESS>"

app = Flask(__name__)


try:
    md = pymongo.MongoClient(f"mongodb+srv://{dbusername}:{dbpassword}@{dbipadres}/?retryWrites=true&w=majority")
except:
    print("mongo db client bağlantısı başarısız")
    sys.exit()


db = md["flaskmongodb"]
col = db["Users"]



@app.route('/adduser', methods=['POST'])
def addUser():
    try:
        data = request.json
        result = col.insert_one(data)
        return "Kullanıcı Ekleme Başarılı"
    except:
        return "Hata!"




@app.route('/<int:number>')
def getGtAge(number):
    li = []
    data = col.find({"Age": {"$gt": number}})

    for i,one in enumerate(data):
        li.append(list(one.values()))
        li[i][0] = str(li[i][0])

    df = pd.DataFrame(li)
    new_columns = ["ID", "Name", "Age", "Job", "Description"]
    df.columns = new_columns

    data = df.to_dict(orient='records')
    return render_template('index.html', data=data)



@app.route('/')
def getAll():
    li = []
    data = col.find()

    for i, one in enumerate(data):
        li.append(list(one.values()))
        li[i][0] = str(li[i][0])

    df = pd.DataFrame(li)
    new_columns = ["ID", "Name", "Age", "Job", "Description"]
    df.columns = new_columns

    data = df.to_dict(orient='records')
    return render_template('index.html', data=data)



@app.route('/deleteuser', methods=["DELETE"])
def delUser():

    try:
        data = request.json
        docid = data.get('id')
        col.find_one_and_delete({'_id': docid})

        return "Silme İşlemi Başarılı"
    except:
        return "Hata!"


if __name__ == '__main__':
    app.run(debug=True)