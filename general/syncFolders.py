
import os
import shutil

# variables
SOURCE_FOLDER           =   'J:\_3d'
DESTINATION_FOLDER      =   'Y:\_3d'



def recursive_copy(src, dst):
        os.chdir(src)
        for item in os.listdir():
            print (item)
            try:
                if os.path.isfile(item):
                    shutil.copy(item, dst)

                elif os.path.isdir(item):
                    new_dst = os.path.join(dst, item)
                    os.mkdir(new_dst)
                    recursive_copy(os.path.abspath(item), new_dst)
            except:
                pass





if __name__ == '__main__':
    recursive_copy(SOURCE_FOLDER,DESTINATION_FOLDER)
