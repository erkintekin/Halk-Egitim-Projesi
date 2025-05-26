CREATE OR REPLACE FUNCTION kursiyer_listele()
RETURNS TABLE (
    kursiyer_id INTEGER,
    ad VARCHAR,
    soyad VARCHAR,
    tc_no VARCHAR,
    telefon VARCHAR,
    email VARCHAR,
    adres VARCHAR,
    kayit_tarihi DATE
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        k.kursiyer_id,
        k.ad,
        k.soyad,
        k.tc_no,
        k.telefon,
        k.email,
        k.adres,
        k.kayit_tarihi
    FROM kursiyer k;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION egitimci_listele()
RETURNS TABLE (
    egitimci_id INTEGER,
    ad VARCHAR,
    soyad VARCHAR,
    tc_no VARCHAR,
    telefon VARCHAR,
    email VARCHAR,
    uzmanlik VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.egitimci_id,
        e.ad,
        e.soyad,
        e.tc_no,
        e.telefon,
        e.email,
        e.uzmanlik_alani
    FROM egitimci e;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION kurs_listele()
RETURNS TABLE (
    kurs_id INTEGER,
    kurs_adi VARCHAR,
    aciklama TEXT,
    sure_saat INTEGER,
    baslangic_tarihi DATE,
    bitis_tarihi DATE,
    kontenjan INTEGER,
    kayitli INTEGER,
    egitimci_adi TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        k.kurs_id,
        k.kurs_adi,
        k.aciklama,
        k.sure_saat,
        k.baslangic_tarihi,
        k.bitis_tarihi,
		CAST((SELECT COUNT(*) FROM katilim kt WHERE kt.kurs_id = k.kurs_id) AS INTEGER) AS kayitli,
        k.kontenjan,
        CONCAT(e.ad, ' ', e.soyad) AS egitimci_adi
    FROM kurs k
    JOIN egitimci e ON k.egitimci_id = e.egitimci_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION devamsizlik_listele(p_kurs_id INTEGER)
RETURNS TABLE (
    kursiyer_id INTEGER,
    ad VARCHAR,
    soyad VARCHAR,
    tarih DATE,
    durum BOOLEAN,
    aciklama TEXT,
    devam_orani DECIMAL(5,2),
    devam_durumu BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        d.kursiyer_id,
        k.ad,
        k.soyad,
        d.tarih,
        d.durum,
        d.aciklama,
        kt.devam_orani,
        kt.devam_durumu
    FROM devamsizlik d
    JOIN kursiyer k ON d.kursiyer_id = k.kursiyer_id
    JOIN katilim kt ON kt.kursiyer_id = d.kursiyer_id AND kt.kurs_id = d.kurs_id
    WHERE d.kurs_id = p_kurs_id
    ORDER BY d.tarih DESC;
END;
$$ LANGUAGE plpgsql;