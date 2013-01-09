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
import sqlite3

app = Bottle()

with sqlite3.connect("kyny.db") as conn:
    c = conn.cursor()
    c.execute("""create table if not exists score(id integer primary key
            autoincrement, user text not null, score int not null, time int not
            null)""")
    conn.commit()

@app.post('/hiscore')
def submit_hiscore():
    name = request.forms.get("name")
    score = request.forms.get("score")
    time = request.forms.get("time")
    with sqlite3.connect("kyny.db") as conn:
        conn.execute("insert into score(user, score, time) values (?, ?, ?)",
                (name, score, time))
    redirect("/highscore")

@app.get("/highscore")
def get_hiscore():
    times = (1, 5, 15)
    page = "<!DOCTYPE HTML><html><head><title>heh</title>" + \
           "<meta charset=\"UTF-8\"></head><body>"
    with sqlite3.connect("kyny.db") as conn:
        c = conn.cursor()
        for time in times:
            c.execute("""select user, score from score where time=? order by
                    score desc""", (str(time),))
            page += "<h1>" + str(time) + " minute highscore</h1>"
            page += "<table border=1>"
            for record in c:
                page += "<tr><td>" + str(record[0]) + "</td>" + \
                        "<td>" + str(record[1]) + "</td></tr>"
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
