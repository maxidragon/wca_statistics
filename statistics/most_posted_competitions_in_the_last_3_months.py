sql = '''
SELECT
CASE 
  WHEN u.wca_id IS NOT NULL THEN CONCAT('[', u.name, '](https://www.worldcubeassociation.org/persons/', u.wca_id, ')')
  ELSE u.name 
END AS member,
COUNT(*) AS results_posted
FROM competitions c
INNER JOIN users u
ON c.results_posted_by = u.id
WHERE TIMESTAMPDIFF(MONTH, results_posted_at, CURRENT_TIMESTAMP) <= 3
GROUP BY results_posted_by
ORDER BY results_posted DESC;
'''
title = 'Most posted competitions in the last 3 months'
description = 'This statistic shows people who posted the most competitions in the last 3 months.'
headers = ['Person', 'Posted competitions']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description