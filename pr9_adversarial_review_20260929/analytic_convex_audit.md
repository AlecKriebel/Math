# Independent adversarial audit: convex and real-analytic route

**Audit date:** 2026-09-30 UTC (2026-09-29 America/Los_Angeles).  
**Assigned snapshot:** PR #9 head `a29887ed0e341851d02fa992c26500d4089267be`.  
**Reviewed file:** `source_snapshot/candidate.md`, 153 lines.  
**SHA-256:** `df5d9bd86562152cb72fd286055b62ded8ce0b4cdcf7d4a5ca1e001eb49ca47e`.  
**Scope:** Theorem 1, Lemmas 2 and 3, and the exposed-point parametrization needed to connect them.  
**Independence:** I read the candidate before consulting any other research document. I did not read prior `REVIEW.md` or verdict files, did not consult another agent's findings, and did not contact an outside individual. This report does not independently establish the source papers' formulations, historical novelty, or Theorem 4.

## Verdict

**PASS in the assigned scope.** I found no mathematical error or missing hypothesis in Theorem 1 or Lemmas 2 and 3. The stated conclusion follows from a proper prime complex polynomial vanishing ideal. Neither complex radical independence nor a complex parametrizing variety is needed.

Confidence is **very high** for this elementary proof chain, subject to the usual limitation that this is a human-readable AI audit rather than a machine-checked proof certificate. The exact mathematical remaining gap in the assigned proof is **none identified**. Bibliographic identification of the target, priority, and the additional result concerning `S(D)` are outside this audit's conclusion.

## Exact claim and dependency chain

At candidate lines 9–15, a disc is a linear image of a closed real Euclidean unit ball, the discs have real dimensions at least two, the number of summands is finite and positive, and `E(D)` is the complex Zariski closure of all exposed points of their Minkowski sum. In particular, the discs here are centered. Ambient dimension need not equal the dimension of their sum.

The proof requires precisely:

1. Each summand's maximizing face is a singleton exactly when its transposed matrix sends the normal to a nonzero vector.
2. The maximizing face of the sum is the sum of those faces; it is a singleton exactly when all the constituent faces are singletons.
3. The resulting normal domain excludes finitely many real linear subspaces of codimension at least two and is connected and open.
4. The unique maximizer varies real analytically on that entire domain.
5. Complex polynomial functions pulled back along that map have the real-analytic identity property; their common vanishing ideal is prime.

All five statements are valid under exactly the written assumptions. The following independently checks them in detail.

## Check 1: injective disc representation and maximizing points

**Candidate locations:** lines 47–64.

Let a given disc be `M(B^k)`, where the real matrix `M` has rank `m ≥ 2`. A singular-value decomposition yields matrices with

\[
M(B^k)=A(B^m),\qquad A\in\mathbb R^{d\times m},\quad \operatorname{rank}A=m.
\]

Indeed, orthogonal projection of `B^k` onto its first `m` singular coordinates is exactly `B^m`; the nonzero singular values and the corresponding left singular vectors define `A`. Thus the injectivity imposed at line 47 does not restrict the class of discs.

For any normal `u`, set `a=A^T u`. Maximizing the real functional over the disc is equivalent to maximizing `a^T v` over `||v|| ≤ 1`. If `a ≠ 0`, Cauchy–Schwarz and its equality case give the unique maximizing input

\[
v=\frac{a}{\|a\|},\qquad p(u)=\frac{AA^{\mathsf T}u}{\|A^{\mathsf T}u\|}.
\]

This uniqueness uses the closed *ball*: equality in `a^T v ≤ ||a|| ||v|| ≤ ||a||` forces both the unit norm and the positive collinearity. There is no missing second choice of sign. Injectivity of `A` also makes the corresponding image point unique.

If `a=0`, the functional is zero on every point of the disc. The maximizing face is the whole disc, which is nonsingleton since `m ≥ 2`. For `Q=AA^T`,

\[
u^{\mathsf T}Qu=\|A^{\mathsf T}u\|^2,
\qquad \ker Q=\ker A^{\mathsf T}.
\]

The second equality follows in both directions: `A^T u=0` implies `Qu=0`, while `Qu=0` implies `||A^T u||^2=u^T Qu=0`. Positive semidefiniteness is essential to this inference and is explicitly available here. Its kernel has codimension `m`, regardless of ambient degeneracy.

## Check 2: Minkowski faces and the exact set of exposed points

**Candidate locations:** lines 66–78.

For compact nonempty convex summands `D_i`, write

\[
C_i(u)=\{x_i\in D_i:\langle u,x_i\rangle=h_i(u)\}.
\]

Independent maximization of each summand gives `h_D(u)=Σ_i h_i(u)`. If `x=Σ_i x_i`, then

\[
h_D(u)-\langle u,x\rangle
=\sum_i\bigl(h_i(u)-\langle u,x_i\rangle\bigr).
\]

