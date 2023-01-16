{{ config(materialized='table') }}

with

source as (

    select * from {{ source('git_repo', 'commits') }}

),

renamed as (

    select
        hash,
        author,
        email,
        message,
        date as datetime
    from source

)

select * from renamed
