# Independent audit of the two flat retractions and secondary routes

UTC checkpoint: 2026-10-24T22:42:00Z. Reviewer: internal subagent `p21124_flats_adversary`, not an author of the submitted arguments. Audit completion estimate: **100% of these partial claims**. Best-guess discovery completion toward the full problem: **3%**, reflecting useful reductions but no full answer. Frozen input hashes are in `RECEIPT.json`.

**Verdict: PASS in the stated scope.** For every k≥2, both exact subgroups `<a,t>` and `<[a,b],t>` are virtual retracts of the stated group G_k. The boundary k=1 also has both retractions, by the separate four-coordinate model detailed below. The secondary routes have their quantifier limitations correctly stated. These conclusions do not resolve Kourovka21.124, establish virtual specialness, or certify novelty. No author file was edited.

## Dependencies and the actual groups

Use exactly

`G_k=<a,b,c,t | tat^-1=a, tbt^-1=ba^k, tct^-1=caba^-1b^-1>`, k≥1,

and `w=aba^-1b^-1`. The assignment a↦a, b↦ba^k, c↦cw is an automorphism of F(a,b,c): it fixes w and its inverse is a↦a, b↦ba^-k, c↦cw^-1. Thus the presented group is the semidirect product F3⋊Z. Both a and w have infinite order, and t has nonzero height. As both commute with t, a relation `a^r t^s=1` or `w^r t^s=1` first gives s=0 by height and then r=0 in the free fiber. The two subgroups really are Z², independently of whether an affine representation is faithful.

The all-k cyclic retraction and its existing fresh review were read only as dependencies. I separately verified the defining affine relations from the closed coordinates, using pullback rather than basis-image permutations. In dimension3k, put A constant with block values(−1,0,1), T constant with block values(k,0,0). Let P rotate each block, B rotate the blocks, and C interchange the same three disjoint pairs in the manuscript. The b-offset has entries `u_(j,0)=0`; for1≤i<k they are `(k−2i,i,i−k)` in the three blocks. These formulas apply to every k≥2; no evenness or k>2 assumption occurs.

Writing D=CT−T, its nonzero entries are `D_(0,0)=D_(0,1)=−k`, `D_(1,0)=k`, `D_(2,1)=k`. Coordinate differences give `(P−I)u=D−(I−B)A`. With the affine multiplication `(v,p)(z,q)=(v+pz,pq)`, this proves all three defining relators. In particular w has image(D,I), not a nontrivial linear part.

## The exact flat `<a,t>`

Let q be the finite linear-part map, and L=q^-1(`<P>`). L has finite index and contains **a and t themselves**. Define

`f_a(v)=sum(v_(2,i))/k`,

`f_t(v)=(sum(v_(0,i))+sum(v_(2,i)))/k²`.

Both forms are P-invariant, and their values on A,T are respectively(1,0),(0,1). Therefore `chi(g)=(f_a(v_g),f_t(v_g))` is a homomorphism on L. Indeed `v_(gh)=v_g+q(g)v_h`, so P-invariance proves additivity without assuming rho(g) and rho(h) commute.

All translation coordinates are integers. Consequently chi(L) is contained in `(1/k²)Z²`. Composing chi with the finite quotient `(1/k²)Z²/Z²` shows that H=chi^-1(Z²) has index at most k^4 in L. It contains a,t because their chi-values are integral. Thus `g↦a^chi_a(g)t^chi_t(g)` is a homomorphism H→`<a,t>` and is the identity on that entire Z². This is a retraction of the exact subgroup, with no replacement of a or t by powers. H need not be normal in G_k. An explicit coarse index bound is k^4·`[q(G_k):<P>]`; the bound is for existence and no sharpness is claimed.

## The exact flat `<w,t>`

K=ker(q) is finite index and contains w,t. On K every affine image is a translation. Besides the abstract rational-extension argument in the manuscript, the following forms are explicit:

`f_w(v)=v_(1,0)/k`, `g_t(v)=sum_(all coordinates)(v)/k²`.

D has total sum0 and coordinate(1,0) equal to k; T has total sumk² and that coordinate0. Thus the forms take D,T to(1,0),(0,1). They are homomorphisms on K simply because translations add. Both values lie in `(1/k²)Z`. The finite-index subgroup `J=(f_w,g_t)^-1(Z²)` contains w,t, and `g↦w^f_w(g)t^g_t(g)` retracts J onto the exact Z². One may bound `[G_k:J]` by k^4·`|q(G_k)|`. No irrational form, infinite denominator, or assumption of global injectivity is used.

## Boundary k=1

The three-transposition model cannot be used at k=1. Instead let `P(v)_i=v_(i+1 mod4)`, A=(1,0,−1,0), T=(0,0,1,1), with a,t acting as translations and b,c having zero offsets and linear parts P,P². Direct computation gives `T−PT=PA` and `T−P²T=P²A−P³A`, the exact b- and c-relators. The finite linear kernel has index4 and contains a,t,w. Here `rho(w)` translates by D=(1,1,−1,−1). The two **integral** forms `v↦v_0` and `v↦v_0+v_2` are simultaneously dual to A,T and to D,T. Hence the index-four subgroup retracts onto each flat with no additional lattice restriction. This boundary extension follows by proof, independently of a finite test; the submitted flat delta carefully claimed only k≥2.

## Fixed subgroup limitation: affine versus linear commutation

