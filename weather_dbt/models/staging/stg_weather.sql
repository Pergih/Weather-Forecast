{{config (
    materialized='table',
    unique_key='id'
)}}

with source as (
    select*
    from {{ source('public', 'weather_data') }}
)

select
    id,
    date,
    location,
    temp_c,
    humidity,
    precip_mm,
    wind_kph,
    api_timestamp
from source
