import os
import sys




SCRIPT_PATH = os.path.abspath(__file__)

SCRIPT_DIR = os.path.dirname(SCRIPT_PATH)

PROJECT_DIR = os.path.dirname(SCRIPT_DIR)


sys.path.append(SCRIPT_DIR)

from extract import extractor
from transform import dimensions
from transform import facts
from load import loader


RAW_DIR = os.path.join(PROJECT_DIR, 'raw')
DW_DIR = os.path.join(PROJECT_DIR, 'DW')

def main():
    print("\n[1/3] Extrayendo datos de RAW...")
    raw_data = extractor.get_raw_data(RAW_DIR)
    if raw_data is None:
        print("ERROR: Falló la extracción. Abortando.")
        return

    
    print("\n[2/3] Transformando datos...")
    
    
    transformed_dims = dimensions.transform_dimensions(raw_data)
    
    
    transformed_facts = facts.transform_facts(raw_data, transformed_dims)
    
    print("  -> Transformación completada.")

    
    print("\n[3/3] Cargando datos al Data Warehouse (DW)...")
    
    
    all_data_to_load = {**transformed_dims, **transformed_facts}
    
    loader.load_data_to_dw(all_data_to_load, DW_DIR)
    
    print("\n--- PIPELINE ETL COMPLETADO EXITOSAMENTE ---")

if __name__ == "__main__":
    main()