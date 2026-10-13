# Independent mathematical audit: weighted affine-line endpoint partials

Problem 30003235 / OWR-15169-009, queue rank 995. Review completed 8 October 2026 UTC. This is an independent AI-assisted mathematical audit of a frozen author packet, not human peer review or formal proof verification.

## Decision

**Accept the stated scoped partial results. Do not mark the intended general problem solved. No mathematical correction patch is required.**

The rational-point-line endpoint proposition is valid, conditional only on the accurately credited weighted dual characterization and coordinate-fiber theorem. The continued-fraction construction, horizontal scope counterexample, nearby-weight corollary, near-parallel estimate, and determinant rank bound are also valid. The packet correctly identifies the missing step in each unsuccessful general approach.

The reviewed input is the 17-file frozen packet whose MANIFEST.json has SHA-256:

`b499c40203ef2203d86d3dd6fd6e612944d7cbad92edb801170626965bc07b90`

The manifest identifies 16 payload files; the manifest itself is the seventeenth file. Every byte count, payload digest, filename, and cumulative proof checkpoint was independently checked. The original packet was not edited. This report and its controls are separate artifacts and contain no copied source documents, source extracts, datasets, or private coordination material.

## 1. Target and source conditions

The intended statement concerns 0<i,j<1, i+j=1, sigma=min(i,j), tau=1/sigma, and a nonzero slope a. With M(q)=max(||qa||,||qb||), the proposed implication is that a positive lower bound for q^tau M(q) yields Hausdorff dimension one for Bad(i,j) on y=ax+b. This remains unproved in the packet for general irrational a and b outside Q+Qa.

