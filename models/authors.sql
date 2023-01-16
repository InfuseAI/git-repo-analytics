{{ config(materialized='table') }}

with commits as (

    select * from {{ ref('stg_commits') }}

)

select distinct
    author as name,
    email as email,
    substr(email, instr(email, '@') + 1) as domain
from commits

