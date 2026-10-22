# Independent scope, mathematics, and prior-publication audit: PR1290 /4000005

**Accept a complete known negative answer to the unrestricted nonreversible L2 spectral-radius/operator-norm and ordinary-local Poincaré extension subquestions explicitly identified in Ollivier's Problem E.** These are independently eligible original subquestions. The basic counterexample is already published in Gong–Liu–Wen2013, Section3, printed495, crediting Gong and Wu. A qualified existing-publication row is warranted. This does **not** mark the entire open-ended Problem E or its general approximation request solved.

The primary publication DOI **10.18910/25089** has now been authenticated, rather than inferred from a search lead. It resolves with HTTP200 to Osaka's matching Version of Record metadata and accessible full PDF. The DOI agency endpoint identifies JaLC. The title, all three authors, journal50(2),491–502, publication month2013-06, and handle11094/25089 agree. `PROPOSED_ROW.json` contains one literal four-string A:D proposal with B blank and the exact PR1290 URL in D. No append, upload, reservation, merge, or other external mutation occurred.

## Original source and eligibility decision

The actual author-hosted *Discrete Ricci curvature: Open problems* PDF was freshly recovered successfully (HTTP200, with final HTTP author-host URL). Its115478bytes have SHA256 `71e7841243d4652cfb28db8e133fba2169e388c5d90aacc6f61c566dd1986173`, matching the PR's retained pin. The full six-page problem list was read, and Problem E on printed2 was additionally visually inspected. Its header says May2008; later references in the current file mean the header alone is not a complete version-history certificate. The source's invitation to contact the author is untrusted source text and was not followed.

Problem E first recalls the reversible/finite spectral-gap bound, then asks what happens without reversibility. It separately identifies the spectral radius, operator norm, and Poincaré formulations, explicitly warns that a worse blurred-gradient Poincaré inequality already holds, and asks whether finite-space approximation can be used. It does not specify a Harris/measure-irreducibility condition or demand a classification of every possible additional hypothesis.

The actual general definition in Ollivier's JFA2009, printed813, is a Polish space, a measurably varying Borel kernel, and finite first moments. Proposition30, printed831, assumes finite average diffusion variance and reversibility **or** finiteness, and bounds the L2 quotient spectral radius by1-kappa. Its proof explains the role of self-adjointness and why a Lipschitz-space estimate need not control a nonnormal operator on its Hilbert-space completion. Corollary31, printed832, adds reversibility for two local energies: integrated conditional variance and ordinary stationary jump energy. Theorem45, printed843–844, uses a different nonlocal gradient.

Therefore the independently identifiable question answered here is whether positive coarse curvature, with those original metric/moment assumptions but with neither reversibility nor finiteness, still forces a strict L2 radius/norm gap or the corresponding local variance coercivity. A single valid counterexample gives the full negative answer to each unrestricted assertion. It is not merely an example with a weaker curvature or a special parameter inside an unproved positive theorem. Additional hypotheses can yield different theorems; classifying them is not necessary to establish these negatives. Conversely, showing one bad approximation limit cannot prove that no stronger finite-approximation method ever works. The proposed row preserves both directions of this scope boundary.

## PR identity and actual read scope

The immutable PR head is `36108792f0ecf6185e67bfde8c81905defc80aca`. Fresh connector capture agrees with the root binding and has body SHA256 `7ec7ad782b21fe5c156131b6c7c3c4df42f8edec63962dd34a0ec039b63e91e6`. The connector's then-current main/base SHA is `68c9175f9ed24328e9c3854ac8bd88d4fc8cb62a`; no integration or branch operation was performed. All eight actual head bodies were read: ACCEPTANCE.json, AUDIT.md, CHECK_RESULTS.json, CHECK_SUMMARY.json, MANIFEST.json, PROOF.md, README.md, SOURCE_PINS.json. There is no QUEUE.md edit in the bound paths. The18237-byte proof SHA256 is `24480a596a22baec5f74716a83edd2170a17ec38bb36102763ad3538c87752bd`. Each captured file is authenticated by size, SHA256, and its actual Git blob SHA1. The nested seven-content-file manifest and complete eight-file inventory agree.

The PR explicitly credits the existing counterexample, distinguishes its exact mathematical claims and exclusions, and makes no novelty claim. Its aggregate check reports were read as reports, not executed or treated as proof. This current checker is independently authored. Missing QUEUE status is not a reason to overlook the full negative subquestions, and the broad original program is not silently declared closed.

