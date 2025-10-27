import os
import sys

# --- Configuración del Pipeline ---

# 1. Obtener la ruta del script actual (scripts/run_pipeline.py)
SCRIPT_PATH = os.path.abspath(__file__)
# Obtener el directorio que contiene el script (mkt_tp_final/scripts)
SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)
# Obtener el directorio raíz del proyecto (un nivel arriba, mkt_tp_final)
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 2. Añadimos la carpeta 'scripts' (SCRIPT_DIR) al path de Python
#    para que pueda encontrar los módulos (extract, transform, load)
sys.path.append(SCRIPT_DIR)

# 3. Ahora importamos nuestros módulos
from extract import extractor
from transform import dimensions
from transform import facts
from load import loader

# 4. Definición de Rutas Principales
#    (RAW_DIR y DW_DIR están en el PROJECT_DIR, un nivel arriba del script)
RAW_DIR = os.path.join(PROJECT_DIR, 'raw')
DW_DIR = os.path.join(PROJECT_DIR, 'DW')

def main():
    """
    Orquesta el pipeline ETL completo.
    """
    print("--- INICIANDO PIPELINE ETL ---")
    
    # 1. EXTRACT
    print("\n[1/3] Extrayendo datos de RAW...")
    raw_data = extractor.get_raw_data(RAW_DIR)
    if raw_data is None:
        print("ERROR: Falló la extracción. Abortando.")
        return

    # 2. TRANSFORM
    print("\n[2/3] Transformando datos...")
    
    # 2a. Crear Dimensiones (incluye dim_date)
    transformed_dims = dimensions.transform_dimensions(raw_data)
    
    # 2b. Crear Hechos (usa raw_data y las dimensiones transformadas)
    transformed_facts = facts.transform_facts(raw_data, transformed_dims)
    
    print("  -> Transformación completada.")

    # 3. LOAD
    print("\n[3/3] Cargando datos al Data Warehouse (DW)...")
    
    # Combinamos todos los dataframes (dims y facts) en un solo dict para cargar
    all_data_to_load = {**transformed_dims, **transformed_facts}
    
    loader.load_data_to_dw(all_data_to_load, DW_DIR)
    
    print("\n--- PIPELINE ETL COMPLETADO EXITOSAMENTE ---")

if __name__ == "__main__":
    main()