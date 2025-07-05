
import telebot
import random
import time
import threading
import json
import os

TOKEN = '7102389575:AAHMc_209ElVL5Qlv7-bLhCkMIiVD9T8Obw'
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

sponsor_channels = [
    '@Vsi_PROMO',
    '@uaclub_casinoman'
]

ADMIN_ID = 7262164512
DATA_FILE = 'users_data.json'

# Жарти для фарт-картки
jokes = [
    "Фарт постукав — не прикидайся, що тебе немає вдома.",
    "Краще один раз пощастити, ніж сто разів пошкодувати.",
    "Фарт — це коли за тебе грають навіть ліхтарі на вулиці.",
    "Якщо не пощастило, почекай – скоро повезе!",
]

# Завантаження даних
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        users_data = json.load(f)
        users_data = {int(k): v for k, v in users_data.items()}
else:
    users_data = {}

def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump({str(k): v for k, v in users_data.items()}, f, indent=4)

# Клавіатура з кнопками
main_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.row('🎁 Щоденний фарт', '🃏 Фарт-картка')
main_keyboard.row('🏆 Розіграші', '👯 Запросити друга')
main_keyboard.row('📊 Мій профіль', '📢 Спонсори / Новини')
main_keyboard.row('⭐️ Топ 5 гравців', '🎟 Промокод')
main_keyboard.row('📣 Додати свій канал у Jackpot Pulse')

# Клавіатура для балансу та виведення
balance_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
balance_keyboard.row('📊 Баланс', '💸 Вивести')

