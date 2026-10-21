# Source-resolution gate, independent audit

PR 248 / 30004630 / OWR-4990378-001. All three actual primary PDFs were obtained on 2026-10-14 UTC and match the submitted SHA256 and byte pins exactly. See `excluded_reading_pins.json`. An initial web fetch of the MFO URL timed out; direct retrieval then succeeded. No substituted version or access-failure inference was used. Complete texts and rendered pages are private excluded reading copies.

## Literal original scope

[Official Oberwolfach Report 9/2021](https://publications.mfo.de/bitstream/handle/mfo/3850/OWR_2021_09.pdf), PDF pages 20–22, printed 438–440, was read and visually inspected. Its final open sentence is: “the case β₂ = 0 is an open problem.” This follows its unchanged strict critical-cone condition and strong L^2-squared growth conclusion. The report uses an L^2 neighborhood and includes a nonnegative terminal H^{-1} velocity-square cost. It does not specify a replacement condition or assert impossibility of all unregularized growth theory.

Verdict: the candidate resolves negatively the contextual question of retaining that displayed condition while deleting β₂>0. It does not resolve the broader program of devising modified conditions, weaker growth, or all possible stability estimates. The live queue's linked title is appropriately narrow; an unqualified “all quadratic-growth theory at β₂=0 is solved” interpretation would overstate this result. This distinction is about scope, not a discovered proof defect.

## Referenced full analysis

[Kunisch–Meinlschmidt arXiv 1907.02744v1](https://arxiv.org/pdf/1907.02744v1), 42 pages, was extracted completely. Relevant text was read at printed 5–9, 16–26, 35–37. Printed 8, 26 and 35 were visually checked. Lemma 2.9 supplies the linear forcing estimate. Proposition 2.7/Corollary 2.8 identify the unique mild/dispersive class. Theorem 4.1 supplies optimal existence for γ>0 and either β₂>0 or an integrable radius. The candidate satisfies the latter alternative. Theorem 4.3 and Lemma 4.6 cover smooth derivatives. The critical cone uses zero first directional derivative, and its sparse substitute second derivative is defined as zero at zero control. Theorem 4.17 assumes β₂>0 and localizes in L^∞ while concluding L^2-squared growth. It imposes no nonzero-cone condition. The candidate's vacuity is therefore legitimate and its vanishing-amplitude pulses defeat either localization.

[The exact author-hosted preprint](https://hannes.meinlschmidt.eu/preprint/KunischMeinlschmidt2020.pdf) was separately retrieved and cross-checked in these sections; printed 8, 26 and 35 were visually inspected. It agrees on these requirements. It remains separately pinned, not silently equated to the publisher's final typesetting, which was not inspected in this audit. Both preprints omit the report's ν-term; the independent direct-method derivation covers that discrepancy for every fixed ν≥0.

## Proof correctness versus resolution and priority

The independent derivation was saved before the old reviewer verdict was opened. Its mathematics supports the stated negative theorem. Later agreement with the old review is corroboration, not the basis of the verdict. Its campaign promotion and priority claims are not mathematical evidence. The paper's estimates and solution theory are classical credited inputs. This audit establishes neither novelty nor historical priority and did not start a deep priority investigation.

No mathematical scope repair is required in `COUNTEREXAMPLE.md`, which already says what it does and does not answer. Any final queue/publication disposition must preserve “counterexample to the unmodified strict-critical-cone implication” and the explicit zero cone. A blanket completion claim for all modified β₂=0 theories remains unsupported.
