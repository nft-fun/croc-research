create or replace view v_9_trait_rarity
            (croc, overall_rarity, a1, a2, a3, a4, a5, a6, a7, a8, a9, a1_rarity, a2_rarity, a3_rarity, a4_rarity,
             a5_rarity, a6_rarity, a7_rarity, a8_rarity, a9_rarity, offset_croc)
as
SELECT cd.croc,
       a1.percentage * a2.percentage * a3.percentage * a4.percentage * a5.percentage * a6.percentage * a7.percentage *
       a8.percentage * a9.percentage AS overall_rarity,
       cd.a1,
       cd.a2,
       cd.a3,
       cd.a4,
       cd.a5,
       cd.a6,
       cd.a7,
       cd.a8,
       cd.a9,
       a1.percentage                 AS a1_rarity,
       a2.percentage                 AS a2_rarity,
       a3.percentage                 AS a3_rarity,
       a4.percentage                 AS a4_rarity,
       a5.percentage                 AS a5_rarity,
       a6.percentage                 AS a6_rarity,
       a7.percentage                 AS a7_rarity,
       a8.percentage                 AS a8_rarity,
       a9.percentage                 AS a9_rarity,
       CASE
           WHEN (cd.croc - 5759) < 1 THEN cd.croc - 5759 + 8888
           ELSE cd.croc - 5759
           END                       AS offset_croc
FROM croc_dna cd
         JOIN v_a1_counts a1 ON a1.a1 = cd.a1
         JOIN v_a2_counts a2 ON a2.a2 = cd.a2
         JOIN v_a3_counts a3 ON a3.a3 = cd.a3
         JOIN v_a4_counts a4 ON a4.a4 = cd.a4
         JOIN v_a5_counts a5 ON a5.a5 = cd.a5
         JOIN v_a6_counts a6 ON a6.a6 = cd.a6
         JOIN v_a7_counts a7 ON a7.a7 = cd.a7
         JOIN v_a8_counts a8 ON a8.a8 = cd.a8
         JOIN v_a9_counts a9 ON a9.a9 = cd.a9;
