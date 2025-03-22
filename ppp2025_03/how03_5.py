hallabong_eat=int(input("몇 그램의 한라봉을 먹었는지 입력해주세요=>"))
strawberry_eat=int(input("몇 그램의 딸기를 먹었는지 입력해주세요=>"))
banana_eat=int(input("몇 그램의 바나나를 먹었는지 입력해주세요=>"))
hallabong_caloreis=hallabong_eat*50/100
strawberry_caloreis=strawberry_eat*34/100
banana_caloreis=banana_eat*77/100
total_caloreis=(hallabong_caloreis)+(strawberry_caloreis)+(banana_caloreis)
print(f"섭취한 전체 칼로리는 {total_caloreis:.2f} kcal 입니다.")
