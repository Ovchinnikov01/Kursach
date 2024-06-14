from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, make_response 
from flask_wtf import FlaskForm, CSRFProtect  
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import secrets
import os
import g

app = Flask(__name__)
app.secret_key = "secret key"

app.config['UPLOAD_FOLDER'] = 'static/product-images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE = 'database.db' 

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('PRAGMA foreign_keys = ON')  
    return conn

def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'logged_in' not in session or not session['logged_in']:
                return redirect(url_for('login'))
            if role and session['role'] != role:
                return 'У вас нет прав доступа.', 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

def create_tables():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subcategory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category(id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            image TEXT NOT NULL,
            price REAL NOT NULL,
            rating REAL DEFAULT 0,
            num_ratings INTEGER DEFAULT 0,
            subcategory_id INTEGER,
            FOREIGN KEY (subcategory_id) REFERENCES subcategory(id)
        );
    """)

    cursor.execute("SELECT * FROM category")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO category (name) VALUES
                ('Смартфоны и фототехника'),
                ('ПК, ноутбуки, периферия'),
                ('ТВ, консоли и аудио'),
                ('Бытовая техника'),
                ('Комплектующие для ПК');
        """)

    cursor.execute("SELECT * FROM subcategory")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO subcategory (name, category_id) VALUES
    ('Смартфоны и гаджеты', (SELECT id FROM category WHERE name = 'Смартфоны и фототехника')),
    ('Планшеты', (SELECT id FROM category WHERE name = 'Смартфоны и фототехника')),
    ('Фототехника', (SELECT id FROM category WHERE name = 'Смартфоны и фототехника')),
    ('Объективы',(SELECT id FROM category WHERE name = 'Смартфоны и фототехника')),
    ('Ноутбуки и аксессуары', (SELECT id FROM category WHERE name = 'ПК, ноутбуки, периферия')),
    ('Компьютеры и ПО', (SELECT id FROM category WHERE name = 'ПК, ноутбуки, периферия')),
    ('Периферия и аксессуары', (SELECT id FROM category WHERE name = 'ПК, ноутбуки, периферия')),
    ('Телевизоры и аксессуары', (SELECT id FROM category WHERE name = 'ТВ, консоли и аудио')),
    ('Консоли', (SELECT id FROM category WHERE name = 'ТВ, консоли и аудио')),
    ('Основные комплектующие', (SELECT id FROM category WHERE name = 'Комплектующие для ПК')),
    ('Материнская плата', (SELECT id FROM category WHERE name = 'Комплектующие для ПК')),
    ('Процессоры', (SELECT id FROM category WHERE name = 'Комплектующие для ПК')),
    ('Видеокарты', (SELECT id FROM category WHERE name = 'Комплектующие для ПК')),
    ('Оперативная память', (SELECT id FROM category WHERE name = 'Комплектующие для ПК')),
    ('Корпуса', (SELECT id FROM category WHERE name = 'Комплектующие для ПК')),
    ('Холодильники', (SELECT id FROM category WHERE name = 'Бытовая техника')),
    ('Стиральные машины', (SELECT id FROM category WHERE name = 'Бытовая техника')),
    ('Посудомоечные машины', (SELECT id FROM category WHERE name = 'Бытовая техника')),
    ('Варочные панели', (SELECT id FROM category WHERE name = 'Бытовая техника')),
    ('Блоки питания', (SELECT id FROM category WHERE name = 'Комплектующие для ПК'));

        """)
    cursor.execute("SELECT * FROM product")
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO product (name, code, image, price, subcategory_id) VALUES
    ('Телефон Realme Note 50', 'realme_note50', 'Realme.png', 15000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Samsung Galaxy S23 Ultra', 'samsung_s23_ultra', 'Samsung Galaxy S23 Ultra.jpg', 120000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Xiaomi Redmi Note 12 Pro', 'xiaomi_redmi_note12_pro', 'Xiaomi Redmi Note 12 Pro.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон OnePlus 11', 'oneplus_11', 'One.jpg', 70000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон OpenAI Pixel 7 Pro', 'google_pixel_7_pro', 'OpenAI Pixel 7 Pro.jpg', 90000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон iPhone 14 Pro Max', 'iphone_14_pro_max', 'iPhone 14 Pro Max.jpg', 120000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон HONOR Magic6 Pro', 'honor_magic6_pro', 'HONOR Magic6 Pro.jpg', 80000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Samsung Galaxy S22', 'samsung_s22', 'Samsung Galaxy S22.jpg', 70000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Realme GT 3', 'realme_gt3', 'Realme GT 3.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Vivo X50 Pro', 'vivo_x50_pro', 'Vivo X50 Pro.jpg', 85000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон OPPO Find X2', 'oppo_find_x2', 'OPPO Find X2.jpg', 95000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Motorola Edge 30 Pro', 'motorola_edge_30_pro', 'Motorola Edge 30 Pro.jpg', 65000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Sony Xperia 1 III', 'sony_xperia_1_iii', 'Sony Xperia 1 III.jpg', 100000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Телефон Huawei P60 Pro', 'huawei_p60_pro', 'Huawei P60 Pro.jpg', 75000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Умные часы Apple Watch Ultra', 'apple_watch_ultra', 'Apple Watch Ultra.jpg', 80000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Умные часы Samsung Galaxy Watch6', 'samsung_galaxy_watch6', 'Samsung Galaxy Watch6.jpg', 40000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Умные часы HUAWEI WATCH GT 4', 'huawei_watch_gt_4', 'HUAWEI WATCH GT 4.jpg', 70000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Фитнес-браслет Xiaomi Mi Band 8', 'xiaomi_mi_band_8', 'Xiaomi Smart Band 8.jpg', 5000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Смарт-часы  Samsung Galaxy Fit3', 'samsung_galaxy_fit3', 'Fit3.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),
    ('Портативная колонка JBL Flip 6', 'jbl_flip_6', 'Flip.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Смартфоны и гаджеты')),

    ('Планшет iPad Air (5th Gen)', 'apple_ipad_air_5th_gen', 'Apple iPad Air.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Samsung Galaxy Tab S9', 'samsung_galaxy_tab_s9', 'Samsung Galaxy Tab S9.jpg', 80000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Apple iPad Pro (4th Gen)', 'apple_ipad_pro_4th_gen', 'Apple iPad Pro (4th Gen).jpg', 110000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Microsoft Surface Go 3', 'microsoft_surface_go_3', 'Microsoft Surface Go 3.jpg', 100000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет HONOR Pad 9', 'honor_pad_9', 'HONOR Pad 9.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Samsung Galaxy Tab S8 Ultra', 'samsung_galaxy_tab_s8_ultra', 'Samsung Galaxy Tab S8 Ultra.jpg', 70000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Apple iPad (10th Gen)', 'apple_ipad_10th_gen', 'Apple iPad (10th Gen).jpg', 40000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Lenovo Tab P11 Pro', 'lenovo_tab_p11_pro', 'Lenovo Tab P11 Pro.jpg', 55000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
    ('Планшет Huawei MatePad 11', 'huawei_matepad_11', 'Huawei MatePad 11.jpg', 45000, (SELECT id FROM subcategory WHERE name = 'Планшеты')),
                       
    ('Фотоаппарат Canon EOS R8', 'canon_eos_r8', 'Canon EOS R8.jpg', 150000, (SELECT id FROM subcategory WHERE name = 'Фототехника')),
    ('Фотоаппарат Sony Alpha 7 IV', 'sony_alpha_7_iv', 'Alpha7.jpg', 200000, (SELECT id FROM subcategory WHERE name = 'Фототехника')),
    ('Фотоаппарат Canon EOS R5', 'canon_eos_r5', 'R5.jpg', 300000, (SELECT id FROM subcategory WHERE name = 'Фототехника')),
    ('Фотоаппарат Nikon Z9', 'nikon_z9', 'Z9.jpg', 450000, (SELECT id FROM subcategory WHERE name = 'Фототехника')),
    ('Фотоаппарат Sony Alpha 7R V', 'sony_alpha_7r_v', '7RV.jpg', 350000, (SELECT id FROM subcategory WHERE name = 'Фототехника')),
    ('Фотоаппарат Fujifilm X-H2', 'fujifilm_x_h2', 'X-H2.jpg', 180000, (SELECT id FROM subcategory WHERE name = 'Фототехника')),
    ('Объектив Canon EF 24', 'canon_ef_24_70mm_f_2_8l_ii_usm', 'EF24-70mm.jpg', 120000, (SELECT id FROM subcategory WHERE name = 'Объективы')),
    ('Объектив Sony FE 24', 'sony_fe_24_105mm_f_4_g_oss', '4GOSS.jpg', 80000, (SELECT id FROM subcategory WHERE name = 'Объективы')),
    ('Объектив Canon EF', 'canon_ef', 'EF.jpg', 250000, (SELECT id FROM subcategory WHERE name = 'Объективы')),
    ('Объектив Sony FE', 'sony_fe', 'Fe.jpg', 220000, (SELECT id FROM subcategory WHERE name = 'Объективы')),
    ('Объектив Nikon', 'nikon', 'Nikon.jpg', 200000, (SELECT id FROM subcategory WHERE name = 'Объективы')),
    ('Объектив Fujifilm XF', 'fujifilm_xf', 'FujifilmXF.jpg', 100000, (SELECT id FROM subcategory WHERE name = 'Объективы')),

    ('Ноутбук Apple MacBook Pro 14', 'apple_macbook_pro_14', 'Pro14.jpg', 200000, (SELECT id FROM subcategory WHERE name = 'Ноутбуки и аксессуары')),
    ('Ноутбук Lenovo Legion 7', 'lenovo_legion', 'Legion7.jpg', 150000, (SELECT id FROM subcategory WHERE name = 'Ноутбуки и аксессуары')),
    ('Ноутбук MSI Katana B12VFK-463XRU', 'katana', 'Katana.jpg', 180000, (SELECT id FROM subcategory WHERE name = 'Ноутбуки и аксессуары')),
    ('Ноутбук Acer Nitro 5', 'acer_nitro_5', 'Nitro5.jpg', 100000, (SELECT id FROM subcategory WHERE name = 'Ноутбуки и аксессуары')),
    ('Мышь Logitech MX Master 3S', 'logitech_mx_master_3s', 'Master.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Ноутбуки и аксессуары')),
    ('Клавиатура Razer Ornata V3', 'Ornata', 'Ornata.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Ноутбуки и аксессуары')),

    ('Компьютер MSI MEG Trident X', 'msi_meg_trident_x', 'Trident.jpg', 250000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Компьютер ASUS ROG Strix G15', 'asus_rog_strix_g15', 'Strix.jpg', 180000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Операционная система Windows 11 Pro', 'microsoft_windows_11_pro', '11Pro.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Антивирус Kaspersky Total Security', 'kaspersky_total_security', 'Security.jpg', 5000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),

    ('Монитор Samsung Odyssey G7', 'samsung_odyssey_g7', 'Odyssey.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Наушники Sennheiser Momentum 4 Wireless', 'sennheiser_momentum_4_wireless', 'Wireless.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Внешний жесткий диск Seagate Backup Plus', 'seagate_backup_plus', 'Plus.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Веб-камера Logitech BRIO 500', 'logitech_c925e', 'BRIO.jpg', 5000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),

    ('Телевизор Samsung QN65Q80A', 'samsung_qn65q80a', 'Samsungy.jpg', 150000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('Телевизор LG OLED55C1PUB', 'lg_oled55c1pub', 'LG.jpg', 180000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('Саундбар Sony HT-A7000', 'sony_ht_a7000', 'SonyHT.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('HIPER IoT IR2', 'HIPER', 'HIPER.jpg', 2000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),

    ('Игровая консоль PlayStation 5', 'sony_playstation_5', 'Play.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Консоли')),
    ('Игровая консоль Xbox Series X', 'microsoft_xbox_series_x', 'Seriesx.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Консоли')),
    ('Игровая консоль Nintendo Switch', 'nintendo_switch', 'Nintendo.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Консоли')),
    ('Игровая приставка PlayStation DualSense', 'sony_ps5_dualsense', 'DualSense.jpg', 7000, (SELECT id FROM subcategory WHERE name = 'Консоли')),
    ('Игровая приставка Microsoft Xbox Series S', 'microsoft_xbox_series', 'SeriesS.jpg', 6000, (SELECT id FROM subcategory WHERE name = 'Консоли')),
    
    ('Процессор Intel Core i9-13900K', 'intel_core_i9_13900k', 'Corei9.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Процессоры')),
    ('Видеокарта Palit GeForce RTX 4090', 'nvidia_geforce_rtx_4090', 'Palit.jpg', 150000, (SELECT id FROM subcategory WHERE name = 'Видеокарты')),
    ('Оперативная память Kingston Fury Beast DDR5', 'kingston_fury_beast_ddr5', 'KingstonFury.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Оперативная память')),
    ('Материнская плата ASUS ROG Strix Z790-E', 'asus_rog_strix_z790_e', 'ASUSROG.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Материнская плата')),
    ('Блок питания Corsair RM850x', 'corsair_rm850x', 'Corsair.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('SSD-накопитель Samsung 990 PRO', 'samsung_990_pro', 'Samsung9.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Основные комплектующие')),
    ('Корпус для ПК Cooler Master MasterBox NR600', 'coolermaster_masterbox_nr600', 'Cooler.jpg', 8000, (SELECT id FROM subcategory WHERE name = 'Корпуса')),
    ('SSD-накопитель Kingston A400', 'kingstona', 'Kingstona.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Основные комплектующие')),
    ('Охлаждение для процессора ID-COOLING SE-224-XTS ARGB', 'ID-COOLING', 'ID-COOLING.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Основные комплектующие')),
    ('Блок питания DEEPCOOL DQ750', 'DEEPCOOL', 'DEEPCOOL.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Основные комплектующие')),
    ('Оперативная память ADATA XPG Lancer Blade RGB', 'ADAT', 'ADATA.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Основные комплектующие')),
    ('Материнская плата MSI B760 GAMING PLUS WIFI', 'msib', 'MSIb.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Материнская плата')),
    ('Материнская плата MSI PRO Z790-P WIFI', 'msi_pro', 'MSIp.jpg', 35000, (SELECT id FROM subcategory WHERE name = 'Материнская плата')),
    ('Материнская плата Gigabyte Z790 AORUS Elite AX', 'gigabyte_z790_aorus_elite_ax', 'Gigabyte.jpg', 28000, (SELECT id FROM subcategory WHERE name = 'Материнская плата')),
    ('Процессор Intel Core i7-14700K BOX', 'intel_core_i7', 'Intel7.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Процессоры')),
    ('Процессор AMD Ryzen 9 7950X', 'amd_ryzen_9_7950x', 'AMD.jpg', 55000, (SELECT id FROM subcategory WHERE name = 'Процессоры')),
    ('Видеокарта ASUS GeForce RTX 4080 SUPER', 'nvidia_4080', 'ASUSs.jpg', 150000, (SELECT id FROM subcategory WHERE name = 'Видеокарты')),
    ('Видеокарта AMD Radeon RX 7900 XT', 'amd_radeon_rx_7900_xt', 'AMDr.jpg', 120000, (SELECT id FROM subcategory WHERE name = 'Видеокарты')),
    ('Оперативная память Kingston FURY Renegade ', 'Kingston', 'Kingstonf.jpg', 12000, (SELECT id FROM subcategory WHERE name = 'Оперативная память')),
    ('Оперативная память G.Skill Trident Z5 Neo DDR5', 'gskill_trident_z5_neo_ddr5', 'G.Skill.jpg', 13000, (SELECT id FROM subcategory WHERE name = 'Оперативная память')),
    ('Корпус для ПК ARDOR GAMING Rare M2 ARGB черный', 'ardorg', 'ARDOR.jpg', 8000, (SELECT id FROM subcategory WHERE name = 'Корпуса')),
    ('Корпус для ПК Cougar Duoface Pro RGB White белый', 'cougar', 'Cougar.jpg', 12000, (SELECT id FROM subcategory WHERE name = 'Корпуса')),
    ('Блок питания Montech TITAN GOLD 850', 'montech', 'Montech.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('Блок питания DEEPCOOL PQ1000M', 'DEEPCOOl', 'DEEPCOOLl.jpg', 13000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('Кулер для процессора ID-COOLING SE-224-XTS ARGB WHITE', 'ID-COOLIN', 'ID-COOLING2.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Комплектующие для ПК')),
    ('Холодильник Samsung RS61R5041SL/WT', 'samsung_rs', 'Samsungrs.jpg', 100000, (SELECT id FROM subcategory WHERE name = 'Холодильники')),
    ('Холодильник Bosch KGN49XI30U ', 'bosch_kgr', 'Bosch.jpg', 80000, (SELECT id FROM subcategory WHERE name = 'Холодильники')),
    ('Холодильник LG GC-B257JLYV', 'lg_gc', 'LGgs.jpg', 90000, (SELECT id FROM subcategory WHERE name = 'Холодильники')),
    ('Стиральная машина Bosch WAN24200ME', 'bosch_w', 'Boschс.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Стиральные машины')),
    ('Стиральная машина Samsung WW90T554CAT/LD', 'samsung_ww', 'Samsungld.jpg', 70000, (SELECT id FROM subcategory WHERE name = 'Стиральные машины')),
    ('Стиральная машина LG F2J3NS1W', 'lg', 'LGf.jpg', 55000, (SELECT id FROM subcategory WHERE name = 'Стиральные машины')),
    ('Посудомоечная машина Bosch Serie 4 SMS44DW01T', 'bosch_se', 'Boschs.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Посудомоечные машины')),
    ('Посудомоечная машина Samsung DW60M6050BB/WT', 'samsung_w', 'Samsungdw.jpg', 45000, (SELECT id FROM subcategory WHERE name = 'Посудомоечные машины')),
    ('Посудомоечная машина DEXP DWF45A3', 'dexp', 'DEXP.jpg', 20000, (SELECT id FROM subcategory WHERE name = 'Посудомоечные машины')),
    ('Варочная панель Bosch PIE631F17E', 'bosch_pie631f17e', 'Boschpi.jpg', 35000, (SELECT id FROM subcategory WHERE name = 'Варочные панели')),
    ('Варочная панель Samsung NZ32R1506BK/WT', 'samsung_nz', 'Samsungnz.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Варочные панели')),
                    
    ('Блок питания MONTECH GAMMA II 650', 'montechg', 'MONTECH GAMMA.jpg', 15000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('Блок питания Cougar GEC 750', 'cougargec', 'Cougargec.jpg', 13000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('Блок питания DeepCool PX1000G WH', 'DeepCoowh', 'DeepCoolwh.jpg', 14000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('Блок питания MONTECH GAMMA II 550', 'MONTECHgamma', 'MONTECHg.jpg', 12000, (SELECT id FROM subcategory WHERE name = 'Блоки питания')),
    ('Компьютер ARDOR GAMING RAGE H335', 'ardor', 'ARDORg.jpg', 250000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Компьютер ARDOR GAMING RAGE H332', 'ardort5', 'ARDORd.jpg', 180000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Компьютер Apple Mac mini', 'applemac', 'Applemac.jpg', 100000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Компьютер ASUS ROG STRIX', 'asusstrix', 'ASUSstrix.jpg', 5000, (SELECT id FROM subcategory WHERE name = 'Компьютеры и ПО')),
    ('Монитор Samsung Odyssey G7', 'samsung_odyssey_g7', 'OdysseyG7.jpg', 60000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Наушники Беспроводные/проводные EPOS Sennheiser MOMENTUM 4', 'epos', 'MOMENTUM.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Внешний жесткий диск SSD Samsung T7', 'samsungt7', 'SSD.jpg', 10000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Веб-камера Logitech C1000e', 'logitech_c925e', 'Logitechc.jpg', 5000, (SELECT id FROM subcategory WHERE name = 'Периферия и аксессуары')),
    ('Телевизор Xiaomi TV A2 55', 'xiaomitv', 'Xiaomitv.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('Телевизор LG OLED55A2RLA', 'lg_oled', 'LGoled.jpg', 180000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('Саундбар Philips TAB7807/10', 'phillipstab', 'Philips.jpg', 50000, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('Кронштейн для ТВ Harper TVM-1742', 'Harper', 'Harper.jpg', 500, (SELECT id FROM subcategory WHERE name = 'Телевизоры и аксессуары')),
    ('Процессор Intel Core i7-13700KF OEM', 'intel_core_i7', 'Intel Core i7.jpg', 30000, (SELECT id FROM subcategory WHERE name = 'Процессоры')),
    ('Процессор AMD Ryzen 5 7500F OEM', 'amd_ryzen_5', 'AMD5.jpg', 17000, (SELECT id FROM subcategory WHERE name = 'Процессоры')),
    ('Видеокарта MSI GeForce RTX 4060 VENTUS 2X WHITE OC', 'nvidia_geforce_rtx_4060', 'MSI4060.jpg', 35000, (SELECT id FROM subcategory WHERE name = 'Видеокарты')),
    ('Видеокарта Sapphire AMD Radeon RX 7800 XT NITRO+', 'amd_radeon', 'Sapphire.jpg', 120000, (SELECT id FROM subcategory WHERE name = 'Видеокарты'));

        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            profile_picture TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            total_price REAL NOT NULL,
            status TEXT DEFAULT 'Новый',  
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username));
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES product(id));
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_characteristics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            name TEXT,
            value TEXT,
            FOREIGN KEY (product_id) REFERENCES product(id) 
        )
    """)

    characteristics = [
    [(1, 'Цвет', 'Черный'), (1, 'Память', '128 ГБ'), (1, 'Оперативная память', '8 ГБ')],
    [(2, 'Цвет', 'Синий'), (2, 'Камера', '108 МП'), (2, 'Экран', '6.7 дюймов')], 
    [(3, 'Цвет', 'Красный'), (3, 'Батарея', '5000 мАч'), (3, 'Зарядка', 'Быстрая зарядка')],
    [(4, 'Цвет', 'Серый'), (4, 'Память', '256 ГБ'), (4, 'Оперативная память', '12 ГБ')],
    [(5, 'Цвет', 'Белый'), (5, 'Камера', '50 МП'), (5, 'Экран', '6.4 дюймов')], 
    [(6, 'Цвет', 'Черный'), (6, 'Память', '512 ГБ'), (6, 'Оперативная память', '16 ГБ')],
    [(7, 'Цвет', 'Синий'), (7, 'Память', '128 ГБ'), (7, 'Оперативная память', '8 ГБ')],
    [(8, 'Цвет', 'Черный'), (8, 'Память', '128 ГБ'), (8, 'Оперативная память', '8 ГБ')],
    [(9, 'Цвет', 'Синий'), (9, 'Память', '256 ГБ'), (9, 'Оперативная память', '12 ГБ')],
    [(10, 'Цвет', 'Черный'), (10, 'Память', '128 ГБ'), (10, 'Оперативная память', '8 ГБ')],
    [(11, 'Цвет', 'Синий'), (11, 'Память', '256 ГБ'), (11, 'Оперативная память', '12 ГБ')],
    [(12, 'Цвет', 'Черный'), (12, 'Память', '128 ГБ'), (12, 'Оперативная память', '8 ГБ')],
    [(13, 'Цвет', 'Белый'), (13, 'Память', '256 ГБ'), (13, 'Оперативная память', '12 ГБ')],
    [(14, 'Цвет', 'Черный'), (14, 'Память', '128 ГБ'), (14, 'Оперативная память', '8 ГБ')],
    [(15, 'Цвет', 'Серебристый'), (15, 'Размер', '41 мм'), (15, 'Аккумулятор', '18 часов')],
    [(16, 'Цвет', 'Серебристый'), (16, 'Размер', '44 мм'), (16, 'Аккумулятор', '20 часов')],
    [(17, 'Цвет', 'Черный'), (17, 'Размер', '46 мм'), (17, 'Аккумулятор', '14 дней')],
    [(18, 'Цвет', 'Черный'), (18, 'Материал', 'выв'), (18, 'Аккумулятор', '14 дней')],
    [(19, 'Цвет', 'Черный'), (19, 'Материал', 'вывы'), (19, 'Аккумулятор', '7 дней')],
    [(20, 'Цвет', 'Черный'), (20, 'Bluetooth', '5.3'), (20, 'Водонепроницаемость', 'IP67')],
    [(21, 'Цвет', 'Черный'), (21, 'Память', '128 ГБ'), (21, 'Оперативная память', '8 ГБ')],
    [(22, 'Цвет', 'Синий'), (22, 'Камера', '108 МП'), (22, 'Экран', '6.7 дюймов')], 
    [(23, 'Цвет', 'Красный'), (23, 'Батарея', '5000 мАч'), (23, 'Зарядка', 'Быстрая зарядка')],
    [(24, 'Цвет', 'Серый'), (24, 'Память', '256 ГБ'), (24, 'Оперативная память', '12 ГБ')],
    [(25, 'Цвет', 'Белый'), (25, 'Камера', '50 МП'), (25, 'Экран', '6.4 дюймов')], 
    [(26, 'Цвет', 'Черный'), (26, 'Память', '512 ГБ'), (26, 'Оперативная память', '16 ГБ')],
    [(27, 'Цвет', 'Синий'), (27, 'Память', '128 ГБ'), (27, 'Оперативная память', '8 ГБ')],
    [(28, 'Цвет', 'Черный'), (28, 'Память', '128 ГБ'), (28, 'Оперативная память', '8 ГБ')],
    [(29, 'Цвет', 'Синий'), (29, 'Память', '256 ГБ'), (29, 'Оперативная память', '12 ГБ')],
    [(30, 'Цвет', 'Черный'), (30, 'Память', '128 ГБ'), (30, 'Оперативная память', '8 ГБ')],
    [(31, 'Цвет', 'Синий'), (31, 'Память', '256 ГБ'), (31, 'Оперативная память', '12 ГБ')],
    [(32, 'Цвет', 'Черный'), (32, 'Память', '128 ГБ'), (32, 'Оперативная память', '8 ГБ')],
    [(33, 'Цвет', 'Белый'), (33, 'Память', '256 ГБ'), (33, 'Оперативная память', '12 ГБ')],
    [(34, 'Цвет', 'Черный'), (34, 'Память', '128 ГБ'), (34, 'Оперативная память', '8 ГБ')],
    [(35, 'Цвет', 'Серебристый'), (35, 'Размер', '41 мм'), (35, 'Аккумулятор', '18 часов')],
    [(36, 'Цвет', 'Серебристый'), (36, 'Размер', '44 мм'), (36, 'Аккумулятор', '20 часов')],
    [(37, 'Цвет', 'Черный'), (37, 'Размер', '46 мм'), (37, 'Аккумулятор', '14 дней')],
    [(38, 'Цвет', 'Черный'), (38, 'Материал', 'ввы'), (38, 'Аккумулятор', '14 дней')],
    [(39, 'Цвет', 'Черный'), (39, 'Материал', 'выв'), (39, 'Аккумулятор', '7 дней')],
    [(40, 'Цвет', 'Черный'), (40, 'Bluetooth', '5.3'), (40, 'Водонепроницаемость', 'IP67')],
    [(41, 'Цвет', 'Серый'), (41, 'Память', '256 ГБ'), (41, 'Оперативная память', '8 ГБ')],
    [(42, 'Цвет', 'Серебристый'), (42, 'Память', '512 ГБ'), (42, 'Оперативная память', '8 ГБ')],
    [(43, 'Цвет', 'Серый'), (43, 'Память', '256 ГБ'), (43, 'Оперативная память', '8 ГБ')],
    [(44, 'Цвет', 'Черный'), (44, 'Память', '256 ГБ'), (44, 'Оперативная память', '8 ГБ')],
    [(45, 'Цвет', 'Серебристый'), (45, 'Память', '256 ГБ'), (45, 'Оперативная память', '8 ГБ')],
    [(46, 'Цвет', 'Серый'), (46, 'Память', '256 ГБ'), (46, 'Оперативная память', '8 ГБ')],
    [(47, 'Цвет', 'Золотой'), (47, 'Память', '256 ГБ'), (47, 'Оперативная память', '8 ГБ')],
    [(48, 'Цвет', 'Серый'), (48, 'Память', '512 ГБ'), (48, 'Оперативная память', '16 ГБ')],
    [(49, 'Цвет', 'Серебристый'), (49, 'Память', '512 ГБ'), (49, 'Оперативная память', '16 ГБ')],
    [(50, 'Цвет', 'Серый'), (50, 'Память', '512 ГБ'), (50, 'Оперативная память', '16 ГБ')],
    [(51, 'Цвет', 'Серебристый'), (51, 'Память', '1 ТБ'), (51, 'Оперативная память', '16 ГБ')],
    [(52, 'Цвет', 'Серый'), (52, 'Память', '1 ТБ'), (52, 'Оперативная память', '16 ГБ')],
    [(53, 'Цвет', 'Серый'), (53, 'Память', '1 ТБ'), (53, 'Оперативная память', '16 ГБ')],
    [(54, 'Цвет', 'Серый'), (54, 'Память', '1 ТБ'), (54, 'Оперативная память', '16 ГБ')],
    [(55, 'Цвет', 'Серый'), (55, 'Память', '1 ТБ'), (55, 'Оперативная память', '16 ГБ')],
    [(56, 'Цвет', 'Серый'), (56, 'Память', '1 ТБ'), (56, 'Оперативная память', '16 ГБ')],
    [(57, 'Цвет', 'Черный'), (57, 'Память', '128 ГБ'), (57, 'Оперативная память', '8 ГБ')],
    [(58, 'Цвет', 'Синий'), (58, 'Камера', '108 МП'), (58, 'Экран', '6.7 дюймов')], 
    [(59, 'Цвет', 'Красный'), (59, 'Батарея', '5000 мАч'), (59, 'Зарядка', 'Быстрая зарядка')],
    [(60, 'Цвет', 'Серый'), (60, 'Память', '256 ГБ'), (60, 'Оперативная память', '12 ГБ')],
    [(61, 'Цвет', 'Белый'), (61, 'Камера', '50 МП'), (61, 'Экран', '6.4 дюймов')],
    [(62, 'Цвет', 'Черный'), (62, 'Память', '512 ГБ'), (62, 'Оперативная память', '16 ГБ')],
    [(63, 'Цвет', 'Синий'), (63, 'Память', '128 ГБ'), (63, 'Оперативная память', '8 ГБ')],
    [(64, 'Цвет', 'Черный'), (64, 'Память', '128 ГБ'), (64, 'Оперативная память', '8 ГБ')],
    [(65, 'Цвет', 'Синий'), (65, 'Память', '256 ГБ'), (65, 'Оперативная память', '12 ГБ')],
    [(66, 'Цвет', 'Черный'), (66, 'Память', '128 ГБ'), (66, 'Оперативная память', '8 ГБ')],
    [(67, 'Цвет', 'Синий'), (67, 'Память', '256 ГБ'), (67, 'Оперативная память', '12 ГБ')],
    [(68, 'Цвет', 'Черный'), (68, 'Память', '128 ГБ'), (68, 'Оперативная память', '8 ГБ')],
    [(69, 'Цвет', 'Белый'), (69, 'Память', '256 ГБ'), (69, 'Оперативная память', '12 ГБ')],
    [(70, 'Цвет', 'Черный'), (70, 'Память', '128 ГБ'), (70, 'Оперативная память', '8 ГБ')],
    [(71, 'Цвет', 'Серебристый'), (71, 'Размер', '41 мм'), (71, 'Аккумулятор', '18 часов')],
    [(72, 'Цвет', 'Серебристый'), (72, 'Размер', '44 мм'), (72, 'Аккумулятор', '20 часов')],
    [(73, 'Цвет', 'Черный'), (73, 'Размер', '46 мм'), (73, 'Аккумулятор', '14 дней')],
    [(74, 'Цвет', 'Черный'), (74, 'Материал', 'аваы'), (74, 'Аккумулятор', '14 дней')],
    [(75, 'Цвет', 'Черный'), (75, 'Материал', 'ыфы'), (75, 'Аккумулятор', '7 дней')],
    [(76, 'Цвет', 'Черный'), (76, 'Bluetooth', '5.3'), (76, 'Водонепроницаемость', 'IP67')],
    [(77, 'Цвет', 'Серый'), (77, 'Память', '256 ГБ'), (77, 'Оперативная память', '8 ГБ')],
    [(78, 'Цвет', 'Серебристый'), (78, 'Память', '512 ГБ'), (78, 'Оперативная память', '8 ГБ')],
    [(79, 'Цвет', 'Серый'), (79, 'Память', '256 ГБ'), (79, 'Оперативная память', '8 ГБ')],
    [(80, 'Цвет', 'Черный'), (80, 'Память', '256 ГБ'), (80, 'Оперативная память', '8 ГБ')],
    [(81, 'Цвет', 'Серебристый'), (81, 'Память', '256 ГБ'), (81, 'Оперативная память', '8 ГБ')],
    [(82, 'Цвет', 'Серый'), (82, 'Память', '256 ГБ'), (82, 'Оперативная память', '8 ГБ')],
    [(83, 'Цвет', 'Золотой'), (83, 'Память', '256 ГБ'), (83, 'Оперативная память', '8 ГБ')],
    [(84, 'Цвет', 'Серый'), (84, 'Память', '512 ГБ'), (84, 'Оперативная память', '16 ГБ')],
    [(85, 'Цвет', 'Серебристый'), (85, 'Память', '512 ГБ'), (85, 'Оперативная память', '16 ГБ')],
    [(86, 'Цвет', 'Серый'), (86, 'Память', '512 ГБ'), (86, 'Оперативная память', '16 ГБ')],
    [(87, 'Цвет', 'Серебристый'), (87, 'Память', '1 ТБ'), (87, 'Оперативная память', '16 ГБ')],
    [(88, 'Цвет', 'Серый'), (88, 'Память', '1 ТБ'), (89, 'Оперативная память', '16 ГБ')],
    [(89, 'Цвет', 'Серый'), (89, 'Память', '1 ТБ'), (89, 'Оперативная память', '16 ГБ')],
    [(90, 'Цвет', 'Черный'), (90, 'Память', '128 ГБ'), (90, 'Оперативная память', '8 ГБ')],
    [(91, 'Цвет', 'Синий'), (91, 'Камера', '108 МП'), (91, 'Экран', '6.7 дюймов')], 
    [(92, 'Цвет', 'Красный'), (92, 'Батарея', '5000 мАч'), (92, 'Зарядка', 'Быстрая зарядка')],
    [(93, 'Цвет', 'Серый'), (93, 'Память', '256 ГБ'), (93, 'Оперативная память', '12 ГБ')],
    [(94, 'Цвет', 'Белый'), (94, 'Камера', '50 МП'), (94, 'Экран', '6.4 дюймов')], 
    [(95, 'Цвет', 'Черный'), (95, 'Память', '512 ГБ'), (95, 'Оперативная память', '16 ГБ')],
    [(96, 'Цвет', 'Синий'), (96, 'Память', '128 ГБ'), (96, 'Оперативная память', '8 ГБ')],
    [(97, 'Цвет', 'Черный'), (97, 'Память', '128 ГБ'), (97, 'Оперативная память', '8 ГБ')],
    [(98, 'Цвет', 'Синий'), (98, 'Память', '256 ГБ'), (98, 'Оперативная память', '12 ГБ')],
    [(99, 'Цвет', 'Черный'), (99, 'Память', '128 ГБ'), (99, 'Оперативная память', '8 ГБ')],
    [(100, 'Цвет', 'Синий'), (100, 'Память', '256 ГБ'), (100, 'Оперативная память', '12 ГБ')],
    [(101, 'Цвет', 'Черный'), (101, 'Память', '128 ГБ'), (101, 'Оперативная память', '8 ГБ')], 
    [(102, 'Цвет', 'Серебристый'), (102, 'Память', '256 ГБ'), (102, 'Оперативная память', '12 ГБ')],
    [(103, 'Цвет', 'Серый'), (103, 'Память', '512 ГБ'), (103, 'Оперативная память', '16 ГБ')],
    [(104, 'Цвет', 'Черный'), (104, 'Размер', '41 мм'), (104, 'Аккумулятор', '18 часов')],
    [(105, 'Цвет', 'Черный'), (105, 'Размер', '44 мм'), (105, 'Аккумулятор', '20 часов')],
    [(106, 'Цвет', 'Черный'), (106, 'Размер', '46 мм'), (106, 'Аккумулятор', '14 дней')],
    [(107, 'Цвет', 'Черный'), (107, 'Материал', 'выф'), (107, 'Аккумулятор', '14 дней')],
    [(108, 'Цвет', 'Черный'), (108, 'Материал', 'вывы'), (108, 'Аккумулятор', '7 дней')],
    [(109, 'Цвет', 'Черный'), (109, 'Bluetooth', '5.3'), (109, 'Водонепроницаемость', 'IP67')],
    [(110, 'Цвет', 'Черный'), (110, 'Камера', '108 МП'), (110, 'Экран', '6.7 дюймов')],
    [(111, 'Цвет', 'Красный'), (111, 'Батарея', '5000 мАч'), (111, 'Зарядка', 'Быстрая зарядка')],
    [(112, 'Цвет', 'Серый'), (112, 'Память', '256 ГБ'), (112, 'Оперативная память', '12 ГБ')],
    [(113, 'Цвет', 'Белый'), (113, 'Камера', '50 МП'), (113, 'Экран', '6.4 дюймов')], 
    [(114, 'Цвет', 'Синий'), (114, 'Память', '128 ГБ'), (114, 'Оперативная память', '8 ГБ')], 
    [(115, 'Цвет', 'Белый'), (115, 'Память', '256 ГБ'), (115, 'Оперативная память', '12 ГБ')],
    [(116, 'Цвет', 'Белый'), (116, 'Камера', '50 МП'), (116, 'Экран', '6.4 дюймов')], 
    [(117, 'Цвет', 'Черный'), (117, 'Память', '512 ГБ'), (117, 'Оперативная память', '16 ГБ')],
    [(118, 'Цвет', 'Серый'), (118, 'Память', '256 ГБ'), (118, 'Оперативная память', '8 ГБ')],
    [(119, 'Цвет', 'Серый'), (119, 'Память', '256 ГБ'), (119, 'Оперативная память', '8 ГБ')],
]
    for char_list in characteristics:
        for product_id, name, value in char_list:
            cursor.execute("INSERT INTO product_characteristics (product_id, name, value) VALUES (?, ?, ?)", (product_id, name, value))

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_rating (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES product(id),
            FOREIGN KEY (user_id) REFERENCES users(id)); 
    """)

    db.commit()
    db.close()

create_tables()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error='Пользователь с таким именем или электронной почтой уже существует')
        finally:
            db.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin_password':
            session['logged_in'] = True
            session['username'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('admin_panel'))
        else:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            db.close()
            if user and user[2] == password:
                session['logged_in'] = True
                session['username'] = user[1]
                session['role'] = user[3]
                if user[3] == 'admin':
                    return redirect(url_for('admin_panel'))
                else:
                    return redirect(url_for('profile'))
            else:
                return 'Неверный логин или пароль.'
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM orders WHERE username=?", (username,))
        orders = cursor.fetchall()
        order_details = []
        for order in orders:
            cursor.execute("SELECT product.*, order_items.quantity FROM product INNER JOIN order_items ON product.id = order_items.product_id WHERE order_items.order_id=?", (order[0],))
            products = cursor.fetchall()
            order_details.append((order, products))
        all_products = cursor.fetchall()
        db.close()
        product_images = []
        for product in all_products:
            product_image = url_for('static', filename='' + product[2])
            product_images.append(product_image)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        categories_dict = []
        for category in categories:
            cursor.execute("SELECT * FROM subcategory WHERE category_id = ?", (category[0],))
            subcategories = cursor.fetchall()
            categories_dict.append({
                'id': category[0],
                'name': category[1],
                'subcategories': subcategories
            })
        db.close()
        return render_template('profile.html', user=user, order_details=order_details, all_products=all_products, product_images=product_images, categories=categories_dict)
    else:
        return redirect(url_for('login'))

@app.route('/checkout', methods=['POST'])
def checkout():
    if 'cart' in session:
        cart_items = session['cart']
        username = session.get('username', None)
        if username:
            db = get_db()
            cursor = db.cursor()
            try:
                if 'total_price' in session: 
                    cursor.execute("INSERT INTO orders (username, total_price) VALUES (?, ?)", (username, session['total_price']))
                    order_id = cursor.lastrowid
                    for code, item_data in cart_items.items():
                        cursor.execute("SELECT id FROM product WHERE code=?", (code,))
                        product_id = cursor.fetchone()
                        if product_id:
                            product_id = product_id[0]
                            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                                           (order_id, product_id, item_data['quantity'], item_data['price']))
                        else:
                            print(f"Продукт с кодом {code} не найден.")
                    db.commit()
                    db.close()
                    session.pop('cart', None)
                    session.pop('total_quantity', None)
                    session.pop('total_price', None)
                    return redirect(url_for('profile'))
                else:
                    return "Ошибка: Общая цена не установлена", 500
            except Exception as e:
                db.rollback()
                db.close()
                print(f"Ошибка при оформлении заказа: {e}")
                return "Произошла ошибка при оформлении заказа", 500
        else:
            return 'Необходимо авторизоваться!'
    else:
        return 'Ваша корзина пуста!'

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'logged_in' in session and session['logged_in']:
        username = session['username']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        db.close()
        if user:
            if request.method == 'POST':
                new_email = request.form['email']
                new_profile_picture = request.files.get('profile_picture')

                db = get_db()
                cursor = db.cursor()
                try:
                    if new_profile_picture:
                        new_profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{username}.jpg'))
                        cursor.execute("UPDATE users SET email=?, profile_picture=? WHERE username=?", 
                                       (new_email, f'/profile_pictures/{username}.jpg', username))
                    else:
                        cursor.execute("UPDATE users SET email=? WHERE username=?", (new_email, username))
                        db.commit()
                    db.close()
                    return redirect(url_for('profile'))
                except sqlite3.IntegrityError:
                    db.close()
                    return render_template('edit_profile.html', user=user, error='Электронная почта уже используется')
                finally:
                    db.close()
            db.close()
            return render_template('edit_profile.html', user=user)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/add', methods=['POST'])
def add_product_to_cart():
    try:
        if request.method == 'POST':
            _quantity = int(request.form.get('quantity', 0))
            _code = request.form['code']
            subcategory_id = int(request.form.get('subcategory_id', 0))

            if _quantity and _code:
                db = get_db()
                cursor = db.cursor()
                cursor.execute("SELECT * FROM product WHERE code=?", (_code,))
                row = cursor.fetchone()
                if row:
                    itemArray = {
                        _code: {
                            'name': row[1],
                            'code': row[2],
                            'quantity': _quantity,
                            'price': float(row[4]),
                            'image': row[3],
                            'total_price': _quantity * float(row[4])
                        }
                    }

                    if 'cart' in session:
                        cart_items = session['cart']
                        if _code in cart_items:
                            cart_items[_code]['quantity'] += _quantity
                            cart_items[_code]['total_price'] = cart_items[_code]['quantity'] * float(row[4])
                        else:
                            cart_items.update(itemArray)
                    else:
                        cart_items = itemArray

                    session['cart'] = cart_items
                    total_quantity = sum(item['quantity'] for item in cart_items.values())
                    total_price = sum(item['total_price'] for item in cart_items.values())
                    session['total_quantity'] = total_quantity
                    session['total_price'] = total_price

                    db.close()
                    return redirect(url_for('product_detail', product_id=row[0]))
                else:
                    db.close()
                    return 'Product not found'
            else:
                return 'Error while adding item to cart'
    except ValueError as e:
        print(f"Ошибка при преобразовании данных: {e}")
        return 'Некорректные данные', 400
    except Exception as e:
        print(f"Ошибка: {e}")
        return 'An error occurred', 500
    finally:
        pass 
    
@app.route('/')
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    categories_dict = []
    for category in categories:
        cursor.execute("SELECT * FROM subcategory WHERE category_id = ?", (category[0],))
        subcategories = cursor.fetchall()
        categories_dict.append({
            'id': category[0],
            'name': category[1],
            'subcategories': subcategories
        })
    db.close()
    return render_template('index.html', categories=categories_dict)

@app.route('/get_products')
def get_products():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    product_list = []
    for product in products:
        product_list.append({
            'id': product[0],  
            'name': product[1],
            'image': product[3],
            'price': product[4],
            'subcategory_id': product[5]
        })
    
    return jsonify(product_list)

@app.route('/products/<int:subcategory_id>')
def products(subcategory_id):
    selected_characteristics = request.args.getlist('characteristic')
    selected_colors = request.args.getlist('color')
    selected_price_ranges = request.args.getlist('price_range')
    sort_by = request.args.get('sort')
    db = get_db()
    cursor = db.cursor()
    products_query = """SELECT p.id, p.name, p.code, p.image, p.price, p.rating, p.num_ratings FROM product p JOIN subcategory s ON p.subcategory_id = s.id WHERE s.id = ?"""
    if selected_characteristics:
        products_query += " AND p.id IN (SELECT product_id FROM product_characteristics WHERE name IN ({})".format(",".join(["'{}'".format(c) for c in selected_characteristics])) + ")"
    if selected_price_ranges:
        products_query += " AND p.price BETWEEN {} AND {}".format(selected_price_ranges[0].split('-')[0], selected_price_ranges[0].split('-')[1])
    if selected_colors:
        products_query += " AND p.id IN (SELECT product_id FROM product_characteristics WHERE name = 'Цвет' AND value IN ({})".format(",".join(["'{}'".format(c) for c in selected_colors])) + ")"
    if sort_by == "price_asc":
        products_query += " ORDER BY p.price ASC"
    elif sort_by == "price_desc":
        products_query += " ORDER BY p.price DESC"
    elif sort_by == "rating_desc":
        products_query += " ORDER BY p.rating DESC"
    cursor.execute(products_query, (subcategory_id,))
    products = cursor.fetchall()
    product_dicts = [dict(zip([column[0] for column in cursor.description], row)) for row in products]
    characteristics = {}
    cursor.execute("SELECT DISTINCT name FROM product_characteristics")
    characteristic_names = cursor.fetchall()
    for name in characteristic_names:
        cursor.execute(f"SELECT DISTINCT value FROM product_characteristics WHERE name = '{name[0]}'")
        characteristics[name[0]] = [row[0] for row in cursor.fetchall()]
    cursor.execute("""SELECT DISTINCT price FROM product ORDER BY price""")
    prices = cursor.fetchall()
    price_ranges = []
    for i in range(0, len(prices), 2):
        if i + 1 < len(prices):
            price_ranges.append(f"{prices[i][0]}-{prices[i+1][0]}")
        else:
            price_ranges.append(f"{prices[i][0]}-")
    cursor.execute("SELECT DISTINCT value FROM product_characteristics WHERE name = 'Цвет' ORDER BY value")
    colors = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    categories_dict = []
    for category in categories:
        cursor.execute("SELECT * FROM subcategory WHERE category_id = ?", (category[0],))
        subcategories = cursor.fetchall()
        categories_dict.append({
            'id': category[0],
            'name': category[1],
            'subcategories': subcategories
        })
    db.close()
    return render_template( 'products.html',products=product_dicts,characteristics_names=characteristic_names,characteristics=characteristics,selected_characteristics=selected_characteristics,selected_price_ranges=selected_price_ranges,selected_colors=selected_colors,sort_by=sort_by,subcategory_id=subcategory_id,categories=categories_dict, price_ranges=price_ranges,colors=colors,)

@app.route('/category/<int:category_id>')
def category_detail(category_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name FROM category WHERE id = ?", (category_id,))
    category_name = cursor.fetchone()[0]
    cursor.execute("SELECT id, name FROM subcategory WHERE category_id = ?", (category_id,))
    subcategories = cursor.fetchall()
    subcategories = [dict(zip(('id', 'name'), subcategory)) for subcategory in subcategories]
    db.close()
    return render_template('category_detail.html', category_name=category_name, subcategories=subcategories)

@app.route('/subcategory/<int:subcategory_id>')
def subcategory_detail(subcategory_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""SELECT s.name AS subcategory_name, p.id, p.name, p.code, p.image, p.price FROM product p JOIN subcategory s ON p.subcategory_id = s.id WHERE s.id = ?""", (subcategory_id,))
    products = cursor.fetchall()
    products = [dict(zip(('subcategory_name', 'id', 'name', 'code', 'image', 'price'), product)) for product in products]
    db.close()
    if products:
        subcategory_name = products[0]['subcategory_name']
        return render_template('subcategory_detail.html', products=products, subcategory_name=subcategory_name)
    else:
        return render_template('subcategory_detail.html', message="В этой подкатегории нет товаров")

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        if not product:
            return 'Товар не найден', 404
        cursor.execute("SELECT name, value FROM product_characteristics WHERE product_id = ?", (product_id,))
        characteristics = cursor.fetchall()
        characteristics_dict = {}
        for name, value in characteristics:
            characteristics_dict[name] = value
        cursor.execute("SELECT AVG(rating), COUNT(*) FROM product_rating WHERE product_id = ?", (product_id,))
        average_rating, rating_count = cursor.fetchone()
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        categories_dict = []
        for category in categories:
            cursor.execute("SELECT * FROM subcategory WHERE category_id = ?", (category[0],))
            subcategories = cursor.fetchall()
            categories_dict.append({
                'id': category[0],
                'name': category[1],
                'subcategories': subcategories
            })
        db.close()
        return render_template('product_detail.html', product=product, characteristics=characteristics_dict, average_rating=average_rating, rating_count=rating_count, categories=categories_dict)
    except Exception as e:
        print(e)
        return "Произошла ошибка при загрузке информации о товаре"
    finally:
        pass

