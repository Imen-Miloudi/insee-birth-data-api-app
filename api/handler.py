import requests
import pandas as pd


class ApiHandler:

    def __init__(self):
        self.url = "https://api.insee.fr/melodi/data/DS_EC_NAIS"

        self.params = {
            "FREQ": "M",
            "EC_MEASURE": "LVB",
            "GEO": "DEP"
        }

        self.df = self.create_df_from_api_insee()

    def get_data_from_api_insee(self):
        response = requests.get(
            self.url,
            params=self.params
        )

        response.raise_for_status()

        return response.json()

    def create_df_from_api_insee(self):
        data = self.get_data_from_api_insee()

        observations = data["observations"]

        df = pd.DataFrame([
            {
                "department": observation["dimensions"]["GEO"],
                "period": observation["dimensions"]["TIME_PERIOD"],
                "births": observation["measures"]["OBS_VALUE_NIVEAU"]["value"]
            }
            for observation in observations
        ])

        return df

    def get_departments(self):
        return sorted(self.df["department"].unique().tolist())

    def get_births_by_department(self, dep):
        return self.df[self.df["department"] == f"2025-DEP-{dep}"].to_dict(orient="records")

    def get_births_by_department_and_month(self, dep, mois):
        df_result = self.df[
            (self.df["department"] == f"2025-DEP-{dep}")
            & (self.df["period"] == mois)
        ]

        if df_result.empty:
            return None

        row = df_result.iloc[0]

        return {
            "department": row["department"],
            "period": row["period"],
            "births": row["births"]
        }