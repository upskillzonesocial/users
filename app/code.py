import datetime

from datetime import datetime
from dateutil.tz import tzutc, tzlocal

from user_model.table import User_Registration_Form
from db_connections.configurations import session
from email_constants import *
from flask import Flask, request
from datetime import datetime

from app.email_constants import MESSAGE
from app.db_operations import is_user_valid, is_userpwd_valid, is_useremail_valid, is_userphone_valid

from utils.reusables import *

app = Flask(__name__)

utc = datetime.now(tzutc())
print('UTC TIME: ' + str(utc))

local = utc.astimezone(tzlocal())
print('Local TIME: ' + str(local))


@app.route('/create-user', methods=['post'])
def create_user():
    """
    Creates a new user
    :return: Response as a dict
    """
    user_data = request.get_json()
    print(f"User data is---: {user_data}")

    if not is_user_valid(user_data.get('fname') + user_data.get('lname')):
        if is_userpwd_valid(user_data['password'], user_data.get('cpassword')):
            if not is_useremail_valid(user_data['mail']):
                if not is_userphone_valid(user_data['ph']):
                    try:
                        record = User_Registration_Form(name=user_data.get('fname') + user_data.get('lname'),
                                                        fname=user_data.get('fname'),
                                                        lname=user_data.get('lname'),
                                                        date=user_data.get('date'),
                                                        password=user_data.get('password'),
                                                        cpassword=user_data.get('cpassword'),
                                                        mail=user_data.get('mail'),
                                                        ph=user_data.get('ph'),
                                                        add=user_data.get('add'),
                                                        category=user_data.get('category'),
                                                        created_date=str(datetime.utcnow()))

                        session.add(record)
                        session.commit()
                        try:
                            send_email(["komalsaikiran05@gmail.com",
                                        "ushavenkateswararao100@gmail.com"], MESSAGE)
                            print(f"Email has been sent to the users ", )
                            return success_response(
                                f"User {user_data['fname'] + user_data['lname']} Created successfully",
                                receivers=["komalsaikiran05@gmail.com",
                                           "ushavenkateswararao100@gmail.com"], status_code=201,
                                datetime=str(datetime.utcnow()))

                        except Exception as err:
                            print("unable to sent email,reason is--", {err})
                            session.rollback()
                            return failure_response(
                                f"User {user_data['fname'] + user_data['lname']} is already created please try "
                                f"another user name", status_code=400)
                    except Exception as err:
                        print(f"Error occurred is --- {err}")
                        session.rollback()
                        return failure_response(f"Database operation failed reason is --- {err}", status_code=400)
                else:
                    return failure_response(f"User {user_data['ph']} already exists", status_code=400)
            else:
                return failure_response(f"User {user_data['mail']} already exists", status_code=400)
        else:
            return failure_response(f"Password and Confirm password doesn't match", status_code=400)
    else:
        return failure_response(f"Username {user_data.get('fname') + user_data.get('lname')} already exist",
                                status_code=400)


@app.route('/get-user-details', methods=['GET'])
def get_all_user_details():
    try:
        result = session.query(User_Registration_Form).all()

        send_email(["komalsaikiran05@gmail.com",
                    "ushavenkateswararao100@gmail.com"], GET_ALL_MESSAGE)
        print(f"Email has been sent to the users ")

    except Exception as err:
        print(f"Error occurred is--- {err}")
        return failure_response(f"error is {err}", status_code=500)

    results_dict = [item.__dict__ for item in result]
    print(f"Result : {result}")
    print(f"Result to Dictionary : {results_dict}")
    for item in results_dict:
        del item['_sa_instance_state']
        print(f"Cleaned Dictionary is --- {results_dict}")
    if results_dict:
        return success_response(results_dict, datetime=str(local))
    else:
        return failure_response(f"{results_dict} Does not exist", status_code=400)


