# main.py
import sys
import psycopg2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget,
    QLabel, QPushButton, QLineEdit, QDateEdit, QTableWidget, QTableWidgetItem,
    QMessageBox, QTextEdit, QComboBox, QGroupBox, QFormLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor

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

        # Tüm sekmeler
        self.kursiyer_tab = self.create_kursiyer_tab()
        self.egitimci_tab = self.create_egitimci_tab()
        self.kurs_tab = self.create_kurs_tab()
        self.devamsizlik_tab = self.create_devamsizlik_tab()
        self.kayit_guncelle_tab = self.create_kayit_guncelleme_tab()

        # Giriş paneli
        self.giris_paneli = self.create_giris_paneli()
        self.tabs.addTab(self.giris_paneli, "🏠 Giriş")

        # Diğer sekmeler
        self.tabs.addTab(self.kursiyer_tab, "👤 Kursiyer")
        self.tabs.addTab(self.egitimci_tab, "👨‍🏫 Eğitimci")
        self.tabs.addTab(self.kurs_tab, "📚 Kurs")
        self.tabs.addTab(self.devamsizlik_tab, "⛔ Devamsızlık")
        self.tabs.addTab(self.kayit_guncelle_tab, "🔄 Kayıt/Güncelleme")

    def create_giris_paneli(self):
        panel = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        layout.addStretch(1)

        # === Hoş geldiniz kutusu ===
        hosgeldin_box = QGroupBox()
        hosgeldin_layout = QVBoxLayout()
        hosgeldin_box.setStyleSheet("""
            QGroupBox {
                background-color: #f8f8f8;
                border: 1px solid #dcdcdc;
                border-radius: 10px;
                padding: 20px;
            }
        """)

        baslik = QLabel("📋 Halk Eğitim Takip Sistemi'ne Hoş Geldiniz")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        alt_baslik = QLabel("Lütfen işlem yapmak istediğiniz bölümü seçin:")
        alt_baslik.setAlignment(Qt.AlignCenter)
        alt_baslik.setStyleSheet("font-size: 14px; color: #666;")

        hosgeldin_layout.addWidget(baslik)
        hosgeldin_layout.addWidget(alt_baslik)
        hosgeldin_box.setLayout(hosgeldin_layout)

        layout.addWidget(hosgeldin_box)

        # === Ortak buton ayarları ===
        button_stylesheet = """
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #bdbdbd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-width: 200px;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """

        button_labels = [
            ("👤 Kursiyer İşlemleri", self.kursiyer_tab),
            ("👨‍🏫 Eğitimci İşlemleri", self.egitimci_tab),
            ("📚 Kurs İşlemleri", self.kurs_tab),
            ("⛔ Devamsızlık", self.devamsizlik_tab),
            ("🔄 Kayıt/Güncelleme", self.kayit_guncelle_tab),
        ]

        for label, tab in button_labels:
            btn = QPushButton(label)
            btn.setFixedSize(200, 45)
            btn.setStyleSheet(button_stylesheet)
            btn.clicked.connect(lambda _, t=tab: self.tabs.setCurrentWidget(t))

            btn_wrapper = QHBoxLayout()
            btn_wrapper.addStretch()
            btn_wrapper.addWidget(btn)
            btn_wrapper.addStretch()
            layout.addLayout(btn_wrapper)

        layout.addStretch(1)

        # === Katkı yazısı (sağ alt) ===
        contributors_layout = QHBoxLayout()
        contributors_layout.addStretch()
        contributors = QLabel("24574588 Erkin Tekin | 24574582 Selçuk Tunalı")
        contributors.setStyleSheet("font-size: 11px; color: gray;")
        contributors_layout.addWidget(contributors)
        layout.addLayout(contributors_layout)

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
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # === Form Kutusu ===
        form_group = QGroupBox("👨‍🏫 Eğitimci Bilgileri")
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

        self.e_ad = QLineEdit()
        self.e_soyad = QLineEdit()
        self.e_tc = QLineEdit()
        self.e_dogum = QLineEdit()
        self.e_tel = QLineEdit()
        self.e_email = QLineEdit()
        self.e_uzmanlik = QComboBox()
        self.e_uzmanlik.addItems(fetch_uzmanliklar())
        self.e_yonetici_id = QLineEdit()

        form_layout.addRow("Ad:", self.e_ad)
        form_layout.addRow("Soyad:", self.e_soyad)
        form_layout.addRow("TC Kimlik No:", self.e_tc)
        form_layout.addRow("Doğum Tarihi (YYYY-AA-GG):", self.e_dogum)
        form_layout.addRow("Telefon:", self.e_tel)
        form_layout.addRow("Email:", self.e_email)
        form_layout.addRow("Uzmanlık Alanı:", self.e_uzmanlik)
        form_layout.addRow("Yönetici ID:", self.e_yonetici_id)

        add_button = QPushButton("➕ Eğitimci Kaydet")
        add_button.setMinimumHeight(36)
        add_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        add_button.clicked.connect(self.add_egitimci)
        form_layout.addRow(add_button)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # === Listeleme Butonu ===
        listele_btn = QPushButton("📄 Eğitimcileri Listele")
        listele_btn.setMinimumHeight(36)
        listele_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        listele_btn.clicked.connect(self.list_egitimci)
        main_layout.addWidget(listele_btn)

        # === Tablo ===
        self.egitimci_table = QTableWidget()
        self.egitimci_table.setMinimumHeight(250)
        self.egitimci_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        main_layout.addWidget(self.egitimci_table)

        # === Sil Butonu ===
        sil_btn = QPushButton("🗑️ Seçili Eğitimciyi Sil")
        sil_btn.setMinimumHeight(36)
        sil_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        sil_btn.clicked.connect(self.egitimci_sil)
        main_layout.addWidget(sil_btn)

        tab.setLayout(main_layout)
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
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # === Form Kutusu ===
        form_group = QGroupBox("📚 Yeni Kurs Bilgileri")
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

        self.k_adi = QLineEdit()
        self.k_aciklama = QTextEdit()
        self.k_aciklama.setFixedHeight(60)
        self.k_sure = QLineEdit()
        self.k_baslangic = QLineEdit()
        self.k_bitis = QLineEdit()
        self.k_kontenjan = QLineEdit()
        self.k_egitimci_combo = QComboBox()
        self.yenile_egitmen_combo(self.k_egitimci_combo)

        form_layout.addRow("Kurs Adı:", self.k_adi)
        form_layout.addRow("Açıklama:", self.k_aciklama)
        form_layout.addRow("Süre (saat):", self.k_sure)
        form_layout.addRow("Başlangıç Tarihi (YYYY-AA-GG):", self.k_baslangic)
        form_layout.addRow("Bitiş Tarihi (YYYY-AA-GG):", self.k_bitis)
        form_layout.addRow("Kontenjan (1-100):", self.k_kontenjan)
        form_layout.addRow("Eğitimci:", self.k_egitimci_combo)

        kaydet_btn = QPushButton("➕ Kurs Oluştur")
        kaydet_btn.setMinimumHeight(36)
        kaydet_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        kaydet_btn.clicked.connect(self.kurs_ekle)
        form_layout.addRow(kaydet_btn)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # === Listeleme Butonu ===
        listele_btn = QPushButton("📄 Kursları Listele")
        listele_btn.setMinimumHeight(36)
        listele_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        listele_btn.clicked.connect(self.kurslari_listele)
        main_layout.addWidget(listele_btn)

        # === Tablo ===
        self.kurs_table = QTableWidget()
        self.kurs_table.setMinimumHeight(250)
        self.kurs_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        main_layout.addWidget(self.kurs_table)

        # === Sil Butonu ===
        self.sil_kurs_btn = QPushButton("🗑️ Seçili Kursu Sil")
        self.sil_kurs_btn.setMinimumHeight(36)
        self.sil_kurs_btn.setStyleSheet("background-color: #f44336; color: white; font-weight: bold;")
        self.sil_kurs_btn.clicked.connect(self.sil_kurs)
        main_layout.addWidget(self.sil_kurs_btn)

        tab.setLayout(main_layout)
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
            "ID", "Ad", "Açıklama", "Süre", "Başlangıç", "Bitiş", "Kayıtlı", "Kontenjan", "Eğitimci"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.kurs_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def sil_kurs(self):
        selected = self.kurs_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen silinecek kursu seçin.")
            return
        kurs_id = self.kurs_table.item(selected, 0).text()
        confirm = QMessageBox.question(
            self, "Onay", f"Kurs ID {kurs_id} silinsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            query = "SELECT sil_kurs(%s)"
            success, message = execute_function(query, (kurs_id,))
            if success:
                QMessageBox.information(self, "Bilgi", "Kurs silindi.")
                self.kurslari_listele()
                # dropdown’ları da yenile
                self.yenile_kurs_combo(self.combo_kurs_devamsizlik)
            else:
                QMessageBox.critical(self, "Hata", message)

    def create_kayit_guncelleme_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # === Kursiyeri Kursa Kaydet Bölümü ===
        kurs_kayit_group = QGroupBox("➕ Kursiyeri Kursa Kaydet")
        kurs_kayit_group.setStyleSheet("""
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
        kurs_kayit_form = QFormLayout()
        kurs_kayit_form.setSpacing(10)

        self.combo_kursiyer_kayit = QComboBox()
        self.combo_kurs_kayit = QComboBox()
        self.yenile_kursiyer_combo(self.combo_kursiyer_kayit)
        self.yenile_kurs_combo(self.combo_kurs_kayit)

        kurs_kayit_form.addRow("👤 Kursiyer:", self.combo_kursiyer_kayit)
        kurs_kayit_form.addRow("📚 Kurs:", self.combo_kurs_kayit)

        kayit_btn = QPushButton("✔️ Kursa Kaydet")
        kayit_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        kayit_btn.setMinimumHeight(36)
        kayit_btn.clicked.connect(self.kaydet_kursa_katilim)
        kurs_kayit_form.addRow(kayit_btn)

        kurs_kayit_group.setLayout(kurs_kayit_form)
        main_layout.addWidget(kurs_kayit_group)

        # === Kurs Eğitmeni Güncelleme Bölümü ===
        egitmen_guncelle_group = QGroupBox("🔄 Kurs Eğitmenini Güncelle")
        egitmen_guncelle_group.setStyleSheet("""
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
        egitmen_guncelle_form = QFormLayout()
        egitmen_guncelle_form.setSpacing(10)

        self.combo_kurs_guncelle = QComboBox()
        self.combo_egitmen_yeni = QComboBox()
        self.yenile_kurs_combo(self.combo_kurs_guncelle)
        self.yenile_egitmen_combo(self.combo_egitmen_yeni)

        egitmen_guncelle_form.addRow("📘 Kurs:", self.combo_kurs_guncelle)
        egitmen_guncelle_form.addRow("👨‍🏫 Yeni Eğitmen:", self.combo_egitmen_yeni)

        guncelle_btn = QPushButton("📝 Eğitmeni Güncelle")
        guncelle_btn.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        guncelle_btn.setMinimumHeight(36)
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
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # === Form Kutusu ===
        form_group = QGroupBox("⛔ Devamsızlık Kaydı")
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

        self.combo_kurs_devamsizlik = QComboBox()
        for k in fetch_function("SELECT kurs_id, kurs_adi FROM kurs"):
            self.combo_kurs_devamsizlik.addItem(f"{k[1]} (ID:{k[0]})", k[0])

        self.combo_kursiyer_devamsizlik = QComboBox()
        for k in fetch_function("SELECT kursiyer_id, ad, soyad FROM kursiyer"):
            self.combo_kursiyer_devamsizlik.addItem(f"{k[1]} {k[2]} (ID:{k[0]})", k[0])

        # Hızlı Tarih Girişi - QDateEdit kullanımı
        self.d_tarih = QDateEdit()
        self.d_tarih.setDate(QDate.currentDate())
        self.d_tarih.setDisplayFormat("yyyy-MM-dd")
        self.d_tarih.setCalendarPopup(True)
        self.d_tarih.setStyleSheet("""
            QDateEdit {
                padding: 5px;
                font-size: 12px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)

        self.d_durum = QComboBox()
        self.d_durum.addItems(["Yok", "Geldi"])
        self.d_aciklama = QTextEdit()
        self.d_aciklama.setFixedHeight(50)

        # Anlık Devam Oranı Göstergesi
        self.devam_durumu_label = QLabel("Devam Durumu: Kurs ve kursiyer seçin")
        self.devam_durumu_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                padding: 8px;
                border-radius: 4px;
                background-color: #f0f0f0;
                border: 1px solid #ddd;
            }
        """)

        # Değişiklik olaylarını bağlama
        self.combo_kursiyer_devamsizlik.currentTextChanged.connect(self.devam_durumu_goster)
        self.combo_kurs_devamsizlik.currentTextChanged.connect(self.devam_durumu_goster)

        form_layout.addRow("Kurs:", self.combo_kurs_devamsizlik)
        form_layout.addRow("Kursiyer:", self.combo_kursiyer_devamsizlik)
        form_layout.addRow("", self.devam_durumu_label)  # Devam durumu göstergesi
        form_layout.addRow("Tarih:", self.d_tarih)
        form_layout.addRow("Durum:", self.d_durum)
        form_layout.addRow("Açıklama:", self.d_aciklama)

        kaydet_btn = QPushButton("➕ Devamsızlık Kaydet")
        kaydet_btn.setMinimumHeight(36)
        kaydet_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        kaydet_btn.clicked.connect(self.devamsizlik_ekle)
        form_layout.addRow(kaydet_btn)

        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)

        # === Butonlar için Yatay Düzen ===
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Genel Devamsızlık Listele Butonu
        listele_btn = QPushButton("📄 Devamsızlık Listele")
        listele_btn.setMinimumHeight(36)
        listele_btn.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        listele_btn.clicked.connect(self.devamsizlik_listele)
        buttons_layout.addWidget(listele_btn)

        # Kişi Bazlı Devamsızlık Listele Butonu
        kisi_listele_btn = QPushButton("👤 Kişi Bazlı Devamsızlık")
        kisi_listele_btn.setMinimumHeight(36)
        kisi_listele_btn.setStyleSheet("background-color: #3F51B5; color: white; font-weight: bold;")
        kisi_listele_btn.clicked.connect(self.devamsizlik_listele_kisi)
        buttons_layout.addWidget(kisi_listele_btn)

        main_layout.addLayout(buttons_layout)

        # === Tablo ===
        self.devamsizlik_table = QTableWidget()
        self.devamsizlik_table.setMinimumHeight(250)
        self.devamsizlik_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
        """)
        main_layout.addWidget(self.devamsizlik_table)

        tab.setLayout(main_layout)
        return tab

    def devam_durumu_goster(self):
        """Seçilen kursiyer ve kurs için anlık devam durumunu gösterir"""
        kurs_id = self.combo_kurs_devamsizlik.currentData()
        kursiyer_id = self.combo_kursiyer_devamsizlik.currentData()

        if not kurs_id or not kursiyer_id:
            self.devam_durumu_label.setText("Devam Durumu: Kurs ve kursiyer seçin")
            self.devam_durumu_label.setStyleSheet("""
                QLabel {
                    background-color: #f0f0f0;
                    color: #666;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 4px;
                    border: 1px solid #ddd;
                }
            """)
            return

        try:
            result = fetch_function(
                "SELECT devam_orani, devam_durumu FROM katilim WHERE kursiyer_id = %s AND kurs_id = %s",
                (kursiyer_id, kurs_id)
            )

            if result and len(result) > 0:
                oran, durum = result[0]
                if oran is not None:
                    # Renk ve durum belirleme
                    if durum:  # %70 ve üzeri
                        renk = "#28a745"  # Yeşil
                        durum_text = "✅ Güvenli"
                        text_color = "white"
                    else:  # %70 altı
                        renk = "#dc3545"  # Kırmızı
                        durum_text = "⚠️ RİSKLİ"
                        text_color = "white"

                    self.devam_durumu_label.setText(f"Devam Oranı: %{oran:.1f} ({durum_text})")
                    self.devam_durumu_label.setStyleSheet(f"""
                        QLabel {{
                            background-color: {renk};
                            color: {text_color};
                            font-weight: bold;
                            padding: 8px;
                            border-radius: 4px;
                            border: 2px solid {renk};
                        }}
                    """)
                else:
                    self.devam_durumu_label.setText("Devam Durumu: Henüz devamsızlık verisi yok")
                    self.devam_durumu_label.setStyleSheet("""
                        QLabel {
                            background-color: #ffc107;
                            color: #212529;
                            font-weight: bold;
                            padding: 8px;
                            border-radius: 4px;
                            border: 1px solid #ffc107;
                        }
                    """)
            else:
                self.devam_durumu_label.setText("Devam Durumu: Bu kursiyer bu kursa kayıtlı değil!")
                self.devam_durumu_label.setStyleSheet("""
                    QLabel {
                        background-color: #6c757d;
                        color: white;
                        font-weight: bold;
                        padding: 8px;
                        border-radius: 4px;
                        border: 1px solid #6c757d;
                    }
                """)
        except Exception as e:
            self.devam_durumu_label.setText(f"Hata: {str(e)}")
            self.devam_durumu_label.setStyleSheet("""
                QLabel {
                    background-color: #dc3545;
                    color: white;
                    font-weight: bold;
                    padding: 8px;
                    border-radius: 4px;
                }
            """)

    def devamsizlik_ekle(self):
        kurs_id = self.combo_kurs_devamsizlik.currentData()
        kursiyer_id = self.combo_kursiyer_devamsizlik.currentData()
        tarih = self.d_tarih.date().toString("yyyy-MM-dd")  # QDateEdit'ten tarih al
        durum_text = self.d_durum.currentText()
        aciklama = self.d_aciklama.toPlainText().strip()

        if not all([kurs_id, kursiyer_id, tarih, durum_text]):
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurmalısınız.")
            return

        durum = True if durum_text == "Geldi" else False

        query = "SELECT devamsizlik_ekle(%s, %s, %s, %s, %s)"
        success, message = execute_function(query, (kursiyer_id, kurs_id, tarih, durum, aciklama))

        if success:
            QMessageBox.information(self, "Başarılı", message)
            # Devam durumunu güncelle
            self.devam_durumu_goster()
            # Listeyi otomatik yenileme
            self.devamsizlik_listele()
        else:
            QMessageBox.warning(self, "Hata", message)

    def devamsizlik_listele(self):
        kurs_id = self.combo_kurs_devamsizlik.currentData()
        tarih = self.d_tarih.date().toString("yyyy-MM-dd")

        try:
            kurs_id = int(kurs_id) if kurs_id is not None else None
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir kurs seçiniz.")
            return

        if not kurs_id:
            QMessageBox.warning(self, "Hata", "Lütfen bir kurs seçiniz.")
            return

        if not tarih:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir tarih seçiniz.")
            return

        query = "SELECT * FROM devamsizlik_listele(%s::INTEGER, %s::DATE)"
        rows = fetch_function(query, (kurs_id, tarih))

        if not rows:
            QMessageBox.information(self, "Bilgi", f"Seçilen kurs ve tarihe kadar devamsızlık kaydı bulunmamaktadır.")
            self.devamsizlik_table.setRowCount(0)
            return

        self.devamsizlik_table.setRowCount(len(rows))
        self.devamsizlik_table.setColumnCount(8)
        self.devamsizlik_table.setHorizontalHeaderLabels([
            "Kursiyer ID", "Ad", "Soyad", "Devam %", "Durum", "Son Tarih", "Son Durum", "Son Açıklama"
        ])

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                if col_idx == 3:  # Devam oranı
                    if value is not None:
                        item = QTableWidgetItem(f"{value:.1f}%")
                        if value < 70:
                            item.setBackground(QColor(255, 200, 200))  # Açık kırmızı
                            item.setForeground(QColor(139, 0, 0))  # Koyu kırmızı
                        elif value < 80:
                            item.setBackground(QColor(255, 255, 200))  # Sarı
                            item.setForeground(QColor(139, 69, 19))  # Kahverengi
                        else:
                            item.setBackground(QColor(200, 255, 200))  # Yeşil
                            item.setForeground(QColor(0, 100, 0))  # Koyu yeşil
                        self.devamsizlik_table.setItem(row_idx, col_idx, item)
                        continue
                    else:
                        value = "N/A"
                elif col_idx == 4:  # Devam durumu
                    value = "✔️ Geçer (%70+)" if value else "❌ Riskli (%70-)" if value is not None else "N/A"
                elif col_idx == 6:  # Son durum
                    value = "✅ Geldi" if value else "❌ Yok" if value is not None else "N/A"
                elif col_idx == 7:  # Son açıklama
                    value = value if value else "Yok"

                self.devamsizlik_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        # Tablo sütunlarını otomatik boyutlandırma
        self.devamsizlik_table.resizeColumnsToContents()

    def devamsizlik_listele_kisi(self):
        kurs_id = self.combo_kurs_devamsizlik.currentData()
        kursiyer_id = self.combo_kursiyer_devamsizlik.currentData()

        try:
            kurs_id = int(kurs_id) if kurs_id is not None else None
            kursiyer_id = int(kursiyer_id) if kursiyer_id is not None else None
        except (ValueError, TypeError):
            QMessageBox.warning(self, "Hata", "Geçerli bir kurs ve kursiyer seçiniz.")
            return

        if not all([kurs_id, kursiyer_id]):
            QMessageBox.warning(self, "Hata", "Lütfen kurs ve kursiyer seçiniz.")
            return

        query = "SELECT * FROM devamsizlik_listele_kisi(%s::INTEGER, %s::INTEGER)"
        rows = fetch_function(query, (kurs_id, kursiyer_id))

        if not rows:
            QMessageBox.information(self, "Bilgi", "Seçilen kursiyerin bu kursta devamsızlık kaydı bulunmamaktadır.")
            self.devamsizlik_table.setRowCount(0)
            return

        self.devamsizlik_table.setRowCount(len(rows))
        self.devamsizlik_table.setColumnCount(8)
        self.devamsizlik_table.setHorizontalHeaderLabels([
            "Kursiyer ID", "Ad", "Soyad", "Tarih", "Durum", "Açıklama", "Devam %", "Sonuç"
        ])

        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                if col_idx == 4:  # Durum sütunu
                    value = "✅ Geldi" if value else "❌ Yok"
                elif col_idx == 6:  # Devam oranı - Renk kodlaması
                    if value is not None:
                        item = QTableWidgetItem(f"{value:.1f}%")
                        if value < 70:
                            item.setBackground(QColor(255, 200, 200))  # Açık kırmızı
                            item.setForeground(QColor(139, 0, 0))  # Koyu kırmızı
                        elif value < 80:
                            item.setBackground(QColor(255, 255, 200))  # Sarı
                            item.setForeground(QColor(139, 69, 19))  # Kahverengi
                        else:
                            item.setBackground(QColor(200, 255, 200))  # Yeşil
                            item.setForeground(QColor(0, 100, 0))  # Koyu yeşil
                        self.devamsizlik_table.setItem(row_idx, col_idx, item)
                        continue
                    else:
                        value = "N/A"
                elif col_idx == 7:  # Sonuç
                    value = "✔️ Geçer (%70+)" if value else "❌ Riskli (%70-)"

                self.devamsizlik_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        # Tablo sütunlarını otomatik boyutlandırma
        self.devamsizlik_table.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())