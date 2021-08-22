# from flask import Flask
# from flask_pymongo import pymongo
# from bson.json_util import dumps
# from bson.objectid import ObjectId
# from flask import jsonify,request
# from werkzeug.security import generate_password_hash,check_password_hash

# #initializing flask app
# app=Flask(__name__)
# app.secret_key="secretkey"
# CONNECTION_STRING = "mongodb+srv://karthik:karthik@mumbai.jjic1.mongodb.net/Mumbai?retryWrites=true&w=majority"
# client = pymongo.MongoClient(CONNECTION_STRING)
# db = client.get_database('Mumbai')
# #user_collection = pymongo.collection.Collection(db, 'user_collection')
# @app.route("/add",methods=["POST"])
# def add_user():
#     _json=request.json
#     _name=_json['name']
#     db.main.insert_one({"name": _name})
#     return jsonify(_name)
    

# if __name__ == "__main__":
#     app.run(debug=True)
#Updated practice session
from flask import Flask, json,request,jsonify
from flask_pymongo import pymongo
#This is where the setting happens
app=Flask(__name__)
app.secret_key="Elon musk"
CONNECTION_URL="mongodb+srv://karthik:karthik@mumbai.jjic1.mongodb.net/Mumbai?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_URL)
db=client.get_database("Mumbai")
@app.route("/signup",methods=['POST','GET'])
def signup():
    def insert_data(email,password,phone):
        db.users.insert_one({"email":email,"password":password,"phone":phone})
        return 1
    signup_json=request.json
    email=signup_json["email"]
    password=signup_json["password"]
    confirm_password=signup_json["confirm_password"]
    phone = signup_json["phone"]
    #Now we will execute conditions on this 
    #email check 
    if(len(phone)!=10):
        return jsonify("OOPS something went wrong with the API collection")
    if password != confirm_password:
        return jsonify("OOPS something went wrong")
    found_contact=list(db.users.find({"email":email}))
    if(len(found_contact)==0):
        if(insert_data(email,password,phone)):
            return jsonify("You were posted in our database !!! Thanks for joining in the team")
        else:
            return jsonify("oops something went wrong")
    else:
        return jsonify("Your already a part of us ...Try logging in")

@app.route("/login",methods=["POST","GET"])
def login():
    def check(incoming_json):
        results=list(db.users.find({"email":incoming_json["email"],"password":incoming_json["password"]}))
        if(len(results)==0):
            #Meaning no entries were found 
            return 0
        else:
            return 1
    incoming_json=request.json
    check_result=check(incoming_json)
    if(check_result):
        return jsonify("You have logged in successfully")
    else:
        return jsonify("Your credentials were wrong")


#This is main branch for allocation of signup and login API for books using cluster 

@app.route("/add",methods=['POST','GET'])
def add():
    incoming_json=request.json
    db.books.insert_one({"name":incoming_json["name"],"author":incoming_json["author"]})
    return jsonify("You have successfully added your book onto our database")
@app.route("/get_details/<book>",methods=['POST','GET'])#Route for getting details of a book
def get_book_don(book):
    book_retr=list(db.books.find({"name":book},{"_id":0}))
    if(len(book_retr)==0):
        return jsonify("no books were found")

@app.route("/update",methods=['POST','GET'])
def update():
    def check_existence(book):
        exist=list(db.books.find({"name":book}))
        if len(exist)==0:
            #book not found
            return 0
        else:
            return 1

    incoming_json=request.json
    book_to_be_updated=incoming_json["book_original"]
    updated_book_name=incoming_json["updated_name"]
    updated_author=incoming_json["updated_author"]
    flag=check_existence(book_to_be_updated)
    if(flag):
        try:
            db.books.update_many({"name":book_to_be_updated},{"$set":{"name":updated_book_name,"author":updated_author}})
            return jsonify("successsfully updated")
        except:
            return jsonify("OOPS connection error")

    else:
<<<<<<< HEAD
        return jsonify("Book does not exist")

    

=======
        return jsonify(book_retr)

@app.route("/delete/<book>",methods=["POST","GET"])
def delete_don(book):
    try:
        db.books.delete_many({"name":book})
        return jsonify("database successfully updated")
    except:
        return jsonify("something went wrong")
>>>>>>> get_details_and_delete




if __name__=="__main__":
    app.run(debug=True)


