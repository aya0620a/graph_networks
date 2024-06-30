import numpy as np  #配列を扱うためのモジュール
import csv  #CSV形式の出力を得るためのモジュール
import random   #乱数を発生するためのモジュール
m=23    #格子グラフの高さ
h=32    #格子グラフの高さ
n=m*h   #格子グラフの頂点数＝横幅x高さ　

#出口を設定
deguchi=13
#入口を設定
iriguchi=14

vadjlist=np.zeros((n,4))    #二次元配列で各頂点の4つの隣接頂点を格納

for i in range(0,n):
    x=i % m
    y=i // m
    
    if x==0:    # 左端の列の頂点には左の近傍はない
        a=-1
    else:       # それ以外の頂点には左の近傍がある
        a=i-1
    if x==m-1:  # 右端の列の頂点には右の近傍はない
        b=-1
    else:
        b=i+1
    if y==0:    # 0行目の頂点には上近傍はない
        c=-1
    else:
        c=i-m
    if y==h-1:  # 一番下の行の頂点には下近傍はない　
        d=-1
    else:
        d=i+m
        
    vadjlist[i]=[int(a),int(b),int(c),int(d)]
    
    
print(vadjlist)

#ファイルに出力して確認してみましょう。ついでにPython の標準的なファイル出力の方法や出力の様子を見てみましょう

#path="latticegraph.csv"     # グラフを書き込むファイルの準備
#with open(path,"w") as f:       # 情報を書き込むファイルの位置や名前をｆにする。ｗは、「作成、上書き」オプション
    #writer= csv.writer(f)     # csv形式の書き込みを使う　　
    #writer.writerows(vadjlist)         # 行単位で改行してかきこむ。
    
plist=np.empty(n)   # 各頂点iの親頂点parent(i)のリスト
status=np.zeros(n)  #各頂点が未探索なら０、探索中なら１

#using=[deguchi]     # 探索中の頂点のリストです。最初は出口頂点99が入ります　
status[deguchi]=1   # 出口頂点のステータスを探索中に設定します

#２．経路上の頂点のリストを作る。   
mypath = [13,36,35,58,57,80,103,102,101,100,123,122,145,144,167,166,189,188,211,210,233,232,255,278,301,300,323,322,345,368,391,392,415,416,439,440,463,486,509,508,507,506,529,530,553,554,577,578,579,580,603,626,649,648,671,670,693,694,717,718,719,720,721,722,723,700,702,725,726,727,728,729,730,731,708,709,686,685,662,661,638,615,616,617,618,595,596,573,572,549,548,525,502,479,456,455,454,453,452,451,450,449,448,447,446,445,444,443,442,441,418,419,420,397,374,373,350,327,304,281,282,259,236,237,238,239,262,263,286,309,332,331,330,353,354,355,378,377,400,399,398,421,422,423,424,425,426,427,428,429,406,405,404,381,380,357,358,359,336,335,334,311,288,265,266,243,244,245,246,269,270,293,316,339,362,385,384,407,430,431,432,433,434,457,458,435,412,413,390,367,344,343,320,319,296,273,250,249,226,203,180,179,156,155,154,131,132,133,134,111,110,87,86,63,62,39,16,15,14]

#頂点のステータスを1に設定
for p in mypath:
    status[p] = 1  
    
#自分で作成したパスを利用
using = mypath  

#親頂点をplistに入れる
for i in range(len(mypath) - 1, 0, -1):    #開始値、終了値、ステップ値
    plist[mypath[i]] = mypath[i - 1] 

while len(using)>0:     # 探索中の頂点のリストが空になったら終了します
    
    x=int(using.pop())  # 探索中リストの最後の頂点xを取り出す
    
    #頂点xの近傍をとってくる
    llist=[vadjlist[x,0], vadjlist[x,1], vadjlist[x,2], vadjlist[x,3]]
    # 近傍の4頂点の左右上下の順番をシャッフルします
    xlist=random.sample(llist,4)
    j=0
    while j<4:
        y= int(xlist[j])
        if y>=0:    # 近傍yを取り出す
            
            if status[y]==0:        # もしyが未探索なら作業
                status[y]=1         # yのステータスを探索中にする　
                plist[y]=x          # yの親頂点をxにする
                using.append(x)     # xを探索中リストに戻す
                using.append(y)     #yを探索中リストの末尾に入れる
                j=4     #yが未探索ならば、次の頂点を探す必要はないので、ループを抜ける
            else:
                j+=1    #yが未探索でない場合、次の頂点を探す
        else:
            j+=1
            
#以下　探索でできた根付き全域木の辺のリストを作ります 

edges=np.zeros((n,2))       # 全域木の辺を格納するリスト（二次元リスト）
for i in range(0,n):        # 全域木の辺を構築
    edges[i]=[i,plist[i]]   # 全域木の各頂点と、親頂点の間の辺を格納
edges=np.delete(edges,deguchi,0)    # 全域木の根（つまり出口）には親頂点がいないので、除去
edges = edges.astype('int')     #整数型に変換

with open("mymaze.csv","w",newline="") as f:    #出力に空行が入らないようにnewline=" "を指定
    writer= csv.writer(f)     # csv で書き込む
    writer.writerow([h, m])   # 格子グラフの高さと横幅を書き込む
    writer.writerow([iriguchi, deguchi])  # 入口と出口の頂点番号を書き込む
    writer.writerow([n-1])    #全域木の辺の数を書き込む
    writer.writerows(edges)   # 全域木の辺を書き込む
print("program succesfully terminated")   #プログラムが正常に終了したことを表示