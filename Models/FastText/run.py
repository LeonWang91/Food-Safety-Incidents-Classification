# -*- coding: utf-8 -*-
# @Time    : 2021/2/17 0017 19:43
# @Author  : Wang
# @FileName: train_test.py
# @Software: PyCharm


import os
import baseio
import numpy as np
from tqdm import tqdm
# import FastText as fasttext
import fasttext.FastText as fasttext
from collections import defaultdict
from sklearn.metrics import classification_report, accuracy_score


def train_model(ipt=None, opt=None, model='', dim=100, epoch=5, lr=0.1, loss='softmax'):
    # suppress: bool, 科学记数法启用
    # True用固定点打印浮点数符号，当前精度中的数字等于零将打印为零。
    # False用科学记数法；最小数绝对值是<1e-4或比率最大绝对值> 1e3。默认值False
    np.set_printoptions(suppress=True)
    if os.path.isfile(model):
        classifier = fasttext.load_model(model)
    else:
        classifier = fasttext.train_supervised(ipt, label='__label__', dim=dim, epoch=epoch,
                                               lr=lr, wordNgrams=2, loss=loss)
        """
          训练一个监督模型, 返回一个模型对象

          @param input:           训练数据文件路径
          @param lr:              学习率
          @param dim:             向量维度
          @param ws:              cbow模型时使用
          @param epoch:           次数
          @param minCount:        词频阈值, 小于该值在初始化时会过滤掉
          @param minCountLabel:   类别阈值，类别小于该值初始化时会过滤掉
          @param minn:            构造subword时最小char个数
          @param maxn:            构造subword时最大char个数
          @param neg:             负采样
          @param wordNgrams:      n-gram个数
          @param loss:            损失函数类型, softmax, ns: 负采样, hs: 分层softmax
          @param bucket:          词扩充大小, [A, B]: A语料中包含的词向量, B不在语料中的词向量
          @param thread:          线程个数, 每个线程处理输入数据的一段, 0号线程负责loss输出
          @param lrUpdateRate:    学习率更新
          @param t:               负采样阈值
          @param label:           类别前缀
          @param verbose:         ??
          @param pretrainedVectors: 预训练的词向量文件路径, 如果word出现在文件夹中初始化不再随机
          @return model object
        """
        classifier.save_model(opt)
    return classifier


def cal_precision_and_recall(file=''):
    # 当字典里的key不存在但被查找时，返回的不是keyError而是一个默认值
    precision = defaultdict(int)
    recall = defaultdict(int)
    total = defaultdict(int)
    lines = baseio.readtxt_list_all_strip(file)
    for line in tqdm(lines):
        label, content = line.split('\t', 1) # only one
        # print(label)
        total[label.strip().strip('__label__')] += 1
        prelabel = classifier.predict(content.strip())
        # print(sublabel)
        pre_label = prelabel[0][0]
        sim = prelabel[1][0]
        # print(pre_label)
        # print(sim)
        recall[pre_label.strip().strip('__label__')] += 1

        if label.strip() == pre_label.strip():
            precision[label.strip().strip('__label__')] += 1
        else:
            unmatch = pre_label.strip() + '\t' + '|' + '\t' + line + '\n'
            baseio.writetxt_a(unmatch, 'unmatch_classification.txt')

    print('precision', precision)
    print('recall', recall)
    print('total', total)
    print('\t\t\t\tprecision\trecall\t\tf1-score\tsupport\n')
    for sub in precision:
        p = precision[sub] / total[sub]
        r = precision[sub] / recall[sub]
        f1 = (2 * p * r) / (p + r)
        s = recall[sub]
        __label__ = '__label__' + str(sub)
        print(f"{__label__}\t\t{p:>.4f}\t\t{r:>.4f}\t\t{f1:>.4f}\t\t{s:>}")


def report(file='', unmatch_path=''):
    rawlabel = []
    prelabel = []
    lines = baseio.readtxt_list_all_strip(file)
    for line in tqdm(lines):
        label, content = line.split('\t', 1)  # only one
        # print(label)
        rawlabel.append(int(label.strip().strip('__label__')))
        prematrix = classifier.predict(content.strip())
        pre_label = prematrix[0][0]
        prelabel.append(int(pre_label.strip().strip('__label__')))
        if label.strip() != pre_label.strip():
            unmatch = pre_label.strip() + '\t' + '|' + '\t' + line + '\n'
            baseio.writetxt_a(unmatch, unmatch_path)
    print(rawlabel)
    print(prelabel)
    # labels = [1, 2, 3, 4]
    # target_names = ['__label__1', '__label__2', '__label__3', '__label__4', '__label__5']
    target_names = ['__label__0', '__label__1', '__label__2', '__label__3']
    print(classification_report(rawlabel, prelabel, target_names=target_names, digits=8))
    print("accuracy\t", accuracy_score(rawlabel, prelabel))


if __name__ == '__main__':
    dim = 200
    lr = 1e-3
    epoch = 30
    # f'string' 相当于 format() 函数
    # model = f'model/data_dim{str(dim)}_lr0{str(lr)}_iter{str(epoch)}.model'
    model = f'model/data_dim{str(dim)}_lr0{str(lr)}_iter{str(epoch)}.model'

    # train_path = 'data/train.txt'
    # test_path = 'data/test.txt'
    for i in range(0, 1):
        train_path = '10-fold-FastText/' + str(i) + '/train.txt'
        test_path = '10-fold-FastText/' + str(i) + '/test.txt'
        # unmatch_path = f'unmatch_classification/unmatch_classification_dim{str(dim)}_lr0{str(lr)}_iter{str(epoch)}.txt'
        unmatch_path = f'unmatch_classification/unmatch_classification_dim{str(dim)}_lr0{str(lr)}_iter{str(epoch)}.txt'

        classifier = train_model(ipt=train_path,
                                 opt=model,
                                 model=model,
                                 dim=dim, epoch=epoch, lr=0.5
                                 )

        # cal_precision_and_recall(test_path)
        report(test_path, unmatch_path)
        # result = classifier.test(test_path)
        # print(result)
        # p = result[1]
        # r = result[2]
        # f1 = 2 * p * r / (p + r)
        # s = result[0]
        # print(f'\n__label__\t\t{p:>.4f}\t\t{r:>.4f}\t\t{f1:>.4f}\t\t{s:>}')


# 整体的结果为(测试数据量，precision，recall)：
# (9885, 0.9740010116337886, 0.9740010116337886)
