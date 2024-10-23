sql = '''
SELECT 
    DATE_FORMAT(results_posted_at, "%Y-%m") month, 
    ROUND(AVG(TIMESTAMPDIFF(SECOND, results_submitted_at, results_posted_at)) / 3600, 2) posting_delay_h
FROM Competitions c
WHERE results_submitted_at < results_posted_at
AND TIMESTAMPDIFF(MONTH, results_posted_at, CURRENT_TIMESTAMP) <= 12
GROUP BY month 
ORDER BY month DESC
'''
title = 'Results posting delay by month'
headers = ['Month', 'Posting delay (hours)']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title