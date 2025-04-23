import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(".env")

class DistFuelProv:
    ID = os.getenv("ID_DIST_FUEL_PROV")
    DATA_DICT = {
        "path": [
            os.getenv("PROV_COL_NAME"),
            os.getenv("FUEL_COL_NAME")
        ],
        "value": os.getenv("AREA_COL_NAME"),
        "color": os.getenv("FUEL_COL_NAME")
    }

    CHART_DICT = {
        "title": os.getenv("CHART_TITLE_DIST_FUEL_TYPE"),
        "hole": float(os.getenv("CHART_HOLE_DIST_FUEL_TYPE")),
        "height": 900,
        "width": 900,
    }

    def __str(self):
        return self.ID