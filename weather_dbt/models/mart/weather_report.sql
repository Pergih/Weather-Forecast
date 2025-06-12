{{ config(
    materialized='table',
    unique_key='id'
)}}

select
    location,
    temp_c,
    humidity,
    precip_mm,
    wind_kph,
    api_timestamp    
from {{ ref('stg_weather') }}
