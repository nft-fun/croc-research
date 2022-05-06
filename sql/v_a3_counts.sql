create or replace view v_a3_counts(a3, count, percentage) as
SELECT croc_dna.a3,
       count(*)                                                   AS count,
       round(count(*)::numeric / 8888::numeric * 100::numeric, 3) AS percentage
FROM croc_dna
GROUP BY croc_dna.a3
ORDER BY croc_dna.a3;
