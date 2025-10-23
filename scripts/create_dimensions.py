import pandas as pd
import os

# --- Configuración de Rutas a prueba de errores ---

# Obtener la ruta absoluta del script que se está ejecutando (ej. .../scripts/create_dimensions.py)
SCRIPT_PATH = os.path.abspath(__file__)

# Obtener el directorio que contiene el script (ej. .../scripts)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

# Obtener el directorio raíz del proyecto (un nivel arriba de 'scripts', ej. .../mkt_tp_final)
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Definimos las rutas a las carpetas 'raw' y 'DW' basándonos en tu estructura
RAW_DIR = os.path.join(PROJECT_DIR, 'raw')  # Carpeta 'raw' en minúscula
DW_DIR = os.path.join(PROJECT_DIR, 'DW')    # Carpeta 'DW' en mayúscula

# --- Funciones de Dimensiones ---

def create_dim_channel():
    """
    Crea la dimensión de Canales a partir de raw/channel.csv [cite: 58-61]
    """
    print("Creando dim_channel...")
    file_path = os.path.join(RAW_DIR, 'channel.csv') 
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo en {file_path}")
        return

    df = df.rename(columns={'code': 'channel_code', 'name': 'channel_name'})
    
    output_path = os.path.join(DW_DIR, 'dim_channel.csv')
    df.to_csv(output_path, index=False)
    print(f"-> dim_channel.csv guardado en {DW_DIR}")

def create_dim_province():
    """
    Crea la dimensión de Provincias a partir de raw/province.csv [cite: 62-65]
    """
    print("Creando dim_province...")
    file_path = os.path.join(RAW_DIR, 'province.csv')
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo en {file_path}")
        return

    df = df.rename(columns={'name': 'province_name'})
    if 'code' in df.columns:
        df = df.drop(columns=['code'])
        
    output_path = os.path.join(DW_DIR, 'dim_province.csv')
    df.to_csv(output_path, index=False)
    print(f"-> dim_province.csv guardado en {DW_DIR}")

def create_dim_product():
    """
    Crea la dimensión de Productos, uniendo product y product_category [cite: 67-73, 96-104]
    """
    print("Creando dim_product...")
    try:
        df_prod = pd.read_csv(os.path.join(RAW_DIR, 'product.csv'))
        df_cat = pd.read_csv(os.path.join(RAW_DIR, 'product_category.csv'))
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró un archivo de producto: {e}")
        return

    df_cat = df_cat.rename(columns={'name': 'category_name'})
    df = pd.merge(df_prod, df_cat, on='category_id', how='left')
    
    # Seleccionamos columnas de la consigna
    df = df[['product_id', 'sku', 'name', 'list_price', 'status', 'category_name']]
    df = df.rename(columns={'name': 'product_name'})
    
    output_path = os.path.join(DW_DIR, 'dim_product.csv')
    df.to_csv(output_path, index=False)
    print(f"-> dim_product.csv guardado en {DW_DIR}")

def create_dim_customer():
    """
    Crea la dimensión de Clientes desde customer.csv [cite: 74-81]
    """
    print("Creando dim_customer...")
    file_path = os.path.join(RAW_DIR, 'customer.csv')
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo en {file_path}")
        return
    
    # Seleccionamos columnas de la consigna
    df = df[['customer_id', 'email', 'first_name', 'last_name', 'status', 'created_at']]
    
    output_path = os.path.join(DW_DIR, 'dim_customer.csv')
    df.to_csv(output_path, index=False)
    print(f"-> dim_customer.csv guardado en {DW_DIR}")

def create_dim_store():
    """
    Crea la dimensión de Tiendas, uniendo store, address y province [cite: 91-95, 82-90, 62-65]
    """
    print("Creando dim_store...")
    try:
        df_store = pd.read_csv(os.path.join(RAW_DIR, 'store.csv'))
        df_addr = pd.read_csv(os.path.join(RAW_DIR, 'address.csv'))
        df_prov = pd.read_csv(os.path.join(RAW_DIR, 'province.csv'))
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró un archivo de tienda/dirección: {e}")
        return

    df_prov = df_prov.rename(columns={'name': 'province_name'})
    
    # Unimos store con address
    df = pd.merge(df_store, df_addr, on='address_id', how='left')
    # Unimos el resultado con province
    df = pd.merge(df, df_prov, on='province_id', how='left')
    
    # Seleccionamos columnas de la consigna
    df = df[['store_id', 'name', 'line1', 'city', 'province_name', 'postal_code']]
    df = df.rename(columns={'name': 'store_name', 'line1': 'address_line'})
    
    output_path = os.path.join(DW_DIR, 'dim_store.csv')
    df.to_csv(output_path, index=False)
    print(f"-> dim_store.csv guardado en {DW_DIR}")

def create_dim_address():
    """
    Crea la dimensión de Direcciones, uniendo address y province [cite: 82-90, 62-65]
    """
    print("Creando dim_address...")
    try:
        df_addr = pd.read_csv(os.path.join(RAW_DIR, 'address.csv'))
        df_prov = pd.read_csv(os.path.join(RAW_DIR, 'province.csv'))
    except FileNotFoundError as e:
        print(f"ERROR: No se encontró un archivo de dirección/provincia: {e}")
        return
    
    df_prov = df_prov.rename(columns={'name': 'province_name'})
    
    # Unimos address con province
    df = pd.merge(df_addr, df_prov, on='province_id', how='left')
    
    # Seleccionamos columnas de la consigna
    df = df[['address_id', 'line1', 'city', 'province_id', 'province_name', 'postal_code']]
    
    output_path = os.path.join(DW_DIR, 'dim_address.csv')
    df.to_csv(output_path, index=False)
    print(f"-> dim_address.csv guardado en {DW_DIR}")


# --- Función Principal ---
def main():
    """
    Función principal que ejecuta la creación de todas las dimensiones.
    """
    print("--- Iniciando creación de Dimensiones ---")
    
    # Asegurarnos de que la carpeta DW exista
    os.makedirs(DW_DIR, exist_ok=True)
    
    # Ejecutar la creación de cada dimensión
    create_dim_channel()
    create_dim_province()
    create_dim_product()
    create_dim_customer()
    create_dim_store()
    create_dim_address()
    
    print("\n¡Todas las dimensiones fueron creadas exitosamente!")

if __name__ == "__main__":
    main()