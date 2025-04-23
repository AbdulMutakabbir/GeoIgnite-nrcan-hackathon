import os
import json 
import pandas as pd
from dotenv import load_dotenv

class AfterFireFuelTypeGrowthProcessor:
    def __init__(self):
        # load env
        load_dotenv(".env")
        
        self.__DATA_DIR = os.getenv('DATA_DIR')
        self.__FILE = os.getenv('AFTER_FIRE_FUEL_GROWTH_PROV_CSV')
        self.__COLOR_MAP_FILE = os.getenv("FUEL_TYPE_COLOR_MAP_JSON")
        self.__COMBINATION_FILE = os.getenv("FUEL_TYPE_COMBINATION_JSON")

        self.FUEL_TYPE_WATER = os.getenv('FUEL_TYPE_WATER')

        self.__init_color_map()
        self.__init_combination_map()

        # get data 
        self.data_df = self.__get_dataframe()

        # run preprocessing
        self.__run_preprocessing()

    def __init_color_map(self):
        with open(self.__get_fuel_color_map_file_loc(), "r") as f:
            self.__COLOR_MAP = json.load(f)

    def __init_combination_map(self):
        with open(self.__get_fuel_combination_file_loc(), "r") as f:
            self.__COMBINATION_MAP = json.load(f)

    def __get_data_file_loc(self):
        return f"{self.__DATA_DIR}{os.sep}{self.__FILE}"
    
    def __get_dataframe(self)->pd.DataFrame:
        return pd.read_csv(
            filepath_or_buffer = self.__get_data_file_loc()
        )
    
    def __drop_column(self, df:pd.DataFrame, col:str)->pd.DataFrame:
        df.drop(
            labels = col,
            axis = 1,
            inplace = True
        )
        return df
    
    def __get_fuel_color_map_file_loc(self):
        return f"{self.__DATA_DIR}{os.sep}{self.__COLOR_MAP_FILE}"
    
    def __get_fuel_combination_file_loc(self):
        return f"{self.__DATA_DIR}{os.sep}{self.__COMBINATION_FILE}"

    def __run_preprocessing(self)->None:
        # drop water data
        self.data_df = self.__drop_column(
            df = self.data_df,
            col = self.FUEL_TYPE_WATER
        )
        print(self.data_df.columns)

    def get_data(self)->pd.DataFrame:
        return self.data_df