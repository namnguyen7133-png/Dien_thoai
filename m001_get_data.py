name: Daily Result Checker

on:
  schedule:
    # Chạy vào 14:30 UTC hàng ngày (tức 21:30 giờ Việt Nam)
    - cron: '30 14 * * *'
  workflow_dispatch: # Cho phép bấm chạy thủ công để test

jobs:
  run-automation:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Execute Relay Chain M001
        run: python m001_get_data.py

      - name: Send Notification
        # Bước này có thể kết hợp với Pushbullet hoặc Telegram API
        # Dưới đây là ví dụ gửi qua Telegram nếu bạn có Bot Token
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: |
          if [ -f ket_qua_temp.txt ]; then
            MESSAGE=$(cat ket_qua_temp.txt)
            curl -s -X POST https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage \
              -d chat_id=$CHAT_ID \
              -d text="$MESSAGE"
          fi
