-- 1. DEVAMSIZLIK ORANI HESAPLAMA TRIGGERI
CREATE OR REPLACE FUNCTION devamsizlik_guncelle()
RETURNS TRIGGER AS $$
DECLARE
    yok_yazilma INTEGER;
    toplam_ders_gunu INTEGER;
    devam_eden_gun INTEGER;
    devam_yuzdesi DECIMAL(5,2);
    kursiyer INTEGER;
    kurs INTEGER;
    baslangic DATE;
    bitis DATE;
BEGIN
    kursiyer := CASE WHEN TG_OP = 'DELETE' THEN OLD.kursiyer_id ELSE NEW.kursiyer_id END;
    kurs := CASE WHEN TG_OP = 'DELETE' THEN OLD.kurs_id ELSE NEW.kurs_id END;

    -- Kursun başlangıç ve bitiş tarihlerini alma
    SELECT baslangic_tarihi, bitis_tarihi INTO baslangic, bitis
    FROM kurs WHERE kurs_id = kurs;

    -- Toplam ders günü hesaplama (hafta sonları dahil - gerekirse filtrelenebilir??)
    toplam_ders_gunu := bitis - baslangic + 1;

    -- Yoklama kayıtlarını sayma
    SELECT COUNT(*) INTO yok_yazilma
    FROM devamsizlik
    WHERE kursiyer_id = kursiyer AND kurs_id = kurs AND durum = FALSE;

    -- Devam eden gün sayısı
    devam_eden_gun := toplam_ders_gunu - yok_yazilma;

    -- Devam oranını hesapla
    IF toplam_ders_gunu > 0 THEN
        devam_yuzdesi := (devam_eden_gun::DECIMAL / toplam_ders_gunu) * 100;
    ELSE
        devam_yuzdesi := 100; -- Kurs henüz başlamamışsa %100 devamlılık
    END IF;

    -- Katılım tablosunu güncelleme
    UPDATE katilim
    SET
        devam_orani = devam_yuzdesi,
        devam_durumu = devam_yuzdesi >= 70
    WHERE kursiyer_id = kursiyer AND kurs_id = kurs;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS devamsizlik_trigger ON devamsizlik;
CREATE TRIGGER devamsizlik_trigger
AFTER INSERT OR UPDATE OR DELETE ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION devamsizlik_guncelle();

-- 2. DEVAMSIZLIK TARİH KONTROL TRIGGERI
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

-- 3. 30 GÜN SINIRI KONTROL TRIGGERI
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

-- 4. DEVAM DURUMU UYARI TRIGGERI
CREATE OR REPLACE FUNCTION engelle_devamsiz_girisi()
RETURNS TRIGGER AS $$
DECLARE
    mevcut_devam_orani DECIMAL(5,2);
BEGIN
    -- Mevcut devam oranını alma
    SELECT devam_orani INTO mevcut_devam_orani
    FROM katilim
    WHERE kursiyer_id = NEW.kursiyer_id AND kurs_id = NEW.kurs_id;

    -- %70'in altındaysa uyarı verme
    IF mevcut_devam_orani IS NOT NULL AND mevcut_devam_orani < 70 THEN
        RAISE NOTICE "UYARI: Kursiyer ID % - Devam oranı zaten %%%'ye düşmüştür!",
                     NEW.kursiyer_id, mevcut_devam_orani;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_devamsizlik_durumu_kontrol ON devamsizlik;
CREATE TRIGGER trg_devamsizlik_durumu_kontrol
BEFORE INSERT ON devamsizlik
FOR EACH ROW
EXECUTE FUNCTION engelle_devamsiz_girisi();

-- 5. MEVCUT KAYIT GÜNCELLEME TRIGGERI
CREATE OR REPLACE FUNCTION guncelle_mevcut_kayit()
RETURNS TRIGGER AS $$
DECLARE
    kurs_no INTEGER;
    yeni_sayi INTEGER;
BEGIN
    kurs_no := CASE WHEN TG_OP = 'DELETE' THEN OLD.kurs_id ELSE NEW.kurs_id END;

    -- Bu kursa kayıtlı toplam kursiyer sayısı
    SELECT COUNT(*) INTO yeni_sayi 
    FROM katilim 
    WHERE kurs_id = kurs_no;

    -- Aynı kurstaki TÜM kayıtları güncelleme
    UPDATE katilim
    SET mevcut_kayit = yeni_sayi
    WHERE kurs_id = kurs_no;

    RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_guncelle_mevcut_kayit ON katilim;
CREATE TRIGGER trg_guncelle_mevcut_kayit
AFTER INSERT OR DELETE ON katilim
FOR EACH ROW
EXECUTE FUNCTION guncelle_mevcut_kayit();
