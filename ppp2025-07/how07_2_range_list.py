# get_range_list(n)1-n까지 리스트를 돌려주는 함수를 만드시오. 함
def get_range_list(n):
    num=[]
    for i in range(1,n+1):
        num.append(int(i))
    return num

def main():
    n=int(input("n은 몇인가요?"))
    print(get_range_list(n))
if __name__ == "__main__":
    main()
