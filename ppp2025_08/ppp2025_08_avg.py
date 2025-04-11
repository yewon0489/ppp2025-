def count(numbers):
    return len(numbers)

def avg(numbers):
    return sum(numbers) / len(numbers)

def max_val(numbers):
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

def min_val(numbers):
    min_num = numbers[0]
    for num in numbers:
        if num < min_num:
            min_num = num
    return min_num

def median(numbers):  
    sorted_list = sorted(numbers)
    n = len(sorted_list)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        return sorted_list[mid]

def main():
    nums = []
    with open("numbers2.txt") as f:
        lines = f.readlines()
        for line in lines:
            text = line.strip()
            print(f"{text}")
            nums.append(int(text))  

    print(f"총 개수: {count(nums)}")
    print(f"평균: {avg(nums)}")
    print(f"최댓값: {max_val(nums)}")
    print(f"최솟값: {min_val(nums)}")
    print(f"중앙값: {median(nums)}")

if __name__ == "__main__":
    main()