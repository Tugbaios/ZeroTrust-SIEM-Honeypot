import customtkinter as ctk
import tkinter as tk
import threading
import time
import random
import joblib
import warnings
import json
import serial # YENİ: Gerçek donanım verisi için

warnings.filterwarnings("ignore", category=UserWarning)

# --- MODERN ARAYÜZ TEMASI ---
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

# 1. YAPAY ZEKA YÜKLEME
try:
    model = joblib.load("anomaly_model.pkl")
    model_hazir = True
except:
    model_hazir = False

simulasyon_aktif = False 
GERCEK_DONANIM_BAGLI = False

# --- 2. GERÇEK VERİ FİLTRELEME (PARSING) MERKEZİ ---
def mesaj_isle(gelen_mesaj):
    # 1. JSON Formatlı Alarmlar (ESP'den gelen sendAlarm)
    if gelen_mesaj.startswith("{"):
        try:
            veri = json.loads(gelen_mesaj)
            sebep = veri.get("reason", "Bilinmeyen Neden")
            mac = veri.get("mac", "Bilinmiyor")
            
            if "Port_Scan" in sebep:
                log_yaz(f"🚨 Port Taraması Tespit Edildi! ({sebep}) | MAC: {mac}\n", "uyari")
            elif "NMAP" in sebep:
                log_yaz(f"🟡 Otomatik Keşif (Nmap) Engellendi! | MAC: {mac}\n", "uyari")
            elif "Unauthorized" in sebep:
                log_yaz(f"🛡️ İzinsiz Giriş Engellendi (Beyaz Liste Dışı) | MAC: {mac}\n", "uyari")
            else:
                log_yaz(f"⚠️ Alarm: {sebep} | MAC: {mac}\n", "alarm")
        except:
            pass

    # 2. Yapay Zekayı Tetikleyen Veriler [ML_DATA]
    elif "[ML_DATA]" in gelen_mesaj:
        try:
            parcalar = gelen_mesaj.split(" ")
            interval = int(parcalar[1].split(":")[1]) 
            count = int(parcalar[2].split(":")[1])    
            
            log_yaz(f"[ŞÜPHELİ TRAFİK] Şifre Deneniyor! Hız: {interval}ms, İstek Sayısı: {count}\n", "uyari")
            
            if model_hazir:
                tahmin = model.predict([[interval, count]])
                if tahmin[0] == 1:
                    log_yaz("🚨 [YAPAY ZEKA ALARMI] KABA KUVVET BOTU TESPİT EDİLDİ! ERİŞİM KESİLDİ. 🚨\n\n", "alarm")
                else:
                    log_yaz("✅ [YAPAY ZEKA] Trafik insan hızında, anomali yok.\n\n", "normal")
        except:
            pass

    # 3. Normal Metin Logları
    elif "[BAŞARILI]" in gelen_mesaj:
        log_yaz(gelen_mesaj + "\n", "normal")
    elif "[TEHDİT]" in gelen_mesaj:
        log_yaz(gelen_mesaj + "\n", "uyari")
    else:
        # Geri kalan standart ESP loglarını mavi/bilgi olarak bas
        log_yaz(gelen_mesaj + "\n", "bilgi")

# --- 3. BAĞLANTI YÖNETİCİSİ (AKILLI GEÇİŞ) ---
def veri_dinleyici():
    global GERCEK_DONANIM_BAGLI
    com_port = "COM3" # Eren cihazı bağladığında burayı cihazın portuna göre değiştirebilirsiniz
    baud_rate = 115200

    try:
        # Cihaz bağlı mı diye USB'yi kontrol et
        ser = serial.Serial(com_port, baud_rate, timeout=1)
        GERCEK_DONANIM_BAGLI = True
        log_yaz(f"[SİSTEM] {com_port} portundan ESP32 Ağına Bağlanıldı. Gerçek veriler dinleniyor...\n\n", "normal")
        
        # Gerçek verileri okuma döngüsü
        while True:
            if ser.in_waiting > 0:
                satir = ser.readline().decode('utf-8').strip()
                mesaj_isle(satir)
                
    except Exception as e:
        # Cihaz yoksa doğrudan simülasyona geç!
        GERCEK_DONANIM_BAGLI = False
        log_yaz(f"[SİSTEM] {com_port} portunda cihaz bulunamadı.\n", "uyari")
        log_yaz("[SİSTEM] Sunum / Simülasyon moduna geçiliyor...\n\n", "bilgi")
        simule_et()

