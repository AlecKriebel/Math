# Independent audit: AMR-052-0056 / 5300056

## Verdict

**PASS for the scoped mathematical partials, with one minor covering-proof correction recorded separately. The general target remains UNSOLVED in this investigation.** Five analytical routes are documented; this audit is not a sixth attempted solution, a novelty finding, or human peer review.

The immutable author archive has 17,955 bytes and SHA-256 `f603686a4d0a3d22cb26b6f1dbb972a8dd37a746a0738ef43165e3d9ff6d66ed`. Its nine members are preserved byte-for-byte under `author_freeze/`. The reviewed proof is 11,994 bytes, SHA-256 `96c90264fa8c741818dac32abd6a4b203d1ee7e782699f55a28c61dbe3ae0014`. The original manuscript's unaudited labels describe that historical freeze, not this appended audit.

No fatal mathematical error was found in the four propositions or Corollary 1.1. The finite tests pass, but they do not certify the infinite arguments. The correction in `CORRECTIONS.md` fixes a literal false ancillary sentence about arbitrary metric spaces without changing any theorem, hypothesis, constant, or conclusion. A clean revised manuscript should make that correction explicitly; this audit does not silently edit the freeze.

## 1. Exact target and source boundary

The primary locator is Przytycki's Problem 2.5, printed page 32 of [Problems in Holomorphic Dynamics, IMS 1992/7](https://www.math.stonybrook.edu/preprints/ims92-7.pdf). The surrounding setup is a holomorphic quasi-repeller, ergodic invariant probability measures with positive entropy, and equivalence of the branchwise pulled-back measure with the original measure. Centering is inherited from Problem 2.2. The source does not assume universal expansion and already credits expanding/Hölder-Jacobian, the specified RB-domain harmonic-measure, and rational maximal-entropy cases. These are not new results of the note. Printed pages 29–34 were independently text-inspected; pages 31–32 were independently rendered from the freshly downloaded PDF and visually checked.

The full target record and its uniquely joined research report reproduce the catalog's statement hash and review hash. The latter uses the entire record/report pair, not just the statement. The catalog's older open/triage status is not proof of current open status. The exact UnsolvedMath page remained unavailable through the web tool. No verified unrestricted resolution was established in this audit; that is a bounded search result, not a bibliographic theorem.

## 2. Hilbert-space argument and orientation

On a probability-preserving system, Uv=v composed with T is an isometry. It need not be onto. The proof uses neither U inverse nor an adjoint identified with inverse iteration. For the stated average A_N,

    (I-U)A_N = phi - U S_N(phi)/N.

The remainder has norm at most C/N. A bounded Hilbert-space sequence admits a weakly convergent subsequence even without a separability assumption on the whole space: one can work in the separable closed span of the countably many sequence elements. Weak continuity of I-U and weak lower semicontinuity of the norm give phi=(I-U)A and norm(A)<=C. Choosing u=-A gives precisely phi=Uu-u, the orientation used later.

Conversely, S_n(phi)=U^n u-u and the triangle inequality gives the stated 2||u|| bound. Probability preservation justifies the zero-mean conclusion. The Borel–Cantelli proof of S_n(phi)/sqrt(n) tending to zero is sound because the tail sum of the integrable variable |u|^2 is finite; no independence is needed.

