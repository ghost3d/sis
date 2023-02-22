import bpy
import os
import sys
import subprocess

    

def create_new_file(view_layer_name,shortname,render_folder):
    
    bpy.context.scene.render.use_single_layer = True
    bpy.context.scene.render.use_file_extension = True
    bpy.context.window.view_layer = bpy.context.scene.view_layers [view_layer_name]
    bpy.context.scene.view_layers[view_layer_name].use = True
    outpath = os.path.join(render_folder ,"renders",view_layer_name)
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    bpy.context.scene.render.filepath = os.path.join(render_folder ,"renders",view_layer_name, shortname+"_"+view_layer_name+".")
    new_file_path = os.path.join(render_folder,shortname+ "_"+view_layer_name + ".blend") 
    bpy.ops.wm.save_as_mainfile(filepath=new_file_path, check_existing=False, copy=True)
    main(new_file_path)

def getfileName():
    bfilename = bpy.path.basename(bpy.context.blend_data.filepath)
    bname = bfilename.split(".")
    bname = bname[0]
    return bname
def getrenderfolder():
    bname  = getfileName()
    file_path = bpy.data.filepath
    render_folder = os.path.join(os.path.dirname(file_path), "renderFiles",bname)
    if not os.path.exists(render_folder):
        os.mkdir(render_folder)
    return render_folder


def splitlayers():
    shortname = getfileName()
    renderFolder = getrenderfolder()
    layerstoRender = []
    for scene in bpy.data.scenes:
        for view_layer in scene.view_layers:
            if bpy.context.scene.view_layers[view_layer.name].use  == True:
                 layerstoRender  = layerstoRender.append(view_layer.name)
                 bpy.context.scene.view_layers[view_layer.name].use = False
    for i in layerstoRender:
        bpy.context.scene.view_layers[i].use = True
        create_new_file(i,shortname,renderFolder)
        bpy.context.scene.view_layers[i].use = False

    # for scene in bpy.data.scenes:
    #     for view_layer in scene.view_layers:
    #         create_new_file(view_layer.name,shortname,renderFolder)
    #         bpy.context.scene.view_layers[view_layer.name].use = False



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

def GetRepositoryFilePath(subdir):
    deadlineCommand = GetDeadlineCommand()
    
    startupinfo = None
    #if os.name == 'nt':
    #   startupinfo = subprocess.STARTUPINFO()
    #   startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    args = [deadlineCommand, "-GetRepositoryFilePath "]   
    if subdir != None and subdir != "":
        args.append(subdir)
    
    # Specifying PIPE for all handles to workaround a Python bug on Windows. The unused handles are then closed immediatley afterwards.
    proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)

    proc.stdin.close()
    proc.stderr.close()

    output = proc.stdout.read()

    path = output.decode("utf_8")
    path = path.replace("\r","").replace("\n","").replace("\\","/")

    return path

def main( file):
    script_file = GetRepositoryFilePath("scripts/Submission/BlenderSubmission.py")

    curr_scene = bpy.context.scene
    curr_render = curr_scene.render    

    scene_file = file
    
    if scene_file != "":
        bpy.ops.wm.save_mainfile()
    
    frame_range = str(curr_scene.frame_start)
    if curr_scene.frame_start != curr_scene.frame_end:
        frame_range = frame_range + "-" + str(curr_scene.frame_end)
    
    output_path = str(curr_render.frame_path( frame=curr_scene.frame_start ))
    threads_mode = str(curr_render.threads_mode)
    threads = curr_render.threads
    if threads_mode == "AUTO":
        threads = 0
    
    platform = str(bpy.app.build_platform)
    
    deadlineCommand = GetDeadlineCommand()
    
    args = []
    args.append(deadlineCommand)
    args.append("-ExecuteScript")
    args.append(script_file)
    args.append(scene_file)
    args.append(frame_range)
    args.append(output_path)
    args.append(str(threads))
    args.append(platform)
    
    startupinfo = None
    #~ if os.name == 'nt':
        #~ startupinfo = subprocess.STARTUPINFO()
        #~ startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    
    subprocess.Popen(args, startupinfo=startupinfo)


if __name__ == "__main__":
    splitlayers()