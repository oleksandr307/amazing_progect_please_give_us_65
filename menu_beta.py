import os
import tkinter as tk
from tkinter import messagebox
import pygame
import subprocess
import sys
pygame.mixer.init()
pygame.mixer.music.load('project/menu_mus_1.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)
General=None
USER_FILE = 'project/users_info.txt'

def load_users():
    users = []
    if not os.path.exists(USER_FILE):
        return users
    with open(USER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            data = {}
            for part in parts:
                key, val = part.split('=', 1)
                data[key] = val.strip().strip('"')
            for field in ('exp', 'games', 'wins'):
                data[field] = int(data.get(field, 0))
            users.append(data)
    return users


def authorize(nick, pw):
    for u in load_users():
        if u['nick'] == nick and u['pw'] == pw:
            return u
    return None


class BattleshipApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Морський бій")
        self.attributes('-fullscreen', True)
        self.current_user = None

        self.frames = {}
        for F in (MainMenu, SettingsFrame, AuthFrame, StatsFrame,GeneralMenu,PickGeneralMenu):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(MainMenu)
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        if hasattr(frame, 'update_view'):
            frame.update_view()

class GeneralMenu(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        container=tk.Frame(self)
        container.pack(pady=40)
        tk.Label(self, text="Оберіть режим гри", font=('Arial', 18)).pack(pady=50)
        tk.Button(container, text="Звичайний режим",
                  command=self.start_game).pack(fill='x', padx=40, pady=30)
        tk.Button(container, text="Режим генералів",
                  command=lambda: master.show_frame(PickGeneralMenu)).pack(fill='x', padx=40, pady=30)
        
    def start_game(self):
        game_script = r'D:\Husevukidezki\project\project.py'
        subprocess.Popen([sys.executable, game_script])
        self.master.destroy()

class PickGeneralMenu(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        container=tk.Frame(self)
        container.pack(pady=40)
        tk.Label(self,text="Обери генерала")
class MainMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Морський Бій 1: Нова Надія", font=('Arial', 18)).pack(pady=50)
        tk.Button(self, text="Почати гру",
                  command=lambda: master.show_frame(GeneralMenu)).pack(fill='x', padx=40, pady=30)
        tk.Button(self, text="Авторизація",
                  command=lambda: master.show_frame(AuthFrame)).pack(fill='x', padx=50, pady=30)
        tk.Button(self, text="Налаштування",
                  command=lambda: master.show_frame(SettingsFrame)).pack(fill='x', padx=50, pady=30)
        tk.Button(self, text="Статистика",
                  command=lambda: master.show_frame(StatsFrame)).pack(fill='x', padx=50, pady=30)
        tk.Button(self, text="Вихід", command=master.quit).pack(fill='x', padx=50, pady=30)
        tk.Label(self, text="by Sokolov&Husevyk team", font=('Arial', 9)).pack(side='bottom')
    def start_game(self):
        game_script = r'D:\Husevukidezki\project\project.py'
        subprocess.Popen([sys.executable, game_script])
        self.master.destroy()

class SettingsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Налаштування звуку").pack(pady=10)

        self.vol_scale = tk.Scale(self,
                                  from_=0, to=100,
                                  orient='horizontal',
                                  label='Гучність музики',
                                  command=self.on_volume_change)
        self.vol_scale.set(50)
        self.vol_scale.pack(padx=20, pady=20)

        tk.Button(self, text="Назад",
                  command=lambda: master.show_frame(MainMenu)).pack(pady=10)

    def on_volume_change(self, value):
        vol = float(value) / 100.0
        pygame.mixer.music.set_volume(vol)


class AuthFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        form = tk.Frame(self)
        form.pack(expand=True)

        self.nick_var = tk.StringVar()
        self.pw_var = tk.StringVar()

        tk.Label(form, text="Нік:").pack(pady=(0, 5))
        tk.Entry(form, textvariable=self.nick_var).pack(pady=(0, 15))

        tk.Label(form, text="Пароль:").pack(pady=(0, 5))
        tk.Entry(form, textvariable=self.pw_var, show='*').pack(pady=(0, 15))

        tk.Button(form, text="Увійти", command=self.login).pack(pady=(0, 5))
        tk.Button(form, text="Зареєструватися", command=self.sign).pack(pady=(0, 5))
        tk.Button(form, text="Назад",
                  command=lambda: master.show_frame(MainMenu)).pack()

    def sign(self):
        with open (USER_FILE, 'a',encoding='utf-8') as f:
            nick = self.nick_var.get().strip()
            pw   = self.pw_var.get().strip()
            line=f'nick="{nick}",pw="{pw}",exp="0",games="0",wins="0"\n'
            f.write(line)
            messagebox.showinfo("Успіх", f"Вітаю, {nick}!")

    def login(self):
        nick = self.nick_var.get().strip()
        pw = self.pw_var.get().strip()
        user = authorize(nick, pw)
        if user:
            self.master.current_user = user
            messagebox.showinfo("Успіх", f"Вітаю, {nick}!")
            self.master.show_frame(MainMenu)
        else:
            messagebox.showerror("Помилка", "Невірний нік або пароль")


class StatsFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Статистика", font=('Arial', 14)).pack(pady=10)

        self.stat_label = tk.Label(self, text="", justify='left', font=('Arial', 12))
        self.stat_label.pack(pady=5)

        tk.Button(self, text="Назад",
                  command=lambda: master.show_frame(MainMenu)).pack(pady=20)

    def update_view(self):
        user = self.master.current_user
        if user:
            txt = (
                f"Нік: {user['nick']}\n"
                f"Досвід: {user['exp']}\n"
                f"Ігор зіграно: {user['games']}\n"
                f"Перемог: {user['wins']}\n"
                f"Відсоток перемог: {user['wins'] / user['games'] * 100:.1f}%"
            )
        else:
            txt = "Спочатку авторизуйтеся."
        self.stat_label.config(text=txt)


if __name__ == '__main__':
    app = BattleshipApp()
    app.mainloop()
