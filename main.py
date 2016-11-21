# A Solution of Winograd Schema Challenge
# Author: LIU Boyu
# Reference: Resolving Complex Cases of Definite Pronouns: The Winograd Schema Challenge.
# Altaf Rahman and Vincent Ng.
# Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP-CoNLL), pp. 777-789, 2012.

import os
import json
import re
import requests
from bs4 import BeautifulSoup
import random
import time


def google_search(q):
    # t = random.uniform(0, 1)
    # time.sleep(t)
    r = requests.get('http://www.bing.com/search',
                     params={'q': '"' + q + '"',
                             "tbs": "li:1"}
                     )

    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        resultstr = soup.find('div', {'id': 'b_tween'}).text
    except Exception:
        return 0
    try:
        return int(re.sub("[^0-9]", "", resultstr))
    except ValueError:
        return 0


def pick_by_google(p1, p2, pron, c0, c1, i):

    for token in p1["sentences"][0]["tokens"]:
        if token["word"] in c0 and token["ner"] == "PERSON":
            return pick_by_nc(p1, p2, pron, c0, c1, i)
        elif token["word"] in c1 and token["ner"] == "PERSON":
            return pick_by_nc(p1, p2, pron, c0, c1, i)

    q0 = sent2[i].replace(pron, c0)
    num0 = google_search(q0)
    q1 = sent2[i].replace(pron, c1)
    num1 = google_search(q1)
    print(" %s: %d; %s: %d" % (q0, num0, q1, num1))
    if num0 > num1 * 1.2:  # *5 and num1!=0 :
        return c0
    elif num1 > num0 * 1.2:  # *5 and num1!=0:
        return c1
    else:
        r = p2["sentences"][0]["enhancedDependencies"][0]["dependentGloss"]
        for token in p2["sentences"][0]["tokens"]:
            if token["word"] == r:
                if 'V' in token["pos"]:
                    q0 = c0 + " " + r
                    q1 = c1 + " " + r
                elif 'JJ' in token["pos"]:
                    q0 = r + " " + c0
                    q1 = r + " " + c1
                else:
                    for dependency in p2["sentences"][0]["enhancedDependencies"]:
                        if dependency["governorGloss"] == r and dependency["dep"] == 'cop':
                            q0 = c0 + ' ' + dependency['dependentGloss'] + ' ' + r
                            q1 = c1 + ' ' + dependency['dependentGloss'] + ' ' + r

        num0 = google_search(q0)
        num1 = google_search(q1)
        print(" %s: %d; %s: %d" % (q0, num0, q1, num1))
        if num0 > num1:  # *5 and num1!=0 :
            return c0
        elif num1 > num0:  # *5 and num1!=0:
            return c1
        else:
            return pick_by_nc(p1, p2, pron, c0, c1, i)


def check_nc(v1, v2, role_of_pron):
    total = 0
    flag = {'s': 0, 'o': 0}
    for nc_item in nc:
        if v1 in nc_item['events'] and v2 in nc_item['events']:
            # print(nc_item['events'])
            item = v2+'-'+role_of_pron
            for nc_chain in nc_item['chains']:
                if item in nc_chain:
                    for node in nc_chain:
                        if v1 == node[:-2]:
                            # if flag != node[-1] and flag != 'waiting':
                            #     return "No Decision"
                            # else:
                            #     flag = node[-1]
                            flag[node[-1]] += 1
                            total += 1
    # if flag == 'waiting':
    #     return "No Decision"
    # else:
    #     return flag
    # if flag['s'] == 0 and flag['o']==0:
    #     return "No Decision"
    # elif flag['s'] > flag['o']:
    #     return 's'
    # else:
    #     return 'o'
    # print("total: %d, s-o: %d" % (total, flag['s'] - flag['o']))
    return [total, flag['s'] - flag['o']]


def pick_by_nc(p1, p2, pron, c0, c1, i):

    r1 = []
    mark1 = []
    r2 = []
    mark2 = []

    # r1index = p1["sentences"][0]["enhancedDependencies"][0]["dependent"]
    # for token in p1["sentences"][0]["tokens"]:
    #     if token["index"] == r1index:
    #             r1 = token["lemma"]
    #
    # r2index = p2["sentences"][0]["enhancedDependencies"][0]["dependent"]
    # for token in p2["sentences"][0]["tokens"]:
    #     if token["index"] == r2index:
    #             r2 = token["lemma"]
    total = 0
    for dependency in p1["sentences"][0]["enhancedDependencies"]:
        if "subj" in dependency['dep'] and dependency['dependentGloss'] in c0:
            r1index = dependency["governor"]
            for token in p1["sentences"][0]["tokens"]:
                if token["index"] == r1index:
                    r1.append(token["lemma"])
                    if 'pass' in dependency['dep']:
                        mark1.append('pass')
                    else:
                        mark1.append('acti')

    for dependency in p2["sentences"][0]["enhancedDependencies"]:
        if "subj" in dependency['dep'] and dependency['dependentGloss'] in pron:
            r2index = dependency["governor"]
            for token in p2["sentences"][0]["tokens"]:
                if token["index"] == r2index:
                    r2.append(token["lemma"])
                    if 'pass' in dependency['dep']:
                        mark2.append('pass')
                    else:
                        mark2.append('acti')

    s_o = 0
    for p, v1 in enumerate(r1):
        for q, v2 in enumerate(r2):
            if mark2[q] == 'acti':
                pr = 's'
            else:
                pr = 'o'
            temp = check_nc(v1, v2, pr)
            total += temp[0]
            temp = temp[1]
            if mark1[p] == 'pass':
                temp = -temp
            s_o += temp
    # print("verb1: %s, verb2: %s, role: %s" % (r1, r2, role))
    if total == 0:
        return "No Decision"
    print(1.0 * s_o / total)
    if 1.0 * s_o / total > 0.3:
        return c0
    elif 1.0 * s_o / total < -0.3:
        return c1
    else:
        return "No Decision"


