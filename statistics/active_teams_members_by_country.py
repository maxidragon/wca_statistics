sql = '''
SELECT p.countryId, COUNT(*) AS count 
FROM user_roles ur JOIN users u ON ur.user_id=u.id 
JOIN Persons p on u.wca_id = p.wca_id
JOIN user_groups ug on ur.group_id = ug.id
WHERE ur.metadata_type = "RolesMetadataTeamsCommittees" 
AND ur.end_date IS NULL
GROUP BY p.countryId ORDER BY count DESC;
'''
title = 'Active team members by country'
description = ''
headers = ['Country', 'Number of active team members']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description