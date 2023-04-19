{{ config(materialized='table') }}

select *
from {{ metrics.calculate(
    [metric('total_commits'), metric('active_authors')],
    grain='week'
)}}
