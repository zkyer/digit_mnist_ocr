
##将mnist数据集前350张图做训练数据，后150张做测试数据
#训练数据放在new_trainImg_path/[label]/[sortNum].jpg
#测试数据放在new_testImg_path/[label]_[sortNum].jpg
#使用说明：
#   路径可修改两个 path


import cv2
import os
import numpy as np

ori_img =cv2.imread('ori_train_img.png',0)
ret,ori_img=cv2.threshold(ori_img,100,250,cv2.THRESH_BINARY_INV)#字体变黑
cv2.imshow('threshold',ori_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

new_trainImg_path =  '../data_train/'
new_testImg_path =  '../data_test/'

def main():
    #创建目录
    if not os.path.exists(new_trainImg_path):   os.mkdir(new_trainImg_path)
    if not os.path.exists(new_testImg_path):    os.mkdir(new_testImg_path)
    for i in range(10):
        if not os.path.exists(new_trainImg_path+'/'+str(i)): os.mkdir(new_trainImg_path+'/'+str(i))

    print('开始获取数据...')
    for row in range(50):
        for col in range(100):
            img=ori_img[row*20:(row+1)*20, col*20:(col+1)*20] #截取单幅图像
            
            #前350张图做训练数据，后150张做测试数据
            if( row%5*100+col < 350 ):  cv2.imwrite(new_trainImg_path+str(row//5)+'/'+str(row%5*100+col)+'.jpg',img)
            else:                   cv2.imwrite(new_testImg_path+str(row//5)+'_'+str(row%5*100+col-350)+'.jpg',img)
    print('数据已保存到:',new_trainImg_path,'、',new_testImg_path)
    input()

if __name__=='__main__':
    main()
         


























