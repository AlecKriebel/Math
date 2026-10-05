# PR95 quantum-source and normalization adversarial audit

Scientific verdict: **PASS for the exact stated counterexample, within the usual theorem-dependent mathematical scope.** The ordinary full SU(5) RT theory at WZW level 5, shifted level 10, is included in the primary construction. Two closed oriented lens spaces with fundamental group Z/5 have nonzero unequal absolute values. An independently derived primary-source computation confirms the submitted numbers exactly. This verdict gives no publication, merge, release, novelty, or priority authority.

The pinned head supplied for this audit is `6534ad01e519c719628a18984b108e73cf2e8ead`. The exact preserved submitted proof has SHA256 `9e412983afbec39f2db103b38e771c0e45d2f5c30b433bd6a92459e9aeb4b6a6`; the preserved verifier has SHA256 `608b10d88b1c57a05a230dd7b4ed954e6cc3305d810ccc804bd58754bcfebf1b`. Object-level head authentication belongs to the parent's adjacent authentication effort. This audit independently records the bytes of all 17 supplied files in `submitted_read_manifest.json` and does not modify them.

## Claim, success criteria, and independence

The hypothesis under test was: in full SU(5), k=5 and r=k+5=10, with tau(S3)=1,

\[
|\tau(L(5,1))|^2=3475+1550\sqrt5,\qquad
|\tau(L(5,2))|^2=4025+1800\sqrt5.
\]

A scientific pass required all of: exact source inclusion of this theory and level; a genuine ordinary unrefined modular RT construction; correct full weight set; correct rational surgery words; complete positive magnitude factors; no dropped nonunit framing factor; nonzero unequal exact results; and isomorphic fundamental groups. Category existence cannot be inferred from a successful matrix program alone.

`PRE_READ_OBLIGATIONS.md` was written before the submitted proof or old review was read. `NORMALIZATION_DERIVATION.md` fixes the primary-source construction and surgery derivation before the submission comparison. The successful independent root-lattice calculation completed at 20:32:58 UTC, before the submitted proof was read. The historical PASS review was read only at the end, after source, exact computation, matrix diagnostics, and source visual checks, for unresolved-finding comparison. Its verdict was not evidence for this verdict. It happens to have used the same readily available HT Gauss-sum family; that overlap does not create a new independent approach family relative to that historical review.

The historical central attempt budget 2/5 remains historical. This audit performs validation of the existing claim and creates no new central proof-search attempt.

## Exact primary source and scope

