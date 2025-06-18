from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
THEME_LIGHT = {"bg": "#f7f5dd", "fg": "#444", "highlight": "#a3d9ff"}
THEME_DARK = {"bg": "#2c2c2c", "fg": "#d0e1f9", "highlight": "#5dade2"}

FONT_NAME = "Courier"
reps = 0
timer = None
is_paused = False
paused_time = 0
current_theme = THEME_LIGHT

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, is_paused, paused_time
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=current_theme['fg'])
    check_marks.config(text="")
    reps = 0
    is_paused = False
    paused_time = 0

# ---------------------------- TIMER START ------------------------------- #
def start_timer():
    global reps, is_paused
    if is_paused:
        count_down(paused_time)
        is_paused = False
        return

    reps += 1

    work_sec = int(work_input.get()) * 60
    short_break_sec = int(short_break_input.get()) * 60
    long_break_sec = int(long_break_input.get()) * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="Long Break", fg="red")
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="Short Break", fg="pink")
    else:
        count_down(work_sec)
        title_label.config(text="Work", fg="green")

# ---------------------------- COUNTDOWN ------------------------------- #
def count_down(count):
    global timer, paused_time
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        paused_time = count
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = "✔" * (reps // 2)
        check_marks.config(text=marks)

# ---------------------------- PAUSE ------------------------------- #
def pause_timer():
    global is_paused
    if timer:
        window.after_cancel(timer)
        is_paused = True

# ---------------------------- THEME TOGGLE ------------------------------- #
def toggle_theme():
    global current_theme
    current_theme = THEME_DARK if current_theme == THEME_LIGHT else THEME_LIGHT
    apply_theme()

def apply_theme():
    window.config(bg=current_theme['bg'])
    canvas.config(bg=current_theme['bg'])
    title_label.config(bg=current_theme['bg'], fg=current_theme['fg'])
    check_marks.config(bg=current_theme['bg'], fg=current_theme['fg'])
    for widget in [start_button, reset_button, pause_button, theme_button]:
        widget.config(highlightbackground=current_theme['highlight'])

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Personal Pomodoro Timer")
window.config(padx=100, pady=50)

canvas = Canvas(width=200, height=224, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill='black', font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

title_label = Label(text="Timer", font=(FONT_NAME, 40))
title_label.grid(row=0, column=1)

check_marks = Label(font=(FONT_NAME, 15))
check_marks.grid(row=4, column=1)

# Inputs for custom durations
work_input = Entry(width=5)
work_input.insert(0, "25")
work_input.grid(row=2, column=0)
Label(text="Work (min)").grid(row=3, column=0)

short_break_input = Entry(width=5)
short_break_input.insert(0, "5")
short_break_input.grid(row=2, column=1)
Label(text="Short Break").grid(row=3, column=1)

long_break_input = Entry(width=5)
long_break_input.insert(0, "20")
long_break_input.grid(row=2, column=2)
Label(text="Long Break").grid(row=3, column=2)

# Buttons
start_button = Button(text="Start", command=start_timer)
start_button.grid(row=5, column=0)

pause_button = Button(text="Pause", command=pause_timer)
pause_button.grid(row=5, column=1)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.grid(row=5, column=2)

theme_button = Button(text="Toggle Theme", command=toggle_theme)
theme_button.grid(row=6, column=1)

apply_theme()
window.mainloop()
