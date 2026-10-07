# Independent full-proof and arbitrary-scope audit of Roydor

Audit date: 2026-10-07. Checkpoint time: 2026-10-07 14:04:23 UTC.

## Verdict and scope of this audit

**Roydor's printed Theorem 1.2 has a separable-predual hypothesis. Consequently, a bare citation of that theorem plus family 295 does not establish the original arbitrary-von-Neumann-algebra target.** The cohomology input itself has the required ordinary bounded, complex-linear, self-coefficient, actual-image conventions. Vanishing in degree three implies the closed-range hypothesis Roydor uses.

There is, however, a checkable way to remove separability using Roydor's geometric results and an explicit involution-preserving multiplication correction. It uses two fixed source algebras, not a directed system of separable subalgebras and not perturbation constants for moving central corners. The detailed argument appears below. Subject to the upstream cohomology theorem and the stated geometric results of Roydor, it establishes both original targets for arbitrary, possibly nonseparable M. The argument does not need Roydor's Theorem 1.1 or Lemma 4.3.

This is an independent dependency/proof audit and a candidate scope-removal proof, not a complete publication review or an independent re-proof of all of family 295. I read the original PROJECT_BRIEF.txt and AGENTS.md, all 26 pages of the supplied Roydor text, and the upstream introduction and full cohomology/reduction section. I did not read other new agents' reports before these findings. The introduction's walk/Liouville/rigidity dependencies were identified but their full probabilistic proofs were not re-audited here. No formal build was reproduced. No Git, publication, manuscript edit, or external communication occurred.

Checkpoint estimates: complete-source scope audit 100%; candidate scope-removal proof 90% pending fresh adversarial verification; full original mathematical objective not certified by this audit alone; publication readiness not assessed.

## Source identity

Supplied file: `sources/roydor/roydor2020_user_supplied.pdf`.

- SHA-256: `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`.
- Full extracted text SHA-256: `30fb985def03134ed115779e02a70e95432bd21bcf005c5bb3232cbd91f4414e`.
- 26 pages, typeset with a “2nd Reading” / December 9, 2020 header.
- Jean Roydor, *Banach–Mazur stability of von Neumann algebras*, DOI `10.1142/S1793525321500151`. Page 1 gives received 18 May 2020, revised/accepted 26 August 2020, published 11 December 2020. This supplied reading proof is complete; I did not byte-compare it to the final 2022 journal issue.
- Pages 15 and 20 were also rendered and visually inspected to distinguish actual printed errors from extraction errors. The temporary renders are not publication artifacts.

