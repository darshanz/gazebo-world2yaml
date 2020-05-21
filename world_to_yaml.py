import untangle
import re

class GazeboWorldToYamlConverter:

    def __init__(self):
        pass
    
    #TODO check for types of models: currently all include tag
    #TODO handle exceptions properly
    def generate_yaml(self, world_, frame_id_, out_yaml_):
        f_out = open(out_yaml_, 'w')
        world_file = untangle.parse(world_)
        models = world_file.sdf.world.include
        for model in models:
            try:
                f_out.write("- type: mesh\n")
                f_out.write("  name: {}\n".format(model.name.cdata))
                f_out.write("  frame_id: {}\n".format(frame_id_))
                model_uri = model.uri.cdata
                model_dae = model_uri.replace("model://","")
                f_out.write('  mesh_resource: "{}/meshes/{}.dae"\n'. format(model_uri, model_dae))
                try:
                    pose = model.pose.cdata
                    pose = re.sub(' +', ' ', pose)
                    pose_split = pose.split(" ")
                    position = [float(i) for i in pose_split[0:3]]
                    orientation = [float(i) for i in pose_split[3:6]]
                    f_out.write("  position: {}\n". format(position))
                    f_out.write("  orientation: {}\n". format(orientation))
                except ValueError:
                    pass
                f_out.write("  scale: [1.0, 1.0, 1.0]\n")
                f_out.write("\n")
            except AttributeError:
                pass
        f_out.close()



world_ = '/home/darshanz/catkin/wspy3/src/avoidance_python/obs_avoid/sim/worlds/simulation.world'
frame_id = "map"

world_to_yaml = GazeboWorldToYamlConverter()
world_to_yaml.generate_yaml(world_, frame_id, "env.yaml")