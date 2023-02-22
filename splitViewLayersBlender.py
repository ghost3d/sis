import bpy
import os

def create_new_file(view_layer_name,shortname):
    bpy.context.scene.render.use_single_layer = True
    bpy.context.scene.render.use_file_extension = True
    bpy.context.window.view_layer = bpy.context.scene.view_layers [view_layer_name]
    bpy.context.scene.view_layers[view_layer_name].use = True
    bpy.context.scene.render.filepath = os.path.join(render_folder ,"renders",view_layer_name, shortname+"_"+view_layer_name+".")
    new_file_path = os.path.join(render_folder,shortname+ "_"+view_layer_name + ".blend") 
    bpy.ops.wm.save_as_mainfile(filepath=new_file_path, check_existing=False, copy=True)
    
bfilename = bpy.path.basename(bpy.context.blend_data.filepath)
bname = bfilename.split(".")
bname = bname[0]

file_path = bpy.data.filepath
render_folder = os.path.join(os.path.dirname(file_path), "renderFiles",bname)

if not os.path.exists(render_folder):
    os.mkdir(render_folder)

for scene in bpy.data.scenes:
    for view_layer in scene.view_layers:
        bpy.context.scene.view_layers[view_layer.name].use = False
for scene in bpy.data.scenes:
    for view_layer in scene.view_layers:
        create_new_file(view_layer.name,bname)
        bpy.context.scene.view_layers[view_layer.name].use = False

    