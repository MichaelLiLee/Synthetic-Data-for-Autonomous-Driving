""" LightRandomizer
"""

""" 
reference:
https://blender.stackexchange.com/questions/209584/using-python-to-add-an-hdri-to-world-node
""" 

import bpy
import os
from glob import glob
import random

class LightRandomizer:
    def __init__(self,
                asset_hdri_lighting_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/hdri_lighting",
                hdri_lighting_strength_range = {"min": 0.5 , "max": 1.5}
                ):
        self.asset_hdri_lighting_folder_path = asset_hdri_lighting_folder_path
        self.hdri_lighting_strength_range = hdri_lighting_strength_range

    def __create_world_shader_nodes(self):
        """ Create world shader nodes
        """ 
        ## Use Nodes
        bpy.data.worlds['World'].use_nodes = True

        ## environment node tree reference
        nodes = bpy.data.worlds['World'].node_tree.nodes

        ## clear all nodes
        nodes.clear()

        ## add new nodes 
        node_WorldOutput = nodes.new("ShaderNodeOutputWorld")
        node_Background = nodes.new("ShaderNodeBackground")
        node_EnvironmentTexture = nodes.new("ShaderNodeTexEnvironment")
        node_Mapping = nodes.new("ShaderNodeMapping")
        node_TextureCoordinate = nodes.new("ShaderNodeTexCoord")

        node_WorldOutput.location = (100, 300)
        node_Background.location = (-100, 300)
        node_EnvironmentTexture.location = (-400, 300)
        node_Mapping.location = (-650, 300)
        node_TextureCoordinate.location = (-900, 300)

        ## link nodes
        links = bpy.data.worlds['World'].node_tree.links
        links.new(node_TextureCoordinate.outputs["Generated"], node_Mapping.inputs["Vector"])
        links.new(node_Mapping.outputs["Vector"], node_EnvironmentTexture.inputs["Vector"])
        links.new(node_EnvironmentTexture.outputs["Color"], node_Background.inputs["Color"])
        links.new(node_Background.outputs["Background"], node_WorldOutput.inputs["Surface"])

    def light_randomize(self):
        """ 
        """ 
        self.__create_world_shader_nodes()

        ## Background node reference
        node_Background = bpy.data.worlds['World'].node_tree.nodes["Background"]
        ## EnvironmentTexture node reference
        node_EnvironmentTexture = bpy.data.worlds['World'].node_tree.nodes["Environment Texture"]

        ## get hdri lighting asset path
        hdri_lighting_path_list = glob(os.path.join(self.asset_hdri_lighting_folder_path, "*.exr"))

        ## randomly select a hdri lighting, then add hdri lighting to node_EnvironmentTexture
        hdri_lighting_selected = random.sample(hdri_lighting_path_list, 1)
        hdri_lighting = bpy.data.images.load(hdri_lighting_selected[0])
        node_EnvironmentTexture.image = hdri_lighting

        ## randomly set lighting strength
        max = int(self.hdri_lighting_strength_range["max"] * 10)
        min = int(self.hdri_lighting_strength_range["min"] * 10)
        lighting_strength = random.randrange(min, max,1)/10

        #bpy.data.worlds["World"].node_tree.nodes["Background"].inputs["Strength"]\.default_value = lighting_strength
        node_Background.inputs["Strength"].default_value = lighting_strength

        print("Light Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = LightRandomizer()
    randomizer.light_randomize()