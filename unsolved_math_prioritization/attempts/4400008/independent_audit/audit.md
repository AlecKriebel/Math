# Independent adversarial audit: Boyle's Pingree problem 2

## Verdict

PASS, with the status **unsolved, five of five documented approaches**. The frozen packet establishes the reductions and failed-method controls it claims. It establishes neither the desired theorem nor a counterexample. No material mathematical defect requiring correction was found. This verdict does not certify novelty, exhaust the literature, establish present global openness, or turn numerical controls into proofs.

Target identifiers: UnsolvedMath 4400008, AMR-043-0008, selection rank 701. The audited input consists of eight files, 56,661 bytes, with manifest SHA-256 `0d9b8a4ad752b292c4d59b262b08090478df48a303959c2de41d612387f045b6`. The original files were preserved. `binding.json` records every input hash and the exact-output rerun. The separate audit has its own manifest.

## Statement and source binding

The primary target is Mike Boyle's item 2 on page 4 of the November 22, 2010 Pingree list. It concerns a subshift orbit equivalent to a mixing SFT and asks whether that subshift is itself a mixing SFT. The adjacent remarks distinguish nonexpansive targets and mixing-sofic sources. Page 3 concerns classification of mixing SFTs, a neighboring question rather than an additional hypothesis. [Original problem list](https://math.huji.ac.il/~mhochman/open-problems/pingree-open-problems.pdf).

Boyle's survey supplies the two-sided, finite-alphabet, one-dimensional conventions in section 2 and the onto-orbit homeomorphism definition in section 23. Problem 23.4(5) is the corresponding finite-type question for an irreducible source. These conventions do not impose continuous cocycles. [Survey](https://terpconnect.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf).

The exact catalog page again failed web retrieval and a direct request returned HTTP 403. Its full research notes remain uninspected. An indexed category listing corroborates the AMR label and target. The available selection catalog was independently hashed and its identifier/title/source/rank agreement checked; it is not the original AI-result corpus. No raw-corpus inspection or raw-record identity match is claimed. No source page's current “open” label is treated as a proof of global openness.

All six substantive PDFs were freshly retrieved with HTTP 200 and matched the authored byte counts and hashes. Text and relevant rendered pages were inspected. Full metadata and exact inspection scopes are in `sources.json`; no PDFs, source extracts, page images, raw catalog records, or private coordination material are included in this audit.

## Conventions checked

An orbit equivalence is a homeomorphism h from X onto Y with h(Orb_S(x)) = Orb_T(h(x)). Equality onto the entire integer orbit matters. The source and target maps are homeomorphisms. The target is not presumed finite type, sofic, mixing, or conjugate to the source. The jump is unique at aperiodic points and generally nonunique at periodic ones.

The finite-source case is correctly separated: a finite mixing permutation has one point, and any homeomorphic target also has one point. In the infinite case a mixing SFT has dense periodic points, dense aperiodic points, and a dense forward orbit. A finite strongly connected graph supplies periodic completions. Genuine branching supplies two distinct equal-length return loops and uncountably many continuations in every cylinder, whereas the periodic points are countable. This justifies the aperiodic-density uses below.

The preliminary claim that a subshift conjugate to an SFT is itself SFT is valid. Both conjugacy directions have finite coordinate radii. A finite window can check the source constraints and the composition identity; applying these checks at every coordinate characterizes the image. Thus an abstract finite graph coding is enough to establish finite type of the actual target subshift.

## Detailed audit of every retained lemma

### 1. Periods and forward transitivity

PASS. The restriction of h to each orbit is a bijection onto a complete orbit. Finite orbit cardinality is exactly least period, so least periods and all fixed-point counts are preserved. Density of each of the periodic and aperiodic sets transfers by the homeomorphism. A dense full orbit also transfers.

The conversion from full-orbit density to forward transitivity uses periodic density and is valid. Given nonempty open U,V, full-orbit density supplies some integer k with T^k(U) meeting V. If k = -l is negative, U intersect T^l(V) is nonempty. A periodic point p in this intersection and a period multiple q > l give T^(q-l)p in V, at positive time. There is no accidental replacement of a dense full orbit by a dense forward orbit without this extra argument.

A useful adversarial control is the compact subshift consisting of zero and configurations with exactly one 1. Its singleton-marker orbit is dense as a full orbit. Nevertheless the cylinder with a marker at 0 cannot reach the cylinder with a marker at +1 in nonnegative time under the left shift. Its periodic points are not dense. This shows why the packet's periodic-density step is necessary.

### 2. Finite type forces mixing under the standing hypotheses

