#4 tuple fuzzy representation - lecture slide 20

a = int(input("Enter a value: "))
b = int(input("Enter b value: "))
alpha = int(input("Enter alpha value: "))
beta = int(input("Enter beta value: "))

x = int(input("Enter test value: "))

if x < a - alpha:
    print(0)
elif x in range(a - alpha, a):
        print((x - a + alpha )/alpha)
elif x in range(a, b):
    print(1)
elif x in range(b, b + beta):
    print((b + beta - x)/beta)
elif x > b + beta:
    print(0)