# Промокоди
promocodes = {
    'nt7v-wz1y-tjbz-j15a': {'value': 45, 'activations': 30},
    'u0pp-rrga-9q5g-ewv5': {'value': 35, 'activations': 30},
    'd7gg-tmgl-2mhv-3s5t': {'value': 25, 'activations': 30},
    't6cz-xuk8-nhao-ejs6': {'value': 25, 'activations': 30},
    'qpwr-ckpw-iqnk-eo47': {'value': 20, 'activations': 30},
    'q3pf-xgb6-9owd-6vjt': {'value': 15, 'activations': 30},
    'nnf1-56z3-urzx-ocq3': {'value': 20, 'activations': 30},
    '1gpw-gvvh-n8ty-g4ds': {'value': 20, 'activations': 30},
    'cxae-68zk-3cs0-lyte': {'value': 15, 'activations': 30},
    '62j1-6zsh-j5i6-s8k7': {'value': 15, 'activations': 30},
    '74c2-eu9v-in1u-rtgh': {'value': 30, 'activations': 30},
    '8ttb-r3km-m0ol-lk7k': {'value': 25, 'activations': 30},
    'dygo-l42j-d6bj-5b38': {'value': 20, 'activations': 30},
    '9gt8-2zvl-tx3v-dsei': {'value': 25, 'activations': 30},
    'bipg-jvs8-n4qj-ppkk': {'value': 20, 'activations': 30},
    'ig2j-inlo-qbzw-o78i': {'value': 25, 'activations': 30},
    'spbx-ldu7-x9om-wfmb': {'value': 25, 'activations': 30},
    '4ocs-s1ig-164x-qyvk': {'value': 25, 'activations': 30},
    'mvod-y9tk-s2xf-uul9': {'value': 15, 'activations': 30},
    'bgcj-5duz-1iev-eqdh': {'value': 15, 'activations': 30},
    '0fiz-wki6-txmt-oppv': {'value': 15, 'activations': 30},
    'y9wg-xsr7-hhmz-i0bd': {'value': 30, 'activations': 30},
    '3hu6-s0de-8ona-xq81': {'value': 30, 'activations': 30},
    'fchg-t8a5-bqno-lksz': {'value': 20, 'activations': 30},
    'ox35-9qtm-c4qq-vkv5': {'value': 20, 'activations': 30},
    '1the-1rf8-aawk-6n4y': {'value': 20, 'activations': 30},
    'xqd7-clb4-9n49-zbyn': {'value': 30, 'activations': 30},
    '0mlm-tnix-wsqa-s10y': {'value': 15, 'activations': 30},
    'nl84-0s7e-c0ad-smuj': {'value': 15, 'activations': 30},
    'c4b8-sk3y-giw1-t6bq': {'value': 25, 'activations': 30},
    'tmym-xrl3-ztdh-kps4': {'value': 15, 'activations': 30},
    'suxe-i3cz-an5l-tbyo': {'value': 30, 'activations': 30},
    'tgt3-znkg-9mnr-ht08': {'value': 15, 'activations': 30},
    '7usj-k7zt-f4un-9ghp': {'value': 25, 'activations': 30},
    'y1qd-lua7-hkqt-ql11': {'value': 30, 'activations': 30},
    'cmd7-k6cw-7a1y-o0dm': {'value': 15, 'activations': 30},
    '3ipx-yrmk-wkd3-fvyk': {'value': 30, 'activations': 30},
    'z174-k22u-soyy-cwyv': {'value': 30, 'activations': 30},
    'mu3e-<OutputTruncated>': {'value': 30, 'activations': 30},
    'isus-lx3b-vzv3-efib': {'value': 20, 'activations': 30},
    '3dkf-edm2-iyiq-1vxw': {'value': 20, 'activations': 30},
    's9g1-63ly-7oen-ftio': {'value': 25, 'activations': 30},
    'y52l-cwkz-1j64-rt47': {'value': 30, 'activations': 30},
    '93kl-2kvd-w6y5-bqmr': {'value': 30, 'activations': 30},
    '3syo-akh4-kq0m-egoc': {'value': 25, 'activations': 30},
    'r9qc-af7d-85cg-w397': {'value': 15, 'activations': 30},
    'q6fz-g4af-ywd5-jvnk': {'value': 25, 'activations': 30},
    'zz8h-7bmx-ke5y-a7k9': {'value': 15, 'activations': 30},
    'zeca-579k-l1b9-xotr': {'value': 20, 'activations': 30},
    'ejtu-ezos-i4sh-87fr': {'value': 25, 'activations': 30},
    'nt65-mglo-85gl-s72x': {'value': 30, 'activations': 30},
    'yii9-i4ck-bc4x-l5l8': {'value': 20, 'activations': 30},
    'f07a-4jvz-cmcb-yql9': {'value': 25, 'activations': 30},
    '2jw1-jv1n-a4bo-qey5': {'value': 25, 'activations': 30},
    'jifb-9rii-u5uz-9vly': {'value': 25, 'activations': 30},
    'c7jg-50wo-xrtu-3ca2': {'value': 20, 'activations': 30},
    'w6x4-5fz7-ktrt-xcd5': {'value': 15, 'activations': 30},
    '8l5a-2cxv-6388-l558': {'value': 30, 'activations': 30},
    'istt-hpw7-ycir-ccl1': {'value': 30, 'activations': 30},
    'jmln-yb5s-iv5f-d4w8': {'value': 15, 'activations': 30},
    '8kvm-fmxe-dzny-7odw': {'value': 20, 'activations': 30},
    'teuc-9hbs-m1gl-xm7w': {'value': 25, 'activations': 30},
    'h4mu-oxv1-cz2h-xssl': {'value': 25, 'activations': 30},
    'qj97-bu0x-coel-byq8': {'value': 20, 'activations': 30},
    'pijd-j2vy-chbw-as0i': {'value': 25, 'activations': 30},
    'tid5-eii7-25iy-ez7e': {'value': 25, 'activations': 30},
    'wp6i-i28p-04ms-iyi6': {'value': 15, 'activations': 30},
    '1ouy-qm11-rn38-0sac': {'value': 30, 'activations': 30},
    'li2c-dt2d-z14m-9t4g': {'value': 30, 'activations': 30},
    '36p9-6dcg-ang4-5skc': {'value': 15, 'activations': 30},
    'kfzn-wm3q-wdan-yzoe': {'value': 20, 'activations': 30},
    'pmag-pk04-y0nh-qsms': {'value': 15, 'activations': 30},
    'n4xr-7pyj-4bxi-ofbt': {'value': 30, 'activations': 30},
    'c7gk-gajj-orq6-8w2j': {'value': 20, 'activations': 30}
}
