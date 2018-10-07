import json
from production import forward,reverse

facts = ""
process = ""
res = ""
isInit = True
mode = None
confirmation_list = set()
waiting = ""


def forwardDispatcher(message):
    global facts, process, res, isInit, confirmation_list, waiting

    message = json.loads(message)

    if message["mode"] == "init":
        print('initing....')
        facts = ' '.join(message["data"])
    elif message["mode"] == "forward":
        facts += ''.join(message["data"])
    elif message["mode"] == "answer":
        if message["data"] == "1":
            facts += " " + waiting
        if len(confirmation_list) > 0:
            waiting = confirmation_list.pop()
            return json.dumps({"err": 0, "mode": 1, "msg": waiting})
        else:
            waiting = ""


    # using existing facts to do forward production
    process, res = forward(facts)

    if res == "" and process == "":
        # no result
        return json.dumps({"err": 1, "mode": 0, "msg": "No result"})
    elif res == "" and process != "":
        # some thing to ask
        if type(process) == list:
            confirmation_list = set(process)
            waiting = confirmation_list.pop()
        return json.dumps({"err": 0, "mode": 1, "msg": waiting})
    elif res != "" and process != "":
        # figure out a conclusion
        return json.dumps({"err": 0, "mode": 0, "msg": {"process": process, "res": res}})
    else:
        return json.dumps({"err": 1, "mode": 1, "msg": "I must miss something"})

def reverseDispatcher(message):
    global facts, process, res, isInit, confirmation_list, waiting

    message = json.loads(message)

    if message["mode"] == "init":
        print('initing....')
        if len(message["data"])>1:
            facts = ' '.join(message["data"])
        else:facts=message["data"][0]
    elif message["mode"] == "forward":
        facts += ''.join(message["data"])
    elif message["mode"] == "answer":
        if message["data"] == "1":
            facts += " " + waiting
        if len(confirmation_list) > 0:
            waiting = confirmation_list.pop()
            return json.dumps({"err": 0, "mode": 1, "msg": waiting})
        else:
            waiting = ""

    # using existing facts to do forward production
    process, res = reverse(facts)

    if res == "" and process == "":
        # no result
        return json.dumps({"err": 1, "mode": 0, "msg": "No result"})
    elif res == "" and process != "":
        # some thing to ask
        if type(process) == list:
            confirmation_list = set(process)
            if len(confirmation_list)>0:
                waiting = confirmation_list.pop()
            else:
                return json.dumps({"err": 0, "mode": 0, "msg": {"process": "", "res": "no result"}})
        return json.dumps({"err": 0, "mode": 1, "msg": waiting})
    elif res != "" and process != "":
        # figure out a conclusion
        return json.dumps({"err": 0, "mode": 0, "msg": {"process": process, "res": res}})
    else:
        return json.dumps({"err": 1, "mode": 1, "msg": "I must miss something"})

if __name__ == '__main__':
    forwardDispatcher(json.dumps({"mode": "init", "data": "123123 232323"}))
