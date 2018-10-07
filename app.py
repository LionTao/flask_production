# coding=utf-8
from gevent import monkey
import jieba

monkey.patch_all()
from flask import Flask, request, render_template, redirect, render_template_string, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, Label, meta, RadioField
from restBackend import forwardDispatcher, reverseDispatcher
import json
import requests


class MyForm(FlaskForm):
    terms = TextAreaField("Facts")
    submit = SubmitField("Submit")


class choice(FlaskForm):
    mychoice = RadioField('choice', choices=[('1', '是'), ('2', '否')], )
    submit = SubmitField("Submit")


cnt = 0
res = ""
process = ""
facts = ""
ask = False
question = ""

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def main():
    global cnt, res, process, facts, ask, question
    factForm = MyForm(meta={"csrf": False})
    askForm = choice(meta={"csrf": False})
    if request.method == "GET":
        return render_template("index.html", form=factForm, choice=askForm, ask=ask, process=process, res=res, cnt=cnt,
                               question=question)
    if request.method == "POST":
        cnt += 1
        if MyForm.validate_on_submit(factForm) and ask == False:
            new_res = request.form["terms"]
            new_res = jieba.cut(new_res, cut_all=True)
            new_res = [i for i in new_res]
            if facts == "":
                facts = new_res
                msg = json.dumps({"mode": "init", "data": new_res})
                api_res = requests.post('http://127.0.0.1:5000/api/forward/', data=msg)
                if api_res.json()["err"] == 0 and api_res.json()["mode"] == 1:
                    # we got something to ask
                    ask = True
                    question = "请问有 “{}” 这个条件吗？".format(api_res.json()["msg"])
                    return redirect('/')
                res = api_res.json()["msg"]

        if choice.validate_on_submit(askForm):
            answer = askForm.mychoice.data
            msg = json.dumps({"mode": "answer", "data": answer})
            api_res = requests.post('http://127.0.0.1:5000/api/forward/', data=msg)
            if api_res.json()["err"] == 0 and api_res.json()["mode"] == 1:
                # wo got something to ask
                ask = True
                question = "请问有 “{}” 这个条件吗？".format(api_res.json()["msg"])
                return redirect('/')
            elif api_res.json()["err"] == 0 and api_res.json()["mode"] == 0:
                ask = False
                api_res = api_res.json()
                process = api_res["msg"]["process"]
                res = api_res["msg"]["res"]
            return redirect('/')
        return redirect('/')


@app.route('/reverse', methods=["GET", "POST"])
def main_reverse():
    global cnt, res, process, facts, ask, question
    factForm = MyForm(meta={"csrf": False})
    askForm = choice(meta={"csrf": False})
    if request.method == "GET":
        return render_template("index.html", form=factForm, choice=askForm, ask=ask, process=process, res=res, cnt=cnt,
                               question=question)
    if request.method == "POST":
        cnt += 1
        if MyForm.validate_on_submit(factForm) and ask == False:
            new_res = request.form["terms"].split(' ')
            if facts == "":
                facts = new_res
                msg = json.dumps({"mode": "init", "data": new_res})
                api_res = requests.post('http://127.0.0.1:5000/api/reverse/', data=msg)
                if api_res.json()["err"] == 0 and api_res.json()["mode"] == 1:
                    # wo got something to ask
                    ask = True
                    question = "请问有 “{}” 这个条件吗？".format(api_res.json()["msg"])
                    return redirect('/reverse')
                res = api_res.json()["msg"]["res"]
                process = api_res.json()["msg"]["process"]
                # print(res)

        if choice.validate_on_submit(askForm):
            answer = askForm.mychoice.data
            # print("answer",answer,type(answer))
            msg = json.dumps({"mode": "answer", "data": answer})
            api_res = requests.post('http://127.0.0.1:5000/api/reverse/', data=msg)
            if api_res.json()["err"] == 0 and api_res.json()["mode"] == 1:
                # wo got something to ask
                ask = True
                question = "请问有 “{}” 这个条件吗？".format(api_res.json()["msg"])
                return redirect('/reverse')
            elif api_res.json()["err"] == 0 and api_res.json()["mode"] == 0:
                ask = False
                api_res = api_res.json()
                process = api_res["msg"]["process"]
                res = api_res["msg"]["res"]
            return redirect('/reverse')
        return redirect('/reverse')


@app.route('/api/forward/', methods=["POST", "GET"])
def doforward():
    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        return jsonify(json.loads(forwardDispatcher(request.data)))


@app.route('/api/reverse/', methods=["POST", "GET"])
def doreverse():
    if request.method == "GET":
        return redirect('/')

    if request.method == "POST":
        return jsonify(json.loads(reverseDispatcher(request.data)))


if __name__ == '__main__':
    app.run(debug=True)
