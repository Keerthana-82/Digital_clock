import tkinter as tk
from time import strftime, localtime
import winsound

class SmartClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Clock")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        # ---------- STATE ----------
        self.is_24hr = True
        self.theme = "dark"
        self.running = True
        self.animation_on = True
        self.clock_shape = "circle"

        # ---------- COLORS ----------
        self.dark_bg = "#0f172a"
        self.light_bg = "#f8fafc"
        self.text_dark = "#e0f2fe"
        self.text_light = "#020617"
        self.accent = "#38bdf8"

        self.root.configure(bg=self.dark_bg)

        self.canvas = tk.Canvas(self.root, bg=self.dark_bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.center_x, self.center_y = 450, 300

        self.draw_ui()

        # Settings button
        self.settings_btn = tk.Button(
            self.root, text="⚙ Settings",
            font=("Segoe UI", 12, "bold"),
            command=self.open_settings
        )
        self.settings_btn.place(x=20, y=20)

        self.update_clock()

    # ---------- UI ----------
    def draw_ui(self):
        self.canvas.delete("all")

        if self.clock_shape == "circle":
            self.canvas.create_oval(
                self.center_x-160, self.center_y-160,
                self.center_x+160, self.center_y+160,
                outline=self.accent, width=4
            )

        elif self.clock_shape == "double":
            self.canvas.create_oval(
                self.center_x-170, self.center_y-170,
                self.center_x+170, self.center_y+170,
                outline=self.accent, width=2
            )
            self.canvas.create_oval(
                self.center_x-150, self.center_y-150,
                self.center_x+150, self.center_y+150,
                outline="#7dd3fc", width=4
            )

        elif self.clock_shape == "square":
            self.canvas.create_rectangle(
                self.center_x-160, self.center_y-160,
                self.center_x+160, self.center_y+160,
                outline=self.accent, width=4
            )

        self.time_text = self.canvas.create_text(
            self.center_x, self.center_y-10,
            font=("Segoe UI", 42, "bold"),
            fill=self.text_dark
        )

        self.date_text = self.canvas.create_text(
            self.center_x, self.center_y+40,
            font=("Segoe UI", 16),
            fill="#7dd3fc"
        )

    # ---------- SOUND ----------
    def play_tick(self):
        winsound.Beep(1200, 40)

    def play_hour_chime(self):
        winsound.Beep(600, 300)
        winsound.Beep(800, 300)

    # ---------- CLOCK ----------
    def update_clock(self):
        if self.running:
            now = localtime()
            fmt = "%H:%M:%S" if self.is_24hr else "%I:%M:%S %p"

            self.canvas.itemconfig(self.time_text, text=strftime(fmt, now))
            self.canvas.itemconfig(
                self.date_text,
                text=strftime("%A • %d %B %Y", now)
            )

            # Tick sound every second
            self.play_tick()

            # Hour chime
            if now.tm_min == 0 and now.tm_sec == 0:
                self.play_hour_chime()

        self.root.after(1000, self.update_clock)

    # ---------- SETTINGS ----------
    def open_settings(self):
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("300x360")
        settings.resizable(False, False)

        tk.Label(
            settings, text="Clock Settings",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        tk.Button(
            settings, text="Toggle 12 / 24 Hour",
            command=self.toggle_format
        ).pack(pady=8)

        tk.Button(
            settings, text="Switch Theme",
            command=self.toggle_theme
        ).pack(pady=8)

        tk.Button(
            settings, text="Pause / Resume Clock",
            command=self.toggle_running
        ).pack(pady=8)

        tk.Button(
            settings, text="Change Clock Shape",
            command=self.change_shape
        ).pack(pady=8)

        tk.Button(
            settings, text="Sound Effect",
            command=self.sound_pause
        ).pack(pady=8)

        tk.Button(
            settings, text="Exit",
            command=settings.destroy
        ).pack(pady=15)

    # ---------- ACTIONS ----------
    def toggle_format(self):
        self.is_24hr = not self.is_24hr

    def toggle_theme(self):
        if self.theme == "dark":
            self.theme = "light"
            self.root.config(bg=self.light_bg)
            self.canvas.config(bg=self.light_bg)
            self.canvas.itemconfig(self.time_text, fill=self.text_light)
        else:
            self.theme = "dark"
            self.root.config(bg=self.dark_bg)
            self.canvas.config(bg=self.dark_bg)
            self.canvas.itemconfig(self.time_text, fill=self.text_dark)

    def toggle_running(self):
        self.running = not self.running

    def change_shape(self):
        shapes = ["circle", "double", "square"]
        index = shapes.index(self.clock_shape)
        self.clock_shape = shapes[(index + 1) % len(shapes)]
        self.draw_ui()


# ---------- RUN ----------
if __name__ == "__main__":
    root = tk.Tk()
    SmartClock(root)
    root.mainloop()
