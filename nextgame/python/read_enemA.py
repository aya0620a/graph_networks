import numpy as np  # 配列を扱うモジュール

# 1. 入力ファイルの読み込み
AppleList = np.empty((0, 3), dtype=np.int64)  # リンゴのリストを入れる為の空配列の作成
OpponentList = np.empty((0, 3), dtype=np.int64)  # 相手のリンゴのリストを入れる為の空配列の作成

FileInput = 'apple.txt'
FileOpponentInput = 'apple.txt'

with open(FileInput, 'r') as f:
    for line in f.readlines():
        AppleList = np.append(AppleList, [[int(n) for n in line.strip().split(', ')]], axis=0)

with open(FileOpponentInput, 'r') as f:
    for line in f.readlines():
        OpponentList = np.append(OpponentList, [[int(n) for n in line.strip().split(', ')]], axis=0)

# 2. x, y, t を (x, t) の形に変換
AppleXT = AppleList @ np.array([[1, 0], [0, 5], [0, 1]])  # 行列の積計算を使用してxとTを入れた配列を作成
OpponentXT = OpponentList @ np.array([[1, 0], [0, 5], [0, 1]])  # 相手の行列の積計算

# x座標が4進むごとにtが1秒ずつ減るように調整
for i in range(len(AppleXT)):
    AppleXT[i, 1] -= (AppleXT[i, 0] // 4) * 5
    if AppleXT[i, 1] <= 0:
        AppleXT = np.delete(AppleXT, i, 0)
        i -= 1

for i in range(len(OpponentXT)):
    OpponentXT[i, 1] -= ((63 - OpponentXT[i, 0]) // 4) * (-5)
    if OpponentXT[i, 1] <= 0:
        OpponentXT = np.delete(OpponentXT, i, 0)
        i -= 1

AppleXT = AppleXT[np.argsort(AppleXT[:, 1])]  # Tを基準にソート
OpponentXT = OpponentXT[np.argsort(OpponentXT[:, 1])]  # 相手のTを基準にソート
Result = ''  # ファイルに記入する為の文字列の格納場所

# 3. n、dpとnext_nodeの初期化
n = len(AppleXT)  # リンゴの数
m = len(OpponentXT)  # 相手のリンゴの数

# 4. 相手の経路を計算
dp_opponent = np.ones(m, dtype=int)
next_node_opponent = -np.ones(m, dtype=int)
graph_opponent = [[] for _ in range(m)]

for i in range(m):
    for j in range(i + 1, m):
        if abs(OpponentXT[j][0] - OpponentXT[i][0]) <= OpponentXT[j][1] - OpponentXT[i][1]:
            graph_opponent[i].append(j)

for i in range(m):
    for j in graph_opponent[i]:
        if dp_opponent[i] + 1 > dp_opponent[j]:
            dp_opponent[j] = dp_opponent[i] + 1
            next_node_opponent[j] = i

max_apples_opponent = 0
best_end_opponent = 0

for i in range(m):
    if dp_opponent[i] > max_apples_opponent:
        max_apples_opponent = dp_opponent[i]
        best_end_opponent = i

path_opponent = []
current_opponent = best_end_opponent

while current_opponent != -1:
    path_opponent.append(current_opponent)
    current_opponent = next_node_opponent[current_opponent]

path_opponent = path_opponent[::-1]

# 5. 自分の経路を計算（相手の経路を考慮）
dp = np.ones(n, dtype=int)
next_node = -np.ones(n, dtype=int)
graph = [[] for _ in range(n)]

for i in range(n):
    for j in range(i + 1, n):
        if abs(AppleXT[j][0] - AppleXT[i][0]) <= AppleXT[j][1] - AppleXT[i][1]:
            graph[i].append(j)

for i in range(n):
    for j in graph[i]:
        if dp[i] + 1 > dp[j] or (dp[i] + 1 == dp[j] and AppleXT[j][0] > 31):
            dp[j] = dp[i] + 1
            next_node[j] = i

# 相手が取るリンゴを優先して自分の経路を決定
for idx in path_opponent:
    x, t = OpponentXT[idx]
    for i in range(n):
        if AppleXT[i][0] == x and AppleXT[i][1] == t:
            dp[i] = 0  # 相手が取るリンゴは無視

max_apples = 0
best_end = 0

for i in range(n):
    if dp[i] > max_apples or (dp[i] == max_apples and AppleXT[i][0] > 31):
        max_apples = dp[i]
        best_end = i

path = []
current = best_end

while current != -1:
    path.append(current)
    current = next_node[current]

# 6. 結果の出力
path = path[::-1]
initial_position = AppleXT[path[0]][0]
Result += str(initial_position) + ','

pos, time = initial_position, 0

for idx in path:
    x, t = AppleXT[idx]
    if x > pos:
        Result += 'r,' * (x - pos)
    elif x < pos:
        Result += 'l,' * (pos - x)
    Result += 's,' * (t - time - abs(x - pos))
    pos, time = x, t

Result += '\n'

# 7. 結果の書き込み
FileOutput = 'read_enemA.txt'
with open(FileOutput, 'w', encoding='UTF-8') as f:
    f.write(Result)
