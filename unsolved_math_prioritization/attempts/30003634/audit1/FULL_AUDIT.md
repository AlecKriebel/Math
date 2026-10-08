# Independent mathematical audit: a third-derived pure braid outside the first solvable term

Date: 2026-10-08 UTC.

## Verdict

**ACCEPTED, with no required mathematical correction.** The frozen proof establishes an explicit element of the ordinary third derived subgroup of the classical three-strand pure braid group whose closure is not integrally 1-solvable. It therefore gives a negative answer to the universal inclusion in OWR Question 3, already at `n = 1, m = 3`. Adding split trivial strands gives the same failure at `n = 1` for every `m >= 3`.

This is an independent mathematical/source audit, supplemented by exact computer checks. It is not formal proof-assistant verification, human peer review, or a claim of historical priority. The imported signature and surgery theorems are accepted as established results after checking their statements, conventions, and applicability. No conclusion about failure at every higher filtration index is asserted.

## 1. Frozen object and audit independence

The audited author packet has 12 files, including its manifest. Its exact identifiers are:

- `PROOF.md`: 13,197 bytes; SHA-256 `0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b`.
- `MANIFEST.json`: SHA-256 `d1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a`.
- `certificate.json`: 25,068 bytes; SHA-256 `66f47cc9a4fe63a50b407808a5a7574ca0fa19ce862b70655aea24124895aa62`.

Every manifest entry was checked against its file's actual byte count and SHA-256, and the exact file set was checked for unmanifested additions. All nine referenced source PDFs matched the public byte counts and SHA-256 values in the author packet. This verifies the association with the recorded source versions; it is not a claim that every page of each source was audited.

The present review reread the complete mathematical proof and the essential source material. An existing independent characteristic-polynomial checker was inspected and rerun, rather than treating its earlier result as a completed review. Additionally, a fresh general Meyer-form checker was written for this audit. It imports neither the candidate verifier nor the earlier checker. The audit did not consult another independent mathematical review.

The author packet and earlier audit artifacts were not edited. This audit bundle contains authored discussion, authored code, exact computational results, and public verification metadata. It contains no copied papers, source extracts, screenshots, or private coordination material.

## 2. Target and conventions

