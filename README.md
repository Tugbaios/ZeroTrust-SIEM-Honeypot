
# 🛡️ Zero Trust SIEM & Honeypot Panel

Bu proje, ağa sızmaya çalışan veya keşif yapan kötü niyetli yazılımları makine öğrenmesi algoritmaları kullanarak tespit eden gerçek zamanlı bir Siber Güvenlik İzleme (SIEM) panelidir. 



## 📂 Proje Dosyaları
* **`traffic_data.csv`**: Sistemimizin eğitim için kullandığı veri seti.
* **`train_model.py`**: Veri setini işleyip "yapay zeka beynini" (`anomaly_model.pkl`) eğiten kod.
* **`test_model.py`**: Modelin başarısını hızlıca test eden yardımcı script.
* **`siem_panel.py`**: Canlı verileri izleyen, saldırı anında alarm veren ve Sıfır Güven (Zero Trust) protokollerini yöneten ana arayüz.

## 🚀 Kurulum (Adım Adım)

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. **Terminali Açın:** Proje klasörüne sağ tıklayıp terminali (CMD/PowerShell) açın.
2. **Gerekli Kütüphaneleri Yükleyin:**
   ```bash
   pip install pandas scikit-learn joblib customtkinter pyserial

   Modeli Eğitin: (Beyni oluşturmak için)
   python train_model.py

   Paneli Başlatın: (Sistemi izlemeye başlamak için)
   python siem_panel.py

   Not: Gerçek bir cihaz bağlı değilse, sistem otomatik olarak "Simülasyon Modu"na geçer. Paneldeki butonlarla saldırı testleri yapabilirsiniz.
