# Independent analytic reconstruction before foreign/supplied evidence

The complete authenticated three-page published PDF, entire8651-byte controlling TeX and all three rendered pages were personally read before this note. No foreign primary body, deposited program/result, triage or old/current peer opinion was opened. Source payload bytes were hashed opaquely for custody, not semantically inspected as evidence. This is a falsifiable independent reconstruction of the deposited hypotheses and conclusions, not acceptance of a target verdict.

## Full literal claim and conventions

F_0=0,F_1=F_2=1,F_(n+1)=F_n+F_(n−1). For **every integer n≥3**, put q=F_n≥2,p=F_(n−1), and take exactly k=0,…,q−1. Write a=k/q, longitude2πpk/q, radius2sqrt(a(1−a)), height1−2a. These q distinct unit vectors z_k have minimum ambient Euclidean chord2/sqrt(q), attained by exactly one unordered pair, {z_0,z_1}. The minimum unit-sphere geodesic distance is consequently2arcsin(1/sqrt(q)). There is no finite upper cutoff on n or q.

The longitude is the exact rational p/q and the heights are unshifted. The singleton n=2 has no pair and is excluded; n≤1 is also outside the theorem. Including both k=0 and k=q creates q+1 points and changes the equality statement. Midpoint heights, irrational golden angle, arbitrary cardinality/step, discrepancy and globally optimal spherical packing are not included. The manuscript's ancillary source-convention isometries and classical arithmetic index are also checkable claims, but no priority/openness conclusion follows just from their citation.

The unit-sphere assertion follows by expanding4a(1−a)+(1−2a)^2=1, and heights make the points distinct independently of longitude. The direct north-pole witness has squared chord4/q for k=1. Only the all-pair lower bound and its equality cases therefore need proof.

## Arithmetic mechanism: an integer basis with opposed approximation errors

For any1≤m<q and any integer ℓ, choose the unique j≥2 with F_j≤m<F_(j+1). The repeated initial1 does not cause ambiguity because j≥2. Necessarily j≤n−1; put h=n−j≥1. The basis columns (F_j,F_(j−1)), (F_(j+1),F_j) have determinant F_j²−F_(j−1)F_(j+1)=(-1)^(j−1), hence every integer vector (m,ℓ) has unique integer coordinates S,T.

The first coordinate alone gives the complete sign restriction. S cannot be0, because m would then be a positive multiple of F_(j+1) smaller than F_(j+1). If T=0 then S>0. If T≠0, both positive exceed the allowed interval, and both negative give m<0. Therefore S,T have opposite signs. No restriction on the size or sign of ℓ is being silently inserted.

Induction in the defining recurrence gives

pF_j−qF_(j−1)=(-1)^(j−1)F_h,
pF_(j+1)−qF_j=(-1)^j F_(h−1).

Thus |mp−ℓq|=|S F_h−T F_(h−1)|≥F_h. This remains valid at h=1, where F_(h−1)=0, because S is a nonzero integer. Since m≥F_j, the product is≥F_jF_h.

For the weaker bound actually used by the spherical proof, the addition formula q=F_jF_(h+1)+F_(j−1)F_h≤3F_jF_h gives

m|mp−ℓq|≥q/3.

Every step is an identity/inequality of positive integers and is uniform in all n; a finite search over n would not establish it. The identities can each be proved from the two-term recurrence, with the j=2 and h=1 initial cases retained.

An independently useful strengthening is also available without importing the classical index theorem: F_(n−2)=F_(j−1)F_h+F_(j−2)F_(h−1)≤F_jF_h. Hence the same basis argument gives m|mp−ℓq|≥F_(n−2). For the complete dual lattice h_1+p h_2≡0 modq, if |h_2|≥q then the max(1,|h_1|)max(1,|h_2|) product is≥q; if h_2=0, the nonzero h_1 is a multiple ofq and gives the same conclusion. Otherwise change the overall sign to put1≤h_2<q and use the proved bound (coprimality prevents h_1=0 there). The vector (F_(n−2),1) lies in the lattice and attains F_(n−2), so the stated exact hyperbolic-cross index follows. This is an independent reconstruction of a credited classical fact, not a novelty claim or repair needed for the main result.

## Geometric mechanism: a two-variable minimum in hyperbolic coordinates

For a<b in[0,1], let d=b−a>0 and c=cos(longitude difference). Put

U=2(a+b−2ab), V=4sqrt(a(1−a)b(1−b)).

Direct Euclidean expansion gives D²=2(U−cV), U−2d=4a(1−b)≥0 and U²−V²=4d². For c≤0, this immediately gives D²≥4d. Equality requires U=2d and cV=0.