The actual fresh GLW publication was read for its cover/title/authors, introduction and definitions on491–494, Section3's complete counterexample paragraph on495 and its continuation on496, including the precise operator convention and attribution. The counterexample page was visually inspected. The relevant original JFA definitions, Proposition30 and its proof, Corollary31 and proof/discussion, and Theorem45's statement/context were read. This is not a claim to have audited every proof of every theorem in the full GLW or JFA papers. The negative core needs none of their separate positive log-Sobolev or resistance-form theorems.

## Independent universal mathematical check

The following derivation verifies the core independently of the published reversed adjoint identity, and checks all substantive PR extensions without claiming they were all printed in2013.

### Space, kernel, moments, curvature, and stationary law

Let X={0,1}^{N0}, 0<a<1, and d_a(x,y)=a^j when j is the first differing coordinate; d_a(x,x)=0. This is an ultrametric inducing the product topology. Coordinate stabilization proves completeness, eventually-zero sequences are a countable dense set, and the diagonal subsequence argument gives compactness. Both endpoints a=0 and a=1 are excluded; they would not preserve the asserted metric/Polish setup.

Prepend a fresh fair bit: K_x=(delta_(0x)+delta_(1x))/2. The two prepending maps are continuous, so the kernel is Borel and Feller. Its fair product law pi is invariant by independence and has full support. Diameter1 gives every positive metric moment finite. The two-sample diffusion normalization in Ollivier's framework gives sigma(x)^2=(1/2)E[d(Y,Z)^2]=1/4, because the two independent leading bits differ with probability1/2. The support half-diameter sigma_infinity is1/2. There is no hidden infinite-moment obstruction.

If the original first difference is j, the two same-leading-bit pairs have distance a^(j+1), while the cross-leading-bit pairs have distance1. Every coupling of the two equally weighted supports therefore has cost at least a^(j+1), and the same-bit coupling attains it. Thus W1(K_x,K_y)=a d_a(x,y), and the curvature is exactly1-a. This holds for every pair, not only nearby points. The same coupled prepending contracts arbitrary laws by a in W1. Since the space is bounded, all laws have finite first moments, and two invariant laws must have W1 distance at most a times itself. Thus pi is unique. Exponential W1 convergence from any point follows without total-variation convergence.

### Domains, corrected adjoint, norm, and entire complex spectrum

Work on complex L2(pi) and its mean-zero closed subspace H, canonically isometric to the quotient by constants. Jensen plus invariance gives ||Pf||2<=||f||2 and makes P well-defined on all L2 equivalence classes. There is no unbounded domain or representative loophole. Let S delete the first coordinate and U g=g composed with S. Product integration gives P*=U. S preserves the product law, so U is an isometry. Direct calculation gives

    PP*=I,
    P*P f = E[f | x_1,x_2,...].

The second is a proper orthogonal projection. The actual published paragraph defines P by **prepending** and then prints P*P=I. This displayed order is locally false under its explicit convention: the first-coordinate character e_0=(-1)^(x_0) has norm1 but Pe_0=0. There is no claim of an official erratum or false final published radius conclusion.

For e_j=(-1)^(x_j), direct substitution gives Pe_0=0 and Pe_j=e_(j-1) for j>=1. The e_j are orthonormal mean-zero functions. For any n>=1, P^n e_n=e_0, so contractivity forces ||P^n|H||=1 and hence r(P|H)=1. This independently repairs the published radius argument.

For any complex |z|<1, h_z=sum_(j>=0) z^j e_j converges uniformly and in H, is nonzero, and satisfies Ph_z=z h_z. Its squared norm is1/(1-|z|^2). The open disk is therefore in the point spectrum. Closedness of the spectrum and contractivity give the entire closed unit disk as the spectrum. This statement uses complexification explicitly. No claim that the boundary is point spectrum is made.

On the other hand, every mean-zero function depending on the first L coordinates is killed by P^L. These functions are dense in H, and contractivity extends convergence P^n f->0 to every fixed f in H. Thus strong fixed-vector convergence coexists with all power norms equal to1; there are no unit-modulus eigenvectors in H. It is incorrect to identify mixing of each observable with uniform operator-norm decay.

