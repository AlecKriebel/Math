# Independent mathematical and reproducibility audit

8 October 2026. Disposition: accept the corrected derivative as scoped partial progress. The full two-loop comparison remains unresolved by this work; no novelty or prior-resolution claim is accepted. The five existing approaches are retained, with no sixth approach.

## Material reviewed and preservation

The entire original REPORT.md, SELF_REVIEW.md, both executable scripts, validation output, and source/package manifests were inspected. The starting report has SHA-256 8f5597c5bca6eec55a6f406fe5ed7218d56b45bfc8e9f14ed487988a130d6ffc (21,554 bytes). Original inputs are preserved byte-for-byte. Corrections are made only in a derivative packet.

Primary-source inspection included the OWR question; Luo–Maibach §1.2 and Theorem 2.1; Ang–Cai–Sun–Wu Theorem 1.1; Kemppainen–Werner §§3.1–3.4; Ang–Remy–Sun Theorems 1.7 and 1.9, Corollary 1.10 and the endpoint-continuity passage in §5.1; Glazman–Harel–Zelesko §1.2; and Benoist–Hongler Theorems 1 and 6 plus §2.1. The supplied six PDFs' hashes, sizes, and PDF signatures were recomputed. This is an independent inspection of those supplied primary-source bytes, not a claim that all six were independently downloaded again. Current public version/status pages were also checked. ARS printed pages 7 and 8 were inspected visually, including the formula and inconsistent χ line. No copied source bodies are included in the deliverable.

## Findings and corrections

### C1. Probability Palm disintegration needs an intensity hypothesis

The original generic setup assumed only almost-sure local finiteness. That does not guarantee that the intensity ν is σ-finite, and therefore does not justify the stated probability Palm disintegration by itself. The derivative explicitly assumes standard Borel loop/configuration spaces and σ-finite ν; finite expected counts on a countable exhaustion of windows suffice.

This is a genuine omitted hypothesis, although it does not invalidate the intended CLE application with its established σ-finite intensity. For a counterexample to the general inference, take a finite random N with P(N=n)=1/[n(n+1)], n≥1, and N independently sampled continuous uniform radii in [1,2]. The resulting concentric circles are distinct and locally finite almost surely. Their intensity is infinite on every radius set of positive Lebesgue measure and zero on every null set, so it is not σ-finite. No countable family of finite-intensity sets can cover that radius interval. Under the repaired hypothesis, disintegrating the Campbell measure over ν gives a probability kernel, and Tonelli proves the reduced-Palm formula.

### C2. Validation coverage wording

The original executable enumerates configurations of five selected subcubic graphs, not all finite subcubic graphs. The derivative says exactly this and calls its 1,482 counted cases single/pair identity checks. The original computations are retained unchanged.

### C3. Explicit source-specific scope

The derivative states the ARS modulus convention A_τ={e^(−2πτ)<|z|<1} and the theorem's range λ>3κ/32+2/κ−1. The report's λ>0 is safely within that range throughout 8/3<κ≤4. It also replaces a time-dependent “current version” label with “inspected v3.”

The Ising statement is now explicitly the square-grid discretization result for simply connected Jordan domains with + boundary conditions and the specified loop-collection metric. It is not a transfer theorem to arbitrary lattices, arbitrary boundary conditions, general O(n), or the finite graph model of Approach 1.

### C4. Conditional law and counterexample precision

The derivative specifies a common measurable finite-positive-mass restriction for both measures, a measurable modulus map, and a nonnegative measurable density f. These are the hypotheses used by Proposition 5.

The rare-event example already disproves pair-intensity convergence without moment control. The derivative adds that Σ_m m^(−2)<∞ makes the configurations eventually empty almost surely on any common probability space. Thus it satisfies the actual finite-matching hypothesis, and uniform integrability is the missing condition, rather than a mismatch between almost-sure and in-probability assumptions.

No main displayed formula required an algebraic or normalization correction.

## Result-by-result review

### Finite loop model: Propositions 1–2

