""" AutoLabeler

reference:
https://blender.stackexchange.com/questions/264385/object-index-blender-3-0/264394#264394
https://blender.stackexchange.com/questions/39969/any-idea-how-to-get-the-location-and-bounds-of-object-in-the-image/39983#39983
https://splunktool.com/bounding-box-from-2d-numpy-array-duplicate
https://splunktool.com/how-to-convert-2d-bounding-box-pixel-coordinates-x-y-w-h-into-relative-coordinates-yolo-format
https://github.com/DIYer22/bpycv/blob/master/bpycv/render_utils.py
"""
import bpy
import numpy as np
import datetime
import os

class AutoLabeler:
    def __init__(self,
                 output_img_path = "C:/Users/user/Documents/project/HDAS/gen_data/images",
                 output_label_path = "C:/Users/user/Documents/project/HDAS/gen_data/labels"
                 ):
        self.output_img_path = output_img_path
        self.output_label_path = output_label_path
        self.obj_name_and_id_dict = {}
        self.obj_name_and_bbox_dict = {}
        self.target_obj_collection = bpy.data.collections["VehicleCollection"]
        self.obj_name_and_class_id_mapping = {"car" : 0}
        self.gen_img_id = None
        self.scene = bpy.data.scenes['Scene']
        self.minimum_obj_pixel = 50

    def create_and_switch_annotation_scene(self):
        """
        """
        scene_list = []
        for scene in bpy.data.scenes:
            scene_list.append(scene.name)

        if ("Scene_Annot" not in scene_list):
            bpy.data.scenes['Scene'].copy()
            bpy.data.scenes["Scene.001"].name = "Scene_Annot"

        bpy.context.window.scene = bpy.data.scenes["Scene_Annot"]

    def create_gen_img_id(self):
        """ 
        """
        now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
        id = now.strftime("%Y%m%d%H%M%S")
        return id

    def create_cryptomatte_nodes(self):
        """
        """
        ## active compositing nodes
        bpy.data.scenes['Scene_Annot'].use_nodes = True

        ## clear all nodes
        bpy.data.scenes['Scene_Annot'].node_tree.nodes.clear()

        ## activate object index pass
        bpy.data.scenes['Scene_Annot'].view_layers["ViewLayer"].use_pass_object_index = True

        ## add new nodes
        node_RenderLayers = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeRLayers")
        node_Cryptomatte = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeCryptomatteV2")
        node_Composite = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeComposite")
        node_Viewer = bpy.data.scenes['Scene_Annot'].node_tree.nodes.new("CompositorNodeViewer")
  
        node_RenderLayers.location = (-100,0)
        node_Composite.location = (250,0)
        node_Cryptomatte.location = (250,-200)
        node_Viewer.location = (600,-200)

        ## link nodes
        links = bpy.data.scenes['Scene_Annot'].node_tree.links
        links.new(node_RenderLayers.outputs["Image"], node_Composite.inputs["Image"])
        links.new(node_RenderLayers.outputs["Image"], node_Cryptomatte.inputs["Image"])
        links.new(node_Cryptomatte.outputs["Image"], node_Viewer.inputs["Image"])

    def add_pass_index(self):
        """ 
        """ 
        bpy.context.scene.view_layers["ViewLayer"].use_pass_object_index = True

        for index, obj in enumerate(self.target_obj_collection.objects, start=1): 
            obj.pass_index = index
            self.obj_name_and_id_dict[obj.name] = index

    def annotation_render(self):
        """ 
        """
        bpy.data.scenes['Scene_Annot'].render.engine = "CYCLES"
        bpy.data.scenes['Scene_Annot'].cycles.device = "GPU"
        bpy.data.scenes['Scene_Annot'].cycles.samples = 1
        bpy.data.scenes['Scene_Annot'].cycles.use_denoising = False

        bpy.ops.render.render(scene='Scene_Annot')

    def find_obj_bbox(self):
        """ 
        """
        for obj_name in self.obj_name_and_id_dict:
            bpy.data.scenes["Scene_Annot"].node_tree.nodes["Cryptomatte"].matte_id = obj_name
            self.annotation_render()

            S = bpy.context.scene
            width  = int(S.render.resolution_x * S.render.resolution_percentage / 100)
            height = int(S.render.resolution_y * S.render.resolution_percentage / 100)
            depth  = 4

            img = list(bpy.data.images['Viewer Node'].pixels)
            img = np.array(img).reshape([height, width, depth])[:,:,0]

            if img.max() == 0: # no object in view
                continue
            if (img > 0).sum() <= self.minimum_obj_pixel: # object too small in view
                continue

            img_flip = np.flip(img,0)
            y, x = np.where(img_flip)
            top_left = [x.min(), y.min()]
            bottom_right = [x.max(), y.max()]

            self.obj_name_and_bbox_dict[obj_name] = [top_left,bottom_right]

    def get_obj_class_id(self, obj_name):
        """ 
        """ 
        obj_class_id = None
        for key in self.obj_name_and_class_id_mapping:
            if key in obj_name:
                obj_class_id = self.obj_name_and_class_id_mapping[key]
                return obj_class_id

    def format_coordinates(self,coordinates,obj_class_id):
        """ 
        This function takes as inputs the coordinates created by the find_bounding box() function, the current class,
        the image width and the image height and outputs the coordinates of the bounding box of the current class
        """ 
        ## If the current class is in view of the camera
        if coordinates: 
            ## Figure out the rendered image size
            render = bpy.data.scenes['Scene_Annot'].render
            fac = render.resolution_percentage * 0.01
            dw = 1./(render.resolution_x * fac)
            dh = 1./(render.resolution_y * fac)
            x = (coordinates[0][0] + coordinates[1][0])/2.0
            y = (coordinates[0][1] + coordinates[1][1])/2.0
            w = coordinates[1][0] - coordinates[0][0]
            h = coordinates[1][1] - coordinates[0][1]
            cx = x*dw
            cy = y*dh
            width = w*dw
            height = h*dh

        ## Formulate line corresponding to the bounding box of one class
            txt_coordinates = str(obj_class_id) + ' ' + str(cx) + ' ' + str(cy) + ' ' + str(width) + ' ' + str(height) + '\n'

            return txt_coordinates
            ## If the current class isn't in view of the camera, then pass
        else:
            pass

    def get_all_coordinates(self):
        """ 
        This function takes no input and outputs the complete string with the coordinates
        of all the objects in view in the current image
        """ 
        ## Initialize the variable where we'll store the coordinates
        main_text_coordinates = ''
        ## Loop through all of the objects
        for obj_name in self.obj_name_and_bbox_dict:
            ## Get current object's coordinates
            obj_class_id = self.get_obj_class_id(obj_name)
            coordinates = self.obj_name_and_bbox_dict[obj_name]
            ## Reformat coordinates to YOLOv3 format
            text_coordinates = self.format_coordinates(coordinates, obj_class_id)
            # print(text_coordinates)

            ## If find_bounding_box() doesn't return None
            ## Update main_text_coordinates variables whith each
            ## line corresponding to each class in the frame of the current image
            if text_coordinates:
                main_text_coordinates = main_text_coordinates + text_coordinates
                                                                            
        return main_text_coordinates # Return all coordinates

    def auto_labeling(self):
        """ 
        """ 
        self.gen_img_id = self.create_gen_img_id()

        self.create_and_switch_annotation_scene()

        ##　save png img
        img_file_path = os.path.join(self.output_img_path,  f'{"a"+str(self.gen_img_id).zfill(15)}.png')
        bpy.data.scenes["Scene"].render.filepath = img_file_path          
        bpy.ops.render.render(write_still=True, scene='Scene')

        ## get objects bbox
        bpy.data.scenes['Scene_Annot'].view_layers["ViewLayer"].use_pass_cryptomatte_object = True
        self.create_cryptomatte_nodes()
        self.add_pass_index()
        #print(f'obj_name_and_id_dict:{self.obj_name_and_id_dict}')
        self.find_obj_bbox()
        #print(f'obj_name_and_bbox_dict:{self.obj_name_and_bbox_dict}')

        ## get objects labels
        text_coordinates = self.get_all_coordinates()
        splitted_coordinates = text_coordinates.split('\n')[:-1]# Delete last '\n' in coordinates

        ## save labels
        text_file_path = os.path.join(self.output_label_path, f'{"a"+str(self.gen_img_id).zfill(15)}.txt')
        text_file = open(text_file_path, 'w+') # Open .txt file of the label
        text_file.write('\n'.join(splitted_coordinates))
        text_file.close()

        print("YOLO-coordinates:\n{}".format(splitted_coordinates))
        print("SAVE IMG AT {}".format(img_file_path))
        print("SAVE LABLE AT {}".format(text_file_path))
        print("Auto Labeling COMPLERED !!!")

if __name__ == '__main__':

    auto_labeler = AutoLabeler()
    auto_labeler.auto_labeling()




    



