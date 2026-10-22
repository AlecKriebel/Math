# Independent mathematical audit: rational VOA automorphism finiteness

Problem 30002842 / OWR-13673-012, queue rank 991. Audit date: 2026-10-07.

## Decision

Accept the frozen report's five routes as rigorously delimited partial progress. Do not accept the full conjecture as proved, disproved, or resolved by the inspected manuscript. The central objection to Han v5 is valid: its final passage from componentwise convergence to convergence of an infinite, moving zero-mode tail is unsupported, and the supplied affine descendant sequence satisfies the actual conditions used in that passage. This is a defect in an argument, not a counterexample to its conclusion.

No mathematical correction to the frozen report is required by this audit. One reproducibility correction is required for running its mutation suite directly from a read-only release. The separate patch changes only permissions of disposable test copies and updates the corresponding manifest entry. The frozen input remains unchanged.

Frozen identity:

- MANIFEST.json SHA-256: a9b478491ffe9f3dd75d177bd863ec8dc2f28ac3ed69f04bce9e35955247e989
- REPORT.md SHA-256: d87d55930ab6d9d3c644dc975cebbc5f9a3bf3523c7cb77a2168ded696231098
- REPORT.md: 28,899 bytes

## 1. Independent primary-source check

The question is Lam's Conjecture 0.1, printed page 904 of [L]. Its assumptions are rationality, C2-cofiniteness, CFT type, and V1=0. Simplicity, unitarity, holomorphicity, and generation in weight two are not additional stated assumptions.

The current arXiv abstract/version page and v5 HTML were inspected independently. They identify v5, dated July 9, 2026, as the latest version displayed. Version v2's withdrawal and its stated omitted case are historical facts; they are not grounds to reject v5. No journal reference was displayed. The proof of Theorem 2.7, especially its final paragraph, was compared against the PDF. A fresh download of the version-specific v5 PDF has 290,613 bytes and SHA-256 1171467d597568d4385aedf560f14e9a3945a67e7bb391b29c61c2a326d590c4, exactly matching the supplied copy. The full mathematical section and displayed construction were read; page 9 was also inspected visually. [H5]

All seven supplied source-PDF fingerprints match the frozen metadata. The radical decomposition, Dong–Griess algebraicity theorem and derivation discussion, and the affine/Virasoro regularity statements were checked in their cited primary sources. This audit does not independently replay the historical repository-search gate or re-establish the corpus fingerprints. Their bytes are authenticated as part of the frozen packet; their historical search coverage remains the original report's qualified account.

## 2. Does the escape example satisfy the actual representative construction?

Yes. Write T=L(-1), and for a homogeneous vector of positive weight k use the translation identity

    o(T^r a) = (-1)^r (k)_r o(a),
    (k)_r = k(k+1)...(k+r-1).

The identity follows by induction from (Ta)_m=-m a_(m-1). There is no limiting argument here.

In the simple rational affine VOA L_1(sl2), take the Cartan current h and a root current e with h_0 e=2e. The currents have weight one and are primary for the Sugawara conformal vector. Thus d=h_0 is a nonzero conformal derivation. Regularity of positive-integral-level affine VOAs is supplied by [R, Theorem 3.7]. Define

    c_N = (-1)^(N-1) T^(N-1)h/(N-1)!,  N>=1.

Then o(c_N)=d. Each c_N, regarded as a formal representative with one nonzero homogeneous component, is pointwise o-additive and belongs to E_d.

The sl2 relations give

    L(1)T^r h = r(r+1)T^(r-1)h,
    L(1)c_N = -N c_(N-1),  N>=2.

All these descendants are nonzero: repeated lowering would otherwise force h=0. Hence the first non-quasi-primary component of c_N is exactly its component in degree N. Its t-index is N, not infinity.

For n>=1 take N=n+2 and b_n=c_N. The displayed construction in [H5, proof of Theorem 2.7] preserves the lower components, sets degree N to zero, and replaces each upper component by its normalized translate. On this input the result is exactly

    hat b_n = -T c_N/N = c_(N+1).

