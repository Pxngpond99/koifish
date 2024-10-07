from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required, current_user, login_user, logout_user
from flask_mongoengine import Pagination
from mongoengine import Q
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from wtforms import validators

from koifish.web import acl
from . import forms, models, utils


module = Blueprint("accounts", __name__, template_folder="templates")


@module.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if not form.validate_on_submit():
        error_msg = form.errors
        print(form.errors)
        return render_template("accounts/login.html", form=form)

    user = models.User.objects(username=form.username.data).first()

    if not user or not user.check_password(form.password.data):
        print(form.errors)
        error_msg = "โปรดตรวจสอบ username และ password ของท่าน"
        return render_template("accounts/login.html", form=form, error_msg=error_msg)

    if user.status == "disactive":
        print(form.errors)
        error_msg = "username ของท่านถูกลบออกจากระบบ"
        return render_template("accounts/login.html", form=form, error_msg=error_msg)

    # if user.status == "disactive":
    #     error_msg = "โปรดติดต่อผู้ดูแลระบบเพื่อยืนยันบัญชีของท่าน"
    #     return render_template("accounts/login.html", form=form, error_msg=error_msg)

    login_user(user, remember=form.remember.data)
    user.last_login_date = datetime.datetime.now()
    user.save()
    next = request.args.get("next")
    if next:
        return redirect(next)

    return redirect(url_for("site.index"))


@module.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@module.route("/profile")
@login_required
def profile():
    user = current_user._get_current_object()
    employer = models.Employer.objects.get(id=user.id)
    return render_template("accounts/profile.html", user=user, employer=employer)


@module.route("/users/<user_id>/setup_password", methods=["GET", "POST"])
def setup_password(user_id):
    user = models.User.objects.get(id=user_id)
    form = forms.accounts.SetupPasswordForm(obj=user)

    if not form.validate_on_submit():
        return render_template(
            "accounts/setup_password.html", form=form, user_id=user_id
        )

    user = models.User.objects.get(id=user_id)
    user.status = "active"
    user.set_password(form.password.data)
    user.save()
    return redirect(url_for("site.index"))


@module.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    form = forms.ResetPasswordForm()
    error = request.args.get("error")
    completed = request.args.get("completed")
    if not form.validate_on_submit():
        print(form.errors)
        return render_template(
            "accounts/forgot_password.html", form=form, error=error, completed=completed
        )
    user = models.User.objects(
        username=form.username.data, phone=form.phone.data
    ).first()
    if not user:
        return redirect(
            url_for(
                "accounts.forgot_password",
                error=f"ไม่พบผู้ใช้ {form.username.data} หรือเบอร์โทร {form.phone.data}",
                completed=completed,
            )
        )
    user.set_password(form.phone.data)
    user.save()
    return redirect(
        url_for(
            "accounts.forgot_password",
            completed="เปลี่ยนรหัสผ่านเป็นเบอร์โทรศัพท์ของผู้ใช้สำเร็จ",
            error=error,
        )
    )


@module.route("/<user_id>/reset_password", methods=["GET", "POST"])
@acl.roles_required("admin", "staff")
def reset_password(user_id):
    user = models.User.objects(id=user_id).first()
    # ตั้งรหัสผ่านใหม่ให้เป็น username
    user.set_password(user.username)
    user.save()

    return redirect(url_for("accounts.customer_index", **request.args))


@module.route("/change_password", methods=["GET", "POST"])
@acl.roles_required("admin", "staff")
def change_password():
    form = forms.ChangePasswordForm()
    user = current_user
    if not form.validate_on_submit():
        print(form.errors)
        return render_template("accounts/change_password.html", form=form)
    user.set_password(form.password.data)
    user.save()
    return render_template("accounts/change_password.html", form=form, completed=True)
