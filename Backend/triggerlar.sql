CREATE OR REPLACE FUNCTION devamsizlik_guncelle()
RETURNS TRIGGER AS $$
DECLARE
    total_gun INTEGER;
    yok_yazilma INTEGER;
    katilim_yuzdesi DECIMAL(5,2);
    kurs_sure INTEGER;
BEGIN
    SELECT sure_saat INTO kurs_sure FROM kurs WHERE kurs_id = NEW.kurs_id;
    total_gun := CEIL(kurs_sure / 8.0);

    SELECT COUNT(*) INTO yok_yazilma
    FROM devamsizlik
    WHERE kursiyer_id = NEW.kursiyer_id AND kurs_id = NEW.kurs_id AND durum = TRUE;

    IF total_gun > 0 THEN
        katilim_yuzdesi := ((total_gun - yok_yazilma)::DECIMAL / total_gun) * 100;
    ELSE
        katilim_yuzdesi := 0;
    END IF;

    UPDATE katilim
    SET
        devam_orani = katilim_yuzdesi,
        devam_durumu = CASE
            WHEN katilim_yuzdesi < 70 THEN FALSE
            ELSE TRUE
        END
    WHERE kursiyer_id = NEW.kursiyer_id AND kurs_id = NEW.kurs_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS devamsizlik_trigger ON devamsizlik;

CREATE TRIGGER devamsizlik_trigger
AFTER INSERT OR UPDATE ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION devamsizlik_guncelle();

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
        IF OLD.tarih < CURRENT_DATE THEN
            RAISE EXCEPTION 'Geçmiş tarihteki devamsızlık kaydı güncellenemez: %', OLD.tarih;
        ELSIF NEW.tarih > CURRENT_DATE THEN
            RAISE EXCEPTION 'Geleceğe ait devamsızlık kaydı olarak güncellenemez: %', NEW.tarih;
        END IF;
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        IF OLD.tarih < CURRENT_DATE THEN
            RAISE EXCEPTION 'Geçmiş tarihteki devamsızlık kaydı silinemez: %', OLD.tarih;
        END IF;
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


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
        RAISE EXCEPTION 'Bu kursiyerin devam hakkı dolmuştur. Yeni devamsızlık girilemez.';
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
    IF TG_OP = 'INSERT' THEN
        kurs_no := NEW.kurs_id;
    ELSIF TG_OP = 'DELETE' THEN
        kurs_no := OLD.kurs_id;
    ELSE
        RETURN NULL;
    END IF;

    SELECT COUNT(*) INTO sayi
    FROM katilim
    WHERE kurs_id = kurs_no;

    UPDATE katilim
    SET mevcut_kayit = sayi
    WHERE kurs_id = kurs_no;

    IF TG_OP = 'INSERT' THEN
        RETURN NEW;
    ELSE
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_guncelle_mevcut_kayit ON katilim;

CREATE TRIGGER trg_guncelle_mevcut_kayit
AFTER INSERT OR DELETE ON katilim
FOR EACH ROW
EXECUTE FUNCTION guncelle_mevcut_kayit();