The elimination targets in degrees 2 through N-1 are already zero. The elimination rule referred to in Proposition 2.5 is conditional on a nonzero component. Therefore choosing no such unnecessary elimination gives tilde b_n=hat b_n, with the required low-degree vanishing and support condition. This is an allowed instance of the displayed procedure, not just an arbitrary sequence in a larger completion.

For each fixed degree i>=2, tilde b_n^(i) is eventually zero. Nonetheless

    o(tilde b_n^(1)) = 0,
    sum_(i>=2) o(tilde b_n^(i)) = d,
    d(e) = 2e != 0.

The moving tail therefore fails to tend to zero even on the single fixed vector e. Every sum in this example has just one nonzero summand. Finiteness of each individual sum does not furnish a bound uniform over n.

The source gives no relation requiring b_(n+1) to be obtained from b_n, no preferred representative selection, no common support bound, and no tail estimate. Its fixed-degree continuity lemma cannot provide any of those facts. The example even forms a coherent translation sequence, so asking for unspecified coherence would not by itself repair the step.

An important qualification: this d is already inner, and E_d also contains h, whose t-index is infinity. The written argument does not exclude this situation before its final passage. If one rewrote the proof to treat attained infinity separately, this particular affine example would already have been handled. That rewrite would still require a proof of tail control for the remaining case; it would not turn the displayed sum-limit inference into a valid general principle. No example of an outer derivation, or of a counterexample with V1=0, is supplied here.

A useful universal check is available. For any b in E_d and m>=1, shift its component b^(i) to degree i+m as

    (-1)^m T^m b^(i)/(i)_m.

Each zero mode is unchanged, and the pointwise finite-support bound merely shifts by m. Thus an arbitrarily long zero initial segment and an arbitrarily large t-index are available for every nonempty E_d, irrespective of innerness. Large t alone measures where the representative is stored; it does not control its action.

## 3. Review of all five mathematical routes

### I. Simplicity, finite generation, algebraicity, and tangent rigidity

The simplicity proof is valid for the stated definition of rationality. Semisimplicity of the admissible module V supplies module projections. Each sends the vacuum to a scalar multiple of itself because V0 is one dimensional and the projections commute with L(0). One projection is the identity on the vacuum; its image contains every a=a_(-1)1. Thus its image is V. Replacing rationality by semisimplicity of A_0(V) would not justify this argument.

The C2 finite-generation induction is sound. In a homogeneous term a_(-2)b of weight n, nonzero a has positive weight unless the term is zero. If b has positive weight, both weights are below n. If b is a vacuum multiple, the term is a translate of a lower-weight vector. Homogeneous representatives of V/C2(V), together with the specified conformal vector when needed, therefore generate V.

Dong–Griess supplies algebraicity for finitely generated VOAs. The restriction to a finite generating truncation is faithful. Linearization gives conformal derivations; conversely, exponentiation of a grade-preserving derivation on finite-dimensional weight spaces yields automorphisms and the corresponding tangent vector. A reduced finite-type complex algebraic group is finite exactly when its Lie algebra vanishes. Hence the stated criterion Aut(V) finite iff Der(V)=0 is valid. [DG]

The finite-full-rank-witness observation is also valid: a family of linear constraints on a finite-dimensional space with zero common kernel has a finite subfamily with zero kernel. It provides no universal weight cutoff. The centralizer in the cited structure theorem cannot be suppressed when V1=0, since then centralizing V1 is no restriction.

### II. Completed representatives and the manuscript audit

The report's interpolation construction is valid assuming the cited rational higher-Zhu decomposition. It chooses finite-truncation corrections and lifts each positive-weight homogeneous part to a new, strictly increasing common weight using the translation identity. Each later correction vanishes on earlier test spaces. Consequently the completed zero-mode sum is pointwise locally finite and equals the prescribed map.

The use of freely chosen increasing lift weights is significant: it avoids relying on the manuscript's asserted strict increase of minimal weight bounds. No proof of that strict-increase assertion is needed here.

