# Independent audit: triangulation obstructions in dimension five

## Decision and scope

**ACCEPT AS A VALID PARTIAL REPORT. No mathematical correction is required.**

The accepted author archive is `KIRBY_ASPHERICAL_3015_AUTHOR_SAFE_FREEZE.zip`, 11,511 bytes, SHA-256 `40ec3c8bdd4c409514a435f922b340032bb2ed3dab16663107c14524b06721a5`. Its six members are preserved byte-for-byte under `author/`. This audit does not alter that archive or retrospectively edit its author-stage pending-audit fields.

All five substantive approaches are accounted for. The results are deductions from established topology and triangulation obstruction theory. They do not construct the aspherical nontriangulable five-manifold sought by KP-5.8, prove that no such manifold exists, or establish novelty. The independent conclusion is **PARTIAL_NOT_SOLVED**.

This is a mathematical review of the stated arguments and their cited inputs, together with data-package integrity checks. It is not a formal proof certification and does not reprove the deep cited results.

## 1. Exact target and category

The complete K3 Problem 5.8 and its two remarks were inspected in the current public preliminary author PDF, including the full rendered printed page 306. The report correctly concerns a compact boundaryless topological five-manifold with vanishing higher homotopy groups and with no simplicial triangulation. The meaning of triangulation permits noncombinatorial simplicial complexes; it must not be replaced by existence of a PL structure. [K3]

Connectedness is explicit in the report. It causes no loss for the existence problem: a compact manifold has finitely many connected components, and a disconnected counterexample would have a nontriangulable component. For the characteristic-number proofs it is essential to apply the top-degree assertions component by component.

The K3 remark concerning virtual triangulability of certain four-manifolds is a separate question. Neither the five-dimensional cover formula nor the higher-dimensional construction answers that question. The author's final paragraph preserves this distinction. [K3]

## 2. Theorem 1: the full five-dimensional criterion

**Accepted.** Write Theta for the oriented integral homology-cobordism group of homology three-spheres, mu for its Rokhlin homomorphism, and A=ker(mu). Two deep inputs are being used:

1. The vanishing of the connecting obstruction delta Delta is necessary and sufficient for simplicial triangulation of a topological manifold of dimension at least five. These cohomology coefficient systems are constant. The sentence preceding Manolescu's Theorem 4.3 explicitly removes the orientability and closedness assumptions used in the preceding exposition. [MC]
2. There is no element of Theta annihilated by 2 whose Rokhlin invariant is one. This is exactly the consequence needed from Manolescu's Corollary 1.2. It is not a claim that Theta has no torsion or that a Floer invariant is an additive homomorphism. [MP]

The remaining reduction is independently valid. Choose y with mu(y)=1. The diagram comparing the integral sequence with the homology-cobordism sequence uses n↦ny in the middle and n↦2ny on the left. Thus delta x=j_*b(x), where b is the integral Bockstein and j(1)=2y lies in A. Omitting the factor of two would invalidate the diagram; the author includes it correctly.

For an orientable closed connected five-manifold, H^5(M;Z)=Z. Exactness makes b(x) a two-torsion element, so it vanishes. The triangulation obstruction therefore vanishes for every degree-four mod-two class, independently of whether the Kirby–Siebenmann class itself vanishes. The first Stiefel–Whitney class is zero as well.

For a nonorientable closed connected five-manifold, duality identifies H^5(M;B), for any constant abelian coefficient group B, with H_0(M;O_M tensor B). The orientation system introduces sign monodromy. Connectedness and the existence of an orientation-reversing loop give precisely the coinvariants B/2B. No freeness, finite generation, or absence of two-torsion in B is needed.

Naturality in the coefficient group is crucial: reduction Z→F2 induces Z/2→F2, which is an isomorphism, while j induces the map Z/2→A/2A taking 1 to 2y modulo 2A. If this last element were zero, then 2y=2a for some a∈A; hence y−a would be annihilated by 2 and have Rokhlin invariant one. This contradicts the second input. Consequently j_* is injective on the particular top-degree group at issue. Choosing a different lift y changes 2y by an element of 2A and does not affect this conclusion.

