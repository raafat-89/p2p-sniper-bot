# ?? P2P Crypto Alert Bot

A Telegram bot that monitors Binance P2P ads for large discounts on selected crypto/fiat pairs and sends instant alerts when deals are detected.

---

## ✅ Features

- Monitors real-time Binance P2P ads.
- Sends Telegram alerts when:
  - Discount ≥ 5% from market price
  - Ad age < 60 seconds
- Simple setup using Python and `requests`
- Easy to extend (add new platforms, coins, filters, etc.)

---

## ⚙️ Installation

### 1. Connect to your VPS and clone the repo:

```bash
cd /root
git clone https://github.com/raafat-89/p2p-sniper-bot.git
cd p2p-sniper-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/bot.pycat >> README.md << 'EOF'

---

## ✉️ Example Alert (Telegram)
cat >> README.md << 'EOF'

---

## ✉️ Example Alert (Telegram)
---

## ?? To-do / Suggestions

- [ ] Auto-start bot on reboot using `tmux` or `systemd`
- [ ] Add support for Bybit, KuCoin P2P
- [ ] Create a config file (e.g. `config.py`)
- [ ] Improve message formatting

---

## ?? License

MIT License
