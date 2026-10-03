# Independent mathematical audit: 6200043 / AMR-061-0043

Review date: 2026-10-03 UTC.
Reviewed repository: AlecKriebel/Math.
Reviewed branch: math/6200043-loewner-cohopf-recovery.
Pinned commit: 9eca3cd5e2c2ae85bfc933e5f0b58758bef748b7.
Reviewed folder: unsolved_math_prioritization/attempts/6200043.

## Verdict

**Request additive corrections before accepting the complete scoped packet. Original conjecture remains unresolved.**

The substantive arguments in Turns 1–4 are sound within their stated analytic scope, with the mandatory existing Turn 3 denominator correction applied throughout. The finite-automaton graph theorem and the intended geometric argument in Turn 5 are sound, but the written geometric theorem omits a required connection between its point-containing chains and reachable safe automaton states. Its literal statement is not accepted. An explicit source-normalization note is also required: the problem list's displayed Loewner definition contains a reversed inequality and inconsistent function letters. Neither issue supplies a counterexample to the intended conjecture.

Required corrections R1 and R2 are specified in REQUIRED_ADDITIVE_CORRECTIONS.md. They are repairs to the frozen statements and attribution, not a sixth research turn. Preserve all 32 reviewed public files verbatim, add the corrections with fresh bindings, then request explicit re-review. No PR, QUEUE change, remote write, or new author search was performed in this review.

This is an independent scoped mathematical/code audit, not human peer review, novelty certification, or a certification that no subsequent literature resolves the source problem. Recovery count is five; the previous historical count remains unknown.

## Input integrity and replay

I read REVIEW_REQUEST.md, all five proof turns, both existing corrections, all source/provenance summaries, all state/check/manifests, and all four public Python programs. I independently fetched every one of the 32 public files through the GitHub connector at the pinned commit and compared its UTF-8 bytes with the local packet. All 32 were byte-exact. This checks the named commit, not a perpetual claim about the moving branch head.

The main manifest binds 29 other files. It plus BIBLIOGRAPHIC_CORRECTION.md and CORRECTION_MANIFEST.json accounts for the full 32-file packet. The correction manifest's two hashes and all five turn manifests pass. Both local source-binding manifests pass, covering 11 distinct local source artifacts, including all four PDFs.

Frozen replay result: 1,228 Turn 3 assertions, 7,560 Turn 4 assertions, and 52,245 Turn 5 assertions; total 61,033. The automaton checker enumerates 4,181 binary automata and finds 2,917 with uniform escape. The public verifier's hard-coded total matches the independently summed outputs. Its explicitly limited statement that it does not validate raw sources is accurate; this review separately checked their bindings and read the relevant source passages.

The exact inventories, byte lengths, SHA-256 hashes, and GitHub blob identifiers are in REVIEW_MANIFEST.json and REMOTE_VERIFICATION_RESULT.json. No frozen input bytes were edited.

## Controlling problem and normalization

Kapovich's author-hosted Problems on Boundaries of Groups and Kleinian Groups, Problem 43, printed/PDF page 13, attributes the conjecture to Juha Heinonen and asks for quasisymmetric co-Hopficity of Loewner hyperbolic-group boundaries. I inspected the actual page image as well as text. This concerns every quasisymmetric embedding of the boundary into itself, not only group endomorphisms, quasi-isometries already assumed coarsely onto, or maps arising from quasiconvex subgroups.

Source: https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

The author's usual analytic convention is sensible and explicit: an Ahlfors Q-regular, Q-Loewner representative in the boundary's quasisymmetric gauge, Q>1. It does not silently identify analytic and combinatorial Loewner properties or presume that a chosen visual metric is the Loewner metric. The packet correctly leaves any exceptional Q=1 interpretation outside its general analytic deductions and does not promote its partials to the original universal conclusion.

However, printed/PDF page 11, Definition 2, visibly gives an upper-bound sign and refers to phi in the display but psi immediately afterward. Standard analytic Loewner is a positive lower modulus bound. Bonk–Kleiner printed page 227, equation (2.6), directly confirms that standard convention. This must be disclosed as normalization of an apparent typographical error rather than left implicit. It is not an invitation to solve a different upper-bound problem. See R1.

