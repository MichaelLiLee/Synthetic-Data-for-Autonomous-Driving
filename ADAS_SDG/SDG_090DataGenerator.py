import sys
module_path = 'C:/Users/user/Documents/project/HDAS/HDAS_SDG/python_main'
sys_path_list = []
for p in sys.path:
    sys_path_list.append(p)
if module_path not in sys_path_list:
    sys.path.append('C:/Users/user/Documents/project/HDAS/HDAS_SDG/python_main')
## prevent create __pycache__ file
sys.dont_write_bytecode = True

import bpy
from SDG_000Initializer import Initializer
from SDG_001RoadPlacementRandomizer import RoadPlacemnetRandomizer
from SDG_002CameraRandomizer import CameraRandomizer
from SDG_003VehiclePlacementRandomizer import VehiclePlacementRandomizer
from SDG_004SignPlacementRandomizer import SignPlacementRandomizer
from SDG_005LightAndBackgroundRandomizer import LightAndBackgroundRandomizer
from SDG_006CameraEffectRandomizer import CameraEffectRandomizer
from SDG_010AutoLabeler_eevee import AutoLabeler
import subprocess


def gen_one_data():
    ## initialize SDG modules
    initializer = Initializer()
    initializer.init()
    road_placemnet_randomizer = RoadPlacemnetRandomizer()
    camera_randomizer = CameraRandomizer()
    vehicle_placement_randomizer = VehiclePlacementRandomizer()
    sign_placement_randomizer = SignPlacementRandomizer()
    light_and_background_randomizer = LightAndBackgroundRandomizer()
    camera_effect_randomizer = CameraEffectRandomizer()
    auto_labeler = AutoLabeler()

    # main SDG process
    road_placemnet_randomizer.road_placement_randomize()
    camera_randomizer.camera_randomize()
    vehicle_placement_randomizer.vehicle_placement_randomize()
    sign_placement_randomizer.sign_placement_randomize()
    light_and_background_randomizer.light_and_background_randomize()
    camera_effect_randomizer.camera_effect_randomize()

    ## Update view layer
    bpy.context.view_layer.update()
    auto_labeler.auto_labeling()

    print("Gen One Data COMPLERED!!!")
    sys.exit()

if __name__ == '__main__':
    gen_one_data()