PASS. Forward transitivity gives an irreducible graph presentation once finite type is assumed. Its period d divides every length n for which a closed n-path exists. A mixing source has an n-periodic point for every sufficiently large n; these points need not have least period exactly n, and the argument correctly needs only nonempty Fix(S^n). Preserved fixed-point counts therefore force d to divide all sufficiently large integers and hence d = 1.

The final graph argument is sound. At a fixed vertex, return lengths have gcd d. A finite subset has gcd 1 when d = 1. Their nonnegative semigroup contains all large integers: fix one generator a, obtain a nonnegative representative of every residue modulo a by adjusting coefficients, and then add copies of a. Prefix and suffix paths through that vertex produce all sufficiently large connecting lengths. This is mixing on cylinders. Irreducibility alone would fail, as the period-two cycle demonstrates.

No target graph is available before finite type is proved. Consequently this is a reduction, not the original theorem.

### 3. Entropy and periodic measures

PASS. An n-periodic target point is determined by its n-block, giving p_n(T) <= |L_n(Y)|. Equality of the source and target p_n, together with Perron–Frobenius asymptotics for the primitive source presentation, yields h_top(T) >= h_top(S). Eventual positivity makes the logarithms legitimate. Formal zeta equality follows coefficientwise and does not require analytic convergence.

Uniform probabilities on the finite fixed-point sets are transported exactly. Weak convergence transfers through a continuous h. This supplies no proof that the image limit maximizes target entropy. The packet correctly does not claim entropy equality or a target Markov presentation from these facts.

External standard ingredients here are primitive-matrix Perron–Frobenius asymptotics and the finite-alphabet language formula for entropy. They were used as standard facts, not independently reproved by the finite controls.

### 4. Invariant probability correspondence

PASS. For R = h^(-1)Th, each equality set {R(x) = S^k(x)} is closed. Choosing the first valid integer from an enumeration gives a countable Borel partition. For any Borel E, the images R(E intersect D_k) are disjoint because R is injective. S-invariance then gives mu(R(E)) = sum_k mu(E intersect D_k) = mu(E). Images are Borel because the maps are homeomorphisms. Applying the same construction with the two orbit relations reversed gives surjectivity of the measure correspondence. Pushforward and its inverse are affine.

This argument requires neither continuous nor bounded jumps. It also does not show preservation of entropy of individual measures.

### 5. Baire regularity and conditional rigidity

PASS. Countably many closed equality sets cover the compact metric source. Every nonempty open subspace is Baire, so one equality set contains an open part of any prescribed open set. The union of their interiors is dense and open, with a locally constant valid jump near each of its points. It need not be all of X. Compactness cannot extract a finite subcover from an incomplete cover.

