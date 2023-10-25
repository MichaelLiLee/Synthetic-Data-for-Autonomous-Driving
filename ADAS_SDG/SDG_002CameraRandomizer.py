""" CameraRandomizer

"""
import bpy
from mathutils import Euler
from math import pi
import random

class CameraRandomizer:
    def __init__(self):
        self.camera_location = (0, 0, 1.2)
        self.camera_location_x_range = [-3.5, 0, 3.5]
        self.camera_pose = (90, 0, 0)
        self.camera_pose_x_offset_range = {"min":-5, "max":5}
        self.camera_pose_z_offset_range = {"min":-10, "max":10}
        self.len_unit = "MILLIMETERS"  #FOV
        self.focal_length = 50
        #self.focal_length_range = [14,20,24,28,35,50,70]
        self.focal_length_range = [15,20,25,30,35,40,45,50,55,60,65]
        # self.fov_degree = 39.5978
        # self.fov_degree_range = [40,50,60]
        self.clip_end = 300
        # self.focus_distance = 10
        # self.focus_distance_range = [10,20,30,40,50,60,70,80]
        # self.sensor_width = 36
        self.img_resolution_x = 1920
        self.img_resolution_y = 1080

    def camera_default_setting(self):
        """ 
        """
        ## set camera location
        bpy.data.objects["Camera"].location = self.camera_location

        ## set camera pose
        cam_rot = (pi*self.camera_pose[0]/180, pi*self.camera_pose[1]/180, pi*self.camera_pose[2]/ 180)
        bpy.data.objects["Camera"].rotation_euler = Euler(cam_rot, 'XYZ')

        ## set camera len unit
        bpy.data.cameras["Camera"].lens_unit = self.len_unit

        # ## set camera fov
        # cam_fov = pi*self.fov_degree/180
        # bpy.data.cameras["Camera"].angle = cam_fov

        ## set camera focal_length
        bpy.data.cameras["Camera"].lens = self.focal_length

        ## set camera clip end distance
        bpy.data.cameras["Camera"].clip_end = self.clip_end

        # ## activate camera dof
        # bpy.data.cameras["Camera"].dof.use_dof = True
        # ## set camera focus distance
        # bpy.data.cameras["Camera"].dof.focus_distance = self.focus_distance

        # ## set camera sensor width
        # bpy.data.cameras["Camera"].sensor_width = self.sensor_width

        ## set camera resoulation
        bpy.data.scenes['Scene'].render.resolution_x = self.img_resolution_x
        bpy.data.scenes['Scene'].render.resolution_y = self.img_resolution_y

    def camera_placement_randomize(self):
        """
        """
        ## camera location randomize
        camera_location_x = random.choice(self.camera_location_x_range)
        bpy.data.objects["Camera"].location.x = camera_location_x
        ## camera pose randomize
        pose_offset_x_max = int(self.camera_pose_x_offset_range["max"]*10)
        pose_offset_x_min = int(self.camera_pose_x_offset_range["min"]*10)
        pose_offset_z_max = int(self.camera_pose_z_offset_range["max"]*10)
        pose_offset_z_min = int(self.camera_pose_z_offset_range["min"]*10)

        pose_offset_x =  random.randrange(pose_offset_x_min, pose_offset_x_max, 1)/10
        pose_offset_z =  random.randrange(pose_offset_z_min, pose_offset_z_max, 1)/10

        cam_rot = (pi * (self.camera_pose[0] + pose_offset_x)/180, 
                   pi * self.camera_pose[1]/180, 
                   pi * (self.camera_pose[2] + pose_offset_z)/180)
        bpy.data.objects["Camera"].rotation_euler = Euler(cam_rot, 'XYZ')

    def camera_intrinsic_randomize(self):
        """ 
        """ 
        # ## camera fov randomize
        # camera_fov = pi * random.choice(self.fov_degree_range) / 180
        # bpy.data.cameras["Camera"].angle = camera_fov

        ## camera focal length randomize
        camera_focal_length = random.choice(self.focal_length_range)
        bpy.data.cameras["Camera"].lens = camera_focal_length

        # ## camera focus distance randomize
        # camera_focus_dist = random.choice(self.focus_distance_range)
        # bpy.data.cameras["Camera"].dof.focus_distance = camera_focus_dist

    def camera_randomize(self):
        """
        Camera Randomizer main function
        """
        self.camera_default_setting()
        self.camera_placement_randomize()
        self.camera_intrinsic_randomize()
        
        print("Camera Randomize COMPLERED !!!")

if __name__ == '__main__':
    randomizer = CameraRandomizer()
    randomizer.camera_randomize()