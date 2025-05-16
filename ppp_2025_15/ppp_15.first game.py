    #초성게임
import random

chosung_list = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
def to_chosung_ch(ch):
    return chosung_list[(ord(ch) - ord('가')) // 588]


def to_chosung(text):
    full_text = []
    for ch in text:
        full_text.append(to_chosung_ch(ch))
    return full_text


def main():
    problems = ["바나나", "딸기", "토마토", "복숭아","사과"]

    solution = problems[random.randrange(len(problems))]
    is_correct= False


    for i in range(3):
        answer = input(f"{','.join(to_chosung(solution))}가 초성인 단어는? => ")

        if answer == solution:
            print("정답입니다.")
            is_correct= True
            break
        else:
            print("오답입니다")
    
    if is_correct:
        print("축하합니다.")

    else:
        print("다시 해보세요.")
if __name__ == "__main__":
    main()



