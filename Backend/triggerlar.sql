CREATE OR REPLACE FUNCTION devamsizlik_guncelle()
RETURNS TRIGGER AS $$
DECLARE
    yok_yazilma INTEGER;
    girilen_gun INTEGER;
    katilim_yuzdesi DECIMAL(5,2);
    kursiyer INTEGER;
    kurs INTEGER;
BEGIN
    kursiyer := CASE WHEN TG_OP = 'DELETE' THEN OLD.kursiyer_id ELSE NEW.kursiyer_id END;
    kurs := CASE WHEN TG_OP = 'DELETE' THEN OLD.kurs_id ELSE NEW.kurs_id END;

    SELECT COUNT(*) INTO girilen_gun
    FROM devamsizlik
    WHERE kursiyer_id = kursiyer AND kurs_id = kurs;

    SELECT COUNT(*) INTO yok_yazilma
    FROM devamsizlik
    WHERE kursiyer_id = kursiyer AND kurs_id = kurs AND durum = FALSE;

    IF girilen_gun > 0 THEN
        katilim_yuzdesi := ((girilen_gun - yok_yazilma)::DECIMAL / girilen_gun) * 100;
    ELSE
        katilim_yuzdesi := 0;
    END IF;

    UPDATE katilim
    SET
        devam_orani = katilim_yuzdesi,
        devam_durumu = katilim_yuzdesi >= 70
    WHERE kursiyer_id = kursiyer AND kurs_id = kurs;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS devamsizlik_trigger ON devamsizlik;
CREATE TRIGGER devamsizlik_trigger
AFTER INSERT OR UPDATE OR DELETE ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION devamsizlik_guncelle();

CREATE OR REPLACE FUNCTION kontrol_devamsizlik_tarihi()
RETURNS TRIGGER AS $$
DECLARE
    baslangic DATE;
    bitis DATE;
BEGIN
    SELECT baslangic_tarihi, bitis_tarihi INTO baslangic, bitis
    FROM kurs WHERE kurs_id = NEW.kurs_id;

    IF NEW.tarih < baslangic OR NEW.tarih > bitis THEN
        RAISE EXCEPTION 'Devamsızlık tarihi kursun başlangıç ve bitiş tarihleri arasında olmalı!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_kontrol_devamsizlik_tarihi ON devamsizlik;
CREATE TRIGGER trg_kontrol_devamsizlik_tarihi
BEFORE INSERT ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION kontrol_devamsizlik_tarihi();

CREATE OR REPLACE FUNCTION devamsizlik_kontrol()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.tarih < CURRENT_DATE - INTERVAL '30 days' THEN
            RAISE EXCEPTION '30 günden eskiye devamsızlık girilemez: %', NEW.tarih;
        ELSIF NEW.tarih > CURRENT_DATE THEN
            RAISE EXCEPTION 'Gelecek tarihe devamsızlık girilemez: %', NEW.tarih;
        END IF;
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.tarih < CURRENT_DATE - INTERVAL '30 days' THEN
            RAISE EXCEPTION '30 günden eski bir tarihteki devamsızlık kaydı güncellenemez: %', OLD.tarih;
        ELSIF NEW.tarih > CURRENT_DATE THEN
            RAISE EXCEPTION 'Geleceğe ait devamsızlık kaydı olarak güncellenemez: %', NEW.tarih;
        END IF;
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        IF OLD.tarih < CURRENT_DATE - INTERVAL '30 days' THEN
            RAISE EXCEPTION '30 günden eski bir devamsızlık kaydı silinemez: %', OLD.tarih;
        END IF;
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_devamsizlik_kontrol ON devamsizlik;
CREATE TRIGGER trg_devamsizlik_kontrol
BEFORE INSERT OR UPDATE OR DELETE ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION devamsizlik_kontrol();

CREATE OR REPLACE FUNCTION engelle_devamsiz_girisi()
RETURNS TRIGGER AS $$
DECLARE
    devam_flag BOOLEAN;
BEGIN
    SELECT devam_durumu INTO devam_flag
    FROM katilim
    WHERE kursiyer_id = NEW.kursiyer_id AND kurs_id = NEW.kurs_id;

    IF devam_flag = FALSE THEN
        RAISE NOTICE 'Uyarı: Kursiyerin devam hakkı %%70 altına düşmüştür.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_devamsizlik_durumu_kontrol ON devamsizlik;
CREATE TRIGGER trg_devamsizlik_durumu_kontrol
BEFORE INSERT ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION engelle_devamsiz_girisi();

CREATE OR REPLACE FUNCTION guncelle_mevcut_kayit()
RETURNS TRIGGER AS $$
DECLARE
    sayi INTEGER;
    kurs_no INTEGER;
BEGIN
    kurs_no := CASE WHEN TG_OP = 'DELETE' THEN OLD.kurs_id ELSE NEW.kurs_id END;

    SELECT COUNT(*) INTO sayi FROM katilim WHERE kurs_id = kurs_no;

    UPDATE katilim
    SET mevcut_kayit = sayi
    WHERE kurs_id = kurs_no;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_guncelle_mevcut_kayit ON katilim;
CREATE TRIGGER trg_guncelle_mevcut_kayit
AFTER INSERT OR DELETE ON katilim
FOR EACH ROW
EXECUTE FUNCTION guncelle_mevcut_kayit();