The [2010 weak-mixing paper](https://lmrs.univ-rouen.fr/sites/lmrs.univ-rouen.fr/files/membres/u101/el-abdalaoui-el-machkouri-nogueira_a_criterion_of_weak_mixing_property.pdf) does state the L2-coboundary criterion on printed page 109. Its surrounding setup is an automorphism. Consequently the general noninvertible claim is justified here by the note's complete proof, rather than by pretending that citation explicitly treats every endomorphism. This distinction does not undermine the proof or its classical attribution.

## 3. Branchwise change of measure, centering, and finiteness

For rho=e^(-u), the branch Jacobian transforms as

    J_nu f = J_m f * (rho composed with f)/rho
           = e^a |Df|^kappa.

The numerator is the density at the image. Reversing that ratio, or using e^u, gives the wrong sign. The branch change-of-variables formula follows first for nonnegative simple functions and then by monotone convergence, so no hidden finite-integral assumption is needed. Measurable branch images and identities are part of the branch-Jacobian setting; this is not a statement about arbitrary nonmeasurable images.

With the probability measure m of the setup, finite real u gives a positive finite density almost everywhere. This proves equivalence and sigma-finiteness by the sets |u|<=k. It does not prove finite total mass. Finiteness holds exactly when the displayed negative exponential moment is finite. Normalization leaves a branch Jacobian unchanged. Invariance of nu is not asserted.

For n iterates the factor is e^(na). The geometric criterion and its corollary use the unweighted derivative Jacobian and explicitly require a=0 where they invoke conformalization. The note never obtains a=0 merely by renaming centered sums. Its separate entropy and dimension identities are sufficient when valid with finite integrals; they are not imported into arbitrary measurable systems.

For ergodic f, any two finite real transfers differ by an invariant function and hence a constant almost everywhere. Thus the exponential-integrability obstruction cannot be removed by choosing another such transfer.

## 4. Binary-shift obstruction

The one-sided fair shift is ergodic and probability preserving; the initial-zero-run variable K has the asserted geometric law. Its moment recurrence yields E(K^2)=3 and E(K^4)=75, hence the centered transfer u=3-K^2 has squared L2 norm 66. Telescoping gives the claimed uniform squared bound 264. The negative-exponential series diverges by its terms, and arbitrarily long zero runs recur almost surely. Therefore the orbit sums are unbounded below almost surely despite their uniform L2 bound.

An independent sharper check is available. If K_n=K composed with T^n, separating the event that the first n bits are zero from its complement gives

    E(K^2 K_n^2) = 9 + 2^(-n)(20n+66),
    ||S_n(phi)||_2^2 = 132 - 2^(1-n)(20n+66).

Thus 132 is the supremum of these squared norms. The author's looser 264 bound is correct and need not be changed.

This is an arbitrary chosen observable on a Bernoulli system. No equality with the constrained holomorphic Jacobian/derivative discrepancy is proved. It is an obstruction to abstract functional-analytic shortcuts, not a counterexample to the historical problem.

## 5. All-scale covering argument

The four explicit geometric assumptions immediately give nu(B(x,r))<=C_x r^kappa at every sufficiently small radius. Passing to countably many uniform sets E_j then proves absolute continuity by the Hausdorff covering definition. The E_j need not be measurable: each covering estimate bounds outer measure and their union covers the conull set. Neither a measurable choice of return time nor a doubling or Besicovitch hypothesis is being smuggled in.

The only correction is the sentence claiming that singleton covering members can always be replaced by positive-diameter balls. This is false at isolated points in an arbitrary metric space. The growth inequality itself proves nu({x})=0 on E_j, so zero-diameter members of the countable cover can instead be discarded after accounting for their zero outer mass. The positive-diameter members are handled exactly as written. See the exact old/new edit in `CORRECTIONS.md`.

The requirement of finite landing mass is substantive. Sigma-finiteness alone gives no common finite bound for the chosen images. A finite nu supplies a global bound, and the corollary says this correctly. The all-small-radii hypothesis is not derived from positive entropy, measurable recurrence, or the L2 coboundary.

## 6. Moran control and its limits

The stage end and peak indices are respectively 2j^2+j and 2j^2-j. The walk has unit steps and b_n^2<=n, so b_n=o(n). The contraction ratios are exactly 1/3 and 3/16. First-divergence gaps are at least the current interval length, giving the claimed ball-overlap bounds. The two-sided mass estimates at intermediate radii therefore prove exact dimension 1/2, including at endpoints because the measure has no atoms.

At troughs, the level-cover half-dimensional cost tends to zero. At peaks, the density upper bound tends to zero for every support point. In fact the trough lower mass estimate makes the upper density infinite at every support point, which emphasizes that a good subsequence cannot imply the all-scale bound. These conclusions are consistent with exact dimension and H^(1/2)(E)=0.

The construction has not been equipped with a holomorphic quasi-repeller realization or the required Jacobian discrepancy. It correctly refutes only the bare geometric inference. No dynamical counterexample or general negative answer follows.

## 7. Later literature and remaining bridge

[Dobbs's paper](https://arxiv.org/abs/0804.3753) was checked at Definition 2, Theorem 8, and Proposition 28. Its conformal reference measure is a probability, and its theorem concerns absolute continuity relative to that specified reference measure under rational-map and positive-Lyapunov hypotheses. It cannot turn an arbitrary sigma-finite density into a finite reference measure, nor identify it with Hausdorff measure without an additional argument.

The [fine-inducing preprint](https://sites.itservices.cas.unt.edu/~urbanski/papers/FI-1-Dim20110924.pdf) was checked at the pressure-gap/Hölder setup, normalized Jacobian formula, Theorem 43, Lemma 57, and Theorems 63–64. These are structured rational equilibrium-state results. The [journal metadata](https://link.springer.com/article/10.1007/s11856-015-1257-6) agree with the author note; theorem numbering is from the inspected preprint. The [Denker–Urbanski publisher abstract](https://link.springer.com/article/10.1007/BF02782852) gives a Hausdorff/conformal comparison in the stated subexpanding class. No unchecked generalization to all quasi-repellers was accepted.

The missing result remains a justified passage from the original constrained L2 hypothesis to suitable integrability/finite landing mass and all-scale geometric control, or a different argument reaching Hausdorff absolute continuity. The note correctly leaves this unresolved.

## 8. Reproducibility and limits

- Original verifier: PASS, 21,193 exact finite assertions.
- Independent verifier: PASS, 20,371 exact finite assertions, including a genuinely nonsurjective Koopman-isometry model and nonuniform Bernoulli branch measures.
- Full-byte corpus verification: three pinned files match; 15,458 problem records and 6,701 research reports; unique target and unambiguous join.
- Statement hash: `a614504e062997e753cc062b35f1d72bf7c9b69525b5d1bdb8b2b2fa6702e469`.
- Full-record review hash: `d699f57822f44019eccaa623b4da5ef95efde4be68233c08d5229e8ed5fa938c`.
- All three hashed scholarly PDFs were independently downloaded and match the author metadata exactly.
- Exact-ID repository code, all-state PR, and branch searches returned no target artifact; a title/author PR search also returned none. The current queue row still showed queued, 0/5. These are bounded search observations and do not exclude deleted, renamed, unindexed, or unpublished work.

Run `python3 verify_audit.py` for the included payload and both arithmetic suites. `verify_provenance.py --help` describes an optional full-byte replay when the omitted inputs are separately supplied. The offline default must not be described as revalidating omitted source or corpus bytes. Source PDFs, extracts, page images, corpus contents, and private coordination are excluded. No remote write was performed.