The Harvey–Park–Ray contribution to Oberwolfach Report 50/2017, PDF pages 34–35, asks whether `P_m^(n+2)` is contained in `F_n^m` for `n >= 1`. Its preceding definition is the ordinary derived series, beginning with the whole group at index zero. The ambient operation is string-link stacking; a closed-link group operation is not involved. The report distinguishes its Whitney-tower result from this solvability question. [MFO report](https://publications.mfo.de/bitstream/handle/mfo/3612/OWR_2017_50.pdf?isAllowed=y&sequence=1)

The precise solvability hypotheses used in the proof agree with Otto Definition 2.3, printed pages 2631–2632: the integral first-homology isomorphism from zero surgery, an integral second-homology basis represented by framed embedded dual surface pairs, and the derived-subgroup conditions on both members at integral level one. Otto also defines string-link solvability through the ordinary closure. These conditions were checked in the PDF, including a fresh rendering of page 2632. The proof neither weakens the integral condition to a rational one nor substitutes a relative exterior-cobordism definition. [Otto](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf)

The acceptance concerns the mathematical containment question under these conventions. It does not certify catalog chronology, present worldwide openness, or all exploratory observations in the source/status discussion.

## 3. Derived membership and the specific link

Starting with `a = sigma_1^2` and `b = sigma_2^2`, define

- `c = [a,b]`, `d = a^(-1)c a`, `e = b^(-1)c b`;
- `u = [c,d]`, `v = [d,e]`, and `beta = [u,v]`;
- `[x,y] = x y x^(-1) y^(-1)`.

Both initial generators are pure. Normality of the first derived subgroup puts all of `c,d,e` in it. Therefore `u,v` lie in the second derived subgroup, and `beta` lies in the third. This is a genuine algebraic membership proof; it does not infer membership from vanishing invariants.

Independent substitution and free cancellation produce exactly the certificate's 104 Artin letters and its 23 alternating exponent pairs. The word is already in the stated alternating form. Both total generator exponent sums are zero. Independently following the strand labels returns the identity permutation and zero signed crossing sums for all three pairs. Dividing those pair sums by two therefore gives linking numbers `(0,0,0)`. The general homomorphism argument for linking numbers gives the same conclusion.

Deleting two strands from a pure braid leaves the unique one-strand braid class, so each individual closed component is an unknot. That auxiliary observation and the resulting component Arf invariants are correct, but neither is used to deduce the obstruction.

## 4. Primary signature computation

Erle's section 2 was checked in text and through fresh PDF renderings of printed pages 162–165. The displayed braid orientation and closure match the candidate. The checkerboard signs give a diagonal contribution `A_j` at the initial region of each first-generator block and a signed cycle edge contribution from each crossing in the following second-generator block. This reconstructs the entire 48 by 48 matrix. The exceptional-crossing correction is the sum of first-generator exponents, hence zero. [Erle, section 2](https://da.lib.kobe-u.ac.jp/da/kernel/E0003685/E0003685.pdf)

The author's source-indexing warning is justified. The printed off-diagonal index in Proposition 2.3, also repeated in its corresponding proof sentence, conflicts with the displayed block matrix. The correct edge sign is that of the current second-generator block. The candidate explicitly uses the crossing contributions and block picture, rather than silently following the defective index. Here there are 23 blocks and 48 regions, so small-cycle and single-generator exceptions do not enter.

Independent exact characteristic-polynomial arithmetic yields:

- positive eigenvalues: 23;
- negative eigenvalues: 25;
- zero eigenvalues: 0;
- determinant: `-7154819319988224`.

The characteristic polynomial is recorded in `INDEPENDENT_CHARACTERISTIC_CHECK.json`. Its sign-variation counts for `p(x)` and `p(-x)` are 23 and 25. Since the matrix is real symmetric, its roots are real; since these two Descartes bounds already sum to 48 and the constant coefficient is nonzero, the bounds are exact. This route does not use the candidate's Schur pivots. The fresh checker independently reconstructs the same matrix and inertia.

The author's complete rational-congruence pivot replay and fraction-free determinant calculation also pass. Thus the signature is `23 - 25 - 0 = -2`, in the stated convention. The nonvanishing conclusion would survive a uniform reversal of signature convention.

## 5. Independent Meyer cross-check and controls

Gambaudo–Ghys Theorem A supplies the negative Meyer-cocycle defect of the closed-braid signature. Their computational definition and section 4.2 give the two 2 by 2 matrices used by the candidate at `-1`; their elementary two-strand normalization agrees with positive trefoil signature `-2`. The order-two root is allowed. [Gambaudo–Ghys](https://www.numdam.org/item/10.24033/bsmf.2496.pdf)

The fresh checker uses a different implementation from the generator-specialized formulas. For each pair of symplectic matrices `A,B`, it computes the full rational kernel of

`[(A^(-1)-I) | -(I-B)]`.

A kernel vector is a pair `(v1,v2)` with common image `e`. On that kernel, the pulled-back quadratic form is `det(v1+v2,e)`. The checker verifies symmetry and explicitly verifies that the kernel of the map to `e` is in the radical. It then computes the form's signature through its characteristic polynomial. Thus a possibly redundant kernel presentation introduces only zero directions, with no spurious signature.

All 104 individual target cocycle terms agree with the certificate: 50 are `+1`, 48 are `-1`, and 6 are zero. Their sum is 2, giving signature `-2`. The exact final Burau matrix is

`[[-1401703009468415, 3686720931790848], [2187353096552448, -5753116310519807]]`.

Its determinant is 1. Also, `det(I-B(beta)) = 7154819319988224`, matching the absolute Goeritz determinant.

The fresh implementation passes 29 identity, torus-link normalization, mirror, inverse, conjugation, generator-exchange, cyclic-shift, cancellation, square, and Artin-relation controls. It also passes 192 independently reconstructed Goeritz/Meyer comparisons, including 6 singular Goeritz matrices, and 216 general Meyer cocycle identities. These are supplementary controls; the proof does not rest on random testing or floating-point signs.

## 6. Detailed audit of the 1-solvability obstruction

### Character and chain-level rank bound

Zero pairwise linking numbers and zero surgery give first homology freely generated by the meridians. The character sending every meridian to `-1` is consequently defined, and the first-homology isomorphism extends it over a hypothetical 1-solution `W`.

For a finite cellular model of `W`, the twisted cellular matrices are obtained by applying this sign character to the integral group-ring matrices. Their reductions modulo two are precisely the ordinary mod-two cellular matrices. A nonzero mod-two minor remains a nonzero odd integral minor. Consequently each twisted rational differential has rank at least its ordinary mod-two counterpart. Applying

`dim H_2 = dim C_2 - rank d_2 - rank d_3`

gives the stated upper bound on twisted second homology. The universal coefficient theorem identifies ordinary mod-two second-homology dimension with `2r`: the specified integral basis makes `H_2(W;Z)` free, and `H_1(W;Z)` is also free. There is no omitted 2-torsion contribution.

### Lifted surfaces and the boundary radical

The fundamental groups of both the Lagrangian surfaces and their duals lie in the commutator subgroup. The sign character is therefore trivial on each surface. A choice of local coefficient trivialization, equivalently an appropriate lifted surface in the double cover, produces each required twisted homology class.

The embedded and framed surface geometry is essential. Distinct pairs are disjoint, self-push-offs can be made disjoint, and a dual pair has exactly one transverse intersection. The latter contributes a unit `+1` or `-1` in the real sign local system. Rescaling one class in each pair makes that coefficient `+1`. The resulting `2r` by `2r` pairing is a direct sum of hyperbolic planes.

A nonsingular pairing on these classes proves their linear independence, even before nondegeneracy of the entire absolute intersection form is known. Combined with the rank upper bound, this makes them a basis of all twisted second homology. This addresses the boundary-radical issue: any class orthogonal to the entire space is zero because its coordinates in this basis are killed by an invertible hyperbolic matrix. No unsupported assumption that absolute intersection forms of bounded manifolds are automatically nonsingular is being made.

The ordinary surface basis likewise gives ordinary signature zero. Extending the rational sign local system to the complex unitary one preserves the displayed real form and its signature. Thus both signatures in the bounding formula are zero, including the case `r = 0`.

### Surgery formula and source hypotheses

Toffoli's equation (1.1) identifies the rho invariant of a boundary carrying an extended unitary character with ordinary minus twisted signature. His section 2.1 identifies the radical of the absolute intersection form with the kernel of the map to relative homology, consistent with the preceding argument. [Toffoli](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf)

For the one-color link, Definition 4.12 gives Seifert framing equal to minus the sums of pairwise linking numbers, hence zero here. The entire framed linking matrix is zero. Definitions 4.19, Theorem 4.24, Remark 4.25, and Corollary 4.28 apply; in particular the latter gives `rho = -sigma_L(-1)`. The character is surgery-compatible. Their domain excludes `1`, not Alexander-polynomial roots; `-1` is allowed. No nullity term or nonzero correction remains. These claims were checked in the PDF, including fresh visual inspection of Corollary 4.28. [Toffoli, section 4.4](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf)

It follows that a hypothetical 1-solution forces `sigma_L(-1) = 0`, contradicting the independently computed `-2`.

Cha's Theorem 8.2, specialized to `n=1`, prime 2, and the order-two character, provides a consistent published corroboration. Its proof uses the same underlying rank-and-duals mechanism. The elementary argument above is sufficient and does not require the general tower machinery. [Cha, section 8.1](https://ems.press/content/serial-article-files/31720)

## 7. Conclusion, replay, and limits

All three logical steps are established: actual third-derived membership; exact nonzero closure signature; and the vanishing obstruction for a hypothetical integral 1-solution. Therefore

`P_3^(3)` is not contained in `F_1^3`.

The split-strand extension is a homomorphism of pure braid groups and preserves derived membership. Its closure adds split unknots, which add no signature. This proves the stated extension to all `m >= 3` at index one. The abelian or trivial cases `m = 2,1` are correctly excluded.

The author verifier passes all 286 of its supplemental controls. The subprocess replay passes normal, `-O`, `-OO`, and `PYTHONOPTIMIZE=2` modes; rejects all 88 specified adversarial cases; and preserves the relocated read-only files byte-for-byte. These outputs are included. The fresh independent checker also reproduces its output exactly on a second run.

To replay the new controls, use Python with SymPy and run:

`python -B recovery_controls.py --packet PATH_TO_FROZEN_AUTHOR_PACKET`

The recorded execution used Python 3.12.14 and SymPy 1.14.0. The new checker writes JSON to standard output and does not change the packet.

There are no blocking corrections. An optional exposition improvement would be to state explicitly in the original proof that the full hyperbolic basis eliminates the boundary radical and that rational-to-complex scalar extension preserves the twisted signature. Both facts already follow from its written argument; this report supplies the details without changing the theorem.