Let y=bab^-1. The fiber automorphism fixes y and a, and these generate a rank-two free subgroup F(a,y). In the uniform k≥2 representation their linear parts both equal P. Their **affine** images need not commute. In fact y has translation A−D, and `[rho(a),rho(y)]` translates by `(I−P)D`, which is nonzero for every k≥2. For example it has entry k at block1 position0. Thus identifying their commuting linear parts with commuting affine maps would be false.

The image of F(a,y), however, is an extension of an abelian translation subgroup by the cyclic group `<P>`, and is metabelian. Its second derived subgroup is killed. The fixed explicit word `[[a,y],a[a,y]a^-1]` is nontrivial in the free group F(a,y), as independent free reduction checks, but maps trivially because its two inner words are translations. This establishes a genuine limitation of this representation, not invisibility in every finite quotient or cover. It provides no obstruction to a different retraction. For k=1 even the first derived subgroup of this fixed free subgroup is killed by this particular boundary representation; no claim of detecting its commutator is made there.

## Direct distortion and its finite-index limit

The normal form of `(bt)^n t^-n` in the free fiber is `product_(i=0)^(n−1) b a^(ki)`. For k>0 all letters are positive, so its exact free length is `n+k n(n−1)/2`. Its displayed ambient representative has length3n. This proves distortion of the rank-two subgroup F(a,b) in G_k. The independent checker verifies600 distinct expansions; positivity and the geometric-series sum supply the unbounded argument.

Carr's [Theorem1.4 and Corollary5.1](https://arxiv.org/pdf/1412.0642) give the stated direct RAAG obstruction. If an embedding G_k→A existed, the image length of any g would be bounded above by a constant times its G_k length, whereas the embedded F(a,b) would have a linear lower bound in its own free metric. The quadratic sequence contradicts both inequalities. No assumption that G_k itself is undistorted in A enters.

This does not obstruct **virtual** embedding. If H has finite index, the intersection H∩F(a,b) has finite index d in F2 and rankd+1 by Schreier's formula, so can have rank greater than2. For an explicit boundary, the valid quotient b↦1∈C2 with a,c,t↦0 has an index-two kernel whose fiber intersection has rank3. Distortion of that larger subgroup is compatible with embedding H in a RAAG. The manuscript also correctly rejects the power shortcut: for e≥2 the word `(ba^k)^e` has individual b-syllables with exponent1, so does not belong to `<a^e,b^e>` when k>0. An actual rank-two subgroup inside every H with a verified distortion sequence remains missing. Carr's own §5.2 discusses a virtually embeddable figure-eight mapping torus with a distorted rank-two fiber, directly falsifying the blanket virtual inference.

## Residual finiteness and geometric filters

[Linton, Theorem1.2](https://arxiv.org/html/2510.10178v2#S1.Thmtheorem2) allows arbitrary-rank free kernels and embeds every finitely generated free-by-Z group in a finite-rank free-by-Z group. The finite-rank latter group is residually finite: separate a nontrivial fiber word by a finite-index subgroup, intersect all subgroups of bounded index to obtain a characteristic finite-index subgroup still excluding it, and form the finite semidirect product by the induced finite-order automorphism. Nonzero-height elements are separated by finite cyclic quotients. Residual finiteness passes to subgroups. Thus the broad kernel convention does not produce a non-residually-finite CAT(0) candidate, since a CAT(0) group is finitely generated. No preservation of the CAT(0) property by Linton's envelope is asserted or needed.

[Delage, Proposition3.1 and §4](https://arxiv.org/html/2602.08759v3#S3) justify the stated commutator-twist warning. In a proper semisimple action, t's minimum set splits with an R factor; translation along that factor is a character on its centralizer. A nontrivial centralizer commutator has zero character and positive transverse translation, contradicting equal lengths for t and its conjugate tv. For this family, w=a y^-1 has abelianization(1,−1) in the fixed free group, so that specific obstruction does not apply. Wu–Ye's [Introduction](https://arxiv.org/html/2504.14192v2#S1) also explicitly distinguishes virtual specialness from cocompact cubulation; the manuscript does not conflate them.

For a fixed affine target with finite linear image, sufficiently large powers have trivial linear parts and commute. Making those powers depend on the target cannot prove that one fixed nontrivial word is invisible in every cover. The manuscript's warning is sound. The phrase “finite-by-abelian” in that paragraph would be clearer as “a virtually abelian affine target” or “abelian-by-finite”: the affine model has an abelian normal translation subgroup and finite quotient. This is an optional terminology clarification, not a substantive mathematical objection to the stated limitation.

## Reproduction and disposition

`independent_check.py` imports no author module. It checks exact affine relations, the two pairs of dual forms, all coordinate-basis denominators, P-invariance,1,680 additivity and integral-subgroup samples,16,940 distinguished-flat elements, the detected first commutator, and the killed fixed second-derived word, at70 parameters including1,2,3,127,128,257,509,1000,1001. All checks passed. It also checks600 distortion expansions and a nonempty reduced second-derived word. Tests do not replace any unbounded proof above. Read-only primary source checks were completed on2026-10-24; no external communication was undertaken.

No substantive objection remains for the stated partials. The full problem remains unsolved by this family: neither a finite-index-persistent negative obstruction nor a virtual RAAG embedding of the entire G_k has been established. No publication or originality gate is passed.
