# Independent geometric/source-family audit — PR778 / 30001054

Verdict: **PASS the finite negative result for the four printed term axioms; NEEDS_SCOPE_CORRECTION for any unqualified solved classification.** The normalized-input polygonal variant is not refuted. This is a mathematical-family review, not a publication, priority or PR decision.

Eligible head supplied by parent: c9a87710414d1d4ac5f21e84a81a7d3d40d4d094, claimed_solved at 1/5. I read the complete imported record (prior research {}), candidate scope correction and witness; INITIAL_POSITION.md was preserved before fresh peer/root mathematical conclusions or historical reviews. No historical review was used. A later parent message supplied only a bibliographic redirect. No outside person was contacted and no Git/index/ref/queue/PR/deposit/sheet action was taken.

## Exact source scope

The imported 181-byte question asks whether every allowable double-permutation sequence arises from connected sets with pseudoline separators and common tangents. Goodman-Pollack Definition 12 refers only to the four term properties of Corollary 11; it does not incorporate the stronger switch properties of Proposition 10. The weak definition is therefore in the primary source. Dhandapani et al. instead require every directed supporting and separating pair once; their pre-switch convention differs from the older post-switch convention. Habert-Pocchiola Theorem 49 assumes a specified fibration and represents it. Their encoding discussion attributes the intended positive result. These statements do not equate the weak definition with a valid fibration.

## Direct topological obstruction

Use the source disk model: compact connected disjoint sets, compatible pseudoline arrangement, strict separator per pair, and four designated common tangents per pair, two internal and two external. Directions are terminal points on the disk boundary, rather than Euclidean slopes. In the source convention a right tangent has its body on its left; a left tangent has its body on its right.

For a directed tangent meeting i before j, the post-switch correspondence is left-left → (i,j), right-right → (i',j'), left-right → (i',j), and right-left → (i,j'). Contact order is meaningful even if a set has disconnected contact with the tangent: contacts Ci,Cj,Ci would force the strict separator to be crossed twice, contradicting compatibility. Reversing the tangent reverses encounter order and changes both left/right roles; the ordered endpoint pair becomes reverse-and-toggle of the original pair. Each direction of an internal tangent therefore records a mixed primed/unprimed pair. This weaker necessity alone suffices; a full proof of all eight switch-once necessities is not required.

For A=(1,2,1',2'), B=(1,2,2',1'), C=(2,1,2',1'), the word A,B,A,B,C,B,C,B has events
(2',1'),(1',2'),(2',1'),(2,1),(1,2),(2,1),(1,2),(1',2').
It has zero mixed events, whereas the two designated internal tangents must contribute mixed events. Hence no realization of the complete source model exists.

The obstruction uses no convexity, smoothness, positive area, Euclidean metric or slope. It survives body renaming, phase change and traversal reversal. Nonconvex bodies, nonsmooth boundaries and disconnected contact sets do not erase designated records. Compactness and connectedness are source hypotheses; the local argument needs less. Dropping strict separation/compatibility or the required internal tangent roles changes the target. Degenerate coincident directions/simultaneous events cannot represent this eight-step nonstationary single-swap encoding; ambiguous side assignments of collapsed bodies cannot silently remove designated internal roles.

## Finite verification and genuine geometric control

Each word term respects i before i'; each transition swaps adjacent endpoints of distinct bodies. Reverse-and-toggle exchanges A,C and fixes B, so P[k+4]=R(P[k]). A smaller least period would divide eight; P[0] differs from P[4], excluding 1,2,4. Thus all four weak axioms hold.

The independent exact checker also uses actual disks at (0,0),(3,0), with radii 1 and 7/10. For normal cosine q, the four endpoints are -1,1,3q-7/10,3q+7/10. Exceptional cosines are 17/30,1/10,-1/10,-17/30. Rational samples 1,1/3,0,-1/3,-1,-1/3,0,1/3 follow a full counterclockwise turn and produce D,A,B,C,E,C,B,A, where D=(1,1',2,2'), E=(2,2',1,1'). Their eight ordered events occur once each, with four mixed events. No numerical approximation is used. An intentionally corrupted witness is rejected. Checks use explicit guards and run with ordinary and optimized Python.

## Fully separated input is stronger

Let D=(i1,i1',...,in,in') be a term of a weak-four-axiom sequence. R(D) reverses the body blocks, reversing all four endpoint comparisons for every body pair. Any adjacent-swap path D→R(D) requires at least 4*binomial(n,2) steps. The prescribed half-period has exactly that length. Every cross-body endpoint pair therefore swaps exactly once, with no backtracking. Applying reverse-and-toggle to the other half gives every directed supporting/separating pair once in the full period.

The witness has no fully separated term. It does not refute the explicit normalized-INPUT variant requiring D. The unrestricted p.2551 wording starts “Given an allowable” and later refers to terms following D: that domain ambiguity must not be silently repaired. The lemma does not construct its requested polygons or same-slope-ended polygonal tangents.

## Representation theorem: supported use and exact limit

I checked the relevant original Habert-Pocchiola proof chain: raiponces, projective-plane extension, completion by convex bodies (Lemma 17), and mutation stability (Theorem 18). Theorem 48 extends the representation to pseudocircles; Theorem 49 applies it to the arrangement augmented by a pencil through infinity. The dual pencil points lie on the primal infinity line, preserving the specified directions while original ovals avoid infinity. Some local case analyses are left to the reader by the source; this review is not a complete independent reproof.

A fibration begins with an arrangement whose two-curve subfamilies have the topology of the designated disjoint ovals/points; its augmentation records every vertex with a pencil direction. The witness does not encode this input. I have not independently reconstructed the claimed encoding equivalence for every proper switch-once interval sequence. A universal positive statement for that proper class remains an attributed literature result. The weak-definition equivalence is false by the finite obstruction. No new proof search was used to fill this gap.

## Source reading and reproducibility

SOURCE_READING.json records precise primary-source locators, URLs, versions, hashes, visual checks and actual tool/storage failures. Full fetched PDFs and page renders were removed from my own scratch after inspection; no third-party bodies remain in the packet. INPUT_IDENTITY.json separately binds the three current inputs and supplied head. MANIFEST.json and verify_packet.py provide recursive, mtime-independent custody; --current-inputs is a distinct optional check. Run:

    python3 check_geometric.py
    python3 -O check_geometric.py
    python3 verify_packet.py
    python3 -O verify_packet.py
    python3 verify_packet.py --current-inputs
