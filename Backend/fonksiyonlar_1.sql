CREATE OR REPLACE FUNCTION kursiyer_kaydet(
    p_tc_no VARCHAR,
    p_ad VARCHAR,
    p_soyad VARCHAR,
    p_dogum_tarihi DATE,
    p_telefon VARCHAR,
    p_email VARCHAR,
    p_adres VARCHAR
)
RETURNS VOID AS $$
DECLARE
    var_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO var_count FROM kursiyer WHERE tc_no = p_tc_no;
    IF var_count > 0 THEN
        RAISE EXCEPTION 'Bu TC kimlik numarası zaten kayıtlı: %', p_tc_no;
    END IF;
	
    SELECT COUNT(*) INTO var_count FROM kursiyer WHERE email = p_email;
    IF var_count > 0 THEN
        RAISE EXCEPTION 'Bu e-posta adresi zaten kayıtlı: %', p_email;
    END IF;

    INSERT INTO kursiyer (tc_no, ad, soyad, dogum_tarihi, telefon, email, adres, kayit_tarihi)
    VALUES (p_tc_no, p_ad, p_soyad, p_dogum_tarihi, p_telefon, p_email, p_adres, CURRENT_DATE);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sil_kurs(p_kurs_id INTEGER)
RETURNS TEXT AS $$
DECLARE
BEGIN
    DELETE FROM katilim WHERE kurs_id = p_kurs_id;

    DELETE FROM devamsizlik WHERE kurs_id = p_kurs_id;

    DELETE FROM kurs WHERE kurs_id = p_kurs_id;

    RETURN 'Kurs başarıyla silindi.';
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'Kurs silinemedi: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION egitimci_kaydet(
    p_tc_no VARCHAR,
    p_ad VARCHAR,
    p_soyad VARCHAR,
    p_dogum_tarihi DATE,
    p_telefon VARCHAR,
    p_email VARCHAR,
    p_uzmanlik VARCHAR,
    p_yonetici_id INTEGER DEFAULT NULL
)
RETURNS VOID AS $$
DECLARE
    var_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO var_count FROM egitimci WHERE tc_no = p_tc_no;
    IF var_count > 0 THEN
        RAISE EXCEPTION 'Bu TC kimlik numarası zaten kayıtlı: %', p_tc_no;
    END IF;
	
    SELECT COUNT(*) INTO var_count FROM egitimci WHERE email = p_email;
    IF var_count > 0 THEN
        RAISE EXCEPTION 'Bu e-posta adresi zaten kayıtlı: %', p_email;
    END IF;

    INSERT INTO egitimci (tc_no, ad, soyad, dogum_tarihi, telefon, email, uzmanlik_alani, yonetici_id)
    VALUES (p_tc_no, p_ad, p_soyad, p_dogum_tarihi, p_telefon, p_email, p_uzmanlik, p_yonetici_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION kurs_olustur(
    p_kurs_adi VARCHAR,
    p_aciklama TEXT,
    p_sure_saat INTEGER,
    p_baslangic DATE,
    p_bitis DATE,
    p_kontenjan INTEGER,
    p_egitimci_id INTEGER
)
RETURNS VOID AS $$
DECLARE
    egitimci_sayisi INTEGER;
    kurs_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO kurs_count FROM kurs WHERE LOWER(p_kurs_adi) = LOWER(kurs_adi);
    IF kurs_count > 0 THEN
        RAISE EXCEPTION 'HATA: % isimli kurs zaten açılmıştır.', p_kurs_adi;
    END IF;

    IF p_sure_saat > 600 THEN
        RAISE EXCEPTION 'Kurs saati 600''den fazla olamaz!';
    END IF;

    SELECT COUNT(*) INTO egitimci_sayisi
    FROM egitimci
    WHERE egitimci_id = p_egitimci_id;
    IF egitimci_sayisi = 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li eğitimci bulunamadı.', p_egitimci_id;
    END IF;

    IF p_baslangic < CURRENT_DATE THEN
        RAISE EXCEPTION 'Geçmiş tarihe (%) ait kurs açılamaz!', p_baslangic;
    END IF;

    IF p_bitis < p_baslangic THEN
        RAISE EXCEPTION 'Bitiş tarihi başlangıçtan önce olamaz!';
    END IF;

    IF p_kontenjan > 100 THEN
        RAISE EXCEPTION 'Kurs kontenjanı 100''den fazla olamaz!';
    END IF;

    INSERT INTO kurs (kurs_adi, aciklama, sure_saat, baslangic_tarihi, bitis_tarihi, kontenjan, egitimci_id)
    VALUES (p_kurs_adi, p_aciklama, p_sure_saat, p_baslangic, p_bitis, p_kontenjan, p_egitimci_id);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION kursiyeri_kursa_kaydet(
    p_kursiyer_id INTEGER,
    p_kurs_id INTEGER
)
RETURNS VOID AS $$
DECLARE
kurs_count INTEGER;
kursiyer_count INTEGER;
kurs_kursiyer_count INTEGER;
mevcut_kayit INTEGER;
max_kontenjan INTEGER;
BEGIN
	SELECT COUNT(*) INTO kurs_count FROM kurs WHERE kurs_id = p_kurs_id;
    IF kurs_count = 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li kurs bulunamadı.', p_kurs_id;
    END IF;

	SELECT COUNT(*) INTO kursiyer_count FROM kursiyer WHERE kursiyer_id = p_kursiyer_id;
	IF kursiyer_count = 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li kursiyer bulunamadı.', p_kursiyer_id;
    END IF;

	SELECT COUNT(*) INTO kurs_kursiyer_count FROM katilim WHERE kurs_id = p_kurs_id AND kursiyer_id = p_kursiyer_id;
	IF kurs_kursiyer_count > 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li kursiyer zaten % ID''li kursa kayıtlı!', p_kursiyer_id, p_kurs_id;
    END IF;
	
	SELECT kontenjan INTO max_kontenjan FROM kurs WHERE kurs_id = p_kurs_id;
    SELECT COUNT(*) INTO mevcut_kayit FROM katilim WHERE kurs_id = p_kurs_id;

    IF mevcut_kayit >= max_kontenjan THEN
        RAISE EXCEPTION 'Kontenjan dolu! En fazla % kişi kayıt olabilir.', max_kontenjan;
    END IF;
		
    INSERT INTO katilim (kursiyer_id, kurs_id, kayit_tarihi)
    VALUES (p_kursiyer_id, p_kurs_id, CURRENT_DATE);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION kurs_egitimci_guncelle(
    p_kurs_id INTEGER,
    p_yeni_egitimci_id INTEGER
)
RETURNS VOID AS $$
DECLARE
    egitimci_count INTEGER;
    kurs_count INTEGER;
    mevcut_egitimci_id INTEGER;
BEGIN
    SELECT COUNT(*) INTO egitimci_count
    FROM egitimci
    WHERE egitimci_id = p_yeni_egitimci_id;

    IF egitimci_count = 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li eğitimci bulunamadı.', p_yeni_egitimci_id;
    END IF;

    SELECT COUNT(*) INTO kurs_count
    FROM kurs
    WHERE kurs_id = p_kurs_id;

    IF kurs_count = 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li kurs bulunamadı.', p_kurs_id;
    END IF;

    SELECT egitimci_id INTO mevcut_egitimci_id
    FROM kurs
    WHERE kurs_id = p_kurs_id;

    IF mevcut_egitimci_id = p_yeni_egitimci_id THEN
        RAISE NOTICE 'Bu eğitimci zaten bu kursa atanmış.';
        RETURN;
    END IF;

    UPDATE kurs
    SET egitimci_id = p_yeni_egitimci_id
    WHERE kurs_id = p_kurs_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION kursiyer_sil(p_kursiyer_id INTEGER)
RETURNS VOID AS $$
DECLARE
    kursiyer_count INTEGER;
BEGIN
	SELECT COUNT(*) INTO kursiyer_count FROM kursiyer WHERE kursiyer_id = p_kursiyer_id;
	IF kursiyer_count = 0 THEN
        RAISE EXCEPTION 'HATA: % ID''li kursiyer bulunamadı.', p_kursiyer_id;
    END IF;
    DELETE FROM kursiyer WHERE kursiyer_id = p_kursiyer_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION devamsizlik_ekle(
    p_kursiyer_id INTEGER,
    p_kurs_id INTEGER,
    p_tarih DATE,
    p_durum BOOLEAN,
    p_aciklama TEXT
)
RETURNS VOID AS $$
DECLARE
    v_var BOOLEAN;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM katilim
        WHERE kursiyer_id = p_kursiyer_id AND kurs_id = p_kurs_id
    ) THEN
        RAISE EXCEPTION 'Kursiyer (%), belirtilen kursa kayıtlı değil.', p_kursiyer_id;
    END IF;

    SELECT durum INTO v_var FROM devamsizlik
    WHERE kursiyer_id = p_kursiyer_id AND kurs_id = p_kurs_id AND tarih = p_tarih;

    IF FOUND THEN
        IF v_var = p_durum THEN
            IF p_durum THEN
                RAISE EXCEPTION 'Kursiyer (%), belirtilen günde zaten gelmiştir.', p_kursiyer_id;
            ELSE
                RAISE EXCEPTION 'Kursiyer (%), belirtilen günde zaten gelmemiştir.', p_kursiyer_id;
            END IF;
        ELSE
            UPDATE devamsizlik
            SET durum = p_durum,
                aciklama = p_aciklama
            WHERE kursiyer_id = p_kursiyer_id AND kurs_id = p_kurs_id AND tarih = p_tarih;
        END IF;
    ELSE
        INSERT INTO devamsizlik (kursiyer_id, kurs_id, tarih, durum, aciklama)
        VALUES (p_kursiyer_id, p_kurs_id, p_tarih, p_durum, p_aciklama);
    END IF;
END;
$$ LANGUAGE plpgsql;





