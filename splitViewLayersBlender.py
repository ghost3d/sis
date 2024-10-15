bl_info = {
    "name": "Split View Layers Blender Addon",
    "blender": (2, 80, 0),
    "category": "Render",
}

import bpy
import os
import subprocess

class SplitViewLayersOperator(bpy.types.Operator):
    bl_idname = "render.split_view_layers"
    bl_label = "Submit View Layers"
    bl_description = "Split view layers and save them as separate .blend files"

    def execute(self, context):
        def create_new_file(view_layer_name, shortname):
            bpy.context.scene.render.use_single_layer = True
            bpy.context.scene.render.use_file_extension = True
            bpy.context.window.view_layer = bpy.context.scene.view_layers[view_layer_name]
            bpy.context.scene.view_layers[view_layer_name].use = True
            render_path = os.path.join(render_folder, "renders", view_layer_name)
            if not os.path.exists(render_path):
                os.makedirs(render_path)
            bpy.context.scene.render.filepath = os.path.join(render_path, shortname + "_" + view_layer_name + ".")
            new_file_path = os.path.join(render_folder, shortname + "_" + view_layer_name + ".blend")
            bpy.ops.wm.save_as_mainfile(filepath=new_file_path, check_existing=False, copy=True)
            
            # Submit to Deadline
            submit_to_deadline(new_file_path)

        def GetDeadlineCommand():
            deadlineBin = ""
            try:
                deadlineBin = os.environ['DEADLINE_PATH']
            except KeyError:
                #if the error is a key error it means that DEADLINE_PATH is not set. however Deadline command may be in the PATH or on OSX it could be in the file /Users/Shared/Thinkbox/DEADLINE_PATH
                pass
                
            # On OSX, we look for the DEADLINE_PATH file if the environment variable does not exist.
            if deadlineBin == "" and  os.path.exists( "/Users/Shared/Thinkbox/DEADLINE_PATH" ):
                with open( "/Users/Shared/Thinkbox/DEADLINE_PATH" ) as f:
                    deadlineBin = f.read().strip()

            deadlineCommand = os.path.join(deadlineBin, "deadlinecommand")
            
            return deadlineCommand

        def submit_to_deadline(file_path):
            deadline_command = GetDeadlineCommand()
            scene = bpy.context.scene
            job_info = f"""
            Plugin=Blender
            Name={os.path.basename(file_path)}
            Comment=Submitted via Blender script
            Frames={scene.frame_start}-{scene.frame_end}
            ConcurrentTasks=1
            FramesPerTask=1
            """
            plugin_info = f"""
            SceneFile={file_path}
            """
            job_info_file = os.path.join(render_folder, "job_info.job")
            plugin_info_file = os.path.join(render_folder, "plugin_info.job")
            
            with open(job_info_file, 'w') as f:
                f.write(job_info)
            
            with open(plugin_info_file, 'w') as f:
                f.write(plugin_info)
            
            subprocess.run([deadline_command, job_info_file, plugin_info_file])

        bfilename = bpy.path.basename(bpy.context.blend_data.filepath)
        bname = bfilename.split(".")[0]

        file_path = bpy.data.filepath
        render_folder = os.path.join(os.path.dirname(file_path), "renderFiles", bname)

        if not os.path.exists(render_folder):
            os.makedirs(render_folder)

        for scene in bpy.data.scenes:
            for view_layer in scene.view_layers:
                bpy.context.scene.view_layers[view_layer.name].use = False
        for scene in bpy.data.scenes:
            for view_layer in scene.view_layers:
                create_new_file(view_layer.name, bname)
                bpy.context.scene.view_layers[view_layer.name].use = False

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SplitViewLayersOperator.bl_idname)

def register():
    bpy.utils.register_class(SplitViewLayersOperator)
    bpy.types.TOPBAR_MT_render.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SplitViewLayersOperator)
    bpy.types.TOPBAR_MT_render.remove(menu_func)

if __name__ == "__main__":
    register()