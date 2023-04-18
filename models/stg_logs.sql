{{ config(materialized='view') }}

with

source as (

    select * from {{ source('git_repo', 'logs') }}

),

renamed as (

    select
        repo_url,
        hash,
        author,
        email,
        message,
        date as datetime,
        raw_date
    from source

)

select * from renamed