Read-only upstream clone: `/Users/alec/Desktop/math`, HEAD `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

Upstream source directory: `preprints/Vanishing-of-higher-bounded-Hochschild-cohomology-September-23-2026`.

- `build/sections/01-introduction.tex`: SHA-256 `ddec01dc15fa257e3f1e85004b54225dd43df633bbdfa957de98353c069ce4b2`.
- `build/sections/05-cohomology.tex`: SHA-256 `c6c8e63bac0e543624ac63fd50a046878ba7082a531115111563455682e4d437`.
- Upstream README identifies OpenAI as author and warns that unformalized results can have issues. `lean/docs/295.md` claims all-algebra bounded cohomology scope; that scope description is not itself a verification of Lean declarations or a reproduced build.

## Exact source hypotheses and what follows immediately

Roydor Theorem 1.2, PDF p. 2, assumes that **M has separable predual**, that `H^2(M,M)=0`, and that `B^3(M,M)` is closed in `Z^3(M,M)`. It then gives a number epsilon depending a priori on M and equivalence of:

1. Jordan *-isomorphism of M and N;
2. linear isometry of M and N;
3. linear isometry of their canonical preduals;
4. ordinary Banach–Mazur predual distance below `1+epsilon`;
5. ordinary Banach–Mazur algebra distance below `1+epsilon`.

N is required to be a von Neumann algebra; no separability restriction is stated on N. Ordinary distance is the infimum of `||L|| ||L^{-1}||` over bounded linear isomorphisms. In this operator-algebra setting the field is complex; the project should explicitly say complex-linear and set the distance to infinity when there is no isomorphism.

The upstream theorem quantifies over every complex von Neumann algebra and every degree k at least two. Its `C_b^k(M,M)` consists of all bounded complex k-linear maps, with the ordinary multilinear operator norm. The denominator is the actual image, without closure. Its differential is the standard Hochschild differential. Thus its k=2 conclusion gives Roydor's H^2 condition. Its k=3 conclusion gives `B^3=Z^3`; since `Z^3=ker d^3` is closed in the Banach space of bounded 3-cochains, Roydor's closed-range condition follows.

This directly proves the two target consequences for separable-predual M, provided family 295 is valid. It does not directly remove Roydor's separability hypothesis.

## Where hypotheses enter the full Roydor proof

The following proof map concerns what is actually in the supplied article, rather than the slides.

| Source component | Actual mechanism | Scope and dependencies |
|---|---|---|
| Proposition 2.2, pp. 5–6 | Near isomorphism sends each unitary to an invertible element close to a unitary; spectral/numerical-radius argument | Unital C*-algebras; no separability or normality of the map |
| Corollary 2.4, p. 6 | Unitize and symmetrize to a unital self-adjoint near isomorphism | Ordinary operator norm; no separability |
| Corollary 2.7, pp. 7–8 | Approximate preservation of Jordan polynomials | Ordinary bilinear/trilinear norms; no separability |
| Proposition 2.13, pp. 10–11 | Rounding images of central projections gives a center lattice isomorphism and hence a center *-isomorphism | Arbitrary von Neumann algebras; no countable projection-family argument |
| Lemma 3.1, pp. 11–13 | Compress at a projection, prove onto by a Neumann/geometric-series argument, then unitize the compression | Arbitrary projection corners; bounds deteriorate from t to order sqrt(t) |
| Theorem 3.2, pp. 13–17 | Use a 2-by-2 matrix system to separate multiplicative and anti-multiplicative pieces by a central projection | Requires the source identity to be divisible into two equivalent orthogonal projections. Its stated type-I restriction excludes odd finite homogeneous source summands. No separability is used in its computations |
| Theorem 1.1 / Lemma 4.3, pp. 18–20 | Preserve type and finiteness/equivalence using projection comparisons | Contains additional proof details/parameter checks discussed below. Not needed by the scope-removal proof here |
| Theorem 4.5, p. 21 | Associative multiplication stability from H^2 vanishing and closed B^3 | A theorem about one fixed Banach algebra, with algebra-dependent constants; its involution clause needs care |
| Theorem 1.2 proof, pp. 21–23 | Split type I off; exactify multiplicative/anti pieces; identify homogeneous type-I dimensions | The visible separability use is `MI=⊕_{j∈J} L∞(Ωj,Mj)` with `J⊂N∪{∞}`. The symbol infinity represents the countable Hilbert dimension; arbitrary type-I algebras have arbitrary cardinal dimensions |

The proof's non-type-I part is already algebraic and norm-based. The missing general-scope work is not a cohomology-normality problem. It is the justification of the type-I step and of a uniform threshold while the central orientation projections may depend on the near map.

The exact source theorem must therefore be distinguished from any general conditional theorem announced in slides. This audit makes no claim that a general conditional statement is new or that the argument below has priority; that requires the independent literature audit.

## Printed errors and proof details that should not be copied literally

1. **The Hochschild formula on p. 20 is misprinted.** The sum is printed only through `k-1`, omitting the last adjacent merge, and its right-action sign is `(-1)^k` rather than `(-1)^{k+1}`. At k=1 the displayed expression becomes `a f(b)-f(a)b`, without `-f(ab)`. It therefore does not define the asserted cochain complex. This was visually confirmed in the PDF. The standard intended differential is unambiguous from the references, the subject, and the rest of the theorem. Our argument must explicitly use the standard differential, which agrees with family 295, rather than assert literal equality with this printed display.

2. **Claim 4 on p. 15 has an off-diagonal index typo.** It prints `T(eij) ≃ gij+hij`; the correct relation is `gij+hji`, used immediately above and again in Claim 7. The transpose map on M2 provides an exact counterexample to the literal printed Claim 4: all off-diagonal gij are zero, hij=eij, and T(eij)=eji. This is a correctable typo in the title of the claim, not a counterexample to the decomposition theorem.

3. **Lemma 4.3(2) invokes its earlier equivalence assertion for a compressed map without rechecking the parameter or source type assumption.** The compression has inverse norm bounded by `1+988 sqrt(t)`, not `1+t`; a corner of a source with even finite type-I blocks can itself have odd finite type-I blocks. An arbitrary infinite projection can also have a finite odd-dimensional part in its corner. The displayed proof needs an additional restriction/argument and smaller threshold. This audit does not claim the lemma's statement is false; it identifies an unsupported invocation in the printed proof. The argument below bypasses Lemma 4.3 and Theorem 1.1 entirely.

4. **Numerical constants cannot be imported from cohomology vanishing alone.** The p. 21 discussion asserts `K=L=1` when all bounded cohomology vanishes. Family 295's stated theorem is an existence theorem, and its written reductions do not by themselves supply norm-one primitives for every ordinary bounded cochain on every algebra. We do not need that assertion and do not claim any universal Banach–Mazur threshold.

5. The movement from cohomology of M to a moving central corner is qualitative unless its constants are controlled. If `p=p(T,N)` varies, simply saying “Johnson applies to pM” does not exhibit one epsilon_M valid for all comparison N. A central extension/restriction argument can control constants, or one can apply stability once to a fixed source algebra. The latter is used below.

## Upstream quantitative scope: what was actually checked

The upstream cohomology section first proves `||g||≤||f||` for **separately normal** cocycles on a separable-predual type-II1 algebra with a faithful normal tracial state. It then removes separability in the tracial setting by independent finite-set subalgebras and trace-preserving expectations, followed by pointwise ultraweak compactness. The uniform primitive estimate is crucial there. This is a valid cohomology mechanism to inspect; it is not automatically a mechanism for approximating an arbitrary Banach-space isomorphism between M and N by compatible isomorphisms of separable subalgebras.

For a general type-II1 algebra the source partitions the center into pieces carrying faithful normal tracial states. Its explicit central homotopy has degree-k bound `(k-1)||f||`, and it assembles corrected primitives with bound `k||f||` for normal cocycles on these pieces. The complementary non-II1 summand is handled as one piece by a classical vanishing theorem with an unspecified finite primitive bound. The reduction of an arbitrary bounded cocycle to a normal cocycle also introduces a bounded cochain b whose norm is not bounded by the displayed theorem statement. Consequently these passages do not justify `K=L=1` for arbitrary ordinary bounded cochains.

For the original existential, algebra-dependent threshold, no explicit primitive bound is needed. Surjectivity and closed range in the Banach cochain complex imply finite constants by the open mapping theorem. The correction below uses precisely those constants for a fixed source algebra.

## Complete involution-preserving multiplication correction

This replaces any ambiguous reading of the final self-adjoint clause of Roydor Theorem 4.5. It requires no complete boundedness, normality, separability, or norm-one splitting.

Let A be a fixed complex C*-algebra with ordinary `H^2(A,A)=0` and closed `B^3(A,A)` in `Z^3(A,A)`. Write C^n for bounded complex n-cochains and d for the standard differential.

Because Z^2 and B^3 are closed Banach subspaces, the maps

- `d:C^2/Z^2 → B^3`, and
- `d:C^1/ker(d:C^1→C^2) → Z^2`

are continuous bijections of Banach spaces. Choose enlarged positive constants K,L, at least one, such that:

- for every f in C^2, there is z in Z^2 with `||f-z||≤K||df||`;
- every z in Z^2 has a primitive h in C^1 with `dh=z` and `||h||≤L||z||`.

For zero right-hand sides choose the exact zero-error solution. Enlarging the inverse bounds slightly allows these inequalities without assuming norm-minimizing representatives or bounded linear right inverses.

Define the conjugate-linear isometric involution on n-cochains by

`S_n f(a1,...,an)=(-1)^((n-1)(n-2)/2) f(an*,...,a1*)*`.

Reversing the differential's terms gives `d S_n=S_{n+1} d`. In particular S1 fixes self-adjoint linear maps and S2 fixes bilinear maps compatible with the involution. If f=S2 f, average an approximate z with S2 z. If z=S2 z, average its primitive h with S1 h. These averages preserve the displayed bounds. This supplies real symmetric choices; no complex-linear selection is required.

Let mu=m+Delta be an associative, involution-compatible bounded multiplication, where m is the original product and `delta=||Delta||`. Associativity gives the exact identity

`dDelta(x,y,z)=Delta(Delta(x,y),z)-Delta(x,Delta(y,z))`,

hence `||dDelta||≤2 delta^2`.

Choose symmetric z and h as above so that

`dh=z`, `||Delta-z||≤2K delta^2`, `||h||≤L(delta+2K delta^2)`.

Put `g=I+h`, `b=g^{-1}`, and transport the product:

`nu(x,y)=g(mu(bx,by))`.

The exact defect identity, at u=bx and v=by, is

`nu(x,y)-xy = [(Delta-dh)(u,v)+h(Delta(u,v))-h(u)h(v)]`.

If `delta≤1/(2K)` and `delta≤1/(4L)`, then `||h||≤2L delta≤1/2`, `||b||≤2`, and therefore

`||nu-m||≤D delta^2`, where `D=8K+8L+16L^2`.

Transport preserves associativity and involution compatibility. Iterate, always using the fixed original differential of A. Take

`delta_* = min{1/(2K), 1/(16L), 1/(2D)}`.

For `||mu-m||≤delta_*`, the defects obey `delta_n≤2^{-n}delta_0`. The corresponding corrections have

`sum_n ||h_n||≤4L delta_0≤1/4`.

The ordered products `Phi_n=g_{n-1}...g_0` converge in operator norm, and

`||Phi-I||≤exp(4L delta_0)-1<1`.

Thus Phi is invertible and commutes with the involution. The exact finite-stage identity

`Phi_n mu(x,y)=mu_n(Phi_n x,Phi_n y)`

passes to the norm limit, yielding

`Phi mu(x,y)=Phi(x)Phi(y)`.

If mu has unit 1, Phi(1)=1 follows because Phi is an onto algebra isomorphism and both original and transported products have that unit. This proves the needed general self-adjoint correction with an algebra-dependent threshold. All choices and norm estimates are checkable directly.

## Halving lemma on a fixed source algebra

Say that A halves if its unit is the sum of two equivalent orthogonal projections. Let A be a fixed von Neumann algebra which halves and has the cohomology conditions in the preceding section. Let `S:A→B` be a unital self-adjoint linear isomorphism with both norms at most `1+t`, where t tends to zero.

Roydor Theorem 3.2 supplies central p in A and q in B and a block map

`F=S_p^q ⊕ S_(1-p)^(1-q)`.

The first block is approximately multiplicative and the second approximately anti-multiplicative. Lemma 3.1 and Theorem 3.2 give

`||F^{-1}||≤1+988 sqrt(t)`

and ordinary bilinear defect at most `c sqrt(t)`, where `c=3147585`.

On the **fixed target Banach *-space** B put the product

`b ⋄ c = qbc+(1-q)cb`.

Because q is central, this is the direct product of the usual multiplication on qB and the opposite multiplication on (1-q)B. It is associative, bounded with norm at most one, has unit 1, and satisfies `(b⋄c)*=c*⋄b*`. It defines a C*-algebra on the same normed *-space B.

Pull it back to the **fixed source algebra A**:

`mu(x,y)=F^{-1}(F(x)⋄F(y))`.

It is associative, unital, and involution-compatible, and

`||mu-m_A||≤(1+988 sqrt(t)) c sqrt(t)`.

Apply the explicit correction for this one A. Once t is sufficiently small, `J=F Phi^{-1}` is a *-isomorphism from A to `(B,⋄)`. As a map into B with its original multiplication, J is a Jordan *-isomorphism. The threshold depends on A, not on the varying orientation projection p, the target B, or its cardinal dimension.

This is the principal way the proof avoids a moving-corner uniformity gap.

## Full central carriers survive rounding

Here is the required projection fact without an unsupported appeal to type continuity.

Let `S:C→D` be unital self-adjoint with both norms at most `1+t`, with t small enough for Proposition 2.13. Put `r=140 sqrt(t)` and `gamma=2(1+t)sqrt(2t+t^2)`. Let theta be its center projection lattice isomorphism. If e is a projection in C and f is a projection in D with `||S(e)-f||≤r`, then

`c_D(f)=theta(c_C(e))`,

provided `2(1+t)r+gamma<1`.

Proof. Write z=c_C(e). Since e≤z, Lemma 2.5 gives `S(e)≤S(z)+gamma`. Thus

`f-theta(z)≤(2r+gamma)1<1`.

As theta(z) is central, the projection `f(1-theta(z))` must vanish: otherwise compression of the displayed order inequality gives `1≤2r+gamma`. Hence `c_D(f)≤theta(z)`.

Conversely write w=c_D(f). Since f≤w, apply the same order estimate to S inverse, using

`||S^{-1}(f)-e||≤(1+t)r` and `||S^{-1}(w)-theta^{-1}(w)||≤r` (or the conservative bound `(1+t)r`).

It gives `e-theta^{-1}(w)≤(2(1+t)r+gamma)1<1`, so `e≤theta^{-1}(w)`. Taking central carriers and applying theta yields `theta(z)≤w`. Equality follows.

The same statement applies to complements because S is unital. Thus if e and 1-e both have full central carrier, their rounded images f and 1-f do as well.

## Removing all separability and cardinal restrictions

**General conditional theorem.** Let M be an arbitrary complex von Neumann algebra with ordinary bounded `H^2(M,M)=0` and `B^3(M,M)` closed in `Z^3(M,M)`, using the standard Hochschild differential. Then there is `epsilon_M>0` such that every complex von Neumann algebra N satisfying either `d_BM(M,N)<1+epsilon_M` or `d_BM(M_*,N_*)<1+epsilon_M` is Jordan *-isomorphic to M. The proof below uses Roydor Corollary 2.4, Proposition 2.13, Lemma 3.1, Theorem 3.2, the explicit multiplication correction above, and classical type-I cohomology/projection facts. It imposes no separability assumption. In particular, family 295's claimed all-algebra vanishing theorem supplies the two cohomology hypotheses for every M. This is a dependency-conditional mathematical proof, not a certification of the upstream theorem or a priority claim.

Let M be any complex von Neumann algebra. Split it into three **fixed central summands**:

- A: its commutative type-I1 summand;
- O: the sum of finite odd homogeneous type-In summands with n≥3;
- P: the rest, namely finite even type-I summands, all infinite type-I summands of every cardinal dimension, and all type-II/type-III summands.

P halves. This is the projection-halving criterion used by Roydor Theorem 3.2; arbitrary infinite Hilbert dimensions cause no obstruction, since an infinite cardinal is the sum of two copies of itself. The II1 unit also halves, and the remaining properly infinite types halve. Infinite direct sums of these choices assemble by strong sums. No separable predual is needed.

If N is sufficiently near M in ordinary Banach–Mazur distance, Corollary 2.4 gives a unital self-adjoint near isomorphism T. Its center lattice isomorphism theta sends the three source central projections to an orthogonal partition of the target identity. Lemma 3.1 supplies unital self-adjoint near isomorphisms from A, O, and P onto the corresponding target summands, which will be denoted B_A, B_O, B_P. Their norm errors tend to zero as the original distortion tends to one.

The commutative summand A and B_A are *-isomorphic by Proposition 2.13 applied to the compressed map. Apply the fixed-source halving lemma to P to obtain a Jordan *-isomorphism `P→B_P`, assuming P's cohomology conditions. Zero summands are simply omitted.

It remains to treat O. Write canonically

`O=product_(n odd,n≥3) M_n(Z_n)`.

This is a countable decomposition by finite integer degree; the abelian centers Z_n may be completely nonseparable. Choose a **fixed** projection e whose component in M_n(Z_n) is `diag(1,...,1,0)`. Then

`eOe=product_(n odd,n≥3) M_(n-1)(Z_n)`

halves. Both e and 1-e have full central carrier in O, and `(1-e)O(1-e)` is abelian.

Let `S:O→B_O` be the compressed near map and choose a rounded projection f close to S(e). Lemma 3.1 supplies a unital self-adjoint near isomorphism `eOe→fB_Of`. The source eOe is fixed. Apply the halving lemma to it, obtaining an exact Jordan *-isomorphism

`eOe ≅_J fB_Of`.

The required cohomology of eOe follows either from family 295 or from the classical type-I vanishing theorem. Apply Lemma 3.1 also at the complementary projection: `(1-e)O(1-e)` is nearly isomorphic to `(1-f)B_O(1-f)`, hence the latter is commutative by Proposition 2.13. The full-carrier result proves

`c(f)=c(1-f)=1`.

Thus B_O has a full abelian projection 1-f and is type I. The compression map `z→zf` identifies `Z(B_O)` with `Z(fB_Of)` because f has full central carrier. Decompose the corner using its exact Jordan equivalence with eOe. For each odd n≥3, let z_n be the corresponding target central projection. On this central part, `z_n fB_Of` is homogeneous type-I_(n-1).

Choose its usual n-1 orthogonal equivalent abelian projections f_1,...,f_(n-1), which sum to z_n f. They are abelian in B_O as well, and each has central carrier z_n in B_O. The abelian projection `z_n(1-f)` also has central carrier z_n. In a type-I von Neumann algebra, abelian projections with the same central carrier are equivalent. Consequently these n projections are equivalent and sum to z_n. Matrix units then give

`z_n B_O ≅ M_n(Z(z_n B_O))`.

The Jordan equivalence of the corners identifies their centers by a *-isomorphism. Hence `Z_n ≅ Z(z_n B_O)` and therefore `M_n(Z_n) ≅ z_n B_O` as *-algebras. Taking the full product over odd n proves `O ≅ B_O` as *-algebras.

Together with the A and P identifications this gives a Jordan *-isomorphism M to N. Arbitrary infinite cardinal type-I summands were handled inside the single fixed halving summand P; they were never enumerated as countable dimension blocks or reduced to separable factors.

### The single-threshold quantifier

There are only finitely many fixed source algebras requiring perturbation thresholds: P and eOe. Everything else has numerical smallness conditions from Roydor's geometric lemmas. For a near map of distortion `1+eta`, the initial unital self-adjoint parameter can be taken of order `10 sqrt(eta)`. Each use of Lemma 3.1 replaces a small parameter s by at most `988 sqrt(s)`. The finite number of such operations still tends to zero as eta tends to zero.

Choose epsilon_M sufficiently small so that these finitely many parameters satisfy the center/order, compression, and halving conditions and the two fixed-algebra thresholds. This choice is positive, depends only on M, and works for every comparison N. No minimum over an unbounded family of N-dependent central corners is taken.

Under the original assumption `H^2(M,M)=0` and closed `B^3(M,M)`, the necessary conditions for the fixed central summand P also follow from extension/restriction: extend a cochain on P to M by cutting every input by the central unit of P, and restrict an M-cochain by multiplying its output by that unit. These are contractive chain maps with restriction after extension equal to identity. They preserve vanishing and closed range. The noncentral corner eOe needs only the already classical type-I theorem. With family 295's all-algebra theorem, both fixed-source cohomology inputs follow immediately, without any Morita-invariance assumption.

## Predual consequence and boundary checks

For a bounded complex-linear isomorphism `L:M_*→N_*`, its adjoint is an isomorphism `L*:N→M` with the same norm and inverse norm. Thus

`d_BM(M,N)≤d_BM(M_*,N_*)`.

The same algebra threshold therefore proves the requested predual implication. It is not necessary to claim equality of the two distances.

A Jordan *-isomorphism between von Neumann algebras is an order isomorphism on their self-adjoint parts. It preserves suprema of all bounded increasing nets, by applying the order inverse to a proposed smaller upper bound. Hence it and its inverse are normal. Its preadjoint is an onto linear isometry of the canonical preduals. This gives the source theorem's isometry equivalences at arbitrary cardinality.

Boundary checks:

- The zero algebra is separate and immediate; it is not Banach-isomorphic to a nonzero algebra.
- If there is no bounded complex-linear isomorphism, distance is infinity and the local premise fails.
- The comparison object remains a von Neumann algebra throughout.
- Opposite multiplication is essential. The conclusion is Jordan *-isomorphism; the argument does not claim *-isomorphism of the halving summand with its original target product.
- Cochain and multiplication estimates are ordinary operator norm estimates, not completely bounded estimates.
- No normality of the initial Banach isomorphism is assumed. Normality is concluded only for the final exact Jordan map.
- In the odd summand, the full-carrier check rules out a target block of degree n-1 with zero complementary projection, which would otherwise be a hidden error in the rank-addition argument.
- The center reconstruction uses type-I projection/matrix-unit facts, not a direct-integral disintegration requiring standard measure spaces.

## Approach ledger and exact remaining gaps

| Approach | Mechanism and evidence | Status | Exact gap |
|---|---|---|---|
| Bare theorem composition | Family 295 matches ordinary H2/H3; Roydor p.2 explicitly assumes separable predual | Insufficient for original scope | Cannot silently delete separability |
| Directed separable subalgebras | Valid uniform-primitive compactness in upstream cohomology §5 | Not a rigidity proof | An arbitrary near Banach isomorphism need not give compatible onto maps between matching separable von Neumann subalgebras; an unproved gluing claim merely transfers the difficulty |
| Arbitrary-cardinal homogeneous enumeration | Replace `N∪{infinity}` with all type-I cardinals | Not needed here | Requires exactification and constants across extracted blocks; this audit does not declare a bare enumeration sufficient |
| Fixed-source global product plus odd-complement reconstruction | Explicit associative opposite-product transport; two fixed correction thresholds; full carriers and finite matrix units | Complete checkable candidate proof | Fresh adversarial verification and dependency certification still required before promotion |
| Universal numerical epsilon from `K=L=1` | Roydor p.21 assertion; special known cohomology classes | Not established from family 295 here | Family's displayed reductions do not supply the asserted universal ordinary primitive constants; no universal claim is needed |

The strongest result justified here is the exact separable-predual consequence by the printed theorem, together with a detailed arbitrary-scope proof based on Roydor's geometric lemmas, the explicit correction, and the cohomology input. Remaining work is to have a fresh independent reviewer falsify the new fixed-source mechanism, finish the independently assigned upstream/literature audits, and propagate the accurately qualified scope and attribution into a complete package. A source theorem announcement already in 2020 slides must not be re-advertised as our first theorem.

## Read-only external bibliographic check

The source's Johnson and Raeburn–Taylor references were cross-checked on primary publisher pages:

- [B. E. Johnson, Perturbations of Banach Algebras](https://doi.org/10.1112/plms/s3-34.3.439), *Proceedings of the London Mathematical Society* 34 (1977), 439–458.
- [I. Raeburn and J. L. Taylor, Hochschild cohomology and perturbations of Banach algebras](https://www.sciencedirect.com/science/article/pii/0022123677900726), *Journal of Functional Analysis* 25 (1977), 258–266. Its abstract states the H2/H3 multiplication-stability implication; it does not by itself certify the involution variant.

No primary full text of Johnson or Raeburn–Taylor was recovered in this audit. The explicit correction above avoids relying on an unaudited reading of their involution clause.