# --- 4. SİMÜLASYON MOTORU (CİHAZ YOKKEN ÇALIŞIR) ---
def simule_et():
    global simulasyon_aktif
    while not GERCEK_DONANIM_BAGLI: # Sadece gerçek cihaz yoksa çalışır
        if simulasyon_aktif:
            time.sleep(random.uniform(2.0, 5.0)) 
            senaryo = random.choice(["normal", "tarama", "bruteforce"])
            if senaryo == "normal": tetikle_normal()
            elif senaryo == "tarama": tetikle_nmap()
            elif senaryo == "bruteforce": tetikle_bruteforce()
        else:
            time.sleep(1)

# --- 5. MANUEL SALDIRI TETİKLEYİCİLERİ ---
def tetikle_normal():
    mesaj_isle("[BAŞARILI] >>> BİR CİHAZ AĞA BAĞLANDI! MAC: 3A:1B:4C:5D:6E:7F")

def tetikle_nmap():
    log_yaz("\n[SİSTEM] Manuel Nmap Tarama Testi Başlatıldı...\n", "bilgi")
    pencere.update()
    time.sleep(0.5)
    mesaj_isle('{"type": "ALARM", "node_id": "9999", "alert": "CRITICAL", "reason": "NMAP_Reconnaissance_Detected", "mac": "FF:EE:DD:CC:BB:AA"}')

def tetikle_bruteforce():
    log_yaz("\n[SİSTEM] Yapay Zeka Brute-Force Testi Başlatıldı...\n", "bilgi")
    pencere.update()
    time.sleep(0.5)
    interval = random.randint(10, 80) 
    count = random.randint(100, 250)
    mesaj_isle(f"[ML_DATA] INTERVAL:{interval} COUNT:{count}")

# 6. YAZI YAZDIRMA FONKSİYONU
def log_yaz(mesaj, tur):
    ekran.config(state=tk.NORMAL)
    ekran.insert(tk.END, mesaj, tur)
    ekran.see(tk.END) 
    ekran.config(state=tk.DISABLED)

# --- 7. BUTON GÖREVLERİ ---
def baslat_durdur():
    global simulasyon_aktif
    if GERCEK_DONANIM_BAGLI:
        log_yaz("\n[HATA] Gerçek cihaz bağlıyken simülasyon başlatılamaz!\n", "uyari")
        return
        
    if simulasyon_aktif:
        simulasyon_aktif = False
        btn_baslat.configure(text="▶ Oto-Simülasyonu Aç", fg_color="#2e7d32", hover_color="#1b5e20")
        log_yaz("\n[SİSTEM] Otomatik trafik akışı DURDURULDU. Manuel test moduna geçildi.\n", "uyari")
    else:
        simulasyon_aktif = True
        btn_baslat.configure(text="⏸ Oto-Simülasyonu Kapat", fg_color="#e65100", hover_color="#e65100")
        log_yaz("\n[SİSTEM] Otomatik trafik akışı BAŞLATILDI...\n", "bilgi")

def temizle():
    ekran.config(state=tk.NORMAL)
    ekran.delete('1.0', tk.END)
    ekran.config(state=tk.DISABLED)

def acil_kilit():
    log_yaz("\n🛡️ [SIFIR GÜVEN PROTOKOLÜ] ACİL DURUM KİLİDİ AKTİF! TÜM AĞ TRAFİĞİ REDDEDİLİYOR! 🛡️\n\n", "alarm")
    global simulasyon_aktif
    if simulasyon_aktif: baslat_durdur()

