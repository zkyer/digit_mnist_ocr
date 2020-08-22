##通过字典文件矫正box
#   原文件重命名为 old_[name].box，新建原名文件用于保存矫正后box
#   实现思路详见 check_box()
##使用说明：
#   修改 boxName
#   修改 mode和 mImgNum 
#   如有需要可以修改 imgNum
import cv2
import os
import numpy as np
import random
import pickle

def check_box( boxName, mImgNum, mode, numNum=10):
    '''
    ----------------------------------------------------------------
    *思路
    lstm对图片每行都生成一‘\t’标志行到box，
    故box文件中，n行数字行后接一标志行。（打开box看就知）
    将原box文件中数字行第一个字符替换成字典文件对应的数字。
    若识别出的数字数小于numNum，则补行
    若识别出的数字数大于numNum，则删行
    由于不能在原文件上读写操作（麻烦不方便），
    故创建一个新的box文件用于转存
    ----------------------------------------------------------------
    *参数说明：
    boxName           box文件名
    mImgNum           tif 中图像数目
    mode              文件模式， 'train'/ 'test'
    numNum            每张图像中数字数目，默认10
    ----------------------------------------------------------------
    '''     
    #读字典，用于矫正box
    with open('./Dict/merge_numDic_'+mode+'.pkl', 'rb') as f:
        dic = pickle.load(f)

    #旧文件重命名
    old_box = 'mergeTif/' + 'old_'+boxName
    if os.path.exists(old_box):         os.remove(old_box)        
    os.rename( 'mergeTif/'+boxName, old_box )
    
    #打开原box文件
    with open( 'mergeTif/'+'old_'+boxName, 'rb') as box:
        #打开新box文件用于转存box
        with open( 'mergeTif/'+boxName,'w') as check_box:
            #每张图片应对应numNum个数字行+ \t行，多余的删除，少则补
            print( '开始纠正'+boxName )
            for imgIndex in range(mImgNum):
                for numOrd in range(numNum):                        #numNum行内的数字行，修改后存入
                    line=box.readline()
                    
                    if(line[0] == 9):                               #数字行少于numNum，进行补行并退出（'\t'对应utf-8编码为9）
                        #print(imgIndex,'补行')
                        #补行
                        for l in range(numNum-numOrd):
                            check_box.write(dic[imgIndex][numOrd+l]+line[1:].decode())
                        break

                    #替换首字符编码，纠正识别结果
                    for label in range(1,4):
                        if(line[label]==32): break                  #空格对应utf-8编码为32,不同字符utf-8编码长度不同
                    line = dic[imgIndex][numOrd].encode() + line[label:]
                    check_box.write(line.decode())                            
                else:                   line=box.readline()

                while line[0] != 9:     line=box.readline()         #识别出的数字数大于等于numNum，去除多余行（'\t'对应utf-8编码为9）
                else:                   check_box.write(line.decode())
    

if __name__ == '__main__':
    #纠正 num.mnist.exp0.box
    check_box( boxName = 'num.mnist.exp0.box'
               , mImgNum = 350, mode = 'train')
    #纠正 num_test.mnist.exp0.box
    check_box( boxName = 'num_test.mnist.exp0.box'
               , mImgNum = 150, mode = 'test')
    input('已纠正完成！按回车退出...')





