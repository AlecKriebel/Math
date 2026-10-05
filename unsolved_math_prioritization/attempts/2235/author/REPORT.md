# Erdős Problem 655: already-known literal counterexample

Checked 2026-10-05 UTC. Numeric target: UnsolvedMath 2235; code EP-655; queue rank 765.

## Outcome

**Already solved in the negative, for the exact literal formulation only.** The smallest possible global number of positive distances under its centered-circle condition is floor(n/2), attained by a regular n-gon. PROOF.md supplies a complete proof, including pinned and summed counts and the quantifier negation. This is credited reproduction of known mathematics. It does not settle any corrected/general-position version.

**Substantive source/verification routes: 1/5; original solution credit: zero.** The first route verifies a prior result and recovers the historical scope distinction. Work stopped there; the proof and exact controls document that known result rather than continue original proof search. Proposed curation is already_solved for the literal statement only, subject to fresh audit. If a queue status cannot preserve this scope, use a qualified unresolved historical-target status instead. No candidate-new-solution claim is made.

## Identity and formulation gate

The actual indexed problem page and the complete imported record agree: the only geometric hypothesis is that a circle centered at one selected point cannot contain three other selected points. The claimed conclusion is a global distinct-distance bound (1+c)n/2 for a fixed c>0 and all sufficiently large n. Distinctness of the n points is made explicit in PROOF.md; even if repetitions were permitted, distinct regular-polygon examples still refute the statement.

Both page background and the imported record already mention Hunter's regular-polygon objection. The queue's eligibility and the proposed degree-compatibility route therefore do not establish a valid open target. We did not silently add general position.

The accessible, search-served tracker discussion still carries OPEN and the ambiguous-statement flag, while crediting Hunter's objection. Its five visible comments include January 19, 2026 discussion of possible repairs and an April 22, 2026 link to a historical overview. This is a source-status observation, not an assertion that the false literal conjecture is unresolved. Direct live requests to the main page and some discussion/history/LaTeX endpoints failed with 403 or tool retrieval errors. The indexed page/forum content was obtainable, but fresh live-page status and completeness after the indexed crawl cannot be certified.

## Primary source and later literature

Erdős, *Some old and new problems in combinatorial geometry* (1988), pp.32–37, printed p.35, equation (6), was downloaded and visually inspected. Its hypotheses include no four concyclic points as well as the centered-circle restriction. The question concerns max_x d_X(x), and a subsequent displayed formula concerns the sum. The text explicitly notes that regular polygons defeat the claim without the concyclicity restriction. Thus the inspected historical target differs from the literal modern target in both its hypotheses and counted quantity.

The tracker cites [Er97e]: Erdős, *Some of my favourite unsolved problems*, Math. Japon. 46(3) (1997), 527–537, MR1487304. The title/year/pages are corroborated by the Erdős publication bibliography. The precise relevant passage of that 1997 paper was not obtained. We do not claim that the 1988 wording proves exactly what was written in 1997, nor that every intended historical interpretation has been recovered.

The unsigned *Erdős Problem #655 and Its Natural Repairs: Exact Resolutions, Historical Sources, and Open Variants* (April 22, 2026), linked by Przemek Chojecki in the forum, gives the same exact local-condition minima in Theorem 3.1 and discusses repaired versions. Its PDF was retrieved and checked. It is an unrefereed overview, not evidence of a new solution here. The proof above was checked directly rather than accepted on that note's authority. Its historical paraphrase writes a trivial n/2 bound; for odd n the correct integral bound is floor(n/2), as proved here and consistent with the original (n-1)/2 inequality.

The current formal-conjectures file labels the literal claim solved and its general-position variant open. It links an external formalization commit. The fetched registry file itself contains `sorry`; no Lean build or external proof certification was performed here. The mathematical proof in PROOF.md does not depend on that registry claim.

Bounded exact-ID, phrase, original-title, later-date, and source searches found no reason to reinterpret this as a novel target. These searches do not prove the absence of unindexed literature, nor certify the present status of repaired variants. A complete known counterexample makes further literal proof search unnecessary.

## Prior work and related targets

At repository main commit 6144d964777214c6963a915288c18fcf97b42026, the target's queue row was queued 0/5, state.json had no target entry, and exact-ID parses of history.jsonl and assessment_history.jsonl found no target event. The expected attempt path returned 404. Bounded all-state PR, branch, commit, and code searches found no exact-target prior attempt. Numeric-only PR search also returned unrelated PR #655 and occurrences of 655 in other reports; these were not treated as target matches. This is a bounded observation, not proof of exhaustive repository history.

The full imported problems corpus and research-results corpus were inspected. The complete target record already contains the known counterexample and a dated ambiguity assessment. No keyed or full-text exact-target research-results report was found. No matching target group was present in the checked related-target index, and no second normalized identical statement was found. Corpus hashes match the pinned public repository manifest; the catalogue additionally matches the live pinned Git blob identity. This establishes integrity against that recorded snapshot, not a fresh download of the dataset.

Related records 1927/EP-98 and 2234/EP-654 concern respectively general-position global distances and no-four-concyclic pinned distances. They have materially different hypotheses or conclusions. Their statuses were not changed, and this counterexample does not dispose of them.

## Precisely what remains

Nothing remains to prove for the literal yes/no question: the answer is no. The historical no-four-concyclic-plus-centered-circle pinned question, its sum variant, and the modern general-position/global variant are separate targets. Their resolution is outside this packet. Recovering the exact 1997 passage and verifying the tracker's current live dynamic state remain source-documentation limitations, without affecting the elementary refutation of the exact retrieved literal statement.

## Files, audit, and publication boundary

Run `python3 verify.py` or `python3 -O verify.py` for exact controls. Run `python3 verify_manifest.py` for inventory and SHA-256 checks after freezing. The manifest excludes itself to avoid self-reference; the separate freeze receipt pins it and the archive.

This author packet is pending fresh uninvolved audit. No remote repository write was made. It contains only authored analysis/proof/code, public source metadata, public hashes, and verification outputs. Source PDFs, page images, full-text extracts, raw dataset records, and private coordination are excluded. AI assistance was substantial; this is not a peer-reviewed publication or formal proof-assistant verification.
