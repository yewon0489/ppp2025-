import random
import tkinter as tk

problems = ["apple", "banana", "orange", "grape", "strawberry", "water melon", "pineapple"]
solution = problems[random.randrange(len(problems))]
is_correct = False
lives = 3
answer = ["_" for _ in range(len(solution))]

def check(solution, answer, input_ch):
    is_correct = False
    for i in range(len(solution)):
        if solution[i] == input_ch:
            answer[i] = input_ch
            is_correct = True
    return is_correct

def end():
    if is_correct:
        result_label.config(text=f"정답!!! {solution}")
    else:
        result_label.config(text=f"다시 해보세요. 정답: {solution}")
    submit_btn.config(state="disabled")

def submit():
    global lives, is_correct
    input_ch = gui_input()
    entry.delete(0, tk.END)

    if len(input_ch) != 1:
        info_label.config(text="한 글자만 입력하세요!")
        return

    if check(solution, answer, input_ch):
        info_label.config(text=f"'{input_ch}'가 포함되어 있습니다.")
    else:
        lives -= 1
        info_label.config(text=f"틀렸어요! 남은 기회: {lives}")

    word_label.config(text="현재 단어: " + "".join(answer))

    if "_" not in answer:
        is_correct = True
        end()
    elif lives == 0:
        end()

def gui_input():
    return entry.get()

window = tk.Tk()
window.title("단어 맞추기 게임")
window.geometry("400x300")

word_label = tk.Label(window, text="현재 단어: " + "".join(answer), font=("Arial", 16))
word_label.pack(pady=10)

entry = tk.Entry(window, font=("Arial", 14))
entry.pack()

submit_btn = tk.Button(window, text="입력", command=submit, font=("Arial", 14))
submit_btn.pack(pady=10)

info_label = tk.Label(window, text="글자 하나를 입력하세요.", font=("Arial", 12))
info_label.pack()

result_label = tk.Label(window, text="", font=("Arial", 14), fg="blue")
result_label.pack(pady=10)

window.mainloop()
