#4 tuple fuzzy representation - lecture slide 20

def main():
    

    a = int(input("Enter a value: "))
    b = int(input("Enter b value: "))
    alpha = int(input("Enter alpha value: "))
    beta = int(input("Enter beta value: "))

    x = int(input("Enter test value: "))
    membership(a,b,alpha,beta,x)
    
def membership(a,b,alpha,beta,x):
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

if __name__ == '__main__':
    main()
