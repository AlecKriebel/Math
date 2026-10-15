# Independent adversarial audit: optimal uniform reduced Hurwitz lifting

Problem 30000403 / OWR-1188-004, rank 655. Audit date: 2026-10-04 UTC.

## Verdict

**PASS, with nonblocking presentation and literature notes.** No mathematical error was found in the frozen proof of the uniform bound `m_k(x) <= 2`, its optimality, or the stronger `m_k(x)=1` assertion when the geometric base stabilizer is `V4`.

The supported disposition remains **claimed_solved, 3/5 author turns**, now with an independent AI audit. This is not external human peer review, formal verification, a novelty certification, or a claim that every fixed Hurwitz datum has optimal bound 2. No remote write was performed. The frozen author packet was not edited.

The audit was performed without delegating any part to another helper. It consisted of a full reading of the proof, independent source retrieval, reconstruction of the descent argument, replay of both supplied controls, newly written exact controls using different algorithms, and an adversarial literature search for counterexamples.

## 1. Binding and source identity

The exact inputs are bound in FROZEN_INPUT_VERIFICATION.json and AUDIT_MANIFEST.json:

- AUTHOR_FREEZE.json: SHA-256 `060a5eecbd96bacd4ca3e54efe4b3d309c1eae177980281b47a97dace0894d0b`.
- author-packet.zip: SHA-256 `c8c844e5d1f5ebbfb180ac025e2cd8aad764297f69ef86f8e3f335e678f25e7e`.
- PROOF.md: SHA-256 `20cb77c2ac8befd8d2f9be9a421d2925580c29e24002a1abc8e3dedb13caeb5a`.

All ten packet files match the author's declared sizes and hashes and their ZIP members. The standalone freeze also matches its ZIP member. Reverification is supplied by verify_audit.py.

Two primary PDFs were downloaded afresh. The 2006 report is 558,725 bytes, SHA-256 `803471040d06fcc1f83d5a0bd605e72bfd3a61434ee2a3dcd5259c48e2869412`. The Cadoret manuscript is 341,279 bytes, SHA-256 `705e6ec3b07bb11140f05ac70467ab96456f0ba444805e905ee60b188d402f76`. Both match the author's metadata; fresh text extraction matches the supplied private extraction.

