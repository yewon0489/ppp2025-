def number():
    numbers_list=[]
    while True:
        input_n=input("자연수를 입력하시오(정지:-1):").strip()
        try:
            num = int(input_n)

            if num ==-1:
                break
            elif num > 0:
                numbers_list.append(num)
            else:
                print("!!!!!!!!!자연수가 아닙니다!!!!!!!!!")

        except ValueError:
            print("!!!!!!!!!정수가 아닙니다!!!!!!!!!")
            
    return numbers_list    

def main():
    numbers=number()
    count= len(numbers)
    if len(numbers) == 0:
        print("자연수를 입력하지 않았습니다.")
        return
    total= sum(numbers)
    avg=total/len(numbers)
    
    print(f"입력하신 값은 {numbers}이며, 총 {count}개의 자연수가 입력 되었습니다.")
    print(f"평균은 {avg:.2f}입니다.")
if __name__=="__main__":
    main()