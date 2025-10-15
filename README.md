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
graph TD
    subgraph "Hechos (Métricas)"
        F1[FACT_SALES]
        F2[FACT_NPS_RESPONSES]
        F3[FACT_WEB_SESSIONS]
    end

    subgraph "Dimensiones Conformadas (Compartidas)"
        D1[DIM_DATE]
        D2[DIM_CUSTOMER]
        D3[DIM_CHANNEL]
    end

    subgraph "Dimensiones Privadas (Solo para Ventas)"
        D4[DIM_PRODUCT]
        D5[DIM_STORE]
        D6[DIM_SETTLEMENT]
    end

    F1 -- date_key --> D1
    F1 -- customer_key --> D2
    F1 -- channel_key --> D3
    F1 -- product_key --> D4
    F1 -- store_key --> D5
    F1 -- settlement_key --> D6

    F2 -- date_key --> D1
    F2 -- customer_key --> D2
    F2 -- channel_key --> D3

    F3 -- date_key --> D1
    F3 -- customer_key --> D2
