create table if not exists os_listings
(
    listing_pk  serial
        constraint os_listings_pk
            primary key,
    croc_number integer,
    price       numeric,
    url         text
);
