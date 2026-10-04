# First mathematical assessment, independent of ZIP conclusions

Frozen UTC: 2026-10-04T06:20:24.072013+00:00

Exposure boundary: source-only freeze, the six pinned candidate filenames/bytes, complete TeX, and all four original candidate PDF pages; no public ZIP members or audit-derived conclusions have been opened. This is a mathematical assessment of the core theorem, not a final publication verdict.

## Independent derivation
The six basis vectors and displayed arrows are consistent. F has support columns 0,1,3 mapping to e1,e2,e4; V has support columns 0,3,5 mapping to e5,e2,e4. Every F-image has zero V-image and conversely, so FV=VF=0. Frobenius and inverse Frobenius are bijections, so imF=span(e1,e2,e4)=kerV and imV=span(e2,e4,e5)=kerF. F^2 sends only e0 to e2, and V^2 sends only e0 to e4. Both third iterates vanish.

The coordinate inverse e0=a,e1=b,e2=z,e3=w-2b,e4=v-z,e5=u-w+b proves the proposed change of basis over every characteristic, without division. Because coefficients lie in the prime field, F and V act on these combinations with no coefficient-twist error. Directly, Fu=Vu=v; Fw=v+z,Vw=z; Fa=b,Va=u-w+b; Fb=z,Vb=0, and v,z are killed. Thus M1=span(u,v) and M2=span(u,v,w,z) are stable. On M2/M1, Fw=Vw=z; on M/M2, Fa=Va=b and Fb=Vb=0. Each factor is the deformable dimension2 module I with imF=imV. Hoshi Lemma4.9 therefore identifies it as a single supersingular elliptic p-kernel over algebraically closed k. Contravariance sends the quotients M/M(3-i) to subgroup Hi, and D(Hi/Hi-1)=M(4-i)/M(3-i), so the flag direction is correct.

The isomorphism invariant delta=dim(imF^2 intersect imV^2) is intrinsic for sigma/sigma^-1-semilinear operators, because their images are subspaces over perfect k and any k-linear intertwiner carries these images bijectively. The distinct e2,e4 lines give delta(M)=0. An independent non-matrix-dual argument gives delta(MD)=1: both kerF^2 and kerV^2 are the same hyperplane span(e1,...,e5). Semilinear duality gives im(FD)^2=(kerV^2)^ann and im(VD)^2=(kerF^2)^ann, the same line k e0*. This confirms the manuscript's prime-field swapped transpose computation and rules out semilinear isomorphisms over the algebraic closure, not merely linear maps over Fp.

For L=span(e0,e3,e5), W-length6,pM=0, and FV=VF=p as endomorphisms of this p-killed module. V|L maps to independent e5,e2,e4 and is injective. L is a complement to imF, so the required composite L to M/imF factors through L/pL=L and induces an isomorphism. Exactness meets Hoshi Def3.4; this is a valid finite Honda object. The p!=2 equivalence in Hoshi Prop3.11 produces an actual finite flat p-killed W(k)-group, compatible with the special-fiber Dieudonne module. Since k is algebraically closed and W(k) is a local DVR, finite flat rank is p^6. Compatibility of Cartier duality and base change makes a W-self-duality impossible once the special fiber is nonselfdual.

For every n>=3, the block direct sum with I^(n-3) preserves Honda conditions and yields rank p^(2n). Product flags extend the qss filtration. Both second iterates vanish on I and its dual, so the extra blocks contribute zero to each intersection, leaving delta=0 versus1. The obstruction is additive for these block sums, so no cancellation issue remains.

## Status and exact gaps
No core mathematical or target-matching blocker found. The strongest verified core result is exactly the theorem for p>3,n>=3 over W(Fpbar), with qss special fiber and nonselfdual total group and special fiber. This does not prove a W-qss filtration, descent to each perfect k, a Jacobian result, or the Coleman conjecture. Minimal n=3 is an attribution to Takao's stated affirmative low-rank theorem; I have not independently reproved that theorem. Cyclic-word/priority/completion assertions require primary-source verification after this freeze. Entire supplement, metadata, source inventory, and computational package are still unreviewed.

## Honest correction to source-only expectation
Root pointed out that deformability alone forces rankF+rankV=dimM, not rankF=rankV. This correction is accepted and independently follows from exactness. The source-only file remains frozen unchanged. Its early expectation was not used as a proof premise: the displayed module independently has ranks3,3. Balance in a qss elliptic-factor filtration can be established separately, but the general Honda statement cannot supply it.

Completion estimate: 35% toward this full-package adversarial review.