@app.route('/search')
def search():
    query = request.args.get('query')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM product WHERE name LIKE ?", ('%' + query + '%',))
    results = [
        {'id': row[0], 'name': row[1]}
        for row in cursor.fetchall()
    ]
    return jsonify(results) 
                        
@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    total_quantity = 0
    total_price = 0.0
    for code, item_data in cart_items.copy().items(): 
        total_quantity += item_data['quantity']
        try:
            total_price += item_data['quantity'] * float(item_data['price']) 
        except ValueError:
            print(f"Ошибка: Некорректная цена для товара с кодом {code}") 
            del cart_items[code]
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM category")
    categories = cursor.fetchall()
    categories_dict = []
    for category in categories:
        cursor.execute("SELECT * FROM subcategory WHERE category_id = ?", (category[0],))
        subcategories = cursor.fetchall()
        categories_dict.append({
            'id': category[0],
            'name': category[1],
            'subcategories': subcategories
        })
    db.close() 
    session['cart'] = cart_items  
    return render_template('cart.html', cart_items=cart_items, total_quantity=total_quantity, total_price=total_price, categories=categories_dict)

@app.route('/empty')
def empty_cart():
    try:
        session.pop('cart', None) 
        return redirect(url_for('products', subcategory_id=1))
    except Exception as e:
        print(e)
        return "Ошибка при очистке корзины", 500

