import numpy as np    # 配列を扱うモジュール

AppleList = np.empty((0,3),dtype=np.int64) # リンゴのリストを入れる為の空配列の作成

FileInput = 'catsura_ukki.txt' # 入力ファイル名
with open(FileInput, 'r') as f: # リンゴのリストのファイルの読み込み
    for line in f.readlines(): # 各行ごとに実行
        AppleList = np.append(AppleList, [[int(n) for n in line.strip().split(', ')]], axis=0) # ファイル内のリンゴのx,y,tを配列に追加

AppleXT = AppleList @ np.array([[1,0],[0,5],[0,1]]) # 行列の積計算を使用してxとTを入れた配列を作成

# x座標が4進むごとにtが1秒ずつ減るように調整
for i in range(len(AppleXT) - 1, -1, -1):
    AppleXT[i, 1] -= ((63 - AppleXT[i, 0]) // 4) * 5
    # AppleXT[i, 1]が0以下になる場合は削除する
    if AppleXT[i, 1] <= 0:
        AppleXT = np.delete(AppleXT, i, 0)
    
Result = '' # ファイルに記入する為の文字列の格納場所


# -- algorithm start --
AppleXT = AppleXT[np.argsort(AppleXT[:, 1])] # Tを基準にソート
# AppleXTの中身を確認
print(AppleXT)

Status = [AppleXT[0][0], 0, 0] # カゴの位置情報（x座標、t座標、y座標）の初期化
Result += str(AppleXT[0][0]) + ',' # カゴの初期位置と初期時間0の記述

for x,t in AppleXT: # リンゴのxとTをループ
    # t_diff = (x - Status[0]) // 4
    if abs(t-Status[1]) >= abs(x-Status[0]): # リンゴが取れる(残り時間が移動可能距離より多い)時
        for i in range(abs(x-Status[0])): # カゴの移動(r:right,l:left)
            Result += 'r,' if x > Status[0] else 'l,'
        for i in range(abs(t-Status[1]) - abs(x-Status[0])): # 余った時間は待機(s:stop)
            Result += 's,'
        Status = [x,t] # 現在のカゴの位置の更新
# --- algorithm end ---

Result += '\n' # 出力ファイルの最後に改行を入れること

FileOutput = 'sumpleB.txt' # 出力ファイル名
with open(FileOutput, 'w', encoding='UTF-8') as f: # 出力ファイルの書き出し
    f.write(Result) # 出力ファイルに記述