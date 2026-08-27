select
    ticket_id,
    store_id,
    trim(brand_name) as brand_name,
    gross_order_value,
    
    -- Cast raw text strings into true system timestamps
    cast(ticket_opened as TIMESTAMP) as ticket_opened_at,
    cast(ticket_ready as TIMESTAMP) as ticket_ready_at,
    
    -- Fix: If order was canceled, default prep time to 0 instead of a breaking NULL
    coalesce(
        date_diff('minute', cast(ticket_opened as TIMESTAMP), cast(ticket_ready as TIMESTAMP)),
        0
    ) as kitchen_prep_time_minutes,
    
    -- Flag canceled/abandoned tickets where order was never finalized
    case
        when ticket_ready is null then 1
        else 0
    end as is_canceled_order
from {{ source('restaurant_raw', 'raw_kitchen_tickets') }}
