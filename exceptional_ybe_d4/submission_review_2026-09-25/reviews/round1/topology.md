# Independent topology and global-structure audit, round 1

Completed 2026-09-26 04:58 UTC (2026-09-25 America/Los_Angeles). Completion estimate: **100% of this bounded audit**, not a probability that the manuscript is error-free. Reviewer: independent topology/global-structure subagent. No prior review was read. No manuscript was edited, no commit/push was made, and no person was contacted.

Audited `exceptional_ybe_d4/main.tex`, SHA-256 `9ef5716ef8c663ae0cb012899b4eea67a7500fee6006e2ce0e3f61e99803f51c`, especially lines 911–1429 and the abstract/global summary. Line references below refer to that input.

## Verdict

**No substantive mathematical defect found within the assigned scope.** The site-opposite comparison, all-strand conjugacy, Clifford frame, finiteness, tower/subalgebra distinction, trace normalization, polynomial-time claim, HOMFLYPT convention, and branched-cover parity/sign are mutually consistent. This is a bounded negative audit, not a certification of the entire paper.

An optional independent proof of the already-known finite-image fact is supplied below. It removes reliance on the concurrent preprint for that consequence; it does not assert a new finite-image theorem.

## Checks against primary sources

1. [Galindo–Rowell, arXiv:2608.16865v1](https://arxiv.org/html/2608.16865v1): directly read §13.1–13.2, Theorem 7.3 and its trace proof, Theorem 7.10 and its reduction, Proposition 8.1, Lemma 8.3, and Theorem 8.4. The literal tensor placements, scalar normalization, normal basis, trace factor, fixed-data hypothesis, and exact bit-complexity claim match the manuscript. The manuscript's use of these statements is accurate.
2. [Rowell, published 2011 paper](https://ems.press/content/serial-article-files/36758?nt=1): Theorem 3.1 is the finite-image result, and **published Lemma 3.2, p. 176**, identifies the braid-generated subalgebra with the quotient. The author's older preprint numbers this lemma 3.4. The manuscript cites the published numbering correctly. Its explicit warning against identifying the full tower algebra with the braid algebra is warranted.
3. [Lickorish–Millett 1986, author's scan](https://web.math.ucsb.edu/~millett/Papers/1986Millett6LickorishCommMathHelv.pdf): inspected the actual printed pp. 353–355, including diagrams and exponent. Theorem 2 uses the cover defined by sending every oriented meridian to 1; its exponent is one-half of the mod-2 first Betti number. The dimension argument preserves parity. The manuscript's orientation convention and signed specialization match it.
4. [Turaev 1988, Göttingen scan](https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0092/LOG_0031.pdf): visually inspected printed pp. 529–532. §§2.2–2.3, the trace formula in §3.1, Theorem 3.1.2, and §3.2 are the cited definitions/results, with ordinary unnormalized trace and the manuscript's ordering of enhancement parameters.
5. [Cai–Chen–Lipton–Lu, original preprint](https://arxiv.org/pdf/1005.2632): Theorem 1.1 has the general quadratic-exponential-sum complexity asserted by the GR reduction. Its full algorithm was not re-proved in this audit; it remains an explicitly identified external theorem.

## Independent reasoning and attacks

### Local bridge and all-strand opposite, lines 1011–1063 and 1201–1263

A fresh literal SymPy encoding checked all entries of `S†S=I`, the separate U and V conjugacies through the site swap, the UV conjugacy, the intrinsic quaternionic squares/product, and the eight-term standard-frame non-Clifford witness. It imports no project verifier. All eight checks passed.

The global reversal maps the opposite two-site block at i to the ordinary GR block at n−i, so the generator relation proves the reflected-word identity. The displayed positive Garside word conjugates σ_i to σ_(n−i), not to an inverse. Consequently `D_n† Rev_n S_n` is the correct order of factors for the same-word intertwiner. Fresh exact Pauli calculations checked every such generator identity for n=2,…,7 (21 checks). The all-n proof is the generator argument, not extrapolation from these cases. The manuscript correctly does not infer a two-site common-local-basis equivalence without the opposite.

### Clifford frame and finite image, lines 1265–1307

The two quarter-turn factors have the correct order: `(I+U)(I+V)=I+U+V+UV`. Each normalizes the finite Pauli group; multiplication by κ changes no conjugation. The transported frame is fixed for each n. The manuscript's explicit standard-Pauli witness is correct; no assumption that S itself is Clifford is used.

**Optional self-contained finiteness paragraph (fully checked).** Let `G_n=ρ_n(B_n)` and let `F_n` be the displayed conjugated finite Pauli group, with scalar phases `{±1,±i}`. Conjugation gives a homomorphism `G_n→Aut(F_n)` with finite image. Because the complex span of `F_n` is the full matrix algebra, its centralizer consists exactly of scalar matrices, so the kernel consists of scalar elements `λI∈G_n`. From the eight copies of each eigenvalue, `det R=(-1)^8q^8=q²=κ`. Hence each embedded generator has determinant `κ^(4^(n−2))=κ`, since `κ³=1` and `4≡1 mod 3`. Every element of `G_n` therefore has determinant in `μ_3`. A kernel element obeys `λ^(3·4^n)=1`, leaving at most `3·4^n` possibilities. Both kernel and image are finite, hence `G_n` is finite. This works for every n≥2. Retain Rowell/GR attribution because the fact is known.

This explicitly avoids the invalid general inference “finite projective image implies finite ordinary image,” as well as the invalid inference from finite-order generators alone.

### Quaternionic tower and exact evaluation, lines 1310–1366

The two distinct assertions are correctly separated: the full twisted tower has dimension `4^(n−1)`, while the Hecke quotient is its braid-generated subalgebra. In the literal Pauli realization, the exponent of each U_i is visible in the Z label on the second qubit of site i; the exponent of each V_i is visible in the X label on the second qubit of site i+1. Thus normal-monomial labels are injective for all n, independently recovering the trace identity `Tr Φ_n=4^n ε_n`. A binary-rank test also checked this through n=100.

The normalization cancellation is exact: `R_GR=κr_0`, so the writhe scalar cancels and `κ^(−wr)2^(−n)Tr ρ_GR=2^n ε_n ρ_r0`. It is this normalized scalar quantity to which the cited metric-family algorithm applies. The metric data are fixed, rather than part of an unbounded input. A fixed number field and polynomial output bit length are addressed in GR's proof. Nothing in the manuscript claims that an exponentially sized tower-basis expansion is polynomial-time.

### Enhancement and HOMFLYPT, lines 1084–1200

The two partial traces are `2κI` and `2κ^(−1)I`; they give both Markov stabilization signs with β=2. Multiplication of the Hecke relation by `R^(−1)` gives `R−qR^(−1)=κI`. The writhe factors turn the negative-crossing coefficient into `qκ^(−2)=−1`, producing `J_++J_−=J_0`. The displayed HOMFLYPT convention at `(i,i)` has this same relation. The unknot is 2, not 1; the c-component unlink is `2^c`. Mirror invariance and three-/six-twist periodicity have the claimed signs.

### Branched cover, lines 1368–1429 and summary lines 213–218

No unoriented-cover assumption is made: the all-positive-meridian map is explicitly specified. Passing from LM's plus-plus-plus skein to the manuscript's plus-plus-minus skein requires exactly the factor `(-1)^(c−1)`, because the oriented smoothing changes component parity. There is no missing factor of i and no absolute-value-only claim. The dimension parity follows from the source's dimension calculation and the unknot base case; it is not an arbitrary choice of square root.

A separate finite-field computation tests this without using the HOMFLYPT skein. Put `ω²+ω+1=0` in F4. The closed-braid group presentation and its Fox differential give the local-system dimension `nullity(B(ω)−I)−1`, with B unreduced Burau. In the triple cover, the two nontrivial deck characters are Frobenius conjugates and have equal dimension; the trivial part is killed by branched filling. Thus `d_2=2(nullity(B(ω)−I)−1)`. This also explains parity independently. The scalar predicted by the manuscript was compared to a separately encoded exact Gaussian-integer Pauli trace.

All **511** comparisons passed. They include all printed examples, empty braid words for n=1,…,7, two-strand powers −30,…,30, 275 seeded random words with n=2,…,6, and stabilization/reflection/mirror/split-unknot variants. The example `(c,d_2,J)` triples are unknot `(1,0,2)`, 2-unlink `(2,2,4)`, Hopf `(2,0,−2)`, trefoil `(1,2,−4)`, figure-eight `(1,2,−4)`, and Borromean `(3,0,2)`.

## Evidence and boundaries

- `evidence/topology/fresh_topology_checks.py` and `.json`: standard-library-only exact arithmetic, deterministic seed 20260925, 511 comparisons, 21 Garside checks, and Pauli-label independence through n=100. **Its Pauli expansion is exponential in n and is not an implementation of the claimed efficient algorithm.**
- `evidence/topology/fresh_local_bridge.py` and `.json`: fresh eight-check literal matrix verification, SymPy 1.14.0.
- No empirical claim from these finite tests substitutes for the manuscript's all-n arguments or the cited topology/complexity theorems. The original LM proof and GR reduction were inspected; the full CCLL algorithm and foundational Markov/Fox machinery are external results, not newly certified here.
- This audit does not re-audit Sections 2–7, discovery priority, version history, or journal formatting. Its strongest result is a clean assigned-scope audit with independently reproduced algebraic and topological tests; no unresolved assigned-scope contradiction remains.

## Checkpoint log

- 2026-09-26 04:51 UTC — 55%: literal claims and primary-source theorem matching complete; no defect identified; independent computations being built.
- 2026-09-26 04:53 UTC — 85%: exact Pauli/F4 and Garside tests complete, all passed; remaining source-convention and local-bridge checks.
- 2026-09-26 04:58 UTC — 100% of bounded round-1 assignment: original Turaev scan and fresh exact local bridge checked; report saved. Optional direct finite-image proof sent to parent for manuscript revision and a separate round-2 audit.
