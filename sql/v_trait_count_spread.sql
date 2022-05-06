create or replace view v_trait_count_spread(trait_count, count) as
SELECT croc_dna.trait_count,
       count(*) AS count
FROM croc_dna
GROUP BY croc_dna.trait_count
ORDER BY croc_dna.trait_count;
