# Independent adversarial audit: all positive parameters

UTC checkpoint: 2026-10-24T22:36:00Z. Reviewer: internal subagent `p21124_retraction_adversary`, not an author of the submitted proof. Audit completion estimate: **100% of the stated partial theorem**. Progress toward a complete answer to Kourovka21.124 is not estimated by this percentage.

**Verdict: PASS for the virtual retraction of the exact cyclic subgroup `<a>` for every integer k≥1.** No complete answer to Kourovka21.124, virtual RAAG embedding, (VRC) theorem, or originality claim follows from this audit.

Inputs were `negative_geometric/ALL_K_RETRACTION_DELTA.md`, `check_uniform_retraction.py`, and `uniform_retraction_results.json`. They were not edited. Their hashes and supporting dependency hashes are in `RECEIPT.json`. The older frozen negative filter was not re-audited here. A separate fresh child checked only its k=1 witness without reading the all-k proof; that report is in `k1_boundary/`.

## Exact claim and conventions

For

`G_k=<a,b,c,t | tat^-1=a, tbt^-1=ba^k, tct^-1=caba^-1b^-1>`,

there is a finite-index subgroup H≤G_k containing **a itself** and a homomorphism r:H→`<a>` whose restriction to `<a>` is the identity. An affine representation need not be injective or proper for this purpose. Infinite order of its image of a already implies infinite order of a in G_k. The ambient CAT(0) assertion is eligibility information, not an input to the retraction proof.

Vectors are columns; the permutation P sends basis position (j,i) to (j,i+1), so its coordinate action is `(Pv)_(j,i)=v_(j,i−1)`. B sends j to j+1, so `(Bv)_(j,i)=v_(j−1,i)`. With multiplication `(v,p)(w,q)=(v+pw,pq)`, the manuscript's affine relations have the stated signs. The independent checker uses the opposite data representation: each output coordinate is specified by an input coordinate and an offset. This directly tests function composition rather than importing the author's permutation algebra.

## Independent unbounded coordinate derivation for k≥2

Let T have block values `(k,0,0)`, and A have block values `(−1,0,1)`. The three transpositions defining C are disjoint for every k≥2, including k=2. All its other coordinates are fixed. In particular C²=1, P^k=1, B³=1, and PB=BP.

Writing `D=CT−T`, its only nonzero coordinates are

- `D_(0,0)=D_(0,1)=−k`;
- `D_(1,0)=k`;
- `D_(2,1)=k`.

Since `(I−B)A` has block values `(−2,1,1)`, the vector `R=D−(I−B)A` has the following entries:

- block0: `2−k` at i=0,1 and 2 at every other i;
- block1: `k−1` at i=0 and −1 elsewhere;
- block2: `k−1` at i=1 and −1 elsewhere.

Every block sum is zero. More directly, an integral solution of `(P−I)u=R` is

`u_(j,0)=0` for j=0,1,2, and, for 1≤i<k,

`u_(0,i)=k−2i`, `u_(1,i)=i`, `u_(2,i)=i−k`.

For example, at i=0 the cyclic differences `u_(j,k−1)−u_(j,0)` are respectively `2−k,k−1,−1`; at i=1 they are `2−k,−1,k−1`; all other differences are `2,−1,−1`. This proves the required equation for all k≥2, without assuming a parity or deriving a general result from finite tests.

The manuscript's block-averaging equation is also correct: for any block-constant vector W, each block of CW has k−2 entries from itself and one from each other block. Hence `ECW=W−(2I−B−B^-1)W/k`. Applying this to T gives the same zero-sum condition above.

## Exact affine relation audit

Set `rho(a)=(A,P)`, `rho(b)=(u,B)`, `rho(c)=(0,C)`, `rho(t)=(T,1)`. All translations are integral. The following calculations do not assume rho is faithful.

1. P fixes A and T, so a commutes with t in the image, and `rho(a)^k=(kA,1)` is a nonzero translation.
2. `kBA=(I−B)T`, since `kA=(B^-1−I)T`. Thus `rho(tbt^-1)=(u+(I−B)T,B)=rho(ba^k)`.
3. Since P and B commute, `rho(aba^-1b^-1)` has linear part1 and translation `(I−B)A+(P−I)u=D`. This remains true though b has a nonzero translation u.
4. Since `CD=C(CT−T)=(I−C)T`, one has `rho(c[a,b])=(CD,C)=rho(tct^-1)`.

Consequently the map is a homomorphism from the exact presentation. Its finite linear image Q is a subgroup of the finite symmetric group S_(3k); no claim about the order or structure of Q is needed.

## Exact `<a>` rather than a proper power

Let L be the inverse image of `<P>` under the linear part of rho. Then `[G_k:L]=[Q:<P>]` is finite, and a∈L. For any integer vector v set `ell(v)=−sum_(i=0)^(k−1)v_(0,i)/k`. The functional ell is invariant under **every** element of `<P>`, and ell(A)=1. Therefore `chi(g)=ell(v_g)` satisfies

