import numpy as np  # 配列を扱うモジュール

# 1. 入力ファイルの読み込み
AppleList = np.empty((0, 3), dtype=np.int64)  # リンゴのリストを入れる為の空配列の作成
FileInput = 'apple.txt'

with open(FileInput, 'r') as f:
    for line in f.readlines():
        AppleList = np.append(AppleList, [[int(n) for n in line.strip().split(', ')]], axis=0)

# 2. x, y, t を (x, t) の形に変換
AppleXT = AppleList @ np.array([[1, 0], [0, 5], [0, 1]])  # 行列の積計算を使用してxとTを入れた配列を作成

# x座標が4進むごとにtが1秒ずつ減るように調整
for i in range(len(AppleXT)):
    AppleXT[i, 1] -= (AppleXT[i, 0] // 4) * 5
    if AppleXT[i, 1] <= 0:
        AppleXT = np.delete(AppleXT, i, 0)
        i -= 1

AppleXT = AppleXT[np.argsort(AppleXT[:, 1])]  # Tを基準にソート
Result = ''  # ファイルに記入する為の文字列の格納場所

# 3. n、dpとnext_nodeの初期化
n = len(AppleXT)  # リンゴの数
dp = np.ones(n, dtype=int)  # 各リンゴを取ることで得られるリンゴの数
next_node = -np.ones(n, dtype=int)  # 次にどのリンゴに遷移するかを記録

# 4. グラフの作成（次のリンゴに移動可能かどうか）
graph = [[] for _ in range(n)]  # グラフの初期化

for i in range(n):  # グラフの作成
    for j in range(i + 1, n):  # i番目のリンゴからj番目のリンゴに移動可能かどうか
        if abs(AppleXT[j][0] - AppleXT[i][0]) <= AppleXT[j][1] - AppleXT[i][1]:  # リンゴが取れる(残り時間が移動可能距離より多い)時
            graph[i].append(j)  # i番目のリンゴからj番目のリンゴに移動可能

# 5. 動的計画法によるリンゴを取る数の計算
for i in range(n):  # 各リンゴに対して
    for j in graph[i]:  # i番目のリンゴから移動可能なリンゴに対して
        if dp[i] + 1 > dp[j] or (dp[i] + 1 == dp[j] and AppleXT[j][0] > 31):  # リンゴを取ることで得られるリンゴの数が増える場合
            dp[j] = dp[i] + 1  # リンゴを取ることで得られるリンゴの数を更新
            next_node[j] = i  # 次にどのリンゴに遷移するかを記録

# 6. 最大のリンゴを取れる経路を見つける
max_apples = 0  # 最大のリンゴを取れる数を記録
best_end = 0  # 最大のリンゴを取れる経路の終点を記録

for i in range(n):
    if dp[i] > max_apples or (dp[i] == max_apples and AppleXT[i][0] > 31):  # リンゴを取ることで得られるリンゴの数が増える場合
        max_apples = dp[i]  # リンゴを取ることで得られるリンゴの数を更新
        best_end = i  # 最大のリンゴを取れる経路を記録

# 7. 経路の復元
path = []  # 経路を記録
current = best_end  # 現在のリンゴの位置を記録

while current != -1:  # 最初のリンゴに戻るまで
    path.append(current)  # 経路を記録
    current = next_node[current]  # 次のリンゴに遷移

# 8. 結果の出力
path = path[::-1]
initial_position = AppleXT[path[0]][0]
Result += str(initial_position) + ','

pos, time = initial_position, 0

for idx in path:  # 経路の各リンゴに対して
    x, t = AppleXT[idx]  # x, t はリンゴの座標と到達時間
    if x > pos:
        Result += 'r,' * (x - pos)
    elif x < pos:
        Result += 'l,' * (pos - x)
    Result += 's,' * (t - time - abs(x - pos))
    pos, time = x, t  # 現在の位置と時間を更新

Result += '\n'

# 9. 結果の書き込み
FileOutput = 'douteki.txt'
with open(FileOutput, 'w', encoding='UTF-8') as f:
    f.write(Result)
