#!/usr/bin/python
#coding: utf8

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
            autoincrement, user text not null, score integer not null, time
            integer not
            null)""")
    conn.commit()

@app.post('/hiscore')
def submit_hiscore():
    name = request.forms.name
    name = name.strip()
    if len(name) > 50:
        name = name[:50]
    if len(name) == 0:
        redirect("/highscore")
    try:
        score = int(request.forms.score)
        if score <= 0 or score > 1337:
            score = 0
    except ValueError:
        score = 0
    time = request.forms.time
    if time in ("1", "5", "15"):
        with sqlite3.connect("kyny.db") as conn:
            conn.execute("insert into score(user, score, time) values (?, ?, ?)",
                    (name, score, time))
    redirect("/highscore")

def fix_strings(in_text):
    replace_dict = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    for key in replace_dict:
        in_text = in_text.replace(key, replace_dict[key])
    return in_text

@app.get("/highscore")
def get_hiscore():
    times = (1, 5, 15)
    page = "<!DOCTYPE HTML><html><head><title>Highscore</title>" + \
        '<link type="text/css" href="/static/hiscore.css" rel="stylesheet">' + \
           "<meta charset=\"UTF-8\"></head><body>"
    with sqlite3.connect("kyny.db") as conn:
        c = conn.cursor()
        for time in times:
            c.execute("""select user, score from score where time=? order by
                    score desc""", (str(time),))
            page += "<h1>" + str(time) + " minute highscore</h1>"
            page += "<table border=1>"
            for record in c:
                fixed = fix_strings(record[0])
                page += "<tr><td>" + fixed + "</td>" + \
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