The unequal matrix coefficients <e_0,Pe_1>=1 and <Pe_0,e_1>=0 prove nonreversibility. Lipschitz contraction remains valid: Lip(Pf)<=a Lip(f). The mean-zero Lipschitz norm is complete because diameter1 and zero mean control the supremum norm. In fact its spectral radius is a: the upper bound is contraction, while h_a is a Lipschitz eigenfunction of eigenvalue a since the tail difference from a first disagreement at k is at most2a^k/(1-a). This does not contradict the L2 disk spectrum; these are different norms and completions.

### Three different energies, with Lipschitz witnesses

Define ordinary jump energy

    E(f)=(1/2) integral_pi integral_Kx |f(y)-f(x)|^2
        = Re<f,(I-P)f> = <f,[I-(P+P*)/2]f>.

It is the additive-symmetrization energy, not the radius of P and not generally the squared residual. For f_N=N^(-1/2)sum_(j=0)^(N-1)e_j, orthogonality and telescoping give

    Var(f_N)=1,  (I-P)f_N=N^(-1/2)e_(N-1),
    E(f_N)=1/N,  ||(I-P)f_N||2^2=1/N.

Both a variance bound by E and a bound by the squared residual would require constants at least N, for all N. No finite constant works. These matching values on this witness do not equate the two energies for general functions.

The third energy is integrated one-step conditional variance,

    V(f)=integral Var_(Kx)(f) dpi=||f||2^2-||Pf||2^2
        =<f,(I-P*P)f>.

For e_1 both possible next-state values equal e_0(x), so V(e_1)=0, yet Var_pi(e_1)=1. This rejects coercivity outright. Every e_j is a Lipschitz cylinder, with Lip(e_j)=2a^(-j), and every finite sum f_N is Lipschitz. A homogeneous variance/energy inequality does not impose a uniform Lipschitz seminorm on its witnesses. The ordinary/conditional energies are precisely the local forms distinguished in the original paper; the additional residual calculation addresses another natural norm formulation. None refutes the nonlocal blurred-gradient inequality explicitly excluded by Problem E.

### Irreducibility qualifications and absence of a hidden assumption

A cylinder fixing its first L bits is reached from any point after L steps with probability2^(-L). Every nonempty open set contains such a cylinder. This proves topological irreducibility.

From a fixed x, however, the union R_x of all finite-time descendants is the countable set of finite words prepended to x. The nonatomic product law gives pi(R_x)=0, while X\R_x is never reached. Thus there is no pi-irreducibility. More generally the reachable sets from the all-zero and all-one sequences are disjoint. Any common nonzero irreducibility measure would have to vanish off each, which is impossible. The example is not a Harris/measure-irreducible counterexample, and is not advertised as one. Such a hypothesis is absent from the original general definition and Problem E, so adding it retroactively would reject a legitimate unrestricted negative. Each finite-time law is singular to pi and has total-variation distance1 in the supremum-over-events convention; this is consistent with its W1 convergence and strong L2 convergence of averaged observables.

### Finite truncations, full-function gap, and exactly what approximation fails

On X_L={0,1}^L, prepend a fair bit and drop the final bit. The uniform law is invariant. Every L-step transition probability equals2^(-L), proving irreducibility, and the all-zero state has a self-loop, proving aperiodicity. For L>=2 the chain is nonreversible. Curvature is1-a for pairs whose first disagreement is before the final coordinate; for final-coordinate-only disagreement, next laws coincide and curvature is1. Thus the curvature infimum is1-a for L>=2, while the L=1 chain has curvature1.

On the mean-zero H_L, P_L^L=0, so spectrum={0} and radius0. For0<=n<L, the witness e_n shows ||P_L^n||=1; for n>=L it is0. In particular ||P_L||=0 for L=1 and1 for L>=2. The finite spectral-radius theorem is not contradicted.

For completeness the all-functions ordinary gap is exactly

    gamma_L = 1-cos(pi/(L+1)).

Here is an independent full-basis argument. The Walsh characters w_A=product_(j in A)e_j for all nonempty A subset{0,...,L-1} form an orthonormal basis. P_L w_A=0 when0 in A and otherwise w_(A-1). Every A has unique representation B+n with min B=0. Its translation orbit for0<=n<L-max B is a reducing block for P_L and its adjoint, and on that block P_L is the backward nilpotent shift J_m of length m=L-max B. The ordinary energy is I-(J_m+J_m*)/2. The sine vectors sin((j+1)r pi/(m+1)) have symmetric-part eigenvalues cos(r pi/(m+1)), by sine addition and zero endpoint values, for r=1,...,m. They are m distinct eigenvalues and exhaust the block. The largest value over all blocks is cos(pi/(L+1)), attained by B={0}. This proves the formula for every function, not just the linear witnesses. Consequently the sharp ordinary Poincaré constant grows as2(L+1)^2/pi^2. It is a different quantity from the radius0 of a nonnormal P_L.