The pinned imported dataset record agrees with the target, but its literature-summary claim about round carpets/buildings is only triage. The packet correctly refuses to infer co-Hopficity from a rigidity theorem for surjective maps. I did not re-fetch the full dataset or repeat an author literature search; selected records and their hashes were inspected. Earlier inaccessible sites and optional PDFs are not silently counted as checked.

## Classical inputs and attribution

Carrasco–Mackay section 8 was independently read in the author PDF and the local extraction. Lemma 8.2 concerns porosity under quasisymmetry with uniformly perfect ambient source. Proposition 8.3 uses attained **Ahlfors regular** conformal dimension and explicitly incorporates an Assouad-dimension/regularization argument. Proposition 8.4 is about limit sets of quasiconvex **subgroups**. Corollary 8.5's proof explicitly permits quasi-isometric subgroup copies. The packet's credits and restrictions agree with these texts.

Source: https://people.maths.bris.ac.uk/~jm13806/pdf/confdimJSJ.pdf (printed pages 43–45).

Bonk–Kleiner's note following Theorem 1.4 on page 222 cites Heinonen's positive-modulus conformal-dimension theorem. Its page 227 states Tyson's modulus theorem for Ahlfors Q-regular, locally compact source and target, with a quasi-Möbius homeomorphism; quasisymmetric maps are included. The existing BIBLIOGRAPHIC_CORRECTION.md correctly changes page 226 to 227.

Source: https://arxiv.org/pdf/math/0208135

Hakobyan section 1.3 distinguishes constructed metric fractals and general hyperbolic spaces from hyperbolic-group boundaries. Its historical open-status discussion is not current-status proof. The packet handles that distinction correctly.

Source: https://arxiv.org/abs/1712.00526

Access limit: David–Semmes Lemma 5.8 and Heinonen Theorems 14.16 and 15.10 remain credited classical dependencies accessed through the checked primary papers; I did not inspect the full books or independently re-prove those general theorems. No claim here depends on the previously inaccessible Kapovich–Benakli or AIM files. Direct web PDF reads succeeded; the web screenshot request for Bonk–Kleiner failed with a cache miss, so I rendered the verified local PDF and visually checked page 227 instead.

## Turn 1: porous-image obstruction

Accepted in the intended scope.

A self-embedding is a quasisymmetric homeomorphism onto its image, so its image has the same Ahlfors regular conformal dimension. If the ambient dimension is attained and positive, its attaining representative is uniformly perfect, and so is the image. The cited porous-subset obstruction therefore applies without assuming the image is already Ahlfors regular in its inherited metric. This is precisely the regularity point that would otherwise invalidate a shortcut proof. In the degenerate attained zero-dimensional compact case, a regular representative is finite, and an injective self-map is already onto.

The auxiliary homeomorphism hypothesis is sufficiently strong: preservation of Y sends a complementary ball to a complementary set, and the asserted inner ball supplies the required hole. A **uniform** small-scale cutoff r0 must be understood; writing it explicitly is recommended. For r>r0, the r0/2 hole sits inside B(y,r), and a reduced constant c r0/(2 diam X) works. Compactness alone does not supply a cutoff if the original quantifiers were interpreted pointwise in y. The unused point z in the statement is harmless and unnecessary.

The cube contraction is a valid countermodel to 'proper QS image implies porous': its image contains ambient-relative open balls. It is not presented as a hyperbolic-group-boundary counterexample. Conjugating the group action by an arbitrary embedding only acts on its image; it does not transport an ambient missing ball. The stated remaining gap is genuine.

## Turn 2: subgroup model and finite coset envelope

Accepted with the quoted classical inputs.

