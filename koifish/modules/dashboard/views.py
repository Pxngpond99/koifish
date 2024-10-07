from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required, current_user, login_user, logout_user
from flask_mongoengine import Pagination
from mongoengine import Q
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import pandas
import numpy
from wtforms import validators
from koifish.web import acl
from koifish.api.redis_rq import redis_queue
from koifish.api.utils import video_utils
from .forms import SelectTimeRange

module = Blueprint(
    "dashboard", __name__, template_folder="templates", url_prefix="/dashboard"
)


def average_every_n_elements(data, n):
    return [int(sum(data[i : i + n]) / n) for i in range(0, len(data), n)]


@module.route("", methods=["GET", "POST"])
def index():
    form = SelectTimeRange()
    df = pandas.read_csv(
        "koifish/modules/dashboard/data/20241002_modify.csv",
    )

    heatmap_data, xedges, yedges = numpy.histogram2d(
        df["x"], df["y"], bins=(1280 // int(form.bin.data) , 960 // int(form.bin.data) )
    )
    heatmap_data = numpy.fliplr(heatmap_data)

    heatmap_data = heatmap_data.T.tolist()
    xedges = xedges.tolist()
    yedges = yedges.tolist()

    df["A"] = numpy.where(df["Area"] == "A", 1, 0)
    df["B"] = numpy.where(df["Area"] == "B", 1, 0)
    df["C"] = numpy.where(df["Area"] == "C", 1, 0)
    result_A = df.groupby("step")["A"].sum().to_list()
    result_B = df.groupby("step")["B"].sum().to_list()
    result_C = df.groupby("step")["C"].sum().to_list()

    averaged_A = average_every_n_elements(result_A, int(form.time.data ))
    averaged_B = average_every_n_elements(result_B, int(form.time.data ))
    averaged_C = average_every_n_elements(result_C, int(form.time.data ))
    all_result = [averaged_A, averaged_B, averaged_C]

    averaged_X = df["x"].iloc[::int(form.time.data )].to_list()
    averaged_Y = df["y"].iloc[::int(form.time.data )].to_list()

    scatter_value = [averaged_X, averaged_Y]
    print(form.errors)
    return render_template(
        "dashboard/index.html",
        heatmap_data=heatmap_data,
        xedges=xedges,
        yedges=yedges,
        all_result=all_result,
        scatter_value=scatter_value,
        form=form,
    )


@module.route("/live", methods=["GET", "POST"])
def live():

    return render_template(
        "dashboard/live.html",
    )
