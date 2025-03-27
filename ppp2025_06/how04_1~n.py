def sum_n(n):
    total=0
    for n in range(1,n+1):
        total =total+n
    print(f"총합은 {total}입니다.")
    return True
n=int(input("몇까지 더하실 생각이신가요?"))


def main():
    sum_n(n)

if __name__ == "__main__":
    main()