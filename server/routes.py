from flask import current_app as app
from flask import request
import json
from datetime import datetime

from . import db
from server.models import User, Caption, FakeUser, Updates

from . import InstaBot


@app.route('/')
def index():
    response = {
        "error": "please add parameters"
    }
    responseJSON = json.dumps(response)
    return responseJSON, 400


@app.route('/api/insta')
def InstaApi():
    response = {
        "error": "You should use the api parameters",
    }
    return json.dumps(response), 400


@app.route('/api/insta/set-fakeuser')
def SetInstaFakeuser():
    username = request.args.get("username")
    password = request.args.get("password")
    if username is None or password is None:
        error = {
            "error": "You must provide a username and a password"
        }
        return json.dumps(error), 400
    user = FakeUser.query.get(1)
    if user is None:
        user = FakeUser(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        response = {
            "message": "fake user was updated",
            "username": user.username,
            "password": user.password
        }
        return json.dumps(response), 200
    user.username = username
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        error_res = {
            "error": "Could not update DB. Try again"
        }
        return json.dumps(error_res), 500
    response = {
        "message": "username set seuccessfully."
    }
    return json.dumps(response), 200


@app.route('/api/insta/get-fakeuser')
def GetInstaFakeuser():
    user = FakeUser.query.get(1)
    if user is None:
        error_response = {
            "error": "No fake user is set."
        }
        return json.dumps(error_response), 500
    response = {
        "message": "Fake user was found successfully.",
        "username": user.username,
    }
    return json.dumps(response), 200


@app.route('/api/insta/add-users')
def AddInstaTargetUser():
    users = request.args.get("users")
    if users is None:
        error = {
            "error": "Please provide new target users in query parameteres."
        }
        return json.dumps(error), 400

    users_lst = users.split(",")
    for user in users_lst:
        user_exists = User.query.filter_by(username=user).first()
        if user_exists is not None:
            continue
        try:
            new_user = User(username=user)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
            error_response = {
                "error": "Failed to add target user to db. Try Again!"
            }
            return json.dumps(error_response), 500
    response = {
        "message": "Target users were successfully added to db.",
        "users": users
    }
    return json.dumps(response), 200


@app.route('/api/insta/get-users')
def GetInstaTargetUsers():
    users = request.args.get("users")
    if users is None:
        try:
            target_users = db.session.query(User).all()
        except:
            error_response = {
                "error": "Could not fetch users from db"
            }
            return json.dumps(error_response), 500
    else:
        try:
            target_users = User.query.filter(User.username in users).all()
        except:
            error_response = {
                "error": "Could not fetch users from db"
            }
            return json.dumps(error_response), 500
    response_users = []
    for t_user in target_users:
        response_users.append({
            "username": t_user.username
        })
    response = {
        "message": "Successfully fetched users from db.",
        "users": response_users
    }
    return json.dumps(response), 200


@app.route('/api/insta/delete-users')
def DeleteInstaTargetUser():
    users = request.args.get("users")
    if users is None:
        error = {
            "error": "Please provide users to be deleted in query parameteres."
        }
        return json.dumps(error), 400

    users_lst = users.split(",")
    for user in users_lst:
        try:
            delete_user = User.query.filter_by(username=user).first()
            db.session.delete(delete_user)
            db.session.commit()
        except Exception as e:
            error_response = {
                "error": "Failed to delete target from db. Try Again!"
            }
            return json.dumps(error_response), 500
    response = {
        "message": "Target users were successfully deleted from db.",
        "deleted_users": users
    }
    return json.dumps(response), 200


@app.route('/api/insta/update')
def UpdateCaptions():
    app_settings = Updates.query.get(1)
    if app_settings is None:
        setting = Updates(isUpdating="FALSE")
        db.session.add(setting)
        db.session.commit()
    app_settings = Updates.query.get(1)
    if app_settings.isUpdating is "TRUE":
        error_response = {
            "error": "An update is in progress on the server. Try Later!"
        }
        return json.dumps(error_response), 500
    '''
    users = request.args.get("users")
    if users is not None:
        users_lst = users.split(",")
        target_users = 
        fakeuser = FakeUser.query.get(1)
        scraper = InstaBot(
            users=[u.username for u in target_users], 
            username=fakeuser.username,
            password=fakeuser.password)
        scraper.test()
        app_settings.isUpdating = "TRUE"
        db.session.add(app_settings)
        db.session.commit()
        response = {
            "message": "Captions are being updated successfully"
        }
        return json.dumps(response), 200
    '''
    target_users = db.session.query(User).all()
    fakeuser = FakeUser.query.get(1)
    scraper = InstaBot(
        users=[u.username for u in target_users], 
        username=fakeuser.username,
        password=fakeuser.password)
    scraper.authenticate_with_login()
    scraper.scrape()
    scraper.save_cookies()
    app_settings.isUpdating = "TRUE"
    db.session.add(app_settings)
    db.session.commit()
    response = {
        "message": "Captions are being updated successfully"
    }
    return json.dumps(response), 200


@app.route('/api/insta/users-captions-json', methods=["POST"])
def SaveCaptions():
    if request.method != 'POST':
        error_response = {
            "error": "You should only send a POST method containing captions data."
        }
        return json.dumps(error_response), 400
    try:
        app_settings = Updates.query.get(1)
    except:
        app_settings = Updates(isUpdating="FALSE")
        db.session.add(app_settings)
        db.session.commit()
    body = request.json
    print(body)
    try:
        for caption in body:
            print(caption)
            user = User.query.filter_by(username=caption["username"]).all()[0]
            # print(user)
            new_caption = Caption(
                text=caption["text"], 
                filePath=caption["filepath"], 
                userId=user.id, 
                dateTime=datetime.strptime(caption["datetime"], '%Y%m%d %Hh%Mm%Ss')
            )
            print(new_caption.text)
            db.session.add(new_caption)
            db.session.commit()
    except Exception as e:
        print(e)
        error_response = {
            "error": "Captions could not be saved. Data Is Lost!"
        }
        return json.dumps(error_response), 500
    app_settings = Updates.query.get(1)
    if app_settings is not None:
        app_settings.isUpdating = "FALSE"
        db.session.add(app_settings)
        db.session.commit()
    response = {
        "message": "Captions were saved succefssfully."
    }
    return json.dumps(response), 200


@app.route('/api/insta/get-feed')
def GetFeed():
    users = request.args.get("users")
    if users is None:
        error_response = {
            "error": "Please provide at least one target user by query args"
        }
        return json.dumps(error_response), 400
    captions = {}
    for user in users.split(","):
        try:
            caption_user = User.query.filter_by(username=user).first()
            if caption_user is not None:
                captions[user] = []
                ordered_caps = sorted(caption_user.captions, key=lambda x : x.dateTime, reverse=True)
                for cap in ordered_caps:
                    captions[user].append({
                        'text': cap.text,
                        'filePath': cap.filePath
                    })
        except Exception as e:
            error_res = {
                "error": "User could not be found or DB error."
            }
            return json.dumps(error_res), 500
    response = {
        "message": "Successfully loaded all user captions.",
        "captions": captions
    }
    return json.dumps(response), 200
