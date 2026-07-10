import json

from flask import Blueprint, jsonify
from flask import request
from first_flask import user

mod = Blueprint('user', __name__, url_prefix='/user')

with open("first_flask//data.json", 'r') as abc:
     data = json.load(abc)
     print(data)
#
# @mod.route('/abc/', methods=['GET'])
# def fetch():
#     return "List of user"
#
# @mod.route('/dfg/', methods=['GET'])
# def login():
#     return "Sakshi Kamthe"
#
# @mod.route('/hij/', methods=['GET'])
# def collage():
#     return "Trinity Academy of Engineering"
#
# @mod.route('/', methods=['GET'])
# def f_fetch():
#     return jsonify(data)

@mod.route('/create_user', methods=['POST'])
def create_user():
    user_data=request.get_json() #get json sent by client(Post

#handle empty data case
    if len(data)==0:
        new_user_id=1
    else:
        new_user_id=data [-1] ['id']+1
        #get last user's ID and increment by 1

    response=user_data              #copy incoming user data into response
    response['id']=new_user_id      #Add generrate ID to response

    data.append(response)           #Add new user to data list

    #proper file handling
    with open("first_flask\\data.json", 'w')as f:            #with keyword is used to close file automatically
        json.dump(data,f)
    return jsonify(response)

@mod.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    #Function receives 'id' from url

    user_data=request.get_json()
    #Get JSON data sent from client (Postman/body)

    for user in data:
        #loop through all users stored in 'data' list

        if user['id']==id:
            #check if current user's id matches the given id

            user["name"]=user_data.get("name", user["name"])
            #update name if provided otherwise kip old value

            user["email"]=user_data.get("email", user["email"])
            #update email if provided, otherwise keep old value
            #user["password"]=user_data.get("password", user["password"])

            with open("first_flask\\data.json", 'w')as f:
                #open JSOn file in write mode
                json.dump(user,f)
                #save updatede data list back into file

            return jsonify({
                "message":"User updated successfully",
                "data":user
            })
            #return success response with updated user
    return jsonify({"message":"User not FOUND"}), 404
    #if no matching user found ->return error with 404 status

@mod.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):

        for user in data:
            #Loop through all users in data list

            if user['id'] ==id:
                #check if current user's id matches given id

                data.remove(user)
            #remove that user from the list

            with open("first_flask\\data.json", 'w')as f:
                #open JSON file in write mode

                json.dump(user,f)
                #save updated data (after deletion)  into file

            return jsonify({
                "message":"User deleted successfully"
            })
            #return success message
        return jsonify({"message":"User NOT FOUND"}), 404