def pick_ans(p1, p2, pron, c0, c1, i):
    return pick_by_google(p1, p2, pron,c0,c1,i)
    # return pick_by_nc(p1, p2, pron, c0, c1, i)


sentences = []
sent1 = []
sent2 = []
conjs = []
prons = []
choice0 = []
choice1 = []
answer = []
flags = []

conjList = [' because ', ',because ', ',since ', ' since ', ' or ', ',or ',' but ', ',but ', ' after ', ',after ', ' so ', ',so ',  ' even if ', ',even if ', ' though ', ',though ',  ' and ', ',and ', ' that ', ',that']

# input the data
data = open('test.c.txt', 'r')
counter = 0
size = 0
for line in data:
    line = line.strip()
    line = line.strip('.')
    if counter % 5 == 0:
        sentences.append(line)
        flags.append('waiting')
        sent1.append("")
        sent2.append("")
        conjs.append("")
        size += 1
    elif counter % 5 == 1:
        prons.append(line)
    elif counter % 5 == 2:
        li = line.split(',')
        li[0] = li[0].replace('a ', '')
        li[1] = li[1].replace('a ', '')
        li[0] = li[0].replace('the ', '')
        li[1] = li[1].replace('the ', '')
        li[0] = li[0].replace('A ', '')
        li[1] = li[1].replace('A ', '')
        li[0] = li[0].replace('The ', '')
        li[1] = li[1].replace('The ', '')
        li[0] = li[0].replace('an ', '')
        li[1] = li[1].replace('an ', '')
        li[0] = li[0].replace('An ', '')
        li[1] = li[1].replace('An ', '')
        choice0.append(li[0])
        choice1.append(li[1])
    elif counter % 5 == 3:
        line = line.replace('a ', '')
        line = line.replace('the ', '')
        line = line.replace('A ', '')
        line = line.replace('The ', '')
        line = line.replace('an ', '')
        line = line.replace('An ', '')
        answer.append(line)
    counter += 1

data.close()

# input Narrative Chain
nc_file = open('schemas.txt', 'r')
nc = []
nc_object = {}
nc_chains = []
for line in nc_file:
    line.strip()
    if "*****" in line:
        if nc_object != {}:
            nc_object["chains"] = nc_chains
            nc.append(nc_object)
        nc_object = {}
        nc_chains = []
    elif line[:7] == "Events:":
        nc_object["events"] = line[7:].strip().split(" ")
    elif line[0] == "[":
        end = line.find("]")
        nc_chains.append(line[1:end].strip().split(" "))
if nc_object != {}:
    nc_object["chains"] = nc_chains
    nc.append(nc_object)
nc_file.close()
nc_output = open('nc_output.txt', 'w')

# print(nc)

# cut the sentence to two parts according to conjunctions
for i in range(size):
    sent = sentences[i]
    con = ""
    for conj in conjList:
        if conj in sent:
            con = conj
            break
    if con != "":
        conjs[i] = con
        subs = sent.split(con)
        sent1[i] = subs[0]
        sent2[i] = subs[1]
    else:
        flags[i] = "No Decision"


# write 2 part of sentences to batches of files with a fileList
fileList = open('fileList.txt', 'w')
subdirectory = "files"

try:
    os.system('rm -fr '+subdirectory)
    os.mkdir(subdirectory)
except Exception:
    pass

for i in range(size):
    tempf = open(os.path.join(subdirectory, str(i)+'p1.in'), 'w')
    tempf.write(sent1[i])
    fileList.write(os.path.join(subdirectory, str(i)+'p1.in')+'\n')
    tempf.close()

    tempf = open(os.path.join(subdirectory, str(i) + 'p2.in'), 'w')
    tempf.write(sent2[i])
    fileList.write(os.path.join(subdirectory, str(i) + 'p2.in') + '\n')
    tempf.close()

fileList.close()

# use Stanford CoreNLP to get the parse result
os.system('corenlp.sh -props prop.properties')

# use Stanford Resolve
srsubdirectory = "srfiles"
srfilelist = open('srFileList.txt')

try:
    os.system('rm -fr '+srsubdirectory)
    os.mkdir(srsubdirectory)
except Exception:
    pass

for i in range(size):
    tempf = open(os.path.join(srsubdirectory, str(i)+'.in'), 'w')
    tempf.write(sentences[i])
    fileList.write(os.path.join(srsubdirectory, str(i)+'.in')+'\n')
    tempf.close()

fileList.close()

os.system('corenlp.sh -props stanRes.properties')

# for each question
for i in range(size):
    if flags[i] != "No Decision":
        with open(os.path.join(subdirectory, str(i)+'p1.out'), 'r') as fp1:
            p1 = json.load(fp1)
        with open(os.path.join(subdirectory, str(i)+'p2.out'), 'r') as fp2:
            p2 = json.load(fp2)
        ans = pick_ans(p1, p2, prons[i], choice0[i], choice1[i], i)
        # print(ans)
        flags[i] = ans

# print(check_nc("give", "want", 's'))


# evaluation
correct = 0
wrong = 0
noDecision = 0
print(flags)
print(answer)
for i in range(size):
    if flags[i] == 'No Decision':
        noDecision += 1
    elif flags[i] == answer[i]:
        correct += 1
    else:
        wrong += 1
print("Total data: %d, Correct: %f, Wrong: %f, No Decision: %f, error: %f" % (size, 1.0*correct*100/size, 1.0*wrong*100/size, 1.0*noDecision*100/size, 1.0*(wrong+noDecision/2)/size))