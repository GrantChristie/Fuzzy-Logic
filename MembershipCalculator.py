def main():
    a = int(input("Enter a value: "))
    b = int(input("Enter b value: "))
    alpha = int(input("Enter alpha value: "))
    beta = int(input("Enter beta value: "))
    x = int(input("Enter test value: "))
    print(membership(a,b,alpha,beta,x))
    
def membership(a,b,alpha,beta,x):
    a = int(a)
    b = int(b)
    alpha = int(alpha)
    beta = int(beta)
    x = int(x)
    if x < a - alpha:
        return 0
    elif x in range(a - alpha, a):
            return (x - a + alpha )/alpha
    elif x in range(a, b):
        return 1
    elif x in range(b, b + beta):
        return(b + beta - x)/beta
    elif x > b + beta:
        return 0

if __name__ == '__main__':
    main()