@app.route('/delete_product/<code>', methods=['GET', 'POST'])
def delete_product(code):
    try:
        total_price = 0
        total_quantity = 0
        session.modified = True

        if 'cart_item' in session and code in session['cart_item']:
            session['cart_item'].pop(code, None)

            if 'cart_item' in session:
                for key, value in session['cart_item'].items():
                    total_quantity += int(value['quantity'])
                    total_price += float(value['total_price'])

        if total_quantity == 0:
            session.clear()
        else:
            session['total_quantity'] = total_quantity
            session['total_price'] = total_price

        return redirect(url_for('.cart')) 
    except Exception as e:
        print(e)

def login_required(role='admin'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'logged_in' in session and session['logged_in']:
                if session['role'] == role:
                    return func(*args, **kwargs)
                else:
                    return 'У вас нет прав доступа к этой странице.'
            else:
                return redirect(url_for('login'))
        return wrapper
    return decorator

@app.route('/admin_panel')
@login_required(role='admin') 
def admin_panel():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM product")
        products = cursor.fetchall()
        products = [dict(zip([column[0] for column in cursor.description], row)) for row in products]
        db.close()
        return render_template('admin_panel.html', products=products)
    except Exception as e:
        app.logger.error(f'Ошибка при получении списка продуктов: {e}')
        return 'Произошла ошибка при получении списка продуктов.', 500

@app.route('/admin/add_product', methods=['GET', 'POST'])
@login_required(role='admin')
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        price = request.form['price']
        subcategory_id = request.form['subcategory_id']
        image_file = request.files.get('image')

        if image_file and image_file.filename != '':
            image_filename = image_file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
        else:
            return 'Ошибка: Загрузите изображение.'

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO product (name, code, image, price, subcategory_id) VALUES (?, ?, ?, ?, ?)",
                           (name, code, image_filename, price, subcategory_id))
            db.commit()
            product_id = cursor.lastrowid
            characteristics = request.form.getlist('characteristic_name')
            values = request.form.getlist('characteristic_value')
            for i in range(len(characteristics)):
                if characteristics[i] and values[i]:
                    cursor.execute("INSERT INTO product_characteristics (product_id, name, value) VALUES (?, ?, ?)",
                                   (product_id, characteristics[i], values[i]))
            db.commit()
            db.close()
            flash('Товар добавлен успешно!', 'success')
            return redirect(url_for('admin_panel'))
        except sqlite3.IntegrityError:
            db.close()
            return render_template('add_product.html', error='Товар с таким кодом уже существует', subcategories=get_subcategories())
    return render_template('add_product.html', subcategories=get_subcategories())

