""" SceneryRandomizer

""" 
import bpy
import random
import numpy
import glob
import os

class SceneryRandomizer:
    def __init__(self):
        self.road_collection = bpy.data.collections["RoadCollection"]
        self.background_plane_collection = bpy.data.collections["BackgroundPlaneCollection"]
        self.road_asset_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/road"
        self.bg_img_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/BG-20K/train"
        self.background_plane_asset_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/background_plane"
        self.background_plane_size = [1500,0.001,750]
        self.background_plane_location = (0, 800, 100)

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
        road_asset_path = random.sample(road_asset_path_list, 1)[0]
        self.load_obj_from_blend_file(filepath = road_asset_path, collection = self.road_collection)

    def import_background_plane_asset(self):
        """ 
        """
        ## get background plane asset path
        background_plane_asset_path = glob.glob(os.path.join(self.background_plane_asset_folder_path, "*.blend"))[0]
        ## import to BackgroundPlaneCollection
        self.load_obj_from_blend_file(filepath = background_plane_asset_path, collection = self.background_plane_collection)

    def background_plane_place(self):
        """ 
        """
        bpy.data.objects["background_plane"].location = self.background_plane_location

    def add_background_image(self):
        """ 
        """ 
        ## get img_texture asset path 
        img_texture_path_list = glob.glob(os.path.join(self.bg_img_folder_path, "*.jpg")) + \
                                glob.glob(os.path.join(self.bg_img_folder_path, "*.png"))

        ## randomly select a bg img texture, then load into blender
        bg_img_texture_selected_path = random.sample(img_texture_path_list, 1)
        bg_img = bpy.data.images.load(bg_img_texture_selected_path[0])

        ## apply img texture on background plane
        bpy.data.objects["background_plane"].material_slots[0].material.node_tree.nodes["Image Texture"].image = bg_img

    def scenery_randomize(self):
        """ 
        """ 
        self.import_road_asset()
        self.import_background_plane_asset()
        self.background_plane_place()
        self.add_background_image()

        print("Scenery Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = SceneryRandomizer()
    randomizer.scenery_randomize()