Therefore delta x vanishes exactly when b(x) vanishes, and reduction detects b(x). The identity rho b=Sq^1 proves the claimed equivalence with Sq^1x=0. The last step uses the degree-one Wu evaluation in dimension five. Since H^5(M;F2) is one-dimensional, its evaluation on the fundamental class detects its vanishing. This establishes precisely

M is nontriangulable if and only if <w1(M) cup Delta(M),[M]_2>=1.

The author does not assert an unrestricted equivalence between the two Bocksteins for arbitrary spaces or dimensions. Nor is the Wu identity used in a degree in which only an evaluation formula would be available. These scope restrictions are correct.

## 3. Product exclusion

**Accepted, including nonorientable fibers.** For a closed connected topological four-manifold X, the stable tangent microbundle of X×S1 is the pullback of that of X plus a trivial line. Both w1 and Delta pull back from X. Their cup product comes from a degree-five class on X, which vanishes. Theorem 1 consequently supplies a simplicial triangulation.

There is also a direct verification of the stated alternative proof: naturality gives delta Delta(X×S1)=p^*(delta Delta(X)), and H^5(X;A)=0. This uses the four-dimensional space's cohomological dimension, not a triangulation of X. No triangulation of X or PL structure on X is assumed. A nonzero Delta(X) can survive in the product, so simplicial triangulability here does not imply PL triangulability.

## 4. Finite-cover parity

**Accepted.** If p:N→M is a finite covering of closed connected topological five-manifolds, the stable tangent microbundle, w1, and Delta are natural under p. The mod-two pushforward of the top-dimensional fundamental class is multiplication by the number of sheets modulo two. The projection formula gives nu(N)=(deg(p) mod 2)nu(M).

It follows that every connected even-degree finite cover in this dimension is triangulable, whether the cover is orientable or nonorientable. Every odd-degree connected cover has the same triangulability status as its base. The assertion about all even degrees is stronger than the familiar orientable-double-cover consequence, but it follows rigorously from the accepted characteristic-number theorem; no orientability of N was smuggled into the argument.

Asphericity is preserved by covering because the higher homotopy groups are unchanged. These facts neither construct a quotient nor guarantee a free finite group action with the required characteristic number. They also do not establish an even-cover triangulation theorem in dimensions greater than five, where H^5 is no longer top degree.

## 5. Mapping-torus criterion and spin exclusion

**Accepted with the stated orientability hypothesis on X.** A homeomorphism of a closed connected orientable topological four-manifold gives a closed connected topological mapping torus and a genuine fiber bundle over S1. The restriction of its orientation character to the fiber group is trivial. Its value on a loop projecting once around S1 is exactly the orientation-reversal parity of the monodromy. Hence w1(T_f)=epsilon(f)q^*u; a section is not needed.

The fiber is locally flat with trivial normal line, so stability and naturality give i^*Delta(T_f)=Delta(X). Mod-two duality identifies q^*u with the fiber class, giving nu(T_f)=epsilon(f)ks(X). No assertion about the full degree-four class of the mapping torus is required.

For every k≥2, both neighboring homotopy groups of the base in the fibration sequence vanish. It follows that pi_k(X)→pi_k(T_f) is an isomorphism, including k=2. Thus asphericity of the fiber is both necessary and sufficient. Within this construction route, the three requirements stated in Theorem 4 are exactly the required ones. They are not asserted to characterize every possible counterexample to KP-5.8.

An orientation-reversing self-homeomorphism identifies the real intersection form with its negative, forcing signature zero. For a closed oriented topological spin four-manifold, the Kirby–Siebenmann number is sigma/8 modulo two. The formula was checked directly on Teichner's printed page 757 and in a rendering, avoiding reliance on the garbled fraction in text extraction. Therefore a reversing spin fiber has ks=0; a preserving monodromy already has epsilon=0. The argument does not require the homeomorphism to preserve a chosen spin structure. [T]

