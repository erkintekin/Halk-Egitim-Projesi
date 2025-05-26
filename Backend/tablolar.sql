CREATE TABLE uzmanlik (
    uzmanlik_id SERIAL PRIMARY KEY,
    ad VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE egitimci (
    egitimci_id SERIAL PRIMARY KEY,
    tc_no VARCHAR(11) UNIQUE NOT NULL,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    dogum_tarihi DATE NOT NULL,
    telefon VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    uzmanlık_alani VARCHAR(100) NOT NULL,
    yonetici_id INTEGER,
    FOREIGN KEY (yonetici_id) REFERENCES egitimci(egitimci_id) ON DELETE SET NULL
);

CREATE TABLE kurs (
    kurs_id SERIAL PRIMARY KEY,
    kurs_adi VARCHAR(100) NOT NULL,
    aciklama TEXT,
    sure_saat INTEGER NOT NULL,
    baslangic_tarihi DATE NOT NULL,
    bitis_tarihi DATE NOT NULL,
    kontenjan INTEGER NOT NULL,
    egitimci_id INTEGER NOT NULL,
    FOREIGN KEY (egitimci_id) REFERENCES egitimci(egitimci_id) ON DELETE CASCADE
);

CREATE TABLE kursiyer (
    kursiyer_id SERIAL PRIMARY KEY,
    tc_no VARCHAR(11) UNIQUE NOT NULL,
    ad VARCHAR(50) NOT NULL,
    soyad VARCHAR(50) NOT NULL,
    dogum_tarihi DATE NOT NULL,
    telefon VARCHAR(15) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    adres VARCHAR(255) NOT NULL,
    kayit_tarihi DATE NOT NULL
);

CREATE TABLE katilim (
    kursiyer_id INTEGER NOT NULL,
    kurs_id INTEGER NOT NULL,
    kayit_tarihi DATE NOT NULL,
    not_ortalamasi DECIMAL(5,2),
    devam_durumu BOOLEAN DEFAULT TRUE,
	devam_orani DECIMAL(5,2),
	mevcut_kayit INTEGER DEFAULT 0,
    PRIMARY KEY (kursiyer_id, kurs_id),
    FOREIGN KEY (kursiyer_id) REFERENCES kursiyer(kursiyer_id) ON DELETE CASCADE,
    FOREIGN KEY (kurs_id) REFERENCES kurs(kurs_id) ON DELETE CASCADE
);

CREATE TABLE devamsizlik (
    devamsizlik_id SERIAL PRIMARY KEY,
    kursiyer_id INTEGER NOT NULL,
    kurs_id INTEGER NOT NULL,
    tarih DATE NOT NULL,
    durum BOOLEAN NOT NULL,
    aciklama TEXT,
    FOREIGN KEY (kursiyer_id, kurs_id) REFERENCES katilim(kursiyer_id, kurs_id) ON DELETE CASCADE
);