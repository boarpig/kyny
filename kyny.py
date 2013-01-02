#!/usr/bin/python

from bottle import Bottle, get, post, route, request, run, static_file, template
import os

app = Bottle()

@app.post('/hiscore')
def submit_hiscore():
    newgame = '<a href="/kyny.html">New game</a>'
    page = "<!DOCTYPE HTML><html><head><title>heh</title>" + \
           "<meta charset=\"UTF-8\"></head><body>"
    name = request.forms.get("name")
    score = request.forms.get("score")
    with open("hiscores.txt", "a") as f:
        print(name + ": " + score + "\n", file=f)
    with open("hiscores.txt", "r") as f:
        scores = f.readlines()
    scoredic = []
    for scori in scores:
        scori = scori[:-1]
        print('"' + scori + '"')
        if len(scori) > 1:
            user, score = scori.split(":")
            scoredic.append((int(score), user))
    scoredic.sort()
    scoredic.reverse()
    for scoor in scoredic:
        page += str(scoor[0]) + ": " + str(scoor[1]) + "<br>"
    page += newgame
    page += "</body></html>"
    return page

@app.route("/")
def index():
    return template("template/game.html")

@app.route("/static/<name>")
def serve_static(name):
    return static_file("static/" + name, root="./")

run(app, server="tornado", host="localhost", port=8080, reloader=True,
        debug=True)
