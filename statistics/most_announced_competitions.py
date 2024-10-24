sql = '''
SELECT u.name, COUNT(*) AS announced_competitions 
FROM Competitions AS c LEFT JOIN users AS u ON c.announced_by=u.id 
WHERE announced_by IS NOT NULL 
GROUP BY announced_by 
ORDER BY announced_competitions DESC;
'''
title = 'Most announced competitions'
description = 'This statistic shows people who announced the most competitions.'
headers = ['Person', 'Announced competitions']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description