#!/usr/bin/env python3

import numpy as np    # 配列を扱うモジュール

AppleList = np.empty((0,3),dtype=np.int64) # リンゴのリストを入れる為の空配列の作成

FileInput = 'input9.txt' # 入力ファイル名
with open(FileInput, 'r') as f: # リンゴのリストのファイルの読み込み
    for line in f.readlines(): # 各行ごとに実行
        AppleList = np.append(AppleList, [[int(n) for n in line.strip().split(', ')]], axis=0) # ファイル内のリンゴのx,y,tを配列に追加

AppleXT = AppleList @ np.array([[1,0],[0,5],[0,1]]) # 行列の積計算を使用してxとTを入れた配列を作成
Result = '' # ファイルに記入する為の文字列の格納場所

# ここからアルゴリズムの考察に入る部分です. 今回は単純な例として以下の様な方針を取っている
# ・スタートのx座標は一番最初にりんごが取れる場所
# ・リンゴを地面到達時間が早い順から見ていく
# ・そのリンゴが取得可能だった場合, そのリンゴを最優先で取りに行く

# -- algorithm start --
AppleXT = AppleXT[np.argsort(AppleXT[:, 1])] # Tを基準にソート
Status = [AppleXT[0][0],0] # カゴの位置情報
Result += str(AppleXT[0][0]) + ',' # カゴの初期位置と初期時間0の記述

for x,t in AppleXT: # リンゴのxとTをループ
    if abs(t-Status[1]) >= abs(x-Status[0]): # リンゴが取れる(残り時間が移動可能距離より多い)時
        for i in range(abs(x-Status[0])): # カゴの移動(r:right,l:left)
            Result += 'r,' if x > Status[0] else 'l,'
        for i in range(abs(t-Status[1]) - abs(x-Status[0])): # 余った時間は待機(s:stop)
            Result += 's,'
        Status = [x,t] # 現在のカゴの位置の更新
# --- algorithm end ---

Result += '\n' # 出力ファイルの最後に改行を入れること

FileOutput = 'sample9.txt' # 出力ファイル名
with open(FileOutput, 'w', encoding='UTF-8') as f: # 出力ファイルの書き出し
    f.write(Result) # 出力ファイルに記述