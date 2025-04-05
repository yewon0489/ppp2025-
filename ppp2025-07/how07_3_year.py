#4로 안되면 평년, 4로 되는데 100로 되면 윤년,4둘다 되면 평년년 4, 100 둘다 되면 윤년

def is_leap_year(y):
    if y%4 == 0:
        if y%100 == 0:
            if y%400 == 0:
                print(f"{y}윤년입니다.")
            else:
                print(f"{y}평년입니다.")
        else:
            print(f"{y}윤년입니다.")
    else:
        print(f"{y}평년입니다.")
        

def main():
    y=int(input("몇년인가요?"))
    is_leap_year(y)
if __name__ == "__main__":
    main()

