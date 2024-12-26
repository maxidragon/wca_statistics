sql = '''
SELECT
CASE 
  WHEN u.wca_id IS NOT NULL THEN CONCAT('[', u.name, '](https://www.worldcubeassociation.org/persons/', u.wca_id, ')')
  ELSE u.name 
END AS member,
COUNT(*) AS announced_competitions
FROM Competitions c
INNER JOIN users u
ON c.announced_by = u.id
WHERE TIMESTAMPDIFF(MONTH, announced_at, CURRENT_TIMESTAMP) <= 3
GROUP BY announced_by
ORDER BY announced_competitions DESC;
'''
title = 'Most announced competitions in the last 3 months'
description = 'This statistic shows people who announced the most competitions in the last 3 months.'
headers = ['Person', 'Announced competitions']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description