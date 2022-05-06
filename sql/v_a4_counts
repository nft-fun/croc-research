create or replace view v_a4_counts(a4, count, percentage) as
SELECT croc_dna.a4,
       count(*)                                                   AS count,
       round(count(*)::numeric / 8888::numeric * 100::numeric, 3) AS percentage
FROM croc_dna
GROUP BY croc_dna.a4
ORDER BY croc_dna.a4;
