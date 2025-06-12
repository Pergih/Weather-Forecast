{{config (
    materialized='table',
    unique_key='id'
)}}

select*
from {{ source('public', 'weather_data') }}