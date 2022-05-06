create or replace view v_zero_trait_counts(offset_croc, croc, attr_list, num_occurrences) as
SELECT v9tr.offset_croc,
       t.croc,
       t.attr_list,
       w.num_occurrences
FROM croc_dna t
         CROSS JOIN LATERAL ( SELECT x.word,
                                     count(*) AS num_occurrences
                              FROM regexp_split_to_table(lower(t.attr_list), '[\s[:punct:]]+'::text) x(word)
                              WHERE t.attr_list ~~ '%| 0 |%'::text
                                 OR t.attr_list ~~ '%0 |%'::text
                                 OR t.attr_list ~~ '%| 0%'::text
                              GROUP BY x.word) w
         JOIN v_9_trait_rarity v9tr ON t.croc = v9tr.croc
ORDER BY w.num_occurrences DESC;
