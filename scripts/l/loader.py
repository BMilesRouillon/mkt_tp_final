import os
import pandas as pd

def load_data_to_dw(dims_dict, facts_dict, dw_dir):
    
    os.makedirs(dw_dir, exist_ok=True)
    
    all_data = {**dims_dict, **facts_dict}
    
    for table_name, df in all_data.items():
        output_path = os.path.join(dw_dir, f"{table_name}.csv")
        
        try:
            df = df.loc[:, ~df.columns.duplicated()]
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"     - {table_name}.csv guardado.")
        except Exception as e:
            print(f"     ERROR guardando {table_name}: {e}")
    
    print(" <i>Carga completada.")