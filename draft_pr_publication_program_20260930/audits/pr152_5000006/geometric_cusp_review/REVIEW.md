# Independent physical geometry and cusp review

**Scope verdict on repaired proof:** PASS for the physical unfolding, cusp/model-direction reduction, faithful physical folding-chart bridge, source parallelism, and exceptional n=3,4,6 cases. No residual gap was found in this scope after the sign repair. This is a first mathematical family review, not whole-package R1 or publication approval. The all-n P-starting angle-index identification in section3 remains the separate affine/type adversary's responsibility.

**Original submitted proof:** REQUIRED REPAIR. Its universal exact-source-label reversal/invariance assertions are false. The sine-ratio theorem is not falsified by the counterexample; the corrected weight-based route remains valid subject to the separate P-starting index lemma.

Reviewed files:

- Original frozen `original_submission/files/unsolved_math_prioritization/attempts/5000006/CANDIDATE.md`, SHA256 `100454abdfcbeb6647e0e0596a86b86b3a39d330de2605fe485ae242d9e91c9a`.
- Repaired `repaired_proof_v1/CANDIDATE.md`, SHA256 `e6d40a40032b5af335777abf692e6b0bb45b1582f85d7a02bed192b4984217b9`.
- Original `SOURCE_AUDIT.md` and `source_manifest.json`; full primary source PDFs as detailed below.
- Root `PROOF_SIGN_REPAIR.md` after the independent mechanism had been formed.

## Mandatory original correction and exact witness

For physical billiard reversal, the endpoint angles obey alpha'=pi-beta and beta'=pi-alpha. Fuchs's parity-selected definition therefore gives k'=k for even N and k'=-k for odd N. The submitted candidate instead stated the unconditional rule -k.

A concrete unit-side pentagon path starts vertically at P_0=(0,0), where P_4=(1,0). It follows P_0 -> B -> C -> B -> P_0 with B=(0,2sin(pi/5)) on side1 and C=(5/4,tan(2pi/5)/4) on side3. All three reflections are in side interiors, with word[1,3,1]. The middle hit is normal to side3, so the path retraces. It has N=4, alpha=beta=pi/2 and physical type2 modulo3. Its physical reverse is the same path and still has type2, whereas -k predicts1. Both sine weights agree.

The repair is local and fully checkable. Write K for the intrinsic cone index. A P-starting physical chart has k=K. A Q-starting chart folds to P by H compose iota, with H a polygon reflection, and global polygon reflection changes physical k to -k for either N parity. Hence k=-K for a Q start. Intrinsic reversal still gives K'=-K, while the physical starting-chart sign flips precisely for even N. Thus k'=(-1)^N k and w_n(k)=w_n(K) in every chart. Affine reduction requires this weight equality, not exact physical label invariance.

The repaired body implements the distinction in its index definition, Q-fold argument, reversal law, model-chord identification, and common affine scaling step. I checked the exact repaired body at the recorded SHA; it no longer relies on the false unconditional source-label rule.

## Verified geometry and classical dependency scope

