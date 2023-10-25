import subprocess
for i in range(99999):


    args = [
        "C:/Program Files/Blender Foundation/Blender 3.2/blender",
        "--python",
        "C:/Users/user/Documents/project/HDAS/HDAS_SDG/python_main/SDG_090DataGenerator.py"
        ]

    subprocess.run(args)

    print("ok") 