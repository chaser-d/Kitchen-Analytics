select
    ticket_id,
    trim(delivery_partner) as delivery_partner,
    commission_fee_usd,
    net_payout_usd,
    
    -- Calculate the exact percentage commission the marketplace charged
    case
        when (net_payout_usd + commission_fee_usd) > 0 
        then round(cast(commission_fee_usd as DOUBLE) / (net_payout_usd + commission_fee_usd) * 100, 2)
        else 0.0
    end as commission_rate_pct
from {{ source('restaurant_raw', 'raw_marketplace_commissions') }}
