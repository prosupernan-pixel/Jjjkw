# PRD — AI SMC Scalping Bot M5 (Inducement + BOS + OB)

## Versi Struktur Sesuai Referensi Gambar

---

# 1. Product Overview

## Nama Produk

SMC Liquidity Scalping Bot

## Deskripsi

Bot trading otomatis berbasis Smart Money Concept (SMC) untuk timeframe M5 dengan fokus pada:

* Market Structure
* Inducement (IDM)
* BOS (Break of Structure)
* Order Block (OB)
* Fibonacci Retracement 50%
* Supply & Demand Zone

Bot dirancang untuk meniru pola entry trader SMC manual seperti pada referensi struktur gambar.

---

# 2. Core Trading Concept

Strategi utama:

> Harga menciptakan inducement terlebih dahulu → melakukan BOS → retrace ke OB/Fibo 50% → entry mengikuti trend utama.

Bot wajib memahami urutan struktur market.

---

# 3. Struktur Utama SMC

## Komponen Struktur

| Komponen         | Fungsi                   |
| ---------------- | ------------------------ |
| Trend            | Menentukan arah market   |
| IDM (Inducement) | Liquidity trap           |
| BOS              | Konfirmasi struktur      |
| OB (Order Block) | Area entry               |
| Supply/Demand    | Zona reaksi market       |
| Fibonacci 50%    | Area retracement optimal |

---

# 4. Market Structure Logic

---

## 4.1 Bullish Structure

Urutan:

```text
Higher Low
↓
Inducement Sweep
↓
BOS Bullish
↓
Retrace ke OB / Fibo 50%
↓
BUY
```

---

## 4.2 Bearish Structure

Urutan:

```text
Lower High
↓
Inducement Sweep
↓
BOS Bearish
↓
Retrace ke OB / Fibo 50%
↓
SELL
```

---

# 5. Trend Detection Engine

## Bullish Trend

Syarat:

* Higher High (HH)
* Higher Low (HL)

## Bearish Trend

Syarat:

* Lower High (LH)
* Lower Low (LL)

---

# 6. IDM (Inducement) Detection

## Definisi

Inducement adalah gerakan market yang memancing trader masuk sebelum arah utama terjadi.

Biasanya:

* Sweep liquidity
* Fake breakout
* Break kecil pada pullback

---

## Rules IDM Bullish

Bot mencari:

* Low kecil di bawah pullback
* Candle sweep wick
* Rejection kuat

---

## Rules IDM Bearish

Bot mencari:

* High kecil di atas pullback
* Fake breakout atas
* Rejection bearish

---

# 7. BOS (Break of Structure)

## Valid BOS

BOS dianggap valid jika:

* Candle close penuh melewati struktur
* Body candle dominan
* Momentum tinggi
* Volume meningkat

---

## BOS Bullish

Harga break:

* Swing High terakhir

---

## BOS Bearish

Harga break:

* Swing Low terakhir

---

# 8. Order Block (OB)

## Definisi

Candle terakhir sebelum impuls BOS.

---

## Bullish OB

* Candle bearish terakhir sebelum impuls naik

## Bearish OB

* Candle bullish terakhir sebelum impuls turun

---

## Rules Valid OB

OB valid jika:

* Menyebabkan BOS
* Volume tinggi
* Belum mitigation penuh
* Dekat Fibo 50%

---

# 9. Fibonacci Confirmation

## Level Utama

Bot menggunakan:

* 50%
* 61.8%

---

## Logic

Setelah BOS:

* Tarik fibo dari swing high-low
* Tunggu retracement ke area optimal

---

# 10. Supply & Demand Zone

## Supply Zone

Area seller dominan.

## Demand Zone

Area buyer dominan.

---

## Rules

Zona valid jika:

* Ada impuls kuat keluar zona
* Ada BOS setelah zona
* Reaksi market sebelumnya jelas

---

# 11. Entry Strategy

---

## SELL Setup

### Syarat

1. Trend bearish
2. IDM terbentuk
3. BOS bearish valid
4. Retrace ke:

   * Bearish OB
   * Fibo 50%
   * Supply zone
5. Rejection candle muncul

---

## Eksekusi SELL

Bot:

* Open sell
* SL di atas OB
* TP pada low berikutnya
* RR minimal 1:1.5

---

## BUY Setup

### Syarat

1. Trend bullish
2. IDM terbentuk
3. BOS bullish valid
4. Retrace ke:

   * Bullish OB
   * Fibo 50%
   * Demand zone
