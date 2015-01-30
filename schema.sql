drop table GraphemeClusterBreak;
create table GraphemeClusterBreak (
    cp      integer not null primary key,
    value   text not null
);

drop table GraphemeClusterBreakTest;
create table GraphemeClusterBreakTest (
    name    text not null primary key,
    pattern text not null,
    comment text not null
);

drop table WordBreak;
create table WordBreak (
    cp      integer not null primary key,
    value   text not null
);

drop table WordBreakTest;
create table WordBreakTest (
    name    text not null primary key,
    pattern text not null,
    comment text not null
);

drop table SentenceBreak;
create table SentenceBreak (
    cp      integer not null primary key,
    value   text not null
);

drop table SentenceBreakTest;
create table SentenceBreakTest (
    name    text not null primary key,
    pattern text not null,
    comment text not null
);

drop table LineBreak;
create table LineBreak (
    cp      integer not null primary key,
    value   text not null
);

drop table LineBreakTest;
create table LineBreakTest (
    name    text not null primary key,
    pattern text not null,
    comment text not null
);

