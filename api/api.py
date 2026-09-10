from fastapi import FastAPI, HTTPException
from pathlib import Path
import csv

from .handler import ApiHandler
from .models import Department


app = FastAPI()

handler = ApiHandler()

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "departments.csv"


# --------------------------------------------------
# Endpoint /hello/{name}
# --------------------------------------------------

@app.get("/hello/{name}")
def hello(name: str) -> str:
    return f"Hello {name}"


# --------------------------------------------------
# Endpoint /departments
# --------------------------------------------------

@app.get("/departments")
def get_departments() -> list[str]:
    return handler.get_departments()


# --------------------------------------------------
# Endpoint /births/{dep}
# --------------------------------------------------

@app.get("/births/{dep}")
def get_births_by_department(dep: str) -> list[dict]:
    return handler.get_births_by_department(dep)


# --------------------------------------------------
# Endpoint /births/{dep}/{mois}
# --------------------------------------------------

@app.get("/births/{dep}/{mois}")
def get_births_by_department_and_month(
    dep: str,
    mois: str
) -> dict:

    result = handler.get_births_by_department_and_month(dep, mois)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Département ou période introuvable"
        )

    return result


# --------------------------------------------------
# Endpoint /insert-department
# --------------------------------------------------

@app.post("/insert-department")
def insert_department(department: Department):

    # Vérifier que le département existe dans les données INSEE
    departments = handler.get_departments()

    departments_numbers = [
        dep.split("-")[-1]
        for dep in departments
        if dep.split("-")[-1].isdigit()
    ]

    if str(department.department) not in departments_numbers:
        raise HTTPException(
            status_code=400,
            detail="Ce département n'existe pas"
        )

    # Vérifier si le fichier existe
    if not CSV_PATH.exists():

        with open(CSV_PATH, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["department", "checked"]
            )
            writer.writeheader()

    # Lire les départements déjà présents
    with open(CSV_PATH, "r", newline="") as file:

        reader = csv.DictReader(file)

        existing_departments = [
            int(row["department"])
            for row in reader
        ]

    # Vérifier si le département existe déjà
    if department.department in existing_departments:

        raise HTTPException(
            status_code=409,
            detail="Ce département existe déjà"
        )

    # Ajouter le département
    with open(CSV_PATH, "a", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["department", "checked"]
        )

        writer.writerow({
            "department": department.department,
            "checked": department.checked
        })

    return {
        "message": "Département ajouté",
        "department": department.department,
        "checked": department.checked
    }


# --------------------------------------------------
# Endpoint /update-department
# --------------------------------------------------

@app.put("/update-department")
def update_department(department: Department):

    if not CSV_PATH.exists():

        raise HTTPException(
            status_code=500,
            detail="Le fichier CSV n'existe pas"
        )

    # Vérifier que le département existe dans les données INSEE
    departments = handler.get_departments()

    departments_numbers = [
        dep.split("-")[-1]
        for dep in departments
        if dep.split("-")[-1].isdigit()
    ]

    if str(department.department) not in departments_numbers:
        raise HTTPException(
            status_code=400,
            detail="Ce département n'existe pas"
        )
    
    # Lire le fichier
    with open(CSV_PATH, "r", newline="") as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    # Chercher le département
    found = False

    for row in rows:

        if int(row["department"]) == department.department:

            row["checked"] = str(department.checked)
            found = True
            break

    # Département absent du CSV
    if not found:

        raise HTTPException(
            status_code=500,
            detail="Le département n'existe pas dans le fichier CSV"
        )

    # Réécrire le fichier
    with open(CSV_PATH, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["department", "checked"]
        )

        writer.writeheader()
        writer.writerows(rows)

    return {
        "message": "Département mis à jour",
        "department": department.department,
        "checked": department.checked
    }