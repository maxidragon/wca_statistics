sql = '''
SELECT 
    DATE_FORMAT(announced_at, "%Y-%m") month, 
    ROUND(AVG(TIMESTAMPDIFF(SECOND, confirmed_at, announced_at)) / 3600, 2) announcement_delay_h
FROM Competitions c
WHERE confirmed_at < announced_at
AND TIMESTAMPDIFF(MONTH, announced_at, CURRENT_TIMESTAMP) <= 12
GROUP BY month 
ORDER BY month DESC
'''
title = 'Announcement delay by month'
description = 'This statistic shows the average delay between confirming competition by WCA Delegate and announcing it by the WCAT.'
headers = ['Month', 'Announcement delay (hours)']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description