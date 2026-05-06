# Project Instructions: assemblylook

## Overview
AssemblyLook is a unified session tracker. Voice generation is delegated to the `assembly-voice` project.

## TTS Interaction
When generating audio for responses, use the script located in the sibling directory:
- **Command:** `python /home/gmusic/workspace/assembly-voice/scripts/tts-generate.py --text "[text]" --persona [name]`

## Voice Personas (Edge-TTS)
- **aureon**: `fr-FR-DeniseNeural` (Female, French)
- **salix**: `fr-FR-HenriNeural` (Male, French)
- **nyro**: `en-US-AriaNeural` (Female, English)
- **jamai**: `en-US-AndrewNeural` (Male, English)
- **synth**: `en-US-GuyNeural` (Male, English)
