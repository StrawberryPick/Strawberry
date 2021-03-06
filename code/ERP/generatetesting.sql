-- commenting 
-- testing https://stackoverflow.com/questions/17931320/how-to-insert-random-data-into-a-sqlite-table-using-only-queries
INSERT INTO TEST (x,y,z)
  SELECT RANDOM(), RANDOM(), RANDOM()
   FROM (SELECT * FROM (
         (SELECT 0 UNION ALL SELECT 1) t2, 
         (SELECT 0 UNION ALL SELECT 1) t4,
         (SELECT 0 UNION ALL SELECT 1) t8,
         (SELECT 0 UNION ALL SELECT 1) t16,
         (SELECT 0 UNION ALL SELECT 1) t32,
         (SELECT 0 UNION ALL SELECT 1) t64,
         (SELECT 0 UNION ALL SELECT 1) t128,
         (SELECT 0 UNION ALL SELECT 1) t256,
         (SELECT 0 UNION ALL SELECT 1) t512,
         (SELECT 0 UNION ALL SELECT 1) t1024,
         (SELECT 0 UNION ALL SELECT 1) t2048
         )
    ) LIMIT 246;