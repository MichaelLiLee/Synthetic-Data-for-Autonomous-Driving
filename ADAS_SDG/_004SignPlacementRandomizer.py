""" SignPlacementRandomizer
"""
import bpy
import random
import numpy as np
import os
import glob

class SignPlacementRandomizer:
    def __init__(self):
        self.sign_collection = bpy.data.collections["SignCollection"]
        self.sign_asset_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/sign"
        self.sign_distance_range = {"min":10, "max":50}
        self.lane_length = 237
        self.sign_right_origin = [6, 0, 0]
        self.sign_location_offset_range = {"min":0,"max":7}
        self.sign_hight_range = {"min":150,"max":210}
        self.num_sign_need_import = 0

    def load_obj_from_blend_file(self,filepath,collection):
        """ 
        """ 
        ## append object from .blend file
        with bpy.data.libraries.load(filepath, link = False,assets_only = True) as (data_from, data_to):
            data_to.objects = data_from.objects
        ## link object to current scene
        for obj in data_to.objects:
            if obj is not None:
                collection.objects.link(obj)
    
    def sign_location_assign(self):
        """ 
        """
        sign_loc_list = []
        current_sign_loc_y = 0
        while True:
            next_sign_loc_y = random.randrange(self.sign_distance_range["min"], self.sign_distance_range["max"])
            sign_loc_y = current_sign_loc_y + next_sign_loc_y
            if sign_loc_y >= self.lane_length:
                break
            sign_loc_x = random.randrange(self.sign_location_offset_range["min"]*10, self.sign_location_offset_range["max"]*10) / 10
            sign_loc_z = random.randrange(self.sign_hight_range["min"], self.sign_hight_range["max"]) / 100
            sign_loc_list.append([sign_loc_x,sign_loc_y, sign_loc_z])
            current_sign_loc_y = sign_loc_y
        return sign_loc_list

    def import_sign_asset(self):
        """ 
        """
        ## get sign asset path
        sign_asset_path_list = glob.glob(os.path.join(self.sign_asset_folder_path, "*.blend"))
        num_sign_asset = len(sign_asset_path_list)
        print(f"num sign asset in folder: {num_sign_asset}")

        ## check num_sign_need_import is bigger than num_sign_asset
        if self.num_sign_need_import >= num_sign_asset:
            ## loop import sign asset
            num_loop = self.num_sign_need_import // num_sign_asset
            num_remain = self.num_sign_need_import % num_sign_asset

            for i in range(num_loop):
                for sign_asset_path in sign_asset_path_list:
                    self.load_obj_from_blend_file(filepath=sign_asset_path, collection=self.sign_collection)

            if num_remain != 0:
                for i in range(num_remain):
                    self.load_obj_from_blend_file(filepath=sign_asset_path_list[i], collection=self.sign_collection)
        else:
            ##randomly select n(n=num_sign_need_import) sign asset from sign_asset_path_list, then import to SignCollection
            sign_asset_path_list_selected = random.sample(sign_asset_path_list, self.num_sign_need_import)
            for sign_asset_path in sign_asset_path_list_selected:
                self.load_obj_from_blend_file(filepath=sign_asset_path, collection=self.sign_collection)

    def sign_placement_randomize(self):
        """ 
        """
        sign_loc_list = np.add(self.sign_location_assign(), self.sign_right_origin).tolist()
        self.num_sign_need_import = len(sign_loc_list)
        print(f"sign_loc:\n{sign_loc_list}")
        print(f"num_sign_need_import:{self.num_sign_need_import}")
        self.import_sign_asset()

        ## move all sign asset to sign_loc
        sign_asset_list = []
        for sign_asset in self.sign_collection.objects:
           sign_asset_list.append(sign_asset)
        for i in range(self.num_sign_need_import):
            sign_location = (sign_loc_list[i][0],sign_loc_list[i][1],sign_loc_list[i][2])
            sign_asset_list[i].location = sign_location

        print("Sign Placement Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = SignPlacementRandomizer()
    randomizer.sign_placement_randomize()
