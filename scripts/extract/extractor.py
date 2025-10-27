import pandas as pd
import os

def get_raw_data(raw_dir):
    """
    Lee todos los archivos CSV de la carpeta 'raw' y los devuelve en un diccionario
    de DataFrames, aplicando la corrección de encoding 'latin1'.
    """
    print("  -> Leyendo archivos RAW...")
    
    # Lista de todos los archivos que necesitamos del PDF
    files_to_read = [
        'address.csv', 'channel.csv', 'customer.csv', 'nps_response.csv',
        'payment.csv', 'product.csv', 'product_category.csv', 'province.csv',
        'sales_order.csv', 'sales_order_item.csv', 'shipment.csv',
        'store.csv', 'web_session.csv'
    ]
    
    dataframes = {}
    for file_name in files_to_read:
        file_key = file_name.replace('.csv', '') # ej. 'customer'
        file_path = os.path.join(raw_dir, file_name)
        
        try:
            dataframes[file_key] = pd.read_csv(file_path, encoding='latin1')
        except FileNotFoundError:
            print(f"    AVISO: No se encontró el archivo {file_name}")
            return None
        except Exception as e:
            print(f"    ERROR leyendo {file_name}: {e}")
            return None
    
    print(f"  -> {len(dataframes)} archivos RAW leídos correctamente.")
    return dataframes