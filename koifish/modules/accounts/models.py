import mongoengine as me
import bcrypt
import datetime
from flask_login import UserMixin

USER_ROLES = [
    ("staff", "Staff"),
    ("admin", "Admin"),
]

USER_STATUS = [
    ("active", "เปิดการใช้งาน"),
    ("pending", "รอดำเนินการ"),
    ("disactive", "ปิดการใช้งาน"),
]

class User(me.Document, UserMixin):
    username = me.StringField(required=True, min_length=3, max_length=64, unique=True)
    password = me.StringField(required=True, default="")
    first_name = me.StringField(required=True, max_length=128)
    last_name = me.StringField(required=True, max_length=128)

    email = me.StringField(required=True, max_length=128)
    # line_id = me.StringField(max_length=128)
    phone = me.StringField(max_length=11)

    status = me.StringField(required=True, default="pending", choices=USER_STATUS)
    roles = me.ListField(me.StringField(), default=[USER_ROLES[0][0]])

    # resources = me.DictField()
    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )
    last_login_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )

    meta = {"collection": "users", "indexes": ["first_name", "last_name"]}

    def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash

        if check_password_hash(self.password, password):
            return True
        return False

    def has_roles(self, roles: list):
        if set(roles) & set(self.roles):
            return True
        return False

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
