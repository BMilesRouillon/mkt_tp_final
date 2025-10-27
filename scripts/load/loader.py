import os

def load_data_to_dw(data_dict, dw_dir):
    """
    Guarda todos los dataframes (dimensiones y hechos) como CSV
    en la carpeta DW, usando encoding UTF-8.
    """
    print("  -> Guardando archivos en DW/...")
    
    # Asegurarnos de que la carpeta DW exista
    os.makedirs(dw_dir, exist_ok=True)
    
    for file_name, df in data_dict.items():
        output_path = os.path.join(dw_dir, f"{file_name}.csv")
        try:
            # Seleccionamos solo las columnas que no son duplicadas (por los joins)
            df = df.loc[:, ~df.columns.duplicated()]
            # Guardamos
            df.to_csv(output_path, index=False, encoding='utf-8')
            print(f"    - {file_name}.csv guardado.")
        except Exception as e:
            print(f"    ERROR guardando {file_name}: {e}")
    
    print("  -> Carga completada.")