# Author: Mario Bezuidenhout : Memorize Sequence
import tkinter as tk
from tkinter import *
import random
from functools import partial
from tkinter import messagebox


class Sim():
    btn_color = ('#ff0800', 'green', '#ffc30b', 'purple', 'blue',
                 '#56002f', '#2e1503', '#fc6b02', '#184343')
    flash_color = ('#ff6b6b', '#b0f895', '#fff666', '#c567a4',
                   '#8fd3fe', '#c9699d', '#6d4e46', '#ff9d5c', '#80a1b0')

    flash_on = 750
    flash_off = 250

    def __init__(self, title='Memorize Number Game'):
        # Creating the window:
        self.root = tk.Tk()
        self.root.title('Memorize Sequence')
        self.root.resizable(False, False)
        self.title = title
        self.root.geometry('1070x620')
        self.root.config(bg='#254e58')

        # Create frame for buttons:
        control_frame = Frame(self.root)
        control_frame.config(bg='#112d32', pady=3, padx=3)
        control_frame.place(x=320, y=150)

        # Creating labels:
        your_score_lbl = Label(self.root, text='YOUR SCORE:', relief=FLAT,
                               font=("arial", 12, 'bold italic'), bg='#254e58', fg='white')
        your_score_lbl.place(x=10, y=180, anchor='w')

        best_score_lbl = Label(self.root, text='BEST SCORE:', relief=FLAT,
                               font=("arial", 12, 'bold italic'), bg='#254e58', fg='white')
        best_score_lbl.place(x=950, y=180, anchor='se')

        # Creating buttons:
        self.buttons = [
            tk.Button(
                control_frame,
                height=6,
                width=17,
                background=c,
                activebackground=c,
                command=partial(self.Push, i))
            for i, c in enumerate(self.btn_color)]

        # Positioning the buttons:
        for i, button in enumerate(self.buttons):
            button.grid({'column': i % 3, 'row': i // 3}, pady=3, padx=3)

    ############################################################# FUNCTIONS #############################################################

    def Start_Countdown(self, time_countdown=3):
        i = 1

        # Creating frame:
        control_countdown = Frame(self.root)
        control_countdown.place(x=420, y=490)

        # Creating label:
        count_down = Label(control_countdown, text=str(time_countdown), relief=FLAT, font=(
            'arial black', 22), bg='#254e58', fg='white', height=1, width=11)
        count_down.pack()

        # Countdown process:
        if(i == 1):
            count_down.config(text=str(time_countdown))
            if(time_countdown > 0):
                control_countdown.after(
                    1000, self.Start_Countdown, time_countdown - 1)
            if(time_countdown == 0):
                count_down.config(text='GO!!!', fg='white', bg='#254e58')
                control_countdown.after(
                    1000, count_down.pack_forget)
                control_countdown.config(bg='#254e58')
                self.root.after(1000, self.Reset)

    def Push(self, index):
        # Creating labels:
        your_score_container = Label(self.root, text=' ', relief=FLAT, font=(
            'arial bold', 15), bg='#254e58', fg='white')

        game_over = Label(self.root, text='GAME OVER', relief=FLAT,
                          font=("arial bold", 17), bg='#254e58', fg='white')

        best_score_container = Label(self.root, text=' ', relief=FLAT, font=(
            'arial bold', 15), bg='#254e58', fg='white')

        if index == self.current:
            try:
                self.current = next(self.iterator)
            except StopIteration:
                your_score_container['text'] = str(len(self.sequence))
                your_score_container.place(x=150, y=165)
                self.Change_Color()
        else:
            game_over.place(x=460, y=70)
            answer = messagebox.askquestion(
                'Confirmation', 'Do you want to exit?')

            if(answer == 'yes'):
                self.root.quit()
            else:
                game_over['text'] = ' '
                user_best_score = len(self.sequence) - 1
                best_score_container['text'] = str(user_best_score)
                best_score_container.place(x=970, y=154)
                self.Start_Countdown()

    def Reset(self):
        self.sequence = []
        self.Change_Color()

    def Change_Color(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        color = random.randrange(0, len(self.buttons))
        self.sequence.append(color)
        self.iterator = iter(self.sequence)
        self.Show_Tile()

    # function will flash a random tile:
    def Show_Tile(self):
        try:
            id = next(self.iterator)
        except StopIteration:
            # No more tiles to show, start waiting for user input
            self.iterator = iter(self.sequence)
            self.current = next(self.iterator)
            for button in self.buttons:
                button.config(state=tk.NORMAL)
        else:
            self.buttons[id].config(background=self.flash_color[id])
            self.root.after(self.flash_on, self.Hide_Tile)

    # function will 'turn off' the randomly flashed tile:
    def Hide_Tile(self):
        for button, color in zip(self.buttons, self.btn_color):
            button.config(background=color)
        self.root.after(self.flash_off, self.Show_Tile)

    def Run(self):
        self.Start_Countdown()
        self.root.mainloop()


if __name__ == '__main__':
    game = Sim()
    game.Run()
