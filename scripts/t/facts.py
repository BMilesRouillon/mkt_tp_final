import pandas as pd
import numpy as np

def create_fact_sales_order(df_orders_all, dim_date_lookup):
    df = df_orders_all.copy()
    
    # Atributos : - order_id, customer_id, channel_id, store_id, shipping_address_id, 
    #             - billing_address_id, date_key, status, subtotal, tax_amount, 
    #             - shipping_fee, total_amount

    df = pd.merge(
        df, 
        dim_date_lookup, 
        left_on='order_date_dt', 
        right_on='full_date_dt', 
        how='left'
    )
    df = df[['order_id', 'customer_id', 'channel_id', 'store_id', 'shipping_address_id', 
             'billing_address_id', 'date_key', 'status', 'subtotal', 'tax_amount', 
             'shipping_fee', 'total_amount']]
             
    return df

def create_fact_sales_order_item(raw_data, df_orders_all, dim_date_lookup):
    
    # Atributos : - order_item_id, order_id, product_id, date_key, quantity, 
    #             - unit_price, discount_amount, line_total
    df = raw_data['sales_order_item'].copy()
    df_valid_items = pd.merge(
        df,
        df_orders_all[['order_id', 'order_date_dt']], 
        on='order_id',
        how='inner' 
    )
    df_with_date = pd.merge(
        df_valid_items,
        dim_date_lookup,
        left_on='order_date_dt',
        right_on='full_date_dt',
        how='left'
    )
    df = df_with_date[['order_item_id', 'order_id', 'product_id', 'date_key', 
                       'quantity', 'unit_price', 'discount_amount', 'line_total']]                 
    return df

def create_fact_payment(raw_data, df_orders_all, dim_date_lookup):
    
    # Atributos : - payment_id, order_id, date_key, method, amount, status
    
  
    df = raw_data['payment'].copy()
    
    df_all_payments = pd.merge(
        df,
        df_orders_all[['order_id', 'order_date_dt']],
        on='order_id',
        how='inner'
    )
    

    df_with_date = pd.merge(
        df_all_payments,
        dim_date_lookup,
        left_on='order_date_dt',
        right_on='full_date_dt',
        how='left'
    )
    
    df = df_with_date[['payment_id', 'order_id', 'date_key', 'method', 'amount', 'status']]
    return df

def create_fact_shipment(raw_data, dim_date_lookup):
    
    # Atributos : - shipment_id, order_id, date_key, carrier, tracking_number, status, 
    #             - shipped_at, delivered_at, delivery_time_days
    
    print("     - Creando fact_shipment...")
    df = raw_data['shipment'].copy()
    
    df['shipped_at'] = pd.to_datetime(df['shipped_at'])
    df['delivered_at'] = pd.to_datetime(df['delivered_at'])
    
 
    df['delivery_time_days'] = (df['delivered_at'] - df['shipped_at']).dt.total_seconds() / (60*60*24)
    
 
    df['shipped_at_dt'] = df['shipped_at'].dt.date
    
    df = pd.merge(
        df, 
        dim_date_lookup, 
        left_on='shipped_at_dt', 
        right_on='full_date_dt', 
        how='left'
    )
    
    df = df[['shipment_id', 'order_id', 'date_key', 'carrier', 'tracking_number', 'status', 
             'shipped_at', 'delivered_at', 'delivery_time_days']]
             
    return df

def create_fact_web_session(raw_data, dim_date_lookup):
    
    # Atributos : - session_id, customer_id, date_key, started_at, ended_at, 
    #             - source, device, session_duration_sec
    
    print("     - Creando fact_web_session...")
    df = raw_data['web_session'].copy()
    
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    

    df['session_duration_sec'] = (df['ended_at'] - df['started_at']).dt.total_seconds()
    
    df['started_at_dt'] = df['started_at'].dt.date
    
    df = pd.merge(
        df, 
        dim_date_lookup, 
        left_on='started_at_dt', 
        right_on='full_date_dt', 
        how='left'
    )
    
    df = df[['session_id', 'customer_id', 'date_key', 'started_at', 'ended_at', 
             'source', 'device', 'session_duration_sec']]
             
    return df

def create_fact_nps_response(raw_data, dim_date_lookup):
    
    # Atributos : - nps_id, customer_id, channel_id, date_key, score, 
    #             - nps_type, comment, responded_at
    
    df = raw_data['nps_response'].copy()
    
    def classify_nps(score):
        if score >= 9: return 'Promotor'
        elif score <= 6: return 'Detractor'
        else: return 'Neutro'
        
    df['nps_type'] = df['score'].apply(classify_nps)
    
    
    df['responded_at'] = pd.to_datetime(df['responded_at'])
    df['responded_at_dt'] = df['responded_at'].dt.date
    
    df = pd.merge(
        df, 
        dim_date_lookup, 
        left_on='responded_at_dt', 
        right_on='full_date_dt', 
        how='left'
    )
    
    df = df[['nps_id', 'customer_id', 'channel_id', 'date_key', 
             'score', 'nps_type', 'comment', 'responded_at']]
             
    return df