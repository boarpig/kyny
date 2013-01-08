#!/usr/bin/python

from bottle import Bottle
from bottle import get
from bottle import post
from bottle import redirect
from bottle import request
from bottle import route
from bottle import run
from bottle import static_file 
from bottle import template
from bottle import view
import os

app = Bottle()

@app.post('/hiscore')
def submit_hiscore():
    name = request.forms.get("name")
    score = request.forms.get("score")
    time = request.forms.get("time")
    with open("hiscore_" + time + ".txt", "a") as f:
        print(name + ": " + score, file=f)
    redirect("/highscore")

@app.get("/highscore")
def get_hiscore():
    times = ("1", "5", "15")
    page = "<!DOCTYPE HTML><html><head><title>heh</title>" + \
           "<meta charset=\"UTF-8\"></head><body>"
    for time in times:
        try:
            with open("hiscore_" + time + ".txt", "r") as f:
                scores = f.readlines()
        except FileNotFoundError:
            scores = ""
        scoredic = []
        for scori in scores:
            scori = scori[:-1]
            if len(scori) > 1:
                user, score = scori.split(":")
                scoredic.append((int(score), user))
        scoredic.sort()
        scoredic.reverse()
        page += "<h1>" + time + " minute highscore</h1>"
        page += "<table border=1>"
        for scoor in scoredic:
            page += "<tr><td>" + str(scoor[0]) + "</td><td>" + str(scoor[1]) + \
                    "</td></tr>"
        page += "</table>"
    page += '<a href="/">Back to main menu</a>'
    page += "</body></html>"
    return page

@app.route("/game/<time>")
@view("game.html")
def index(time="1"):
    if time in ["1", "5", "15"]:
        return dict(time=time)

@app.route("/")
def serve_main():
    return static_file("main.html", root="static/")

@app.route("/favicon.ico")
def serve_favicon():
    return static_file("favicon.png", root="static/")

@app.route("/static/<name>")
def serve_static(name):
    return static_file(name, root="static/")

run(app, server="tornado", host="localhost", port=8080, reloader=True, debug=True)