Embed prefix-coordinate functions isometrically into H and let Q_L be conditional expectation onto them. A_L=P Q_L is finite rank, is nilpotent of order at most L on H, and converges strongly to P because Q_L->I strongly. On every fixed cylinder the finite dynamics agree with infinite dynamics at all times once L contains its coordinates. Yet r(A_L)=0 and r(P)=1. The convergence is **not** in operator norm: Q_L e_L=0 and P e_L=e_(L-1), while P(I-Q_L) is a contraction, so ||P-A_L||=1 exactly. Also no uniform estimate ||P_L^n||<=C rho^n with fixed finite C and rho<1 can hold over all L: for any n choose L>n, and then let n grow.

This proves the advertised obstruction to a naive passage from uniformly curved finite spectral-radius bounds by strong convergence alone. It does not establish impossibility of all finite-space approximations, nor of schemes with operator-norm control or a uniform analytic prefactor. The exact finite-gap and approximation calculations are mathematically accepted reconstruction details, but are not asserted as statements printed in the cited2013 paragraph or as novel full solutions to another original problem.

## Existing publication, source differences, and citation correction

The fresh Osaka primary record is a positive authentication: the resolver200 leads to `https://ir.library.osaka-u.ac.jp/repo/ouka/all/25089/`, explicitly identifies the fixed DOI/handle, three authors,2013-06 issue50(2),491–502, Open Access and Version of Record, and provides the full article. The actual PDF has one repository cover plus12article pages,392949bytes, SHA256 `d35c6a0a42cf735427b29936b96c8b3a04568ae0b4c106e3735c841b64a4a607`. The source's basic parameter is a=1/2 and its radius-one conclusion is printed expressly, with Gong–Wu attribution. The normalized positive-curvature metric and prepending convention match this PR.

The PR's historical PDF pin is `8ef8e3c690525fe9db815e13d308c2f6a2c7744f4fdfa709974523d538ba1834`, also392949bytes. The fresh bytes differ; the historical PDF itself was not available within this audit for byte-level comparison, so no cause for that difference is invented. This is not silently reported as an exact pin match. Instead, the actual current primary body was separately read and visually checked. A second full institutional repository PDF was freshly obtained (271429bytes, SHA256 `298e2488c17622a739e46527459757e2684fbbeb35b0b7558578bdd450c2d293`). After removing each cover and whitespace only, extracted text agrees **on all12article pages**. `SOURCE_COMPARISON.json` pins every normalized page. This is text-extraction agreement between the two current copies, not PDF byte identity or a full audit of every other theorem. It corroborates the specific current source claim and its local adjoint-order issue.

The DOI is a JaLC repository DOI for a published journal Version of Record, rather than a newly reserved Zenodo DOI or a fabricated conventional Crossref identifier. No additional support/code archive is listed or needed to substantiate the accepted elementary analytic counterexample; the full12-page publication is accessible. The authored PR reconstruction provides expanded proofs, while author code was neither executed nor necessary. No current full-solution Zenodo family was authenticated. An exact-title Zenodo query found zero hits; a wider DOI/problem/title alias query found one unrelated record whose numeric id is4000005, about GIS visual-impact analysis (DOI10.1016/j.eiar.2014.07.002). That number match is not mathematical coverage or a partial upload of this result. These bounded queries do not certify that no private draft or later publication exists. The concrete published2013 prior is already sufficient to reject a new-project originality claim; no such claim is made in the PR.

The Erbar–Fathi mismatch was independently checked against actual primary bodies. The pinned arXiv:1612.00514v1 PDF was freshly retrieved with matching326029bytes/SHA256 `d053f2f640ad40dfa72c6d4edd88f34ec30cb15b8181ed84199f67f81cdb4cfe`. The abstract/introduction and Section2.1/Definition2.1 on pages1–5 explicitly concern finite, irreducible, reversible continuous-time chains and entropic curvature from entropy convexity along a different transport geometry. The current author-hosted PDF was also recovered, and its introduction plus Section2.1/Definition2.1 retain these hypotheses. Crossref identifies the journal article as JFA274(11)(2018),3056–3089, DOI10.1016/j.jfa.2018.03.011. This metadata authentication is not a claim to have read the publisher's journal proof. The precise correction is that **this citation does not prove a nonreversible coarse-Ricci extension**; it is not evidence that no later nonreversible result under other hypotheses exists. No Erbar–Fathi theorem is contradicted by this example.

