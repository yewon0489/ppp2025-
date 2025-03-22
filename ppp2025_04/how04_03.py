#칼로리 계산산

hallabong_eat=int(input("섭취한 한라봉의 양을 입력해주세요=> "))

strawberry_eat=int(input("섭취한 딸기의 양을 입력해주세요=>"))

banana_eat=int(input("섭취한 바나나의 양을 입력해주세요=>"))
calories=[50/100, 34/100, 77/100] # 한라봉, 딸기, 바나나
total_calories=calories[0]*hallabong_eat + calories[1]*strawberry_eat + calories[2]*banana_eat

print(f"섭취하신 칼로리의 총량은 {total_calories} kcal 입니다.")