# --- 8. GÖRSEL ARAYÜZ (GUI) İNŞASI ---
pencere = ctk.CTk()
pencere.title("Siber Tuzak (Honeypot) - Gelişmiş Komuta Merkezi")
pencere.geometry("1000x750")

baslik = ctk.CTkLabel(pencere, text="🛡️ SIFIRDAN GÜVEN (ZERO TRUST) AĞ İZLEME PANELİ", font=("Roboto", 22, "bold"), text_color="#00E676")
baslik.pack(pady=(20, 10))

log_frame = ctk.CTkFrame(pencere, corner_radius=15, fg_color="#1e1e1e")
log_frame.pack(padx=20, pady=10, fill="both", expand=True)

ekran = tk.Text(log_frame, bg="#1a1a1a", fg="#ffffff", font=("Consolas", 11), relief="flat", padx=15, pady=15)
ekran.pack(fill="both", expand=True, padx=5, pady=5)

ekran.tag_config("bilgi", foreground="#00e5ff")
ekran.tag_config("normal", foreground="#00e676")
ekran.tag_config("uyari", foreground="#ffea00")
ekran.tag_config("alarm", foreground="#ff1744", background="#4a0000")

# --- ÜST BUTONLAR ---
buton_frame_ust = ctk.CTkFrame(pencere, fg_color="transparent")
buton_frame_ust.pack(pady=10)

btn_baslat = ctk.CTkButton(buton_frame_ust, text="▶ Oto-Simülasyonu Aç", fg_color="#2e7d32", hover_color="#1b5e20", font=("Roboto", 13, "bold"), width=180, height=40, command=baslat_durdur)
btn_baslat.grid(row=0, column=0, padx=10)

btn_temizle = ctk.CTkButton(buton_frame_ust, text="🗑️ Ekranı Temizle", fg_color="#546e7a", hover_color="#37474f", font=("Roboto", 13, "bold"), width=180, height=40, command=temizle)
btn_temizle.grid(row=0, column=1, padx=10)

btn_kilitle = ctk.CTkButton(buton_frame_ust, text="🛑 Acil Durum Kilidi", fg_color="#d50000", hover_color="#b71c1c", font=("Roboto", 13, "bold"), width=180, height=40, command=acil_kilit)
btn_kilitle.grid(row=0, column=2, padx=10)

# --- ALT BUTONLAR (SUNUM MODU) ---
sunum_baslik = ctk.CTkLabel(pencere, text="--- MANUEL SALDIRI TESTLERİ (SUNUM MODU) ---", font=("Roboto", 12), text_color="#78909c")
sunum_baslik.pack(pady=(10, 0))

buton_frame_alt = ctk.CTkFrame(pencere, fg_color="transparent")
buton_frame_alt.pack(pady=10)

btn_test_normal = ctk.CTkButton(buton_frame_alt, text="🟢 Normal Giriş Testi", fg_color="#004d40", hover_color="#00251a", font=("Roboto", 13, "bold"), width=180, height=40, command=tetikle_normal)
btn_test_normal.grid(row=0, column=0, padx=10)

btn_test_nmap = ctk.CTkButton(buton_frame_alt, text="🟡 Nmap Taraması Yap", fg_color="#f57f17", hover_color="#bc5100", font=("Roboto", 13, "bold"), text_color="black", width=180, height=40, command=tetikle_nmap)
btn_test_nmap.grid(row=0, column=1, padx=10)

btn_test_brute = ctk.CTkButton(buton_frame_alt, text="🔴 Brute-Force Testi", fg_color="#b71c1c", hover_color="#7f0000", font=("Roboto", 13, "bold"), width=180, height=40, command=tetikle_bruteforce)
btn_test_brute.grid(row=0, column=2, padx=10)

# Dinleyiciyi arka planda başlat
thread = threading.Thread(target=veri_dinleyici, daemon=True)
thread.start()

pencere.mainloop()