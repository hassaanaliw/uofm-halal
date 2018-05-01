#!/usr/bin/env bash
# If the error is caused by something besides the directory already existing

python3 -c "from uofm_dining_hall_api import menu_scraper; menu_scraper.weekly_download();"
