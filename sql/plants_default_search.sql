SELECT p.scientific_name, p.slug, GROUP_CONCAT( DISTINCT n.common_name SEPARATOR ', ') as common_names, GROUP_CONCAT( DISTINCT CONCAT('<a href="/plants/category/',c2.slug,'">',c2.category,'</a>') SEPARATOR ', ') as categories 
FROM plants_plant_category pc 
LEFT JOIN plants_category c ON c.id = pc.category_id 
LEFT JOIN plants_plant p ON p.id = pc.plant_id 
LEFT JOIN plants_plant_category pc2 ON pc2.plant_id = p.id 
LEFT JOIN plants_category c2 ON pc2.category_id = c2.id 
LEFT JOIN plants_commonname n ON p.id = n.plant_id 
LEFT OUTER JOIN plants_cultivar cv ON (p.`id` = cv.`plant_id`) 
LEFT OUTER JOIN taggit_taggeditem ti ON (p.`id` = ti.`object_id`) 
LEFT OUTER JOIN taggit_tag t ON (ti.`tag_id` = t.`id`) 
LEFT OUTER JOIN `django_content_type` ON (ti.`content_type_id` = `django_content_type`.`id`) 
WHERE (p.`scientific_name` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR p.`comment` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR n.`common_name` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR cv.`cultivar` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR (t.`name` REGEXP '[[:<:]]peony[[:>:]]' = 1 AND `django_content_type`.`id` = 12 ) 
OR p.`color` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR p.`flower_color` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR p.`flower` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR p.`foliage` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR p.`season` REGEXP '[[:<:]]peony[[:>:]]' = 1 
OR c.`category` REGEXP '[[:<:]]peony[[:>:]]' = 1 ) 
GROUP BY p.id ORDER BY common_name ASC