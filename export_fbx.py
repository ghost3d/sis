import pymel.core as pm
import sys
pm.loadPlugin("fbxmaya") # LOAD PLUGIN
import maya.cmds as cmds
import maya.mel as mel
# EXAMPLE SYNTAX
# pm.mel.FBXCommand(args)
exportPath = "C:/Users/mkiry/Documents/work/zombies/zombie/cache/fbx/"
#for example
def exportFBX(list):
    try: 
        cmds.loadPlugin('fbxmaya')
    except:
        sys.stderr.write('ERROR: FBX Export Plug-in was not detected.\n')
        return False
    for i in list:
        filename = i+".fbx"
        fileEsport = exportPath+filename
        
        # mel.eval('FBXExport -f \"{}\" -s').format(fileEsport)
        mel.eval(('FBXExport -f \"{}\" -s').format(fileEsport))
        # cmds.file(fileEsport,pr=1,typ="OBJexport",es=1,op="groups=0; ptgroups=0; materials=0; smoothing=0; normals=0")
                                                                

if __name__ == "__main__":
   mylist = cmds.ls( selection=True )
   exportFBX(mylist)
