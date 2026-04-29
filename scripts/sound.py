import bge

cont = bge.logic.getCurrentController()
own = cont.owner

if "music" not in own:
    sound = bge.logic.expandPath("//sound_effects/soundtrack_main_v1.mp3")
    aud = bge.logic.audioDevice()
    handle = aud.play(sound)
    handle.loop_count = -1
    own["music"] = handle