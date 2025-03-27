fruits = {
    "hallabong": 50 / 100,  
    "strawberry": 34 / 100,  
    "banana": 77 / 100  
}


fruit_eaten = {
    "hallabong": int(input("섭취한 한라봉의 양(g): ")),
    "strawberry": int(input("섭취한 딸기의 양(g): ")),
    "banana": int(input("섭취한 바나나의 양(g): "))
}

# 총 칼로리 계산
total_calories = 0
for fruit in fruits:
    total_calories += fruits[fruit] * fruit_eaten[fruit]
print(f"섭취하신 칼로리의 총량은 {total_calories:.2f} kcal 입니다.")




