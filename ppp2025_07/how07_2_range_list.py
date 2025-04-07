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

#질문= num[]이 for문 안에 들어가있으면 안되는 이유가 return을 1번만 받아서 그런가요?, 아니면 전에 했던 num이 사라졌기 때문인가요?
#7번 제출할때 -로 제출해서 피드백 받았는데, 그럼 다시 제출하면 될까요?

