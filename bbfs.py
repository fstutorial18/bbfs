import json
import os
import random
import time
import sys
from datetime import datetime

try:
    import winsound
    is_windows = True
except ImportError:
    is_windows = False

# Warna terminal
def warna(teks, kode):
    return f"\033[{kode}m{teks}\033[0m"

# Bersihkan layar
os.system('cls' if os.name == 'nt' else 'clear')

# Buat folder paito jika belum ada
if not os.path.exists("paito"):
    os.makedirs("paito")

# Judul
judul = "\n=============================\n   MESIN BBFS TOGEL\n=============================\n"
print(warna(judul, "91"))

# Daftar pasaran tanpa Macau All Time
pasaran_list = [
    "Hongkong Pool",
    "Hongkong Lotto",
    "Sydney Pool",
    "Sydney Lotto",
    "China",
    "Singapore",
    "Taiwan"
]

print(warna("Pilih Pasaran:", "93"))
for idx, p in enumerate(pasaran_list, 1):
    print(f"{idx}. {p}")

try:
    idx = int(input(warna("\nMasukkan nomor pasaran (1-7): ", "93"))) - 1
    pasaran = pasaran_list[idx].replace(" ", "_").lower()
except:
    print(warna("Pilihan tidak valid!", "91"))
    sys.exit()

file_data = f"paito/data_{pasaran}.json"

# Load atau buat data awal
if os.path.exists(file_data):
    with open(file_data) as f:
        history = json.load(f)
else:
    history = []

today = datetime.now().strftime("%Y-%m-%d")
if history and history[-1]['date'] == today:
    print(warna(f"\nData keluaran terbaru untuk {pasaran.replace('_',' ').title()} sudah ada hari ini ({today})", "92"))
    print(warna(f"Keluaran terakhir: {history[-1]['number']}", "96"))
else:
    print(warna(f"\nMasukkan nomor keluaran terbaru untuk {pasaran.replace('_',' ').title()}:", "93"))
    while True:
        terbaru = input(warna("Nomor keluaran (angka): ", "93"))
        if terbaru.isdigit():
            break
        else:
            print(warna("Input harus angka!", "91"))

    history.append({"date": today, "number": terbaru})
    if len(history) > 10:
        history.pop(0)
    with open(file_data, 'w') as f:
        json.dump(history, f)

print(warna(f"\nHistory terakhir:", "96"))
for item in history:
    print(warna(f"{item['date']}: {item['number']}", "96"))

# Animasi loading 1–100%
print(warna("\nMesin algoritma sedang menghitung kemungkinan terbaik...", "95"))
for i in range(1, 11):
    percent = i * 10
    bar = ('█' * i) + ('-' * (10 - i))
    sys.stdout.write(f"\r{warna(f'[{bar}] {percent}%', '92')}")
    sys.stdout.flush()
    time.sleep(1)

# -----------------------------
# === Markov Chain Pattern ====
# -----------------------------

# 1. Hitung frekuensi transisi antar digit
transitions = {i: [] for i in range(10)}
for item in history:
    num = item['number']
    for i in range(len(num) - 1):
        a, b = int(num[i]), int(num[i+1])
        transitions[a].append(b)

# 2. Mulai dari digit populer, telusuri next digit populer
freq = {}
for item in history:
    for d in item['number']:
        freq[int(d)] = freq.get(int(d), 0) + 1

most_common = sorted(freq, key=freq.get, reverse=True)[:3]

chain = []
current = random.choice(most_common)
chain.append(current)

while len(chain) < 6:
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

# Buat BBFS cadangan dari digit jarang
rare = [d for d in range(10) if d not in bbfs_kuat]
random.shuffle(rare)
bbfs_cadangan = sorted(rare[:6])

angka_kuat = ' '.join(map(str, bbfs_kuat))
angka_cadangan = ' '.join(map(str, bbfs_cadangan))

kotak_kuat = f"""
+-----------------------+
|  ANGKA BBFS KUAT      |
+-----------------------+
|   {angka_kuat}   |
+-----------------------+
"""

kotak_cadangan = f"""
+-----------------------+
|  ANGKA BBFS CADANGAN  |
+-----------------------+
|   {angka_cadangan}   |
+-----------------------+
"""

# Beep
if is_windows:
    winsound.Beep(1000, 500)
    winsound.Beep(1200, 500)
else:
    print('\a')

print("\n\n" + warna("Ini dia angka yang dihasilkan berdasarkan rumus algoritma mesin pengeluaran togel", "96"))
print(warna(kotak_kuat, "92"))
print(warna(kotak_cadangan, "92"))

pesan = "\nSemoga JACKPOT ya! Kalau tembus, jangan lupa balik lagi ke MESIN BBFS TOGEL 😊🙏✨"
print(warna(pesan, "94"))
