sql = '''
SELECT 
    TIMESTAMPDIFF(SECOND, (
        SELECT end_time 
        FROM (
            schedule_activities sa 
            JOIN venue_rooms vr ON (sa.holder_id = vr.id AND sa.holder_type = 'VenueRoom')
        ) 
        JOIN competition_venues cv ON vr.competition_venue_id = cv.id
        WHERE cv.competition_id = c.id 
        ORDER BY sa.end_time DESC 
        LIMIT 1
    ), c.results_posted_at) / 3600 AS diff_in_hours, 
    CONCAT('[', c.id, '](https://www.worldcubeassociation.org/competitions/', c.id, ')') AS competition_id,
    CASE 
        WHEN u.wca_id IS NOT NULL THEN CONCAT('[', u.name, '](https://www.worldcubeassociation.org/persons/', u.wca_id, ')')
        ELSE u.name 
    END AS posted_by,
    GROUP_CONCAT(
        CONCAT('[', d.name, '](https://www.worldcubeassociation.org/persons/', d.wca_id, ')')
        SEPARATOR ', ') AS delegates
FROM 
    Competitions c
JOIN 
    users u ON c.results_posted_by = u.id
LEFT JOIN 
    competition_delegates cd ON cd.competition_id = c.id
LEFT JOIN 
    users d ON cd.delegate_id = d.id
GROUP BY 
    c.id, u.name
HAVING 
    diff_in_hours IS NOT NULL
ORDER BY 
    diff_in_hours
LIMIT 20;
'''
title = 'Fasted posted competitions'
description = 'This statistic shows the competitions that were posted the fastest after last schedule activity ended. The difference is calculated in hours.'
headers = ['Difference in hours', 'Competition ID', 'Posted by', 'Delegates']

def execute(db):
  cursor = db.cursor()
  cursor.execute(sql)
  return cursor.fetchall(), headers, title, description