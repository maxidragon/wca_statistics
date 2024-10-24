sql = '''
SELECT u.name AS member, COUNT(*) AS announced_competitions
FROM Competitions c
INNER JOIN users u
ON c.announced_by = u.id
WHERE TIMESTAMPDIFF(MONTH, announced_at, CURRENT_TIMESTAMP) <= 3
GROUP BY u.name
ORDER BY announced_competitions DESC;
'''
title = 'Most announced competitions in the last 3 months'
description = 'This statistic shows people who announced the most competitions in the last 3 months.'
headers = ['Person', 'Announced competitions']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description