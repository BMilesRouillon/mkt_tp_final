import pandas as pd
import os

# --- Configuración de Rutas a prueba de errores ---

# Obtener la ruta absoluta del script que se está ejecutando
SCRIPT_PATH = os.path.abspath(__file__)
# Obtener el directorio que contiene el script
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
# Obtener el directorio raíz del proyecto (un nivel arriba)
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Definimos las rutas a las carpetas 'raw' y 'DW'
RAW_DIR = os.path.join(PROJECT_DIR, 'raw')
DW_DIR = os.path.join(PROJECT_DIR, 'DW')

# --- Funciones de Hechos ---

def create_fact_sales():
    """
    Crea la tabla de hechos de ventas (la más importante).
    Une sales_order, sales_order_item, payment y dim_address.
    """
    print("Creando fact_sales...")
    
    try:
        # Leemos las tablas transaccionales
        df_orders = pd.read_csv(os.path.join(RAW_DIR, 'sales_order.csv'))
        df_items = pd.read_csv(os.path.join(RAW_DIR, 'sales_order_item.csv'))
        df_payments = pd.read_csv(os.path.join(RAW_DIR, 'payment.csv'))
        
        # Leemos la dimensión de direcciones que creamos
        df_dim_address = pd.read_csv(os.path.join(DW_DIR, 'dim_address.csv'))
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró un archivo base para fact_sales: {e}")
        return

    # --- 1. Preparar Pagos ---
    # Agrupamos para tener un solo método de pago por orden y sumar el total pagado.
    df_payments_agg = df_payments.groupby('order_id').agg(
        payment_method = pd.NamedAgg(column='method', aggfunc=lambda x: ', '.join(x.unique())),
        total_paid = pd.NamedAgg(column='amount', aggfunc='sum')
    ).reset_index()

    # --- 2. Filtrar Órdenes ---
    # [cite_start]La consigna pide solo órdenes 'PAID' o 'FULFILLED' para las ventas [cite: 180-181]
    valid_status = ['PAID', 'FULFILLED']
    df_orders_filtered = df_orders[df_orders['status'].isin(valid_status)].copy()
    
    # --- 3. Enriquecer Órdenes ---
    # Unimos las órdenes filtradas con sus ítems (INNER join)
    df_sales = pd.merge(df_orders_filtered, df_items, on='order_id', how='inner')
    
    # Unimos con los pagos agregados (LEFT join)
    df_sales = pd.merge(df_sales, df_payments_agg, on='order_id', how='left')
    
    # [cite_start]Unimos con dim_address usando 'shipping_address_id' para obtener la provincia [cite: 186]
    df_sales = pd.merge(
        df_sales, 
        df_dim_address[['address_id', 'province_id', 'province_name']], 
        left_on='shipping_address_id', 
        right_on='address_id', 
        how='left'
    )

    # --- 4. Extraer Fechas (ya que no usamos dim_date) ---
    df_sales['order_date'] = pd.to_datetime(df_sales['order_date'])
    df_sales['order_year'] = df_sales['order_date'].dt.year
    df_sales['order_month'] = df_sales['order_date'].dt.month
    df_sales['order_month_name'] = df_sales['order_date'].dt.strftime('%B')
    df_sales['order_date_only'] = df_sales['order_date'].dt.date # Para series temporales

    # --- 5. Seleccionar y Renombrar Columnas ---
    final_columns = [
        'order_id', 'order_item_id', 'customer_id', 'channel_id', 'store_id', 
        'product_id', 'shipping_address_id', 'province_id', 'quantity', 
        'unit_price', 'discount_amount', 'line_total', 'subtotal', 'tax_amount', 
        'shipping_fee', 'total_amount', 'total_paid', 'status', 'payment_method', 
        'province_name', 'order_date', 'order_year', 'order_month', 'order_month_name',
        'order_date_only'
    ]
    
    df_final = df_sales[[col for col in final_columns if col in df_sales.columns]]

    # Guardamos
    output_path = os.path.join(DW_DIR, 'fact_sales.csv')
    df_final.to_csv(output_path, index=False)
    print(f"-> fact_sales.csv guardado en {DW_DIR}")


