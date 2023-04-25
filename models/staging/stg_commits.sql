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
        raw_date
    from source

)

select * from renamed