The report's p.2780 prints the epsilon-removal question without explicitly excluding a=0. The reviewer inspected its rendered page. ABV's published Theorem 1.2 expressly assumes a!=0 and references the positive-weight condition (1.1). Its Remarks 3–5 confirm the common 1/2-winning projection, endpoint necessity, and different horizontal exponent. The published page 152 was visually inspected; pp.152–153 and the weight definition were checked in text. [OWR report](https://ems.press/content/serial-article-files/46650), [ABV published paper](https://eprints.whiterose.ac.uk/id/eprint/124399/1/1_s2.0_S0001870817303286_main.pdf).

The reviewer additionally checked the original An preprint, Theorem 1.2 and the accompanying remarks: fixing the first coordinate of weight s requires inf q^(1/s)||q theta||>0 and gives a 1/2-winning fiber. Exchanging coordinates supplies the horizontal version used here. The original theorem's statement and conventions were inspected, not its entire proof re-proved. [An, Badziahin–Pollington–Velani's theorem and Schmidt's game](https://arxiv.org/pdf/1203.2996).

The four public PDF hashes and byte counts recorded by the author match the available PDF bytes. Retrieval timestamps remain the author's recorded history; this audit does not treat a timestamp as independent proof of an earlier action. The five checkpoint files are cumulative prefixes of the final proof, and the fifth equals it exactly. There are five distinct mathematical method sections. These facts validate the recorded artifact sequence, not a quantitative measure of research effort or an externally timestamped chronology.

The duplicate/priority search described in GATE.md was not independently repeated across every repository or historical reference. No novelty, exhaustive literature coverage, or global current-openness conclusion is accepted or needed.

### Scope at weight zero

At i=0 or j=0, tau is undefined. None of the formulas with 1/sigma are assertions at those boundary weights. Under the usual convention, Bad(1,0)=Bad x R and Bad(0,1)=R x Bad. A nonzero-slope line has a full-dimensional intersection with either of these elementary sets, but that separate observation does not extend the displayed endpoint hypothesis to a meaningless exponent. The proof maintains positive weights throughout. Equal weights i=j=1/2 are included without difficulty.

### Equivalent normalizations and finite initial denominators

The definition max(q^i||qx||,q^j||qy||)>=c is equivalent to the power-normalized definition used in the sources: taking positive fixed powers changes the witnessing constant. Constants need not be uniform across points.

A positive endpoint liminf is equivalent to an all-q positive lower bound here. If M(q*)=0 for any positive q*, then both a and b are rational and M(kq*)=0 for every positive k, contradicting the liminf. Otherwise the finitely many initial values q^tau M(q) have a positive minimum. This argument would not automatically apply to arbitrary inhomogeneous definitions, but the packet uses the homogeneous coefficient condition.

## 2. Approach 1: continued fractions and the horizontal counterexample

For real t>=2, the construction begins with q0=1, q1=2 and uses a_(n+1)=ceil(q_n^(t-1)). Hence

q_n^t <= q_(n+1) <= q_n^t+q_n+q_(n-1) <= q_n^t+2q_n <= 3q_n^t.

The infinite continued fraction defines an irrational alpha between 1/3 and 1/2. The standard consecutive-convergent estimates give

1/(4q_n^t) < ||q_n alpha|| < 1/q_n^t.

Indeed q_n+q_(n+1)<=4q_n^t, and from q1 onward the convergent numerator is the nearest integer. Best approximation of the second kind gives the lower bound for all q_n<=q<q_(n+1), since q>=q_n. The initial q=1 follows from alpha>1/3. Thus inf q^t||q alpha||>=1/4, whereas multiplying the convergent upper estimate by q_n^(t-epsilon) gives a quantity tending to zero for every epsilon>0. The proof is valid for real t, not merely integer t. Finite controls do not establish the infinite tail or replace the quoted continued-fraction facts.

Consequently a=alpha, b=0, t=tau is a genuine nonzero-slope endpoint instance outside every positive-excess-exponent hypothesis. This defeats a direct attempt to subsume the endpoint under a strict-exponent theorem. It is not a bad-approximation counterexample.

For the horizontal scope test take a=0, i=1/3, j=2/3, and use t=2 for b. The construction yields q^3||qb||>=q/4 and even q^(5/2)||qb||>=q^(1/2)/4. However q_n^(3/2)||q_n b||<q_n^(-1/2) tends to zero. The dual forms (0,q_n,-p_n) have height q_n^(3/2) and values independent of x. Their normalized values tend to zero at every point of the horizontal line, so its intersection with Bad(1/3,2/3) is empty. The wider literal statement is false even with a positive excess exponent. The intended nonzero-slope problem is unaffected.

The necessity calculation is correct. Choosing B=q and nearest integers A to -qa and C to -qb gives a form bounded by (1+|x|)M(q), and height at most (1+|a|)^(1/i)q^tau. A dual lower bound for one point forces the endpoint coefficient bound. This only proves necessity. It cannot be reversed by manipulating those selected forms, since membership requires control of all integer dual forms.

## 3. Approach 2: nearby weights and common winning parameter

Fix the original tau0. For each new positive pair with smaller minimum weight, taun>tau0. The choice epsilonn=(taun-tau0)/2 gives

q^(taun-epsilonn)M(q) >= kappa q^((taun-tau0)/2).

Every pair therefore separately satisfies the strict-exponent hypothesis. The projected sets all have the same winning parameter 1/2, which is the essential fact for taking their countable intersection. No uniform separation of their minimum weights from the original minimum, and no uniform positive epsilonn, is required. The graph parametrization is globally bi-Lipschitz, giving dimension one on the line.

There is no continuity principle permitting passage to the critical weight. The scalar diagnostic u_q=v_q=q^(-1/2)/log(q+1) is valid as an inequality-level test: the critical normalized maximum tends to zero, while every fixed unequal pair has normalized maximum q^delta/log(q+1) with positive infimum. The packet explicitly refrains from claiming these arrays are the actual approximation errors of a real vector. It correctly uses the diagnostic only to identify the missing uniform estimate.

## 4. Approach 3: detailed audit of the endpoint partial

### 4.1 Rational translations

For r,s rational choose d>=1 with dr,ds integers. Multiplying a translated dual form by d gives coefficients dA,dB,dC-dAr-dBs at the original point. Its height is at most d^(1/sigma)H(A,B). If the original dual lower bound is c, the translated point therefore has lower bound at least c/d^(1+1/sigma). The extra factor d comes from the value of the form itself. The author states only that the new factor is fixed and positive, which is sufficient and correct. Applying the inverse rational translation gives equivalence.

No real-translation invariance is licensed. The rationality is exactly what makes the transformed coefficients integral after one fixed dilation.

### 4.2 Inversion in the heavier coordinate

Assume i>=j and x!=0. Put (u,v)=(1/x,y/x), and consider F=A'u+B'v+C' with (A',B') nonzero. Let H'=max(|A'|^(1/i),|B'|^(1/j)). Integer nontriviality gives H'>=1.

If |F|>=1, the new normalized form is already at least one. For |F|<1, put K=1+|u|+|v|. Then

|C'| <= 1+|u||A'|+|v||B'| <= K max(|A'|,|B'|).

The transformed old form is xF=C'x+B'y+A'. Because i>=j, integer B' satisfies |B'|^(1/i)<=|B'|^(1/j), including B'=0. Consequently

H(C',B') <= K^(1/i)H'.

When (C',B') is nonzero, the old dual bound gives

H'|F| >= c(x,y)/(|x|K^(1/i)).

The exceptional pair (C',B')=(0,0) must not be fed to the old dual theorem. It instead has A'!=0 and directly gives

H'|F|=|A'|^(1+1/i)/|x| >= 1/|x|.

Thus the minimum of 1, c/(|x|K^(1/i)), and 1/|x| is a positive new constant for every integer form. The map is an involution and preserves x!=0, so the identical reasoning yields the converse. All constants may depend on the point, as the definition permits.

The proof is valid for arbitrary positive real weights with i>=j, including equality. Inverting the lighter coordinate without exchanging weights would invalidate the displayed height estimate. The independent controls include an explicit failure of that estimate in the reversed order. This is a restriction of the supplied proof, not an assertion that every other possible transformation fails.

### 4.3 Reducing coefficients at a rational point

If (r,s) is rational on the line, b=s-ar. Choose d as above and K=max(d,|dr|). For each positive integer q,

||dq a||<=d||qa||, and ||dq b||=||(dr)qa||<=|dr| ||qa||.

Hence M(dq)<=K||qa||. An all-q lower bound M(q)>=kappa q^(-t) implies

||qa|| >= kappa d^(-t)K^(-1)q^(-t).

The converse follows immediately from M(q)>=||qa||. No assumption about primitivity of denominators is needed. The stronger positive hypothesis forces a irrational. In particular, the endpoint implication for a rational-point line of rational slope is vacuous because its intercept is then rational too.

For a!=0, take p nearest to q/a. For sufficiently large q, p!=0 and |p|<=C_a q, where for example C_a=|1/a|+1 suffices. Then

|a| ||q/a||=|q-pa|>=||pa||>=kappa |p|^(-t)>=kappa C_a^(-t)q^(-t).

Negative p causes no difficulty because ||pa||=|| |p|a||. The finitely many remaining q have positive distances since a and 1/a are irrational. Exchanging a and 1/a proves equivalence in both directions. The argument applies to every t>0 as stated.

### 4.4 Fiber reduction and local dimension

After the rational translation the line is (x,ax). When i>=j, sigma=j and inversion takes it to (u,a). The coefficient reduction is precisely inf q^(1/j)||qa||>0, so the credited horizontal fiber theorem applies. Let W={u:(u,a) is in Bad(i,j)}. W has Hausdorff dimension one in every nonempty interval.

For clarity about the pole and dimension, on a compact interval J with 0<delta<=|x|<=R and constant sign,

|x-x'|/R^2 <= |1/x-1/x'| <= |x-x'|/delta^2.

Thus inversion and its inverse are bi-Lipschitz on such intervals. The graph maps have fixed nonzero linear scaling. The image of the interior of J under x->1/x is a nonempty interval, where W has dimension one. Pulling that portion back and translating gives dimension one within the corresponding original line interval. This uses dimension invariance under a bi-Lipschitz map; it does not claim that the inversion is globally bi-Lipschitz or that it preserves a uniform winning constant.

If a countable-cover formulation is desired, the sets [-n,-1/n] and [1/n,n], n>=1, cover every nonzero parameter. Constants may depend on n, which is harmless. More directly, every nonempty relatively open line interval contains a nondegenerate compact subinterval away from the translated rational point. Applying the preceding local argument there proves the claimed full dimension in the original open interval. The ambient line supplies the upper bound one.

When i<j, swapping coordinates and weights changes the slope to 1/a and puts the heavier weight first. The reciprocal coefficient lemma gives the required hypothesis. The coordinate swap is an isometry, so no dimensional loss occurs. This covers all positive weights and either sign of a.

### 4.5 Exact remaining scope

A line has a rational point precisely when b=s-ar for some rational r,s, equivalently b belongs to Q+Qa. Thus Proposition 3 does not handle irrational a with b outside that two-dimensional rational span. A general shear or an arbitrary real translation has not been shown to preserve the weighted bad set. ABV already handles nonzero rational slopes under the endpoint condition; this is credited separately. Neither class solves the general remaining case, and neither finite experimentation nor the projective argument proves an unrestricted inhomogeneous extension.

## 5. Approach 4: near-parallel resonances

With Q=|B| and |A+aB|<=|a|Q/2, the triangle inequality gives |a|Q/2<=|A|<=3|a|Q/2. The proposed constants

h_-=min(1,(|a|/2)^(1/i)), h_+=max(1,(3|a|/2)^(1/i))

therefore give h_-Q^tau<=H(A,B)<=h_+Q^tau, regardless of which weight is smaller. Positivity of h_- uses a!=0.

For a dangerous x with |x|<=X, write alpha=A+aB and beta=C+bB. Integer A,C and either sign of B give

kappa Q^(-tau)<=M(Q)<=max(|alpha|,|beta|)<=(X+1)|alpha|+eta/h.

The choice eta<=kappa h_-/2 makes eta/h<=kappa Q^(-tau)/2. Thus alpha is nonzero and |alpha|>=kappa Q^(-tau)/(2(X+1)). Multiplying by the lower bound for h and using the unrestricted interval length 2eta/(h|alpha|) proves the stated bound. Intersecting with I cannot increase the length.

Under a strict-exponent bound, Q>=1 allows the same small-eta assumption; rearrangement supplies the additional Q^epsilon in |alpha| and hence Q^(-epsilon) in interval length. At the endpoint that decay disappears.

For the constructed a and b=0, convergent forms (-p_n,q_n,0) have h comparable to q_n^tau and |alpha| comparable to q_n^(-tau). Their product stays between positive constants; their unrestricted dangerous intervals have lengths comparable to eta and share center zero. The near-parallel condition holds eventually since ||q_n a||<=1/2 while |a|q_n/2 tends to infinity. This is a legitimate example of lost individual-interval decay. It is not an empty-intersection example: the earlier rational-point proposition applies to this same line.

The unresolved deletion budget is correctly identified. Bounds on each interval and a common-center example do not establish manageable clustering for every possible intercept.

## 6. Approach 5: determinant and the missing Cantor induction

In one height window, h<=H gives |A|<=H^i and |B|<=H^j. With m=max(i,j), H>=1 gives |A+aB|<=(1+|a|)H^m. If the form is small somewhere in the radius-r interval, its center value is at most E=(1+|a|)H^m r+eta R/H.

Replacing the third column C by A x0+B(ax0+b)+C preserves the determinant. Every one of the six permutation terms contains one first-column entry, one second-column entry, and one new third-column entry, so its absolute value is at most H^(i+j)E=HE. The proposed hypotheses make the total at most 1/2. An integer determinant of absolute value at most 1/2 is zero. Every triple is therefore linearly dependent, which gives rank at most two even if the family is regarded as infinite.

For a rank-two span, the cross product of independent integer rows is a nonzero integer vector. Orthogonality says that every associated rational line contains the resulting projective point. A nonzero last coordinate gives ordinary concurrency; a zero last coordinate gives a common direction. Rank-one rows are scalar multiples. The empty family/rank-zero case is harmless.

This exact pencil structure is weaker than the required measure or branching estimate. No bound for the union of dangerous intervals follows merely from rank two. The geometric radius H^(-(1+m)) also need not track 1/(h|alpha|). A positive branching induction, then a dimension estimate tending to one, remains absent. The packet expressly says so. The audit does not convert the determinant lemma into a completed Cantor construction.

## 7. Later-source applicability

Beresnevich–Nesharim–Yang's analytic-curve result assumes that the component functions together with 1 are real-linearly independent. For (x,ax+b) the relation y-ax-b=0 violates that assumption. Datta–Shao's 2024/2025 curve theorem retains the same nondegeneracy requirement. Their stronger inhomogeneous conclusions therefore do not directly remove the line endpoint gap. The reviewer inspected the relevant primary theorem statements and definitions, not every proof. [BNY](https://arxiv.org/pdf/2005.02128), [Datta–Shao curve theorem](https://link.springer.com/article/10.1007/s00208-024-03012-6).

The audit also checked Datta–Shao's later *Winning and nullity of inhomogeneous bad*, available as arXiv:2504.06795. Its ambient hyperplane-winning theorem does not by itself provide a restriction theorem on arbitrary affine lines. Its manifold nullity theorem assumes nondegeneracy and concerns measure rather than the requested critical dimension conclusion. A line-supported measure is not absolutely decaying with respect to ambient hyperplanes, because one such hyperplane contains its support. No resolution of the present endpoint follows from those stated results. This is an applicability check, not an exhaustive current-status claim. [Primary preprint](https://arxiv.org/pdf/2504.06795).

## 8. Verification and reproducibility

The author's run_controls.py was replayed independently and reproduced the recorded 9,485 checks. All valid normal/-O/-OO runs passed, all eleven named negative controls were rejected in each mode, and an actually write-protected source-free relocated copy passed without changing bytes. AUTHOR_REPLAY.json is the resulting receipt.

A separately written independent_check.py imports none of the author's checker. Its 9,638 checks use integer/Fraction arithmetic, rational powers cleared to integer exponents, direct determinant expansion, finite continued-fraction recurrences including t=5/2, rational coefficient identities, heavier-coordinate height bounds, both signs of local inversion, negative slopes, and genuine enumerated unequal-weight dangerous families. Independent integrity checks are anchored to the externally supplied manifest digest rather than merely trusting a replaceable manifest.

run_independent_controls.py runs the independent checker in normal, -O and -OO modes. Its 24 negative controls each reject in all three modes, including zero/negative/nonnormalized weights, wrong weight order, a projective pole, wrong image, wrong rank, rank three, boolean/integer confusion, malformed rational and row data, missing/extra fields, duplicate JSON keys, nonfinite JSON, a false global-solution flag, payload drift, manifest rewrite, and an extra file. Valid replay outputs match exactly across optimization modes. A relocated package containing only the frozen packet and independent checker/probe runs from an unrelated working directory under enforced read-only permissions; a real attempted write fails. It does not read any source PDF. Original frozen hashes match before and after. INDEPENDENT_CONTROLS.json records the results.

These computations check finite identities, stated sample inequalities, metadata, and byte integrity. They do not prove transference, the fiber theorem, the infinite continued-fraction construction, winning-set closure, Hausdorff dimension, or the general endpoint statement. Mathematical acceptance rests on the written arguments and accurately delimited imported theorems.

### Nonblocking tooling qualification

The author's optional --probes input enforces three entries but does not require one occurrence of each probe kind. An external file containing three copies of its valid continued-fraction probe is accepted. The built-in mathematical suite still runs and the default frozen probes are hash-verified, so this does not invalidate the packet or its recorded controls. Do not advertise that interface as a complete strict schema validator. Requiring exactly one of each intended kind would be optional hardening. The independent checker uses a distinct fixed strict schema and explicitly rejects its malformed cases.

The author's manifest checks internal consistency; a manifest rewritten together with all payload hashes is not an external authenticity guarantee. The independent frozen-digest anchor addresses that audit requirement. Neither checker is a general-purpose proof parser.

## 9. Final acceptance boundary

Accepted:

- the positive-weight, nonzero-slope interpretation of the intended target;
- the explicit failure of the wider horizontal statement;
- the exact critical family and endpoint necessity calculation;
- the simultaneous strictly-noncritical-weight corollary;
- the rational-point-line endpoint theorem relative to credited inputs;
- the near-parallel estimate and genuine nonshrinking resonance example;
- the weighted determinant rank lemma;
- the explicit gaps and unsolved disposition after the five recorded approaches;
- the frozen byte identity and the finite control results within their declared scope.

Not accepted as established: the arbitrary irrational-slope/intercept endpoint, an unrestricted projective invariance theorem, a completed Cantor construction, historical novelty, exhaustive openness, human refereeing, or formal machine certification.

No required mathematical patch was found. Optional clarifications about explicit translation constants, local compact intervals, or the strict external-probe schema can be added later without changing the mathematical disposition. The frozen author packet should remain preserved as reviewed.
