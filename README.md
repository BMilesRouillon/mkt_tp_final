# Trabajo Práctico Final — Introducción al Marketing Online y los Negocios Digitales

Repositorio del trabajo práctico final de la materia.

**Consigna y documento principal:** [Trabajo Práctico Final](https://docs.google.com/document/d/15RNP3FVqLjO4jzh80AAkK6mUR5DOLqPxLjQxqvdzrYg/edit?usp=sharing)
**Diagrama Entidad Relación (OLTP):** [DER](./assets/DER.png)


**[➡️ Ver el Modelo de Datos en Power BI ()]()**

---

## 📌 Contexto del Proyecto

Este repositorio contiene la solución completa al **Trabajo Práctico Final** de la materia **"Introducción al Marketing Online y los Negocios Digitales"**.

> **🎯 Objetivo de la Consigna:** Diseñar e implementar un mini-ecosistema de datos comercial (online + offline) y construir un dashboard que sirva como reporte para un área comercial, con KPIs clave: Ventas, Usuarios Activos, Ticket Promedio, NPS, Ventas por Provincia y Ranking Mensual por Producto.

### Desarrollo y Origen de Datos

El pipeline **ETL (Extract, Transform, Load)** se desarrolló en `Python 🐍` y `Pandas`, siguiendo una arquitectura modular (`e/`, `t/`, `l/`) que se orquesta desde el script `scripts/run_pipeline.py`.

El proceso utiliza los 13 archivos `.csv` de datos crudos (ventas, clientes, sesiones, etc.) provistos por la cátedra, los cuales se encuentran en el siguiente repositorio base:

* 📦 **Repositorio de Datos Crudos:** `https://github.com/Augusto Carmona/mkt_tp_final`


---
## ⚙️ Instrucciones de Ejecución Local

Sigue estos pasos para ejecutar el pipeline ETL en tu máquina local.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/BMilesRouillon/mkt_tp_final.git](https://github.com/BMilesRouillon/mkt_tp_final.git)
    cd mkt_tp_final
    ```

2.  **Crear el Entorno Virtual:**
    ```bash
    python -m venv .venv
    ```

3.  **Activar el Entorno Virtual:**
    * En Windows (PowerShell):
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```
    * En macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **Instalar las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ejecutar el Pipeline ETL:**
    El orquestador `run_pipeline.py` se encargará de llamar a los scripts de `e`, `t` y `l` en el orden correcto.
    ```bash
    python scripts/run_pipeline.py
    ```

6.  **Verificar la Salida:**
    Revisa la carpeta `DW/`. Ahora debería contener todas las tablas de dimensiones y hechos (14 archivos `.csv`) listas para ser importadas en Power BI.

---


## ⭐ Modelo de Datos: Esquema Estrella

El Data Warehouse está modelado como un Esquema Estrella. Las tablas de dimensiones (DIM) rodean a las tablas de hechos (FACT).



## 📚 Diccionario de Datos

El Data Warehouse (`DW/`) se compone de 13 tablas: 7 Dimensiones y 6 Hechos.

### Tablas de Dimensiones (DIM)

#### `dim_date`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `date_key` | `INT` | **PK** - Clave única (Ej: 20240115) |
| `full_date` | `DATE` | Fecha completa (Ej: 2024-01-15) |
| `year` | `INT` | Año (Ej: 2024) |
| `quarter` | `INT` | Trimestre (Ej: 1) |
| `month` | `INT` | Mes (Ej: 1) |
| `month_name` | `VARCHAR` | Nombre del mes (Ej: Enero) |
| `day` | `INT` | Día del mes (Ej: 15) |
| `day_of_week` | `INT` | Día de la semana (Lunes=0, Domingo=6) |
| `day_name` | `VARCHAR` | Nombre del día (Ej: Lunes) |

#### `dim_channel`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `channel_id` | `INT` | **PK** - Identificador único del canal. |
| `code` | `VARCHAR` | Código del canal (Ej: 'online', 'retail') |
| `name` | `VARCHAR` | Nombre del canal (Ej: Tienda Online) |

#### `dim_province`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `province_id` | `INT` | **PK** - Identificador único de la provincia. |
| `province_name` | `VARCHAR` | Nombre de la provincia (Ej: Córdoba) |
| `code` | `VARCHAR` | Código de la provincia (Ej: AR-X) |

#### `dim_customer`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `customer_id` | `INT` | **PK** - Identificador único del cliente. |
| `email` | `VARCHAR` | Email del cliente. |
| `first_name` | `VARCHAR` | Nombre del cliente. |
| `last_name` | `VARCHAR` | Apellido del cliente. |
| `phone` | `VARCHAR` | Teléfono del cliente. |
| `status` | `VARCHAR` | Estado de la cuenta (Ej: 'active') |
| `created_at` | `DATETIME` | Fecha de alta del cliente. |

#### `dim_product`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `product_id` | `INT` | **PK** - Identificador único del producto. |
| `sku` | `VARCHAR` | Código SKU del producto. |
| `product_name` | `VARCHAR` | Nombre del producto. |
| `list_price` | `DECIMAL` | Precio de lista. |
| `status` | `VARCHAR` | Estado del producto (Ej: 'published') |
| `created_at` | `DATETIME` | Fecha de creación del producto. |
| `category_id` | `INT` | ID de la categoría (denormalizado). |
| `category_name` | `VARCHAR` | Nombre de la categoría (denormalizado). |
| `parent_id` | `INT` | ID de la categoría padre (nullable). |

#### `dim_address`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `address_id` | `INT` | **PK** - Identificador único de la dirección. |
| `line1` | `VARCHAR` | Calle y número. |
| `line2` | `VARCHAR` | Piso, departamento, etc. (nullable). |
| `city` | `VARCHAR` | Ciudad. |
| `province_id` | `INT` | **FK** - Llave a `dim_province`. |
| `province_name` | `VARCHAR` | Nombre de la provincia (denormalizado). |
| `postal_code` | `VARCHAR` | Código postal. |
| `country_code` | `VARCHAR` | Código de país (Ej: AR). |
| `created_at` | `DATETIME` | Fecha de creación de la dirección. |

#### `dim_store`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `store_id` | `INT` | **PK** - Identificador único de la tienda. |
| `store_name` | `VARCHAR` | Nombre de la tienda (Ej: Tienda Palermo). |
| `address_id` | `INT` | **FK** - Llave a `dim_address`. |
| `line1` | `VARCHAR` | Dirección (denormalizada). |
| `line2` | `VARCHAR` | Dirección (denormalizada, nullable). |
| `city` | `VARCHAR` | Ciudad (denormalizada). |
| `province_id` | `INT` | Provincia ID (denormalizada). |
| `province_name` | `VARCHAR` | Provincia (denormalizada). |
| `postal_code` | `VARCHAR` | Código postal (denormalizado). |
| `country_code` | `VARCHAR` | País (denormalizado). |

---

### Tablas de Hechos (FACT)

#### `fact_sales_order`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `order_id` | `BIGINT` | **PK** - Identificador único de la orden. |
| `customer_id` | `INT` | **FK** - Llave a `dim_customer`. |
| `channel_id` | `INT` | **FK** - Llave a `dim_channel`. |
| `store_id` | `INT` | **FK** - Llave a `dim_store` (nullable). |
| `shipping_address_id` | `INT` | **FK** - Llave a `dim_address`. |
| `billing_address_id` | `INT` | **FK** - Llave a `dim_address`. |
| `date_key` | `INT` | **FK** - Llave a `dim_date` (fecha de la orden). |
| `status` | `VARCHAR` | Estado (Ej: PAID, FULFILLED). |
| `subtotal` | `DECIMAL` | **Métrica** - Subtotal antes de imp/envío. |
| `tax_amount` | `DECIMAL` | **Métrica** - Monto de impuestos. |
| `shipping_fee` | `DECIMAL` | **Métrica** - Costo de envío. |
| `total_amount` | `DECIMAL` | **Métrica** - Monto total pagado. |

#### `fact_sales_order_item`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `order_item_id` | `BIGINT` | **PK** - Identificador único de la línea. |
| `order_id` | `BIGINT` | **FK** - Llave a `fact_sales_order`. |
| `product_id` | `INT` | **FK** - Llave a `dim_product`. |
| `date_key` | `INT` | **FK** - Llave a `dim_date`. |
| `quantity` | `INT` | **Métrica** - Cantidad de unidades. |
| `unit_price` | `DECIMAL` | **Métrica** - Precio unitario. |
| `discount_amount` | `DECIMAL` | **Métrica** - Descuento aplicado. |
| `line_total` | `DECIMAL` | **Métrica** - Total de la línea (cant * precio - desc). |

#### `fact_payment`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `payment_id` | `BIGINT` | **PK** - Identificador único del pago. |
| `order_id` | `BIGINT` | **FK** - Llave a `fact_sales_order`. |
| `date_key` | `INT` | **FK** - Llave a `dim_date`. |
| `method` | `VARCHAR` | Método de pago (Ej: credit_card). |
| `amount` | `DECIMAL` | **Métrica** - Monto de la transacción. |
| `status` | `VARCHAR` | Estado del pago (Ej: approved). |

#### `fact_shipment`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `shipment_id` | `BIGINT` | **PK** - Identificador único del envío. |
| `order_id` | `BIGINT` | **FK** - Llave a `fact_sales_order`. |
| `date_key` | `INT` | **FK** - Llave a `dim_date` (fecha de `shipped_at`). |
| `carrier` | `VARCHAR` | Transportista (Ej: Correo Argentino). |
| `tracking_number` | `VARCHAR` | Número de seguimiento (nullable). |
| `status` | `VARCHAR` | Estado del envío (Ej: DELIVERED). |
| `shipped_at` | `DATETIME` | Fecha y hora de despacho. |
| `delivered_at` | `DATETIME` | Fecha y hora de entrega. |
| `delivery_time_days` | `DECIMAL` | **Métrica** - Días de entrega (calculada). |

#### `fact_web_session`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `session_id` | `VARCHAR` | **PK** - Identificador único de la sesión. |
| `customer_id` | `INT` | **FK** - Llave a `dim_customer` (nullable). |
| `date_key` | `INT` | **FK** - Llave a `dim_date` (fecha de `started_at`). |
| `started_at` | `DATETIME` | Fecha y hora de inicio de sesión. |
| `ended_at` | `DATETIME` | Fecha y hora de fin de sesión. |
| `source` | `VARCHAR` | Fuente de tráfico (Ej: ads, direct). |
| `device` | `VARCHAR` | Dispositivo (Ej: mobile). |
| `session_duration_sec` | `DECIMAL` | **Métrica** - Duración de la sesión en seg (calculada). |

#### `fact_nps_response`
| Atributo | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `nps_id` | `BIGINT` | **PK** - Identificador único de la respuesta. |
| `customer_id` | `INT` | **FK** - Llave a `dim_customer`. |
| `channel_id` | `INT` | **FK** - Llave a `dim_channel`. |
| `date_key` | `INT` | **FK** - Llave a `dim_date` (fecha de `responded_at`). |
| `score` | `INT` | **Métrica** - Puntaje (0-10). |
| `nps_type` | `VARCHAR` | **Atributo Calc.** - (Promotor, Detractor, Neutro). |
| `comment` | `TEXT` | Comentario del cliente (nullable). |
| `responded_at` | `DATETIME` | Fecha y hora de la respuesta. |

## 🧠 Supuestos y Decisiones de Negocio

Durante la fase de `Transformación`, se tomaron las siguientes decisiones:

1.  **Órdenes Válidas:** Una "venta" (para `fact_sales_order`, `_item` y `_payment`) se considera válida solo si su estado en `sales_order.csv` es **`PAID`** o **`FULFILLED`**. Las órdenes `CANCELLED` o `REFUNDED` se excluyen de los KPIs de ventas.
2.  **Fecha de Venta:** La fecha que se usa para unir a `dim_date` en las tres tablas de ventas es la `order_date` de la cabecera del pedido.
3.  **Fecha de Envío:** La fecha que se usa para `fact_shipment` es la `shipped_at` (fecha de despacho).
4.  **Clasificación NPS:** El atributo `nps_type` se calcula siguiendo la regla estándar:
    * **Promotor:** Score 9 o 10.
    * **Detractor:** Score 0 a 6.
    * **Neutro:** Score 7 u 8.

## 🔑 Lógica de KPIs Clave

Esta tabla detalla la lógica de negocio y las medidas DAX principales utilizadas para construir el dashboard de Power BI, basadas en las 6 tablas de hechos de nuestro Data Warehouse.

| KPI (Indicador) | Icono | Lógica de Creación (Medida DAX) | Tabla de Hechos Base | Dimensiones Clave (Filtros) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Ventas ($M)** | 💰 | `SUM('fact_sales_order'[total_amount])` | `fact_sales_order` | `dim_date`, `dim_channel`, `dim_province` |
| **Ticket Promedio ($K)** | 💳 | `DIVIDE([Total Ventas], [Total Órdenes])` | `fact_sales_order` | `dim_date`, `dim_channel` |
| **Usuarios Activos (nK)** | 👥 | `DISTINCTCOUNT('fact_web_session'[customer_id])` | `fact_web_session` | `dim_date` (por fecha de sesión) |
| **NPS Score** | 🚀 | `DIVIDE(([Promotores] - [Detractores]), [Total Encuestas]) * 100` | `fact_nps_response` | `dim_date` (por fecha de respuesta), `dim_channel` |
| **Ranking Productos** | 🏆 | `SUM('fact_sales_order_item'[line_total])` | `fact_sales_order_item` | `dim_product` (Nombre), `dim_date` (Mes) |
| **Tiempo Entrega Prom.** | 🚚 | `AVERAGE('fact_shipment'[delivery_time_days])` | `fact_shipment` | `dim_date` (por fecha de envío), `dim_province` |

## Historial de Comandos de Consola

Toda la gestión del repositorio y la ejecución del pipeline se realizó a través de la consola de PowerShell. Los comandos clave utilizados fueron:

* **Configuración del Proyecto:**
    ```powershell
    git clone ...
    cd mkt_tp_final
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install pandas
    pip freeze > requirements.txt
    ```

* **Creación de Estructura ETL:**
    ```powershell
    mkdir scripts\extract
    mkdir scripts\transform
    mkdir scripts\load
    New-Item scripts\extract\__init__.py
    New-Item scripts\transform\__init__.py
    New-Item scripts\load\__init__.py
    New-Item scripts\extract\extractor.py
    New-Item scripts\transform\dimensions.py
    New-Item scripts\transform\facts.py
    New-Item scripts\load\loader.py
    New-Item scripts\run_pipeline.py
    ```

* **Ejecución del Pipeline:**
    ```powershell
    python scripts/run_pipeline.py
    ```

* **Gestión de Repositorio (Git):**
    ```powershell
    git add .
    git commit -m "..."
    git pull origin main
    git push origin main
    ```

* **Gestión de Documentación (README y Assets):**
    ```powershell
    ls raw
    Remove-Item ...
    Copy-Item ...
    Set-Content ...
    Add-Content ...



