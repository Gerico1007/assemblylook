# Issue: Replace ElevenLabs with Free Edge-TTS

## Problem
ElevenLabs has strict character quotas that are frequently reached during active development and collaboration sessions. This interrupts the "Assembly" workflow and requires manual intervention or waiting for quota resets.

## Solution
Replace ElevenLabs integration with Microsoft Edge-TTS (via `edge-tts` library).

### Benefits
- **No Quotas:** Completely free and unlimited.
- **High Quality:** Utilizes Microsoft's neural voices which are comparable to ElevenLabs.
- **No API Key:** Simplifies setup and reduces security risks in `.env` files.

### Tasks
- [x] Research free alternatives (Edge-TTS identified as best candidate).
- [x] Create prototype script `tts-edge.py`.
- [x] Verify voice mappings for all personas:
  - `aureon`: `fr-FR-DeniseNeural` (Female)
  - `salix`: `fr-FR-HenriNeural` (Male)
  - `nyro`: `en-US-AriaNeural` (Female)
  - `jamai`: `en-US-AndrewNeural` (Male) - *Corrected to Male*
  - `synth`: `en-US-GuyNeural` (Male)
- [ ] Create a new branch for the migration.
- [ ] Replace `tts-generate.py` logic with Edge-TTS.
- [ ] Remove ElevenLabs dependencies from `package.json` (if applicable) and Python requirements.
- [ ] Clean up `.env` instructions regarding ElevenLabs.
- [ ] Verify dashboard integration.