5. Rejection candle muncul

---

## Eksekusi BUY

Bot:

* Open buy
* SL di bawah OB
* TP pada high berikutnya
* RR minimal 1:1.5

---

# 12. Candle Confirmation

## Confirmation Candle

Bot mencari:

* Pinbar
* Engulfing
* Strong rejection
* Momentum candle

---

# 13. AI Confirmation Layer

AI menilai probabilitas setup berdasarkan:

| Faktor         | Bobot |
| -------------- | ----- |
| BOS strength   | 25%   |
| IDM quality    | 20%   |
| OB reaction    | 20%   |
| Volume         | 15%   |
| Trend momentum | 20%   |

---

## AI Score

| Score | Action       |
| ----- | ------------ |
| 85+   | Strong Entry |
| 70-84 | Medium Entry |
| <70   | Skip         |

---

# 14. Risk Management

## Default Risk

* 1% per trade

---

## Max Drawdown

* 5% harian

---

## Max Consecutive Loss

* 3x loss

---

## Position Rule

* 1 posisi per pair

---

# 15. Stop Loss Logic

## SELL

SL:

* Di atas OB
* Atau di atas inducement high

---

## BUY

SL:

* Di bawah OB
* Atau di bawah inducement low

---

# 16. Take Profit Logic

## TP Methods

### Conservative

RR 1:1.5

### Normal

RR 1:2

### Aggressive

Liquidity berikutnya

---

# 17. Trade Management

## Optional Features

### Break Even

Saat RR 1:1 tercapai

### Trailing Stop

Mengikuti structure baru

### Partial TP

50% close di RR 1:1

---

# 18. Multi Filter System

Bot menghindari entry saat:

* Spread tinggi
* News besar
* Sideways
* Volatilitas rendah
* Session sepi

---

# 19. Session Filter

## Session Prioritas

✅ London
✅ New York
✅ London-New York Overlap

---

# 20. Dashboard Features

## Dashboard Menampilkan

* Market trend
* BOS terbaru
* IDM aktif
* OB zone
* AI score
* Active trades
* Winrate
* Daily PnL

---

# 21. Telegram Notification

## Contoh

```text
SELL USDCHF

Trend: Bearish
BOS: Confirmed
IDM: Valid
OB Retest: YES
AI Score: 89

Entry: 0.89250
SL: 0.89380
TP: 0.88950
RR: 1:2
```

---

# 22. Technical Stack

## Backend

Python

## Trading API

* MetaTrader5
* Binance API

## AI Engine

* TensorFlow
* Scikit-learn

## Database

PostgreSQL

## Dashboard

Next.js

---

# 23. Bot Workflow

```text
Ambil Candle M5
↓
Deteksi Trend
↓
Cari IDM
↓
Cari BOS
↓
Identifikasi OB
↓
Hitung Fibo 50%
↓
Tunggu Retest
↓
Confirmation Candle
↓
AI Validation
↓
Open Trade
↓
Manage Position
```

---

# 24. Pseudocode Logic

```python
IF trend == bearish:

    detect_idm()

    IF bos_bearish:

        mark_order_block()

        wait_retracement()

        IF price_reach_ob AND fibo_50:

            IF rejection_candle:

                execute_sell()

ELSE IF trend == bullish:

    detect_idm()

    IF bos_bullish:

        mark_order_block()

        wait_retracement()

        IF price_reach_ob AND fibo_50:

            IF rejection_candle:

                execute_buy()
```

---

# 25. Backtesting Requirements

Bot harus support:

* MT5 historical data
* Winrate analysis
* RR analysis
* Drawdown analysis
* Session analysis
* Pair analysis

---

# 26. KPI Target

| Metric          | Target   |
| --------------- | -------- |
| Winrate         | >65%     |
| RR Minimum      | 1:1.5    |
| Max DD          | <10%     |
| Avg Entry Delay | <1 detik |

---

# 27. Future Upgrade

## V2

* Fair Value Gap (FVG)
* Liquidity Heatmap
* Multi Timeframe Bias
* Smart Session Detection
* Auto News Avoidance
* Deep Learning Prediction

---

# 28. Final Goal

Bot harus mampu:

✅ Membaca market structure otomatis
✅ Menentukan inducement secara akurat
✅ Mendeteksi BOS valid
✅ Menandai OB berkualitas
✅ Entry presisi pada retracement
✅ Menghindari fake breakout
✅ Scalping cepat dan disiplin di M5
