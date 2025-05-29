INSERT INTO uzmanlik (ad) VALUES
('Matematik'),
('Bilişim'),
('Dil Eğitimi'),
('Müzik'),
('El Sanatları');


INSERT INTO egitimci (tc_no, ad, soyad, dogum_tarihi, telefon, email, uzmanlik_alani, yonetici_id) VALUES
('11111111111', 'Ali', 'Yılmaz',   '1980-02-01', '05551110001', 'ali.yilmaz@example.com',    'Matematik',    NULL),
('22222222222', 'Ayşe', 'Demir',   '1985-05-15', '05551110002', 'ayse.demir@example.com',    'Bilişim',      1),
('33333333333', 'Mehmet', 'Kaya',  '1975-08-22', '05551110003', 'mehmet.kaya@example.com',   'Dil Eğitimi',  1),
('44444444444', 'Fatma', 'Aydın',  '1990-11-09', '05551110004', 'fatma.aydin@example.com',   'Müzik',        2),
('55555555555', 'Zeynep', 'Taş',   '1992-01-17', '05551110005', 'zeynep.tas@example.com',    'El Sanatları', 3);


INSERT INTO kurs (kurs_adi, aciklama, sure_saat, baslangic_tarihi, bitis_tarihi, kontenjan, egitimci_id) VALUES
('Matematik Temel Kursu', 'Lise seviyesi temel matematik eğitimi', 100, '2024-06-01', '2024-09-15', 30, 1),
('Python Programlama', 'Giriş seviyesi Python programlama kursu', 80, '2024-06-15', '2024-09-15', 25, 2),
('İngilizce Konuşma', 'Pratik konuşma ağırlıklı İngilizce', 120, '2024-07-01', '2024-10-01', 20, 3),
('Piyano Başlangıç', 'Piyano çalmaya giriş kursu', 60, '2024-07-10', '2024-09-10', 12, 4),
('Amigurumi Sanatı', 'El işi ile oyuncak yapımı kursu', 70, '2024-07-15', '2024-09-15', 16, 5);

INSERT INTO kursiyer (tc_no, ad, soyad, dogum_tarihi, telefon, email, adres, kayit_tarihi) VALUES
('11122233344', 'Burak', 'Çelik', '2000-03-10', '05553334444', 'burak.celik@example.com', 'Ankara', CURRENT_DATE),
('22233344455', 'Elif', 'Koç', '1998-09-23', '05554445555', 'elif.koc@example.com', 'İstanbul', CURRENT_DATE),
('33344455566', 'Onur', 'Bora', '1995-01-20', '05555556666', 'onur.bora@example.com', 'İzmir', CURRENT_DATE),
('44455566677', 'Derya', 'İnce', '2002-04-18', '05556667777', 'derya.ince@example.com', 'Antalya', CURRENT_DATE),
('55566677788', 'Serkan', 'Gül', '1997-12-12', '05557778888', 'serkan.gul@example.com', 'Eskişehir', CURRENT_DATE);

-- 5. Katılım (katilim)
INSERT INTO katilim (kursiyer_id, kurs_id, kayit_tarihi) VALUES
(1, 1, CURRENT_DATE),
(2, 2, CURRENT_DATE),
(3, 3, CURRENT_DATE),
(4, 4, CURRENT_DATE),
(5, 5, CURRENT_DATE),
(1, 2, CURRENT_DATE), 
(2, 3, CURRENT_DATE);

INSERT INTO devamsizlik (kursiyer_id, kurs_id, tarih, durum, aciklama) VALUES
(1, 1, '2024-06-05', TRUE,  'Geldi'),
(1, 1, '2024-06-06', FALSE, 'Gelmedi'),
(2, 2, '2024-06-16', TRUE,  'Geldi'),
(3, 3, '2024-07-02', FALSE, 'Sağlık sorunu nedeniyle gelmedi'),
(3, 3, '2024-07-03', TRUE,  'Geldi'),
(4, 4, '2024-07-11', TRUE,  'Geldi'),
(5, 5, '2024-07-16', FALSE, 'İzinli'),
(1, 2, '2024-06-17', TRUE,  'Geldi'),
(2, 3, '2024-07-04', TRUE,  'Geldi');


