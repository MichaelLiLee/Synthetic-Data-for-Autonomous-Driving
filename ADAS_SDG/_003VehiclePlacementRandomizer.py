""" VehiclePlacementRandomizer
""" 
import bpy
import random
import numpy as np
import os
import glob

class VehiclePlacementRandomizer:
    def __init__(self):
        self.vehicle_collection = bpy.data.collections["VehicleCollection"]
        self.vehicle_asset_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/vehicle"
        self.vehicle_distance = {"min":10,"max":60}
        self.lane_length = 237
        self.lane_width = 3.5
        self.vehicle_lane_offset = 0.2
        self.lane_1_origin = [-3.5, -30]
        self.lane_2_origin = [0, 0]
        self.lane_3_origin = [3.5, -30]

    def lane_origin_setting(self):
        """
        """ 
        camera_location_x = bpy.data.objects["Camera"].location.x

        self.lane_1_origin[1] = -self.vehicle_distance["min"]
        self.lane_2_origin[1] = -self.vehicle_distance["min"]
        self.lane_3_origin[1] = -self.vehicle_distance["min"]

        if self.lane_1_origin[0] == camera_location_x:
            self.lane_1_origin[1] = 0

        elif self.lane_2_origin[0] == camera_location_x:
            self.lane_2_origin[1] = 0

        elif self.lane_3_origin[0] == camera_location_x:
            self.lane_3_origin[1] = 0

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

    def vehicle_location_assign(self):
        """ 
        """ 
        vehicle_loc_list = []
        current_vehicle_loc_y = 0
        while True:
            next_vehicle_loc_y = random.randrange(self.vehicle_distance["min"], self.vehicle_distance["max"])
            vehicle_loc_y = current_vehicle_loc_y + next_vehicle_loc_y
            if vehicle_loc_y >= self.lane_length:
                break
            vehicle_loc_x = random.randrange(-self.lane_width*self.vehicle_lane_offset*100,
                                             self.lane_width*self.vehicle_lane_offset*100) / 100
            vehicle_loc_list.append([vehicle_loc_x,vehicle_loc_y])
            current_vehicle_loc_y = vehicle_loc_y
        return vehicle_loc_list

    def import_vehicle_asset(self, num_vehicle_need_import):
        """ 
        """ 
        ## get vehicle asset path
        vehicle_asset_path_list = glob.glob(os.path.join(self.vehicle_asset_folder_path, "*.blend"))
        num_vehicle_asset = len(vehicle_asset_path_list)
        print(f"num vehicle asset in folder: {num_vehicle_asset}")

        ## check num_vehicle_need_import is bigger than num_vehicle_asset
        if num_vehicle_need_import >= num_vehicle_asset:
            ## loop import vehicle asset
            num_loop = num_vehicle_need_import // num_vehicle_asset
            num_remain = num_vehicle_need_import % num_vehicle_asset

            for i in range(num_loop):
                for vehicle_asset_path in vehicle_asset_path_list:
                    self.load_obj_from_blend_file(filepath=vehicle_asset_path, collection=self.vehicle_collection)

            if num_remain != 0:
                for i in range(num_remain):
                    self.load_obj_from_blend_file(filepath=vehicle_asset_path_list[i], collection=self.vehicle_collection)
        else:
            ##randomly select n(n=num_vehicle_need_import) vehicle asset from vehicle_asset_path_list, then import to VehicleCollection
            vehicle_asset_path_list_selected = random.sample(vehicle_asset_path_list, num_vehicle_need_import)
            for vehicle_asset_path in vehicle_asset_path_list_selected:
                self.load_obj_from_blend_file(filepath=vehicle_asset_path, collection=self.vehicle_collection)

    def vehicle_placement_randomize(self):
        """ 
        """ 
        self.lane_origin_setting()
        vehicle_lane_1_loc_list = np.add(self.vehicle_location_assign(),self.lane_1_origin).tolist()
        vehicle_lane_2_loc_list = np.add(self.vehicle_location_assign(),self.lane_2_origin).tolist()
        vehicle_lane_3_loc_list = np.add(self.vehicle_location_assign(),self.lane_3_origin).tolist()
        vehicle_loc_list = vehicle_lane_1_loc_list + vehicle_lane_2_loc_list + vehicle_lane_3_loc_list
        num_vehicle_need_import = len(vehicle_loc_list)
        print(f"vehicle_loc:\n{vehicle_loc_list}")
        print(f"num_vehicle_need_import:{num_vehicle_need_import}")
        self.import_vehicle_asset(num_vehicle_need_import=num_vehicle_need_import)

        ## move all vehicle asset to vehicle_loc
        vehicle_asset_list = []
        for vehicle_asset in self.vehicle_collection.objects:
           vehicle_asset_list.append(vehicle_asset)
        for i in range(num_vehicle_need_import):
            vehicle_location = (vehicle_loc_list[i][0],vehicle_loc_list[i][1], 0)
            vehicle_asset_list[i].location = vehicle_location       

        print("Vehicle Object Placement Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = VehiclePlacementRandomizer()
    randomizer.vehicle_placement_randomize()
    