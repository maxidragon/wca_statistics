sql = '''
SELECT 
    CASE 
    WHEN d.wca_id IS NOT NULL THEN CONCAT('[', d.name, '](https://www.worldcubeassociation.org/persons/', d.wca_id, ')')
    ELSE d.name 
    END as delegate_name,
    COUNT(DISTINCT c.country_id) AS num_countries
FROM 
    competition_delegates cd
JOIN 
    competitions c ON cd.competition_id = c.id
JOIN 
    users d ON cd.delegate_id = d.id
WHERE
    c.country_id NOT IN ('XA', 'XE', 'XF', 'XM', 'XN', 'XO', 'XS', 'XW')
GROUP BY 
    d.id, d.name
HAVING
    num_countries > 1
ORDER BY 
    num_countries DESC;
'''
title = 'Delegated a competition in most countries'
description = 'This statistic shows the delegates who have delegated a competition in most countries. Multi-location FMC competitions are excluded.'
headers = ['Name', 'Countries']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description