from logic import ListInSet, ListOneInSet, topological

PATH = "test.txt"


def readData():
    # if fact then conculusion
    fact = []
    res = []
    fo = open(PATH, 'r', encoding='utf-8')
    for line in fo:
        line = line.strip('\n')
        if line == '':
            continue
        line = line.split(' ')
        res.append(line[len(line) - 1])
        line.pop()
        fact.append(line[:-1])
    fo.close()
    return fact, res,


def readData_reverse():
    # if conculusion then fact
    fact = []
    res = []
    fo = open(PATH, 'r', encoding='utf-8')
    for line in fo:
        line = line.strip('\n')
        if line == '':
            continue
        line = line.split(' ')
        fact.append(line[len(line) - 1])
        line.pop()
        res.append(line)
    fo.close()
    return fact, res,

# forward production
def forward(input):
    topological()
    facts = input.split(' ')
    db_facts, db_res = readData()
    # data preparation done

    temp_db = set(facts)

    process = ""  # 存储推导过程
    res = ""  # 存储推导结果

    for f in db_facts:
        if set(f) & temp_db == set(f):
            ans = db_res[db_facts.index(f)]
            temp_db.add(ans)  # 将匹配到的前置结果添加到结果集合
            res = ans
            process += "{fact}-->{ans}\n".format(fact='，'.join(f), ans=ans)

    if res == "":
        confirm_list = []
        # seems we cannot figure a exist conclusion
        for f in db_facts:
            if len(set(f) & temp_db) > 0:
                for element in f:
                    if element not in temp_db:
                        confirm_list.append(element)
        return confirm_list, ""  # make sure res is empty for confirmation
    else:
        # yeah! we find a conclusion
        return process, res


# forward production
def reverse(input):
    topological()
    facts = input.split(' ')
    print("facts",facts)
    db_facts, db_res = readData_reverse()
    # data preparation done

    temp_db = set(facts)

    process = ""  # 存储推导过程
    res = ""  # 存储推导结果

    for f in db_facts:
        print("f",temp_db)
        if f in temp_db:
            ans = db_res[db_facts.index(f)]
            # db_res 是由 list 组成的list
            for i in ans:
                temp_db.add(i)
            res = ans
            process += "{fact}-->{ans}\n".format(fact='，'.join(f), ans=ans)

    if res == "":
        confirm_list = []
        # seems we cannot figure a exist conclusion
        for f in db_facts:
            if len(set(f) & temp_db) > 0:
                for element in f:
                    if element not in temp_db:
                        confirm_list.append(element)
        return confirm_list, ""  # make sure res is empty for confirmation
    else:
        # yeah! we find a conclusion
        return process, res
