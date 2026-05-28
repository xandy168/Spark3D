import bpy, math
from mathutils import Vector

# --- clear scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for block in list(bpy.data.meshes) + list(bpy.data.materials):
    try:
        if block.users == 0:
            (bpy.data.meshes if hasattr(block,'vertices') else bpy.data.materials).remove(block)
    except Exception:
        pass

def mat(name, rgba, rough=0.5, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

SKIN  = mat("skin",  (0.95, 0.78, 0.66, 1.0), 0.6)
HAIR  = mat("hair",  (0.78, 0.78, 0.78, 1.0), 0.7)
SUIT  = mat("suit",  (0.04, 0.04, 0.05, 1.0), 0.35)
SHOE  = mat("shoe",  (0.02, 0.02, 0.02, 1.0), 0.2)
GLASS = mat("glass", (0.05, 0.05, 0.05, 1.0), 0.3, 0.6)
EYEW  = mat("eyew",  (1.0, 1.0, 1.0, 1.0), 0.4)
EYEB  = mat("eyeb",  (0.05, 0.05, 0.05, 1.0), 0.4)
LOBR  = mat("lobster", (0.85, 0.12, 0.08, 1.0), 0.5)
LOBD  = mat("lobster_dark", (0.55, 0.05, 0.04, 1.0), 0.5)
MOUTH = mat("mouth", (0.5, 0.18, 0.18, 1.0), 0.6)

def add(prim, name, loc, scale=(1,1,1), rot=(0,0,0), material=None, **kw):
    if prim == 'sphere':
        bpy.ops.mesh.primitive_uv_sphere_add(location=loc, **kw)
    elif prim == 'cube':
        bpy.ops.mesh.primitive_cube_add(location=loc, **kw)
    elif prim == 'cyl':
        bpy.ops.mesh.primitive_cylinder_add(location=loc, **kw)
    elif prim == 'cone':
        bpy.ops.mesh.primitive_cone_add(location=loc, **kw)
    elif prim == 'torus':
        bpy.ops.mesh.primitive_torus_add(location=loc, **kw)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    o.rotation_euler = rot
    if material:
        o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    return o

# ============ MAN ============
# Body (suit) - torso
torso = add('cube', 'torso', (0, 0, 1.4), scale=(0.55, 0.28, 0.85), material=SUIT)
# bevel torso
bpy.ops.object.modifier_add(type='BEVEL')
torso.modifiers["Bevel"].width = 0.12
torso.modifiers["Bevel"].segments = 4
bpy.ops.object.modifier_apply(modifier="Bevel")

# Neck
add('cyl', 'neck', (0, 0, 2.35), scale=(0.13, 0.13, 0.12), material=SKIN)

# Head
head = add('sphere', 'head', (0, -0.02, 2.7), scale=(0.42, 0.45, 0.48), material=SKIN, segments=48, ring_count=24)

# Hair (cap)
hair = add('sphere', 'hair', (0, 0.02, 2.85), scale=(0.46, 0.46, 0.32), material=HAIR, segments=48, ring_count=24)

# Ears
add('sphere', 'ear_L', (-0.42, 0.0, 2.7), scale=(0.06, 0.10, 0.13), material=SKIN)
add('sphere', 'ear_R', ( 0.42, 0.0, 2.7), scale=(0.06, 0.10, 0.13), material=SKIN)

# Eyes (whites + pupils) – face is on +Y? Let's say face faces +Y? In sketch face faces forward.
# We'll have the figure face +Y (negative Y is back). Actually let's face -Y so default camera (negative Y) sees the face.
# Default camera typically -Y looking +Y. Let's put face on -Y.
add('sphere', 'eye_wL', (-0.16, -0.40, 2.78), scale=(0.06, 0.04, 0.06), material=EYEW)
add('sphere', 'eye_wR', ( 0.16, -0.40, 2.78), scale=(0.06, 0.04, 0.06), material=EYEW)
add('sphere', 'eye_pL', (-0.16, -0.44, 2.78), scale=(0.03, 0.02, 0.03), material=EYEB)
add('sphere', 'eye_pR', ( 0.16, -0.44, 2.78), scale=(0.03, 0.02, 0.03), material=EYEB)

# Glasses - two torus rims + bridge
gl_L = add('torus', 'glasses_L', (-0.16, -0.42, 2.78), rot=(math.pi/2, 0, 0), material=GLASS,
           major_radius=0.10, minor_radius=0.012)
gl_R = add('torus', 'glasses_R', ( 0.16, -0.42, 2.78), rot=(math.pi/2, 0, 0), material=GLASS,
           major_radius=0.10, minor_radius=0.012)
add('cyl', 'glass_bridge', (0, -0.42, 2.78), rot=(0, math.pi/2, 0), scale=(0.012, 0.012, 0.06), material=GLASS)

# Mouth (smile - small flattened sphere)
add('sphere', 'mouth', (0, -0.44, 2.56), scale=(0.07, 0.02, 0.025), material=MOUTH)

# Arms - holding lobster in front, so arms come forward
# Upper arms
import math as m
arm_rot = (m.radians(70), 0, 0)  # rotate forward
add('cyl', 'uarm_L', (-0.55, -0.18, 1.75), scale=(0.10, 0.10, 0.45), rot=(m.radians(70),0,m.radians(8)), material=SUIT)
add('cyl', 'uarm_R', ( 0.55, -0.18, 1.75), scale=(0.10, 0.10, 0.45), rot=(m.radians(70),0,m.radians(-8)), material=SUIT)
# Forearms (meet in front)
add('cyl', 'farm_L', (-0.30, -0.55, 1.45), scale=(0.09, 0.09, 0.40), rot=(m.radians(95),0,m.radians(30)), material=SUIT)
add('cyl', 'farm_R', ( 0.30, -0.55, 1.45), scale=(0.09, 0.09, 0.40), rot=(m.radians(95),0,m.radians(-30)), material=SUIT)
# Hands
add('sphere', 'hand_L', (-0.10, -0.75, 1.40), scale=(0.10, 0.10, 0.10), material=SKIN)
add('sphere', 'hand_R', ( 0.10, -0.75, 1.40), scale=(0.10, 0.10, 0.10), material=SKIN)

# Legs
add('cyl', 'leg_L', (-0.18, 0, 0.45), scale=(0.13, 0.13, 0.55), material=SUIT)
add('cyl', 'leg_R', ( 0.18, 0, 0.45), scale=(0.13, 0.13, 0.55), material=SUIT)
# Shoes
add('cube', 'shoe_L', (-0.18, -0.10, -0.13), scale=(0.16, 0.28, 0.08), material=SHOE)
add('cube', 'shoe_R', ( 0.18, -0.10, -0.13), scale=(0.16, 0.28, 0.08), material=SHOE)

# ============ LOBSTER (held in front) ============
# Body - segmented look with stretched sphere
lob_body = add('sphere', 'lob_body', (0, -0.80, 1.55), scale=(0.22, 0.30, 0.22), material=LOBR, segments=32, ring_count=18)

# Tail segments (curling back)
for i, (y, z, s) in enumerate([(-1.02, 1.50, 0.18), (-1.18, 1.40, 0.15), (-1.30, 1.28, 0.12)]):
    add('sphere', f'lob_tail_{i}', (0, y, z), scale=(s, s*1.1, s*0.9), material=LOBR)
# Tail fan
add('sphere', 'lob_tailfan', (0, -1.40, 1.20), scale=(0.18, 0.10, 0.05), material=LOBD)

# Head bump on body (front)
add('sphere', 'lob_head', (0, -0.62, 1.60), scale=(0.17, 0.15, 0.18), material=LOBR)

# Eyes (stalky, big)
add('sphere', 'lob_eye_L', (-0.10, -0.72, 1.78), scale=(0.06, 0.06, 0.06), material=EYEW)
add('sphere', 'lob_eye_R', ( 0.10, -0.72, 1.78), scale=(0.06, 0.06, 0.06), material=EYEW)
add('sphere', 'lob_pup_L', (-0.10, -0.78, 1.78), scale=(0.03, 0.03, 0.03), material=EYEB)
add('sphere', 'lob_pup_R', ( 0.10, -0.78, 1.78), scale=(0.03, 0.03, 0.03), material=EYEB)

# Claws (large pincers raised up - one up high reaching, one to side)
# Big raised claw (right, pointing up-out)
add('sphere', 'lob_arm_R', ( 0.25, -0.80, 1.85), scale=(0.08, 0.08, 0.20), rot=(m.radians(-20), m.radians(20), 0), material=LOBR)
claw_R = add('sphere', 'lob_claw_R', ( 0.42, -0.85, 2.18), scale=(0.16, 0.10, 0.22), rot=(0, m.radians(25), 0), material=LOBR)
# Pincer tips
add('cone', 'lob_pinch_R1', ( 0.50, -0.85, 2.35), scale=(0.06, 0.06, 0.10), rot=(0, m.radians(25), 0), material=LOBR)

# Left claw (held lower / across)
add('sphere', 'lob_arm_L', (-0.22, -0.85, 1.70), scale=(0.08, 0.08, 0.18), rot=(m.radians(-10), m.radians(-15), 0), material=LOBR)
add('sphere', 'lob_claw_L', (-0.38, -0.92, 1.85), scale=(0.16, 0.10, 0.20), rot=(0, m.radians(-25), 0), material=LOBR)
add('cone', 'lob_pinch_L1', (-0.48, -0.95, 1.98), scale=(0.06, 0.06, 0.10), rot=(0, m.radians(-25), 0), material=LOBR)

# Small legs (under body)
for i, x in enumerate([-0.12, 0.0, 0.12]):
    add('cyl', f'lob_leg_{i}', (x, -0.85, 1.38), scale=(0.015, 0.015, 0.08), rot=(m.radians(20),0,0), material=LOBD)

# Antennae
add('cyl', 'lob_ant_L', (-0.06, -0.80, 1.95), scale=(0.008, 0.008, 0.18), rot=(m.radians(-30),0,m.radians(-5)), material=LOBD)
add('cyl', 'lob_ant_R', ( 0.06, -0.80, 1.95), scale=(0.008, 0.008, 0.18), rot=(m.radians(-30),0,m.radians(5)), material=LOBD)

# ============ Ground + lighting + camera ============
# Ground
add('cube', 'ground', (0, 0, -0.22), scale=(4, 4, 0.02), material=mat("ground", (0.9,0.9,0.92,1.0), 0.8))

# Camera
bpy.ops.object.camera_add(location=(2.6, -3.6, 2.4), rotation=(m.radians(72), 0, m.radians(35)))
cam = bpy.context.active_object
cam.data.lens = 50
bpy.context.scene.camera = cam

# Lights: key + fill + rim
bpy.ops.object.light_add(type='AREA', location=(2.5, -2.5, 4.0))
key = bpy.context.active_object; key.data.energy = 800; key.data.size = 2.0
bpy.ops.object.light_add(type='AREA', location=(-2.5, -1.0, 2.5))
fill = bpy.context.active_object; fill.data.energy = 300; fill.data.size = 2.5
bpy.ops.object.light_add(type='AREA', location=(0, 2.5, 3.0))
rim = bpy.context.active_object; rim.data.energy = 400; rim.data.size = 2.0

# World background
world = bpy.context.scene.world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs[0].default_value = (0.95, 0.95, 0.97, 1.0)
bg.inputs[1].default_value = 1.0

# Render settings
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items] else 'BLENDER_EEVEE'
scene.render.resolution_x = 900
scene.render.resolution_y = 1200
scene.render.film_transparent = False

print("BUILD_OK objects=", len(bpy.data.objects))
