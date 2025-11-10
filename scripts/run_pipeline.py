import os
import sys
import pandas as pd
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(SCRIPT_DIR)
from e.extractor import get_raw_data
from t import dimensions as dims
from t import facts as f
from l.loader import load_data_to_dw
RAW_DIR = os.path.join(PROJECT_DIR, 'RAW')
DW_DIR = os.path.join(PROJECT_DIR, 'DW')
def main():
    print("\n[1/3] Extrayendo datos de RAW...")
    raw_data = get_raw_data(RAW_DIR)
    if raw_data is None:
        print("ERROR: Falló la extracción. Abortando.")
        return

    dims_dict = {}
    dims_dict['dim_date'] = dims.create_dim_date(raw_data)
    dims_dict['dim_channel'] = dims.create_dim_channel(raw_data)
    dims_dict['dim_province'] = dims.create_dim_province(raw_data)
    dims_dict['dim_customer'] = dims.create_dim_customer(raw_data)
    dims_dict['dim_product'] = dims.create_dim_product(raw_data)
    dims_dict['dim_address'] = dims.create_dim_address(raw_data, dims_dict['dim_province'])
    dims_dict['dim_store'] = dims.create_dim_store(raw_data, dims_dict['dim_address'])

    facts_dict = {}

    dim_date_lookup = dims_dict['dim_date'][['date_key', 'full_date']].copy()
    dim_date_lookup['full_date_dt'] = pd.to_datetime(dim_date_lookup['full_date']).dt.date
    df_orders_all = raw_data['sales_order'].copy()
    df_orders_all['order_date_dt'] = pd.to_datetime(df_orders_all['order_date']).dt.date
    facts_dict['fact_sales_order'] = f.create_fact_sales_order(df_orders_all, dim_date_lookup)
    facts_dict['fact_sales_order_item'] = f.create_fact_sales_order_item(raw_data, df_orders_all, dim_date_lookup)
    facts_dict['fact_payment'] = f.create_fact_payment(raw_data, df_orders_all, dim_date_lookup)
    facts_dict['fact_shipment'] = f.create_fact_shipment(raw_data, dim_date_lookup)
    facts_dict['fact_web_session'] = f.create_fact_web_session(raw_data, dim_date_lookup)
    facts_dict['fact_nps_response'] = f.create_fact_nps_response(raw_data, dim_date_lookup)
    

    load_data_to_dw(dims_dict, facts_dict, DW_DIR)
    
    print("\n--- PIPELINE ETL COMPLETADO EXITOSAMENTE ---")

if __name__ == "__main__":
    main()
