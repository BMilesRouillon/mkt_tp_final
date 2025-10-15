## 1. Modelo de Datos — Esquema Estrella Kimball 🧠

Para cumplir con los objetivos de análisis, se diseñó un Data Warehouse con una **arquitectura de bus de datos**. Este modelo se representa a continuación con un esquema estrella separado para cada proceso de negocio, garantizando la claridad y consistencia del análisis.

### Diagrama Visual del Modelo

#### Esquema 1: Ventas (Sales)
```mermaid
   erDiagram
    %% --- Título y Estilos para el Diagrama de Ventas ---
    accTitle: Esquema Estrella de Ventas
    classDef fact fill:#F2C279,stroke:#b88b4a,stroke-width:2px,color:black
    classDef dimConformed fill:#85C1E9,stroke:#5288ad,stroke-width:2px,color:black
    classDef dimPrivate fill:#A3E4D7,stroke:#66a195,stroke-width:2px,color:black

    %% --- Tablas ---
    FACT_SALES {
        int date_key FK
        int customer_key FK
        int product_key FK
        int channel_key FK
        int store_key FK
        int settlement_key FK
        bigint order_id DD
    }
    DIM_DATE { int date_key PK; date full_date }
    DIM_CUSTOMER { int customer_key PK; varchar full_name }
    DIM_CHANNEL { int channel_key PK; varchar channel_name }
    DIM_PRODUCT { int product_key PK; varchar product_name }
    DIM_STORE { int store_key PK; varchar store_name }
    DIM_SETTLEMENT { int settlement_key PK; varchar center_name }

    %% --- Relaciones ---
    FACT_SALES }o--|| DIM_DATE : "fecha"
    FACT_SALES }o--|| DIM_CUSTOMER : "cliente"
    FACT_SALES }o--|| DIM_PRODUCT : "producto"
    FACT_SALES }o--|| DIM_CHANNEL : "canal"
    FACT_SALES }o--|| DIM_STORE : "tienda"
    FACT_SALES }o--|| DIM_SETTLEMENT : "despacho"

    %% --- Aplicar Estilos ---
    class FACT_SALES fact
    class DIM_DATE,DIM_CUSTOMER,DIM_CHANNEL dimConformed
    class DIM_PRODUCT,DIM_STORE,DIM_SETTLEMENT dimPrivate
```

#### Esquema 2: Encuestas NPS
```mermaid
   erDiagram
    %% --- Título y Estilos para el Diagrama de NPS ---
    accTitle: Esquema Estrella de NPS
    classDef fact fill:#F2C279,stroke:#b88b4a,stroke-width:2px,color:black
    classDef dimConformed fill:#85C1E9,stroke:#5288ad,stroke-width:2px,color:black

    %% --- Tablas ---
    FACT_NPS_RESPONSES {
        int date_key FK
        int customer_key FK
        int channel_key FK
        smallint nps_score
    }
    DIM_DATE { int date_key PK; date full_date }
    DIM_CUSTOMER { int customer_key PK; varchar full_name }
    DIM_CHANNEL { int channel_key PK; varchar channel_name }

    %% --- Relaciones ---
    FACT_NPS_RESPONSES }o--|| DIM_DATE : "fecha"
    FACT_NPS_RESPONSES }o--|| DIM_CUSTOMER : "cliente"
    FACT_NPS_RESPONSES }o--|| DIM_CHANNEL : "canal"

    %% --- Aplicar Estilos ---
    class FACT_NPS_RESPONSES fact
    class DIM_DATE,DIM_CUSTOMER,DIM_CHANNEL dimConformed
```

#### Esquema 3: Sesiones Web
```mermaid
   erDiagram
    %% --- Título y Estilos para el Diagrama de Sesiones Web ---
    accTitle: Esquema Estrella de Sesiones Web
    classDef fact fill:#F2C279,stroke:#b88b4a,stroke-width:2px,color:black
    classDef dimConformed fill:#85C1E9,stroke:#5288ad,stroke-width:2px,color:black

    %% --- Tablas ---
    FACT_WEB_SESSIONS {
        int date_key FK
        int customer_key FK
        int session_count
    }
    DIM_DATE { int date_key PK; date full_date }
    DIM_CUSTOMER { int customer_key PK; varchar full_name }

    %% --- Relaciones ---
    FACT_WEB_SESSIONS }o--|| DIM_DATE : "fecha"
    FACT_WEB_SESSIONS }o--|| DIM_CUSTOMER : "cliente"

    %% --- Aplicar Estilos ---
    class FACT_WEB_SESSIONS fact
    class DIM_DATE,DIM_CUSTOMER dimConformed
```