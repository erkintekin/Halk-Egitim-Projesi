# 📚 Halk Eğitim Kursiyer ve Eğitimci Takip Sistemi

Bu proje, PyQt5 ile geliştirilmiş kullanıcı dostu bir arayüz üzerinden PostgreSQL veritabanına bağlanarak halk eğitim merkezlerinde kursiyer, kurs ve eğitimci takibini yapmayı amaçlayan bir masaüstü uygulamasıdır.

---

## 🎯 Proje Amacı

- Kursiyer ve eğitimcilerin kayıtlarının tutulması  
- Kursların açılması, eğitmenlerin atanması  
- Kursiyerlerin kurslara kaydedilmesi  
- Devamsızlık takibi ve devam oranlarının hesaplanması  
- Görsel, sade ve kullanıcı dostu bir arayüz üzerinden tüm işlemlerin yapılabilmesi

---

## 🧰 Kullanılan Teknolojiler

| Teknoloji      | Açıklama                            |
|----------------|-------------------------------------|
| Python         | Uygulama geliştirici dil            |
| PyQt5          | Masaüstü GUI framework              |
| PostgreSQL     | Veritabanı yönetim sistemi          |
| SQL (PL/pgSQL) | Trigger, fonksiyon, constraint yazımı |

---

## 🏗️ Veritabanı Yapısı

Veritabanı aşağıdaki temel tabloları içerir:

- `kursiyer`  
- `egitimci`  
- `kurs`  
- `katilim`  
- `devamsizlik`  
- `uzmanlik_alani`  

Trigger ve fonksiyonlarla:
- Devamsızlık oranı hesaplanır  
- Devam durumu (`✔️ / ❌`) kontrol edilir  
- Maksimum kontenjan, kayıt tekrarları engellenir  

---

## 📷 Arayüz Özellikleri

- **Kursiyer sekmesi**: Kursiyer ekleme, listeleme, silme  
- **Eğitimci sekmesi**: Eğitimci ekleme, listeleme, uzmanlık seçimi  
- **Kurs sekmesi**: Yeni kurs oluşturma, kontenjan ve tarih doğrulama  
- **Devamsızlık sekmesi**: Öğrencinin devam durumunu gösteren gelişmiş tablo  
- **Kayıt & Güncelleme sekmesi**:  
  - Kursiyeri kursa kaydet  
  - Eğitmeni güncelle (dropdown seçimli)

---

## 🚀 Başlatmak için

1. PostgreSQL’de `halk_egitim` adında bir veritabanı oluştur  
2. `tablolar.sql`, `fonksiyonlar.sql`, `triggerlar.sql` dosyalarını sırasıyla çalıştır  
3. `main.py` dosyasını çalıştır

```bash
python main.py