@app.route('/user-range', methods=['GET'])
def user_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    user_name = request.args.get('name')
    print(f"Name is {user_name}")
    print(f"is_user_valid is {is_user_valid(user_name)}")
    if is_user_valid(user_name):
        pass
    else:
        return failure_response(f"{user_name} not allowed to see the data", status_code=403)
    try:
        result = session.query(User_Registration_Form).filter(
            User_Registration_Form.created_date >= start_date, User_Registration_Form.created_date <= end_date).all()
    except Exception as err:
        print(f"Error occurred is--- {err}")
        return failure_response(f"Error is {err}", status_code=500)
    results_dict = [item.__dict__ for item in result]
    print(f"Result : {result}")
    print(f"Result to Dictionary : {results_dict}")
    for item in results_dict:
        raw_item = item.copy()
        del item['_sa_instance_state']
        item.update({"today_date": str(datetime.utcnow())})
        item.update({"date_range": [start_date, end_date]})
        item.update({"current_time": str(local)})
        item.update({"raw_results": str(raw_item)})
        print(f"Cleaned Dictionary is --- {results_dict}")
    if results_dict:
        return success_response(results_dict, receivers=user_name)
    else:
        return failure_response(f"{results_dict} Does not exist", status_code=400)


@app.route('/single-user', methods=['GET'])
def single_user():
    result = []
    user_name = request.args.get('name')
    print(f"name is username--- {user_name}")
    print(f"is user valid is---{is_user_valid(user_name)}")
    if is_user_valid(user_name):
        pass

        try:
            result = session.query(User_Registration_Form).filter(User_Registration_Form.name == user_name).all()

            send_email(["komalsaikiran05@gmail.com",
                        "ushavenkateswararao100@gmail.com"], GET_SINGLE_MESSAGE)
            print(f"Email has been sent to the users ")
            return success_response(f"user{user_name}", datetime=str(datetime.utcnow()))
        except Exception as err:
            print(f"Error occurred is {err}")
        results_dict = [item.__dict__ for item in result]
        print(f"Result : {result}")
        print(f"Result to Dict : {results_dict}")

    else:
        return failure_response(f"{user_name} not allowed to see the data", status_code=403)
    for item in results_dict:
        del item['_sa_instance_state']
    print(f"Cleaned Dict - {results_dict}")
    if results_dict:
        return success_response(results_dict, datetime=str(datetime.utcnow()))
    else:
        return failure_response(f"User name {user_name} doesn't exist", status_code=400)


@app.route('/update-user-table', methods=['PATCH'])
def updated_user_table():
    data = request.get_json()
    print(f"Data is : {data}")
    if not is_user_valid(data.get('name')):
        return failure_response(f"{data.get('name')} User doesn't exist")

    try:
        session.query(User_Registration_Form).filter \
            (User_Registration_Form.name == data.get('name')).update(data)
        session.commit()
        send_email(["komalsaikiran05@gmail.com",
                    "ushavenkateswararao100@gmail.com"], UPDATE_MESSAGE)
        print(f"Email has been sent to the users ", )

        return success_response(f"User {data['name']} Updated successfully",
                                receivers=["komalsaikiran05@gmail.com",
                                           "ushavenkateswararao100@gmail.com"],
                                datetime=str(datetime.utcnow()))

    except Exception as err:
        session.rollback()
        return failure_response(f"Unable to update User {data.get('name')} Reason is:{err}")


@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    """
    This function deletes the user info
    :return:
    """
    data = request.get_json()
    print(f"Data is : {data}")
    if not is_user_valid(data.get('name')):
        return failure_response("{data.get('name')} User doesn't exist")
    try:
        session.query(User_Registration_Form).filter(
            User_Registration_Form.name == data.get('name')).delete()
        session.commit()
        send_email(["komalsaikiran05@gmail.com",
                    "ushavenkateswararao100@gmail.com"], DELETE_MESSAGE)
        print(f"Email has been sent to the users ")
        return success_response(f"{data.get('name')} User has been deleted", datetime=str(datetime.utcnow()))
    except Exception as err:
        session.rollback()
        return failure_response(f"Unable to delete User {data.get('name')} Reason is:{err}",
                                status_code=500)


app.run()
