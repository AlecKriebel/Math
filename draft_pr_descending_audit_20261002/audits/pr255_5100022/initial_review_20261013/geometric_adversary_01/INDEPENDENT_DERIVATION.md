# Independent Cartesian construction, real domain and analytic completion

Reviewed target: PR255, problem 5100022 / AMR-050-0022 / k404. Frozen PROOF.md SHA256: b8edd78d03dac33a7be77837649eef7a8558900b3499774725174836fa54d462. This derivation was written without consulting the sibling review or submitted historical independent review. Its exact and numerical Cartesian checkers were constructed before the submitted checker was read.

## Exact objects and assumptions

The original side pedal is formed from orthogonal projections of a fixed original focus onto the original billiard side lines. The original antipedal is formed by intersecting the consecutive lines through original impact points perpendicular to their rays from that focus. All polygon areas below are ordered signed shoelace areas; no region-union or vertex-average convention is used.

The claim is constancy of the literal quotient A*/A for a fixed confocal pair and primitive least period N≡2 mod4, including star winding classes, all real phases and either focus. The outer ellipse is noncircular and its caustic is a strictly nested nondegenerate confocal ellipse. The denominator must be nonzero; the numerator need not be. These hypotheses imply the smallest nonempty period in the requested class is six. Artificial repetition of a different primitive parity is not included.