The construction works for arbitrary grade-preserving linear maps killing the vacuum, so it cannot by itself establish the derivation-specific conclusion. The descendant test above verifies the report's central objection. The separate minimal-model example with omega gives o(a_N)=L(0), correctly classified as a continuity example only: L(0) is not a conformal derivation when omega is nonzero.

### III. Weight-two algebras and the tensor-Virasoro subclass

With V1=0, skew symmetry makes a_1 b commutative on V2. Automorphisms preserve this product and the scalar product a_3 b. Injectivity of restriction to V2 requires V2-generation, which is not inferred for all target VOAs.

For a tensor product of nontrivial simple Virasoro minimal-model vacuum VOAs, V2 has basis omega_i, and

    omega_i * omega_j = 2 delta_ij omega_i,
    (omega_i)_3 omega_j = delta_ij (c_i/2)1.

After putting f_i=omega_i/2, the weight-two algebra is C^r with coordinatewise multiplication. Its primitive idempotents are exactly f_i; thus every VOA automorphism permutes them. Preservation of the scalar form forces equal central charges in each orbit. Conversely, factors with the same central charge are isomorphic simple Virasoro vacuum VOAs, and permutations of equal factors extend to conformal VOA automorphisms. Generation by these vectors prevents an additional kernel. This proves precisely the stated product of symmetric groups, including repeated central charges. The exclusion of trivial factors avoids spurious zero conformal vectors.

The spin-factor obstruction is valid. In A=Ce+W with wv=B(w,v)e and e the identity, the stated form is associative and nondegenerate. Every B-skew endomorphism of W, extended by zero on e, is a derivation. Conversely, writing D(w)=ell(w)e+Kw in Leibniz forces ell=0 and K skew. Hence the derivation dimension is s(s-1)/2. No VOA realization of this algebra is asserted.

### IV. Closed inner space and valid tail repairs

The closedness proof is valid. The finite-dimensional operator space o(V1) has a finite truncation on which restriction is injective: the descending kernels eventually stabilize, and their intersection is zero. Its image is closed in the finite-dimensional truncation space. The inverse on that image is continuous, so pointwise convergence of inner derivations identifies a unique inner limit on every weight space. The proof works for nets as well as sequences.

If whole tails tend to zero pointwise, then the weight-one zero modes tend to d and closedness applies. The alternative uniform cutoff on a finite generating space is also sufficient: choose n beyond the common cutoff, compare the two derivations on generators, and extend by Leibniz. Both repairs have the necessary quantifier uniformity. Neither is derived from the target hypotheses.

### V. Pointwise-locally-finite spectral separation

Theorem 4 is valid as stated, including its lack of rationality or finite-generation assumptions. Put A_i=o(q_i) and C(A)=[T,[L(1),A]]. For i>=2, quasi-primarity and the mode commutator yield

    C(A_i) = -i(i-1)A_i.

For i=1, L(1)q_1 is a vacuum multiple and its mode of index zero vanishes, so C(A_1)=0 without assuming L(1)q_1=0. A conformal derivation commutes with T and L(1), giving C(d)=0.

There is no invalid infinite interchange in this proof. To evaluate C once on a locally finite sum at v, only the sum's evaluations at finitely many vectors, including v, Tv, L(1)v, TL(1)v, and L(1)Tv, are needed. An iterate of fixed length still needs only finitely many test vectors. Taking their maximum support bound legitimizes termwise commutators. Therefore C^r(d)=sum_i[-i(i-1)]^r A_i for every fixed r.

For fixed v let J consist of the finitely many i>=2 with A_i v nonzero. The polynomial P(x)=product_(i in J)(1+x/[i(i-1)]) has P(0)=1 and annihilates the relevant nonzero eigenvalues. Evaluating P(C)d at v gives d(v)=A_1 v. The dependence of P on v is harmless because equality of two fixed operators is established separately at each v.

