# Independent adversarial audit: 10000069 / AMR-099-0069

Date: 2026-10-05. Assigned rank: 711.

## Verdict

The credited interior spectral theorem survives this independent audit. Accept it as an exact implicit characterization of the hierarchical terminal-distance **expectation** exponent for each fixed p in (1/2,1), subject to the local erratum below and the original source/interpretation limitations. No fatal analytical gap was found. This is a mathematical review, not formal verification, human peer review, or a novelty certificate.

One incorrect equality occurs in the authored reconstruction, not in the corresponding external argument. At PROOF_RECONSTRUCTION.md line 90, replace E(X-Y)^2 = 2(R-1) by

E(X-Y)^2 = 2(EX^2-1) <= 2(R-1).

Here R is an upper bound on EX^2. The intended inequality and ensuing asymptotic follow from the corrected relation; neither requires equality with the cap. Originals remain unchanged and exactly bound by EXACT_BINDING.json. ERRATA_AND_SCOPE.md records the correction separately.

Disposition: **qualified credited prior characterization, with an attached erratum**. Do not promote this to an unqualified solution of the informal request for the whole “shape” of delta. In particular, an implicit infinite-dimensional eigenvalue formula is not an elementary scalar formula or a proved global curvature description. The audit does not settle that interpretive choice. Campaign work remains one substantive source-verification/reconstruction route, 1/5; this audit is not a second discovery attempt and does not establish five-route exhaustion.

## 1. Materials and independence

The nine frozen payload files and their manifest were all checked byte-for-byte. The input MANIFEST.sha256 is 792 bytes and hashes to 65297b9b4168ebd859dace3416a1bb01c559ad6ebd90235d52e9e82a6420f50d. The independent audit did not alter them.

The complete authored reconstruction, complete external canonical proof (556 lines), manuscript TeX, and all four manuscript PDF pages were inspected. The immutable candidate source is DannyExperiments/random-series-parallel-distance-exponent at a875da08e8bfbdb70fd8165c097ab036731b5f6f. Fresh HTTP retrievals of the canonical proof, TeX, and PDF matched the previously reported hashes and sizes exactly. The repository's current main commit was also this commit at inspection. Public attribution is to DannyExperiments; no identification with the user is inferred. Self-audit badges and source claims of resolution were not used as proof.

The author's finite program was replayed independently and produced byte-identical JSON with 2,158 assertions. Separately authored controls use literal graph replacement plus breadth-first search, symbolic gate counts, tail-probability laws, and exact quantile-step integration. They passed 156,596 assertions. These computations test identities and detect implementation errors; they cannot prove infinite-dimensional compactness or an asymptotic theorem.

Earlier-user-attempt searches described in the frozen history report were not repeated as part of this analytical audit. That report remains bounded historical evidence, not an absence proof. Neither current catalogue text nor a raw corpus statement was obtained.

## 2. Exact object, normalization, and recursion

The model is an edge-replacement hierarchical multigraph. Every edge is separately replaced by two unit edges, in series with probability p and in parallel otherwise. Thus the edge count after n replacements is exactly 2^n. The distinguished terminals are those of the initial edge. Removing parallel multiplicities before later replacement would change the model.

Condition on the first gate. Its two descendant networks use disjoint independent gate families. At a series gate a terminal path must cross both descendants, so terminal distances add. At a parallel gate the shorter descendant path can be chosen, so distances take the minimum. This proves the distributional sum/min recursion with independent copies and D_0=1.

The exponent is lim_n log(E D_n)/n, using natural logarithms. When expressed as a power of the deterministic number of edges, it is delta/log 2. The parameter p is the probability of the series operation, including in the published near-critical theorem. It is not q=1-p, and epsilon=p-1/2 is not 2p-1.

The independent graph control constructs every multigraph gate assignment through depth four, computes terminal distance by BFS, and compares its joint counts with the independently convolved distance/series-gate counts. Agreement of these integer counts verifies finite-depth laws for every p, not only the tested rational p values. It does not change the universal proof requirement.

## 3. Operator and Jensen domination

For each nonnegative integrable decreasing profile f, independent uniform evaluations produce an integrable output: both the sum and the minimum are bounded above by f(U)+f(V). Decreasing quantiles are well-defined modulo null sets. Using a common U,V and gate establishes order preservation and positive homogeneity. The sum and minimum are each Lipschitz with respect to the sum of coordinatewise absolute differences. Consequently their coupled output difference has expectation at most 2||f-g||_1; the one-dimensional optimal quantile coupling then gives the stated L1 bound for T. This continuity does not need an L2 hypothesis.

