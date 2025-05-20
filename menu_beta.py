import os
import tkinter as tk
from tkinter import messagebox
import pygame
import subprocess
import sys
from PIL import Image, ImageTk
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
        self.frames = {}
        for F in (MainMenu, SettingsFrame, AuthFrame, StatsFrame,GeneralMenu,PickGeneralMenu):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)
        self.current_user = None
        self.show_frame(MainMenu)
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()
        if hasattr(frame, 'update_view'):
            frame.update_view()

class GeneralMenu(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.app = master
        container=tk.Frame(self)
        container.pack(expand=True)
        label= tk.Label(container, text="Оберіть режим гри", font=('Arial', 18))
        label.grid(row=0, column=0,columnspan=2,pady=(0,35))
        buton_vanil=tk.Button(container, text="Звичайний режим",
                  command=self.start_game)
        buton_vanil.grid(row=1, column=0,pady=(0,10), padx=(0,30))
        buton_general=tk.Button(container, text="Режим генералів",
                  command=lambda: master.show_frame(PickGeneralMenu))
        buton_general.grid(row=1, column=1,pady=(0,10), padx=(0,30))

    def start_game(self):
        game_script = r'D:\Husevukidezki\project\project.py'
        if self.app.current_user:
            nick = self.app.current_user['nick']
        else:
            nick = ''
        subprocess.Popen([sys.executable, game_script,"vanilla",nick])
        self.master.destroy()

class PickGeneralMenu(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.gen=generals
        self.index=0
        left = tk.Frame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        left.columnconfigure(0, weight=1)
        right = tk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        self.label=tk.Label(left,text="Обери генерала  ",font=('Arial',18))
        self.label.grid(row=0,column=2,columnspan=1,pady=(30,30), padx=(0,100))
        self.image_label=tk.Label(right)
        self.image_label.grid(row=0,column=3,columnspan=1)
        self.text_label=tk.Label(left,text=" ",font="Arial,13",wraplength=400)
        self.text_label.grid(row=1, column=1, columnspan=2, pady=(0, 20), sticky="nsew")
        btn_choose=tk.Button(left,text="Обрати Генерала",command=self.choose)
        btn_choose.grid(row=3,column=0, pady=(10,10))
        btn_next=tk.Button(left,text="Наступний Генерал",command=self.next)
        btn_next.grid(row=3,column=1,pady=(10,10))
        self.show()

    def show(self):
        gen=self.gen[self.index]
        img=Image.open(gen['image_path'])
        img = img.resize((600, 600), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.photo)
        self.text_label.config(text=f"{gen['name']}\n\n{gen['descripthion']}")

    def choose(self):
        chosen = self.gen[self.index]
        general_name = chosen['name']
        game_script = r'D:\Husevukidezki\project\project.py'
        user = self.master.current_user
        if user is not None:
            nick = user['nick']
        else:
            nick = ""   

        subprocess.Popen([sys.executable,game_script,general_name,nick])
        self.master.destroy()
    def next(self):
        self.index=self.index+1
        if self.index==3: self.index=0
        self.show()
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
        global user
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

generals=[
    
    {'name':'Глоріус Олексійович',
    'descripthion':'Веде за собою гільдію сміливих воїнів. Особлива здібність: кожні 10 кроків випускає ПОТУЖНУ бомбу, що взривається хрестом ',
    'image_path':'project\image_folder\knigts_image.png'

    },
    {'name':'Демон Матіуасан',
    'descripthion':'Веде за собою потвор з пекла. Особлива здібність: тричі за гру може підірвати свій випадковий корабель, аби той розлетіся на шмаття та поцілив в 4n клітинок ворога, де n-кількість палуб знищеного корабля',
    'image_path':'project\image_folder\demon_image.png'

    },
    {'name':'Денис Підривник',
    'descripthion':'Веде за собою мерзотників з усіх країн світу. Особлива здібність: коли по коралям Джонса потрапляє ворог, то з імовірність в 50% поцілить в випадкову клітинку ворога',
    'image_path':'project\image_folder\pirates_image.png'

    }
]
if __name__ == '__main__':
    app = BattleshipApp()
    app.mainloop()