The missing existence claim is genuinely separate. Finite vectors admit repeated quasi-primary/translation reduction by [Rad, Lemma 3.3]. Infinite representatives can send infinitely many high components into the same low degree, with no convergent sum there. Pointwise local finiteness before reduction does not establish it afterward. The theorem is a conditional innerness criterion, not a construction of such representatives.

## 4. Source-level qualifications that do not overturn the report

The inspected manuscript's Proposition 2.5 is stated for CFT-type VOAs but its written proof invokes rationality and finite generation. The frozen report supplies the independent spectral proof needed to remove that dependency; it does not silently rely on the source's proof at its stated generality.

The finite-supremum part of the manuscript has a piecewise-definition overlap at degree t-1 that is naturally read as an endpoint typo. Neither the report's high-support construction nor the counterexample depends on it. This audit does not need to certify every earlier manuscript reduction before diagnosing the final passage: the concrete example realizes the prescribed support conclusion directly.

The topological embedding of the finite-dimensional weight-one quotient can be strengthened to closedness, as the frozen report does. That part is repairable. It cannot supply the absent convergence of the higher-weight tail.

## 5. Reproducibility correction and independent controls

The supplied release is read-only. Its baseline verifier succeeds in ordinary Python, -O, and -OO. Its unmodified negative-control runner fails on its first file mutation because shutil.copytree preserves the read-only modes, causing PermissionError before the intended rejection test. This is an execution defect, not an accepted bad mathematical fixture.

READONLY_REPLAY_FIX.patch makes only the newly created disposable fixture directory and its files writable. It also updates the changed script's manifest entry. Applied to an isolated copy and then frozen read-only again, the corrected suite succeeds: 3 positive baselines, 30 rejected false mathematical claims, and 21 rejected integrity fixtures across the three modes. No original frozen byte was modified.

The independent verifier additionally pins the original manifest and report, rejects unexpected files, symlinks, duplicate keys and rehashed changes, checks strict claim types, and recomputes finite exact arithmetic independently. Its own negative controls include scope inflation, sign and coefficient changes, false subclass group orders, and inventory/integrity mutations. Rejection is required to arise from the intended explicit validation, not merely any process failure. Results are recorded separately.

These programs establish finite arithmetic and release integrity only. They do not constitute a formal proof of general VOA results. A release hash is an integrity anchor, not a cryptographic signature or an independent literature review.

## 6. Final acceptance boundary

- Accepted: the five partial routes, their stated assumptions, and the exact v5 sum-limit objection.
- Accepted with a separate execution patch: mutation-suite reproducibility from a read-only freeze.
- Rejected as conclusions of this packet: full finiteness, a counterexample, verified prior resolution, novelty, formal verification, or exhaustive current literature coverage.
- Preserved outcome: unsolved_partial; five substantive approaches; no theorem or conjecture falsification claimed.

## Primary references

[L] Ching Hung Lam, Vertex operator algebras and finite groups, in Subfactors and Conformal Field Theory, Oberwolfach Reports 12 (2015), no. 2, Conjecture 0.1, p. 904. https://ems.press/journals/owr/articles/13673

[H5] Jianzhi Han, Derivations of rational vertex operator algebras are inner, arXiv:2606.05854v5, July 9, 2026. https://arxiv.org/abs/2606.05854v5 ; https://arxiv.org/html/2606.05854v5 ; https://arxiv.org/pdf/2606.05854v5

[DG] Chongying Dong and Robert L. Griess Jr., Automorphism groups and derivation algebras of finitely generated vertex operator algebras, Michigan Mathematical Journal 50 (2002), 227-239. https://arxiv.org/abs/math/0106051

[Rad] Chongying Dong, Haisheng Li, Geoffrey Mason and Paul Montague, The radical of a vertex operator algebra, The Monster and Lie Algebras (1998), 17-25. https://arxiv.org/abs/q-alg/9608022

[R] Chongying Dong, Haisheng Li and Geoffrey Mason, Regularity of rational vertex operator algebras, Advances in Mathematics 132 (1997), 148-166. https://arxiv.org/abs/q-alg/9508018
