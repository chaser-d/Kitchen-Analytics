select
    t.ticket_id,
    t.store_id,
    t.brand_name,
    t.gross_order_value,
    t.ticket_opened_at,
    t.ticket_ready_at,
    t.kitchen_prep_time_minutes,
    t.is_canceled_order,
    
    -- Marketplace Financials
    coalesce(c.delivery_partner, 'Direct Pickup') as fulfillment_channel,
    coalesce(c.commission_fee_usd, 0.0) as commission_fee_usd,
    coalesce(c.net_payout_usd, t.gross_order_value) as net_payout_usd,
    coalesce(c.commission_rate_pct, 0.0) as commission_rate_pct,
    
    -- Executive Financial Metrics
    case
        when t.is_canceled_order = 1 then 0.0
        else (t.gross_order_value - coalesce(c.commission_fee_usd, 0.0))
    end as net_contribution_margin_usd
from {{ ref('stg_tickets') }} t
left join {{ ref('stg_commissions') }} c on t.ticket_id = c.ticket_id
