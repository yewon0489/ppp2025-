# dan=int(input("숫자를 입력하세요"))
# for i in range(1,10):
#     n= dan*i
#     print(f'{dan}*{i}={n}')

def gugudan(dan):
    
    for i in range(1,10):
        n= dan*i
        print(f'{dan}*{i}={n}')
    return n

dan=int(input("숫자를 입력하세요"))

def main():
    gugudan(dan)

if __name__ == "__main__":
    main()