The actual rigidity dependency is correctly stated: Boyle–Tomiyama Theorem 3.2 requires topologically free same-orbit homeomorphisms, a continuous integer jump, and transitivity of one map. Theorem 2.3 with bounded jump N instead removes a closed nowhere-dense set of periodic points of period at most 2N; Corollary 2.7 gives flip conjugacy on its complement in the transitive case. [Published source](https://www.jstage.jst.go.jp/article/jmath1948/50/2/50_2_317/_pdf).

In this application S and R are topologically free by aperiodic density, share complete orbits, and are transitive. A continuous integer function on the compact source is bounded, and the continuous theorem applies globally. The exceptional set for a merely bounded jump is finite for a finite-alphabet subshift, since there are only finitely many points of bounded period. Finiteness does not prove extension of the conjugacy or its inverse across that set. No such extension, nor any stronger bounded-cocycle classification theorem, is asserted here.

### 6. The explicit unbounded-jump orbit homeomorphism

PASS, including at every exceptional and periodic point. The cylinder U_n has its nearest nonzero coordinate at +n and the partner V_n at -n. Their prescribed intervals force all smaller absolute coordinates to vanish, and the sign separates the two cylinders with the same n. Thus every named cylinder is disjoint from all the others. Shifting U_n by 2n gives exactly V_n, including the asymmetric endpoints [-5n,n]. The opposite branch is the inverse. Outside the cylinders the map is the identity, so h squared is the identity globally.

All images lie in their original S-orbits. This plus global bijectivity gives onto-orbit equality: if h(z) is in the orbit of x, then z is in that same orbit. Inclusion has not been substituted for equality.

For continuity away from o = 0^Z, choose a nonzero coordinate k of the point and fix it in a neighborhood. Every cylinder with n > |k| misses that neighborhood. Only finitely many clopen branches remain there, each a continuous shift or identity. At o, the central-zero cylinder of radius r maps into itself: any exchanged point in it has n > r, and its partner also vanishes on that radius. This proves continuity precisely at the sole accumulation point of unbounded branch indices. The inverse equals h and is continuous for the same reason. Periodic points other than o are covered by the finite-branch argument.

The witness with support {n+1,3n+2} is outside all exchanged cylinders, whereas its left shift has support {n,3n+1} and lies in U_n. Therefore h(Sx) = S^(2n+1)h(x). Finite nonempty support proves aperiodicity, so the exponent is unique and grows without bound. Both endpoints in this calculation matter: 3n+1 lies just beyond the U_n zero interval, while 3n+2 lies inside the U_(n+1) interval. Independent endpoint controls verify these distinctions.

To connect this directly to the pulled-back-map argument, h is an involution and R = hSh. If y = h(x), then R(y) = S^(a(x))y where a is the displayed orbit jump. In particular the chosen witnesses satisfy h(x) = x. Thus this really obstructs uniform control of the pulled-back map, not merely an unrelated function.

Both underlying shifts remain the binary full shift. This disproves the proposed automatic-cocycle upgrade, not finite-type preservation and not the possible existence of another better orbit equivalence.

### 7. Shadowing, finite type, and stabilization

PASS. In the shadowing-to-finite-type direction, choose m with 2^(-m) < delta. The local witnesses for a configuration in Y_m agree sufficiently on overlaps to make a two-sided delta-pseudo-orbit. Accuracy below 1/2 forces their central symbols, hence every coordinate of the tracing point, to equal the prescribed configuration. Thus Y_m is contained in Y; the reverse containment is automatic.

Conversely, a sufficiently accurate pseudo-orbit gives exact coordinate identities throughout a window wider than both the finite-type memory and the desired tracing radius. Defining z_i = x^i_0 propagates those identities in both positive and negative directions. All defining finite-type blocks of z occur in genuine points of Y, so z belongs to Y and traces every time. The strict inequalities and one-coordinate margins are sufficient; there is no boundary off-by-one error.

A sufficiently large odd window detects any finite forbidden list. This proves all three equivalences, not just one implication. These are two-sided shadowing statements for the shift homeomorphism, without importing a one-sided convention.

### 8. Even-shift nonstabilization

PASS. For each m >= 1, the periodic sequence with one 1 followed by 2m+1 zeros violates the even-gap rule. Every window of length 2m+1 contains at most one 1, so it extends to an allowed whole configuration with at most one 1. Hence it belongs to E_m but not E. The witness can be chosen for every m, showing genuine nonstabilization. The independent verifier additionally checks the words with the two-state even-shift automaton.

This does not furnish an orbit equivalence between the even shift and a mixing SFT. Nor does the example contest that the intersection of all canonical approximations equals the subshift. It blocks finite-stage stabilization based solely on arbitrary finite tests.

### 9. Positive same-orbit speedups

PASS. On an infinite S-orbit, identify points with Z. The induced R-permutation p has p(k) > k everywhere. Complete orbit equality forces the double-infinite sequence p^i(0) to enumerate every integer once. It is strictly increasing in i in both directions. A jump of two or more would permanently skip an integer, so each jump equals one. Thus p(k) = k+1 on the entire orbit.

Equality on all aperiodic orbits extends to the whole space by density and continuity of R and S. The negative case applies the same argument to S^(-1). The proof does not need regularity of the jump. Finite cycles permit coprime positive steps, but they do not invalidate the dense-aperiodic extension. S squared is bijective yet splits each infinite S-orbit into parity classes, failing the essential same-complete-orbit condition.

### 10. Return maps and integer roofs

PASS. If finitely many iterates of a clopen section cover the space, applying that cover to a sufficiently far future iterate gives a uniform positive return bound. Each first-return-time level is clopen. A sufficiently high block presentation is one-step and detects section membership at the current symbol. Positive-length first-return paths between marked symbols, with no interior marked symbol, form a finite alphabet. Matching endpoints is the only adjacency condition. Concatenation gives a unique original bi-infinite configuration with a return at time zero, proving both injectivity and surjectivity of the coding. The itinerary map is continuous; compactness supplies the continuous inverse.

For an integer roof, compactness and continuity give finite range and finite coordinate dependence. Recoding makes the roof depend on the current symbol. Splitting each symbol into its finite ordered levels produces a finite directed graph. The current level and base path are recovered uniquely, so this is a conjugacy, not just a factor map.

“Return path” necessarily means positive length, as it is a first positive return. Spelling out this convention would be harmless editorial clarification; it does not change the construction or require correction of the packet.

### 11. Flow equivalence as an equivalent closing goal

PASS, conditional on the named external theorems. Boyle–Handelman section 1.4 records the Parry–Sullivan common-section theorem: two section return maps are discrete suspensions over a common return map. Theorem 1.12 assumes both systems are irreducible SFTs and states that orbit equivalence implies flow equivalence. Section 1.10 also explicitly notes finite-type preservation under flow equivalence. [Source](https://terpconnect.umd.edu/~mboyle/papers/bhoemaster.pdf).

For the forward reduction, the common base is a clopen discrete section in the SFT suspension model. Lemma 10(a) makes the base finite type; Lemma 10(b) makes the other discrete suspension finite type. Conjugacy invariance then applies to the actual target. For the converse, target finite type first invokes Lemmas 1–2 to satisfy the second irreducible-SFT hypothesis. Only then is Theorem 1.12 applied. There is no circular proof of the original conclusion.

The symbol expansion control is correct. Coding 1 by 1a produces transitions 0 to 0 or 1, 1 to a, and a to 0 or 1. This is an integer-roof tower over the binary full shift; rescaling the roof intervals gives an orientation-preserving flow equivalence. Only the all-zero point is fixed, unlike the two fixed points of the binary full shift. Therefore it cannot satisfy the original orbit equivalence. Finite cyclic-word counts independently reproduce this discrepancy.

## Nearby results and exclusions

Salo's Theorem 1 concerns a conjugacy between the free parts of two infinite transitive SFTs. Theorem 3 replaces finite type by explicit synchronization and one-sided-projection density hypotheses on both ambient subshifts, still starting with a conjugacy. It resolves the neighboring Hochman problem, not this unrestricted orbit-map question. [Salo](https://villesalo.com/article/CoTSmPP.pdf).

Matsumoto's Proposition 6.5 assumes normal subshifts and continuous orbit equivalence of their associated one-sided systems, with that term defined through the preceding presentation framework. No application to the present unrestricted two-sided relation follows. [Matsumoto](https://ems.press/content/serial-article-files/28864).

No source's theorem has been strengthened by dropping its continuity, finite-type, synchronization, normality, direction, or orbit-surjectivity hypothesis.

## Five approaches and their remaining obligations

1. Periodic/measure rigidity recovers invariants and conditional mixing. It supplies no finite bound on target forbidden-word length and no target entropy-maximizing theorem.
2. Cocycle rigidity proves a conditional solution and defeats automatic regularity of an arbitrary orbit map. It leaves the construction or control of a better map unproved.
3. Shadowing proves an exact reformulation. Variable, reversed, or unbounded source excursions prevent the asserted ordinary-pseudo-orbit transfer.
4. Positive speeds rule out a specific counterexample mechanism. A nonmonotone construction would still need continuity, inverse continuity, expansivity, and non-finite type.
5. Flow reconstruction proves another exact reformulation. The one-SFT extension of the orbit-to-flow result is not established.

These are substantively distinct approaches, not five versions of the same numerical test. The recorded five-of-five budget is supported as five documented approaches. Historical interaction/turn count was not independently audited. None of the approaches supplies a complete resolution, and none is called a new theorem resolving the target.

## Verification, dependencies, and boundaries

The author's script was inspected, executed once for exact-output comparison, and independently checked against the frozen manifest. It reproduces 9,198 assertions and exactly the saved 2,026-byte JSON result. That execution is evidence about the controls, not mathematical peer review.

The separate independent script imports no authored implementation. It checks 165,565 exact assertions, including all 32,766 binary periodic words of lengths 1 through 14, involutivity, orbit membership, least-period preservation, 21,837 central-zero-neighborhood checks, 2,056 endpoint checks, aperiodic witness parameters through 257, 9,504 even-shift windows, and cyclic-word counts for the symbol expansion. `negative_controls.py` additionally demonstrates that deliberately faulty inverse and boundary variants are rejected. These finite computations support, but do not replace, the infinite arguments above.

The external mathematical dependencies remain explicit: basic finite-graph SFT facts, Baire category, Perron–Frobenius and the entropy language formula, Boyle–Tomiyama's continuous/bounded-cocycle theorems, and Parry–Sullivan/Boyle–Handelman for the flow reduction. This audit checked relevant hypotheses and applications; it did not formally verify the entirety of those external papers.

Original source-file retrieval history beyond the six substantive PDFs, the author's bounded repository-history searches, and the absence of unavailable raw AI corpora were not upgraded into new exhaustive claims. The thesis scans remain irrelevant to this verdict and uninspected here. Public material is limited to authored analysis, reproducible controls, hashes, byte counts, public bibliographic references, inspection scopes, and qualified status.

No helpers, remote writes, source redistribution, or modification of the frozen packet occurred. The appropriate disposition is to retain the packet as an audited **unsolved 5/5** investigation.
