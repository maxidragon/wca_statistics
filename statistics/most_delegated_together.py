sql = '''
WITH dt1 AS (
    SELECT delegate_id AS id1, 
           CONCAT('[', users.name, '](https://www.worldcubeassociation.org/persons/', users.wca_id, ')') AS d1name, 
           users.wca_id, 
           competition_id AS cid1 
    FROM competition_delegates 
    JOIN users ON delegate_id = users.id
), 
dt2 AS (
    SELECT delegate_id AS id2, 
           CONCAT('[', users.name, '](https://www.worldcubeassociation.org/persons/', users.wca_id, ')') AS name, 
           users.wca_id, 
           competition_id AS cid2 
    FROM competition_delegates 
    JOIN users ON delegate_id = users.id
), 
dpc AS (
    SELECT competition_id, COUNT(delegate_id) AS num_d 
    FROM competition_delegates 
    GROUP BY competition_id
)
SELECT DISTINCT 
    CONCAT(IF(dt1.d1name<dt2.name,dt1.d1name,dt2.name), " + ", IF(dt1.d1name<dt2.name,dt2.name,dt1.d1name)) AS Delegates, 
    COUNT(dt2.id2) AS num_comps_together
FROM dt1
JOIN dpc ON dpc.competition_id = dt1.cid1
JOIN dt2 ON dt2.cid2 = dt1.cid1   
JOIN competitions ON competitions.id = dt1.cid1  
WHERE NOT dt1.id1 = dt2.id2 
  AND competitions.results_posted_at IS NOT NULL 
  AND num_d = 2
GROUP BY id1, id2
ORDER BY num_comps_together DESC
LIMIT 100;
'''
title = 'Most competitions delegated together'
description = 'This statistic shows the number of competitions that two delegates have delegated together.'
headers = ['Delegates', 'Number of competitions delegated together']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description