
import os
import json
import pandas as pd
from dotenv import load_dotenv
from pandas.api.types import CategoricalDtype

class ProvFuelTypeLandAreaDataProcessor:
    
    def __init__(self):
        # load env
        load_dotenv(".env")

        self.__DATA_DIR = os.getenv('DATA_DIR')
        self.__FILE = os.getenv('FUEL_TYPE_LAND_AREA_PROV_CSV')
        self.__COLOR_MAP_FILE = os.getenv("FUEL_TYPE_COLOR_MAP_JSON")
        self.__COMBINATION_FILE = os.getenv("FUEL_TYPE_COMBINATION_JSON")
        
        self.PROV_COL_NAME = os.getenv('PROV_COL_NAME')
        self.FUEL_COL_NAME = os.getenv('FUEL_COL_NAME')
        self.COUNT_COL_NAME = os.getenv('COUNT_COL_NAME')
        self.AREA_COL_NAME = os.getenv('AREA_COL_NAME')

        self.FUEL_TYPE_WATER = os.getenv('FUEL_TYPE_WATER')

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
            self.COMBINATION_MAP = json.load(f)

    def __get_data_file_loc(self):
        return f"{self.__DATA_DIR}{os.sep}{self.__FILE}"
    
    def __get_fuel_color_map_file_loc(self):
        return f"{self.__DATA_DIR}{os.sep}{self.__COLOR_MAP_FILE}"
    
    def __get_fuel_combination_file_loc(self):
        return f"{self.__DATA_DIR}{os.sep}{self.__COMBINATION_FILE}"
    
    def __get_dataframe(self)->pd.DataFrame:
        return pd.read_csv(
            filepath_or_buffer = self.__get_data_file_loc()
        )
    
    def __make_col_categorical(self, df:pd.DataFrame, col:str)->pd.DataFrame:
        df[col] = df[col].astype(
            CategoricalDtype(
                categories = self.PROV_ORDER,
                ordered = True
            )
        )
        return df
    
    def __discard_col_value(self, df:pd.DataFrame, col:str, value:str)->pd.DataFrame:
        df = df[df[col] != value]
        return df
    
    def __convert_pixels_to_km_2(self, df:pd.DataFrame, count_col:str, new_col:str)->pd.DataFrame:
        df[new_col] = df[count_col] * 0.0009 # 30mx30m in km sq
                
        # drop pixel count col 
        df = self.__drop_column(
            df = df,
            col = count_col
        )

        return df

    def __drop_column(self, df:pd.DataFrame, col:str)->pd.DataFrame:
        df.drop(
            labels = col,
            axis = 1,
            inplace = True
        )
        return df
    
    def __grouper_sum(self, df:pd.DataFrame, col:str)->pd.DataFrame:
        return df.groupby(
            by = col,
            observed = False # for version issue
        ).sum().reset_index()

    def __merge_types(self, df:pd.DataFrame, type_col:str, other_cols:list, merge_map:dict)->pd.DataFrame:
        # combine the same groups
        for group in merge_map:
            # get index of new group
            new_group_df = df[
                df[type_col].isin(
                    merge_map[group]
                )
            ]

            # !!! this should be right after extracction of data and before index reset
            # drop the data 
            df.drop(
                new_group_df.index,
                inplace = True
            )

            # combine the same groups into one
            new_group_df = new_group_df.groupby(other_cols).sum().reset_index()

            # add the new fuel type name
            new_group_df[type_col] = group

            # add the combined data back
            df = pd.concat(
                [
                    df,
                    new_group_df
                ]
            )
        return df
    
    def __run_preprocessing(self)->None:
        # drop water data
        self.data_df = self.__discard_col_value(
            df = self.data_df,
            col = self.FUEL_COL_NAME,
            value = self.FUEL_TYPE_WATER
        )

        # merge same types
        self.data_df = self.__merge_types(
            df = self.data_df,
            type_col = self.FUEL_COL_NAME,
            other_cols = [self.PROV_COL_NAME],
            merge_map = self.COMBINATION_MAP
        )

        # covert pixels to sq km
        self.data_df = self.__convert_pixels_to_km_2(
            df = self.data_df,
            new_col = self.AREA_COL_NAME,
            count_col = self.COUNT_COL_NAME
        )

        # # categorize prov col
        # self.data_df = self.__make_col_categorical(
        #     df = self.data_df,
        #     col = self.PROV_COL_NAME
        # )

    def get_data(self)->pd.DataFrame:
        return self.data_df
    
    def get_provs(self)->list:
        return sorted(self.PROV_ORDER)

    def get_inner_ring_data(self)->pd.DataFrame:
        inner_ring_df = self.__grouper_sum(
            df = self.data_df,
            col = self.PROV_COL_NAME
        )

        inner_ring_df.drop(
            labels = self.FUEL_COL_NAME,
            axis = 1,
            inplace = True
        )

        inner_ring_df[self.PROV_COL_NAME] = inner_ring_df[self.PROV_COL_NAME].astype(
            CategoricalDtype(
                categories = self.PROV_ORDER,
                ordered = True
            )
        )

        inner_ring_df = inner_ring_df.sort_values(
            by = self.PROV_COL_NAME,
            ascending = True,
        )

        return inner_ring_df
