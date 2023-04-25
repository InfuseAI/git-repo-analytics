{{ config(materialized='table') }}

select *
from {{ metrics.calculate(
    [metric('total_commits'), metric('active_authors')],
    dimensions=['repo'],
    grain='week',
    start_date='2022-07-01'
)}}
