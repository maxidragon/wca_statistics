sql = '''
SELECT
CASE 
  WHEN u.wca_id IS NOT NULL THEN CONCAT('[', u.name, '](https://www.worldcubeassociation.org/persons/', u.wca_id, ')')
  ELSE u.name 
END AS member,
COUNT(*) AS announced_competitions 
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