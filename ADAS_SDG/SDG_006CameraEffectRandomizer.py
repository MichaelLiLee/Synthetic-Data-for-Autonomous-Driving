""" CameraEffectRandomizer

reference:
Modeling Camera Effects to Improve Visual Learning from Synthetic Data
ChromaticAberration : https://blender.stackexchange.com/questions/168498/is-chromatic-aberration-possible-in-blender
Blur : https://docs.blender.org/manual/en/latest/compositing/types/filter/blur_node.html​
Exposure : https://docs.blender.org/manual/en/latest/compositing/types/color/exposure.html​
Noise: https://blender.stackexchange.com/questions/238692/how-to-add-film-grain-using-the-compositor​
"""

import bpy
import random

class CameraEffectRandomizer:
    def __init__(self):
        self.scene = bpy.data.scenes['Scene']

        self.ChromaticAberration_probability = 0.3
        self.Blur_probability = 0.5
        self.Exposure_probability = 0.3
        self.Noise_probability = 0.5

        self.ChromaticAberration_value = 0.5
        self.Blur_value_range = {"min": 2 , "max": 4}
        self.Exposure_value_range = {"min": -1.5 , "max": 1.5}
        self.Noise_value = 1


    def create_compositing_nodes(self):
        """
        """
        ## active compositing nodes
        bpy.context.scene.use_nodes = True

        ## clear all nodes
        bpy.data.scenes['Scene'].node_tree.nodes.clear()

        ## create camera_sensor_noise_texture
        bpy.data.textures.new("camera_sensor_noise", type="NOISE")
        bpy.data.textures["camera_sensor_noise"].intensity = 1.6

        ## add new nodes
        node_RenderLayers = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeRLayers")
        node_Lensdist = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeLensdist")
        node_Lensdist.use_projector = True
        node_Blur = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeBlur")
        node_Exposure = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeExposure")
        node_Mix = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeMixRGB")
        node_Mix.blend_type = 'MULTIPLY'
        node_Mix.inputs[0].default_value = 0
        node_Texture = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeTexture")
        node_Texture.texture = bpy.data.textures["camera_sensor_noise"]
        node_Composite = bpy.data.scenes['Scene'].node_tree.nodes.new("CompositorNodeComposite")

        node_RenderLayers.location = (-600,0)
        node_Lensdist.location = (-300,0)
        node_Blur.location = (-100,0)
        node_Exposure.location = (100,0)
        node_Mix.location = (300,0)
        node_Texture.location = (-300,-300)
        node_Composite.location = (500,0)
        
        ## link nodes
        links = bpy.data.scenes['Scene'].node_tree.links
        links.new(node_RenderLayers.outputs["Image"], node_Lensdist.inputs["Image"])
        links.new(node_Lensdist.outputs["Image"], node_Blur.inputs["Image"])
        links.new(node_Blur.outputs["Image"], node_Exposure.inputs["Image"])
        links.new(node_Exposure.outputs["Image"], node_Mix.inputs[1])
        links.new(node_Mix.outputs["Image"], node_Composite.inputs["Image"])
        links.new(node_Texture.outputs["Color"],  node_Mix.inputs[2])

    def camera_effect_randomize(self):
        """
        """
        self.create_compositing_nodes()

        ## set happen distribution
        ChromaticAberration_happen_distribution = [self.ChromaticAberration_probability, 1 - self.ChromaticAberration_probability]
        Blur_happen_distribution = [self.Blur_probability, 1 - self.Blur_probability]
        Exposure_happen_distribution = [self.Exposure_probability, 1 - self.Exposure_probability]
        Noise_happen_distribution = [self.Noise_probability, 1 - self.Noise_probability]

        ## ChromaticAberration randomize
        ChromaticAberration_value = random.choices([self.ChromaticAberration_value,0],  ChromaticAberration_happen_distribution)
        bpy.data.scenes["Scene"].node_tree.nodes["Lens Distortion"].inputs[2].default_value = ChromaticAberration_value[0]

        ## Blur randomize
        Blur_value_max = self.Blur_value_range["max"]
        Blur_value_min = self.Blur_value_range["min"]
        random_Blur_value = random.randrange(Blur_value_min, Blur_value_max, 1)
        Blur_value = random.choices([random_Blur_value,0], Blur_happen_distribution)
        bpy.data.scenes["Scene"].node_tree.nodes["Blur"].size_x = Blur_value[0]
        bpy.data.scenes["Scene"].node_tree.nodes["Blur"].size_y = Blur_value[0]

        ## Exposure randomize
        Exposure_value_max = int(self.Exposure_value_range["max"] * 10)
        Exposure_value_min = int(self.Exposure_value_range["min"] * 10)
        random_Exposure_value = random.randrange(Exposure_value_min, Exposure_value_max, 1)/10
        Exposure_value = random.choices([random_Exposure_value,0], Exposure_happen_distribution)
        bpy.data.scenes["Scene"].node_tree.nodes["Exposure"].inputs[1].default_value = Exposure_value[0]

        ## Noise randomize
        Noise_value = random.choices([self.Noise_value,0], Noise_happen_distribution)
        bpy.data.scenes["Scene"].node_tree.nodes["Mix"].inputs[0].default_value = Noise_value[0]

        print("Camera Effect Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = CameraEffectRandomizer()
    randomizer.camera_effect_randomize()



