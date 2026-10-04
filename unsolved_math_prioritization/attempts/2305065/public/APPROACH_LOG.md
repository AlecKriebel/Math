# Verification log: 2305065

## Budget

One substantive prior-result verification, 1/5. The exact question is resolved by the primary literature, so no further original search turns are needed. The five checks below are components of that verification, not five new discovery claims or artificially separate turns.

## 2026-10-04 08:56 UTC — Source identity and existing work (20%)

Started with the requested numeric catalogue URL. The web fetch failed and a later direct header request returned HTTP 403; this route was not bypassed. Read the complete recovered input record and prior report. The prior report labelled the question open and asserted that the 2018 source did so. Fresh repository reads found rank 578 queued at 0/5, no state entry, no attempt directory, and no matching PR under numeric ID, AMR code, problem number, or the author Stegenga. A Gol'dberg search found an unrelated Problem 2.5 PR. Related-target groups contained no numeric match. The six selected corpus records containing disc-algebra or Stegenga terms are mathematically distinct; none duplicates the present exact target.

## 2026-10-04 08:57 UTC — Primary literature (55%)

The actual Hayman–Lingham Update 5.65 says the answer is affirmative, crediting Stegenga–Stephenson and Gol'dberg. Located the 1985 primary publisher paper, which explicitly references Problem 5.65 and proves a stronger generic theorem. Downloaded it for private verification. This is a decisive correction of the earlier report, not a novel research result.

## 2026-10-04 08:58–09:00 UTC — Proof and boundary checks (90%)

Read the geometric approximation lemma and the proof of the disc-algebra theorem. Visually inspected the theorem, lemma, and proof pages. Re-downloaded the current arXiv PDF; its SHA-256 equals the recovered version. The full argument in FULL_PROOF.md distinguishes these checks:

1. **Direct published-theorem implication.** The h(t)=t case gives angular nullness. Select a function in the radius-1/2 ball around z to ensure nonconstancy. Status: complete.
2. **Rouche stability and Baire deduction.** Proved uniform persistence of interior coverage on compact subsets and supplied the entire elementary deduction from the published geometric lemma. Status: complete, with the geometric input explicitly cited.
3. **Composition and surjectivity.** Checked that f composed with g has the same interior image as f; the contraction countercontrol proves why merely mapping into D is inadequate. Status: complete.
4. **Constant, univalent, and maximum-modulus controls.** Identified the need to exclude constants in the openness proof, and proved that the exceptional set cannot be empty for a nonconstant solution and that univalent functions cannot work. Status: complete.
5. **Alternative-construction provenance.** The source includes a slit-domain example using a conformal map followed by cubing, and credits a 1984 Gol'dberg construction separately. We do not claim to have audited McMillan's twist-point theorem or obtained Gol'dberg's proof. Status: supplementary provenance only; not needed for the resolution.

## Freeze checkpoint — 2026-10-04

Completion toward exact prior-result verification: 100% before independent audit. Mathematical target has no remaining gap under the cited published theorem. This packet is ready for a fresh uninvolved audit. No remote changes, commit, branch, PR, release, or DOI were made. Any subsequent publication must respect the separate audit and publication gate. Reproducible controls are finite checks, not an analytic proof certificate.
