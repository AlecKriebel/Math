# Source and continuity audit

## Exact target and type convention

The full 25-page publisher PDF of Dmitry Fuchs's 2021 article was retrieved and hashed. Printed pp.502–503 define the endpoint-angle types; pp.510–511 specify the parallel-angle convention and Conjecture 2.6. The source's hexagonal lattice classes are on p.506, with the elementary proof of this conjecture on pp.511–512. The target is not the neighboring length-ratio Conjecture 2.7 on p.512.

The parity selector preceding Definition 2.1 is indispensable. The sum relation applies to odd segment count and the difference relation to even segment count. Isolated numerical equalities may overlap in symmetric directions; the parity-selected definition agrees with the direct-chord example. The pinned upstream shorthand for A0 is not treated as the complete definition.

The complete source was available, and the type-definition page (including Figure 8) and conjecture/table page were rendered and visually checked. The full inequalities were transcribed into the exact verifier. Their 14,658 tested interior comparisons agree with the candidate's congruence formula. Boundary sides are dealt with directly and the two representatives 0 and n−2 are identified.

The source's hexagon proof has apparent printed type-label slips: its residue calculation (2,1) modulo three corresponds to A3 in the explicit p.506 classification, although nearby prose says A2. The reconstruction retains the already-known hexagon result and independently checks its arithmetic from the p.506 classification. It does not claim that case as new.

## Precise classical dependencies

Three complete primary papers were retrieved. The PDF hashes match the earlier PR152 source manifest:

1. Fuchs 2021: exact conventions and target
2. Finster, arXiv:1005.4588v3: §§3.1–3.2 and Remarks3.2/3.5 provide the one-cusp odd and two-cusp even group descriptions; printed p.20 specifies the base group's two cusp representatives
3. Boulanger–Lanneau–Massart 2024: §1.4, printed p.791, states the Veech-surface saddle-connection/cusp correspondence

Finster's even case is explicitly for n≥8. Her p.7 states that the two-polygon cover has the same group as the opposite-side quotient, citing Lemma J of Hubert–Schmidt. That statement, the base-group cusp paragraph, and the general correspondence page were rendered and visually checked. The later papers' statements are used with their full hypotheses. The even double polygon is never silently replaced by its lower-genus quotient, and the odd one-cusp statement is not used for even n.

The result imports Veech's classical theorems. The original Veech 1989 full text was not retrieved during this reconstruction; its exact relevant consequences were checked in the complete later primary papers above. No new proof of the Veech theorems is claimed. Riemann–Hurwitz and uniqueness of the hyperelliptic involution are standard compact-Riemann-surface dependencies, with the particular involution and its fixed points checked in the proof.

## Recovery and related prior work

The surviving main-branch queue snapshot showed zero turns for 5000005, but the supplied interruption history identifies an earlier consumed substantive route and missing local-only candidate. That historical work is not erased. The parent-approved conservative count is one earlier turn plus one substantive reconstruction response: **2/5 turns, one approach family**. The unavailable historical hash is recorded in continuity.json, separately from the new candidate hash.

PR152 / target 5000006 was checked through its current GitHub metadata and read from origin/dot/math-5000006 at commit 99ef28d28bf380658400886d1f8c2120a5096d97. Its proof and independent review supply useful prior cone/type work, but its conclusion concerns length ratios only. The current proof does not assume that conclusion. Its new central statement is the common-label reflection law for the matching between all outgoing and backward endpoint germs.

The pinned dataset record was selectively recovered by byte-range requests at immutable revision 37e53eabe540fb458758e198be61634bd02ee008. Its statement hash exactly matches the preexisting catalog. The complete keyed prior report was recovered selectively as well. Its normalized joint review hash exactly matches the preexisting catalog. It is OPEN-TRIAGE literature triage rather than a proof of the target.

## Current literature check and limits

A bounded search on 2026-10-01 used the article title, the exact conjecture number with billiard/type qualifiers, the target title, and proof terminology. It recovered the source and established regular-polygon literature but did not locate a later authoritative proof of the exact all-n signed type rule. This is not an exhaustive bibliography or a historical-priority certificate. Fuchs himself points toward Veech theory and related pentagon work, and that credit is retained.

The parent supplied the exact original missing-route description; reconstruction followed that mechanism rather than opening unrelated proof families. No external researcher was contacted, and no source PDF or source-page render is intended for redistribution. Source caches are ignored by Git.