For each finite fixed gate tree, its leaf evaluation is concave, monotone, nonnegative, and homogeneous. The minimum of concave functions is concave: its hypograph is the intersection of their convex hypographs. Alternatively, for nonnegative leaf lengths, the evaluation is the minimum of the finitely many linear path lengths. Both descriptions justify the direction of Jensen. Independence of the leaves is needed to identify the T iterate, but Jensen itself only needs their mean vector and integrability. The output is at most the sum of leaf lengths, so Jensen applies even for unbounded L1 inputs.

Therefore M(T^n f)<=m_n for every mean-one admissible profile. Applying this to T^k1/m_k gives m_(n+k)<=m_n m_k. All m_k are positive. Fekete applies to log m_n; the bounds 1<=D_n<=2^n keep the rate finite. The one-step mean bounds imply 2p<=rho<=1+p in the interior. This part of the argument does not presuppose an eigenprofile or convergence of normalized laws.

## 4. The moment inequality and the compact set

For decreasing f, min(f(U),f(V))=f(max(U,V)), and max(U,V) has density 2u. This verifies the definitions A=2 integral u f and C=2 integral u f^2. Expanding the series operation yields S(Tf)=2pS+2pM^2+qC. At mean one, d=M(Tf)=2p+qA and S(Tf)=2pS+2p+qC.

The load-bearing inequality C M<=A S is valid. Expand the symmetric double integral in the reconstruction: its four terms combine into AS-CM with the stated coefficient. All terms are absolutely integrable since u,v are bounded and f is nonnegative in L1 and L2. Its pointwise integrand is nonnegative because (u-v)(f(v)-f(u))>=0. The decreasing assumption is essential; an increasing profile reverses this sign, as the negative controls demonstrate.

For M=1, substitution gives S(Tf)<=dS+2p, and division by d^2 gives

S(Tf/d)<=S/d+2p/d^2<=(S+1)/(2p).

Since (R+1)/(2p)=R for R=1/(2p-1), the normalized map preserves S<=R. No reciprocal cap is valid. The deterministic initial profile lies in this set, proving the finite-depth normalized second-moment bound by induction.

The mean-one slice is convex, including its L2 constraint. Every such decreasing f satisfies f(u)<=1/u after choosing a monotone representative. On each interval bounded away from zero, Helly selection applies. A diagonal selection converges almost everywhere. The uniform L2 cap gives uniform integrability on the full interval, not only local boundedness; Vitali then upgrades convergence to L1. Mean one survives L1 convergence and the L2 cap survives by Fatou. The limit is nonnegative and decreasing modulo null sets. Hence K is a compact convex nonempty subset of L1, exactly the topology needed for Schauder. Mean normalization is continuous because d>=2p>0.

The finite cap is not available at p=1/2. The sequence n times the indicator of (0,1/n) explains why mean one and monotonicity alone do not supply L1 compactness.

## 5. Perturbation, selection, and maximality

The perturbation must be defined on the cone by T_e(f)=T(f)+epsilon M(f)1. Replacing M(f) by 1 on the entire cone would destroy homogeneity, although the two expressions agree on the mean-one slice. The reviewed proof retains the correct definition. T_e is order-preserving, homogeneous, and L1 continuous before normalization. No unjustified claim that the normalized map is order-preserving is used.

Adding a nonnegative constant c to a variable with mean m>0 and second moment s reduces its normalized second moment. The cross-multiplied difference is exactly c(2m+c)(s-m^2)>=0. Applying this after T proves that the normalized perturbed map is a continuous self-map of K. Schauder therefore gives a fixed point f_e with eigenvalue lambda_e=d(f_e)+epsilon and lower bound f_e>=epsilon/lambda_e.

Because of that positive lower bound, homogeneity and order comparison give lambda_e^n f_e >= c_e T^n1. Integrating and taking n-th roots proves lambda_e>=rho; c_e may depend on epsilon, but it is held fixed while n tends to infinity. This order of limits is legitimate.

As epsilon tends to zero, compactness permits a converging subsequence of profiles, and the scalar bounds permit a converging scalar subsequence. L1 continuity passes the perturbed identity to Tf=lambda f, with M(f)=1 and lambda>=rho. Jensen domination of this limiting eigenprofile gives lambda^n<=m_n for every n; hence lambda<=rho. Thus lambda=rho. There is no reliance on convergence of N^n1.

