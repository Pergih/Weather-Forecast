{{ config(
    materialized='table',
)}}


with base as (

    select
        date(api_timestamp) as date,
        location,
        temp_c,
        humidity,
        precip_mm,
        wind_kph
    from {{ ref('stg_weather') }}

),

aggregated as (

    select
        date,
        location,
        avg(temp_c) as avg_temp_c,
        avg(humidity) as avg_humidity,
        avg(precip_mm) as avg_precip_mm,
        avg(wind_kph) as avg_wind_kph
    from base
    group by date, location

)

select * from aggregated