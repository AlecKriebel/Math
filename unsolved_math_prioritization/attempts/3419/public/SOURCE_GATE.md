# Source and scope gate

Target 3419 / OPG-37237, checked 3 October 2026. This is an unresolved research packet, not a solution claim.

## Identity and prior work

The numerical UnsolvedMath URL was requested directly and returned HTTP 403. A pinned catalogue was used only to identify the title, number and source, not to establish any mathematical claim. The original Open Problem Garden page was successfully read. It asks for a smooth/PL S² embedding in S⁴ with an undecidable complement-group word problem. The original research sources use locally flat PL/smooth knots.

The live AlecKriebel/Math repository was checked independently of its queue row:

- The queue row for rank 539 / 3419 read queued, 0/5.
- All-state PR searches for 3419, 37237 and “Unsolvability word problem” returned no matches.
- A broader “2-knot” PR search returned unrelated PRs 66 and 275, neither an attempt at this question.
- Default-branch searches for the ID and compact title returned no matching work.
- Direct listings of the attempts directory (49 entries) and problems directory (13 entries) had no matching target.
- Branch search for 3419 returned no match and no continuation cursor.

These bounded checks found no prior target attempt to supersede. They are not an exhaustive assertion about every historical or differently titled branch.

## Original mathematical sources

### González-Acuña–Gordon–Simon (2010)

Obtained the complete 29-page published PDF. Read the definitions and characterizations in §2; Proposition 3.1 and its complete printed proof (which explicitly suppresses some free-subgroup cancellation details); Theorem 3.3 and Corollaries 3.4–3.5; and the comparison construction in Theorem 3.6. Printed p.151 was also visually inspected to fix all stable-letter directions and squares.

The perfect-container theorem and Kervaire realization theorem are cited established inputs, not re-proved from foundations or computer-certified. PROOF.md independently expands the subsequent homology calculation. Kervaire realization is used only in knot dimension at least three. The claimed implication to dimension two is expressly rejected.

### González-Acuña (1994)

Obtained the complete eight-page publisher scan. OCR was used for search, and the definition/theorem/proof pages were visually checked. Read Theorem 1 and its complete proof on pp.223–224, including the braid closure, bands, unlink condition, capping disks and genus-zero requirement. The theorem is about a connected, unlinked, saddled presentation of genus zero, not an arbitrary Wirtinger presentation. The introduction and the surface generalization on p.227 were checked.

The PDF's opening author heading is F. González-Acuña. The publisher web metadata and the scan's final address line have an inconsistent name; the bibliography follows the opening heading and the subsequent author's own 2010 citation.

### Yajima (1969)

Obtained the complete institutional scan. Read §§2–3, including the band construction, the generator/relator elimination in (3.1)–(3.5), and the realization in (3.7)–(3.10). The tree-construction page 441 was visually checked. Only the sufficient theorem for a specified deficiency-one Wirtinger presentation is used; no conclusion is drawn merely from the abstract group having deficiency one.

### Hillman, The groups of fibred 2-knots

Obtained the complete 11-page author preprint. Read the relevant finiteness/fibering discussion in §2 and the entire pertinent §4 passage on p.7. The mapping-torus decidability assertion and the satellite presentation are used. The stronger finiteness-to-fibering claims are not treated as unconditional. The cited satellite realization is an established topological input; the packet supplies its own detailed word-problem and finite-quotient arguments.

## Updates actually inspected

### Blackwell–Kirby–Klug–Longo–Ruppik (2025)

Obtained both the complete arXiv manuscript and the complete published PDF. Checked the group-trisection definitions relevant to the application and the complete §§5C–D argument, including Corollary 5.8 and Question 5.9. No claim of independently auditing every proof of the trisection correspondence is made, because the correspondence is not an input to any new positive result here. The recognition statements are not promoted to a fixed-group word-problem theorem.

### Nozaki (June 2026)

Obtained the complete arXiv v1 manuscript. Read §3.2 and the full proof of Proposition 1.3, which turns BS(1,2) into a deficiency-one Wirtinger presentation. The BNSR theorem itself is not needed or re-proved. The example is used solely as a ribbon-group control; its decidable word problem is established separately.

### Kegel–Li–Ren (September 2026)

Obtained arXiv:2609.10461v1, dated 9 September 2026. Read §2 and its full construction, Propositions 2.3–2.4, the complete §3 proofs of the injective HNN stages and edge-group presentations, and Appendix B's normal-form lemmas and proofs. The relevant earlier Borisov embeddings/freeness statements, restated in Theorem 2.1 and Propositions 3.3–3.4, remain explicitly cited external inputs. No Lean code was downloaded or executed, and the authors' formalization is not described as independently reproduced.

PROOF.md Proposition 5 is a separate rational homology calculation from those group decompositions. The calculation never assumes Δ is free. It needs no full presentation of the unspecified semigroup words. This is a concrete obstruction for the group's use in the present problem, not a challenge to its published undecidability construction.

### K3 (2026), Problem 4.35

The author PDF's printed p.219 was checked. Its parenthetical shortcut about arbitrary Wirtinger presentations is not used: it conflicts with the precise original distinctions between sphere-knot groups and surface groups in the sources above. The actual 1994 theorem resolves the scope.

## Other limits and safeguards

The OPG bibliography's Dranišnikov–Repovš article was checked at its publisher bibliographic page/abstract only, not at a complete proof. No conclusion here depends on that article's proof. The argument explains why an arbitrary embedded thickening would in any case leave peripheral/realization conditions unproved.

No public source PDFs, OCR text, scraped pages, catalogue data, private conversation, credentials or coordination records are included. SOURCE_HASHES.json identifies the actually inspected source bytes; all mathematics to be shared is in the written packet.

The searches are dated and bounded. Neither the old open-question statement nor failure to locate a later solution proves that the literature contains none. The outcome recorded is simply that this work has not resolved the question.
