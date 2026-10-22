# Independent audit: antisymmetric Borcherds targets 713 and 893

## Decision and scope

**ACCEPT the frozen packet as bounded arithmetic partial results. The two specified modularity identities remain UNSOLVED in this investigation. No mathematical correction to the frozen RESULT.md is required.**

The audited author manifest is SHA-256 `7162a7e1927ccaaf5454fde977da28f50d910ed695931e08431eb77d9a878991`. The audit preserves every original byte. This is an independent computational and mathematical review by a second AI agent, not human peer review, formal verification, a novelty certificate, or a proof that the broader literature contains no resolution.

This report checks every mathematical section of RESULT.md, source attribution, the numerical certificate, and executable acceptance boundaries. Its separate standard-library verifier does not import the author's code or use SymPy. It rederives the finite-field counts in a different quadratic-extension basis, computes discriminants by a fraction-free determinant, checks polynomial identities by its own arithmetic, and checks finite-field irreducibility by repeated Frobenius powering. Imported theorems are explicitly distinguished from these finite computations.

Public corpus hashes and the historical repository duplicate search are provenance metadata. This audit did not independently replay the full corpus retrieval or every historical repository search. No dataset contents, source PDF, source extract, third-party prose, private coordination, or credentials are included in this audit packet. No remote write occurred.

## 1. Exact target and source attribution

The official Oberwolfach report, printed p.1278, identifies the weight-two level-713 and level-893 constructions as conjectural paramodular correspondences. GPY §§7–8 fixes the F1 parameters, the absolute-value convention, inflation vector, and the two curves:

\[
f_{713}=x^6-2x^5+x^4+2x^3+2x^2-4x+1,
\qquad
f_{893}=x^6-2x^4-2x^3-3x^2-2x+1.
\]

The objects are the Jacobians of the smooth projective curves \(y^2=f_N(x)\), paired with the particular constructed Borcherds products. The goal is equality of the specified spin and Hasse–Weil L-functions, not merely existence of a form at the same level.

GPY Table 1 places the relevant products in the weight-two cuspidal spaces with Fricke sign −1. The author's use of that source for holomorphy and cuspidality is appropriate. The packet does not independently prove the forms are rational Hecke eigenforms, or prove a dimension statement that would imply this. Its explicit eigenform qualification is necessary and correct. BPP's proven levels 277, 353, and 587 do not supply a distinguishing-prime theorem at either new conductor.

All six local PDF byte counts and hashes agree with the author metadata. The PDFs were successfully extracted directly for inspection; the audit did not rely solely on the pre-existing text extracts. The separate BPP errata repairs the covariant-form argument and does not amend Lemma 4.1.1.

Current primary-source checks also confirmed the arXiv v1 metadata for BCGP and GPY. The published SIAM version of Gee's account is now directly readable: *Proceedings of the International Congress of Mathematicians 2026*, volume 3, pp.377–395, published online 13 July 2026. Its Theorem 1.5 retains the good-ordinary-at-3 condition. The original packet's statement that its author did not inspect the final text remains accurate as an inspection-history statement; this audit adds a later inspection.

## 2. Conductor, bad factors, and root numbers

### Smoothness and semistable reduction

The exact identities \(f=h^2+4g\) hold for

| N | h | g |
|---|---|---|
| 713 | \(x^3-x^2+1\) | \(x^2-x\) |
| 893 | \(x^3+x+1\) | \(-x^4-x^3-x^2-x\) |

Thus the models \(y^2+hy=g\) are integral. In characteristic two the common zeros of the equation and its two derivatives would force a common root of \(h\) and \((g')^2+(h')^2g\). Independent Euclidean polynomial arithmetic gives gcd 1 in each case. At infinity, the coordinates \(u=1/x,v=y/x^3\) give two points at \(u=0\), and the derivative in \(v\) is 1. This proves geometric smoothness at 2; enumerating only rational points would not have sufficed.

The independently computed sextic discriminants are
\[
\operatorname{disc}(f_{713})=2920448=2^{12}\cdot23\cdot31,
\quad
\operatorname{disc}(f_{893})=3657728=2^{12}\cdot19\cdot47.
\]
At all remaining odd primes outside the displayed pairs the standard two-chart hyperelliptic models are smooth. At each listed bad prime the gcd with the derivative is exactly linear, the residual quartic after dividing by the squared linear factor is squarefree, and its value at the double root is nonzero:

