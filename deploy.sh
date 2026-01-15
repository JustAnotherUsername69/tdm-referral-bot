#!/bin/bash
cd /home/ubuntu/tdm-referral-bot || exit 1
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl daemon-reload
sudo systemctl restart tdm-bot
sudo systemctl restart tdm-worker
