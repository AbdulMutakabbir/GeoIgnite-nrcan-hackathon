from .ProvFuelTypeLandAreaDataProcessor import ProvFuelTypeLandAreaDataProcessor
from .AfterFireFuelTypeGrowthProcessor import AfterFireFuelTypeGrowthProcessor
import os
from dotenv import load_dotenv

class Store:
    def __init__(self):
        # load env
        load_dotenv(".env")

        self.ALL_PROV_VAL = os.getenv("ALL_PROV_DATA_VAL")

        self.__prov_processor = ProvFuelTypeLandAreaDataProcessor()
        self.__fire_processor = AfterFireFuelTypeGrowthProcessor()

        list_prov = self.__prov_processor.get_provs()
        list_prov = [self.ALL_PROV_VAL] + list_prov

        self.state = {
            "prov_fuel_type_data": self.__prov_processor.get_data(),
            "percent_grown_after_fire_data": self.__fire_processor.get_percentage_data(prov = self.ALL_PROV_VAL),
            "area_grown_after_fire_data":self.__fire_processor.get_area_data(prov = self.ALL_PROV_VAL),
            "prov_list": list_prov,
            "active_prov": self.ALL_PROV_VAL,
            "color_map": self.__fire_processor.get_color_map()
        }

        del list_prov

    def set_active_prov(self, prov)->None:
        if prov in self.state["prov_list"]:
            self.state["active_prov"] = prov
            self.__updated_prov_specific_data()

    def __updated_prov_specific_data(self)->None:
        self.state['percent_grown_after_fire_data'] = self.__fire_processor.get_percentage_data(prov = self.state["active_prov"])
        self.state['area_grown_after_fire_data'] = self.__fire_processor.get_area_data(prov = self.state["active_prov"])