The assertion that a successful orientable fiber must be nonspin with zero signature is accordingly valid. The report credits the existing Kronheimer mechanism. Its known simply connected fiber has nonzero H_2, hence nonzero pi_2 by Hurewicz, so the published mapping-torus example supplies no aspherical solution. [MC]

## 6. Hyperbolization and current source scope

**Accepted as a limitation of this route, not an impossibility theorem.** The complete DFL article was reviewed. Its main existence theorem starts in dimension six. Its dimension-five paragraph distinguishes a PL resolution before hyperbolization from the needed PL resolution after hyperbolization. The original resolved four-dimensional boundary has vanishing stable Kirby–Siebenmann obstruction but does not admit a PL structure. Accordingly Delta=0 cannot replace the missing four-dimensional PL hypothesis. The author's account preserves the exact missing step and does not claim that relative hyperbolization independently repairs it. [DFL]

Lafont–Ruffoni Theorem 5.12 and its full proof were inspected in the stated 2025 revision. The theorem improves the group properties of examples in dimensions at least six. Remark 5.13 discusses odd-degree covers and the uncertainty about even-degree covers of those higher-dimensional examples. It does not contradict the top-degree five-dimensional calculation here. Its displayed target degree for Sq^1 has a typographical mismatch; the present proof uses degree five throughout. The dimension-five necessity-and-sufficiency input is correctly sourced to [MC], rather than inferred from the more restricted statement in that later remark. [LR]

Current primary-source retrieval and targeted searching located no full solution of the exact question. This is a bounded research result, not a proof that no later or unindexed solution exists.

## 7. Independent source, corpus, and artifact verification

All six cited PDFs were independently retrieved from their stated public locations on 2026-10-06. Every byte count and SHA-256 matches the author metadata. The complete selected corpus problem and its associated report were read; the report is empty and the background is literature triage. The complete-pair digest is `bbd801fb67a2840b1840235cbd05e2ad313e2aaf1807085f8f0f5d40b2248c2f`. Its exact serialization is recorded in `CORPUS_VERIFICATION.json`. No corpus contents are distributed.

The author's archive, external manifest, all six members, and internal manifest were verified independently as data. An external read-only verifier was exercised with isolated normal and optimized interpreters, with relocation and hostile local module names. Both normal and optimized test harnesses completed four positive configurations and rejected 22 deliberately corrupted fixtures. Fault-injection tests reanchor only the relevant test metadata to reach deeper checks; production validation retains the original pinned archive and manifest digests.

These tests verify integrity, not mathematics. The author bundle and this public audit bundle contain no executable payload or formal proof checker. The external verification scripts, copied source PDFs, source text, screenshots, corpus records, and private coordination material are excluded. The original author freeze remains unchanged. Nothing was published during this independent audit.

## References

- [K3] Baykur, Kirby, and Ruberman, *K3 – A New Problem List in Low-Dimensional Topology*, preliminary author version, Problem 5.8, p. 306. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [DFL] Davis, Fowler, and Lafont, *Aspherical manifolds that cannot be triangulated*, Algebraic & Geometric Topology 14 (2014), 795–803. https://msp.org/agt/2014/14-2/agt-v14-n2-p06-p.pdf
- [MC] Manolescu, *The Conley index, gauge theory, and triangulations*, updated author version, Section 4. https://web.stanford.edu/~cm5/conley.pdf
- [MP] Manolescu, *Pin(2)-equivariant Seiberg–Witten Floer homology and the Triangulation Conjecture*, Corollary 1.2. https://arxiv.org/abs/1303.2354
- [T] Teichner, *On the signature of four-manifolds with universal covering spin*, Mathematische Annalen 295 (1993), 745–759, especially p. 757. https://math.berkeley.edu/~teichner/Papers/Signature.pdf
- [LR] Lafont and Ruffoni, *Relative cubulation of relative strict hyperbolization*, arXiv v2 revised 2 April 2025, Theorem 5.12 and Remark 5.13; Journal of the London Mathematical Society 111 (2025), no. 4. https://arxiv.org/abs/2304.14946v2 ; https://doi.org/10.1112/jlms.70093
