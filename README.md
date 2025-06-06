# Stop Addiction Tracker (SAT)

🚭 A lightweight Windows desktop app to help you quit smoking (and soda!).  
✔️ Tracks daily progress  
✔️ Motivates you with quotes  
✔️ Shows money saved and habits broken  
✔️ Multilingual + graphical reports

## Features
- Checkboxes for soda rinse and no-smoking periods (08–24h)
- Visual progress charts (bar + line graph)
- Automatic reminders
- Local language and currency detection
- No console – runs as a full desktop app with icon

## Installation
1. Install requirements:
   ```bash
   pip install matplotlib plyer
# stop_addiction_tracker

🚀 Run aplikacije (dev način)
Potrebno: Python 3.11+ i instalirane zavisnosti

bash
Copy
Edit
pip install matplotlib plyer
python "Stop Addiction Tracker.py"
🏗️ Build .exe (Windows)
Potrebno: pyinstaller i .ico fajl

bash
Copy
Edit
pip install pyinstaller
pyinstaller --onefile --windowed --icon=stop_addiction.ico "Stop Addiction Tracker.py"
Output .exe će se nalaziti u dist/ direktorijumu.

Application tracking your addiction
