import json
import os
import random
import time
import sys
from datetime import datetime
import subprocess

# === AUTO INSTALL COLORAMA ===
try:
    from colorama import init, Fore, Style
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Style

init(autoreset=True)

try:
    import winsound
    is_windows = True
except ImportError:
    is_windows = False

# === FUNGSI WARNA (GANTI KE COLORAMA) ===
def warna(teks, color):
    return f"{color}{teks}{Style.RESET_ALL}"

# === BERSIHKAN LAYAR ===
os.system('cls' if os.name == 'nt' else 'clear')

# === BUAT FOLDER PAITO ===
if not os.path.exists("paito"):
    os.makedirs("paito")

# === JUDUL ===
judul = "\n=============================\n   MESIN BBFS TOGEL\n=============================\n"
print(warna(judul, Fore.LIGHTRED_EX))

# === DAFTAR PASARAN ===
pasaran_list = [
    "Hongkong Pool",
    "Hongkong Lotto",
    "Sydney Pool",
    "Sydney Lotto",
    "China",
    "Singapore",
    "Taiwan"
]

print(warna("Pilih Pasaran:", Fore.LIGHTYELLOW_EX))
for idx, p in enumerate(pasaran_list, 1):
    print(f"{idx}. {p}")

try:
    idx = int(input(warna("\nMasukkan nomor pasaran (1-7): ", Fore.LIGHTYELLOW_EX))) - 1
    pasaran = pasaran_list[idx].replace(" ", "_").lower()
except:
    print(warna("Pilihan tidak valid!", Fore.LIGHTRED_EX))
    sys.exit()

file_data = f"paito/data_{pasaran}.json"

# === LOAD / BUAT DATA ===
if os.path.exists(file_data):
    with open(file_data) as f:
        history = json.load(f)
else:
    history = []

today = datetime.now().strftime("%Y-%m-%d")
if history and history[-1]['date'] == today:
    print(warna(f"\nData keluaran terbaru untuk {pasaran.replace('_',' ').title()} sudah ada hari ini ({today})", Fore.GREEN))
    print(warna(f"Keluaran terakhir: {history[-1]['number']}", Fore.CYAN))
else:
    print(warna(f"\nMasukkan nomor keluaran terbaru untuk {pasaran.replace('_',' ').title()}:", Fore.LIGHTYELLOW_EX))
    while True:
        terbaru = input(warna("Nomor keluaran (angka): ", Fore.LIGHTYELLOW_EX))
        if terbaru.isdigit():
            break
        else:
            print(warna("Input harus angka!", Fore.LIGHTRED_EX))
    history.append({"date": today, "number": terbaru})
    if len(history) > 10:
        history.pop(0)
    with open(file_data, 'w') as f:
        json.dump(history, f)

print(warna(f"\nHistory terakhir:", Fore.CYAN))
for item in history:
    print(warna(f"{item['date']}: {item['number']}", Fore.CYAN))

# === ANIMASI LOADING ===
print(warna("\nMesin algoritma sedang menghitung kemungkinan terbaik...", Fore.MAGENTA))
for i in range(1, 11):
    percent = i * 10
    bar = ('█' * i) + ('-' * (10 - i))
    sys.stdout.write(f"\r{warna(f'[{bar}] {percent}%', Fore.GREEN)}")
    sys.stdout.flush()
    time.sleep(0.4)

# === MARKOV CHAIN PRESISI ===
transitions = {i: [] for i in range(10)}
transitions2 = {}

for item in history:
    num = item['number']
    for i in range(len(num) - 1):
        a, b = int(num[i]), int(num[i+1])
        transitions[a].append(b)
    for i in range(len(num) - 2):
        key = (int(num[i]), int(num[i+1]))
        transitions2.setdefault(key, []).append(int(num[i+2]))

freq = {}
for idx, item in enumerate(history):
    weight = idx + 1
    for d in item['number']:
        freq[int(d)] = freq.get(int(d), 0) + weight

most_common = sorted(freq, key=freq.get, reverse=True)[:3]

chain = []
current = random.choice(most_common)
chain.append(current)

while len(chain) < 6:
    if len(chain) >= 2:
        key = (chain[-2], chain[-1])
        next_digits = transitions2.get(key, [])
    else:
        next_digits = transitions.get(current, [])

    if next_digits:
        next_freq = {}
        for d in next_digits:
            next_freq[d] = next_freq.get(d, 0) + 1
        next_sorted = sorted(next_freq, key=next_freq.get, reverse=True)
        for d in next_sorted:
            if d not in chain:
                chain.append(d)
                current = d
                break
        else:
            current = random.randint(0, 9)
    else:
        current = random.randint(0, 9)

    if current not in chain:
        chain.append(current)

bbfs_kuat = sorted(list(set(chain))[:6])

# === RUMUS CADANGAN ===
last_number = history[-1]['number']
kebalikan = [10 - int(d) for d in last_number]
kebalikan = [5 if d == 0 else 0 if d == 5 else d for d in kebalikan]

hasil = []
n = len(kebalikan)
for i in range(n):
    for j in range(i+1, n):
        total = kebalikan[i] + kebalikan[j]
        if i == 0 and j == 1:
            hasil.extend([int(x) for x in str(total)])
        else:
            satuan = total % 10
            hasil.append(satuan)

hasil = [5 if d == 0 else 0 if d == 5 else d for d in hasil]

bbfs_cadangan = []
[bbfs_cadangan.append(x) for x in hasil if x not in bbfs_cadangan]
bbfs_cadangan = bbfs_cadangan[:7]

angka_kuat = ' '.join(map(str, bbfs_kuat))
angka_cadangan = ' '.join(map(str, bbfs_cadangan))

# === CETAK KOTAK DENGAN WARNA & TEBAL ===
kotak_kuat = f"""
{Fore.CYAN}╔══════════════════════════════╗
║ {Style.BRIGHT}ANGKA BBFS KUAT                {Fore.CYAN}║
╠══════════════════════════════╣
║   {Style.BRIGHT}{Fore.YELLOW}{angka_kuat.center(24)}   {Fore.CYAN}║
╚══════════════════════════════╝
"""

kotak_cadangan = f"""
{Fore.CYAN}╔══════════════════════════════╗
║ {Style.BRIGHT}ANGKA BBFS CADANGAN            {Fore.CYAN}║
╠══════════════════════════════╣
║   {Style.BRIGHT}{Fore.YELLOW}{angka_cadangan.center(24)}   {Fore.CYAN}║
╚══════════════════════════════╝
"""

# === BEEP ===
if is_windows:
    winsound.Beep(1000, 500)
    winsound.Beep(1200, 500)
else:
    print('\a')

print("\n\n" + warna("Ini dia angka yang dihasilkan berdasarkan rumus algoritma mesin pengeluaran togel:", Fore.CYAN))
print(kotak_kuat)
print(kotak_cadangan)

pesan = "\nSemoga JACKPOT ya! Kalau tembus, jangan lupa balik lagi ke MESIN BBFS TOGEL 😊🙏✨"
print(warna(pesan, Fore.LIGHTBLUE_EX))
