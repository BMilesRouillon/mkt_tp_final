import pandas as pd

def create_dim_date(raw_data):

    # Atributos : - date_key, full_date, year, quarter, month, month_name, day, day_of_week, day_name

    try:
        order_dates = pd.to_datetime(raw_data['sales_order']['order_date'])
        nps_dates = pd.to_datetime(raw_data['nps_response']['responded_at'])
        session_dates = pd.to_datetime(raw_data['web_session']['started_at'])
    except Exception as e:
        print(f"      ERROR al leer fechas para dim_date: {e}")
        return None
    
    all_dates = pd.concat([order_dates, nps_dates, session_dates])
    min_date = all_dates.min().date()
    max_date = all_dates.max().date()
    
    df = pd.DataFrame({'full_date': pd.date_range(start=min_date, end=max_date)})
    
  
    df['date_key'] = df['full_date'].dt.strftime('%Y%m%d').astype(int) # PK
    df['year'] = df['full_date'].dt.year
    df['quarter'] = df['full_date'].dt.quarter
    df['month'] = df['full_date'].dt.month
    df['month_name'] = df['full_date'].dt.strftime('%B')
    df['day'] = df['full_date'].dt.day
    df['day_of_week'] = df['full_date'].dt.dayofweek 
    df['day_name'] = df['full_date'].dt.strftime('%A')
    
    df = df[['date_key', 'full_date', 'year', 'quarter', 'month', 'month_name', 'day', 'day_of_week', 'day_name']]
    return df

def create_dim_channel(raw_data):
    
    # Atributos : - channel_id, channel_code, channel_name
    
    df = raw_data['channel'].copy()
    return df

def create_dim_province(raw_data):
    
    # Atributos : - province_id, province_name, code
    
    df = raw_data['province'].copy()
    df = df.rename(columns={'name': 'province_name'})
    return df 

def create_dim_customer(raw_data):
    
    # Atributos : - customer_id, email, first_name, last_name, phone, status, created_at
    
    df = raw_data['customer'].copy()
    return df[['customer_id', 'email', 'first_name', 'last_name', 'phone', 'status', 'created_at']]

def create_dim_product(raw_data):
    
    # Atributos : - product_id, sku, product_name, list_price, status, created_at, category_id, category_name, parent_id
    
    df_prod = raw_data['product'].copy()
    df_cat = raw_data['product_category'].copy()
    df_cat = df_cat.rename(columns={'name': 'category_name'})
    df = pd.merge(df_prod, df_cat, on='category_id', how='left')
    df = df[['product_id', 'sku', 'name', 'list_price', 'status', 'created_at', 'category_id', 'category_name', 'parent_id']]
    df = df.rename(columns={'name': 'product_name'})
    return df

def create_dim_address(raw_data, dim_province):
    
    # Atributos : - address_id, line1, line2, city, province_id, province_name, postal_code, country_code, created_at
    
    df_addr = raw_data['address'].copy()
    df_prov = dim_province.copy() 
    df = pd.merge(df_addr, df_prov, on='province_id', how='left')
    return df[['address_id', 'line1', 'line2', 'city', 'province_id', 'province_name', 'postal_code', 'country_code', 'created_at']]

def create_dim_store(raw_data, dim_address):
    
    # Atributos : - store_id, store_name, address_id, line1, line2, city, province_id, province_name, postal_code, country_code
    
    df_store = raw_data['store'].copy()
    df_addr_prov = dim_address.copy() 
    df = pd.merge(df_store, df_addr_prov, on='address_id', how='left', suffixes=('_store', '_address'))
    df = df.rename(columns={'name': 'store_name'})
    return df[['store_id', 'store_name', 'address_id', 'line1', 'line2', 'city', 'province_id', 'province_name', 'postal_code', 'country_code']]

