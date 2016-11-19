# A Solution of Winograd Schema Challenge
# Author: LIU Boyu
# Reference: Resolving Complex Cases of Definite Pronouns: The Winograd Schema Challenge.
# Altaf Rahman and Vincent Ng.
# Proceedings of the 2012 Joint Conference on Empirical Methods in Natural Language Processing and Computational Natural Language Learning (EMNLP-CoNLL), pp. 777-789, 2012.

import os

sentences = []
prons = []
choice0 = []
choice1 = []
answer = []
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
data.close()
#write sentences to batches of files with a fileList
fileList = open('fileList.txt', 'a')
subdirectory = "files"
try:
    os.mkdir(subdirectory)
except Exception:
    pass
for i in range(size):
    tempf = open(os.path.join(subdirectory, str(i)+'.txt'), 'w')
    tempf.write(sentences[i])
    fileList.write(str(i)+'.txt\n')
    tempf.close()
fileList.close()
