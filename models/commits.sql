{{ config(materialized='table') }}

with logs as (

    select * from {{ ref('stg_logs') }}

)

select distinct
    hash,
    author,
    email,
    message,
    datetime,
    concat('UTC', substr(raw_date, 20)) as utc_offset
from logs

