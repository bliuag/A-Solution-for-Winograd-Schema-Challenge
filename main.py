# A Solution of Winograd Schema Challenge
# Author: LIU Boyu
# Reference: Resolving Complex Cases of Definite Pronouns: The Winograd Schema Challenge.
# Altaf Rahman and Vincent Ng.
# Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP-CoNLL), pp. 777-789, 2012.

import os

sentences = []
sent1 = []
sent2 = []
conjs = []
prons = []
choice0 = []
choice1 = []
answer = []
flags = []
conjList = [' because ', ',because ', ' and ', ',and ', ' or ', ',or ',' but ', ',but ', ' after ', ',after ', ' so ', ',so ',  ' even if ', ',even if ', ' though ', ',though ', ' that ', ',that']

# input the data
data = open('train.c.txt', 'r')
counter = 0
size = 0
for line in data:
    line = line.strip()
    if counter % 5 == 0:
        sentences.append(line)
        size += 1
    elif counter % 5 == 1:
        prons.append(line)
    elif counter % 5 == 2:
        li = line.split(',')
        choice0.append(li[0])
        choice1.append(li[1])
    elif counter % 5 == 3:
        answer.append(line)
    counter += 1
    flags.append('waiting')
    sent1.append("")
    sent2.append("")
    conjs.append("")
data.close()

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
# os.system('corenlp.sh -props prop.properties')
