#!/bin/bash
# extract_notifications.sh
# Script to extract Telegram notifications from Windows Push Notification Database
# Usage: ./extract_notifications.sh <path_to_wpndatabase.db>

if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_wpndatabase.db>"
    echo "Example: $0 '/path/to/Users/username/AppData/Local/Microsoft/Windows/Notifications/wpndatabase.db'"
    exit 1
fi

WPNDB="$1"

if [ ! -f "$WPNDB" ]; then
    echo "Error: Database file not found: $WPNDB"
    exit 1
fi

echo "=============================================="
echo "Windows Push Notification Database Extractor"
echo "=============================================="
echo ""

echo "[*] Listing notification handlers..."
sqlite3 "$WPNDB" "SELECT RecordId, PrimaryId FROM NotificationHandler;" 2>/dev/null
echo ""

echo "[*] Extracting Telegram notifications..."
echo "----------------------------------------------"
sqlite3 "$WPNDB" "
SELECT
    nh.PrimaryId as App,
    n.Payload as Content
FROM Notification n
JOIN NotificationHandler nh ON n.HandlerId = nh.RecordId
WHERE nh.PrimaryId LIKE '%Telegram%'
" 2>/dev/null | while IFS='|' read -r app payload; do
    echo "App: $app"
    echo "Payload:"
    echo "$payload" | sed 's/&amp;/\&/g' | grep -oP '<text[^>]*>\K[^<]+' | while read -r line; do
        echo "  - $line"
    done
    echo ""
done

echo "[*] Extracting all notification summaries..."
echo "----------------------------------------------"
sqlite3 "$WPNDB" "
SELECT
    nh.PrimaryId as App,
    n.Payload as Content
FROM Notification n
JOIN NotificationHandler nh ON n.HandlerId = nh.RecordId
" 2>/dev/null | strings | grep -E "(target|victim|encrypt|ransom)" -i

echo ""
echo "[*] Done!"