The same Jensen argument bounds the eigenvalue of any nonnegative, nonzero, integrable decreasing eigenprofile, whether or not it is in K. This proves maximality in the stated large class. Existence plus maximality does not prove uniqueness of the profile. Every sequence of perturbed eigenvalues has cluster value rho, so the eigenvalues converge regardless of selection; this does not show the selected profiles converge without passing to subsequences.

As an additional boundary check, no mean-one eigenprofile with rho>1 can be bounded below by a positive constant. For q>0, the essential infimum of the sum/min output equals the input essential infimum, whereas the eigen-equation multiplies it by rho. Thus the positive lower bound of the perturbed profiles need not survive the limit. The proof correctly does not use such a surviving lower bound.

## 6. Variational formulas and invariant measures

For a lower subeigenprofile Tf>=a f, iteration and Jensen give a^n<=m_n, so a<=rho. The constructed eigenprofile attains equality. Zero values of f cause no difficulty when the statement is phrased as a pointwise inequality instead of dividing by f.

For an upper supersolution Tf<=b f with f>=c>0, compare cT^n1<=T^n f<=b^n f. The resulting c m_n<=b^n proves rho<=b. The perturbed fixed points give admissible upper supersolutions at b=lambda_e, whose values approach rho. These two directions prove the infimum formula. The proof does not require or establish that the upper infimum is attained.

The invariant-measure formula also holds. The observable log d is continuous and bounded on compact K. Homogeneity telescopes the logarithm of M(T^n f) into the sum of log d along the normalized orbit. Integrating against an invariant measure yields n times its average, bounded by log m_n through Jensen. A Dirac measure on the eigenprofile attains log rho. Nothing forces all maximizing invariant measures to be fixed-point masses.

The external canonical proof includes a continuous ergodic dual not retained in the shorter reconstruction or four-page manuscript. It is also valid: choose N with log m_N/N<c for c>delta. Jensen then bounds every N-step sum by Nc. For h=max_(0<=j<N)(F_j-jc), the elementary shift of this finite maximum gives log d+h composed with N-h<=c. Weak duality follows from invariance. This is supplementary and not needed for the main verdict.

## 7. Endpoints and status limits

The primary published Theorem 1 was checked in text, publisher HTML, and the rendered journal page 82. It uses epsilon=p-1/2 and states delta(1/2+epsilon)/sqrt(epsilon) tending to pi/sqrt(6). Some search-index extractions flatten the radical incorrectly; those do not override the theorem's visual typesetting. In the alternative bias parameter h=2p-1, the same constant becomes pi/sqrt(12) multiplying sqrt(h). The long published proof was not independently rederived in this audit.

Coupling all finite gate trees by shared uniform marks proves monotonicity in p. Nonnegativity and the published right-hand critical asymptotic squeeze delta(1/2) to zero; no continuity assumption is needed. This does not assert first priority for the critical identity. At p=1, D_n=2^n directly gives log 2.

For the right endpoint, write s=EX^2 and use E(X-Y)^2=2(s-1)<=2(R-1). Cauchy-Schwarz then gives the reviewed lower bound on E min(X,Y), hence

1+p-(1-p)^(3/2)/sqrt(2p-1)<=rho<=1+p.

For p near one the lower bound is positive, and a uniform logarithmic expansion gives delta=log 2-(1-p)/2+O((1-p)^(3/2)). The equality typo identified at the start is therefore repairable locally without changing the theorem or adding a new assumption.

The frozen manuscript gives no scalar closed form, global convexity theorem, eigenprofile uniqueness, full normalized-orbit convergence, or general almost-sure distance exponent. These remain exclusions from **this theorem**, not assertions that no later literature treats them. SOURCE_UPDATE.md documents the newly located September 2026 preprint. Its existence requires care with literature-wide openness claims, but its results are not used anywhere in the audited proof.

## 8. Final acceptance boundary

The original author PDF still returned 404 and the exact catalogue page still returned 403 in this independent pass. An indexed primary-source excerpt at the author's erdos.pdf URL corroborated Question 9.6 and the expected-distance formulation; it remains index-only and does not restore original PDF bytes or a full inspected catalogue entry. No raw-corpus statement hash is certified.

Within those constraints, the reconstructed theorem is substantive: it proves existence of an actual maximal eigenprofile and matching comparison formulas, rather than merely renaming the defining limit. It still leaves the semantic breadth of “shape” unresolved. A responsible record should say that a credited exact implicit spectral characterization passed analytical audit with one minor reconstruction erratum, and should retain the source access limitations and 1/5 accounting. No remote writes, commits, branches, pull requests, queue mutations, or publications were made during this audit.
