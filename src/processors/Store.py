from .ProvFuelTypeLandAreaDataProcessor import ProvFuelTypeLandAreaDataProcessor
from .AfterFireFuelTypeGrowthProcessor import AfterFireFuelTypeGrowthProcessor

class Store:
    def __init__(self):
        self.__prov_processor = ProvFuelTypeLandAreaDataProcessor()
        self.__fire_processor = AfterFireFuelTypeGrowthProcessor()

        list_prov = self.__prov_processor.get_provs()
        list_prov = ["Canada"] + list_prov

        self.state = {
            "prov_fuel_type_data": self.__prov_processor.get_data(),
            "after_fire_growth_data": self.__fire_processor.get_data(),
            "prov_list": list_prov,
            "active_prov": list_prov[0],
        }

