
# 🛡️ Zero Trust SIEM & Honeypot Panel

Bu proje, ağa sızmaya çalışan veya keşif yapan kötü niyetli yazılımları makine öğrenmesi algoritmaları kullanarak tespit eden gerçek zamanlı bir Siber Güvenlik İzleme (SIEM) panelidir. 

## 🚀 Özellikler
* **Makine Öğrenmesi ile Anomali Tespiti:** Kaba kuvvet (brute-force) saldırılarını Karar Ağacı algoritması ile tespit eder.
* **Zero Trust (Sıfır Güven) Mimarisi:** Acil durumlarda tüm ağ trafiğini reddeden güvenlik kilidi.
* **Oto-Simülasyon Modu:** Donanım bağlı olmadığında Nmap ve Brute-Force saldırılarını otomatik simüle eder.

## 🛠️ Kurulum ve Gereksinimler

Terminali proje klasörünüzde açın ve şu kütüphaneleri yükleyin:

```bash
pip install pandas scikit-learn joblib customtkinter pyserial

⚙️ Çalıştırma Talimatı
Modeli Eğitme: python train_model.py (Bu işlem modeli eğitip kaydeder).

Paneli Başlatma: python siem_panel.py (Arayüzü başlatır).

Not: Gerçek ESP32 cihazı bağlı değilse sistem otomatik olarak simülasyon moduna geçecektir.

### 3. Adım: Kaydetme (Commit)
1. Metni yapıştırdıktan sonra sayfanın en altına in.
2. **"Commit changes..."** yazan yeşil butona tıkla.
3. Açılan küçük pencerede "Add README" gibi bir açıklama yazılıdır, doğrudan **"Commit changes"** butonuna tekrar basarak işlemi bitir.

İşte bu kadar! Artık deponun ana sayfasına döndüğünde, hazırladığın bu şık rehber herkesin görebileceği şekilde orada duracak. Arkadaşlarına bu linki gönderdiğinde, "README dosyasını okuyup kurulumu yapın" demen yeterli.