Each term is nonnegative. Therefore equality holds exactly when every term vanishes, which proves

\[
C_D(u)=\sum_i C_i(u).
\]

This conclusion holds for *any* chosen decomposition of an exposed-face point. Nonuniqueness of decomposition causes no issue.

A sum of nonempty sets can be a singleton only when each set is a singleton: if two distinct points occur in one set, fixing an arbitrary point in every other set produces two distinct points of the sum. Thus different summands cannot cancel a nonsingleton face into a singleton. Conversely, the sum of singleton faces is a singleton.

Combining these facts with Check 1, a normal exposes a point of `D` exactly when it belongs to

\[
U=\mathbb R^d\setminus\bigcup_i\ker A_i^{\mathsf T}.
\]

The origin belongs to every excluded kernel, so every element of `U` is nonzero, as required by the definition of exposed point. Every exposed point has a normal and hence arises from the displayed formula. Conversely every `u ∈ U` yields a unique maximizing point. This proves the exact equality at line 75,

\[
\operatorname{Exp}(D)=F(U),\qquad
F(u)=\sum_i\frac{Q_i u}{\sqrt{u^{\mathsf T}Q_i u}},
\]

without any density qualification, differentiability assumption on the full boundary, or injectivity of `F`.

## Check 3: connected normal complement

**Candidate locations:** Lemma 2, lines 21–29; application at line 82.

The complement of finitely many closed subspaces is open. It is nonempty because each proper subspace is contained in the kernel of a nonzero real linear form `ℓ_i`; the product `Π_i ℓ_i` is a nonzero polynomial and cannot vanish at every real point. The last assertion can be checked inductively in the number of variables, using that a nonzero univariate real polynomial has finitely many roots. Thus no algebraic-geometric hypothesis is hidden in the nonemptiness argument.

For path connectedness, fix `x,y ∈ U`. For each `i`, both `L_i+Rx` and `L_i+Ry` have dimension at most

\[
\dim L_i+1\leq d-1.
\]

Choose `z` outside their finite union. If `(1-t)x+tz ∈ L_i` for `0<t≤1`, then

\[
z\in L_i+\mathbb Rx,
\]

contradicting the choice. The endpoint `t=0` lies outside `L_i` by the assumption on `x`. The same reasoning holds for the segment from `y` to `z`. Concatenating the segments constructs a polygonal path from `x` to `y` within `U`.

This argument covers repeated subspaces, intersections of arbitrary dimensions, the smallest applicable case `d=2`, and ambient directions perpendicular to the sum. It needs neither simple connectedness nor an assumption that the subspaces are in general position. In the theorem, the codimensions are `rank A_i=m_i≥2`, exactly as required.

## Check 4: global real analyticity on this domain

**Candidate locations:** lines 76–82.

For every `u ∈ U`, each `q_i(u)=u^T Q_i u` is strictly positive. The function `t ↦ t^{-1/2}` is real analytic locally around every positive real `t`; composing it with the polynomial `q_i` and multiplying by `Q_i u` makes each summand of `F` real analytic near every point of `U`. Their finite sum is real analytic on all of `U`.

The square root is the positive real square root. It is a globally defined real analytic function of the positive real radicand. Although the corresponding complex quadratic may vanish on isotropic vectors and a complex square root may have monodromy, neither fact affects this statement about real analyticity on `U`. No complex square-root branch on a global complex domain is asserted or used.

The derivatives may become unbounded toward excluded kernels. The identity theorem requires only local analyticity at every included point; it imposes no uniform derivative bounds or extension to the removed set.

## Check 5: complex prime vanishing ideal

**Candidate locations:** Lemma 3, lines 31–41.

Let `S=F(U)` and let

\[
I(S)=\{P\in\mathbb C[X_1,\ldots,X_m]:P(F(u))=0\ \forall u\in U\}.
\]

This is an ideal because pointwise evaluation is a ring homomorphism. It is proper since `U` is nonempty and the constant polynomial `1` cannot vanish there.

For `PQ ∈ I(S)` with `P ∉ I(S)`, choose `u_0` with `P(F(u_0)) ≠ 0`. Continuity gives an open neighborhood in which `P∘F` never vanishes. On that neighborhood, `Q∘F` must vanish. Its real and imaginary parts are real analytic functions.

For clarity, the real-analytic identity step has no missing continuation hypothesis. For a real analytic scalar function `g` on connected open `U`, define `H` to be the points where `g` vanishes on some neighborhood. If `H` is nonempty then it is open. At any limit point `u ∈ U` of `H`, continuity of every derivative implies every derivative of `g` at `u` is zero. A convergent local Taylor expansion then makes `g` zero on a neighborhood of `u`. Thus `H` is relatively closed as well as open, and connectedness gives `H=U`. Apply this to both real and imaginary parts of `Q∘F`. It follows that `Q ∈ I(S)`, proving primeness over **complex** coefficients.