Accepted for a finite simple graph with free boundary, unoriented simple cycles, vertex-disjoint configurations, n>0 and x>0. Occupying a specified cycle removes all its vertices and their incident edges. This gives the exact marked partition sums. Deleting only occupied edges would allow incompatible cycles touching a marked vertex and is incorrect. For two distinct compatible marked cycles, the pair weight has n² and no factor 1/2: it is the mass at a fixed ordered pair. Intersecting distinct cycles have mass zero.

The ratio is Z_G Z_(G−Vγ−Vη)/(Z_(G−Vγ) Z_(G−Vη)). The linear coefficient of its logarithm at n=0 is the sum of x^|α| over cycles meeting both marked vertex sets. Inclusion–exclusion establishes the sign and multiplicity. The remainder is graph-dependent. The finite model does not supply critical-mesh estimates, boundary renormalizations, convergence to CLE, or a Brownian-loop interaction formula. The n=0 endpoint is explicitly outside the positive-fugacity probability division.

### Campbell/Palm and nested descendants: Proposition 3

Accepted after C1. The factorial measure is the off-diagonal part of E[C⊗C]. It is neither ν⊗ν nor a samplewise normalized probability on available pairs. The diagonal identity is an identity of measures/test integrals, not ∞−∞ arithmetic.

Kemppainen–Werner's nested Markov construction supplies the adjacent origin-surrounding transition Q and adjacent intensity ν_0(dγ)Q(γ,dη). Summing generation gaps gives ν_0(dγ)Σ_(j≥1)Q^j(γ,dη) by nonnegative Tonelli. The sector fixes both the marked origin and outer-to-inner ordering; this is not all sphere pairs. The cascade in this sector is ν_0(dγ)ν^0_(Dγ)(dη) in the same one-loop normalization. Equality up to constant is precisely equality of these kernels ν_0-almost everywhere. The sphere one-loop intensity theorem does not identify the disk successor resolvent.

### Geometry and disintegration: Propositions 4–5

Accepted with C4's explicit hypotheses. The inequality |ε(z+w)|≤2ε<1 proves injectivity of z+εz² on the closed unit disk. It therefore preserves the annular conformal type. Its outer boundary cannot be a circle: a disk-to-disk conformal bijection is Möbius after affine normalization, whereas the specified quadratic polynomial is not. Möbius maps preserve generalized circles, so the ambient pairs are inequivalent. The measurable circle-pair indicator is a counterexample on analytic pairs; no claim about nontriviality on SLE-typical pairs follows.

For normalized finite restrictions, ν=f(T)μ is equivalent to the stated modulus marginal density and equality of conditional embedded-pair laws on the ν-modulus law. Equality of modulus marginals alone is inadequate. The determinant-line discussion is correctly conditional on identifying the actual model trivializations; it is not an independent identification theorem.

### Imported ARS formula and deductions (7)–(9)

Accepted with the stated conventions. Set a=4/κ−1, C=cos(πa), and s²=a²−8λ/κ. Direct transcription of Theorem 1.7 is H_κ(λ)r_κ(λ)^j, with H=a sin(κπs/4)/[s sin(π(1−κ/4))] and r=C/cos(πs). Theorem 1.7 is a Laplace transform of annulus modulus, with 2πλ in the exponential; it is not just a conformal-radius transform.

For positive λ, either 0≤s<a<1/2 or s is positive imaginary. Thus 0<r<1. The removable s=0 value uses sin(κπs/4)/s→κπ/4. The z-weighted descendant sum is Hr/(1−zr), where z=0 selects the first successor and z=1 counts all descendants. Replacing it by the adjacent term or including Q^0 is wrong.

At κ=4, a/sin(π(1−κ/4))→1/π, s→i√(2λ), and u=π√(2λ). This gives sinh(u)/(u cosh(u)^j) and sinh(u)/[u(cosh(u)−1)]. ARS explicitly justifies the κ→4 extension using continuity in §5.1. Individual transforms tend to 1 as λ↓0; the summed descendant transform diverges. The bound 1_(τ≤T)≤exp(2πλT)exp(−2πλτ), conformal transport from the disk, and the finite outer ν_0 window yield the claimed finite pair mass.

