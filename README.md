

# Food-Safety-Incidents-Classification

[![standard-readme compliant](https://img.shields.io/badge/Food%20Safety%20Incidents-Classification-brightgreen.svg?style=flat)](https://github.com/LeoWang91/Food-Safety-Incidents-Classification)

We captured all the news reports of food safety incidents in 11 years from January 2007 to December 2017 and finally constructed a food safety incidents corpus containing 4156 reports after automatic de-duplication. Based on the corpus, a classification model for food safety incidents is constructed by training SVM,  BERT and FastText models.

The following is a description of the datasets and models in this project.


## Table of Contents

- [1.Datasets](#1.Datasets)
  - [1.1Introduction](#1.1Introduction)
  - [1.2.Preprocessing](#1.2.Preprocessing)
- [2.Models](#2.Models)
  - [2.1.SVM](#2.1.SVM)
    - [2.1.1.About](#2.1.1.About)
    - [2.1.2.Usage](#2.1.2.Usage)
    - [2.1.3.Result](#2.1.3.Result)
  - [2.2.BERT](#2.2.BERT)
    - [2.2.1.About](#2.2.1.About)
    - [2.2.2.Usage](#2.2.2.Usage)
    - [2.2.3.Result](#2.2.3.Result)
  - [2.3.FastText](#2.3.FastText)
    - [2.3.1.About](#2.3.1.About)
    - [2.3.2.Usage](#2.3.2.Usage)
    - [2.3.3.Result](#2.3.3.Result)
- [3.Conclusion](#3.Conclusion)

## 1.Datasets

### 1.1Introduction

The corpus required for this experiment comes from six websites that reported food safety events comprehensively, such as "China food safety network" and so on. By using the crawler tool developed by python, we captured all the news reports of food safety incidents in 11 years from January 2007 to December 2017. Since the same food safety incidents may be reported many times by different news websites, in order to prevent the interference caused by data duplication, a food safety incidents corpus containing 4156 reports is finally constructed after automatic de-duplication. 

### 1.2.Preprocessing

According to the existing Chinese food safety law, food safety incidents are divided into nine categories. After manually labeling the data, the existing corpus is labeled into four categories. The specific categories and their quantities are shown as follows:

|  Label  |               Meaning                | Quantity |
| :-----: | :----------------------------------: | :------: |
| label_1 | Food  safety incidents of additives  |   226    |
| label_2 | Pesticide  residues and heavy metals |   1704   |
| label_3 |            Dairy products            |   169    |
| label_4 |      Fake  and shoddy products       |   2057   |

The datasets and labels used in the three models are as follows:

|  Model   |     Datasets     |                          Labels                          |
| :------: | :--------------: | :------------------------------------------------------: |
|   SVM    |   10-fold-SVM    |                   ['0', '1', '2', '3']                   |
|   BERT   |   10-fold-BERT   |                   ['0', '1', '2', '3']                   |
| FastText | 10-fold-FastText | ['__label__0', '__label__1', '__label__2', '__label__3'] |

## 2.Models

On the basis of preprocessing, the corresponding data are divided into training set and test set according to 9:1, and the experiment is carried out in the way of the 10-fold cross-validation, so as to avoid the contingency of the results caused by a single experiment. The following are the specific steps of using the three models to study the automatic classification of food safety events.

### 2.1.SVM

#### 2.1.1.About

![SVM](H:\Food_Safety_Incidents\Models\SVM\SVM.png)

**Support Vector Machine (SVM)** is a supervised machine learning classifier that supports vector computation. The core idea is to classify data into two or more classes by constructing a partition surface. Support vector machine is widely used in the field of natural language classification. The frequency of words in a text is input to SVM as a feature attribute, which means that the text is regarded as a bag of words, and each word in the bag has a feature, and the value of the feature is the frequency of the word, and then the frequency of the word is vectorized to use SVM classification.

#### 2.1.2.Usage

```python
python svm.py
```

#### 2.1.3.Result

The specific classification of the best performance SVM model 

| Serial number |   P    |   R    |   F    |
| :-----------: | :----: | :----: | :----: |
|    label_1    | 81.55% | 78.14% | 79.81% |
|    label_2    | 17.40% | 50.00% | 25.81% |
|    label_3    | 76.47% | 75.14% | 75.80% |
|    label_4    | 94.12% | 80.00% | 86.49% |
| Macro average | 67.38% | 70.82% | 66.98% |



### 2.2.BERT

#### 2.2.1.About

![BERT](H:\Food_Safety_Incidents\Models\BERT\BERT.png)

**BERT** (Devlin et al., 2019) is a language representation model, which stands for Bidirectional Encoder Representations from Transformers. BERT is able to extract deep semantic features based on a bidirectional context and is designed to pre-train deep bidirectional representations from unlabeled text, and pre-trained BERT models can be fine-tuned by simply adding an output layer to create state-of-the-art models for a wide range of tasks.

#### 2.2.2.Usage

```python
python run.py --model bert
```

#### 2.2.3.Result

The specific classification of the best performance BERT model 

| Serial number |   P    |   R    |   F    |
| :-----------: | :----: | :----: | :----: |
|    label_1    | 83.67% | 91.62% | 87.47% |
|    label_2    | 46.67% | 66.67% | 54.90% |
|    label_3    | 88.36% | 74.57% | 80.88% |
|    label_4    | 75.00% | 81.82% | 78.26% |
| Macro average | 73.42% | 78.67% | 75.38% |

### 2.3.FastText

#### 2.3.1.About

![FastText](H:\Food_Safety_Incidents\Models\FastText\FastText.png)

**FastText** is a word embedding based classifier developed by Facebook, which was in traduced by Armand Joulin, et al.2016. It was based on n-gram features, dimensionality reduction, and a fast approximation of the Softmax classifier. FastText model propose to learn representations for character n-grams, and to represent words as the sum of the n-gram vectors. 

#### 2.3.2.Usage

```python
python run.py
```

#### 2.3.3.Result

The specific classification of the best performance FASTTEXT model 

| Serial number |    P    |    R    |   F    |
| :-----------: | :-----: | :-----: | :----: |
|    label_1    | 100.00% | 82.44%  | 90.37% |
|    label_2    | 100.00% | 90.91%  | 95.24% |
|    label_3    | 80.57%  | 100.00% | 89.24% |
|    label_4    | 100.00% | 81.25%  | 86.49% |
| Macro average | 95.14%  | 88.65%  | 91.13% |

## 3.Conclusion

![img](file:///C:/Users/ADMINI~1/AppData/Local/Temp/msohtmlclip1/01/clip_image002.gif)

From the F value of each category in the experimental results, it can be concluded that the performance of the three models for the classification of food safety incidents from high to low is: FastText > Bert > SVM.

