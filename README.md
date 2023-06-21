# 三値分類予測 - *Recommender.py*
組成情報を用いて化合物の安定性を予測するプログラム

作成者：濱家雅人（名工大・中山研）

作成日：2023年6月7日


## 概要
無機固体材料の安定性を安定・準安定・不安定と仮定した際の分類予測スクリプト

下記のように分解エネルギーで安定性の分類を仮定した。

<img width="569" alt="image" src="https://github.com/NakayamaLab-NITech/Recommender/assets/102635361/42f11309-32a4-462e-9035-3af5e1389099">

*RandomForest* を用いた分類予測により、とても高精度な予測が可能となった。本スクリプトでは、学習済みモデルを読み込むことにより、新しく提示された化学組成の材料について安定性を出力している。スクリプト作動後、安定性予測結果と分類確率がファイル出力される。

## 詳細説明
本スクリプトの学習済みモデル作成には *MaterialsProject* から抽出された9.8万件のデータセットを用いた。

分解エネルギーは図(a)のような分布となり、拡大すると図(b)のように分布していることがわかる。各分類の分布割合は図(c)のようになる。

<img width="855" alt="image" src="https://github.com/NakayamaLab-NITech/Recommender/assets/102635361/f39dd687-5264-4697-9922-2fab82e1dc4b">

また、説明変数には中山研究室で開発されたヒストグラム記述子を用いた。詳しくは [中山研_ヒストグラム記述子](https://github.com/NakayamaLab-NITech/composional-histogram-descriptor) を参照。

上述したデータセットを 80% の訓練データと 20% のテストデータに分割した。訓練データで学習し、テストデータで分類精度を評価した。また、訓練データの中で、k分割交差検証法を用いたハイパーパラメータチューニングを行っており、汎用性の高いパラメータ探索に尽力した。

4つの機械学習モデルを検証した中で、最も分類精度の高かった *RandomForest* を本スクリプトに掲載している。 *RandomForest* を用いた分類精度は **AUC = 0.88**, **正解率91%** を記録した。（AUCは1を最高値とし、1に近づくにつれよい予測であるといえる）

下図は最も精度の良かった *RandomForest* の ROC曲線である。顕著に左上に近づくカーブを描いており、予測精度が良いことが読み取れる。

<img width="359" alt="画像11" src="https://github.com/NakayamaLab-NITech/Recommender/assets/102635361/863f64ff-1152-4f49-a16e-627011c23a01">

本スクリプトでは、上述した *RandomForest* を学習済みモデルとし、使用する。

## 使用方法（Linux環境のみ対応しています）
1.以下に示すディレクトリ構造を用意する。
  * histgram_desc

     ┣━ DefElem.csv
     
     ┗━ make_hist_in_ver5.py

  * need_files
     
     ┣━ descript_list
     
     ┣━ descripter_table
     
     ┣━ histdef.dat
     
     ┣━ histgram_desc.py
     
     ┣━ mix_desc.py
     
     ┗━ model_fit.py
     
  * predict
     
     ┣━ * **RandomForest_model.pickle**
     
     ┗━ list.dirname
     
  * Recommender.py

2. ここで predict 内の RandomForest_model.pickle はファイルサイズが大きく、別の方法で取得します。
   以下のようなコマンドで、DropBox 内にある pickle ファイルを取得します。
   
   `wget https://www.dropbox.com/s/qsvewtf2o6en5df/RandomForest_model.pickle`

   取得した pickle ファイルを predict 内において準備完了となります。

4.  `python Recommender.py 〇 〇 〇` と入力する。〇 には安定性を知りたい組成式を入力（Li2O MgO FeO など...）
    
    組成式に数の制限はないためスペース区切りでいくつもの元素を一度に予測できる
    
    ※注意点
    
    * python3.8 ~ 3.10 にのみ対応しているため、バージョンの確認が必要
    

## 結果の確認方法
まず、出力の上部について確認する。下図に実際に入力した際の出力を示す。

初めに入力した組成式の確認があり、その後説明変数がどのような形なのかを表示している。また、次に表示されているデータフレームは先述した中山研のヒストグラム記述子を示している。

<img width="829" alt="image" src="https://github.com/NakayamaLab-NITech/Recommender/assets/102635361/20945844-43c2-43ac-a830-a4e10c434b70">

次に、実際に予測結果が下図のように出力される。

![image](https://github.com/NakayamaLab-NITech/Recommender/assets/102635361/040a28e3-759a-4780-baa7-ebded98a6c08)

予測結果は下記に示す表のように出力されており、*after_predict_box* というディレクトリの中にも保管されている。

|formula|this_Stability_percent|predict_number|Stability|probability class 0 (0-0.01 eV / atom) |probability class 1 (0.01-0.1 eV / atom) |probability class 2 (0.1- eV / atom)|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|入力した化学組成|安定性を選んだ際の確率|予測したクラス名|安定性|クラス0の確率（安定と判断した確率）|クラス1の確率（準安定と判断した確率）|クラス2の確率（不安定と判断した確率）|

これらから入力した化学組成が合成可能かの予測結果を確認でき、実際に合成をする際に判断する材料の一つに数えられる。


## ライセンス、引用について (License, Citing)
**ライセンス(About License)**　This software is released under the MIT License, see the LICENSE.
**引用先(Citing)**
