################################################################################
### UI SOUND EFFECTS
################################################################################
# One-shot UI sounds live in game/audio/sfx/ (procedurally generated, quiet by
# design). The button click is wired globally through the button style; every
# other cue goes through play_ui_sound(), which degrades to silence if a file
# is missing instead of erroring.
#
# Cues:
#   ui_click   - any button activation (global style)
#   day_chime  - day transition (main_flow: label next_day)
#   coin       - reserved for shop/economy hooks
#   notify     - reserved for notification hooks
#
# Channel routing (audit note): BGM is on the "music" channel; per-event music
# is on the "sound" channel (main_flow). Button clicks (style activate_sound,
# via config.play_channel) use the fixed "ui_click" channel; play_ui_sound()
# uses the fixed "ui_cue" channel, keeping cues independent of music and clicks.
# The button click is a 60ms, peak-0.15, pop-free clip (fade-in + near-zero
# tail, verified); a new click simply replaces the previous one.
#
# Why fixed channels (crash fix, 2026-10-06): Ren'Py's default play channel is
# the auto channel "audio", which creates a new "audio N" sub-channel whenever
# sounds overlap. Its native layer (renpysound check_channel) grows the channel
# array with realloc() WITHOUT locking the audio callback, so a growth while the
# mixer runs can read freed memory: a random access-violation crash in
# librenpython.dll (player report: offset 0x6cdac4 = callback, Ren'Py 8.3.7;
# still unfixed upstream). Channels registered at init are allocated once, at
# startup, so normal play never grows the array. Do not route sounds back to
# "audio" or other auto channels.

init python:
    renpy.music.register_channel("ui_click", mixer="sfx", loop=False, stop_on_mute=True, tight=False)
    renpy.music.register_channel("ui_cue", mixer="sfx", loop=False, stop_on_mute=True, tight=False)
    config.play_channel = "ui_click"

    def play_ui_sound(name):
        """Play a one-shot UI sound from audio/sfx/, silently skipping missing files."""
        path = "audio/sfx/%s.wav" % name
        try:
            if renpy.loadable(path):
                renpy.play(path, channel="ui_cue")
        except Exception as e:
            renpy.log(f"AUDIO: could not play {path}: {e}")

# Late offset so this wins over the default style definitions.
init offset = 5

style button:
    activate_sound "audio/sfx/ui_click.wav"
