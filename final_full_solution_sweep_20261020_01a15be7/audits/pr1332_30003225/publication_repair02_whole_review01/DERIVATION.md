# Independent reconstruction before legacy code/review

Written 2026-10-22 after fresh duplicate checks, after reading main.tex and the actual original arXiv definitions pp.5–7 and conjecture p.31; before any preparer/earlier reviewer proof checker or DERIVATION/REPORT. This is a new written argument, not a code verdict. Completion of bounded mathematical review: 40%; priority and package review pending.

## Claim reconstructed

Work with C-valued formal centered arcs of the smooth plane; order(0)=infinity and all equalities of closed sets mean reduced supports. Use centers c1=origin, c2=zero tangent, …, cn, D_j created by c_j. Fix k centers, 2<=k<n. The set must range over every final prime divisor of the all-free minimal chain sharing these centers. It must not silently range over only singular-branch resolution divisors or raw transverse arc loci. The original pp.5–7 explicitly allow free divisors and extra free centers following a smooth curvetta. The conjecture's undefined bare equivalence and Remark4.14's indexing are limitations of interpretation, not license to claim unique authored intention.

## Geometry, independently checked

At the jth newest component use coordinates (x,u), where the plane map is y=P_{<j}(x)+x^j u. Its old-component intersection is u=infinity, for j>=2. A finite center u=a is free. Its blowup charts are (x,v), u=a+xv, and (b,h), x=bh, u=a+h, with v=1/b. On the latter new component h=0 and old strict transform b=0; b=0,h=0 is the unique point missed by the former chart, and is satellite. Induction proves that all finite a_k,…,a_{n-1} occur, and every free continuation of the minimal predecessor chain occurs exactly once. A different older component choice would not be a minimal predecessor chain to this final divisor; a satellite continuation changes proximity data. First fixed tangent excludes the infinity tangent as a free *initial* alternative, so the j>=2 restriction matters.

Subtract P(x) to call the second plane coordinate z. The final two maps are (x,w)->(x,x^n w), (b,h)->(bh,b^(n-1)h^n). Any arc centered on the new component gives ord x>=1,ord z>=n, including the old/new intersection. These finite coefficient conditions define an integral polynomial coefficient ring. The open locus x_1!=0 is nonempty, hence dense. Every arc there divides z by x^n and meets the new component transversely in the finite chart. Thus the closure is exactly S_P={ord z>=n} in centered arc space. For arbitrary S_P arc, keeping z fixed and replacing x by x+s t gives a polynomial coefficient specialization with dense parameter values transverse; it also handles x identically0 and the constant arc. No single deformation uniform in P is required by an intersection of closures. Arcs whose original plane image is constant are obtained only as limits; no unique lift is falsely asserted for them.

## A jet-linear-map route to the universal intersection

Fix an arbitrary truncation of a formal arc to degree n-1. Write L_x:C^(n-k)->tC[t]/(t^n), (a_e)->sum_e a_e x(t)^e modulo t^n. Requiring the same y-jet to equal L_x(a) for **every** a says y_low=0 (take a=0) and L_x=0 (take basis vectors). Its first column is x^k; all later columns vanish if that one vanishes. Since C[[t]] is a domain, x^k=0 modulo t^n iff k*ord x>=n, including x=0. Therefore the intersection is precisely ord y>=n,ord x>=ceil(n/k), without a generic parameter assumption. For the exact-contact subset a_k!=0, its affine span is all parameter space: choose a_k=1 and2 and all other coordinates independently. Subtract the two equations to force the first column, then force all others. It has exactly the same intersection. This is also an independent way to challenge whether nonreduced coefficient equations have been substituted for their radical: over a non-domain coefficient ring the inference can fail, and no such scheme equality is asserted.

## Reference contact cylinders for all positive integers

For D_j the same charts with P=0 show that exact order q along its local defining equation x or h forces ord x>=q and ord y>=j q. The second chart is needed here; at a satellite point ord b>=1 only increases plane orders. The order cylinder is irreducible, and its open locus with ord x=q lifts through w=y/x^j and has exact contact q. Hence it is the closure, for both exact and >=q conventions. For j=1 use its ordinary two charts (bh,h), so no nonexistent old component is assumed. The statement remains about closures of nonconstant arcs; coordinate-zero and constant arcs enter by specialization.

## Uniform falsification and positive boundaries

