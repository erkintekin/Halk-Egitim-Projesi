# main.py
import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QTextEdit, QComboBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt

DB_PARAMS = {
    "host": "localhost",
    "database": "halk_egitim_db",
    "user": "postgres",
    "password": "12345",
    "port": "5432"
}

def execute_function(query, params=()):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
        return True, "İşlem başarılı."
    except psycopg2.Error as e:
        return False, e.diag.message_primary

def fetch_uzmanliklar():
    query = "SELECT ad FROM uzmanlik ORDER BY ad"
    return [row[0] for row in fetch_function(query)]


def fetch_function(query, params=()):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print("HATA:", e)
        return []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Halk Eğitim Takip Sistemi")
        self.setGeometry(200, 100, 1000, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tüm sekmeleri oluştur
        self.kursiyer_tab = self.create_kursiyer_tab()
        self.egitimci_tab = self.create_egitimci_tab()
        self.kurs_tab = self.create_kurs_tab()
        self.devamsizlik_tab = self.create_devamsizlik_tab()
        self.kayit_guncelle_tab = self.create_kayit_guncelleme_tab()

        # Giriş paneli en üstte olacak
        self.giris_paneli = self.create_giris_paneli()
        self.tabs.addTab(self.giris_paneli, "🏠 Giriş")

        # Diğer sekmeleri girişten sonra ekle
        self.tabs.addTab(self.kursiyer_tab, "👤 Kursiyer")
        self.tabs.addTab(self.egitimci_tab, "👨‍🏫 Eğitimci")
        self.tabs.addTab(self.kurs_tab, "📚 Kurs")
        self.tabs.addTab(self.devamsizlik_tab, "⛔ Devamsızlık")
        self.tabs.addTab(self.kayit_guncelle_tab, "🔄 Kayıt/Güncelleme")

    def create_giris_paneli(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)  # tüm içeriği ortala

        # === Üst boşluk (sayfanın ortasına yaklaşmak için) ===
        layout.addStretch(1)

        # === Başlık ===
        baslik = QLabel("📋 Halk Eğitim Takip Sistemi'ne Hoş Geldiniz")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(baslik)

        alt_baslik = QLabel("Lütfen işlem yapmak istediğiniz bölümü seçin:")
        alt_baslik.setAlignment(Qt.AlignCenter)
        alt_baslik.setStyleSheet("font-size: 14px;")
        layout.addWidget(alt_baslik)

        # === Butonlar ===
        buttons = [
            ("👤 Kursiyer İşlemleri", self.kursiyer_tab),
            ("👨‍🏫 Eğitimci İşlemleri", self.egitimci_tab),
            ("📚 Kurs İşlemleri", self.kurs_tab),
            ("⛔ Devamsızlık", self.devamsizlik_tab),
            ("🔄 Kayıt/Güncelleme", self.kayit_guncelle_tab),
        ]

        for label, tab in buttons:
            btn = QPushButton(label)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda _, t=tab: self.tabs.setCurrentWidget(t))
            layout.addWidget(btn)

        # === Alt boşluk ===
        layout.addStretch(2)

        panel.setLayout(layout)
        return panel

    # === Kursiyer Sekmesi ===
    def create_kursiyer_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # === Form Kutusu ===
        form_group = QGroupBox("🧾 Kursiyer Bilgileri")
        form_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 6px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                top: 5px;
            }
        """)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.k_ad = QLineEdit()
        self.k_soyad = QLineEdit()
        self.k_tc = QLineEdit()
        self.k_dogum = QLineEdit()
        self.k_tel = QLineEdit()
        self.k_email = QLineEdit()
        self.k_adres = QTextEdit()
        self.k_adres.setFixedHeight(60)

        form_layout.addRow("Ad:", self.k_ad)
        form_layout.addRow("Soyad:", self.k_soyad)
        form_layout.addRow("TC Kimlik No:", self.k_tc)
        form_layout.addRow("Doğum Tarihi (YYYY-AA-GG):", self.k_dogum)
        form_layout.addRow("Telefon:", self.k_tel)
        form_layout.addRow("Email:", self.k_email)
        form_layout.addRow("Adres:", self.k_adres)

        add_button = QPushButton("➕ Kursiyer Kaydet")
        add_button.setMinimumHeight(36)
        add_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        add_button.clicked.connect(self.add_kursiyer)
        form_layout.addRow(add_button)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # === Listeleme Butonu ===
        listele_btn = QPushButton("📄 Kursiyerleri Listele")
        listele_btn.setMinimumHeight(36)
        listele_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        listele_btn.clicked.connect(self.list_kursiyer)
        main_layout.addWidget(listele_btn)

        # === Tablo ===
        self.kursiyer_table = QTableWidget()
        self.kursiyer_table.setMinimumHeight(250)
        self.kursiyer_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        main_layout.addWidget(self.kursiyer_table)

        # === Sil Butonu ===
        sil_btn = QPushButton("🗑️ Seçili Kursiyeri Sil")
        sil_btn.setMinimumHeight(36)
        sil_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        sil_btn.clicked.connect(self.kursiyer_sil)
        main_layout.addWidget(sil_btn)

        tab.setLayout(main_layout)
        return tab

    def add_kursiyer(self):
        tc = self.k_tc.text().strip()
        email = self.k_email.text().strip()

        if not all([
            self.k_ad.text().strip(),
            self.k_soyad.text().strip(),
            tc,
            email
        ]):
            QMessageBox.warning(self, "Hata", "Tüm zorunlu alanları doldurmalısınız.")
            return

        if not tc.isdigit() or len(tc) != 11:
            QMessageBox.warning(self, "Hata", "TC Kimlik Numarası 11 haneli rakamlardan oluşmalıdır.")
            return

        if "@" not in email:
            QMessageBox.warning(self, "Hata", "Geçerli bir e-posta adresi giriniz.")
            return

        query = "SELECT kursiyer_kaydet(%s, %s, %s, %s, %s, %s, %s)"
        params = (
            tc,
            self.k_ad.text(),
            self.k_soyad.text(),
            self.k_dogum.text(),
            self.k_tel.text(),
            email,
            self.k_adres.toPlainText()
        )
        success, message = execute_function(query, params)
        QMessageBox.information(self, "Bilgi", message)

        self.yenile_kursiyer_combo(self.combo_kursiyer_devamsizlik)
        self.yenile_kursiyer_combo(self.combo_kursiyer_kayit)

    def kursiyer_sil(self):
        selected = self.kursiyer_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek kursiyeri seçin.")
            return
        kursiyer_id = self.kursiyer_table.item(selected, 0).text()
        confirm = QMessageBox.question(
            self, "Onay", f"Kursiyer ID {kursiyer_id} silinsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            query = "SELECT kursiyer_sil(%s)"
            success, message = execute_function(query, (kursiyer_id,))
            if success:
                QMessageBox.information(self, "Bilgi", "Kursiyer silindi.")
                self.list_kursiyer()
                # dropdown’ları da yenile
                self.yenile_kursiyer_combo(self.combo_kursiyer_devamsizlik)
            else:
                QMessageBox.critical(self, "Hata", message)

    def list_kursiyer(self):
        query = "SELECT * FROM kursiyer_listele()"
        rows = fetch_function(query)
        self.kursiyer_table.setRowCount(len(rows))
        self.kursiyer_table.setColumnCount(len(rows[0]) if rows else 0)
        self.kursiyer_table.setHorizontalHeaderLabels([
            "ID", "Ad", "Soyad", "TC", "Tel", "Email", "Adres", "Kayıt Tarihi"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.kursiyer_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # === Eğitimci Sekmesi ===
    def create_egitimci_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.e_ad = QLineEdit()
        self.e_soyad = QLineEdit()
        self.e_tc = QLineEdit()
        self.e_dogum = QLineEdit()
        self.e_tel = QLineEdit()
        self.e_email = QLineEdit()
        self.e_uzmanlik = QComboBox()
        self.e_uzmanlik.addItems(fetch_uzmanliklar())
        self.e_yonetici_id = QLineEdit()
        add_button = QPushButton("Eğitimci Kaydet")
        add_button.clicked.connect(self.add_egitimci)

        form_layout = QVBoxLayout()
        for label, widget in [
            ("Ad", self.e_ad), ("Soyad", self.e_soyad), ("TC Kimlik No", self.e_tc),
            ("Doğum Tarihi (YYYY-AA-GG)", self.e_dogum), ("Telefon", self.e_tel), ("Email", self.e_email),
            ("Uzmanlık Alanı", self.e_uzmanlik), ("Yönetici ID", self.e_yonetici_id)
        ]:
            form_layout.addWidget(QLabel(label))
            form_layout.addWidget(widget)
        form_layout.addWidget(add_button)

        self.egitimci_table = QTableWidget()
        listele_btn = QPushButton("Eğitimcileri Listele")
        listele_btn.clicked.connect(self.list_egitimci)

        sil_btn = QPushButton("Seçili Eğitimciyi Sil")
        sil_btn.clicked.connect(self.egitimci_sil)
        

        layout.addLayout(form_layout)
        layout.addWidget(listele_btn)
        layout.addWidget(self.egitimci_table)
        layout.addWidget(sil_btn)
        tab.setLayout(layout)
        return tab


    def add_egitimci(self):
        tc = self.e_tc.text().strip()
        email = self.e_email.text().strip()
        if not all([self.e_ad.text().strip(), self.e_soyad.text().strip(), tc, email]):
            QMessageBox.warning(self, "Hata", "Tüm zorunlu alanları doldurmalısınız.")
            return
        if not tc.isdigit() or len(tc) != 11:
            QMessageBox.warning(self, "Hata", "TC Kimlik Numarası 11 haneli rakamlardan oluşmalıdır.")
            return
        if "@" not in email:
            QMessageBox.warning(self, "Hata", "Geçerli bir e-posta adresi giriniz.")
            return

        query = "SELECT egitimci_kaydet(%s, %s, %s, %s, %s, %s, %s, %s)"
        params = (
            tc, self.e_ad.text(), self.e_soyad.text(),
            self.e_dogum.text(), self.e_tel.text(), email,
            self.e_uzmanlik.currentText(), self.e_yonetici_id.text() or None
        )
        success, message = execute_function(query, params)
        QMessageBox.information(self, "Bilgi", message)

    def egitimci_sil(self):
        selected = self.egitimci_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek eğitimciyi seçin.")
            return
        egitimci_id = self.egitimci_table.item(selected, 0).text()
        confirm = QMessageBox.question(
            self, "Onay", f"Eğitimci ID {egitimci_id} silinsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            query = "SELECT egitimci_sil(%s)"
            success, message = execute_function(query, (egitimci_id,))
            if success:
                QMessageBox.information(self, "Bilgi", "Eğitimci silindi.")
                self.list_egitimci()
            else:
                QMessageBox.critical(self, "Hata", message)


    def list_egitimci(self):
        query = "SELECT * FROM egitimci_listele()"
        rows = fetch_function(query)
        self.egitimci_table.setRowCount(len(rows))
        self.egitimci_table.setColumnCount(len(rows[0]) if rows else 0)
        self.egitimci_table.setHorizontalHeaderLabels([
            "ID", "Ad", "Soyad", "TC", "Doğum", "Telefon", "Email", "Uzmanlık"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.egitimci_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # === Kurs Sekmesi ===
    def yenile_kurs_combo(self, combo):
        combo.clear()
        for k in fetch_function("SELECT kurs_id, kurs_adi FROM kurs"):
            combo.addItem(f"{k[1]} (ID:{k[0]})", k[0])

    def yenile_kursiyer_combo(self, combo):
        combo.clear()
        for k in fetch_function("SELECT kursiyer_id, ad, soyad FROM kursiyer"):
            combo.addItem(f"{k[1]} {k[2]} (ID:{k[0]})", k[0])

    def yenile_egitmen_combo(self, combo):
        combo.clear()
        for e in fetch_function("SELECT egitimci_id, ad, soyad FROM egitimci"):
            combo.addItem(f"{e[1]} {e[2]} (ID:{e[0]})", e[0])

    def create_kurs_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.k_adi = QLineEdit()
        self.k_aciklama = QTextEdit()
        self.k_sure = QLineEdit()
        self.k_baslangic = QLineEdit()
        self.k_bitis = QLineEdit()
        self.k_kontenjan = QLineEdit()
        self.k_egitimci_combo = QComboBox()
        self.yenile_egitmen_combo(self.k_egitimci_combo)

        kaydet_btn = QPushButton("Kurs Oluştur")
        kaydet_btn.clicked.connect(self.kurs_ekle)
        listele_btn = QPushButton("Kursları Listele")
        listele_btn.clicked.connect(self.kurslari_listele)

        form = QVBoxLayout()
        for label, widget in [
            ("Kurs Adı", self.k_adi), ("Açıklama", self.k_aciklama),
            ("Süre (saat)", self.k_sure), ("Başlangıç Tarihi (YYYY-AA-GG)", self.k_baslangic),
            ("Bitiş Tarihi (YYYY-AA-GG)", self.k_bitis), ("Kontenjan (Max 100 kişi)", self.k_kontenjan),
            ("Eğitimci", self.k_egitimci_combo)
        ]:
            form.addWidget(QLabel(label))
            form.addWidget(widget)
        form.addWidget(kaydet_btn)

        self.kurs_table = QTableWidget()

        layout.addLayout(form)
        layout.addWidget(listele_btn)
        layout.addWidget(self.kurs_table)
        self.sil_kurs_btn = QPushButton("Seçili Kursu Sil")
        self.sil_kurs_btn.clicked.connect(self.sil_kurs)
        layout.addWidget(self.sil_kurs_btn)
        
        tab.setLayout(layout)
        return tab

    def kurs_ekle(self):
        query = "SELECT kurs_olustur(%s, %s, %s, %s, %s, %s, %s)"
        params = (
            self.k_adi.text(), self.k_aciklama.toPlainText(), int(self.k_sure.text()),
            self.k_baslangic.text(), self.k_bitis.text(),
            int(self.k_kontenjan.text()), self.k_egitimci_combo.currentData()
        )
        success, message = execute_function(query, params)
        QMessageBox.information(self, "Bilgi", message)

        self.yenile_kurs_combo(self.combo_kurs_devamsizlik)
        self.yenile_kurs_combo(self.combo_kurs_kayit)
        self.yenile_kurs_combo(self.combo_kurs_guncelle)
    
    def kurslari_listele(self):
        query = "SELECT * FROM kurs_listele()"
        rows = fetch_function(query)
        self.kurs_table.setRowCount(len(rows))
        self.kurs_table.setColumnCount(len(rows[0]) if rows else 0)
        self.kurs_table.setHorizontalHeaderLabels([
            "ID", "Ad", "Açıklama", "Süre", "Başlangıç", "Bitiş","Kayıtlı" ,"Kontenjan", "Eğitimci"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.kurs_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    def sil_kurs(self):
        selected = self.kurs_table.currentRow()
        kurs_id = self.kurs_table.item(selected, 0).text()
        if not kurs_id.isdigit():
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek kursu seçin.")
            return
        confirm = QMessageBox.question(
        self, "Onay", f"Kurs ID {kurs_id} silinsin mi?",
        QMessageBox.Yes | QMessageBox.No
    )
        if confirm == QMessageBox.Yes:
            query = "SELECT sil_kurs(%s)"
            success, message = execute_function(query, (kurs_id,))
            if success:
                QMessageBox.information(self, "Bilgi", "Kurs silindi.")
            else:
                QMessageBox.critical(self, "Hata", message)
        
        self.kurslari_listele()
        # dropdown’ları da yenile
        self.yenile_kurs_combo(self.combo_kurs_devamsizlik)

    # === Kayıt Güncelleme Sekmesi ===
    def create_kayit_guncelleme_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()

        # === Kursiyeri Kursa Kaydet Bölümü ===
        kurs_kayit_group = QGroupBox("Kursiyeri Kursa Kaydet")
        kurs_kayit_form = QFormLayout()

        self.combo_kursiyer_kayit = QComboBox()
        self.combo_kurs_kayit = QComboBox()
        self.yenile_kursiyer_combo(self.combo_kursiyer_kayit)
        self.yenile_kurs_combo(self.combo_kurs_kayit)

        kurs_kayit_form.addRow("Kursiyer:", self.combo_kursiyer_kayit)
        kurs_kayit_form.addRow("Kurs:", self.combo_kurs_kayit)

        kayit_btn = QPushButton("Kursa Kaydet")
        kayit_btn.clicked.connect(self.kaydet_kursa_katilim)
        kurs_kayit_form.addRow(kayit_btn)

        kurs_kayit_group.setLayout(kurs_kayit_form)
        main_layout.addWidget(kurs_kayit_group)

        # === Kurs Eğitmeni Güncelleme Bölümü ===
        egitmen_guncelle_group = QGroupBox("Kurs Eğitmenini Güncelle")
        egitmen_guncelle_form = QFormLayout()

        self.combo_kurs_guncelle = QComboBox()
        self.combo_egitmen_yeni = QComboBox()
        self.yenile_kurs_combo(self.combo_kurs_guncelle)
        self.yenile_egitmen_combo(self.combo_egitmen_yeni)

        egitmen_guncelle_form.addRow("Kurs:", self.combo_kurs_guncelle)
        egitmen_guncelle_form.addRow("Yeni Eğitmen:", self.combo_egitmen_yeni)

        guncelle_btn = QPushButton("Eğitmeni Güncelle")
        guncelle_btn.clicked.connect(self.guncelle_kurs_egitmeni)
        egitmen_guncelle_form.addRow(guncelle_btn)

        egitmen_guncelle_group.setLayout(egitmen_guncelle_form)
        main_layout.addWidget(egitmen_guncelle_group)

        tab.setLayout(main_layout)
        return tab

    def kaydet_kursa_katilim(self):
        kurs_id = self.combo_kurs_kayit.currentData()
        kursiyer_id = self.combo_kursiyer_kayit.currentData()

        query = "SELECT kursiyeri_kursa_kaydet(%s, %s)"
        success, message = execute_function(query, (kursiyer_id, kurs_id))
        QMessageBox.information(self, "Bilgi", message)

    def guncelle_kurs_egitmeni(self):
        kurs_id = self.combo_kurs_guncelle.currentData()
        yeni_egitmen_id = self.combo_egitmen_yeni.currentData()

        query = "SELECT kurs_egitimci_guncelle(%s, %s)"
        success, message = execute_function(query, (kurs_id, yeni_egitmen_id))
        QMessageBox.information(self, "Bilgi", message)

    # === Devamsızlık Sekmesi ===
    def create_devamsizlik_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.combo_kurs_devamsizlik = QComboBox()
        for k in fetch_function("SELECT kurs_id, kurs_adi FROM kurs"):
            self.combo_kurs_devamsizlik.addItem(f"{k[1]} (ID:{k[0]})", k[0])

        self.combo_kursiyer_devamsizlik = QComboBox()
        for k in fetch_function("SELECT kursiyer_id, ad, soyad FROM kursiyer"):
            self.combo_kursiyer_devamsizlik.addItem(f"{k[1]} {k[2]} (ID:{k[0]})", k[0])

        self.d_tarih = QLineEdit()
        self.d_durum = QComboBox()
        self.d_durum.addItems(["Yok", "Geldi"])
        self.d_aciklama = QTextEdit()

        kaydet_btn = QPushButton("Devamsızlık Kaydet")
        kaydet_btn.clicked.connect(self.devamsizlik_ekle)
        listele_btn = QPushButton("Devamsızlık Listele")
        listele_btn.clicked.connect(self.devamsizlik_listele)

        form = QVBoxLayout()
        form.addWidget(QLabel("Kurs"))
        form.addWidget(self.combo_kurs_devamsizlik)
        form.addWidget(QLabel("Kursiyer"))
        form.addWidget(self.combo_kursiyer_devamsizlik)
        form.addWidget(QLabel("Tarih (YYYY-AA-GG)"))
        form.addWidget(self.d_tarih)
        form.addWidget(QLabel("Durum"))
        form.addWidget(self.d_durum)
        form.addWidget(QLabel("Açıklama"))
        form.addWidget(self.d_aciklama)
        form.addWidget(kaydet_btn)

        self.devamsizlik_table = QTableWidget()

        layout.addLayout(form)
        layout.addWidget(listele_btn)
        layout.addWidget(self.devamsizlik_table)
        tab.setLayout(layout)
        return tab

    def devamsizlik_ekle(self):
        kurs_id = self.combo_kurs_devamsizlik.currentData()
        kursiyer_id = self.combo_kursiyer_devamsizlik.currentData()
        tarih = self.d_tarih.text().strip()
        durum_text = self.d_durum.currentText()
        aciklama = self.d_aciklama.toPlainText().strip()

        if not all([kurs_id, kursiyer_id, tarih, durum_text]):
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurmalısınız.")
            return

        durum = True if durum_text == "Geldi" else False

        query = "SELECT devamsizlik_ekle(%s, %s, %s, %s, %s)"
        success, message = execute_function(query, (kursiyer_id, kurs_id, tarih, durum, aciklama))
        QMessageBox.information(self, "Bilgi", message)

    def devamsizlik_listele(self):
        kurs_id = self.combo_kurs_devamsizlik.currentData()
        kursiyer_id = self.combo_kursiyer_devamsizlik.currentData()
        tarih = self.d_tarih.text().strip()

        if not all([kurs_id, kursiyer_id, tarih]):
            QMessageBox.warning(self, "Hata", "Lütfen zorunlu alanları doldurunuz.")
            return

        query = "SELECT * FROM devamsizlik_listele(%s, %s, %s)"
        rows = fetch_function(query, (kurs_id, kursiyer_id, tarih))
        self.devamsizlik_table.setRowCount(len(rows))
        self.devamsizlik_table.setColumnCount(8)
        self.devamsizlik_table.setHorizontalHeaderLabels([
            "Kursiyer ID", "Ad", "Soyad", "Tarih", "Durum", "Açıklama", "Devam %", "Sonuç"
        ])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                if col_idx == 4:
                    value = "Var" if value else "Yok"
                elif col_idx == 6:
                    value = f"{value:.2f}%"
                elif col_idx == 7:
                    value = "✔️ Geçti" if value else "❌ Kaldı"
                self.devamsizlik_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
