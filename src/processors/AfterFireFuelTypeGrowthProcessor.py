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

        self.FIRE_PROV_COL_NAME = os.getenv('FIRE_PROV_COL_NAME')
        self.FIRE_YEAR_COL_NAME = os.getenv('FIRE_YEAR_COL_NAME')

        self.FUEL_TYPE_WATER = os.getenv('FUEL_TYPE_WATER')

        self.ALL_PROV_VAL = os.getenv("ALL_PROV_DATA_VAL")

                # set order of prov
        self.PROV_ORDER = [
            'Yukon',
            'NorthWest Territories',
            'Nunavut',
            'British Columbia',
            'Alberta',
            'Saskatchewan',
            'Manitoba',
            'Quebec',
            'Ontario',
            'NewFoundLand and Labrador',
            'New Brunswick',
            'Nova Scotia',
            'Prince Edward Islands',
        ]

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
    
    def __drop_column(self, df:pd.DataFrame, col:str|list)->pd.DataFrame:
        df.drop(
            labels = col,
            axis = 1,
            inplace = True
        )
        return df
    
    def __merge_types(self, df:pd.DataFrame, merge_map:dict)->pd.DataFrame:
        # combine the same groups
        for cobined_type in merge_map:
            fusion_columns = merge_map[cobined_type]
            # merge the data
            df[cobined_type] = df[fusion_columns].sum(
                axis = 1
            )

            # deleted the old columns
            df = self.__drop_column(
                df = df,
                col = fusion_columns
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

        # merge same types
        self.data_df = self.__merge_types(
            df = self.data_df,
            merge_map = self.__COMBINATION_MAP
        )

    def get_data(self)->pd.DataFrame:
        return self.data_df
    
    def get_percentage_data(self, prov:str):
        # set default prov val
        if prov is None:
            prov = self.ALL_PROV_VAL

        # init df
        percentage_df = pd.DataFrame()

        # provess prov data
        if prov == self.ALL_PROV_VAL:
            # group by year
            percentage_df = self.data_df.groupby(
                by = self.FIRE_YEAR_COL_NAME
            ).sum()

        elif prov in self.PROV_ORDER:
            # filter to only the specific prov and set index to year
            percentage_df = self.data_df[self.data_df[self.FIRE_PROV_COL_NAME] == prov].set_index(
                self.FIRE_YEAR_COL_NAME
            )
        else:
            raise ValueError("Not a valid Provience value")
        
        # drop prov col
        percentage_df = self.__drop_column(
            df = percentage_df,
            col = self.FIRE_PROV_COL_NAME
        )
        
        # calculate percentage
        percentage_df = percentage_df.div(
            percentage_df.sum(axis=1),
            axis = 0
        ) * 100

        # reset index to include year
        percentage_df = percentage_df.reset_index()
        
        return percentage_df

    def get_area_data(self, prov:str):
        # set default prov val
        if prov is None:
            prov = self.ALL_PROV_VAL

        # init df
        area_df = pd.DataFrame()

        # provess prov data
        if prov == self.ALL_PROV_VAL:
            # group by year
            area_df = self.data_df.groupby(
                by = self.FIRE_YEAR_COL_NAME
            ).sum()
        elif prov in self.PROV_ORDER:
            # filter to only the specific prov and set index to year
            area_df = self.data_df[self.data_df[self.FIRE_PROV_COL_NAME] == prov].set_index(
                self.FIRE_YEAR_COL_NAME
            )
        else:
            raise ValueError("Not a valid Provience value")
        
        # drop prov col
        area_df = self.__drop_column(
            df = area_df,
            col = self.FIRE_PROV_COL_NAME
        )
        
        ## set units to km sq
        area_df = area_df * 0.0009

        # reset index to include year
        area_df = area_df.reset_index()
        
        return area_df