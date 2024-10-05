#!/usr/bin/env python3
import mongoengine as me
import sys
from koifish.modules.accounts.models import User


def init_admin():
    if User.objects(username="admin").first():
        print("already have admin user in database")
        return

    admin_user = User(
        username="admin",
        email="admin@example.com",
        first_name="admin",
        last_name="admin",
        roles=["admin"],
        phone="0999999999",
    )
    admin_user.set_password("p@ssw0rd")
    admin_user.save()
    print("create admin user username: admin password: p@ssw0rd")


if __name__ == "__main__":
    DB_NAME = "koifishdb"
    if len(sys.argv) > 1:
        me.connect(db=DB_NAME, host=sys.argv[1])
    else:
        me.connect(db=DB_NAME)
    print(f"connect to {DB_NAME}")

    init_admin()
    print("======= create user success ========")
