import tkinter as tk
import datetime
import os
from tkinter import messagebox
import subprocess

BOX_SIZE = 20
PADDING = 4

COLORS = [
    "#ebedf0",  # 0 commit
    "#9be9a8",  # 1 commit
    "#40c463",  # 2 commits
    "#30a14e",  # 3 commits
    "#216e39",  # 4+ commits
]

NAME_GITHUB = ""
EMAIL_GITHUB = ""
GITHUB_REMOTE_URL = "https://github.com/PaulSchemith/Github-Calendar-Stamp.git"
BRANCH_NAME = "main"

class Tooltip:
    """Simple tooltip widget for tkinter widgets"""
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None

    def show(self, text, x, y):
        self.hide()
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, background="#ffffe0", relief="solid", borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=2)

    def hide(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

class GithubCalendarSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GitHub Calendar Stamp")
        self.commit_data = {}

        self.today = datetime.date.today()

        self.start_date = self.today - datetime.timedelta(days=365)
        while self.start_date.weekday() != 6:
            self.start_date -= datetime.timedelta(days=1)

        # 53 colonnes (semaines) * 7 lignes (jours)
        self.num_weeks = 53
        self.num_days = 7

        canvas_height = self.num_days*(BOX_SIZE+PADDING) + 70
        canvas_width = self.num_weeks*(BOX_SIZE+PADDING)
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack()

        self.rectangles = {}
        self.date_for_rect = {}

        self.is_painting = False
        self.is_erasing = False

        self.draw_grid()
        self.draw_legend()

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

        self.canvas.bind("<ButtonPress-3>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_release)
        self.canvas.bind("<B3-Motion>", self.on_mouse_drag)

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", lambda e: self.tooltip.hide())

        self.tooltip = Tooltip(self.canvas)
        self.btn = tk.Button(self, text="Valider & Pousser", command=self.validate_and_push)
        self.btn.pack(pady=10)

    def date_from_pos(self, row, col):
        days_offset = col*7 + row
        return self.start_date + datetime.timedelta(days=days_offset)

    def draw_grid(self):
        for col in range(self.num_weeks):
            for row in range(self.num_days):
                date = self.date_from_pos(row, col)
                if date > self.today:
                    color = "#f0f0f0"
                else:
                    commits = self.commit_data.get(date, 0)
                    level = min(commits, 4)
                    color = COLORS[level]
                x1 = col*(BOX_SIZE+PADDING)
                y1 = row*(BOX_SIZE+PADDING)
                rect = self.canvas.create_rectangle(
                    x1, y1, x1+BOX_SIZE, y1+BOX_SIZE,
                    fill=color, outline="#ddd"
                )
                self.rectangles[(row, col)] = rect
                self.date_for_rect[rect] = date

    def update_cell(self, row, col):
        date = self.date_from_pos(row, col)
        if date > self.today:
            return
        
        self.commit_data[date] = self.commit_data.get(date, 0) + 1
        commits = self.commit_data[date]
        level = min(commits, 4)
        color = COLORS[level]
        rect_id = self.rectangles[(row, col)]
        self.canvas.itemconfig(rect_id, fill=color)

    def decrease_cell(self, row, col):
        date = self.date_from_pos(row, col)
        if date > self.today:
            return
        current = self.commit_data.get(date, 0)
        if current > 0:
            self.commit_data[date] = current - 1
            level = min(self.commit_data[date], 4)
            color = COLORS[level]
            rect_id = self.rectangles[(row, col)]
            self.canvas.itemconfig(rect_id, fill=color)
            if self.commit_data[date] == 0:
                del self.commit_data[date]

    def on_button_press(self, event):
        col = event.x // (BOX_SIZE + PADDING)
        row = event.y // (BOX_SIZE + PADDING)
        if 0 <= col < self.num_weeks and 0 <= row < self.num_days:
            if event.num == 1:  # clic gauche
                self.is_painting = True
                self.update_cell(row, col)
            elif event.num == 3:  # clic droit
                self.is_erasing = True
                self.decrease_cell(row, col)

    def on_button_release(self, event):
        if event.num == 1:
            self.is_painting = False
        elif event.num == 3:
            self.is_erasing = False

    def on_mouse_drag(self, event):
        col = event.x // (BOX_SIZE + PADDING)
        row = event.y // (BOX_SIZE + PADDING)
        if 0 <= col < self.num_weeks and 0 <= row < self.num_days:
            if self.is_painting:
                self.update_cell(row, col)
            elif self.is_erasing:
                self.decrease_cell(row, col)

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        items = self.canvas.find_overlapping(x, y, x, y)
        for item in items:
            if item in self.date_for_rect:
                date = self.date_for_rect[item]
                if date > self.today:
                    self.tooltip.hide()
                else:
                    self.tooltip.show(date.isoformat(), event.x_root + 10, event.y_root + 10)
                break
        else:
            self.tooltip.hide()

    def draw_legend(self):
        start_x = 10
        start_y = self.num_days*(BOX_SIZE+PADDING) + 10
        self.canvas.create_text(start_x, start_y, anchor="w", text="Légende :", font=("Arial", 12, "bold"))

        for i, color in enumerate(COLORS):
            x = start_x + 80 + i*(BOX_SIZE + PADDING)
            y = start_y - BOX_SIZE//2
            self.canvas.create_rectangle(x, y, x+BOX_SIZE, y+BOX_SIZE, fill=color, outline="#ddd")
            label = f"{i}" if i < 4 else "4+"
            self.canvas.create_text(x + BOX_SIZE//2, y + BOX_SIZE + 10, text=label, font=("Arial", 9))

    def make_commit(self, date, message="stamp"):
        git_date = date.strftime('%a %b %d %H:%M:%S %Y +0000')
        with open("log.txt", "a") as f:
            f.write(f"{date.isoformat()}: {message}\n")
        os.system("git add log.txt")
        os.system(f'GIT_AUTHOR_DATE="{git_date}" GIT_COMMITTER_DATE="{git_date}" git commit -m "{message}"')

    def setup_git(self):
        os.system(f'git config user.name "{NAME_GITHUB}"')
        os.system(f'git config user.email "{EMAIL_GITHUB}"')

    def setup_remote(self):
        if os.system("git remote get-url origin > /dev/null 2>&1") != 0:
            os.system(f"git remote add origin {GITHUB_REMOTE_URL}")

    def push_to_github(self):
        os.system(f"git push -u origin {BRANCH_NAME}")

    def validate_and_push(self):
        if not self.commit_data:
            messagebox.showwarning("Avertissement", "Aucun commit à envoyer.")
            return

        self.setup_git()
        self.setup_remote()

        for date, commits in sorted(self.commit_data.items()):
            for _ in range(commits):
                self.make_commit(date)

        self.push_to_github()
        messagebox.showinfo("Succès", "Commits poussés avec succès sur GitHub !")


if __name__ == "__main__":
    app = GithubCalendarSimulator()
    app.mainloop()
