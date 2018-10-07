# coding=utf-8
import sys
PATH = "database.txt"

# 判断list中至少有一个在集合set中
def ListOneInSet(li, se):
    for i in li:
        if i in se:
            return True
    return False

# 判断list中所有元素是否都在集合set中
def ListInSet(li, se):
    for i in li:
        if i not in se:
            return False
    return True

# 将知识库做拓扑排序
def topological():
    # if P then Q
    Q = []
    P = []
    ans = ""  # 排序后结果
    for line in open(PATH,encoding='utf-8'):
        line = line.strip('\n')
        if line == '':
            continue
        line = line.split(' ')
        Q.append(line[len(line) - 1])
        line.pop()
        P.append(line)

    # 计算入度
    inn = []
    for i in P:
        sum = 0
        for x in i:
            if Q.count(x) > 0:  # 能找到，那么
                sum += Q.count(x)
        inn.append(sum)

    while (1):
        x = 0
        if inn.count(-1) == len(inn):
            break
        for i in inn:
            if i == 0:
                str = ' '.join(P[x])
                # print("%s %s" %(str, Q[x]))
                ans = ans + str + " " + Q[x] + "\n"  # 写入结果
                # print("%s -- %s" %(P[x],Q[x]))
                inn[x] = -1
                # 更新入度
                y = 0
                for j in P:
                    if j.count(Q[x]) == 1:
                        inn[y] -= 1
                    y += 1
            x += 1
    print(ans)

    # 将结果写入文件
    fw = open(PATH, 'w', buffering=1,encoding="utf-8")
    fw.write(ans)
    fw.flush()
    fw.close()

# 正向推理 Flag表示是否 无结果
def go(lines, flag=True):
    # 将产生式规则放入规则库中
    # if P then Q
    # 读取产生式文件
    Q = []
    P = []
    fo = open(PATH, 'r', encoding='utf-8')
    for line in fo:
        line = line.strip('\n')
        if line == '':
            continue
        line = line.split(' ')
        Q.append(line[len(line) - 1])
        line.pop()
        P.append(line)
    fo.close()


    print("开始正向推理")

    # 检测输入是否是utf8编码，减少乱码对程序的影响
    if type(lines)!=str:
        lines=lines.decode('utf8')
    lines = lines.split(' ')  # 按回车分割成组
    DB = set(lines) # 去重
    #print(DB)
    string = "" # 存储推导过程
    # print(string)
    # flag = True
    temp = "" # 存储推导结果

    for x in P:  # 对于每条产生式规则
        if ListInSet(x, DB):  # 如果所有前提条件都在规则库中
            DB.add(Q[P.index(x)])
            temp = Q[P.index(x)] # 得出了结论
            flag = False  # 至少能推出一个结论
            # print("%s --> %s" %(x, self.Q[self.P.index(x)]))
            string += "%s --> %s\n" % ('，'.join(x), Q[P.index(x)])

    # s = SecondWindow()
    if flag:  # 一个结论都推不出
        # print("Oops no Conclusion")
        # print(P)
        for x in P:  # 对于每条产生式
            if ListOneInSet(x, DB):  # 事实是否满足部分前提
                flag1 = False  # 默认提问时否认前提
                for i in x:  # 对于前提中所有元素
                    if i not in DB:  # 对于不满足的那部分，询问用户是否存在
                        # btn = s.quest("是否" + i)
                        print("是否 " + i)
                        return "是否 " + i,""
                        # if btn == "1":
                        #     # self.textEdit.setText(self.textEdit.toPlainText() + "\n" + i)  # 确定则增加到textEdit
                        #     DB.add(i)  # 确定则增加到规则库中
                        #     flag1 = True  # 肯定前提
                        #     # self.go(self)
                if flag1:  # 如果肯定前提，则重新推导
                    string, temp=go(' '.join(DB))
                    return string, temp

    # print("----------------------")
    # print(string)
    if flag:
        print("找不到结论")
        return string,temp
        # btn = print("Oops I cannot figure out a Conclusion!!!")
        # # if btn == QtWidgets.QMessageBox.Ok:  # 点击确定
        # #     self.textEdit.setText(self.textEdit.toPlainText() + "\n确定")
    else:
        # 有结果，就返回
        print(temp)
        return string,temp

# 反向推理，就是正向推理反过来
def reverse(lines,flag=True):
    print("开始反向推理")
    if type(lines)!=str:
        lines=lines.decode('utf8')
    lines = lines.split(' ')  # 分割成组
    DB = set(lines)

    Q = []
    P = []
    fo = open(PATH, 'r', encoding='utf-8')
    for line in fo:
        line = line.strip('\n')
        if line == '':
            continue
        line = line.split(' ')
        Q.append(line[:-1])
        P.append([line[-1]])
    fo.close()

    print("DB: "+str(DB))
    string = ""
    print(P)
    print(Q)
    # print(string)
    # flag = True
    temp = ""
    for x in P:  # 对于每条产生式规则
        if ListInSet(x, DB):  # 如果所有前提条件都在规则库中
            DB.add(i for i in Q[P.index(x)])
            temp = Q[P.index(x)]
            flag = False  # 至少能推出一个结论
            # print("%s --> %s" %(x, self.Q[self.P.index(x)]))
            string += "%s --> %s\n" % (x, Q[P.index(x)])

    # s = SecondWindow()
    if flag:  # 一个结论都推不出
        print("Oops no Conclusion")
        print(P)
        for x in P:  # 对于每条产生式
            if ListOneInSet(x, DB):  # 事实是否满足部分前提
                flag1 = False  # 默认提问时否认前提
                for i in x:  # 对于前提中所有元素
                    if i not in DB:  # 对于不满足的那部分
                        # btn = s.quest("是否" + i)
                        print("是否(0/1) " + i)
                        return "是否(0/1) " + i,""
                        # if btn == "1":
                        #     # self.textEdit.setText(self.textEdit.toPlainText() + "\n" + i)  # 确定则增加到textEdit
                        #     DB.add(i)  # 确定则增加到规则库中
                        #     flag1 = True  # 肯定前提
                        #     # self.go(self)
                if flag1:  # 如果肯定前提，则重新推导
                    go(' '.join(DB))
                    return

    # self.textEdit_2.setPlainText(self.str)
    print("----------------------")
    print(string)
    if flag:
        btn = print("Oops I cannot figure out a Conclusion!!!")
        # if btn == QtWidgets.QMessageBox.Ok:  # 点击确定
        #     self.textEdit.setText(self.textEdit.toPlainText() + "\n确定")
    else:
        print(temp)


if __name__ == '__main__':
    topological()
    reverse(input().encode(sys.stdin.encoding))