def get_subcategories():
    """Получает список подкатегорий для формы добавления товара."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM subcategory")
    subcategories = cursor.fetchall()
    subcategories = [dict(zip(('id', 'name'), subcategory)) for subcategory in subcategories]
    db.close()
    return subcategories
    
@app.route('/admin/edit_product/<int:product_id>')
def edit_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM product WHERE id=?", (product_id,))
            product = cursor.fetchone()
            if product:
                product = dict(zip([column[0] for column in cursor.description], product))
                db.close()
                return render_template('edit_product.html', product=product)
            else:
                db.close()
                return 'Товар не найден.'
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/edit_product/<int:product_id>', methods=['POST'])
def update_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            name = request.form['name']
            code = request.form['code']
            price = request.form['price']
            image_file = request.files.get('image')

            db = get_db()
            cursor = db.cursor()

            if image_file and image_file.filename != '':
                image_filename = image_file.filename
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_path)
                cursor.execute("UPDATE product SET name=?, code=?, image=?, price=? WHERE id=?",
                               (name, code, image_filename, price, product_id))
            else:
                cursor.execute("UPDATE product SET name=?, code=?, price=? WHERE id=?",
                               (name, code, price, product_id))

            db.commit()
            db.close()
            flash('Товар изменен успешно!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/delet_product/<int:product_id>')
def delet_product(product_id):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute("DELETE FROM product WHERE id=?", (product_id,))
                db.commit()
                db.close()
                flash('Товар удален успешно!', 'success')
                return redirect(url_for('admin_panel'))
            except Exception as e:
                print(e)
                db.close()
                flash('Ошибка удаления товара', 'error')
                return redirect(url_for('admin_panel'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/orders', methods=['GET'])
def admin_orders():
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM orders")
            orders = cursor.fetchall()
            orders = [dict(zip([column[0] for column in cursor.description], row)) for row in orders]
            db.close()
            return render_template('admin_orders.html', orders=orders)
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))

@app.route('/admin/order/<int:order_id>/<string:action>', methods=['POST'])
def handle_order(order_id, action):
    if 'logged_in' in session and session['logged_in']:
        if session['username'] == 'admin':
            db = get_db()
            cursor = db.cursor()

            if action == 'accept':
                cursor.execute("UPDATE orders SET status='Принят' WHERE id=?", (order_id,))
                db.commit()
                db.close()
                flash('Заказ принят в работу!', 'success')
            elif action == 'reject':
                cursor.execute("UPDATE orders SET status='Отклонен' WHERE id=?", (order_id,))
                db.commit()
                db.close()
                flash('Заказ отклонен!', 'success')
            elif action == 'complete':
                cursor.execute("UPDATE orders SET status='Завершен' WHERE id=?", (order_id,))
                db.commit()
                db.close()
                flash('Заказ завершен!', 'success')
            else:
                db.close()
                flash('Некорректное действие.', 'error')
            return redirect(url_for('admin_orders'))
        else:
            return 'У вас нет прав доступа к административной панели.'
    else:
        return redirect(url_for('login'))
if __name__ == "__main__":
    app.run(debug=True)