1. Reflection in a physical side sends a centered regular polygon P to 2c-P, where c is the side midpoint. It follows that developed copies alternate between translates of P and -P; passing to the reversed-endpoint translation gluing preserves length and first-vertex stopping. The double is a quotient of the labelled unfolding, which need not itself contain just two polygons.
2. The corner successor is P_j -> Q_(j+1) -> P_(j+2). Odd n gives one vertex class and genus(n-1)/2; even n gives two classes and genus(n-2)/2. The even double was retained throughout: the single opposite-side quotient loses vertex data and has different genus. At n=3,4 the vertex classes are regular marked points, so the elementary treatment is necessary rather than an unmarked-torus saddle-connection argument.
3. In each model direction perpendicular to a polygon reflection axis, every nonfixed vertex is paired to its reflected vertex by a chord parallel to the direction. Convexity makes that chord the full intersection of its line with the polygon. Fixed vertices have supporting perpendicular lines. Consequently every inward cone-corner germ reaches another vertex in its first polygon; boundary rays are sides. This exhausts all model connections without an unlabelled-spectrum shortcut.
4. Finster's odd double surface has signature(2,n,infinity) and one cusp. Its even section works with the smaller quotient, but printed p.7 explicitly reports equality of its group with the even double-polygon group for n>=8. Remark3.5 gives signature(n/2,infinity,infinity). Printed p.20 identifies the BASE-group cusp representatives infinity and +/-cot(pi/n); these are horizontal and anglepi/n directions under the x/y projective convention. The many cusps of the later cover group Gamma_n are unrelated and were not substituted.
5. Boulanger-Lanneau-Massart section1.4 states the saddle-connection/cusp correspondence for Veech surfaces generally. Its specialized one-cusp family is odd. The candidate applies the general statement to the even lattice surface and takes even cusp counts from Finster, which is legitimate.
6. The faithful physical/source parallelism is generated by polygon rotations/reflections on unoriented slopes. Their actions preserve the physical weight. For odd n, the half-step rotation of the doubled polygon exchanging P,Q is an affine isometry; the repaired chart distinction justifies its weight invariance. The common affine map acts on every connection in a common model direction and scales all their lengths by the same factor.
7. The triangular and square primitive-lattice proofs hold. For the hexagon the marked honeycomb vertex set is p+q !=2 mod3. Its first vertex is v or2v according to primitive residue s=0,1 or2. The source's labels then give L^2/w^2=4Q/3 for s=0 and4Q for s=1,2, with Q=p^2+q^2-pq. Triangular direction symmetries preserve Q and primitivity and send s to +/-s, proving the elementary ratio claim directly.

Detailed derivations, including the sign bridge and the pentagon witness, are in `GEOMETRIC_DERIVATIONS.md`.

## Primary sources checked

Full legitimate PDFs, with relevant pages visually inspected:

- [Fuchs2021](https://amj.math.stonybrook.edu/pdf-Springer-final/020-0170.pdf): source parallelism p.494, parity and Definition2.1 pp.502-503, elementary rules p.506, Conjecture2.7 p.512. The immediately preceding parity convention is retained. Its printed branch displays alone would give overlapping numerical labels.
- [Finster, arXiv v3](https://arxiv.org/pdf/1005.4588v3): sections3.1-3.2, Remarks3.2/3.5, printed p.20. This supports the actual double-even use through its explicit group equality statement.
- [Boulanger-Lanneau-Massart2024](https://www.numdam.org/item/10.5802/ahl.211.pdf): section1.4 p.791, general cusp correspondence; odd-family scope separated from it.
- [Hubert-Schmidt2001](https://www.numdam.org/item/10.5802/aif.1829.pdf): LemmaJ p.473 independently corroborates the balanced double cover and Veech-group isomorphism behind Finster's citation. Cached PDF SHA256 `9ce86b09a91994ed7771ed8c3469936226ac5ef787380cf34e5d3b15d37cc642`.

The original Veech1989 full text was not retrieved. The candidate transparently imports its classical theorems through later full primary mathematical papers. This is a documented access limit, not a missing even-surface theorem after the citations above.

## Falsifiable controls

`artifacts/check_geometry.py` is independent of the submission verifier and uses exact integers/rationals. All controls passed for n=3..200,297 model reflection partitions,292152 triangular/hexagonal orbit controls, and194784 square orbit controls, with primitive coordinates bounded by100.

`artifacts/physical_billiard_smoke.py` implements actual side-interior reflections and literal source type branches with parity selection. It checked704 paths for n=5,7,8,9,10,11,12,14, with up to17 segments. Worst relative variation of L/w within a selected common direction was1.9604187968365393e-14. It also supplied coordinate checks for the pentagon witness. This is floating-point falsification support only; it does not certify all-n geometry or the imported theorems.

## Strongest verified result and exact remaining scope

Conditional on the candidate's separately audited P-starting angle-index identification, the repaired geometric/cusp argument proves Fuchs's labelled ratio for every n>=3, including side boundary trajectories, the broader source parallelism, and all three exceptional cases. The repaired physical/intrinsic bridge adds no new unsupported central claim: it follows from explicit polygon-fold and endpoint-angle transformations.

No Conjecture2.3,2.4,2.6, novelty claim, historical-priority claim, whole-package R1 gate, or publication release is established by this review. No original/global candidate files were modified, no Git/tracker/publication operations performed, and no external outreach initiated.