For Theorem A, interpolating the image of a source geodesic produces a uniform quasigeodesic; hyperbolic stability puts target geodesics near the image. Finite Hausdorff distance transfers quasiconvexity to H. A quasiconvex subgroup is undistorted and finitely generated, giving the necessary quasi-isometry and boundary quasisymmetry. The cited infinite-index subgroup obstruction then forces finite index, which makes F(G) coarsely dense. No homomorphism assumption is inserted, and no quasiconvex subset is promoted to a subgroup.

For Theorem B, each non-elementary infinite-index quasiconvex subgroup has a porous limit set. Quasisymmetric boundary action and change of gauge preserve porosity because the boundary is uniformly perfect. In the attained Ahlfors Q-regular representative, each such limit set has Assouad dimension strictly below Q. Elementary limit sets have at most two points and dimension zero; the explicit Q>0 hypothesis handles them.

The finite-union Assouad bound is valid even with an ambient ball center outside a component: recenter at a point in that component's intersection and double the outer radius, then sum finitely many covering estimates. For any exponent larger than all component dimensions, the sum still has that exponent. The use of finiteness is indispensable.

For the limit-set containment, follow a source ray toward a chosen boundary point, take images under F, choose bounded-distance points in the finite coset union, and pass to a subsequence with a fixed coset index. These points escape to infinity and have the same boundary limit. The result lies in that coset's limit set. This establishes containment for every point of the boundary image, not merely a selected dense set.

The image Y is compact, doubling (as a subset of the regular ambient space), and uniformly perfect (by quasisymmetry with the non-elementary boundary). Hence the cited regularization applies to Y: for every exponent above its Assouad dimension it has an Ahlfors regular quasisymmetric model. Taking an infimum contradicts its conformal dimension Q. No attainment of the infimum for Y at its Assouad dimension is asserted or needed.

Neither theorem covers arbitrary images without the additional subgroup/envelope hypothesis. The packet makes that limitation explicit. Ordinary, commensurable, quasi-isometric, and boundary quasisymmetric co-Hopficity remain distinct.

## Turn 3: distortion collapse, attractor, and measure series

Accepted **only with ADDITIVE_T3_NORMALIZATION.md applied to every quantitative denominator**. Let h_n=max{1, eta_n(D/s)}. For clarity, choose U=B(a,s) inside X minus f(X).

The layers f^n(U) are disjoint by cancellation of the injective f^n. Compactness of the proper image supplies such a ball. A farthest point from f^n(a) has distance at least half the image diameter. If b and z_n are distinct, quasisymmetry gives the claimed bound; if b=z_n, h_n>=1 makes the same estimate automatic. Thus for m>n the orbit point f^m(a) lies at distance at least d_n/(2h_n) from f^n(a).

Consequently every set of indices with d_n/(2h_n)>=epsilon yields epsilon-separated orbit points. Total boundedness makes it finite, proving d_n/h_n tends to zero. This is a necessary behavior for the actual distortion bounds, not a quantitative lower bound on how fast an arbitrary sequence must collapse. Inflated distortion bounds weaken the information.

For a common distortion function, h_n is constant, so the image diameters tend to zero. The compact images are nested and nonempty, giving a singleton intersection. Its point is fixed by continuity, and the diameter estimate gives uniform convergence of all iterates to it. Any fixed point must lie in every image, so the attractor is unique. This does not contradict proper contractions.

The packing bound uses relative balls of radius epsilon/3, whose pairwise disjointness follows from their centers' separation. The lower measure bound must hold at those radii, exactly as stated. Summing their measures gives the claimed finite cardinality bound.

For the independent measure estimate, take positive lower-Lipschitz constants lambda_n. The inverse on f^n(X) is lambda_n^(-1)-Lipschitz, so the Hausdorff-measure inequality has the correct direction. Since U is relatively open and f^n(X) is closed, f^n(U) is Borel in X. Countable additivity and disjointness justify the series inequality. The polynomial-divergence threshold alpha Q<=1 is correct. The use of Hausdorff measure avoids unjustified exact scaling for an arbitrary comparable regular measure.

