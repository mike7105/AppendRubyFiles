# -*- coding: utf-8 -*-
import os
import glob
import shutil
import time

t1 = time.time()
path_prev = r"L:\convert\RUBY\CaseData" # r"O:\Progs\Python\AppendRubyFiles\examples\wave1-2"
path_curr = r"L:\convert\RUBY\CaseData2" # r"O:\Progs\Python\AppendRubyFiles\examples\wave3"
path_res = r"L:\convert\RUBY\CaseData3" # r"O:\Progs\Python\AppendRubyFiles\examples\wave1-3"
num_prev = 0
num_same = 0
num_new = 0

# копирую все файлы met
for met_file in glob.glob(path_curr + "\\*.met"):
    shutil.copy(met_file, path_res)

# считает кол-во строк в файле
def count_lines(filename, chunk_size=1<<13):
    with open(filename) as file:
        chunk = '\n'
        nlines = 0
        for chunk in iter(lambda: file.read(chunk_size), ''):
            nlines += chunk.count('\n')
    return nlines + (not chunk.endswith('\n'))

# прохожусь по всем cd файлам path_curr
for cd_file_c in glob.glob(path_curr + "\\*.cd"):
    cd_file_p = os.path.join(path_prev,os.path.split(cd_file_c)[1])
   
    # если в path_prev есть такой же файл, то его окпирую и 
    # дописываю содержимым файла из path_curr
    if os.path.exists(cd_file_p):
        num_same += 1
        if num_prev == 0:
            num_prev = count_lines(cd_file_p)

        cd_file_r = shutil.copy(cd_file_p, path_res)

        with open(cd_file_c, 'rb') as fsrc:
            with open(cd_file_r, 'ab') as fdst:
                shutil.copyfileobj(fsrc, fdst)

    # если файла нет, то нужно создать пустой с определенным кол-вом строк
    else:
        num_new += 1
        if num_prev == 0:
            num_prev = count_lines(os.path.join(path_prev,"id.cd"))

        cd_file_r = os.path.join(path_res,os.path.split(cd_file_c)[1])

        with open(cd_file_r,'w') as f:
            f.write('\n' * num_prev)

        with open(cd_file_c, 'rb') as fsrc:
            with open(cd_file_r, 'ab') as fdst:
                shutil.copyfileobj(fsrc, fdst)
t2 = time.time()
tr=t2-t1
print ("same files {0:>5}\nnew files {1:>5}\nduration {2:>10.3f}".format(num_same, num_new, tr))
input ("___")