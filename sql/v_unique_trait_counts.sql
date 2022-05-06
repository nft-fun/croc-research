create or replace view v_unique_trait_counts
            (croc, offset_croc, dna, trait_count, attr_list, a1_rare_attribute, a1_rarity, a2_rare_attribute, a2_rarity,
             a3_rare_attribute, a3_rarity, a4_rare_attribute, a4_rarity, a5_rare_attribute, a5_rarity,
             a6_rare_attribute, a6_rarity, a7_rare_attribute, a7_rarity, a8_rare_attribute, a8_rarity,
             a9_rare_attribute, a9_rarity)
as
WITH all_crocs AS (SELECT croc_dna.croc,
                          croc_dna.dna,
                          croc_dna.bin_dna,
                          croc_dna.initial_bin_length,
                          croc_dna.optimized_bin_length,
                          croc_dna.padded_bin,
                          croc_dna.trait_count,
                          croc_dna.hex_dna,
                          croc_dna.bytes_dna,
                          croc_dna.a1,
                          croc_dna.a2,
                          croc_dna.a3,
                          croc_dna.a4,
                          croc_dna.a5,
                          croc_dna.a6,
                          croc_dna.a7,
                          croc_dna.a8,
                          croc_dna.a9,
                          croc_dna.a10,
                          croc_dna.a11,
                          croc_dna.attr_list
                   FROM croc_dna)
SELECT ac.croc,
       v9tr.offset_croc,
       ac.dna,
       ac.trait_count,
       ac.attr_list,
       ac.a1          AS a1_rare_attribute,
       v1c.percentage AS a1_rarity,
       ac.a2          AS a2_rare_attribute,
       v2c.percentage AS a2_rarity,
       ac.a3          AS a3_rare_attribute,
       v3c.percentage AS a3_rarity,
       ac.a4          AS a4_rare_attribute,
       v4c.percentage AS a4_rarity,
       ac.a5          AS a5_rare_attribute,
       v5c.percentage AS a5_rarity,
       ac.a6          AS a6_rare_attribute,
       v6c.percentage AS a6_rarity,
       ac.a7          AS a7_rare_attribute,
       v7c.percentage AS a7_rarity,
       ac.a8          AS a8_rare_attribute,
       v8c.percentage AS a8_rarity,
       ac.a9          AS a9_rare_attribute,
       v9c.percentage AS a9_rarity
FROM all_crocs ac
         JOIN v_9_trait_rarity v9tr ON ac.croc = v9tr.croc
         JOIN v_a1_counts v1c ON ac.a1 = v1c.a1
         JOIN v_a2_counts v2c ON ac.a2 = v2c.a2
         JOIN v_a3_counts v3c ON ac.a3 = v3c.a3
         JOIN v_a4_counts v4c ON ac.a4 = v4c.a4
         JOIN v_a5_counts v5c ON ac.a5 = v5c.a5
         JOIN v_a6_counts v6c ON ac.a6 = v6c.a6
         JOIN v_a7_counts v7c ON ac.a7 = v7c.a7
         JOIN v_a8_counts v8c ON ac.a8 = v8c.a8
         JOIN v_a9_counts v9c ON ac.a9 = v9c.a9
WHERE v1c.percentage < 0.035
   OR v2c.percentage < 0.035
   OR v3c.percentage < 0.035
   OR v4c.percentage < 0.035
   OR v5c.percentage < 0.035
   OR v6c.percentage < 0.035
   OR v7c.percentage < 0.035
   OR v8c.percentage < 0.035
   OR v9c.percentage < 0.035
ORDER BY v9tr.offset_croc;