The target is Conjecture 7.5 on printed page 474, PDF page 102, in [Ohtsuki's publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf). Section 7.1, printed pages 471–474, defines the quantum G invariant on closed oriented 3-manifolds and uses r=k+h∨. The target assertion concerns the absolute value of the nonvanishing invariant and the fundamental group. It is not confined to SU(2), projective/root-lattice variants, prime levels, or homotopy-equivalent manifolds. Nearby odd-level SU(2)/SO(3) comparisons and the preceding prime-level Casson congruence are separate statements. SU(5), k=5, and the two rational homology spheres fit the stated scope.

The attribution is [Guadagnini–Pilo, hep-th/9612090v1](https://arxiv.org/abs/hep-th/9612090v1), whose introduction formulates the conjecture for closed connected orientable manifolds. Its restricted established result concerns SU(2) lens spaces; its SU(3) work is finite numerical evidence. A full SU(5) counterexample does not contradict either restricted result.

The publisher PDF, GP v1, and [Hansen–Takata, math/0209403v2](https://arxiv.org/abs/math/0209403v2) were fetched directly, retained privately, hashed, extracted, and checked at the exact relevant scopes. `SOURCE_READ_SCOPE.json` identifies full-page and excerpt reads and visual checks; `primary_sources/retrieval_manifest.json` and `render_processes.json` preserve provenance. All three PDF hashes coincide with those in the submission's historical source manifest, but this audit obtained them independently. No current literature-status or priority search was conducted.

## Admissible root, group, and label set

HT Section 4, printed pages 26–27, states the modular category induced from U_q(g) at q=exp(pi i/r), r=mκ, κ≥h∨. It invokes Bakalov–Kirillov Theorem 3.3.20. This is a cited quantum-group construction input. Here g=A4, m=1, h∨=5, κ=r=10, so q is a primitive twentieth root. HT's full shifted simple-object set is int(C10)∩X, with X the weight lattice. Unshifted labels are a=(a1,a2,a3,a4), ai≥0, sum ai≤5. The vacuum is shifted rho=(2,1,0,-1,-2), with rho²=10. There are binomial(9,4)=126 labels.

The root-lattice denominator 5 creates no inadmissibility condition gcd(r,5)=1 in that stated construction. HT's later Proposition 5.2 has a coprime (r,p)=1 hypothesis for a simplified lens-space formula. The general Theorem 5.1 used here has no such hypothesis. With p=5 and r=10, that simplification is inapplicable; the construction and general formula remain applicable.

The full category is essential. Its labels have center charges 0,1,2,3,4 with counts 26,25,25,25,25, independently enumerated in the diagnostic. A root-lattice-only restriction would retain only center charge zero and change the object set. At this level one should not silently identify that restriction with a modular quotient or PSU(5) theory. No quotient, transparent-object removal, cohomology-sector selection, spin choice, or bundle label is part of the submitted computation.

The root parameter also needs care. GP uses exp(-2pi i/k_GP), where k_GP is renormalized coupling, corresponding to shifted r; it is not the submission's WZW k. HT's q²=exp(2pi i/r) is the conjugate convention. These mirror conventions preserve the magnitudes at issue. No substitution of WZW k=5 into GP's renormalized-coupling root is justified.

## Unitarity and all normalization factors

HT Eq. (12) gives the normalized matrices on the full shifted weight set. For A4 and r=10, the Weyl sum coefficient is

\[
\frac{i^{10}}{10^2}\sqrt{\frac{\operatorname{vol}(X)}{\operatorname{vol}(Y)}}
=-\frac1{100\sqrt5}.
\]

The root covolume is sqrt5, weight covolume 1/sqrt5, and their ratio is 5. Let S denote this normalized matrix, s=S00>0, D=1/s, theta the relative twist matrix. HT's categorical Hopf matrix is H=D S, not S. The exact values are

\[
s^2=\frac{9-4\sqrt5}{2000},\quad
D^2=18000+8000\sqrt5,\quad D=100+40\sqrt5.
\]

The dimension/rank expressions follow independently from HT Eq. (26)'s positive-root product. All factors are positive at this level. In particular s is neither 1 nor a removable phase.

HT Remark 2.3 supports unitarity using symmetry, conjugation under charge duality, and S²=C. Twist unitarity follows directly because its exponents are real. The full source-derived numeric matrix diagnostic checks all 126 labels without importing the submitted code: maximum symmetry residual 3.54e-16, unitarity residual 7.03e-16, S²=C residual 6.72e-16, and (S T_linear)³=C residual 2.63e-15. Twist moduli differ from 1 by at most 1.12e-16. These are diagnostics, not exact proofs of category existence or replacements for the cited construction.

Here dim(g)=24 and central charge c=(10-5)/10 times24=12. Thus omega=exp(2pi i c/24)=-1 and HT Δ/D=omega^-3=-1. HT T_linear=-theta. All central-charge, projective, mirror, orientation, and signature corrections used in this comparison have modulus one. GP's explicit SU(3) signature correction must not be transplanted to SU(5); HT supplies the correct general-category correction independently. The one-component linking matrix [5] has signature 1, and the two-component matrix [[3,1],[1,2]] has signature 2.

HT uses tau_HT(S3)=s and tau_HT(S1×S2)=1. The submitted normalization is tau'=tau_HT/s. GP Eq. (19) instead displays its invariant normalized to 1 on S3 as a vacuum matrix coefficient divided by a_k, with a_k=S00. These are the same magnitudes after the fixed theory normalization. More directly, HT Corollary 4.2 together with Eqs. (29),(30) and Eq. (35) proves the normalized vacuum-word relation for full SU(5), independently of GP's explicit SU(2)/SU(3) constants.

For either surgery chain, the correct relation is

\[
|\tau'(L)|^2=|F_{00}|^2/s^2.
\]

There is one division by s regardless of the number of chain components. The reason is visible from the Kirby color: for n components tau'=unit × D^-n F_link(Ω,...,Ω), Ω=sum dλVλ. For an unknot the evaluation is sum dλ² thetaλ^5; for the Hopf chain it is sum dλdμ Hλμ thetaλ^3 thetaμ^2. Inserting H=D S, dλ=S0λ/s, gives exactly the same single s^-1 vacuum-word factor. Omitting H's D in the two-component evaluation is a genuine potential error, but the submission's powers of 50000 do retain it.

Control cases agree: the source-derived diagnostic gives normalized |tau'(S3)| approximately1, and |tau'(S1×S2)| approximatelyD=189.44271910. Both lens squared values are below D², as required by the unitary vacuum-coefficient bound. Their sizes above 1 do not violate unitarity after the S3 normalization.

## Surgery words and lens conventions

GP Eq. (16) gives negative continued fractions, with the order z_d,...,z_1. The slopes are 5=[5] and 5/2=3-1/2=[3,2]. Its Eqs. (19),(20) therefore give ST^5S and ST^3ST^2S. Reversing the chain transposes the vacuum word, preserving that coefficient because S is symmetric and T diagonal.

An explicit SL2Z control avoids reading the filling denominator from the wrong matrix entry. With S_class=[[0,-1],[1,0]] and T_class=[[1,1],[0,1]],

\[
S_{class}T_{class}^5S_{class}=\begin{pmatrix}-1&0\\5&-1\end{pmatrix},\quad
S_{class}T_{class}^3S_{class}T_{class}^2S_{class}=\begin{pmatrix}-2&1\\5&-3\end{pmatrix}.
\]

HT writes its lens matrix U with first column (q,p) and defines L(p,q) through slope -p/q. Thus these positive GP slopes correspond to HT q=-1,-2, or q=4,3 modulo5. The general HT formula computed at q=1,2 is their orientation-reversed convention. The exact computation separately checks q=4,3 and obtains the same respective squares. Both positive/negative surgery and inverse-denominator conventions leave the comparison valid.

For topology, rational surgery on the unknot adds mu^5=1 to the exterior group Z, so each fundamental group is Z/5. The two-component Hopf complement has group Z²; surgery relations 3x+y=0 and x+2y=0 give cyclic order5. The same chain's Schur complement gives slope 3-1/2=5/2. The pair need not be homotopy equivalent for a fundamental-group assertion to apply. Its nonhomeomorphism is not needed to establish the failure; unequal invariants already force it in the fixed oriented invariant theory.

## Independently verified finite proof

The full detailed derivation is in `NORMALIZATION_DERIVATION.md`. The principal exact check uses HT Theorem 5.1, independently specialized before the submitted proof was read. In Y={ν∈Z5:sum νi=0}, at p=5 and κ=10 the quadratic Gauss phase is exp(2pi i q|ν|²)=1. The remaining character sum over Y/5Y is 625 if all coordinates of q rho-w rho agree modulo5, and zero otherwise. This criterion is equivalent to q rho-w rho∈5X.

For each q=1,2,3,4, all 120 Weyl permutations and all 625 lattice residues were enumerated. Exactly five permutations survive. The character histogram is [625,0,0,0,0] for each survivor and [125,125,125,125,125] for every other permutation; the latter vanishes exactly by Φ5. The four free lattice coordinates are coefficients of e_i-e_5, i=1,...,4. These generate the entire root lattice and give a genuine complete residue set.

Let z=exp(2pi i/50) and u=z^10-z^15=(sqrt5-1)/2. For q=1 the surviving signs are all positive and rho-dot values 10,0,-5,-5,0. For q=2 the signs are all negative and dot values 5,5,-5,0,-5. The sums are

\[
G_1=z^{-10}+2+2z^5,\quad
G_2=-1-2z^{-5}-2z^5=-(2+\sqrt5).
\]

All subsequent operations are exact rational arithmetic modulo Φ50=z20-z15+z10-z5+1. Conjugation is z→z^-1; division is a checked 20-dimensional rational linear solve. The program proves

\[
|G_1|^2=11+2\sqrt5,\quad |G_2|^2=9+4\sqrt5,
\]

and HT's surviving prefactor has squared magnitude 1/80. Consequently

\[
|\tau_{HT}(L(5,1))|^2=\frac{11+2\sqrt5}{80},\quad
|\tau_{HT}(L(5,2))|^2=\frac{9+4\sqrt5}{80}.
\]

Multiplying by D² gives the submitted squares. The difference is 550+250sqrt5>0. Both are strictly positive. Even in HT normalization their difference is (sqrt5-1)/40>0, so a manifold-independent nonzero rescaling cannot restore equality. No numerical tolerance, inferred zero, semiclassical approximation, or large-level assumption enters this proof.

The successful exact script is `computation/independent_ht_gauss.py`, SHA256 `f6f7e1c1d714373ac5296efc321ff5af25de2962b331fb69d63f99e9ef742682`; stdout SHA256 `a0d6786d75ab49cb5e70d7a0cef33d34438538400a5e866ba9d7526b5f365306`. Its full output and empty stderr are preserved. It needs only Python's standard library. A numeric all-weight computation separately reconstructs both surgery words from HT Eq. (12), yielding 6940.90536512463 and 8049.92235949978. This is corroboration of the exact result.

## Submitted proof and historical review comparison

The supplied proof's A4 prefactor, vacuum shift, label count, ζ100 exponents, relative twists, and surgery-word normalizing powers agree with the independent derivation. In its notation S=-D_ab/(100sqrt5), each one-component numerator has two S factors and each two-component numerator three before division by S00; the denominator powers in its squared formulas are therefore correct. Its integer exponent divisibility follows from common coordinate residues and zero coordinate sum. Its Φ100 is correct. The inequalities 0<u<5/8 and u²+u=1 are valid and provide exact nonvanishing checks.

This auditor did not execute the submitted NumPy verifier in place, nor use its receipt as proof of the outcome. The controlled standard-library independent computation is the main calculation artifact. Parent integration may separately replay the preserved author verifier in an isolated copy.

The historical review was read only after these findings were fixed. It raised the same level, full-weight, sign-of-surgery, S00, and coprimality questions and resolved them consistently. No unresolved scientific normalization finding was identified. Its campaign-status recommendation and claimed assertion count have no authority in this audit; this audit does not adopt a publication status from a previous PASS.

## Mandatory repair versus publication precision

**Mandatory proof/source repair: none identified.** The pinned submitted mathematics and source fit pass this audit. Optional precision for a future authorized rewrite: explicitly distinguish k_GP=r from WZW k, cite HT Corollary4.2/Eqs.(26)–(30)/(35) for full SU(5) instead of relying solely on GP's SU(2)/SU(3) constants, give the concrete omega=-1 and D=100+40sqrt5 normalization, and state the negative-slope lens convention. These improve auditability; they do not repair a missing argument or change the conclusion. Preserve the historical frozen proof and review as historical if integration adds explanatory material.

## Remaining gap and limits

There is no unresolved mathematical gap in this source/normalization audit under the explicitly cited HT modular-category construction and RT surgery theorems. Those are imported published mathematical inputs; this audit does not reconstruct the quantum-group category, establish the ribbon axioms from first principles, or prove the general RT construction anew. The exact finite calculation, all factors, labels, group equality, and source inclusion are independently checked.

Novelty, priority, present literature status, human peer review, publication packaging, merge readiness, remote head authentication, and release permissions are outside this audit. No claim that this is the first counterexample, a minimal example, a homotopy-equivalent pair, or a result about every group or level is warranted. No individual was contacted. No Git/index/branch/native app/PR/Zenodo/Sheets/editor/UI state was mutated. All writes stayed in this dedicated private audit folder. Scientific pass is not publication authority.

## Process and byte closure

Two unsuccessful execution attempts encountered missing SymPy, once in system Python and once in the bundled runtime. Both actual stderr and empty stdout streams, exit1 metadata, and the attempted script are preserved under `environment_failure` and `bundled_environment_failure`. They provide no scientific evidence. The completed exact computation replaced that dependency with transparent rational standard-library arithmetic; its exit0 process receipt is separate. The modular diagnostic also has an exit0 receipt. Source extraction and rendering commands have actual streams and completion metadata.

`PROCESS_MANIFEST.json` summarizes completed/failed controlled processes and stream hashes. `FILE_MANIFEST.json` inventories every payload file, including this report, proof derivation, obligations, source scopes, PDFs, rendered source pages, logs, scripts, receipts, and outputs. `SHA256SUMS` seals the payloads and `FILE_MANIFEST.json`; it excludes itself to avoid recursive checksums. Closure is conventional transitive hash closure, with the final SHA256SUMS hash reported to the parent. The input manifest is rechecked against the preserved originals at closure.
