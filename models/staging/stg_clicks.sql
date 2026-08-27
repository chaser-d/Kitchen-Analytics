select
    event_id,
    user_id,
    
    -- Remediate tracking anomaly: fallback to 'UNKNOWN_SESSION' if tracking dropped the ID
    coalesce(session_id, 'UNKNOWN_SESSION') as session_id,
    
    trim(platform_channel) as platform_channel,
    trim(target_brand) as brand_name,
    
    -- Convert textual ingestion strings into true system timestamps for data freshness auditing
    cast(event_timestamp as TIMESTAMP) as event_timestamp_at
from {{ source('restaurant_raw', 'raw_customer_clicks') }}
