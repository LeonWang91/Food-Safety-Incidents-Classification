from multiprocessing.dummy import Pool
from sklearn import svm
import numpy as np
import os
import baseio
from gensim.models import Word2Vec
import joblib
from sklearn.metrics import classification_report, accuracy_score


def build_vec(list_sentence, model):
    list_vec_sentence = []
    for sentence in list_sentence:
        if len(sentence) > 1000:
            arrlists = [model[word] for word in sentence[0:1000]]
            x = np.average(arrlists, axis=0)
        else:
            arrlists = [model[word] for word in sentence]
            x = np.average(arrlists, axis=0)
        list_vec_sentence.append(x)
    return list_vec_sentence


def main(i, do_train, do_test):
    x = int(i)
    path = "10-fold-SVM\\" + i 

    train_text = baseio.readtxt_list_all_strip(path + "/train.txt")
    list_sentence_train_mid = [_.split("\t")[1].replace("  "," ") for _ in train_text]
    list_sentence_train = [_.split() for _ in list_sentence_train_mid]
    tag_train = [_.split("\t")[0] for _ in train_text]

    test_text = baseio.readtxt_list_all_strip(path + "/dev.txt")
    list_sentence_test_mid = [_.split("\t")[1] for _ in test_text]
    list_sentence_test = [_.split() for _ in list_sentence_test_mid]
    tag_test = [_.split("\t")[0] for _ in test_text]

    a = list_sentence_train + list_sentence_test
    print("开始创建model")
    if not os.path.exists("vec_model/" + i + ".model"):
        model = Word2Vec(a, sg=1, size=50, min_count=0)
        model.save("vec_model/" + i + ".model")
    else:
        model = Word2Vec.load("vec_model/" + i + ".model")
    print("model创建完毕")
    vec_sentence_train = build_vec(list_sentence_train, model)
    print("vec_sentence创建完毕")
    #####train
    clf = svm.SVC(C=2.0, kernel='rbf', gamma=0.5)
    if not os.path.exists("svm_model/" + i + ".model"):
        clf.fit(np.array(vec_sentence_train), np.array(tag_train))
        filename = joblib.dump(clf, "svm_model/svm_model_" + i + ".m")
        print(filename)
    else:
        clf = joblib.load("svm_model/svm_model_" + i + ".m")
    print("训练结束")

    ####test

    # clf = joblib.load("save_model/svm_model_" + i +".m")
    correct = 0
    wrong = 0
    # model = Word2Vec.load("vec_model/" + i + ".model")
    vec_test_sentence = build_vec(list_sentence_test, model)
    cata_pre, cata_real = clf.predict(np.array(vec_test_sentence)) , tag_test

    print(cata_pre)
    print(cata_real)
    target_names = ['__label__0', '__label__1', '__label__2', '__label__3']
    print(classification_report(cata_pre, cata_real, target_names=target_names, digits=8))
    print("accuracy\t", accuracy_score(cata_pre, cata_real))
    #     if result == tag_test[j]:
    #         correct += 1
    #     else:
    #         wrong += 1
    # print(correct/(correct+wrong))
    # with open("result/" + i + ".txt","w") as w:
    #     w.write(str(correct) + "\t" + str(wrong) + "\t" + str(correct/(correct+wrong)))

    # def calc_single_label(label):
    #     tt, tf, ff, ft = 0, 0, 0, 0
    #     for i in range(len(cata_real)):
    #         real = cata_real[i]
    #         pre = cata_pre[i]
    #         if real == label:
    #             if pre == label:
    #                 tt += 1
    #             else:
    #                 tf += 1
    #         else:
    #             if pre == label:
    #                 ft += 1
    #             else:
    #                 ff += 1
    #     p = tt / (tt + ft)  if(tt + ft)  else 0
    #     r = tt / (tt + tf)  if(tt + tf)  else 0
    #     f = 2 * p * r / (p + r)  if(p + r)  else 0
    #     return p, r, f
    # bp, br, bf = calc_single_label("0")
    # pp, pr, pf = calc_single_label("1")
    # rp, rr, rf = calc_single_label("2")
    # cp, cr, cf = calc_single_label("3")
    # avg_p = (bp + pp + rp + cp) / 5
    # avg_r = (br + pf + rr + cr) / 5
    # avg_f = 2 * avg_p * avg_r / (avg_p + avg_r) if(avg_p+avg_r) else 0
    # print(i + "\t" + str(avg_p*100) + '\t' + str(avg_r*100) + "\t" + str(avg_f*100))
    # baseio.writetxt_w(i + "\t" + str(avg_p*100) + '\t' + str(avg_r*100) + "\t" + str(avg_f*100), "result/" + i + '.txt')



if __name__ == '__main__':
    if not os.path.exists("vec_model"):
        os.mkdir("vec_model")
    if not os.path.exists("svm_model"):
        os.mkdir("svm_model")
    if not os.path.exists("result"):
        os.mkdir("result")
    # pool = Pool()
    # excs = [str(i) for i in range(1, 11)]
    # pool.map(main, excs)
    for i in range(10): # 文件名的序号,如有data_1 data_2 data_3...多个数据集(通常在跑10折交叉时用到),只需修改区间(1,2)
        main(str(i), do_train=True, do_test=True)
