import bge
from mathutils import Vector

# -------------------
# CONFIG
# -------------------
MOVE_SPEED = 6.0
ACCEL = 20.0
AIR_CONTROL = 0.4

JUMP_FORCE = 8.0
GRAVITY = 20.0
MAX_FALL_SPEED = 25.0

GROUND_CHECK_DIST = 0.3

# -------------------
# MAIN
# -------------------
def main():
    cont = bge.logic.getCurrentController()
    own = cont.owner
    keyboard = bge.logic.keyboard

    # init properties
    if "vel" not in own:
        own["vel"] = Vector((0, 0, 0))
        own["onGround"] = False
        own["groundNormal"] = Vector((0, 0, 1))

    vel = own["vel"]
    input = keyboard.events

    # -------------------
    # INPUT
    # -------------------
    left = input[bge.events.AKEY] == bge.logic.KX_INPUT_ACTIVE
    right = input[bge.events.DKEY] == bge.logic.KX_INPUT_ACTIVE
    jump = input[bge.events.SPACEKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED

    move_input = 0
    if left:
        move_input -= 1
    if right:
        move_input += 1

    # -------------------
    # GROUND CHECK
    # -------------------
    down = -own["groundNormal"]

    start = own.worldPosition
    end = start + down * GROUND_CHECK_DIST

    hit_obj, hit_pos, hit_normal = own.rayCast(end, start, GROUND_CHECK_DIST)

    if hit_obj:
        own["onGround"] = True
        own["groundNormal"] = hit_normal
    else:
        own["onGround"] = False

    # -------------------
    # LOCAL AXES (relative to surface)
    # -------------------
    up = own["groundNormal"]
    forward = own.worldOrientation @ Vector((0, 1, 0))

    # right vector aligned to surface
    right_vec = forward.cross(up).normalized()

    # -------------------
    # MOVEMENT
    # -------------------
    target_speed = move_input * MOVE_SPEED

    current_speed = vel.dot(right_vec)

    control = 1.0 if own["onGround"] else AIR_CONTROL
    speed_diff = target_speed - current_speed

    accel = ACCEL * control
    vel += right_vec * speed_diff * accel * bge.logic.getFrameTime()

    # -------------------
    # JUMP
    # -------------------
    if jump and own["onGround"]:
        vel += up * JUMP_FORCE
        own["onGround"] = False

    # -------------------
    # GRAVITY
    # -------------------
    vel += down * GRAVITY * bge.logic.getFrameTime()

    # clamp fall speed
    fall_speed = vel.dot(down)
    if fall_speed > MAX_FALL_SPEED:
        vel -= down * (fall_speed - MAX_FALL_SPEED)

    # -------------------
    # APPLY MOVEMENT
    # -------------------
    own.worldPosition += vel * bge.logic.getFrameTime()

    # -------------------
    # ALIGN TO SURFACE
    # -------------------
    align_to_normal(own, up)

    # save velocity
    own["vel"] = vel


# -------------------
# ALIGN FUNCTION
# -------------------
def align_to_normal(own, normal):
    # make character "stand" on surface
    z = normal.normalized()

    x = own.worldOrientation.col[0]
    y = z.cross(x).normalized()
    x = y.cross(z).normalized()

    own.worldOrientation = (x, y, z)