#!/usr/bin/python3

import bpy

print('Creating instanced animation')

"""
filepath = 'C:/Users/conta/Work/Randy/misc_supporting/create_instanced_animation.py'
exec(compile(open(filepath).read(), filepath, 'exec'))

"""

NUM_FRAMES = 30
REF_SPHERE_NAME = "og_sphere"

def set_keys_constant(obj):
    fcurves = obj.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'CONSTANT'

def set_visible_frame_range(obj, start_frame, end_frame, max_frames):
    print(obj)
    if start_frame > 1:
        obj.scale = (0.01,0.01,0.01)
        obj.keyframe_insert(data_path="scale", frame=1)
        obj.keyframe_insert(data_path="scale", frame=start_frame-1)
    obj.scale = (1.0,1.0,1.0)
    obj.keyframe_insert(data_path="scale", frame=start_frame)
    # if end_frame > start_frame:
    #     obj.keyframe_insert(data_path="scale", frame=end_frame-1)
    # if end_frame < max_frames:
    obj.keyframe_insert(data_path="scale", frame=end_frame)
    obj.scale = (0.01,0.01,0.01)
    obj.keyframe_insert(data_path="scale", frame=end_frame+1)
    obj.keyframe_insert(data_path="scale", frame=max_frames)

# create 2nd material
def create_mat(name, color):
    mat = (bpy.data.materials.get(name) or 
        bpy.data.materials.new(name))
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    combined_col = (color[0], color[1], color[2], 1)
    print('name', name)
    print('combined_col', combined_col)
    bpy.data.materials[name].node_tree.nodes["Principled BSDF"].inputs[0].default_value = combined_col

    return mat

def create_sphere(name):
    bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.active_object.name = name
    sphere = bpy.data.objects[name]
    return sphere


# node = nodes.new('ShaderNodeBsdfPrincipled')
# node.location = (100,100)

def copy_linked(name):
    bpy.ops.object.duplicate_move_linked(OBJECT_OT_duplicate={"linked":True})
    # print('bpy.context.active_object.name', bpy.context.active_object.name)
    # print('name', name)
    # bpy.context.active_object.name = name
    # copied = bpy.data.objects[name]
    print('bpy.context.active_object',bpy.context.active_object)
    return bpy.context.active_object

def create_linked_sphere(name):
    print('create_linked_sphere')
    bpy.ops.object.select_all(action='DESELECT')
    # for obj in bpy.data.objects:
    #     print('obj', obj)
    og_sphere = bpy.data.objects[REF_SPHERE_NAME]
    bpy.context.view_layer.objects.active = og_sphere
    bpy.context.view_layer.objects.active.select_set(state=True)
    print('create_linked_sphere bpy.context.active_object.name', bpy.context.active_object.name)
    sphere = copy_linked(name)
    # for obj in bpy.data.objects:
    #     print('obj', obj)
    bpy.ops.object.select_all(action='DESELECT')
    return sphere

def create_sphere_at_frame(frame_num, frame_max, color):
    mat = create_mat("x"+str(frame_num), color)
    sphere = create_linked_sphere("my_sphere"+str(frame_num))
    set_visible_frame_range(sphere, frame_num, frame_num+1, frame_max)
    sphere.data.materials.append(mat)
    sphere.material_slots[0].link = 'OBJECT'
    sphere.material_slots[0].material = mat

    set_keys_constant(sphere)


def main():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    bpy.context.scene.frame_end = 20
    create_sphere(REF_SPHERE_NAME)
    for i in range(0,20):
        create_sphere_at_frame(i,i,(0.8, float(i)/20.0, 0.254486))

    bpy.ops.object.select_all(action='DESELECT')
    og_sphere = bpy.data.objects[REF_SPHERE_NAME]
    bpy.context.view_layer.objects.active = og_sphere
    bpy.context.view_layer.objects.active.select_set(state=True)
    bpy.ops.object.delete()

main()

# # create material
# mat_name = "Pink"
# mat = create_mat("Pink",(0.8, 0.117355, 0.254486) )

# # create 2nd material
# mat_name = "yello"
# mat2 = create_mat("yello", (0.8, 0.745191, 0.0080575) )

# # create sphere
# my_sphere = create_sphere("my_sphere")

# #set keyframes
# # my_sphere.scale = (1.0,1.0,1.0)
# # my_sphere.keyframe_insert(data_path="scale", frame=1)
# # my_sphere.keyframe_insert(data_path="scale", frame=10)
# # my_sphere.scale = (0.01,0.01,0.01)
# # my_sphere.keyframe_insert(data_path="scale", frame=11)
# # my_sphere.keyframe_insert(data_path="scale", frame=20)
# set_visible_frame_range(my_sphere, 1, 10, 20)

# # assign mesh
# my_sphere.data.materials.append(mat)

# set_keys_constant(my_sphere)


# # ****************
# # create sphere
# my_sphere2 = create_sphere("my_sphere2")

# #set keyframes
# set_visible_frame_range(my_sphere2, 10, 20, 20)


# # assign mesh
# my_sphere2.data.materials.append(mat2)
# set_keys_constant(my_sphere2)




# bpy.ops.node.add_node(type="ShaderNodeBsdfPrincipled", use_transform=True)


# https://vividfax.github.io/2021/01/14/blender-materials.html#:~:text=Assign%20a%20material%20to%20an%20object%20in%20Blender%20using%20Python&text=The%20function%20takes%20a%20string%20as%20the%20name%20for%20the%20new%20material.&text=Then%20add%20a%20shader%20to,glossy)%20and%20the%20rgb%20colour.&text=Then%20create%20the%20object%2C%20assign%20the%20material%20and%20call%20the%20function.


"""
bpy.ops.material.new()
"""

print('done')