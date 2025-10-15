# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación (Original):** [DER](./assets/DER.png)

---

## 1. Modelo de Datos — Esquema Estrella Kimball 🧠

Para cumplir con los objetivos de análisis, se diseñó un Data Warehouse con una **arquitectura de bus de datos** (o constelación de esquemas estrella). Este modelo cuenta con múltiples tablas de hechos que comparten dimensiones comunes (conformadas), lo que garantiza la consistencia al analizar KPIs de diferentes áreas del negocio.

```mermaid
%% ===================================================
%% DEFINICIÓN DE ESTILOS Y COLORES (APLICA A TODOS)
%% ===================================================
classDef fact fill:#F2C279,stroke:#b88b4a,stroke-width:2px;
classDef dimConformed fill:#85C1E9,stroke:#5288ad,stroke-width:2px;
classDef dimPrivate fill:#A3E4D7,stroke:#66a195,stroke-width:2px;

%% ===================================================
%% ESQUEMA 1: VENTAS (SALES)
%% ===================================================
erDiagram
    %% --- Título del Diagrama ---
    accTitle: Esquema Estrella de Ventas

    %% --- Tablas ---
    FACT_SALES {
        int date_key "FK"
        int customer_key "FK"
        int product_key "FK"
        int channel_key "FK"
        int store_key "FK"
        int settlement_key "FK"
        bigint order_id "DD"
        int quantity_sold
        decimal line_total
    }

    DIM_DATE {
        int date_key "PK"
        date full_date
    }

    DIM_CUSTOMER {
        int customer_key "PK"
        varchar full_name
    }

    DIM_CHANNEL {
        int channel_key "PK"
        varchar channel_name
    }

    DIM_PRODUCT {
        int product_key "PK"
        varchar product_name
    }

    DIM_STORE {
        int store_key "PK"
        varchar store_name
    }

    DIM_SETTLEMENT {
        int settlement_key "PK"
        varchar center_name
    }

    %% --- Relaciones ---
    DIM_DATE ||--o{ FACT_SALES : "relaciona"
    DIM_CUSTOMER ||--o{ FACT_SALES : "relaciona"
    DIM_CHANNEL ||--o{ FACT_SALES : "relaciona"
    DIM_PRODUCT ||--o{ FACT_SALES : "relaciona"
    DIM_STORE ||--o{ FACT_SALES : "relaciona"
    DIM_SETTLEMENT ||--o{ FACT_SALES : "relaciona"

    %% --- Aplicar Estilos ---
    class FACT_SALES fact;
    class DIM_DATE,DIM_CUSTOMER,DIM_CHANNEL dimConformed;
    class DIM_PRODUCT,DIM_STORE,DIM_SETTLEMENT dimPrivate;
```