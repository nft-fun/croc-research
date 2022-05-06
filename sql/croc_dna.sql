create table if not exists croc_dna
(
    croc                 integer,
    dna                  varchar(999),
    bin_dna              varchar(999),
    initial_bin_length   integer,
    optimized_bin_length integer,
    padded_bin           varchar(999),
    trait_count          integer,
    hex_dna              text,
    bytes_dna            text,
    a1                   integer,
    a2                   integer,
    a3                   integer,
    a4                   integer,
    a5                   integer,
    a6                   integer,
    a7                   integer,
    a8                   integer,
    a9                   integer,
    a10                  integer,
    a11                  integer,
    attr_list            text
);
