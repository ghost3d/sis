import os

source_dir = "/mnt/projects"
project_name = "cloudForest"
season_name = "001"

# Create the project folder inside the source directory
project_path = os.path.join(source_dir, project_name)
os.makedirs(project_path)

# Create the assets folder inside the project folder
assets_path = os.path.join(project_path, "assets")
os.makedirs(assets_path)
os.makedirs(os.path.join(project_path, "out"))
os.makedirs(os.path.join(project_path, "edit"))
os.makedirs(os.path.join(project_path, "ref"))
# Create the props, vehicles, env, and character folders inside the assets folder
props_path = os.path.join(assets_path, "props")
os.makedirs(props_path)
vehicles_path = os.path.join(assets_path, "vehicles")
os.makedirs(vehicles_path)
env_path = os.path.join(assets_path, "env")
os.makedirs(env_path)
character_path = os.path.join(assets_path, "character")
os.makedirs(character_path)

# Create the work, ref, and shared folders inside the assets folder
in_folders = ['ref','client','edit']
os.makedirs(os.path.join(props_path, "work"))
props_in_path = os.path.join(props_path, "in")
os.makedirs(props_in_path)
for folder in in_folders:
    os.mkdir(os.path.join(props_in_path,folder))
os.makedirs(os.path.join(vehicles_path, "work"))
vehicle_in_path = os.path.join(vehicles_path, "in")
os.makedirs(vehicle_in_path)
for folder in in_folders:
    os.mkdir(os.path.join(vehicle_in_path,folder))
os.makedirs(os.path.join(env_path, "work"))
env_in_path = os.path.join(env_path, "in")
os.makedirs(env_in_path)
for folder in in_folders:
    os.mkdir(os.path.join(env_in_path,folder))
os.makedirs(os.path.join(character_path, "work"))
char_in_path = os.path.join(character_path, "in")
os.makedirs(char_in_path)
for folder in in_folders:
    os.mkdir(os.path.join(char_in_path,folder))

# Create the season folder inside the project folder
season_path = os.path.join(project_path, season_name)
os.makedirs(season_path)

# Create the episode folders inside the season folder
for i in range(1, 2):
    episode_path = os.path.join(season_path, "Sq_{:04d}".format(i))
    os.makedirs(episode_path)
    # Create the sequence inside the episode folder
    for g in range (1,2):
        sequence_path = os.path.join(episode_path, "Ep_{:04d}".format(g))
    # Create the shot folders inside the episode folder
        for j in range(1, 5):
            shot_path = os.path.join(sequence_path, "Shot_{:04d}".format(j))
            os.makedirs(shot_path)
            
            # Create the subfolders inside the shot folder
            cg_path = os.path.join(shot_path, "work", "3d")
            os.makedirs(cg_path)
            os.makedirs(os.path.join(cg_path,"renders" ))
            os.makedirs(os.path.join(cg_path,"tex" ))
            os.makedirs(os.path.join(cg_path,"cache" ))
            os.makedirs(os.path.join(cg_path,"geo" ))
            comp_path = os.path.join(shot_path, "work", "2d")
            os.makedirs(comp_path)
            os.makedirs(os.path.join(comp_path,"renders" ))
            os.makedirs(os.path.join(comp_path,"precomp" ))
            shot_in_path = os.path.join(shot_path, "in")
            os.makedirs(shot_in_path)
            for folder in in_folders:
                os.makedirs(os.path.join(shot_in_path,folder))
            os.makedirs(os.path.join(shot_path, "publish"))
            os.makedirs(os.path.join(shot_path, "plates"))
            os.makedirs(os.path.join(shot_path, "vendor"))
