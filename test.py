def a():
    n, s = map(int, input().split())
    res = 0
    a = input().split()
    for i in range(n):
        a[i] = int(a[i])
        if s - a[i] >= 0 and res < a[i]:
            res = a[i]

    print(res)


def b():
    s = input()
    letter_count = {}

    for letter in "sheriff":
        letter_count[letter] = 0

    for letter in s:
        if letter in letter_count:
            letter_count[letter] += 1
    max_sheriffs = min(letter_count.values())

    print(max_sheriffs)


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def c():
    n = int(input())
    a = [int(num_str) for num_str in input().split()]
    b = [int(num_str) for num_str in input().split()]
    l, r = 0, n - 1

    for l in range(n):
        if a[l] != b[l]:
            break

    for r in range(n - 1, -1, -1):
        if a[r] != b[r]:
            break

    if l > r:
        print("YES")
        return

    if quick_sort(a[l:r + 1]) == b[l:r + 1]:
        print("YES")
    else:
        print("NO")


def d():
    target, m = map(int, input().split())
    denominations = [int(num) for num in input().split() for _ in range(2)]
    dp = [0 for _ in range(2 * m + 1)]
    found = False
    for right in range(1, 2 * m + 1):
        dp[right] = dp[right - 1] + denominations[right - 1]
        if dp[right] - target >= 0 and dp[right] - target in dp:
            found = True
            left = dp.index(dp[right] - target)
            print(right - left)
            print(denominations[left:right])
            break
    if not found:
        print(-1)


def f():
    n, m = map(int, input().split())
    teams = {}
    for i in range(n):
        teams[i + 1] = ([i + 1], 1)
    for i in range(m):
        s = input().split()
        question, x = int(s[0]), int(s[1])
        if question == 1:
            y = int(s[2])
            team_x = teams.pop(x)
            team_y = teams.pop(y)
            temp_x_arr = list(team_x[0])

            team_x[0].extend(team_y[0])
            team_y[0].extend(temp_x_arr)

            teams[x] = (team_x[0], team_x[1])
            teams[y] = (team_y[0], team_y[1])

            for el in teams[x][0]:
                var = teams.pop(el)

                teams[el] = (var[0], var[1] + 1)

        elif question == 2:
            y = int(s[2])
            if y in teams[x][0]:
                print("YES")
            else:
                print("NO")
        else:
            print(teams[x][1])


def e():
    n, m = map(int, input().split())
    max_self_len = 0
    graph = {}

    for _ in range(m):
        u, v, length = map(int, input().split())

        if u == v:
            max_self_len = max(max_self_len, length)
            continue

        if u not in graph:
            graph[u] = 0
        graph[u] = max(length, graph[u])

        if v not in graph:
            graph[v] = 0
        graph[v] = max(length, graph[v])

    if not graph:
        print(max_self_len)
    else:
        min_max_len = min(graph.values())
        print(min_max_len - 1)


if __name__ == "__main__":
    c()
