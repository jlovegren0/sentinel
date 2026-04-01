#!/usr/bin/env python3
"""
Transcribe a Telegram voice note with metalinguistic analysis via Gemini.

Usage:
    python scripts/transcribe_voice.py <path_to_oga>
    python scripts/transcribe_voice.py --latest     # grabs most recent voice file
    python scripts/transcribe_voice.py --list       # lists recent voice files

Output: JSON to stdout (pipe to file or read directly).
"""

import sys
import json
import mimetypes
from pathlib import Path

from google import genai
from google.genai import types

VOICE_DIR = Path.home() / "claude-tty/data/telegram/media/voice"
MODEL = "gemini-3.1-pro-preview"

PROMPT = """\
You are transcribing a voice note about fourth-grade girls' social dynamics. \
The speaker may be Ada herself (a 9-year-old girl, the primary informant) \
speaking in first person, OR her father (an adult male researcher) relaying \
what Ada told him. Identify which based on voice and framing. If Ada is \
speaking directly, her first-person claims carry more weight than paraphrased \
reports.

## Name mappings (apply these in the transcript)
STT often garbles these names. Correct them silently in the transcript:
- "Lao" → Lou
- "Alila" / "Lila" → Lyla
- "Anjali" → Anjolie
- "Anushka" → Anyeshka
- "Baboo" → Babu
- "Ma Perry" → Maperi
- "Samm" → Sanvi
- "Lola" → Leela
- "Nazza" → Navya
Note: "Me" and "Mia" may be confused — use context to disambiguate.
Note: Lyla (Bell homeroom) and Leela (Clendenon homeroom) are two different girls.

## Known names in this study
Ada, Mia, Olivia N, Alicia, Natalia, Annie, Julia, Alice, Lyla, Ashley, \
Madeline H (or Madeline), Jane, Anyeshka, Anjolie, Navya, Mallorie, Kaisha, \
Lou, Maperi, Ruby, Margaret, Abby, Kiara, Sanvi, Leela, Olivia Q, Milan, Ellie.

Homeroom teachers: Bell, Johnson, Babu, Clendenon, Gryser, Bareres.

## Output format
Return a single JSON object with these fields:

{
  "transcript": "Full verbatim transcript with corrected names. Preserve \
filler words (um, uh, like) and false starts — these are analytically \
meaningful.",

  "metalinguistic": [
    {
      "timestamp_approx": "0:00-0:15",
      "observation": "Description of tone, prosody, emphasis, laughter, \
hesitation, pace change, or other paralinguistic feature",
      "analytical_relevance": "Why this matters for interpreting the content"
    }
  ],

  "new_claims": [
    {
      "claim": "A factual assertion made in the voice note",
      "source_framing": "How the speaker frames this — as Ada's direct quote, \
Ada's paraphrase, speaker's inference, or uncertain",
      "names_involved": ["list", "of", "names"]
    }
  ],

  "names_mentioned": ["all names mentioned, using corrected forms"],

  "ambiguities": [
    "Any names, words, or passages you couldn't confidently resolve"
  ],

  "duration_seconds": 0,

  "summary": "2-3 sentence plain-language summary of what was communicated"
}

Return ONLY the JSON object. No markdown fencing, no commentary outside the JSON.\
"""


def find_voice_files():
    return sorted(VOICE_DIR.glob("*.oga"), key=lambda p: p.stat().st_mtime, reverse=True)


def transcribe(path: Path) -> dict:
    client = genai.Client()
    audio_bytes = path.read_bytes()
    mime_type, _ = mimetypes.guess_type(path.name)
    if not mime_type:
        mime_type = "audio/ogg"

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            PROMPT,
            types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
        ),
    )
    text = (response.text or "").strip()
    return json.loads(text)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path.oga | --latest | --list>", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--list":
        for f in find_voice_files()[:20]:
            size_kb = f.stat().st_size // 1024
            print(f"  {f.name}  ({size_kb} KB)")
        return

    if arg == "--latest":
        files = find_voice_files()
        if not files:
            print("No voice files found", file=sys.stderr)
            sys.exit(1)
        path = files[0]
        print(f"Using: {path.name}", file=sys.stderr)
    else:
        path = Path(arg)

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    result = transcribe(path)
    result["source_file"] = str(path)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
