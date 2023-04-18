{{ config(materialized='table') }}

with logs as (

    select * from {{ ref('stg_logs') }}

)

select
    repo_url,
    hash,
    author,
    email,
    message,
    datetime
from logs

