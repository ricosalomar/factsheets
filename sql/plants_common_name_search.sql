SELECT p.scientific_name, p.slug, n.common_name, GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/category/',c2.slug,'">',c2.category,'</a>') SEPARATOR ', ') as categories 
FROM plants_commonname n
LEFT JOIN plants_plant p ON p.id = n.plant_id
LEFT JOIN plants_plant_category pc ON pc.plant_id = p.id
LEFT JOIN plants_category c ON c.id = pc.category_id 
LEFT JOIN plants_plant_category pc2 ON pc2.plant_id = p.id 
LEFT JOIN plants_category c2 ON pc2.category_id = c2.id 
LEFT OUTER JOIN plants_cultivar cv ON (p.`id` = cv.`plant_id`) 
LEFT OUTER JOIN taggit_taggeditem ti ON (p.`id` = ti.`object_id`) 
LEFT OUTER JOIN taggit_tag t ON (ti.`tag_id` = t.`id`) 
LEFT OUTER JOIN `django_content_type` ON (ti.`content_type_id` = `django_content_type`.`id`) 
WHERE (p.`scientific_name` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR p.`comment` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR n.`common_name` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR cv.`cultivar` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR (t.`name` REGEXP '[[:<:]]thistle[[:>:]]' = 1 AND `django_content_type`.`id` = 12 ) 
OR p.`color` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR p.`flower_color` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR p.`flower` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR p.`foliage` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR p.`season` REGEXP '[[:<:]]thistle[[:>:]]' = 1 
OR c.`category` REGEXP '[[:<:]]thistle[[:>:]]' = 1 ) 
GROUP BY n.common_name ORDER BY n.common_name ASC

