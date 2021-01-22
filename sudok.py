#!/usr/bin/env python
# coding: utf-8

# In[1]:


#数独求解

import numpy as np
import copy

puzzle = np.array(
    [[5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]])

#盘面分块
def piece_get():
    piece = [[x,y] for x in range(9) for y in range(9)]
    piece_rows = [piece[:27],piece[27:54],piece[54:]]
    piece_cut = []
    for row_piece in piece_rows:
        for i in [0,3,6]:
            piece_cut.append(row_piece[i :i+3]+row_piece[i+9:i+12]+row_piece[i+18:i+21])
    return piece_cut

#现有数字的位置字典
def crt_dic_num(puzzle):
    dic_num = {i:np.where(puzzle==i) for i in range(10)}
    dic_num2 ={}
    for i in range(10):
        dic_num2[i] = []
        for x,y in [[dic_num[i][0][j],dic_num[i][1][j]] for j in range(len(dic_num[i][0]))]:
            dic_num2[i].append([x,y]) 
    return dic_num2

#建立预期数字可能存在的坐标字典
def crt_dic_num_p(dic_num2,piece_cut):
    dic_num_p = {}
    for i in range(1,10):
        dic_num_p[i] = copy.deepcopy(piece_cut)
        for block in piece_cut:
             for x,y in dic_num2[i]:
                if [x,y] in block:
                    dic_num_p[i].remove(block)
                    break
    return dic_num_p

#清除块和横纵坐标不可能存在的位置
def exclude_1(dic_num_p,dic_num,num):
    for x,y in dic_num[num]:
        for block in dic_num_p[num]:
            for site in block:
                if x == site[0] or y==site[1] :
                    site.clear()
            while [] in block:
                block.remove([])
    return dic_num_p

#清除非空位置
def exclude_2(dic_num_p, dic_num, num):
    for block in dic_num_p[num]:
        #others = []
        for site in block:
            if site not in dic_num[0]:
                #others.append([x,y])
                site.clear()
        while [] in block:
            block.remove([])
    return dic_num_p

#去除所有3*3块中所有不可能位置
def exclude(dic_num_p,dic_num):
    for num in range(1,10):
        dic_num_p = exclude_1(dic_num_p, dic_num, num)
        dic_num_p = exclude_2(dic_num_p, dic_num, num)
    return dic_num_p

def block_fill_update(num_p_dic,num_dic):
    for num in range(1,10):
        for block in num_p_dic[num]:
            if len(block) == 1:
                num_dic[0].remove(block[0])            
                num_dic[num].append(block.pop())
        while [] in num_p_dic[num]:
            num_p_dic[num].remove([])
            exclude(num_p_dic,num_dic)
            block_fill_update(num_p_dic,num_dic)
    return

#初始化并简单排除
def main(puzzle):
    num_dic = crt_dic_num(puzzle)
    num_p_dic = crt_dic_num_p(num_dic,piece_get())
    dic_num_p = exclude(num_p_dic, num_dic)
    block_fill_update(num_p_dic,num_dic)
    print(num_dic)
    
if __name__ == "__main__":
    main(puzzle)
    