Independent order thresholds distinguish two cylinders: test monomials with the other exponent taken large. With r=ceil(5/k), r=3 or2, equality to reference(q,jq) forces q=r and jr=5, impossible for every integer j>=1. Uniform witnesses: if q<r take (t^q,t^max(5,jq)); if q>r take (t^r,t^5); if q=r and jr>5 take the latter; if jr<5 take (t^r,t^(jr)). They work even when j exceeds the number of original centers, using the continued zero chain. No finite q,j search proves this quantifier.

The formula agrees with D_k multiples exactly when k divides n. It also agrees with other D_j if ceil(n/k) divides n and j=n/ceil(n/k), an allowed distinction from the text's particular D_k sentence. Fixing the final center is the singleton S_0, not an obstruction. Varying the tangent too intersects all directional order constraints and gives equal thresholds(n,n), hence D_1 contact n. These are positive controls, not refutations.

## Why this does not refute arbitrary divisoriality

I independently generate primitive weights by toric star subdivisions. From coordinate rays, insert(1,1),(1,2),(2,3),(3,5) for the first weight; for the second insert(1,1),(1,2),(1,3),(2,5). Each ray is sum of its then adjacent determinant-one neighbors, realized by blowing up their intersection. The resulting toric prime has a dense transverse exact-order locus with plane orders equal to its weight. Adjacent charts have nonnegative exponents; their images lie in the corresponding lower-order cylinder, and the exact-order locus is dense in that cylinder. Thus both computed intersections ARE primitive divisorial Nash sets. It would be false to call them non-Nash sets. The counterexample concerns only the specified reference ray, not Conjecture2, all divisors, general Nash surjectivity or arbitrary scheme intersections.

## Independent diagnostics to follow

Use a newly written truncated-series linear-map test over Q, plus independently generated toric rays and chart substitutions, exact-contact affine-span tests, degeneration/satellite tests, and negative/positive controls. Run ordinary, -O,-OO. Finite tests challenge the written universal proof and do not prove arbitrary complex parameters or infinite arcs. I have not read any prior checker/reviewer derivation at this checkpoint.

## Post-reconstruction adversarial checks and additional proof details

The pre-checker text above remains unchanged in its separate file. After writing it, I read the packaged checker and original PR materials; they do not replace this independent argument. The new normal/-O/-OO diagnostic outputs match exactly (62,340 checks,43,904 jet cases). The archived programs and all six products were separately replayed/rebuilt.

For the nonreduced four-jet caveat, set I=(x1^2,2x1*x2,x2^2+2*x1*x3). Since x1^2 is in I, x1 belongs to radical(I); modulo I, x2^2=-2*x1*x3, whence x2^4=4*x1^2*x3^2=0. Thus x2 belongs too. Conversely I lies in the prime ideal(x1,x2), so this is exactly its radical. Homogeneous generators of degree2 cannot generate the degree1 polynomial x1. For the cubic case, x1^3 is a generator and every generator is divisible by x1, giving radical(x1). Linear y-coefficients have already been eliminated; these are statements about the indicated two-member ideals, not a claim of nonreduced equality for the entire family.

For the all-tangent positive boundary, two complete zero free chains following the coordinate axes already force ord y>=n and ord x>=n. Those bounds imply the cylinder condition for every free chain with any tangent after an invertible linear coordinate change and a polynomial jet subtraction. Hence the full all-tangent intersection is precisely(n,n), equal to contact n along the first exceptional divisor. For a fixed final center, no parameters remain and the single Nash cylinder is(1,n). Both limits oppose a careless blanket negative.

At n5 the order pairs(3,5)/(2,5) have gcd1 and correspond to actual primitive toric primes. Adjacent charts with exponents(3,1;5,2) and(2,1;5,3) have determinant1 and inverse monomials as displayed in the manuscript. Their dense exact-order loci lift with transverse order1 and the other coordinate a unit. A wrong claim that these intersections are non-Nash sets is therefore mathematically false, independently of any source-notation question.

The two chart maps require regular formal coordinates. A separating polynomial arc may have z/x^n of negative order and so not lift to a finite free chart; no such lift is asserted. Its membership is in the closed Nash set, and the direct polynomial coefficient deformation establishes it individually for each P. The intersection of closures is not replaced by the closure of an intersection.

The original actual source and all explicit interpretation mappings have been checked. For p0=c1,p2=c3 and at least2 common centers one obtains I52/D3; for fixing selected c3 one obtains I53/D3; last-shared convention gives I52/D2; one-based labels give I53/D3. The arithmetic excludes every continued D_j anyway. Conditional exact contact k is correctly a_k!=0. These exhaust the readings expressly claimed, not every conceivable unstated replacement.

No substantive objection remains within this exact qualified theorem. Finite diagnostics, archive hashes, priority search and source interpretation are different evidentiary tasks and have not been conflated.
