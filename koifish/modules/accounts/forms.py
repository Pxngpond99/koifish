from flask_wtf import FlaskForm, file

from wtforms import fields, validators
from flask_mongoengine.wtf import model_form
from . import models


class LoginForm(FlaskForm):
    username = fields.StringField(
        "Username",
        [
            validators.DataRequired("Username is required."),
            validators.Length(min=5),
        ],
    )
    password = fields.PasswordField(
        "Password",
        validators=[
            validators.InputRequired("Password is required."),
            validators.Length(min=6),
        ],
    )
    remember = fields.BooleanField("Remember")
    submit = fields.SubmitField("Login")


class UserFullNameForm(FlaskForm):
    first_name = fields.StringField(
        "First Name",
        [
            validators.DataRequired("First Name is required."),
            validators.Length(min=0, max=128),
            validators.InputRequired(),
        ],
        render_kw={
            "placeholder": "First Name",
        },
    )
    last_name = fields.StringField(
        "Last Name",
        [
            validators.DataRequired("Last Name is required."),
            validators.Length(min=0, max=128),
            validators.InputRequired(),
        ],
        render_kw={
            "placeholder": "Last Name",
        },
    )


class ResetPasswordForm(FlaskForm):
    username = fields.StringField(
        "ชื่อผู้ใช้",
        render_kw={"placeholder": "ชื่อผู้ใช้", "autocomplete": "off"},
        validators=[
            validators.DataRequired("Username is required."),
            validators.Length(min=5),
        ],
    )
    phone = fields.StringField(
        "เบอร์โทรศัพท์",
        render_kw={"placeholder": "เบอร์โทรศัพท์", "autocomplete": "off"},
        validators=[validators.InputRequired()],
    )


class ChangePasswordForm(FlaskForm):
    password = fields.PasswordField(
        "รหัสผ่าน",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
        ],
        render_kw={"placeholder": "รหัสผ่าน", "autocomplete": "off"},
    )
    confirm_password = fields.PasswordField(
        "ยืนยันรหัสผ่าน",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
            validators.EqualTo("password", message="รหัสผ่านไม่ตรงกัน"),
        ],
        render_kw={"placeholder": "ยืนยันรหัสผ่าน", "autocomplete": "off"},
    )


# ----------------- Customer ----------------- #

BaseCustomerForm = model_form(
    models.User,
    FlaskForm,
    exclude=[
        "addresses",
        "roles",
        "approver",
        "resources",
        "created_date",
        "updated_date",
        "password",
        "last_login_date",
        "medicine_license",
        "commercial_registration",
        "professional_license",
        "certification_tax_registration",
    ],
    field_args={
        "username": {
            "label": "ชื่อผู้ใช้",
            "render_kw": {"placeholder": "ชื่อผู้ใช้"},
        },
        "email": {
            "label": "อีเมล",
            "render_kw": {"placeholder": "อีเมล"},
            "validators": [validators.Email(), validators.InputRequired()],
        },
        "first_name": {
            "label": "ชื่อต้น",
            "render_kw": {"placeholder": "ชื่อ"},
        },
        "last_name": {
            "label": "นามสกุล",
            "render_kw": {"placeholder": "นามสกุล"},
        },
        "phone": {
            "label": "เบอร์โทรศัพท์",
            "render_kw": {"placeholder": "เบอร์โทรศัพท์"},
            "validators": [validators.InputRequired()],
        },
        "line_id": {
            "label": "Line ID",
            "render_kw": {"placeholder": "Line ID"},
        },
        "shop_name": {
            "label": "ชื่อร้าน",
            "render_kw": {"placeholder": "ชื่อร้าน"},
        },
        "status": {
            "label": "สถานะลูกค้า",
            "render_kw": {"placeholder": "สถานะลูกค้า"},
        },
    },
)


