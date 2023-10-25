""" LightAndBackgroundRandomizer

""" 

import bpy
import os
from glob import glob
import random
import math
from mathutils import Euler

class LightAndBackgroundRandomizer:
    def __init__(self):
        self.asset_hdri_lighting_folder_path = "C:/Users/user/Documents/project/HDAS/Asset/hdri_lighting"
        self.asset_bg_img_folder_path = 'C:/Users/user/Documents/project/HDAS/Asset/BG-20K/train'
        self.hdri_lighting_strength_range = {"min": 0.5 , "max": 1.5}
        self.bg_img_strength_range = {"min": 0.5 , "max": 1.5}

    def create_world_shader_nodes(self):
        """ Create world shader nodes
        """ 
        ## Use Nodes
        bpy.data.worlds['World'].use_nodes = True

        ## environment node tree reference
        nodes = bpy.data.worlds['World'].node_tree.nodes

        ## clear all nodes
        nodes.clear()

        ## add new nodes(Lighting)
        node_TextureCoordinate_Lighting = nodes.new("ShaderNodeTexCoord")
        node_Mapping_Lighting = nodes.new("ShaderNodeMapping")
        node_Mapping_Lighting.name = "Mapping_lighting"
        node_EnvironmentTexture = nodes.new("ShaderNodeTexEnvironment")
        node_Background_Lighting = nodes.new("ShaderNodeBackground")
        node_Background_Lighting.name = "Background_lighting"
        ## add new nodes(Background)
        node_TextureCoordinate_Background = nodes.new("ShaderNodeTexCoord")
        node_Mapping_Background = nodes.new("ShaderNodeMapping")
        node_BackgroundImage = nodes.new("ShaderNodeTexImage")
        node_Background_Background = nodes.new("ShaderNodeBackground")
        node_Background_Background.name = "Background_background"
        ## add MixShader、LightPath、WorldOutput nodes
        node_MixShader = nodes.new("ShaderNodeMixShader")
        node_LightPath = nodes.new("ShaderNodeLightPath")
        node_WorldOutput = nodes.new("ShaderNodeOutputWorld")

        ## locate nodes
        node_WorldOutput.location = (300, 300)
        node_MixShader.location = (100, 300)
        node_LightPath.location = (-100, 700)

        ## locate nodes(Lighting)
        node_Background_Lighting.location = (-100, 300)
        node_EnvironmentTexture.location = (-400, 300)
        node_Mapping_Lighting.location = (-650, 300)
        node_TextureCoordinate_Lighting.location = (-900, 300)
        ## locate nodes(Background)
        node_Background_Background.location = (-100, -100)
        node_BackgroundImage.location = (-400, -100)
        node_Mapping_Background.location = (-650, -100)
        node_TextureCoordinate_Background.location = (-900, -100)

        ## link nodes
        links = bpy.data.worlds['World'].node_tree.links

        links.new(node_TextureCoordinate_Lighting.outputs["Generated"], node_Mapping_Lighting.inputs["Vector"])
        links.new(node_Mapping_Lighting.outputs["Vector"], node_EnvironmentTexture.inputs["Vector"])
        links.new(node_EnvironmentTexture.outputs["Color"], node_Background_Lighting.inputs["Color"])
        links.new(node_Background_Lighting.outputs["Background"], node_MixShader.inputs[1])
        links.new(node_MixShader.outputs[0], node_WorldOutput.inputs["Surface"])
        links.new(node_LightPath.outputs["Is Camera Ray"], node_MixShader.inputs[0])

        links.new(node_TextureCoordinate_Background.outputs["Window"], node_Mapping_Background.inputs["Vector"])
        links.new(node_Mapping_Background.outputs["Vector"], node_BackgroundImage.inputs["Vector"])
        links.new(node_BackgroundImage.outputs["Color"], node_Background_Background.inputs["Color"])
        links.new(node_Background_Background.outputs["Background"], node_MixShader.inputs[2])

        ## node_BackgroundImage setting
        node_BackgroundImage.extension = "CLIP"


    def light_randomize(self):
        """ 
        """ 
        ## Background node reference
        node_Background_lighting = bpy.data.worlds['World'].node_tree.nodes["Background_lighting"]
        ## EnvironmentTexture node reference
        node_EnvironmentTexture = bpy.data.worlds['World'].node_tree.nodes["Environment Texture"]
        ## Mapping node reference
        node_Mapping_Lighting = bpy.data.worlds["World"].node_tree.nodes["Mapping_lighting"]

        ## get hdri lighting asset path
        hdri_lighting_path_list = glob(os.path.join(self.asset_hdri_lighting_folder_path, "*.exr"))

        ## randomly select a hdri lighting, then add hdri lighting to node_EnvironmentTexture
        hdri_lighting_selected = random.sample(hdri_lighting_path_list, 1)
        hdri_lighting = bpy.data.images.load(hdri_lighting_selected[0])
        node_EnvironmentTexture.image = hdri_lighting

        ## randomly set lighting strength
        light_max = int(self.hdri_lighting_strength_range["max"] * 10)
        light_min = int(self.hdri_lighting_strength_range["min"] * 10)
        lighting_strength = random.randrange(light_min, light_max,1)/10
        node_Background_lighting.inputs["Strength"].default_value = lighting_strength

        ## randomly rotate lighting
        random_rot = random.random() * 2 * math.pi
        node_Mapping_Lighting.inputs["Rotation"].default_value[2] =  random_rot

    def background_randomize(self):
        """
        """
        ## Background node reference
        node_Background_background = bpy.data.worlds['World'].node_tree.nodes["Background_background"]
        ## BackgroundImage node reference
        node_BackgroundImage = bpy.data.worlds['World'].node_tree.nodes["Image Texture"]

        ## get background img asset path
        bg_img_path_list = glob(os.path.join(self.asset_bg_img_folder_path, "*.jpg")) + \
                           glob(os.path.join(self.asset_bg_img_folder_path, "*.png"))

        ## randomly select an img texture , then add img texture to node_BackgroundImage
        bg_img_texture_selected = random.sample(bg_img_path_list, 1)
        bg_img = bpy.data.images.load(bg_img_texture_selected[0])
        node_BackgroundImage.image = bg_img

        ## randomly set bg img strength
        bg_img_max = int(self.bg_img_strength_range["max"] * 10)
        bg_img_min = int(self.bg_img_strength_range["min"] * 10)
        bg_img_strength = random.randrange(bg_img_min, bg_img_max,1)/10
        node_Background_background.inputs["Strength"].default_value = bg_img_strength

    def light_and_background_randomize(self):
        """ 
        """ 
        self.create_world_shader_nodes()
        self.light_randomize()
        self.background_randomize()

        print("Light and Background Randomize COMPLERED !!!")


if __name__ == '__main__':
    randomizer = LightAndBackgroundRandomizer()
    randomizer.light_and_background_randomize()


