{{ config(materialized='table') }}

with source_data as (

    select *
    from {{ source('git_repo', 'commits') }}

)

select distinct
    author as name,
    email as email
from source_data

