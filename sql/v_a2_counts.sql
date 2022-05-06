create or replace view v_a2_counts(a2, count, percentage) as
SELECT croc_dna.a2,
       count(*)                                                   AS count,
       round(count(*)::numeric / 8888::numeric * 100::numeric, 3) AS percentage
FROM croc_dna
GROUP BY croc_dna.a2
ORDER BY croc_dna.a2;
