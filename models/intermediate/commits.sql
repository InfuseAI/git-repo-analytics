{{ config(materialized='table', tags='piperider') }}

with commits as (

    select * from {{ ref('stg_commits') }}

)

select distinct
    repo,
    hash,
    author,
    email,
    message,
    datetime
from commits