| N | p | r | quartic g_p in F_p[x] | g_p(r) | #E_p(F_p) | epsilon |
|---|---:|---:|---|---:|---:|---:|
| 713 | 23 | 7 | \(x^4-11x^3+5x^2-10x+8\) | 7 | 20 | −1 |
| 713 | 31 | 15 | \(x^4-3x^3-4x^2-x+4\) | 2 | 39 | +1 |
| 893 | 19 | 4 | \(x^4+8x^3+8x^2-9x+6\) | 11 | 25 | +1 |
| 893 | 47 | 7 | \(x^4+14x^3+4x^2-21x-23\) | 38 | 51 | −1 |

Each special fiber is geometrically irreducible with one ordinary node and elliptic normalization \(z^2=g_p(x)\). The squarefree quartic cannot be a square in the rational function field, so the normalization is connected. The two infinity points are rational and smooth. This supplies a semistable curve model and a dual graph with one loop. Standard semistable-Jacobian theory then gives toric rank one, vanishing Swan conductor, and conductor exponent one. The author does not conflate curve discriminant and Jacobian conductor. The conductors are therefore precisely \(23\cdot31=713\) and \(19\cdot47=893\).

### Local factors and signs

Let epsilon be the splitting character of the node, equivalently the quadratic character of \(g_p(r)\), and let \(a_E=p+1-\#E_p(\mathbf F_p)\). The graph and elliptic contributions to inertia invariants give
\[
P_p(T)=(1-\epsilon T)(1-a_ET+pT^2).
\]
The independently verified factors are

| N,p | P_p(T) |
|---|---|
| 713,23 | \((1+T)(1-4T+23T^2)\) |
| 713,31 | \((1-T)(1+7T+31T^2)\) |
| 893,19 | \((1-T)(1+5T+19T^2)\) |
| 893,47 | \((1+T)(1+3T+47T^2)\) |

The local root number at such a node is \(-\epsilon\). Good finite places contribute +1 and the real place contributes \((-1)^2=+1\). Consequently both global signs are −1. This is a surface-side assertion; it does not prove matching automorphic factors or analytic rank exactly one.

## 3. Simplicity and geometric endomorphisms

The good Frobenius polynomials at 11 for 713 and at 5 for 893 are respectively
\[
Q_{713,11}=X^4-2X^3-6X^2-22X+121,
\quad Q_{893,5}=X^4+4X^3+11X^2+20X+25.
\]
They agree with the independently counted local data, not merely with separately hard-coded simplicity labels. The first is irreducible modulo 3: the repeated-Frobenius criterion checks no factor of degree one or two and \(X^{3^4}=X\) modulo the polynomial. Hence it is irreducible over Q.

For the second, Gauss's lemma reduces a rational factorization to integral monic factors. Testing all signed divisors of 25 excludes a linear factor. In a quadratic factorization \((X^2+uX+a)(X^2+vX+b)\), one must have \(ab=25\), \(u+v=4\), \(uv+a+b=11\), and \(ub+va=20\). Up to interchange the four constant pairs are \((1,25),(5,5),(-1,-25),(-5,-5)\). The first requires nonintegral \(u=2/3\); the second requires sum 4 and product 1, with nonsquare discriminant 12; the third gives \(u=-1,v=5\) and the wrong middle coefficient; the last gives the wrong coefficient of X. All possibilities fail.

If a Jacobian were not Q-simple, Poincare reducibility over Q would give an isogeny to two elliptic curves. At any good prime their Tate modules would be unramified direct summands, so the Frobenius polynomial would factor into two rational integral quadratics. These irreducible examples exclude that possibility. This proves Q-simplicity, not geometric simplicity by reduction alone.

BPP Lemma 4.1.1 now applies exactly: the surfaces are Q-simple, semistable, and have nonsquare conductor. Its conclusion is \(\operatorname{End}_{\overline{\mathbf Q}}(A)=\mathbf Z\). The cited proof uses the endomorphism classification and conductor multiplicities to obtain \(\operatorname{End}_{\mathbf Q}(A)=\mathbf Z\), then Ribet's semistable descent result to identify all geometric endomorphisms with those over Q. This imported lemma is correctly credited, and avoids a stronger unproved inference from one irreducible reduction.

## 4. Mod-2 representations

At level 713 the exact cubic factors are \(x^3+x^2-1\) and \(x^3-3x^2+4x-1\). Neither has a rational root. Their discriminants are −23 and −31, and their resultant is 64. Each splitting field has group S3. The intersection is Galois over Q and gives a common quotient of S3. A nontrivial quotient would force a common quadratic subfield, contradicting \(\mathbf Q(\sqrt{-23})\ne\mathbf Q(\sqrt{-31})\). Hence the compositum group is S3 × S3 on the two triples.

The standard Jacobian 2-torsion model is the even-sum subspace of \(\mathbf F_2^6\), modulo the all-ones line. The sum of the two even-sum spaces on the triples has dimension four and meets that line trivially. It therefore maps isomorphically onto the quotient and gives the asserted invariant 2+2 decomposition.

For 893, multiplication, squarefreeness, and irreducibility of every certificate factor were checked independently at 3, 7, and 349. The degree patterns are 6; 1+5; and 1+1+1+1+2. They give a transitive group containing a 5-cycle and a transposition. A nontrivial block system in degree six has block size two or three. An order-five permutation can act neither on the two or three blocks nor inside those blocks, contradicting the 5-cycle. Thus the group is primitive. The graph of conjugate transpositions is connected because its connected components are blocks. Transpositions along a connected graph generate S6, proving the group is S6.

The even-subset quotient identifies this faithful S6 action with the natural Sp4(F2) action. Absolute irreducibility follows directly from symplectic transvections: a nonzero invariant subspace over an algebraic closure contains a rational nonzero vector obtained by subtracting its image under a suitable rational transvection; transitivity on nonzero rational vectors then forces the full space. The argument in RESULT.md is valid.

These statements identify surface representations. They do not identify the residual representation of either specific Borcherds eigenform, whose eigenform status has not itself been imported or proved.

## 5. Borcherds inputs, character, and normalization

The F1 coefficient matrix and inflation vector in the independent verifier were checked against GPY §7. Applying the source's componentwise absolute values gives two zero entries in all three cases, hence weight 2. All zero positions have inflation factor 1, so m=1. The nonzero multisets for the two 713 parameters agree both before and after inflation, exactly as stated in RESULT.md.

The independent verifier additionally checks GPY's finite Laurent-polynomial identity without division: with \(t=\zeta^{1/2}\), it multiplies the baby theta block for phi by the prescribed polynomial in the first two elementary symmetric sums of \(t^{2d}+t^{-2d}\), and obtains the inflated baby block for Xi. This is an exact identity for all three inputs, not a Fourier cutoff. The ordinary and inflated indices are \(N\) and \(2N\); the leading q-order is 2.

The multiplier and normalization details can be made fully explicit. For each theta block, the eta multiplier exponent is \(2k+2\ell=48\), and the sum of its entries is even, so the Heisenberg multiplier is also trivial. The Jacobi quotient has principal expansion
\[
\psi=q^{-1}+4+\sum_{d>0}(\zeta^d+\zeta^{-d})+O(q),
\]
where repeated entries contribute with multiplicity. Thus the Borcherds weight is \(c(0,0)/2=2\), its Weyl data are
\[
(A,B,C)=(2,75,713)\quad\text{for both 713 entries},
\qquad (A,B,C)=(2,84,893)\quad\text{for 893},
\]
and its character on K(N) is trivial. The negative q-part contributes D0=1; therefore the Fricke sign is \((-1)^{2+1}=-1\).

The source's product convention fixes the scalar by its explicit product and leading Fourier–Jacobi coefficient phi. The two 713 parameterizations have exactly equal phi and Xi, so they have equal psi, equal Weyl prefactor, equal individual product exponents, and equal normalization. They are the same form, not merely proportional or equal in weight and level. No sign ambiguity survives the source's positive-entry convention. Holomorphy and cuspidality still rely on the cited GPY result; indices and multipliers alone would not prove them.

## 6. All twenty good-prime factors

For \(n_r=\#C(\mathbf F_{p^r})\), the independently enumerated counts give
\(a=p+1-n_1\), \(b=(a^2-p^2-1+n_2)/2\), and
\(P_p(T)=1-aT+bT^2-paT^3+p^2T^4\).
Every row below agrees exactly with certificate.json.

| p | n1,n2 for 713 | a,b for 713 | n1,n2 for 893 | a,b for 893 |
|---:|---|---|---|---|
| 2 | 6,6 | −3,5 | 6,6 | −3,5 |
| 3 | 7,13 | −3,6 | 6,12 | −2,3 |
| 5 | 9,37 | −3,10 | 10,32 | −4,11 |
| 7 | 9,49 | −1,0 | 9,63 | −1,7 |
| 11 | 10,106 | 2,−6 | 12,160 | 0,19 |
| 13 | 15,133 | −1,−18 | 15,143 | −1,−13 |
| 17 | 24,330 | −6,38 | 18,326 | 0,18 |
| 29 | 31,881 | −1,20 | 30,748 | 0,−47 |
| 37 | 40,1330 | −2,−18 | 52,1390 | −14,108 |
| 41 | 44,1788 | −2,55 | 41,1747 | 1,33 |

The author's two odd-characteristic methods share a field-arithmetic implementation. This is reasonable internal cross-checking, but not complete computational independence. The audit supplies an independent implementation using \(u^2+u+c\) instead of \(u^2=d\), square-fiber enumeration rather than the norm-character formula, and no author imports. Binary fields are handled separately by the integral models.

## 7. Exact modularity-theorem boundaries

At 3 the Frobenius polynomials factor as
\[
Q_{713,3}=(X^2+3)(X^2+3X+3),
\qquad Q_{893,3}=(X^2-X+3)(X^2+3X+3).
\]
The corresponding normalized Newton slopes are respectively \((1/2,1/2,1/2,1/2)\) and \((0,1/2,1/2,1)\). Both surfaces have good reduction at 3, but neither is ordinary. Their p-ranks are zero and one. Newton slopes are invariant under isogeny and finite extension; a quadratic twist retaining good reduction has the same slopes after a field extension trivializing the twist. The stated obstruction therefore survives those changes.

BCGP Theorem A requires a prime-to-3 polarization, surjective mod-3 image, a specified unramified local mod-3 condition at 2 excluding two repeated-quadratic characteristic polynomials, and good ordinary reduction at 3 with distinct Frobenius roots. BCGP Theorem 9.5.2 weakens the residual image hypothesis to its enumerated subgroup list together with the endomorphism condition; it still requires the local condition at 2 and good ordinary, 3-distinguished reduction at 3. The known failure of ordinarity already prevents both direct applications. The audit does not claim to have established their mod-3 image hypotheses. Gee's Theorem 1.5, including its published 2026 version, has the same decisive obstruction.

At 2 both surfaces are ordinary, since their middle coefficient is 5. BCGP Theorem 8.3.2 additionally requires residual image between the designated A5 and S5 subgroups, a specified nontrivial complex-conjugation class in A5, and ordinary, 2-distinguished local representation. S3 × S3 has order 36 and cannot contain A5; S6 has order 720 and cannot be a subgroup of S5. Therefore the image condition fails for both, independently of the other requirements.

There is an important positive qualification: **BCGP Theorem 10.3.9 does apply to their mod-2 residual representations.** Good ordinary reduction at 2 provides an ordinary finite-flat, Cartier-self-dual model through the principal polarization. Good reduction at 3 gives unramified mod-2 representation, and Frobenius at 3 is nontrivial: for 893 its sextic is irreducible modulo 3, while at 713 its first cubic factor is irreducible modulo 3. The theorem consequently gives abstract ordinary residual modularity of weight two and level prime to six. It does not give a characteristic-zero identification of the original surfaces or of the specified Borcherds forms. The further hypotheses of the broader lifting theorem, especially Proposition 7.5.10 in characteristic two, have not been established here. One must not broaden the packet's direct-obstruction claims into a statement that every result in BCGP is inapplicable.

The level-713 polynomial on BCGP printed p.221 is the reciprocal \(X^6f_{713}(1/X)\). The coordinate change extends from the affine birational map to the smooth projective curves. Its occurrence is a local construction in the proof of Lemma 10.3.6, not a proof of modularity of this original surface. RESULT.md correctly distinguishes those roles.

## 8. Finite agreement and the missing global argument

The twenty factors are entirely surface-side. The packet supplies no independently calculated matching automorphic Euler data. The author reports the Ryan–Tornaria L-series directory to be curve-derived. This audit's direct web read of that directory failed, so that specific directory inspection remains an author-reported provenance claim; it is not needed for any accepted arithmetic result. No conclusion here depends on its uninspected Fourier coefficient file.

The quadratic-twist negative example is mathematically sound. If \(q\equiv1\pmod{8\prod_{p\in S,\,p\text{ odd}}p}\) is a new prime outside the conductor, the q-twist has trivial local twisting character at every p in S. At q it twists an unramified four-dimensional representation by a nontrivial tame quadratic character, removing all inertia invariants and adding conductor exponent four. At the old bad primes the twist is unramified, so their conductor exponents remain one. Thus the conductor is Nq^4, not N. The checked prime 120121 satisfies the claimed congruence for S={2,3,5,7,11,13}. Dirichlet's theorem supplies infinitely many such primes for any finite S.

The example refutes an unrestricted finite-agreement-to-isogeny inference. It does not refute uniqueness at a fixed conductor, and does not refute paramodularity. RESULT.md states these limits correctly. A valid completion still needs certification of the specific eigenforms, the appropriate residual identification, a conductor-specific comparison theorem with controlled discrepancy extensions, and the exact required Hecke comparisons. Neither more unstructured surface counts nor abstract residual modularity supplies those steps.

## 9. Executable controls and acceptance limits

The original verifier passed in normal, −O, and −OO modes. Its supplied controls produced three relocated positive passes, 21 repinned mathematical rejections, and 15 integrity rejections. Independent controls produced three positive passes and **87 rejections**: 29 malformed or false claims in each interpreter mode. These cover status, approach count, boolean/float scalar substitution, counts, factors, ordinarity, signs, normalization, groups, factor witnesses, weights, indices, multipliers, theta entries, q-order, simplicity, twist conductor, missing/extra claims, duplicate JSON keys, nonfinite numbers, truncated JSON, and a nonobject root.

Both verifiers also passed all three interpreter modes in a genuinely read-only root filesystem mount; an explicit write probe failed with EROFS. Temporary storage was separate. A separate network namespace was unavailable because NETLINK_ROUTE was denied; it is not claimed. Neither verifier makes network calls, and the successful arithmetic replay needs no network or private source files. The source-PDF check and source inspection were separate audit operations.

The author's JSON parser uses Python's default last-key-wins behavior for duplicate keys. The externally pinned frozen bytes contain no duplicates, so this does not undermine the frozen acceptance. The independent parser deliberately rejects duplicate keys and nonfinite numbers even in an unpinned separate claim file. This is a hardening qualification rather than a mathematical erratum. Cryptographic inventory checks establish identity, not the truth of arbitrary edited proof prose; neither verifier is a formal proof checker.

The original archive passed its CRC and contained byte-for-byte copies of the nine frozen public files. After the audit, the original public inventory and externally pinned manifest still match. The audit's acceptance remains limited to the mathematical partials and precise unresolved disposition stated above.

## Sources

- [Oberwolfach Report 23/2016, *Moduli spaces and Modular forms*](https://ems.press/content/serial-article-files/46626), printed pp.1275–1278.
- [Gritsenko–Poor–Yuen, *Antisymmetric Paramodular Forms of Weights 2 and 3*](https://arxiv.org/abs/1609.04146), §§2–3, 5, 7–8; [journal DOI](https://doi.org/10.1093/imrn/rnz011). Author-preprint bytes inspected; final journal full text not inspected.
- [Brumer–Pacetti–Poor–Tornaria–Voight–Yuen, *On the paramodularity of typical abelian surfaces*](https://msp.org/ant/2019/13-5/ant-v13-n5-p05-p.pdf), especially Lemma 4.1.1 and §7; [2020 errata](https://msp.org/ant/2019/13-5/ant-v13-n5-x05-Errata-Paramodularity.pdf).
- [Boxer–Calegari–Gee–Pilloni, *Modularity theorems for abelian surfaces*](https://arxiv.org/abs/2502.20645), v1, Theorems A, 7.5.11, 8.3.2, 9.5.2, and 10.3.9, Proposition 7.5.10, Lemma 10.3.6; [inspected author PDF](https://www.math.uchicago.edu/~fcale/papers/Modular.pdf).
- [Gee, *Modularity Theorems for Abelian Surfaces*, ICM 2026 proceedings](https://epubs.siam.org/doi/10.1137/25M1806697), pp.377–395, Theorem 1.5. Published HTML and the separately pinned [preprint](https://arxiv.org/abs/2510.02756) inspected.
