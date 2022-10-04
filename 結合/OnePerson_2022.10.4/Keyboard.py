def test(x):
    x += x
    return x

ans = 0
for i in range(100):
    if i%10 == 1:
        ans += test(i)
        print(ans)