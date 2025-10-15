# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación (Original):** [DER](./assets/DER.png)

---

## 1. Modelo de Datos — Esquema Estrella Kimball 🧠

Para cumplir con los objetivos de análisis, se diseñó un Data Warehouse con una **arquitectura de bus de datos** (o constelación de esquemas estrella). Este modelo cuenta con múltiples tablas de hechos que comparten dimensiones comunes (conformadas), lo que garantiza la consistencia al analizar KPIs de diferentes áreas del negocio.

### Diagrama Visual del Modelo (Mermaid)

Este diagrama representa la estructura final del Data Warehouse que se construirá con los scripts de Python.

```mermaid
erDiagram
    %% --- Tablas de Hechos (Métricas) ---
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

    FACT_NPS_RESPONSES {
        int date_key "FK"
        int customer_key "FK"
        int channel_key "FK"
        smallint nps_score
    }

    FACT_WEB_SESSIONS {
        int date_key "FK"
        int customer_key "FK"
        int session_count
    }

    %% --- Dimensiones (Contexto) ---
    DIM_DATE {
        int date_key "PK"
        date full_date
        varchar month_name
        int year_number
    }

    DIM_CUSTOMER {
        int customer_key "PK"
        int customer_id "NK"
        varchar full_name
        varchar email
    }

    DIM_CHANNEL {
        int channel_key "PK"
        int channel_id "NK"
        varchar channel_name
    }

    DIM_PRODUCT {
        int product_key "PK"
        int product_id "NK"
        varchar product_name
        varchar category_name
    }

    DIM_STORE {
        int store_key "PK"
        int store_id "NK"
        varchar store_name
        varchar province_name
    }

    DIM_SETTLEMENT {
        int settlement_key "PK"
        int settlement_id "NK"
        varchar center_name
    }

    %% --- Relaciones ---
    DIM_DATE ||--o{ FACT_SALES : "fecha"
    DIM_CUSTOMER ||--o{ FACT_SALES : "cliente"
    DIM_PRODUCT ||--o{ FACT_SALES : "producto"
    DIM_CHANNEL ||--o{ FACT_SALES : "canal"
    DIM_STORE ||--o{ FACT_SALES : "tienda"
    DIM_SETTLEMENT ||--o{ FACT_SALES : "despacho"

    DIM_DATE ||--o{ FACT_NPS_RESPONSES : "fecha"
    DIM_CUSTOMER ||--o{ FACT_NPS_RESPONSES : "cliente"
    DIM_CHANNEL ||--o{ FACT_NPS_RESPONSES : "canal"

    DIM_DATE ||--o{ FACT_WEB_SESSIONS : "fecha"
    DIM_CUSTOMER ||--o{ FACT_WEB_SESSIONS : "cliente"