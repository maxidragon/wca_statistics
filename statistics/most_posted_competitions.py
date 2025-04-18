sql = '''
SELECT
CASE 
  WHEN u.wca_id IS NOT NULL THEN CONCAT('[', u.name, '](https://www.worldcubeassociation.org/persons/', u.wca_id, ')')
  ELSE u.name 
END AS posted_by,
COUNT(*) AS posted_competitions 
FROM competitions AS c LEFT JOIN users AS u ON c.results_posted_by=u.id 
WHERE results_posted_by IS NOT NULL 
GROUP BY results_posted_by 
ORDER BY posted_competitions DESC;
'''
title = 'Most posted competitions overall'
description = 'This statistic shows people who posted the most competitions.'
headers = ['Person', 'Posted competitions']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description