# 1번과제에서 만든 함수를 이용하며, 메인에서 split()함수를 이용하여 여러 값을 한줄로 입력
# 받아 평균을 출력할 수 있는 프로그램을 완성하시오.

def average(nums):
        avg=sum(nums)/len(nums)
        return avg

def main():
    number= input("숫자 입력=")
    nums = [int(x) for x in number.split(",")]
    print(f"{average(nums):.3f}")
if __name__ == "__main__":
    main()