class CustomerForm(BaseCustomerForm):
    upload_shop_picture = fields.FileField(
        "รูปหน้าร้านหรือรูปบุคคล ( ไฟล์ขนาดไม่เกิน 100 kB )",
        validators=[
            file.FileAllowed(["jpg", "jpeg", "png"], "เฉพาะไฟล์ jpg, jpeg, png")
        ],
    )
    upload_medicine_license = fields.FileField(
        "ใบอนุญาตขายยา (ถ้ามี)",
        validators=[
            file.FileAllowed(["pdf"], "เฉพาะไฟล์ pdf"),
        ],
    )
    upload_commercial_registration = fields.FileField(
        "ทะเบียนพาณิชย์ (ถ้ามี)",
        validators=[
            file.FileAllowed(["pdf"], "เฉพาะไฟล์ pdf"),
        ],
    )
    upload_professional_license = fields.FileField(
        "ใบประกอบวิชาชีพ",
        validators=[
            file.FileAllowed(["pdf"], "เฉพาะไฟล์ pdf"),
        ],
    )
    upload_certification_tax_registration = fields.FileField(
        "ใบ ภ.พ. 20 (ถ้ามี)",
        validators=[
            file.FileAllowed(["pdf"], "เฉพาะไฟล์ pdf"),
        ],
    )

    password = fields.PasswordField(
        "รหัสผ่าน",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
        ],
        render_kw={"placeholder": "รหัสผ่าน", "autocomplete": "new-password"},
    )
    confirm_password = fields.PasswordField(
        "ยืนยันรหัสผ่าน",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
            validators.EqualTo("password", message="รหัสผ่านไม่ตรงกัน"),
        ],
        render_kw={"placeholder": "ยืนยันรหัสผ่าน", "autocomplete": "new-password"},
    )

    house_number = fields.StringField(
        "เลขที่อยู่",
        render_kw={
            "placeholder": "เลขที่อยู่",
        },
    )
    alley = fields.StringField(
        "ซอย",
        render_kw={
            "placeholder": "ซอย",
        },
    )
    village_number = fields.StringField(
        "หมู่ที่",
        render_kw={
            "placeholder": "หมู่ที่",
        },
    )
    road = fields.StringField(
        "ถนน",
        render_kw={
            "placeholder": "ถนน",
        },
    )
    sub_district = fields.StringField(
        "แขวง/ตำบล",
        render_kw={
            "placeholder": "แขวง/ตำบล",
        },
    )
    district = fields.StringField(
        "เขต/อำเภอ",
        render_kw={
            "placeholder": "เขต/อำเภอ",
        },
    )
    province = fields.StringField(
        "จังหวัด",
        render_kw={
            "placeholder": "จังหวัด",
        },
    )
    zipcode = fields.StringField(
        "รหัสไปรษณีย์",
        render_kw={
            "placeholder": "รหัสไปรษณีย์",
        },
    )
    customer_type = fields.SelectField(
        "ประเภทลูกค้า",
        validators=[validators.InputRequired()],
        render_kw={"placeholder": "ประเภทลูกค้า"},
    )


class EditCustomerForm(CustomerForm):
    password = None
    confirm_password = None
    username = None
    email = None


class SearchCustomerForm(BaseCustomerForm):
    customer_type = fields.SelectField(
        "ประเภทลูกค้า",
        validators=[validators.Optional()],
        render_kw={"placeholder": "ประเภทลูกค้า"},
    )
    customer_status = fields.SelectField(
        "สถานะลูกค้า",
        validators=[validators.Optional()],
        render_kw={"placeholder": "สถานะลูกค้า"},
    )
    username = fields.StringField("ชื่อผู้ใช้", render_kw={"placeholder": "ชื่อผู้ใช้"})
    email = fields.StringField("อีเมล", render_kw={"placeholder": "อีเมล"})
    first_name = fields.StringField("ชื่อ", render_kw={"placeholder": "ชื่อ"})
    last_name = fields.StringField("นามสกุล", render_kw={"placeholder": "นามสกุล"})
    phone = fields.StringField("เบอร์โทรศัพท์", render_kw={"placeholder": "เบอร์โทรศัพท์"})


class VerifyCustomerForm(FlaskForm):
    customer_type = fields.SelectField(
        "ประเภทลูกค้า",
        validators=[validators.InputRequired()],
        render_kw={"placeholder": "ประเภทลูกค้า"},
    )
    customer_status = fields.SelectField(
        "สถานะลูกค้า",
        validators=[validators.InputRequired()],
        render_kw={"placeholder": "สถานะลูกค้า"},
    )


class UploadCustomer(FlaskForm):
    upload_file = fields.FileField(
        "ไฟล์เอกสาร",
        validators=[
            file.FileAllowed(["xlsx", "csv"], "ไฟล์ xlsx หรือ csv เท่านั้น"),
        ],
    )


# ----------------- User ----------------- #
class SearchUserForm(FlaskForm):
    email = fields.StringField("อีเมล", render_kw={"placeholder": "อีเมล"})
    first_name = fields.StringField("ชื่อต้น", render_kw={"placeholder": "ชื่อต้น"})
    last_name = fields.StringField("นามสกุล", render_kw={"placeholder": "นามสกุล"})
    roles = fields.SelectField(
        "บทบาทผู้ใช้",
        choices=[
            ("", "ทั้งหมด"),
            ("staff", "พนักงาน"),
            ("admin", "ผู้ดูแล"),
        ],
    )


class UserForm(SearchUserForm):
    username = fields.StringField(
        "ชื่อผู้ใช้",
        [
            validators.DataRequired("Username is required."),
            validators.Length(min=5),
        ],
        render_kw={"placeholder": "ชื่อผู้ใช้"},
    )
    email = fields.StringField(
        "อีเมล",
        render_kw={"placeholder": "อีเมล"},
        validators=[validators.InputRequired()],
    )
    phone = fields.StringField(
        "เบอร์โทรศัพท์",
        render_kw={"placeholder": "เบอร์โทรศัพท์"},
        validators=[validators.InputRequired()],
    )
