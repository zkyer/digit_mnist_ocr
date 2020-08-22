# digit_Mnist_OCR

## 介绍
Tesseract v5.0 +Mnist数据集 LSTM训练，为减小文件大小，删除了不需要的中间文件，需要可按教程生成

--------------------------------
## 文件夹说明

   digit_W	白字黑底数据版本

   digit_B	白底黑字数据版本

--------------------------------
## 项目总操作步骤（详见‘训练及测试文档.docx‘）

### 一.creat_data文件夹下操作

   获取图像数据（data_test/、data_train/）：使用creat_data/creat_data.py 
 
### 二.data_merge文件夹下操作
#### 1.获取合并数据（mergeData_train/、mergeData_test）：

   使用 `data_merge/pro_mergeImg/merge_img.py` 

   同时生成合并数据数字序列字典（ Dict/ ），用于判断正确率及纠正box文件

#### 2.合成tif
   使用jTessBoxEditor，合成tif放 mergeTif/

#### 3.命令行生成box（ mergeTif/目录下运行）

```
tesseract num.mnist.exp0.tif num.mnist.exp0 -l eng --psm 6 lstmbox
tesseract num_test.mnist.exp0.tif num_test.mnist.exp0 -l eng --psm 6 lstmbox
```
#### 4.对box文件矫正（三种方法）
   jTessBoxEditor矫正、直接打开box文件矫正、 程序矫正 check_box.py

#### 5.命令行生成lstmf文件用于训练/测试（ mergeTif/目录下运行）
```
cd .. & md lstmf & cd mergeTif
tesseract num.mnist.exp0.tif ../lstmf/num.mnist.exp0 -l eng --psm 6 lstm.train
tesseract num_test.mnist.exp0.tif ../lstmf/num_test.mnist.exp0 -l eng --psm 6 lstm.train
```

### 三.train文件夹下操作 
#### 1.从已有.traineddata文件中提取.lstm文件
   从[https://github.com/tesseract-ocr/tessdata_best](https://github.com/tesseract-ocr/tessdata_best) 对应语言例如这里是eng提取

   命令行：`combine_tessdata -e eng.traineddata eng.lstm`
#### 2.训练
   创建txt 写入.lstmf文件路径，命令行：`set /p =..\data_merge\lstmf\num.mnist.exp0.lstmf<nul>eng.training_files.txt`

   训练命令行：`lstmtraining --debug_interval -1 --max_iterations 6000 --target_error_rate 0.01 --continue_from=".\eng.lstm"  --model_output=".\output\output" --train_listfile=".\eng.training_files.txt" --traineddata=".\eng.traineddata"`  

   随着训练均方根、Δ、train（错误率）都会下降，结束会显示finish

#### 3.合并模型
   将checkpoint文件和.traineddata文件合并成新的.traineddata文件

   命令行：`lstmtraining --stop_training --traineddata=".\eng.traineddata" --continue_from=".\output\output_checkpoint"  --model_output=".\output\mnist_aug2.traineddata"`

#### 4.完成，开始测试
   两种测试方式，1.利用测试集进行测试，2.将新生成的语言包导入安装路径进行实际的文字识别。

   ------------------------------
   *测试方式1：测试集测试

   ①生成测试集.lstmf文件，前边已生成到 `data_merge\lstmf\num_test.mnist.exp0.lstmf`

   ②创建写有 .lstmf文件路径的txt文件（train/目录下执行）：

   命令行：`set /p =..\data_merge\lstmf\num_test.mnist.exp0.lstmf<nul>eng.test_files.txt `

   ③测试（train/目录下执行）

   `lstmeval --model=".\output\mnist.traineddata" --eval_listfile=".\eng.test_files.txt"`
  