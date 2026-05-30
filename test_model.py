import joblib

# 1. Eğittiğimiz beyni (modeli) yüklüyoruz
model = joblib.load("anomaly_model.pkl")

# 2. Sanal bir saldırı senaryosu oluşturuyoruz:
# Diyelim ki ağımıza sızmaya çalışan biri 50 milisaniyede bir istek atıyor 
# ve toplamda 120 kez şifre denemesi yaptı.
request_interval = 50
request_count = 120

# 3. Yapay zekaya soruyoruz: Sence bu bir bot mu?
prediction = model.predict([[request_interval, request_count]])

# 4. Sonucu ekrana yazdırıyoruz
if prediction[0] == 1:
    print("🚨 ALARM: KABA KUVVET (BRUTE-FORCE) BOTU TESPİT EDİLDİ! 🚨")
else:
    print("✅ NORMAL KULLANICI TRAFİĞİ.")