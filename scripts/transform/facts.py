import pandas as pd

def transform_facts(raw_data, dims):
    """
    Crea todas las tablas de hechos "anchas", uniendo con las dimensiones
    y devolviendo un diccionario de dataframes.
    """
    print("  -> Transformando Tablas de Hechos...")
    facts = {}
    
    # Obtenemos las dimensiones clave que necesitaremos
    dim_date = dims['dim_date'].copy()
    dim_address = dims['dim_address'].copy()
    
    # Preparamos dim_date para los joins (convirtiendo su 'full_date' a tipo date)
    dim_date['full_date_dt'] = pd.to_datetime(dim_date['full_date']).dt.date
    
    # --- 1. fact_sales ---
    print("    - Creando fact_sales...")
    df_orders = raw_data['sales_order'].copy()
    df_items = raw_data['sales_order_item'].copy()
    df_payments = raw_data['payment'].copy()

    # a. Preparar Pagos
    df_payments_agg = df_payments.groupby('order_id').agg(
        payment_method = pd.NamedAgg(column='method', aggfunc=lambda x: ', '.join(x.unique())),
        total_paid = pd.NamedAgg(column='amount', aggfunc='sum')
    ).reset_index()

    # b. Filtrar Órdenes válidas
    valid_status = ['PAID', 'FULFILLED']
    df_orders_filtered = df_orders[df_orders['status'].isin(valid_status)].copy()
    
    # c. Unir Órdenes + Ítems
    df_sales = pd.merge(df_orders_filtered, df_items, on='order_id', how='inner')
    # d. Unir + Pagos
    df_sales = pd.merge(df_sales, df_payments_agg, on='order_id', how='left')
    # e. Unir + Provincia (desde dim_address)
    df_sales = pd.merge(
        df_sales, 
        dim_address[['address_id', 'province_id', 'province_name']], 
        left_on='shipping_address_id', 
        right_on='address_id', 
        how='left'
    )
    # f. Unir + dim_date (¡Nuevo!)
    df_sales['order_date_dt'] = pd.to_datetime(df_sales['order_date']).dt.date
    df_sales = pd.merge(
        df_sales,
        dim_date,
        left_on='order_date_dt',
        right_on='full_date_dt',
        how='left'
    )
    # Seleccionamos todas las columnas
    facts['fact_sales'] = df_sales

    # --- 2. fact_sessions ---
    print("    - Creando fact_sessions...")
    df = raw_data['web_session'].copy()
    df = df[df['customer_id'].notna()].copy() # Solo sesiones de clientes logueados
    
    # a. Convertir fechas y calcular métrica
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'], errors='coerce') # 'coerce' maneja errores
    df['session_duration_min'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    
    # b. Unir + dim_date
    df['session_date_dt'] = df['started_at'].dt.date
    df = pd.merge(
        df,
        dim_date,
        left_on='session_date_dt',
        right_on='full_date_dt',
        how='left'
    )
    facts['fact_sessions'] = df
    
    # --- 3. fact_nps ---
    print("    - Creando fact_nps...")
    df = raw_data['nps_response'].copy()
    
    # a. Clasificar (Métrica)
    def classify_nps(score):
        if score >= 9: return 'Promotor'
        elif score <= 6: return 'Detractor'
        else: return 'Neutro'
    df['nps_type'] = df['score'].apply(classify_nps)
    
    # b. Unir + dim_date
    df['response_date_dt'] = pd.to_datetime(df['responded_at']).dt.date
    df = pd.merge(
        df,
        dim_date,
        left_on='response_date_dt',
        right_on='full_date_dt',
        how='left'
    )
    facts['fact_nps'] = df
    
    # --- 4. fact_shipments ---
    print("    - Creando fact_shipments...")
    df_ship = raw_data['shipment'].copy()
    df_orders_ref = raw_data['sales_order'][['order_id', 'shipping_address_id']]
    df_dim_address_ref = dim_address[['address_id', 'province_id', 'province_name']]

    # a. Filtrar y calcular métrica
    df_ship_delivered = df_ship[df_ship['status'] == 'DELIVERED'].copy()
    df_ship_delivered['shipped_at'] = pd.to_datetime(df_ship_delivered['shipped_at'])
    df_ship_delivered['delivered_at'] = pd.to_datetime(df_ship_delivered['delivered_at'])
    df_ship_delivered['delivery_time_days'] = (df_ship_delivered['delivered_at'] - df_ship_delivered['shipped_at']).dt.days

    # b. Unir para obtener provincia
    df = pd.merge(df_ship_delivered, df_orders_ref, on='order_id', how='left')
    df = pd.merge(df, df_dim_address_ref, left_on='shipping_address_id', right_on='address_id', how='left')
    
    # Esta fact no necesita unirse a dim_date, ya que su métrica es una duración
    facts['fact_shipments'] = df

    print(f"  -> {len(facts)} Tablas de Hechos creadas.")
    return facts
