{{ config(materialized='table') }}

with 
R as (
    select * from {{ ref('stg_repos') }}
),
C as (
    select
        count(*) as contributers,
        repo,
    from {{ ref('stg_contributers') }}
    group by repo
),
S as (
    select
        count(*) as commits,
        repo,
    from {{ ref('stg_commits') }}
    group by repo
)
select R.*, C.contributers, S.commits
from R
left join C on R.repo = C.repo
left join S on R.repo = S.repo
order by R.stars desc

