from user_model.table import User_Registration_Form
from db_connections.configurations import session


def is_user_valid(name):
    result = session.query(User_Registration_Form).filter(User_Registration_Form.name == name).all()
    if result:
        return True
    else:
        return False


def is_userpwd_valid(pwd, cnf_pwd):
    print(f"PWD - {pwd}")
    print(f"CNFPWD - {cnf_pwd}")
    if pwd == cnf_pwd:
        return True
    else:
        return False


def is_useremail_valid(mail):
    result = session.query(User_Registration_Form).filter(User_Registration_Form.mail == mail).all()
    if result:
        return True
    else:
        return False


def is_userphone_valid(ph):
    result = session.query(User_Registration_Form).filter(User_Registration_Form.ph == ph).all()
    if result:
        return True
    else:
        return False