The cube shell example gives equality in the geometric series, and its uniform distortion coexists with a point attractor. No required uniformity or nonsummable lower metric bound follows here from the source hypotheses. Independently normalizing successive images would indeed destroy the nesting used by this argument.

## Turn 4: modulus computation and scope

Accepted for finite real p>=1.

The constant-density upper bound and the vertical-segment lower bound agree. Tonelli handles nonnegative densities and infinite energies. Holder yields the lower estimate for p>1, with p=1 treated directly. Similarity density transport scales energy by s^(n-p); applying the inverse gives equality, including infinite modulus cases. At p=n this is exact invariance for every transported rectifiable curve family.

The proper cube similarity therefore invalidates the proposed inference from perfect critical-modulus preservation to surjectivity. No group-boundary realization is claimed. Curves joining a point or continuum of Y to one in its complement cannot be pulled back through f. For transported curves wholly inside the closed image, restricting an admissible density to the image preserves all line integrals. These observations do not establish ambient surjectivity.

The target regularity warning is correct. Being quasisymmetric to a regular source does not alone prove Ahlfors Q-regularity of the inherited image metric. Tyson's quoted theorem cannot be applied with target X without surjectivity, or with target Y without its needed regularity. The 'conditional closure' paragraph is a research desideratum involving an unspecified lifting/capacity statement, not an additional established theorem.

## Turn 5: finite-state graph lemma and geometric gap

Graph lemma: accepted. From each reachable safe vertex, a shortest escape path has no repeated safe vertex, so its length is at most m (indeed at most the number of reachable safe vertices). An absorbing reject permits padding to a common length N. At most b^N-1 blocks survive from any reachable safe state, and iteration yields the displayed block count. A proper regular language can nevertheless contain an unrestricted recurrent safe component; the first-symbol-0 example demonstrates exactly that obstruction.

Geometric theorem: **literal statement requires repair**. It only says that cells in the point-containing chains have finite states; it does not say those states are reachable and safe or produced by the automaton along the cell labels. The next clause quantifies only over reachable safe states. Hence the proof is not entitled to apply escape at its chosen chain cell. A vacuous-state assignment, with every chain cell declared rejected and no applicable safe cells, illustrates the omitted premise. The actual-ball clause is then never triggered by an escape, although Y may equal X.

The repair must tie labels, transitions, and chains together; R2 gives a sufficient precise formulation. It must retain a geometric certificate for actual metric holes. A rejected address alone does not certify absence of its point under many-to-one coding. The automaton certifies only uniformly bounded escape words and symbolic counts; geometry separately certifies that those words yield ambient holes at every relevant safe prefix.

Once those premises are explicit, the proof is correct. For r<2A choose the least k with A rho^k<=r/2. Then k>=1 and rho^k>rho r/(2A). An escape of length at most N has certified hole radius at least c0 rho^(k+N), strictly exceeding c0 rho^(N+1) r/(2A). Its containing parent cell has diameter <=r/2 and contains y, so the hole lies in B(y,r). Taking a smaller concentric ball establishes the displayed porosity constant. The finite-state structure of a hyperbolic group does not automatically provide a compatible automaton for an arbitrary quasisymmetric self-image.

## Independent controls and stopping point

independent_controls.py uses forward breadth-first searches from every reachable state, independent of the frozen checker's relaxation routine. It exhausts all binary total automata with 1–4 safe states and all ternary total automata with 1–2 safe states: 395,543 automata, 272,016 with uniform escape, and 5,319,784 graph assertions. It explicitly includes the proper-language/non-escaping-state negative control.

Additional exact arithmetic checks: 540 non-dyadic similarity shell identities; 3,645 finite-step Holder controls; 4,320 metric-scale inequalities at scale endpoints and interior values. All pass. These controls corroborate finite ingredients, not the infinite analytic theorem or the source conjecture.

The review stops at the frozen five-turn research scope. The intended partial results survive, but acceptance of the entire packet awaits R1/R2 addenda and explicit re-review against newly bound bytes. No result here resolves Heinonen's universal conjecture, claims novelty, authorizes a PR, or changes its unresolved disposition.