The source row and constructions agree in [arXiv v11, Table5 and Sections2/3.3/3.5](https://arxiv.org/pdf/2004.12497v11) and the [published paper, Table5 p348](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). Both mark this ratio as unproved there. This source observation establishes the original question; it does not establish current historical openness.

## Canonical family completeness

Normalize the caustic major semiaxis to one. Its semiaxes are 1 and b0=sqrt(1-k²), with 0<k<1 and foci (±k,0). For each fixed strict confocal outer ellipse, b>b0 gives a unique v∈(0,K) satisfying cn(v)=b0/b: cn decreases continuously from one to zero on this interval. Confocality then gives a=dn(v)/cn(v). Thus this coordinate choice excludes no strict ellipse pair.

The credited [Stachel Theorem4.3 and equation4.9](https://repositum.tuwien.at/bitstream/20.500.12708/136087/1/Stachel-2022-European%20Journal%20of%20Applied%20Mathematics-vor.pdf) identify the billiard map as w↦w+2v in P(w)=(-a sn(w),b cn(w)), with caustic contact at B(w+v)=(-sn(w+v),b0 cn(w+v)). That theorem includes turning number τ and gcd(N,τ)=1. Our exact tangent calculations below independently check the resulting chords and contacts, while our Cartesian diagnostics also check the physical specular law.

The real parametrization P is injective modulo 4K, since (sn,cn) traverse the unit circle once. Therefore least closure N means N(2v)=4Kτ with gcd(N,τ)=1. Reversing the orientation if necessary selects 0<τ<N/2 and v=2Kτ/N. This is the full positive-orientation strict elliptic-caustic family, including stars, rather than a selected sampled phase.

Write N=2m. Coprimality implies τ odd, gcd(τ,m)=1 and m(2v)=2Kτ≡2K mod4K, so the second half of the orbit is the central inversion of the first half. Cyclic relabeling gives area period δ=2v. Inversion switches the foci and preserves signed area; the half-orbit relabeling then makes the two focal areas equal and gives area period 2K. Bezout applied to δ=τh and 2K=mh, where h=2K/m, proves h is a period of every focal area function under consideration. No minimality assertion for h is needed.

## Direct Cartesian chord and antipedal intersection

For a side with contact parameter u, put s=sn(u), c=cn(u), d=dn(u), t=sn(v), C=cn(v), D=dn(v), and L=1-k²t²s². Jacobi addition gives its endpoints P-=P(u-v), P+=P(u+v). Direct averaging and subtraction give

M=(P-+P+)/2=(-sD²/L,b0c/L),

H=(P+-P-)/2=-Dt d/(CL)(c,b0s).

The actual caustic tangent normal is n=(-s,c/b0). It satisfies n·M=1, n·H=0 and n·B(u)=1. Its gradient relation to x²+y²/b0²=1 verifies tangency. The endpoints lie on x²/a²+y²/b²=1, and a²-b²=k². All these are exact polynomial reductions in the fresh checker.

For F=(k,0), write the two antipedal equations as

(M-F-H)·(U-M+H)=0,

(M-F+H)·(U-M-H)=0.

Subtracting gives H·(U-2M+F)=0. Since H⊥n, U=2M-F+ηn. Adding then gives η=(|H|²-|M-F|²)/((M-F)·n), and (M-F)·n=1+ks. Substitution and cancellation produce exactly the submitted formula

Ux=-[E0s+k(C²-D²s²)]/(C²L),

Uy=c[2b0²-E0(1+ks)]/(b0C²L),

where E0=1-2k²t²+k²t⁴. The fresh checker derives η from the line equations, reduces both components against this expression, and separately substitutes into the original endpoint line equations.

The same Cartesian calculation gives

det(P--F,P+-F)=2b0Dt d(1+ks)/(CL)>0

for every real u: b0,D,t,d,C are strictly positive, |s|≤1, 1+ks≥1-k>0, and L≥1-k²t²>0. Thus every actual antipedal intersection is finite. Geometrically, a caustic tangent cannot contain its interior focus. Reflecting in the origin proves the same for F=(-k,0).

## Actual original-side pedal and strict positive signed area

The perpendicular projection onto the actual side n·X=1 is

q=F+(1-n·F)n/(n·n)=((k-s)/(1-ks),b0c/(1-ks)).

The checker derives this projection, proves the side incidence and perpendicularity, and also obtains q·q=1. This circle property is not used to infer area positivity.

Write q-F=ρ n_hat, where ρ=(1+ks)/|n|>0 and n_hat is the outward unit normal. The lifted angle ψ of n satisfies

ψ'(u)=det(n,n')/|n|²=d/(b0|n|²)>0.

The pair (sn,cn) makes one real turn in 4K, and its nonsingular linear transformation n makes one turn as well. Central inversion gives ψ(u+2K)=ψ(u)+π. Since 0<δ<2K,

0<ψ(u+δ)-ψ(u)<π.

Therefore every consecutive determinant relative to F is positive:

det(q(u)-F,q(u+δ)-F)=ρ(u)ρ(u+δ)sin(ψ(u+δ)-ψ(u))>0.

For the closing edge, use the lifted parameters u+(N-1)δ and u+Nδ=u+4Kτ, whose points agree with the first point. Its angle increment still lies strictly between zero and π. Thus the signed area A=(1/2)Σdet(qj-F,qj+1-F) is strictly positive, even if the polygon is a star. Translating back from F does not change shoelace area. Reversal changes every area sign, and repeating an already-admissible polygon scales both areas equally.

This is an all-period real-domain proof. The numerical tests check it independently for sampled Cartesian polygons but are not its justification. Positivity may tend to zero at an excluded boundary; there is no uniform lower bound asserted across all ellipse pairs.

## Independent audit of the analytic completion

The geometric calculations alone prove finiteness and positive denominator, not family constancy. I checked the submitted analytic completion separately, using the standard [Jacobi period/pole tables](https://dlmf.nist.gov/22.4) and [addition identities](https://dlmf.nist.gov/22.8). This section independently verifies that argument; it does not claim a distinct purely real proof of the invariant.

On the 2K,2iK' lattice, sn² has one double pole. L therefore has exactly two zeros counted with multiplicity. They are iK'±v, and are simple since sn=±1/(kt), while cn and dn there are nonzero for the strict parameters. Common sn/cn poles in U are removable, since its numerator and denominator have matching maximal order two. Thus U has at most simple poles at those two points. The area B(w)=(1/2)Σdet(U(w+v+jδ),U(w+v+(j+1)δ)) has at most double poles only at w=iK'-jδ modulo the stated lattice. On the h,4iK' torus these reduce to precisely the two possible points iK' and 3iK'.

Inversion plus half-orbit relabeling gives equality of the two focal areas. Reflection in the y-axis maps antipedal index j to -j-1 and switches focus: reflection and traversal reversal each negate area, so together B(-w)=B(w). The 2iK' shift fixes sn and negates cn; this reflects in the x-axis without reversing index order and fixes either focus, so B(w+2iK')=-B(w). Consequently B(iK'+z)=-B(iK'-z), which eliminates the possible double-pole Laurent term. Every remaining pole is at most simple.

S(w)=Σdn(w+jδ) has periods h,4iK', imaginary anti-period 2iK', and exactly two simple poles on that torus. At iK' only j=0,m contribute; their 2K real shift gives equal nonzero residues, rather than cancellation. Matching the first residue of B with a scalar multiple of S matches the second by anti-periodicity. The difference is holomorphic on a compact connected torus, hence constant; the anti-period forces that constant to vanish. Thus B=bF S, with bF real by real evaluation. A zero bF is fully allowed.

For the pedal trace T(u), the only possible singularities of q are sn(u)=1/k, among the dn-zero translates of r=K+iK'. Common Jacobi poles are removable. At r,

sn(r+z)=dn(z)/(k cn(z)), cn(r+z)=-i b0/(k cn(z)),

so q(r+z) is even and has at most a double pole. Its two incident area terms combine into (1/2)det(q(r+z),q(r+z+δ)-q(r+z-δ)). The second vector is odd and regular because 0<δ<2K prevents adjacent singularities from coinciding. Their product therefore has at most a simple pole. Nonadjacent singular vertices occur in separate summands and do not raise the order. The same real period and imaginary anti-period put these poles at the two poles of S(u+K). The same compact-torus argument yields T(u)=pF S(u+K).

Finally, the actual pedal area at impact phase w is T(w+v). Since m and τ are odd, K+v=((m+τ)/2)h is an integer period, giving A(w)=pF S(w). On the real axis S>0, while the geometric argument gives A>0, so pF>0. Hence A*/A=bF/pF everywhere in the real family. Equality for both foci has already been justified. When m is even this alignment becomes a half-integer shift; the parity cannot be discarded.

An independent local identity for the original area also checks the phase bookkeeping: det(P-,P+)=2ab tC d/L, while dn(u-v)+dn(u+v)=2Dd/L. Summing the edge identities gives original area ab tC/D·S(w)>0, consistently in impact phase w.

## Exact zero-numerator example

The direct Cartesian six-orbit exploration retained in explore_exact_six.py uses vertices (0,b),(-1,br),(-1,-br),(0,-b),(1,-br),(1,br), with a²=1/(1-r²), b=ar/(1-r), 0<r<1/2. Its tangent-side condition determines a strict confocal caustic with major semiaxis one. At the single symmetric phase, the derived ratio is

γ=(3r-1)/[r²(r-2)²(1-r)].

Taking r=1/3 produces a zero numerator. The standalone exact certificate exact_zero_numerator.py verifies the concrete case without assuming family constancy:

outer semiaxes a=3√2/4, b=3√2/8;

caustic semiaxis squares 1 and 5/32; confocal gap 1/8;

foci F=(±3√6/8,0);

vertices (0,3√2/8),(-1,√2/8),(-1,-√2/8),(0,-3√2/8),(1,-√2/8),(1,√2/8).

All six vertices are distinct, all consecutive chords are tangent with contact strictly inside the segment, every specular reflection is exact, every focal-normal determinant is positive, and every focal-pedal determinant is positive. The ordered polygon is convex with winding one and least period six. Exact signed areas are original √2, focal pedal 10√2/9, and focal antipedal zero at either focus. Thus the permitted zero numerator is a concrete real case. The all-phase zero conclusion follows only after applying the separately audited universal theorem. No novelty claim is made for this example.

## Reproducible checks and boundaries

cartesian_exact_checks.py gives 45 exact geometric certificates and 3,358 primitive-index arithmetic controls. It uses independent endpoint addition formulas and solves the actual focal line system. Its additional exact 8/3 star is a previously used control, not a new construction.

cartesian_numeric_checks.py uses only canonical impact vertices followed by actual Cartesian side projections and two-line solves, with 180 decimal digits and relative tolerance 1e-80. It checks 62 permitted families at 186 phases, both foci, 79,266 comparisons. This includes k=1e-25, k=1-1e-40, N=202 with winding99, N=102 with winding49, contact-in-segment, caustic tangency, actual reflection, winding, individual pedal positivity, closing edges, reversal and repetition. The largest recorded relative error is below 4.21e-140. Four excluded-parity controls show nonconstant k404 ratios while retaining the general even antipedal/original ratio.

The original checker was then read fully and replayed. Its receipt is byte-identical: 27,524 exact controls and 27,320 separately labelled 90-digit diagnostics. All frozen-manifest hashes match.

Circular, hyperbolic and degenerate caustics remain excluded. Near-circle controls agree with the regular-polygon limit but do not silently enlarge the theorem. Very thin caustics create small determinants and large quotients, so ordinary machine precision would be inadequate; the rigorous inequalities and explicit high precision address this separately. No numerical evidence is used as a proof of universality.
