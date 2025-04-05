def average(nums):
        avg=sum(nums)/len(nums)
        return avg

def main():
    number = [1,2,3,4,5,10,9]
    print(f"{average(number):.3f}")
if __name__ == "__main__":
    main()


#리스트를 숫자로 나눌 수 없다.