`chi(gh)=ell(v_g+q_g v_h)=chi(g)+chi(h)` for all g,h∈L.

It takes values in `(1/k)Z`, so `L'=chi^-1(Z)` has index at most k in L. It contains a because chi(a)=1. Thus `r(g)=a^{chi(g)}` for g∈L' is a well-defined homomorphism and `r(a^n)=a^n` for every integer n. This is a retraction onto the **exact** subgroup `<a>`.

The preliminary 3k-point cover detecting a^k need not itself contain a. The retraction subgroup L' can have index larger than3k; the written proof does not conflate these two covers. A coarse existence bound is `[G_k:L']≤|Q|≤(3k)!`. Normality is not required by the definition of a virtual retract. Taking a normal core could remove a and is not part of this argument. Thus there is no contradiction with a restricted obstruction involving normal covers that kill a's holonomy, nor does failure of G_k itself to be RFRS invalidate the construction.

## Hand boundaries

For k=2, the new closed form gives

`A=(−1,−1 | 0,0 | 1,1)`, `T=(2,2 | 0,0 | 0,0)`, `u=(0,0 | 0,1 | 0,−1)`.

The transpositions are `(00,10),(11,20),(21,01)`, all disjoint. Thus k=2 does not collapse C or require three distinct positions inside one block.

For k=3 it gives

`A=(−1,−1,−1 | 0,0,0 | 1,1,1)`,

`T=(3,3,3 | 0,0,0 | 0,0,0)`,

`u=(0,1,−1 | 0,1,2 | 0,−2,−1)`.

The odd-parameter case obeys the same differences and relations. For k=1 the proposed three-block construction is not defined and is correctly excluded. The independent boundary reviewer instead checked the four-coordinate witness: with `P(v)_i=v_(i+1 mod4)`, `A=(1,0,−1,0)`, `T=(0,0,1,1)`, take a and t to be translations by A,T and b,c to have linear parts P,P² and zero translations. The relators reduce to `T−PT=PA` and `T−P²T=P²A−P³A`. The index-four kernel of the linear map contains a and has an integral translation-coordinate character taking a to1. See the separate hashed `k1_boundary/AUDIT.md`.

## Reproduction and falsification attempts

`independent_check.py` imports no author code. Its closed-form offsets and output-coordinate substitution passed all affine relations for **131** parameters: k=2,...,128,257,509,1000,1001. It also checks inverses, the literal long b-relator, commutator convention, P^k, B³, C², PB=BP, nonzero a^k translation, and invariance of the character. Exact tests on **18,000** generated words across k=2,3,4,5,7,8 confirm additivity on the subgroup with P-power linear part and closure of the integral-character subgroup. These tests supplement the unbounded proof and do not replace it.

`independent_cellular_check.py` also imports no author code. In a different edge ordering it uses primitive integer row elimination to calculate rational ranks exactly. For k=2,3,5,7 it verifies every lifted relator, verifies that the offset cochain vanishes on every boundary, computes C2-boundary ranks9,15,27,39 respectively, and shows the a^k-cycle at every vertex is outside that boundary span. At vertex0 the displayed cocycle evaluates to−k. This independently reproduces all the author's sampled lifted certificates and adds k=2.

The author's checker was additionally executed with its output redirected into this review directory by supplying a different `__file__` binding, leaving the submitted files unchanged. All output fields other than the fresh UTC timestamp exactly match the submitted certificate; see `AUTHOR_REPRODUCTION.json`.

No counterexample, hidden parity restriction, denominator issue, inverse-action mismatch, exceptional k=2 collision, or exact-subgroup gap was found. The proof does not require a proper Euclidean action; demanding properness would be an additional hypothesis unrelated to this conclusion.

## Primary eligibility check and limits

Fresh primary read: Leo Delage, *Which F3-by-Zs are CAT(0)?*, [arXiv2602.08759v3, Theorem4.1 and Remark4.2](https://arxiv.org/html/2602.08759v3#S4), read2026-10-24. For `w=aba^-1b^-1`, the word is cyclically reduced, b-balanced, of b-height1, starts at level0, and has a-weights `N_(a,0)=1`, `N_(a,1)=−1`. The first CAT(0) inequality is `0<2k`, so applies to every k>0. This confirms exactly the claimed source subclass. The defining map is triangular and invertible; indeed it fixes w, so its inverse sends a↦a, b↦ba^-k, c↦cw^-1. Thus the free kernel has rank3.

This source check is a verified application of the published theorem, not a new independent reconstruction of Delage's CAT(0) metric construction. The statement that G_k itself is not RFRS for k>2 belongs to the separately reviewed negative filter; the current positive proof neither requires nor reproves it. No priority audit for novelty of this virtual retraction has been performed. Nothing here establishes virtual specialness, or disproves it, for G_k, and no publication gate is passed by this partial theorem alone.
