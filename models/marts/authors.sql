{{ config(materialized='table') }}

with C as (
    select * from {{ ref('stg_commits') }}
)

select distinct
    repo as repo,
    author as name,
    email as email,
    substr(email, instr(email, '@') + 1) as domain
from C