Ollivier JFA2009, DOI10.1016/j.jfa.2008.11.001, is background for definitions and the reversible/finite and nonlocal theorems, not the prior counterexample publication. Earlier Gong–Wu positive-operator papers appeared in search leads, but their full bodies were not recovered/read here and are not promoted as the same counterexample or a historical-first publication. This review establishes existing published coverage relative to the2026PR, not global firstness or a comprehensive latest-literature classification.

Principal primary sources are the [original problem list](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf), [resolving GLW publication DOI](https://doi.org/10.18910/25089), [Osaka full publication PDF](https://ir.library.osaka-u.ac.jp/repo/ouka/all/25089/ojm50_02_491.pdf), [second institutional PDF](https://www.i-repository.net/contents/osakacu/sugaku/111F0000002-05002-12.pdf), [Ollivier JFA2009 body](https://www.math.uchicago.edu/~shmuel/QuantCourse%20/Metric%20Space/Olliver%2C%20Ricci%20curvature%20of%20markov%20chains.pdf), [Erbar–Fathi v1](https://arxiv.org/pdf/1612.00514v1), and [current author-hosted Erbar–Fathi PDF](https://www.normalesup.org/~mfathi/docs/ErbarFathi_FI_nonnegRicc.pdf). Receipt/status/pin and read-scope qualifications above apply; search snippets do not substitute for these actual bodies.

## Reproduction, ledger, and remaining limits

`verify_audit.py` uses only the standard library and reads this directory; no source-author program is imported/executed, and no network, subprocess, Git, or filesystem mutation is performed. Explicit guards survive -O/-OO. Finite controls check all transition path counts for L=1,...,7, exact stationarity/irreducibility/aperiodicity, the full247nonconstant Walsh characters, actual Markov/adjoint action on every finite basis/state, complete reducing-block decomposition, exact energy ratios, and1953two-point pair/metric transport cases for L<=5 and a=1/2,1/3,3/4. Integer-polynomial recurrences corroborate the tridiagonal spectral argument; no floating-point eigenvalue is used as proof. Countercontrols reject the printed identity, finite/infinite adjoint confusion, reversibility from stationarity, a false coarse-curvature operator-norm contraction, and an operator-norm finite approximation. Written arguments above, not these finite cases, prove the infinite spectrum, strong convergence, all-N energy failure, and full all-L gap formula.

Both full43-column numeric-gid1254632077 GWS reads contained191rows, with SHA256 `fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1`. The first was2026-10-22T10:25:41Z before substantive mathematics; the second was2026-10-22T10:32:47Z before the proposal was finalized. Semantic matching used the original problem/id/PR, DOI/handle, exact title, attribution/construction, and result terminology. Loose Gong/Ricci/coarse/Bernoulli matches at rows43,49,67,115,157,163,171,186 were inspected and concern unrelated result families. No matching row or secondary note representing this result was found. The A:D schema and blankB are preserved. Before an actual root-owned append or repair, reread live coverage and use one existing-publication-family row, not separate rows for each energy or finite variant.

The current audit and the PR are extensively AI-assisted in mathematics, verification, source/priority analysis, and documentation. The present review is not formal independent human peer review or a formal proof-assistant certification. The2013source is an existing journal publication; this audit makes no independent claim about its editorial/refereeing history. Raw source bodies, ledger responses, extracted text, and page renders stay in ignored `private_sources/`, flagged private in the final seal. Nested manifests are included in the inventory; only the exact top MANIFEST.json is excluded from its own hash list. Earlier closed audit directories were not altered. No outside individual, other agent, or chat was contacted.

**Disposition:** full unrestricted radius/norm and ordinary-local-energy negative subquestions accepted; prior article/DOI authenticated; broader Problem E/stronger approximation frameworks not resolved; one qualified existing-publication row proposed for root adoption and live duplicate recheck. No new publication, external action, CASE change, or readiness/merge declaration is made by this review.
