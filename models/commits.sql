{{ config(materialized='table') }}

with logs as (

    select * from {{ ref('stg_logs') }}

)

select distinct
    hash,
    author,
    email,
    message,
    datetime
from logs

