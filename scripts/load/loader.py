import os

def load_data_to_dw(data_dict, dw_dir):
   
    os.makedirs(dw_dir, exist_ok=True)
    
    for file_name, df in data_dict.items():
        output_path = os.path.join(dw_dir, f"{file_name}.csv")
        try:
            df = df.loc[:, ~df.columns.duplicated()]
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"    - {file_name}.csv guardado.")
        except Exception as e:
            print(f"    ERROR guardando {file_name}: {e}")
    
    print("  -> Carga completada.")