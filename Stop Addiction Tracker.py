import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import random
import os
import locale

DATA_FILE = "progress.json"
SETTINGS_FILE = "user_settings.json"

# Load existing data if available
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(date, entry):
    data = load_data()
    data[date] = entry
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return None

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def load_quotes(language):
    try:
        with open("quotes.json", "r", encoding="utf-8") as f:
            quotes_data = json.load(f)
        return quotes_data.get(language, quotes_data.get("en", []))
    except FileNotFoundError:
        return []

class TrackerApp:
    def load_translations(self, lang):
        try:
            with open("translations.json", "r", encoding="utf-8") as f:
                translations = json.load(f)
            return translations.get(lang, translations.get("en", {}))
        except FileNotFoundError:
            return {}

    def __init__(self, root):
        self.root = root
        lang_code = locale.getdefaultlocale()[0][:2]
        self.translations = self.load_translations(lang_code)
        self.root.title(self.translations.get("title", "Stop Addiction Tracker"))

        self.date = datetime.now().strftime("%Y-%m-%d")

        # Load or ask user settings
        self.settings = load_settings()
        if not self.settings:
            self.settings = {}
            self.ask_user_settings()
            save_settings(self.settings)

        self.cigs_per_day = int(self.settings["cigarettes_per_day"])
        self.price_per_pack = float(self.settings["pack_price"])
        self.currency = self.settings["currency"]

        lang_code = locale.getdefaultlocale()[0][:2]
        self.quotes = load_quotes(lang_code)
        quote = random.choice(self.quotes) if self.quotes else "Stay strong. You're doing great!"
        tk.Label(root, text=quote, wraplength=400, justify="left", fg="gray").grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.vars = {
            "no_smoke": tk.IntVar(),
            "no_soda": tk.IntVar(),
            "soda_rinse_1": tk.IntVar(),
            "soda_rinse_2": tk.IntVar(),
            "soda_rinse_3": tk.IntVar(),
            "pastila_or_ice": tk.IntVar(),
            "herbal_tea": tk.IntVar(),
            "walk": tk.IntVar()
        }

        row = 1
        tk.Label(root, text=self.translations.get("day_label", f"Dan: {self.date}"), font=("Arial", 14, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        for label, var in self.vars.items():
            if label.startswith("soda_rinse"):
                text = "Soda rinse"
            else:
                text = label.replace("_", " ").capitalize()
            tk.Checkbutton(root, text=text, variable=var).grid(row=row, column=0, sticky="w")
            row += 1

        tk.Label(root, text=self.translations.get("stress_label", "Stres (1 = miran, 5 = visok)")).grid(row=row, column=0, sticky="w")
        self.stress_scale = tk.Scale(root, from_=1, to=5, orient="horizontal")
        self.stress_scale.set(3)
        self.stress_scale.grid(row=row, column=1)
        row += 1

        tk.Label(root, text=self.translations.get("comment_label", "Komentar / Osećaj")).grid(row=row, column=0, sticky="w")
        self.comment = tk.Text(root, height=3, width=40)
        self.comment.grid(row=row, column=1)
        row += 1

        tk.Button(root, text=self.translations.get("save_entry", "Sačuvaj unos"), command=self.save_entry).grid(row=row, column=0, pady=10)
        tk.Button(root, text=self.translations.get("show_history", "Prikaži istoriju"), command=self.show_history).grid(row=row, column=1, pady=10)
        row += 1

        tk.Button(root, text=self.translations.get("show_graph", "Prikaži grafikon"), command=self.show_graph).grid(row=row, column=0, columnspan=2, pady=10)

    def ask_user_settings(self):
        self.settings["cigarettes_per_day"] = simpledialog.askstring("Unos", "Koliko cigareta dnevno pušite?", initialvalue="30")
        self.settings["pack_price"] = simpledialog.askstring("Unos", "Koliko košta kutija cigareta koju pušite?", initialvalue="460")
        self.settings["candy_price"] = simpledialog.askstring("Unos", "Koja je cena bombonica koje koristite (dnevna potrošnja)?", initialvalue="100")

        system_locale = locale.getdefaultlocale()[0]
        if system_locale and system_locale.startswith("sr"):
            self.settings["currency"] = "RSD"
        elif system_locale and system_locale.startswith("en_US"):
            self.settings["currency"] = "$"
        elif system_locale and system_locale.startswith("de") or "EU" in system_locale:
            self.settings["currency"] = "€"
        else:
            self.settings["currency"] = "$"

    def save_entry(self):
        entry = {key: var.get() for key, var in self.vars.items()}
        entry["stress"] = self.stress_scale.get()
        entry["comment"] = self.comment.get("1.0", tk.END).strip()

        save_data(self.date, entry)
        messagebox.showinfo(self.translations.get("success_title", "Uspeh"), self.translations.get("entry_saved", "Današnji unos je sačuvan!"))

    def show_history(self):
        data = load_data()
        history_window = Toplevel(self.root)
        history_window.title(self.translations.get("history_title", "Istorija unosa"))

        text_area = scrolledtext.ScrolledText(history_window, width=80, height=20)
        text_area.pack(padx=10, pady=10)

        if not data:
            text_area.insert(tk.END, self.translations.get("no_data", "Nema podataka za prikaz."))
        else:
            for date, entry in sorted(data.items()):
                text_area.insert(tk.END, f"Datum: {date}\n")
                for key, value in entry.items():
                    text_area.insert(tk.END, f"  {key.replace('_', ' ').capitalize()}: {value}\n")
                text_area.insert(tk.END, "\n")
        text_area.config(state="disabled")

    def show_graph(self):
        data = load_data()
        if not data:
            messagebox.showinfo(self.translations.get("graph_title", "Grafikon"), self.translations.get("no_graph_data", "Nema dovoljno podataka za prikaz grafikona."))
            return

        # General summary
        total_days = len(data)
        total_cigs = total_days * self.cigs_per_day
        candy_cost = float(self.settings.get("candy_price", 0)) * total_days
        total_savings = ((self.price_per_pack / 20) * total_cigs) - candy_cost

        labels = ['Cigarete izbegnute', 'Ušteda (neto)']
        values = [total_cigs, total_savings]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))

        ax1.bar(labels, values, color=['orange', 'green'])
        ax1.set_title(self.translations.get("progress_title", "Napredak bez pušenja"))
        ax1.set_ylabel(self.translations.get("y_axis_label", "Broj / Vrednost"))

        # Daily net savings line chart
        dates = []
        savings = []
        price_per_cig = self.price_per_pack / 20
        candy_price = float(self.settings.get("candy_price", 0))

        for date_str in sorted(data.keys()):
            day_data = data[date_str]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if day_data.get("no_smoke"):
                daily_savings = (self.cigs_per_day * price_per_cig) - candy_price
                savings.append(daily_savings)
            else:
                savings.append(-candy_price)
            dates.append(date_obj.strftime("%d.%m"))

        ax2.plot(dates, savings, marker='o', linestyle='-', color='blue')
        ax2.set_title(self.translations.get("daily_progress_title", "Dnevna neto ušteda"))
        ax2.set_ylabel(self.translations.get("y_axis_label", "Broj / Vrednost"))
        ax2.set_xticks(range(len(dates)))
        ax2.set_xticklabels(dates, rotation=45)

        graph_window = Toplevel(self.root)
        graph_window.title(self.translations.get("graph_title", "Statistika"))

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackerApp(root)
    root.mainloop()
