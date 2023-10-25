""" RoadPlacemnetRandomizer

""" 
import bpy
import random
import numpy
import glob
import os

class RoadPlacemnetRandomizer:
    def __init__(self):
        self.road_collection = bpy.data.collections["RoadCollection"]
        self.road_asset_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/road"

    def load_obj_from_blend_file(self,filepath,collection):
            """ Asset Linking

            reference:
            https://studio.blender.org/training/scripting-for-artists/5eabe54d521eafd0953f6d45/
            https://docs.blender.org/api/current/bpy.types.BlendDataLibraries.html
            https://blender.stackexchange.com/questions/17876/import-object-without-bpy-ops-wm-link-append/33998#33998 
            https://blender.stackexchange.com/questions/34540/how-to-link-append-a-data-block-using-the-python-api?noredirect=1&lq=1
            """ 
            ## append object from .blend file
            with bpy.data.libraries.load(filepath, link = False,assets_only = True) as (data_from, data_to):
                data_to.objects = data_from.objects
            ## link object to current scene
            for obj in data_to.objects:
                if obj is not None:
                    collection.objects.link(obj)
        
    def import_road_asset(self):
        """ 
        """ 
        ## get road asset path
        road_asset_path_list = glob.glob(os.path.join(self.road_asset_folder_path, "*.blend"))
        num_road_asset = len(road_asset_path_list)
        print(f"num road asset in folder: {num_road_asset}")

        ## randomly select a road asset, then import to RoadCollection
        road_asset_path = random.sample(road_asset_path_list, 1)[0] # return a list of str
        self.load_obj_from_blend_file(filepath = road_asset_path, collection = self.road_collection)

    def road_placement_randomize(self):
        """ 
        """ 
        self.import_road_asset()

        print("Road Placemnet Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = RoadPlacemnetRandomizer()
    randomizer.road_placement_randomize()

