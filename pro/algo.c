#include <stdio.h>
#include <stdlib.h>

// 配列の長さを取得する関数
int len(int* arr) {
    int length = 0;
    while(arr[length] != '\0') {
        length++;
    }
    return length;
}

// 配列を降順にソートする関数
void sort(int* arr, int n) {
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {
            if (arr[j] < arr[j+1]) {
                int temp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = temp;
            }
        }
    }
}

// Havel-Hakimiアルゴリズムを実装する関数
int havelHakimi(int* D, int n) {
    // Step 1
    if (n == 0) {
        return 1;
    }
    // Step 2
    if (D[0] > n-1) {
        return 0;
    }
    // Step 3
    int d1 = D[0];
    for (int i = 0; i < d1; i++) {
        D[i+1]--;
    }
    for (int i = 0; i < n-d1; i++) {
        D[i] = D[i+d1];
    }
    sort(D, n-d1);
    return havelHakimi(D, n-d1);
}

int main() {
    int D[] = {4, 3, 3, 1, 0};
    int n = len(D);
    sort(D, n);
    int result = havelHakimi(D, n);
    printf("%d\n", result);
    return 0;
}