The ideal of the complex Zariski closure `Z` equals `I(S)` directly: a polynomial that vanishes on `S` defines a closed zero set containing `S`, hence contains `Z`; conversely, any polynomial vanishing on `Z` vanishes on its subset `S`. This equality does not require an unproved radical computation.

Finally, prime vanishing ideal implies irreducibility here by the following direct argument. If `Z=Z_1∪Z_2` were a union of two proper relatively algebraic closed subsets, choose polynomials `P` and `Q` that vanish respectively on `Z_1` and `Z_2` but do not vanish on all of `Z`. Such polynomials exist by the definitions of relative algebraic closed subsets and properness. Their product vanishes on all of `Z`, contradicting primeness. Thus `Z` is irreducible. This also avoids any hidden appeal to an uncertain complexification of a real ideal.

## Targeted falsification attempts

| Attempt | Check and result |
|---|---|
| Rank-two summands in the smallest ambient dimension | In `R^2`, every kernel is `{0}` and `U=R^2\{0}` is connected. Positive-root analyticity persists around every included normal. No sign-separated component appears. |
| Lower-dimensional sum in a large ambient space | A normal perpendicular to the entire span has nonsingleton exposed face `D` and is excluded. Other included normals work exactly as above. Ambient linear equations simply belong to the prime ideal; full-dimensionality is unnecessary. |
| Three repeated planar discs in `R^5` | For unit discs, `F(u)=3(u_1,u_2,0,0,0)/sqrt(u_1^2+u_2^2)`. Its closure is the conic `X_1^2+X_2^2=9`, `X_3=X_4=X_5=0`. Over `C`, the conic's coordinate ring becomes `C[a,a^{-1}]` after `a=X_1+iX_2`, `b=X_1-iX_2`, `ab=9`; hence it is a domain. Repeated radicals cause no defect. |
| Two independent planar blocks in `R^5` | The sum is `B^2×B^2×{0}` and exposed points form `S^1×S^1×{0}`. Its complex closure is the product of two conics, with coordinate ring a Laurent polynomial ring in two variables. Image differential rank is lower than ambient dimension, but irreducibility survives. |
| Nonunique decompositions or opposing summands | Fixing other summand points embeds any nonsingleton face by translation into the sum face. Cancellation cannot make that face a singleton. |
| Complex isotropic normals and radical dependencies | Such normals are not part of the real parametrization domain. The proof uses real analyticity and complex polynomial coefficients; it never assumes independent radicals or an irreducible complex covering space. |
| Noncompact or non-simply-connected `U` | The elementary identity theorem requires connected openness, not compactness or simple connectedness. The punctured planar domain is an explicit applicable case. |
| Allowing rank-one discs | The interval has two exposed points and reducible closure. A planar unit disc plus a segment has two algebraically distinct translated circular caps. This breaks the codimension-two condition and confirms that the given threshold performs real work. |
| Replacing analytic by smooth | A smooth map from `R` whose positive half maps to one coordinate axis and negative half to the other can have reducible Zariski closure. For example use `exp(-1/t^2)` on its respective side and zero otherwise. All derivatives match at zero, but analyticity fails. The candidate does not make this invalid extension. |

As a small arithmetic check, exact rational points `(3/5,4/5)` on the unit circle and `(5/13,12/13)` on a second unit circle reproduce the radius-three repeated-disc equation and both product-disc equations exactly. These sanity checks are not evidence replacing the general proof.

## Findings by source line

- **Lines 21–29:** Lemma 2 is correct as written. Its two-segment construction proves the required stronger path-connected conclusion.
- **Lines 31–41:** Lemma 3 is correct for complex coefficients. The continuity/identity-theorem argument and equality of vanishing ideals are sound.
- **Lines 47–64:** The injective matrix representation, support function, and unique maximizer are valid for all allowed ranks.
- **Lines 66–78:** Exact exposed-point coverage is valid; singleton-face logic has no cancellation exception.
- **Lines 82–84:** All lemma hypotheses are verified and the irreducibility conclusion follows.
- **Line 86:** The stated absence of radical-independence, injectivity, smooth-image, and differential-rank requirements agrees with the proof.

**No actionable mathematical correction is requested in the assigned scope.**

## Audit log and checkpoint

- **2026-09-30 04:24:44 UTC:** Initial independent candidate read and dependency checks completed; estimated completion of this assigned audit: 55%.
- **2026-09-30 04:27:04 UTC:** Real-versus-complex prime-ideal details and ambient/rank falsification attempts resolved; candidate checksum recorded; estimated completion: 90%.
- **2026-09-30 04:30:47 UTC:** Final report checkpoint; assigned audit complete, estimated completion: **100%**. Strongest verified result is the full written Theorem 1 under its stated hypotheses. No mathematical gap was found within the assigned scope. The root reviewer controls publication and any broader validation.
