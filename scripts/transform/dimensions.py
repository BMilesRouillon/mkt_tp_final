import pandas as pd

def _create_dim_date(raw_data):
    """
    (Privado) Genera una dimensión de fecha completa a partir de las fechas mínimas y máximas
    encontradas en las tablas de hechos (órdenes, nps, sesiones).
    """
    print("    - Creando dim_date...")
    
    try:
        # 1. Convertir todas las columnas de fecha a datetime
        order_dates = pd.to_datetime(raw_data['sales_order']['order_date'])
        nps_dates = pd.to_datetime(raw_data['nps_response']['responded_at'])
        session_dates = pd.to_datetime(raw_data['web_session']['started_at'])
    except Exception as e:
        print(f"      ERROR al leer fechas para dim_date: {e}")
        return None
    
    # 2. Encontrar la fecha mínima y máxima global
    all_dates = pd.concat([order_dates, nps_dates, session_dates])
    min_date = all_dates.min().date()
    max_date = all_dates.max().date()
    
    # 3. Crear el rango de fechas
    df = pd.DataFrame({'full_date': pd.date_range(start=min_date, end=max_date)})
    
    # 4. Enriquecer la dimensión de fecha
    df['date_key'] = df['full_date'].dt.strftime('%Y%m%d').astype(int) # PK
    df['year'] = df['full_date'].dt.year
    df['quarter'] = df['full_date'].dt.quarter
    df['month'] = df['full_date'].dt.month
    df['month_name'] = df['full_date'].dt.strftime('%B')
    df['day'] = df['full_date'].dt.day
    df['day_of_week'] = df['full_date'].dt.dayofweek # Lunes=0, Domingo=6
    df['day_name'] = df['full_date'].dt.strftime('%A')
    
    # Reordenamos
    df = df[['date_key', 'full_date', 'year', 'quarter', 'month', 'month_name', 'day', 'day_of_week', 'day_name']]
    return df

def transform_dimensions(raw_data):
    """
    Crea todas las dimensiones "anchas" (con todos los atributos)
    y las devuelve en un diccionario de dataframes.
    """
    print("  -> Transformando Dimensiones...")
    dims = {}

    # 1. Crear dim_date (ahora parte de este script)
    dims['dim_date'] = _create_dim_date(raw_data)
    
    # 2. dim_channel
    print("    - Creando dim_channel...")
    df = raw_data['channel'].copy()
    # Usamos todas las columnas del raw
    df = df.rename(columns={'code': 'channel_code', 'name': 'channel_name'})
    dims['dim_channel'] = df
    
    # 3. dim_province
    print("    - Creando dim_province...")
    df = raw_data['province'].copy()
    df = df.rename(columns={'name': 'province_name'})
    # Usamos todas las columnas del raw (incluyendo 'code' si existe)
    dims['dim_province'] = df
    
    # 4. dim_customer (dimensión "ancha")
    print("    - Creando dim_customer...")
    df = raw_data['customer'].copy()
    # Usamos todas las columnas del raw
    dims['dim_customer'] = df[['customer_id', 'email', 'first_name', 'last_name', 'phone', 'status', 'created_at']]
    
    # 5. dim_product (ancha, uniendo con categoría)
    print("    - Creando dim_product...")
    df_prod = raw_data['product'].copy()
    df_cat = raw_data['product_category'].copy()
    df_cat = df_cat.rename(columns={'name': 'category_name'})
    df = pd.merge(df_prod, df_cat, on='category_id', how='left')
    # Usamos todas las columnas de la unión
    dims['dim_product'] = df[['product_id', 'sku', 'name', 'list_price', 'status', 'created_at', 'category_id', 'category_name', 'parent_id']]
    dims['dim_product'] = dims['dim_product'].rename(columns={'name': 'product_name'})
    
    # 6. dim_address (ancha, uniendo con provincia)
    print("    - Creando dim_address...")
    df_addr = raw_data['address'].copy()
    df_prov = dims['dim_province'].copy() # Usamos la dim_province ya limpia
    df = pd.merge(df_addr, df_prov, on='province_id', how='left')
    # Usamos todas las columnas de la unión
    dims['dim_address'] = df[['address_id', 'line1', 'line2', 'city', 'province_id', 'province_name', 'postal_code', 'country_code', 'created_at']]

    # 7. dim_store (ancha, uniendo con address y provincia)
    print("    - Creando dim_store...")
    df_store = raw_data['store'].copy()
    df_addr_prov = dims['dim_address'].copy() # Usamos la dim_address ya limpia
    df = pd.merge(df_store, df_addr_prov, on='address_id', how='left', suffixes=('_store', '_address'))
    df = df.rename(columns={'name': 'store_name'})
    # Usamos todas las columnas de la unión
    dims['dim_store'] = df[['store_id', 'store_name', 'address_id', 'line1', 'line2', 'city', 'province_id', 'province_name', 'postal_code', 'country_code']]

    print(f"  -> {len(dims)} Dimensiones creadas.")
    return dims