def create_fact_sessions():
    """
    [cite_start]Crea la tabla de hechos de sesiones web para el KPI de Usuarios Activos [cite: 182-183]
    """
    print("Creando fact_sessions...")
    
    try:
        file_path = os.path.join(RAW_DIR, 'web_session.csv')
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró web_session.csv: {e}")
        return
    
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['session_date'] = df['started_at'].dt.date
    df['session_year'] = df['started_at'].dt.year
    df['session_month'] = df['started_at'].dt.month
    
    # [cite_start]Filtramos usuarios no nulos (la consigna dice COUNT(DISTINCT customer_id)) [cite: 182]
    df_cleaned = df[df['customer_id'].notna()].copy()
    df_cleaned['customer_id'] = df_cleaned['customer_id'].astype(int)
    
    df_final = df_cleaned[['session_id', 'customer_id', 'source', 'device', 'session_date', 'session_year', 'session_month']]
    
    output_path = os.path.join(DW_DIR, 'fact_sessions.csv')
    df_final.to_csv(output_path, index=False)
    print(f"-> fact_sessions.csv guardado en {DW_DIR}")

def create_fact_nps():
    """
    [cite_start]Crea la tabla de hechos de NPS [cite: 185]
    """
    print("Creando fact_nps...")
    
    try:
        file_path = os.path.join(RAW_DIR, 'nps_response.csv')
        df = pd.read_csv(file_path)
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró nps_response.csv: {e}")
        return
    
    df['responded_at'] = pd.to_datetime(df['responded_at'])
    df['response_date'] = df['responded_at'].dt.date
    df['response_year'] = df['responded_at'].dt.year
    df['response_month'] = df['responded_at'].dt.month
    
    # [cite_start]Clasificamos el score para el cálculo de NPS [cite: 185]
    def classify_nps(score):
        if score >= 9:
            return 'Promotor'
        elif score <= 6:
            return 'Detractor'
        else:
            return 'Neutro'
            
    df['nps_type'] = df['score'].apply(classify_nps)
    
    df_final = df[['nps_id', 'customer_id', 'channel_id', 'score', 'nps_type', 'response_date', 'response_year', 'response_month']]
    
    output_path = os.path.join(DW_DIR, 'fact_nps.csv')
    df_final.to_csv(output_path, index=False)
    print(f"-> fact_nps.csv guardado en {DW_DIR}")

def create_fact_shipments():
    """
    Crea la tabla de hechos de envíos.
    [cite_start]Clave para la meta del trimestre: "reducir tiempos de entrega en Mendoza" [cite: 56]
    """
    print("Creando fact_shipments...")
    
    try:
        df_ship = pd.read_csv(os.path.join(RAW_DIR, 'shipment.csv'))
        df_orders = pd.read_csv(os.path.join(RAW_DIR, 'sales_order.csv'))
        df_dim_address = pd.read_csv(os.path.join(DW_DIR, 'dim_address.csv'))
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró un archivo base para fact_shipments: {e}")
        return
    
    # [cite_start]Filtramos solo envíos que fueron entregados ('DELIVERED') [cite: 157]
    df_ship_delivered = df_ship[df_ship['status'] == 'DELIVERED'].copy()
    
    df_ship_delivered['shipped_at'] = pd.to_datetime(df_ship_delivered['shipped_at'])
    df_ship_delivered['delivered_at'] = pd.to_datetime(df_ship_delivered['delivered_at'])
    
    # --- 1. Calcular Métrica: Días de Entrega ---
    df_ship_delivered['delivery_time_days'] = (df_ship_delivered['delivered_at'] - df_ship_delivered['shipped_at']).dt.days
    
    # --- 2. Enriquecer con Provincia ---
    df_ship_final = pd.merge(
        df_ship_delivered,
        df_orders[['order_id', 'shipping_address_id']],
        on='order_id',
        how='left'
    )
    df_ship_final = pd.merge(
        df_ship_final,
        df_dim_address[['address_id', 'province_id', 'province_name']],
        left_on='shipping_address_id',
        right_on='address_id',
        how='left'
    )
    
    df_final = df_ship_final[[
        'shipment_id', 'order_id', 'carrier', 'shipping_address_id', 
        'province_id', 'province_name', 'delivery_time_days'
    ]]
    
    output_path = os.path.join(DW_DIR, 'fact_shipments.csv')
    df_final.to_csv(output_path, index=False)
    print(f"-> fact_shipments.csv guardado en {DW_DIR}")


# --- Función Principal ---
def main():
    """
    Función principal que ejecuta la creación de todas las tablas de Hechos.
    """
    print("--- Iniciando creación de Tablas de Hechos ---")
    
    os.makedirs(DW_DIR, exist_ok=True)
    
    create_fact_sales()
    create_fact_sessions()
    create_fact_nps()
    create_fact_shipments()
    
    print("\n¡Todas las tablas de Hechos fueron creadas exitosamente!")

if __name__ == "__main__":
    main()