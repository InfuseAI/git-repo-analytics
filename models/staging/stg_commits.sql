{{ config(materialized='view') }}

with

source as (

    select * from {{ source('git_repo', 'raw_commits') }}

),

renamed as (

    select
        repo,
        hash,
        author,
        email,
        message,
        date as datetime,
        raw_date,
        concat('UTC', substr(raw_date, 20)) as utc_offset
    from source

)

select * from renamed where repo = 'duckdb/duckdb'