A separate analytic derivation of the positive-cosine bound is to set U=2d cosh u,V=2d sinh u for u≥0. For0<c<1 let v=artanh(c). Then

U−cV=2d sqrt(1−c²) cosh(u−v)≥2d sqrt(1−c²).

Thus D²≥4d sqrt(1−c²). This minimizes over a larger continuous latitude domain, so it is a lower bound without any assumption that the minimizer is an actual discrete pair. It also explains the paper's algebraic certificate (U−cV)²−4d²(1−c²)=(V−cU)². No false distance-preservation property of an equal-area planar map is required. At c=0 either route is consistent; c=1 is separately excluded for the actual nonzero rational residues below.

The geometric bound is genuinely sharp on its continuous domain: at a=1/4,b=3/4,c=3/5, one has U=5/4,V=3/4,d=1/2 and both sides of the second inequality equal8/5. Pole and endpoint cases also remain literal rather than hidden in division by a radius.

## All-pair reduction, strict branch and uniqueness

For arbitrary0≤i<j<q set m=j−i. Consecutive Fibonacci numbers are coprime, by the Euclidean recurrence. Therefore a least-absolute residue r=mp−ℓq exists with0<|r|≤q/2. A tie at |r|=q/2 when q is even can be given either sign; it has c=−1 and causes no ambiguity in the proof. The actual c is cos(2πr/q), never1.

If c≤0, D²≥4m/q≥4/q. If c>0, the chosen angle satisfies0<2π|r|/q<π/2. Concavity gives sin(2π|r|/q)≥4|r|/q. The geometric and arithmetic bounds consequently give

D²≥(4m/q)sin(2π|r|/q)≥16m|r|/q²≥16/(3q)>4/q.

This branch has a fixed relative margin of4/3 against the desired squared minimum. No floating-point sign test or asymptotic estimate enters the universal argument. Quarter residues, if present, give c=0 and belong to the nonpositive branch, not the strict open branch.

Equality therefore can only lie in the nonpositive branch. It forces m=1 and U=2d. Since b=j/q<1, U−2d=4a(1−b) forces a=0, so i=0,j=1. Its squared distance is4/q by the direct pole calculation. The q=2,3,5 cases are already included; q=2 has just that one unordered pair. Geodesic distance is the strictly increasing function2arcsin(D/2), so the secondary minimum follows without a new optimization argument.

For exact finite diagnostics, no transcendental chord calculation is needed to certify the lower bound: the sign branch is decided by whether4|r| is at leastq. Nonpositive-cosine nonwitnesses with m≥2 have a rational margin4(m−1)/q; those with m=1 and i>0 have the positive rational margin at least8i(q−i−1)/q² from U−2d. The positive branch has the rational lower certificate16m|r|/q². These certificates are consequences of the written infinite proof, not a replacement for it.

## Convention isometries and boundary falsifiers

The endpoint-shifted set k=1,…,q is isometric to k=0,…,q−1: replacing k byq−k negates longitude and height, and the orthogonal map(x,y,z)↦(x,−y,−z) gives the stated correspondence. If both endpoints are included, the south pole is an additional distinct point and the pair {q−1,q} also attains4/q, so uniqueness cannot be copied unchanged to that q+1-point set.

For the reversed planar order, let the alternative point indexed j have latitude {pj/q} and longitude j/q. Reindex k≡pj modq. Cassini gives p²≡(-1)^n modq, so j≡(-1)^n p k modq. The spherical longitudes therefore agree for even n; odd n needs the reflection of the second Euclidean coordinate. This is an unordered-set isometry, not equality of the original point labels. The exact primary definitions still need to be read after this seal.

The distinctions are falsifiable. Midpoint heights at q=2,p=1 give two antipodal points, chord2 rather than sqrt2. An arbitrary coprime rational step is also insufficient: take q=16,p=1,i=7,j=8. Then D²=2−(sqrt63/4)cos(π/8)<1/4=4/q, since cos²(π/8)=(2+sqrt2)/4 and sqrt2>10/9. This is an excluded non-Fibonacci construction, not a counterexample to the stated theorem. No claim that all other conventions fail is needed.

## Early status and remaining tasks

The full literal all-n theorem and unique equality case admit the reconstruction above; no central mathematical gap is currently identified. All central inequalities are self-contained. The exact primary conjecture/range conventions, classical index attribution and any bibliographic or priority qualifications remain to be checked from actual primary bodies after sealing this note. Optional deposited code/data have not yet been inspected. Bounded computations may falsify implementations or certify finite instances, but cannot establish all n. No world-first, current-open or independently-originated-method claim is inferred. No research follow-up is proposed. Findings remain withheld from root until the114initial-independence gate opens.
