# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sentinel is a qualitative social network study of fourth grade girls (~28 subjects) at a school in a rich, academically competitive neighborhood. The data comes from handwritten interview notes, speech-to-text transcripts of a key informant (Ada), and diagram decoding. There is no application code — the repo is structured data files and analytical documents.

## Workflow

All work happens on feature branches off `main`, submitted as PRs. The branch naming convention is `claude/plan-session-*`. Commits are granular and descriptive — one logical change per commit.

## Repository Structure

- `data/roster.json` — 28 girls, homerooms, demographics, abbreviations
- `data/rankings.json` — Best-friend rankings from 10 girls, margin note reads, open questions
- `data/cliques.json` — 8 overlapping cliques, disputes, bridge roles, ethnic dynamics, seating maps
- `data/interim_findings.md` — The primary analytical document (~535 lines). Six sections: The Map, Clique Structure, Key Dynamics, Structural Analysis, Analysis of Social Mechanisms, Follow-Up Questions
- `plan.md` — Implementation plans for document restructuring
- `SESSION_STATE.md` — Authoritative tracking document: what's done, what's next, open/resolved questions, current clique summary

## Key Conventions

**SESSION_STATE.md is the source of truth** for project status. Update it whenever findings are integrated, questions are resolved, or the clique summary changes. Keep the "What's Done" list as a numbered changelog.

**Single-source constraint:** Ada is the only active informant. Her assertions are treated as single-source intelligence, not confirmed facts. Follow-up interviews are on hold to protect her confidentiality. Always note sourcing provenance.

**Name handling:** Several names have STT variants that must be mapped correctly: Lao=Lou, Alila/Lila=Lyla, Anjali=Anjolie, Anushka=Anyeshka, Ma Perry=Maperi, Baboo=Babu, Samm=Sanvi, Lola=Leela. "Me"/"Mia" are not reliably distinguished in STT. Annie has no abbreviation. Lyla (Bell) and Leela (Clendenon) are two different people.

**Contradictions are flagged, not resolved.** When Ada's accounts conflict across sessions (e.g., the Lyla discrepancy), document both versions and mark for resolution via future interviews. Do not silently pick one version.

**Analytical labels vs. informant perception:** "Core Five" is an analytical construction; Ada perceives two overlapping triads (Ada/Mia/Lou + Ada/Mia/Natalia). Always distinguish between the researcher's framing and what Ada actually said.

**Relative dates must be converted to absolute dates** when writing to any file (e.g., "Thursday" in conversation becomes "2026-03-05" in the document).

## Data Integrity

- The "D" row in any grid/diagram is a smudge, not real data
- "Nazza" in diagrams = Navya (misread)
- Margin notes required interpretive reading — mark their provenance where they appear
- The `.gitignore` is R-oriented (the project may eventually include R analysis); no R code exists yet
