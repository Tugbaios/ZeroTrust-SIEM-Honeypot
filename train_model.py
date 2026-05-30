import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Veri setini bilgisayardan okuyoruz
data = pd.read_csv("traffic_data.csv")

# 2. Girdileri (Süre ve İstek Sayısı) ve Çıktıyı (Bot mu/Değil mi) ayırıyoruz
X = data[["request_interval_ms", "request_count"]]
y = data["label"]

# 3. Verinin %80'ini eğitim, %20'sini test için ayırıyoruz
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 4. Karar Ağacı (Decision Tree) modelimizi oluşturuyoruz
model = DecisionTreeClassifier()

# 5. Yapay zekayı verilerle eğitiyoruz
model.fit(X_train, y_train)

# 6. Modelin başarısını test ediyoruz
predictions = model.predict(X_test)
print("Model Başarı Doğruluğu (Accuracy):", accuracy_score(y_test, predictions))

# 7. Eğitilen bu yapay zeka beynini daha sonra kullanmak üzere kaydediyoruz
joblib.dump(model, "anomaly_model.pkl")
print("Yapay zeka modeli 'anomaly_model.pkl' adıyla başarıyla kaydedildi!")