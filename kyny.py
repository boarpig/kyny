#!/usr/bin/python
#coding: utf8

from bottle import Bottle
from bottle import get
from bottle import post
from bottle import redirect
from bottle import request
from bottle import response
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
    response.set_cookie("name", name, max_age=20 * 365 * 24 * 3600)
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
    response.set_cookie("score", str(score), max_age=60)
    time = request.forms.time
    if time in ("1", "5", "15"):
        with sqlite3.connect("kyny.db") as conn:
            conn.execute("insert into score(user, score, time) values (?, ?, ?)",
                    (name, score, time))
    redirect_page = """<!DOCTYPE html>
                    <html>
                    <head>
                    <title>Redirecting to highscore list</title>
                    <meta charset="UTF-8">
                    <meta http-equiv="Refresh" content="0; url=/highscore" />
                    </head>
                    <body>
                    <p>You are being redirected to <a
                    href="/highscore">highscore list</a>.</p>
                    <p>If you are not redirected after a few seconds, please click on the
                    link above!</p>
                    </body>
                    </html>"""
    return redirect_page

def fix_strings(in_text):
    replace_dict = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
    for key in replace_dict:
        in_text = in_text.replace(key, replace_dict[key])
    return in_text

@app.get("/highscore")
def get_hiscore():
    times = (1, 5, 15)
    if request.get_cookie("name"):
        cookie_name = request.get_cookie("name")
    else:
        cookie_name = ""
    if request.get_cookie("score"):
        cookie_score = request.get_cookie("score")
    else:
        cookie_score = ""
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
            scored = False
            for record in c:
                name = fix_strings(record[0])
                score = str(record[1])
                if name == cookie_name:
                    if score == cookie_score and scored == False:
                        page += "<tr class=hi><td class=hi><b>" + name + "</b></td>"
                        page += "<td><b>" + score + "</b></td></tr>"
                        scored = True
                    else:
                        page += "<tr class=hi><td class=hi>" + name + "</td>"
                        page += "<td>" + score + "</td></tr>"
                else:
                    page += "<tr><td>" + name + "</td>"
                    page += "<td>" + score + "</td></tr>"
            page += "</table>"
    page += '<a href="/">Back to main menu</a>'
    page += "</body></html>"
    return page

@app.route("/game/<time>")
@view("game.html")
def index(time="1"):
    if request.get_cookie("name"):
        name = request.get_cookie("name")
    else:
        name = ""
    name = fix_strings(name)
    if time in ["1", "5", "15"]:
        return dict(time=time, name=name)

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
