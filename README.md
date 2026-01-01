# CPU_scheduling_simulator

**Gerçek sistem süreçleriyle CPU çizelgeleme algoritmalarını görselleştiren interaktif masaüstü uygulaması.**

İşletim sistemleri derslerinde öğrenilen CPU scheduling algoritmalarını, bilgisayarınızda çalışan gerçek süreçler üzerinde test edebilir, görselleştirebilir ve karşılaştırabilirsiniz.

---

## 🎯 Ne Yapar?

Bu uygulama, bilgisayarınızda çalışan gerçek süreçleri (Chrome, Discord, VS Code vb.) alır ve seçtiğiniz CPU çizelgeleme algoritmasıyla nasıl yönetileceklerini simüle eder. 

**Ana İşlevler:**
- Sisteminizdeki aktif süreçleri otomatik olarak getirir
- Her süreç için burst time (CPU kullanım süresi) hesaplar veya siz düzenlersiniz
- 4 farklı algoritmayla simülasyon çalıştırır
- Gantt Chart ile zaman çizelgesini görselleştirir
- Performans metriklerini hesaplar ve karşılaştırır

---

## 📊 Desteklenen Algoritmalar

### 1. **FCFS (First Come First Serve)**
- En basit algoritma
- Geliş sırasına göre işlem yapar
- Adil ama bazen verimsiz (convoy effect)
- **Ne zaman kullanılır:** Basit batch işlemler

### 2. **SJF (Shortest Job First - Preemptive)**
- En kısa işi önce yapar
- Optimal ortalama bekleme süresi sağlar
- Uzun süreçler açlık çekebilir (starvation)
- **Ne zaman kullanılır:** Minimum bekleme süresi hedeflendiğinde

### 3. **Priority Scheduling (Preemptive)**
- Önceliğe göre işlem yapar (sistemden alınan priority değerleri)
- Yüksek öncelikli işler öne geçer
- Priority inversion riski var
- **Ne zaman kullanılır:** Gerçek zamanlı sistemler, kritik işler

### 4. **Round Robin**
- Her süreç belirli zaman dilimi (quantum) alır
- Adil dağılım sağlar
- Time quantum seçimi kritik
- **Ne zaman kullanılır:** Time-sharing sistemler, interaktif uygulamalar

---

## 🚀 Kurulum ve Çalıştırma

### Windows Kullanıcıları (.exe)
1. **İndirin:** `CPUSchedulingSimulator.exe` dosyasını indirin
2. **Çalıştırın:** Dosyaya çift tıklayın
3. **Uyarı çıkarsa:** "More info" → "Run anyway" seçin
4. **Hepsi bu kadar!** Python kurulumu gerekmez

### Linux/macOS veya Kaynak Koddan Çalıştırma

**Adım 1: Python Kontrol**
```bash
python --version  # 3.8 veya üzeri olmalı
```

**Adım 2: Bağımlılıkları Yükle**
```bash
pip install customtkinter psutil
```

**Adım 3: Uygulamayı Çalıştır**
```bash
python CPUSchedulingSimulator.py
```

**Linux'ta izin hatası alırsanız:**
```bash
sudo python CPUSchedulingSimulator.py
```

---

## 💻 Nasıl Kullanılır?

### Adım 1: Süreçleri Getir
1. Sol panelde **"🔄 Fetch PC Processes"** butonuna tıklayın
2. Kısa bir loading animasyonu görünür
3. Sağ tarafta 30 süreç listesi belirir
4. Her süreç için otomatik burst time hesaplanır (0-100 arası)

**Burst Time Nasıl Hesaplanır?**
- Gerçek CPU kullanımı + Random faktör
- Yoğun süreçler (Chrome) daha yüksek değer alır
- Hafif süreçler (system services) düşük değer alır

### Adım 2: Burst Time Düzenle (Opsiyonel)
- Tabloda **"Burst Time"** sütunundaki herhangi bir değere tıklayın
- Yeni değer yazın (0-100 arası)
- Enter'a basın
- Eğitim senaryoları oluşturmak için kullanışlı

### Adım 3: Algoritma Seç
- Dropdown menüden algoritma seçin:
  - FCFS (basit)
  - SJF (optimal)
  - Priority (gerçek zamanlı)
  - Round Robin (adil)
- Round Robin seçtiyseniz **Time Quantum** girin (varsayılan: 2)

### Adım 4: Simülasyonu Çalıştır
- **"▶ Run Simulation"** butonuna tıklayın
- Sonuçlar anında görünür

### Adım 5: Sonuçları Analiz Et

**İnteraktif Gantt Chart:**
- Her süreç farklı renkle gösterilir
- Zaman çizelgesini görselleştirir
- **Zoom In/Out:** Detay görmek için büyüt/küçült
- **Pan:** Mouse ile sürükle
- **Scroll:** Yatay kaydırma

**KPI Metrikleri (4 Kart):**
1. **CPU Utilization** - CPU'nun ne kadar meşgul olduğu (%)
2. **Throughput** - Birim zamanda tamamlanan süreç sayısı
3. **Avg Turnaround Time** - Ortalama tamamlanma süresi
4. **Avg Waiting Time** - Ortalama bekleme süresi

**Detaylı Sonuç Tablosu:**
- Her süreç için completion, turnaround, waiting time
- Sütun başlıklarına tıklayarak sıralama yapabilirsiniz

### Adım 6: Karşılaştır (Manuel)
1. Sonuçları not alın
2. **"🔄 Reset Data"** butonuna tıklayın
3. Başka bir algoritma seçin
4. Aynı süreçlerle tekrar simüle edin
5. KPI metriklerini karşılaştırın

---
---

**⭐ Eğitim amaçlı kullanım için geliştirilmiştir. Projeyi beğendiyseniz yıldız vermeyi unutmayın!**
