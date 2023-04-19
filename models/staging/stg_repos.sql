{{ config(materialized='view') }}

select * from {{ source('git_repo', 'raw_repos') }}