Inspected primary-source scope: the 2006 contribution, printed pp. 325-328, asks for an optimal upper bound on the residue-field degree of an ordinary coarse Hurwitz point over a reduced point. It assumes characteristic zero and subsequently r >= 3. Its groupoid retains the G-marking. The problem is not a request for actual cover models over the same extension. The reported proof has those hypotheses. Printed p. 326 was visually inspected after fresh rendering. [Report](https://publications.mfo.de/bitstream/handle/mfo/2936/OWR_2006_06.pdf?isAllowed=y&sequence=1).

Manuscript sections 1-3, particularly Lemma 2.1, Lemma 2.3, Proposition 2.4, Corollaries 3.9/3.11 and Remark 3.14, were checked against the proof's uses. Pages 5 and 15 were visually inspected. The reference supplies the required standard representatives, normalizers and obstruction framework; it does not state the new packet's full uniform result. Proposition labels refer to this manuscript, not a certified comparison with publisher typesetting. [Manuscript](https://webusers.imj-prg.fr/~anna.cadoret/GPGL2.pdf). The publisher confirms Israel Journal of Mathematics 164 (2008), 19-59: [publication](https://doi.org/10.1007/s11856-008-0019-0).

The live catalogue URL was attempted and returned HTTP 403; web retrieval also failed. The privately available record matches the primary problem in mathematical scope. The large catalogue corpus itself was not independently rehashed in this audit; its global hash remains author-supplied metadata. Historical repository readiness/queue assertions were not re-audited. These limitations do not affect the proof/source match.

## 2. Statement audit

The minimum over closed points and the minimum over finite extensions admitting a rational point agree: a K-point has a residue field embedded in K, and a closed point of this finite-type k-fiber has finite residue degree. Characteristic zero removes inseparability issues. The notation correctly uses residue fields relative to the selected k, rather than presuming k is the smallest possible absolute field of definition.

The branch divisor has r distinct points. Its stabilizer is finite for r >= 3; the cover-point stabilizer is a subgroup of it because the branch morphism is PGL2-equivariant. A projective transformation acting trivially on those r points is identity. Thus no positive-dimensional stabilizer was omitted.

The proof only changes the target coordinate. It keeps the connected cover, the deck-group marking, the inertia data and the coarse inner moduli problem. A k-fixed geometric coarse point need not come from a G-cover object over k. The proof never uses this false implication.

The theorem is an optimal *universal constant*. It does not determine the least degree for every individual point or the optimum after fixing k, G, C and r. The author's explicit exclusions are necessary and accurate.

## 3. Normalizer reduction and orientations

Set H=PGL2(kbar), with the stated left action. Conjugate the stabilizer to a Galois-stable standard subgroup E. If sigma(p0)=a_sigma^{-1} p0, then its stabilizer is both E and a_sigma^{-1} E a_sigma; hence a_sigma is in N=N_H(E).

If another choice a'_sigma works, then a'_sigma a_sigma^{-1} is in E, so the quotient c_sigma=a_sigma E is independent of choice. Applying sigma to tau(p0) gives

    (sigma tau)(p0) = (a_sigma sigma(a_tau))^{-1} p0.

Consequently c_(sigma tau)=c_sigma sigma(c_tau), with the standard cocycle direction. A finite extension defining p0 has an open stabilizer; the quotient-valued transition function is therefore continuous. A finite collection of transition maps can be selected and put in a finite extension.

For a coboundary b_sigma=h^{-1}sigma(h) in N with b_sigma E=c_sigma, the product b_sigma a_sigma^{-1} lies in E. Thus sigma(h p0)=h p0. This produces a rational *point*, requiring no compatible choices of source-curve isomorphisms.

The adjustment from cohomology classes is also correct. If p(b_sigma)=q^{-1}c_sigma sigma(q), choose n in N mapping to q and replace h by h n^{-1}; the new coboundary is n b_sigma sigma(n)^{-1}, whose quotient is c_sigma. No inverse or multiplication order needs correction.

## 4. Stabilizers other than V4

- **E=1:** N=H and the quotient cocycle is a genuine PGL2 cocycle. Its class is a genus-zero form of P1, equivalently a conic. A k-line meeting a smooth plane conic transversely supplies a separable degree-two divisor. Since k is infinite, such lines exist. Its support contains a point of degree 1 or 2; over that field the conic is split. The argument uses the index bound for a conic, not a period-index assertion for arbitrary 2-torsion Brauer classes. No extra field extension must be multiplied into the bound.
- **E=S4,A5:** N=E, so the quotient is trivial and p0 is already fixed.
- **E=A4 or D_(2n), n>=3:** N/E has order 2 and therefore trivial Galois action. Killing its character requires degree at most 2. The proof does not presume a Galois-equivariant splitting of N -> N/E. Odd dihedral strata have stronger known results, but omission of those improvements does not weaken the universal theorem.
- **E=C_n, n>=2:** Both N and N/E are the split group kbar^* semidirect C2; the quotient map on the torus is the nth-power map. Restricting to the kernel of the component character gives degree at most 2 and leaves a usual multiplicative cocycle. Hilbert 90 kills it over that same field. This is not a successive pair of quadratic extensions. C2 is included correctly.

This list is exhaustive in characteristic zero, with D4=V4 separated from the other dihedral groups.

## 5. The V4 improvement

This is the substantive point most likely to conceal an error. It withstands the following checks.

### 5.1 The quotient action is constant, although the normalizer is not

For E0={z,-z,1/z,-1/z}, all four transformations are k-rational. Conjugation N -> Aut(E0) has kernel E0 and is surjective. Therefore N/E0 is the constant S3, equivariantly. The statement is about a group with Galois action, not an assertion that N is constant over k.

The independent control constructs the 24 projective matrices generated by z -> i z and z -> (z+1)/(z-1) over Q(i). It verifies all six quotient permutations and that complex conjugation fixes each quotient class. Only eight of the 24 projective matrices are Q-rational. In particular, a rational group-theoretic section cannot be assumed; the proof correctly avoids one.

### 5.2 Every cocycle, including full S3 image, has the required realization

A cocycle into constant S3 is a continuous permutation action on three elements, hence a degree-three finite etale algebra. Over the infinite field k a generator with three distinct geometric images exists. Its characteristic polynomial is a separable monic cubic F.

The elliptic curve Y^2=F(X) has a rational origin at infinity. Translation by each nonzero 2-torsion point commutes with negation because T=-T. It therefore induces an automorphism of the *split* x-line P1_k after base change. The three descended translations and identity give a Klein four subgroup E'. Nontriviality and distinctness can also be read from the matrices: each has lower row (1,-e_i), and distinct roots give distinct projective matrices.

The formula M_i=[[e_i,F'(e_i)-e_i^2],[1,-e_i]] is the same as the packet's formula. Its determinant is -F'(e_i), its square is F'(e_i) times identity, and distinct nonidentity elements multiply to the remaining one. The coefficients involving the other two roots are symmetric. Hence sigma(M_i)=M_sigma(i), as projective transformations. The new symbolic control checks these identities for generic roots and every permutation, independently of the supplied script.

The four possible subgroup-image types 1, C2, C3 and S3 are separately exercised by rational cubic examples. In particular, t^3-t-1 has full S3 Galois group. The proof does not tacitly assume a cyclic or split cubic algebra.

### 5.3 Labeling and the coboundary direction

Choose h with h E0 h^{-1}=E', matching the specified root labels. Every labeling is obtainable because the geometric normalizer surjects onto Aut(E0). For e in E0,

    sigma(h) e sigma(h)^{-1} = h c_sigma(e) h^{-1}.

Multiplying by h^{-1} and h proves that b_sigma=h^{-1}sigma(h) normalizes E0 and acts on it as c_sigma, not its inverse. The kernel of N -> Aut(E0) is E0, so b_sigma E0=c_sigma. This is precisely the lifting criterion in section 3.

There is no demand that h be rational, quadratic, or in N. It can require a much larger auxiliary field. The *resulting moduli point* h p0 is k-rational. Confusing those two fields would incorrectly reject this argument.

Thus the V4 stratum really has m=1. The construction gives a lift whose PGL2 class vanishes, rather than merely any lift to N or a degree-six field killing c.

## 6. Sharpness audit

The six points 0,infinity,1,-1,2+2i,-(1+i)/4 are distinct. The degree-five squarefree right side of the displayed double cover gives precisely those six branch points and a connected genus-two curve. Over an algebraically closed field, an even reduced branch divisor on P1 determines its connected double cover up to target-preserving isomorphism. Since C2 has no nontrivial marking automorphism, the cover-point base stabilizer equals the divisor stabilizer here.

The newly written checker does not import either author program. It imposes all six projective point correspondences as a homogeneous linear system in four matrix entries, for **all 720 permutations**. For the sharp example, 719 systems have rank 4 and only the identity permutation gives rank 3 with an invertible matrix. For the negative control a=2+i, exactly two permutations survive. This independently confirms both the lower-bound certificate and the original rejected control.

The checker also reconstructs each four-point binary quartic, calculates its classical degree-two and degree-three invariants, and obtains the j-value without using the author's cross-ratio implementation. All 15 values match the frozen certificate and are pairwise distinct. The invariant argument's implication from fixed four-subsets to fixed two-subsets to identity is valid.

The antipodal conjugation tau(z)=-1/conjugate(z) preserves D. Therefore the reduced C2 point is Q-rational. If a point in its fiber were real, its branch divisor would be a real divisor h(D), even if no cover model existed over R. Pulling back ordinary conjugation gives rho=h^{-1} j h preserving D. The composition rho tau^{-1} is a projective automorphism of D and hence identity. This is impossible: rho has a fixed circle whereas tau has no fixed point. Thus there is no real, and in particular no rational, coarse lift. The Q(i)-model supplies a degree-two lift, proving m_Q=2.

As a separate check of the conic geometry, the audit verifies the parametrization [u:v] -> [u^2-v^2:i(u^2+v^2):2uv] of X^2+Y^2+Z^2=0 over Q(i). Coefficient conjugation corresponds projectively to the antipodal involution. This conic has no real point and splits over Q(i), exactly the type of obstruction used in the example.

## 7. Adversarial literature check

A targeted search found an apparently conflicting older claim by Fuertes and Gonzalez-Diez: a hyperelliptic family with reduced V4 and a minimum real hyperelliptic definition field of degree three. It is unsafe to treat that abstract as a counterexample. The authors' corrigendum restricts the assertion by requiring a specified field of definition for the *isomorphism*. The publisher confirms the erratum at Archiv der Mathematik 101 (2013), 599-600. [Erratum record](https://link.springer.com/article/10.1007/s00013-013-0582-4), [author corrigendum](https://verso.mat.uam.es/~gabino.gonzalez/Corrigendum.pdf). The author's indexed text was read; direct byte retrieval failed with HTTP 502, so no PDF hash is invented.

Independently, Lercier, Ritzenthaler and Sijsling, section 3D, printed pp. 483-484, identify the error and explicitly descend the genus-five family to Q. This resolves the apparent contradiction by a second primary source. [Published paper](https://msp.org/obs/2013/1-1/obs-v1-n1-p23-s.pdf). Its large formulas were not copied into the audit or used as proof dependencies.

Hidalgo's 2013 and 2022 related manuscripts were checked only for context. The older arXiv identifier was withdrawn in July 2026 with a duplicate-print explanation pointing to the 2022 identifier; this is recorded as publication-status context, not evidence against the theorem. The related cyclic/hyperelliptic results do not by themselves certify a prior general marked-Hurwitz theorem. No exhaustive novelty conclusion is made.

## 8. Replays and reproducibility

- verify.py: passed; 1,754 exact assertions; output byte-identical to CONTROL_RESULTS.json.
- verify_symbolic.py: passed; 32 assertions; output byte-identical to SYMBOLIC_RESULTS.json.
- independent_checks.py: passed; 96 audit assertions, 720 full-correspondence systems per configuration, 15 binary-quartic calculations, 24 normalizer elements, generic V4 identities, all cubic action types, and an explicit conic check.
- Runtime: Python 3.12.14; SymPy 1.14.0.

The initial independent script used an unsupported conjugate method on a SymPy Gaussian-domain element and stopped before checks; it was corrected to use the domain conversion. This was an audit implementation issue and changed no author input. The final script was rerun successfully. Finite checks do not prove classification, Hilbert 90, existence/effectivity of the coarse spaces, or the universal descent argument; those are separately reviewed above.

CORRECTIONS.md is separate and contains only nonblocking recommendations. It does not silently alter the frozen proof. The portable packet contains original audit analysis, code, finite results, hashes, byte counts and public bibliographic metadata. It excludes source PDFs, extracted text, screenshots, catalogue contents and private coordination material.
