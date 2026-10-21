# Unreviewed WIP: k904,a outer focus-inverse area product

5100063 / AMR-050-0063, rank227. Author turn1 active; no reviewed result, PR or queue promotion. The exact target is the product of signed areas of the OUTER tangent-intersection polygon inverted about the two ORIGINAL billiard foci, for odd least periodN. This differs from k903,a (original-vertex inversions) and k906 (inversion about the outer-locus ellipse's own foci). arXiv2004.12497v11 Table10 contains the literal formula; the published Fifty companion has no900-series table. The imported report's implication of an identical published table is not accepted.

Full pinned source_record/prior_imported_report read. NumericID/k904 all-state PR search, target branch search, and default-branch target-path history found no prior campaign attempt. No reset. Source conventions: signed straight-edge polygon areas, unit-circle vertex inversion, nondegenerate nested confocal ellipses, primitive odd periods including stars; no hyperbolic or parity-by-repetition extension.

## Exact turn1 reduction

Use Stachel's canonical coordinates with caustic alpha,beta, k=c/alpha, k'=beta/alpha, v=2K tau/N, gcd(N,tau)=1, 0<tau<N/2, delta=2v. Let h=sn v, C=cn v, d=dn v, t=h^2, q=C^2, U=1-2k^2t+k^2t^2, V=1-2t+k^2t^2, W=1-k^2t^2.

The outer vertices, up to a fixed phase, are

Q(u)=(-A_o sn u,B_o cn u), A_o=alpha d^2/q, B_o=alpha k'/q.

This tangent-intersection formula was derived and separately reviewed in the preceding k115 work; it will be derived again here. The original foci are ±c on the horizontal axis; they are not silently replaced by the foci of this outer-locus ellipse.

For f=(c,0), squared distance factors exactly as

|Q(u)-f|^2 = alpha^2/q^2 (1+k sn u)(U+kV sn u).

The real expression is positive. For an inverse-polygon edge with endpoints Q(u-v),Q(u+v), let E(u) be its signed half-cross-product after unit inversion. Set

L0=(U^2-k^2 V^2 t)/d,
L1=(V^2-U^2 t)/C,
D(u)=1-k^2t sn^2u,
C0=B_o h d q^4/(alpha^3 C)>0.

Then exact addition algebra yields

E(u)=C0 dn(u)D(u)/[(d+kC sn u)^2(L0+kL1 sn u)].

Key intermediate identities:

(1+k sn(u-v))(1+k sn(u+v))=(d+kC sn u)^2/D(u),

(U+kV sn(u-v))(U+kV sn(u+v))
=(d+kC sn u)(L0+kL1 sn u)/D(u),

1/2 det(Q(u-v)-f,Q(u+v)-f)
=alpha B_o h d dn(u)(d+kC sn u)/(C D(u)).

The last two formulas have been checked by symbolic preliminary expansion and65-digit direct inversion, but await the final exact checker.

Let Z=W^2-4k^2t^2 q d^2>0. Triple-angle addition gives

L0=Z dn(3v), L1=Z cn(3v).

For odd primitiveN, L1 cannot vanish: 0<3v<3K and cn(3v)=0 would require v=K/3, hence N=6tau, impossible for oddN. The factor d+kC sn u has two simple zeros at r0±v, r0=3K+iK'. The factor L0+kL1 sn u has zeros at r0±3v. At a noncritical such zero E has at most a simple pole. The only odd-period critical coalescence is N3,tau1,3v=2K; there the linear factor has a double zero but dn(u) has a simple zero, leaving at most a simple pole. These locations do not coincide with r0±v for0<v<K. At the ordinary Jacobi poles the numerator and denominator have equal order3, hence removable singularities.

Thus E has at most double poles at r0±v and simple poles at r0±3v, together with imaginary translates. It is odd about r0 by Jacobi reflection (sn even about r0, dn odd). Hence the double-pole coefficients at r0+v and r0-v are opposite. Their separation is delta, so in F(u)=sum_(j=0)^(N-1) E(u+jdelta) these double parts cancel. All remaining poles lie in that one cyclic real orbit and its2iK' translate.

## Proposed final compact-torus step

For oddN the reduced real period is L=4K/N; F has anti-period2iK' and period4iK'. On C/(L Z+4iK' Z), its only permitted poles are simple, at R=r0+v and R+2iK'. F is not identically zero because every real edge contribution is positive: its direct numerator contains a+c sn u>0 and the real inverse denominators are squared distances. If no poles survived, compactness plus the anti-period would force F=0, contradiction. Thus these are exactly two simple poles.

F remains odd about r0 under cyclic reindexing, and is also odd about R because2v=delta is a period. It therefore vanishes at R+L/2 and R+L/2+2iK'. Those two finite distinct zeros exhaust its zero divisor and are simple. Hence F(u)F(u+L/2) is constant.

The opposite focus is obtained by shifting the outer phase by2K and centrally reflecting the inverted polygon; the reflection preserves signed area. Since2K=N L/2 andN is odd, this is exactly the half-real-period shift. Thus the target product is constant, if the stated complete pole/edge calculations survive final checks and separate review.

Preliminary direct real inversions for N3,5,7,9, including primitive stars, match the edge formula and constant product to65 digits. This is evidence only, not the proof.

## Credit and next steps

Canonical coordinates and classical Jacobi/pole methods are prior work. The source author of k903,a shared its frozen proof and warned that its isotropic-contact argument uses the foci of the original vertex ellipse; it was NOT imported for the outer-locus/original-focus problem. The present tangent-locus and edge reduction instead reuse explicitly derived formulas from this author's k115 and k804,a work. No claim of independent validation or historical novelty follows from this reuse.

Next: finish all exact coefficient identities, poles andN3 exception; assemble frozen complete proof and locally authored checks; independent uninvolved review before any claimed-resultPR. Remote checkpoint protects ongoing public mathematical work. Completion estimate75% of full proof-and-review deliverable. One substantive author turn is active; if unresolved, continue through five rather than stop early.
