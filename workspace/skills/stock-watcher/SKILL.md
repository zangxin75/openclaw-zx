---
name: stock-watcher
description: |
  Manage and monitor a personal stock watchlist with support for adding, removing, listing stocks, and summarizing their recent performance using data from 10jqka.com.cn. Works with Chinese A-shares.
---

# Stock Watcher

Manage and monitor a personal stock watchlist for Chinese A-shares.

## Features

- ✅ **Add stocks** to watchlist using 6-digit stock codes
- ✅ **View watchlist** with clear formatting
- ✅ **Remove individual stocks** from watchlist
- ✅ **Clear entire watchlist** with one command
- ✅ **Get performance summary** for all watched stocks

## Installation

The skill will be automatically installed when first used. Creates:

- Standardized watchlist directory: `~/.clawdbot/stock_watcher/`
- Watchlist file: `~/.clawdbot/stock_watcher/watchlist.txt`

## Usage Commands

### Add a stock
```bash
cd ~/.clawdbot/skills/stock-watcher/scripts && python3 add_stock.py 600053
```

### View watchlist
```bash
cd ~/.clawdbot/skills/stock-watcher/scripts && python3 list_stocks.py
```

### Remove a stock
```bash
cd ~/.clawdbot/skills/stock-watcher/scripts && python3 remove_stock.py 600053
```

### Clear watchlist
```bash
cd ~/.clawdbot/skills/stock-watcher/scripts && python3 clear_watchlist.py
```

### Get performance summary
```bash
cd ~/.clawdbot/skills/stock-watcher/scripts && python3 summarize_performance.py
```

## Data Source

- **Primary source**: 同花顺 (10jqka.com.cn)
- **Stock pages**: `https://stockpage.10jqka.com.cn/{stock_code}/`
- **Supported markets**: Shanghai A-shares, Shenzhen A-shares, STAR Market

## Storage Location

All user data is stored in a single, standardized location:
- **Directory**: `~/.clawdbot/stock_watcher/`
- **Watchlist file**: `~/.clawdbot/stock_watcher/watchlist.txt`

## Troubleshooting

### "Command not found" errors
Ensure you have Python 3 and required packages installed:
```bash
pip3 install requests beautifulsoup4
```

### Network issues
The skill fetches data from 10jqka.com.cn. Ensure you have internet access.
