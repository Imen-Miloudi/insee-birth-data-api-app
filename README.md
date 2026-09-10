# INSEE Birth Data — API & Interactive Application

> **Master 2 — Applied Mathematics, Statistics: Data Science**  
> Aix-Marseille University · 2026–2027

## Overview

This project consists of a **FastAPI REST API** and an interactive **Streamlit application** for exploring birth data from the French National Institute of Statistics and Economic Studies (**INSEE**).

The API retrieves and processes INSEE data, while the Streamlit application provides an interactive interface to explore the evolution of births by department.

## Project Architecture

```text
INSEE API
    │
    ▼
FastAPI REST API
    │
    ▼
Streamlit Application
    │
    ├── Department selection
    ├── Data table
    └── Interactive visualization
```

## Features

### FastAPI
- REST API for retrieving INSEE birth data by department and period
- Department management through `POST` and `PUT` endpoints
- Data validation with Pydantic

### Streamlit
- Interactive department selection
- Tabular data exploration
- Interactive time-series visualization with Plotly
- Data retrieval through the FastAPI API

## Data Processing

INSEE birth data are retrieved through the INSEE API and transformed into a structured Pandas DataFrame.

The application processes and sorts the data chronologically before displaying them through the Streamlit interface.

## Technologies

**Programming & Data:** Python · Pandas · Requests  
**API:** FastAPI · Pydantic  
**Visualization:** Streamlit · Plotly

## Project Structure

```text
insee-birth-data-api-app/
│
├── api/
│   ├── api.py
│   ├── handler.py
│   └── models.py
│
├── app/
│   ├── app.py
│   └── handler.py
│
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/departments` | Retrieve available departments |
| GET | `/births/{dep}` | Retrieve births by department |
| GET | `/births/{dep}/{mois}` | Retrieve births by department and period |
| POST | `/insert-department` | Add a department |
| PUT | `/update-department` | Update a department |

## Project Objective

This project combines **data acquisition, processing, REST API development and interactive visualization** in a complete Python application.
