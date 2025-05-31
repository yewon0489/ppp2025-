import tkinter as tk
from tkinter import simpledialog

window = tk.Tk()
window.withdraw()

def gui_input(text):
    return simpledialog.askstring(title="입력창", prompt=text)

def count_down(count):
    def update():
        nonlocal count
        if count > 0:
            label.config(text=f"{count}...")
            count -= 1
            window.after(1000, update)
        else:
            label.config(text="Bomb!!")
    
    window.deiconify()
    update()

def main():
    what_count = gui_input("몇 초 뒤 폭발합니까?")
    if what_count is None:
        print("취소되었습니다.")
        return
    
    try:
        count = int(what_count)
        count_down(count)
        window.mainloop()
    except ValueError:
        print("숫자를 입력하세요.")

label = tk.Label(window, text="", font=("Arial", 32))
label.pack(expand=True)

if __name__ == "__main__":
    main()