The printed Corollary 1.10 line χ=(1−κ/4)π conflicts with (1.9), where χ=(1−4/κ)π. At κ=3 these give √2 and 1 for n. The derivative correctly retains (1.9) and uses Theorem 1.7 directly; no correction to the report's numerical formulas follows from the source typo. Neither annulus-modulus data nor these transforms identify the full embedded-pair law or its RN density.

### Pair-intensity convergence: Proposition 6

Accepted. A finite matching with convergent loop locations makes every bounded continuous test sum converge almost surely. The bound by ||f||∞N_m(N_m−1) and uniform integrability permit expectation convergence. The stronger (2+ε)-moment bound implies the required uniform integrability by a power bound. Cutoff-boundary continuity and the matching itself remain model-specific hypotheses.

For the rare-event example, E N_m=1/m, while E[N_m(N_m−1)]=1−1/m. The expected tail stays bounded away from zero for thresholds below m(m−1), so uniform integrability fails. The circles are simple, distinct, and mutually disjoint; this failure is not caused by multiplicities. The added Borel–Cantelli observation makes the example satisfy almost-sure eventual finite matching to the empty process.

## Literature and normalization boundaries

Luo–Maibach Theorem 2.1 supplies the reference two-loop cascade for 0<κ≤4; §1.2 explicitly distinguishes the alternative CLE construction. Oxford's publisher record confirms acceptance 2 May 2025 and publication 23 May 2025, IMRN 2025(11), rnaf133. The author's accepted-version PDF is internally dated 22 April 2025 despite its filename. This published cascade construction is prior work, not a resolution of its own alternative-measure comparison.

Ang–Cai–Sun–Wu Theorem 1.1 identifies the full-plane CLE one-loop intensity with a positive multiple of Zhan's one-loop measure for 8/3<κ<8. Within the simple regime the report absorbs that constant consistently into ν and its domain restrictions. It does not infer a second factorial moment or conditional independence from a first intensity.

The inspected GHZ v3 concerns percolation/loop-model results including macroscopic-loop behavior and distinguishes these from full CLE convergence. Benoist–Hongler supplies a genuine full nested Ising ensemble limit in its own specific setup, not the missing general model theorem. The wider comparison remains unproved here even in that special setting.

Primary references and version identifiers are in SOURCES.json and SOURCE_AUDIT.json. This was a bounded inspection, not an exhaustive search for every later resolution.

## Reproducibility and acceptance standard

The independent audit uses two combinatorially different finite-model constructions: DFS enumeration of cycles with a least-vertex partition recurrence, checked against direct degree-0/2 edge-subset configurations. It covers 82 labeled/selected graph inputs, including all labeled simple graphs with at most four vertices, K5, K6, two linked triangles, a bowtie, the cube, and three bridged triangles. Isolated vertices do not alter the partition function. The exact checks also cover a finite Campbell/Palm law, a substochastic matrix resolvent, conditional embedded-shape counterexamples, symbolic parameter/endpoint identities, and rare-event moments. The geometric four-point determinant gives a second exact check that the quadratic image boundary is not a circle.

High-precision checks at 70 decimal digits are separately identified as numerical diagnostics. They compare independent transcriptions of the imported formula across real, removable, and imaginary s, use an explicit geometric-series tail, and check the κ=4 limit. They are not substitutes for the analytic proof or an independent proof of ARS.

Nineteen mathematical mutations cover vertex-vs-edge deletion, missing fugacity, pair ordering, ratio inversion, low-fugacity sign, independent realizations, diagonal inclusion, random normalization, biased-vs-unbiased Palm laws, adjacent-only and shifted resolvents, modulus-only inference, the dilute parameter, the κ=4 constant, the Laplace scale, ARS generation and sine factor, and the missing pair-moment assumption. Acceptance requires their semantic rejection in normal, -O, and -OO modes, in addition to the original explicit failure controls. Test logs record actual nonroot UID, a denied directory-write probe, and before/after file hashes. A forced exception alone is not counted as a mathematical mutation.

Accepted content remains Propositions 1–6 with the repairs above and credited elementary deductions from ARS. The complete embedded-pair comparison, general lattice convergence, worldwide novelty, and an exhaustive prior-resolution claim are not accepted.
