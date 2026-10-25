# Complete independent analytic review — Zenodo 23430906

**Status: COMPLETE. Scientific verdict: PASS for the literal central theorem. Precise remaining central mathematical gap: none found.** This is one AI analytic review, not publication clearance, human peer review, formal proof-assistant certification, a novelty certification, or a certification of every historical support assertion. The parent must read this report, its derivation/addendum, and the actual deposited paper before adopting any conclusion.

Reviewed work: Alec Kriebel, *A localized Gaussian-witness lower bound for fractional iterated area on uniform grids*, version 1.0, original publication date 14 October 2026, DOI [10.5281/zenodo.23430906](https://doi.org/10.5281/zenodo.23430906), public preprint. Author ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Review role: analytic/structural; requested model identity GPT-6.1 Sol, ultra; no child agents. All new files are confined to `papers/23430906/reviews/analytic/`. No source, Git, Sheet, site, deployment, release, UI, or other-review mutation was performed. No external human communication or outreach was prepared or initiated.

## Source identity and reader accounting

The intake worker fetched the public Zenodo API and both actual deposited files on 25 October 2026 UTC. I independently recomputed the hashes and inspected the fresh API metadata/receipt. The frozen queue's local PDF was used only as an early locator. It matches the actual fresh deposit exactly, so there is no development-copy substitution.

| Asset | Bytes | SHA256 | MD5 when applicable |
|---|---:|---|---|
| Fresh `sources/record-raw.json` | 6040 | `50b895ad48cc40a5c948428fff572d53f69a3643fb8ebb22122812796d54730b` | — |
| Deposited `sources/paper.pdf` | 93113 | `33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b` | `655dd4be1adb3ab629d207c3adde4c93` |
| Deposited `PR1071_preprint_v1_0_support.zip` | 3101130 | `4e4a1b20c2da7f5a6e686256f7f8d7bba9c8db71e21f316f99da63285f7b0191` | `2c012b29eda4305081acd5ac4d0d2b0b` |
| Embedded `support/paper.pdf` | 93113 | same as standalone PDF | same |
| Authored `support/paper.tex` | 20792 | `4ffbe0d65609213fd91aecf675661ff278e4e1bd5037db8836f1291f5bdc1d78` | — |

All seven manuscript pages were read completely in text and rendered/viewed. The ZIP has exactly one PDF reader member, `paper.pdf`, byte-identical to the standalone reader; there is one unique published reader, seven pages. All 225 extracted regular members were compared byte-for-byte against their archive contents after review. The complete TeX source, submitted historical rough proof, convention note, all-H supplement, current support prose, and selected finite-checker code were inspected. Old favorable verdicts and old seals were not used to establish mathematics. Detailed hashes and read boundaries are in `SOURCE_READ_LEDGER.json`, `source_start_custody.json`, and `all_published_support_custody.json`.

## Literal claim and success criterion

Fix H∈(1/4,1). The model consists of **two independent standard centered fractional Brownian motions with the same H**, covariance

    R_H(s,t)=(s^(2H)+t^(2H)-|s-t|^(2H))/2,   s,t>=0.

The target is the canonical *iterated* integral

    X_T=integral_0^T B_s^1 dB_s^2,

defined as the L² limit of polygonal lifts. The observation sigma-field is

    G_(T,n)=sigma(B^i_(jT/n): i=1,2; j=1,...,n).

Thus there are n sample values in **each** component, including T; B_0=0 is deterministic. The theorem asserts, simultaneously for all T>0, all integers n>=1, and every F∈L²(G_(T,n)),

    ||X_T-F||_2 >= c_H T^(2H)n^(1/2-2H).

Its explicit positive H-only constant is

    c_H=2pi a/[D_H sqrt(Pbar_f Pbar_g)],   a=4/45045,
    D_H=integral_R |exp(i xi)-1|² |xi|^(-1-2H)dxi,
    alpha=2H+1,
    Pbar_r=pi^alpha ||r||_1²+
       2||r'''||_1² pi^(alpha-6)[1+1/(2(5-alpha))],
    phi=x^4(1-x)^4 on [0,1], zero elsewhere; f=phi', g=phi.

Derivatives are weak derivatives of the zero extensions. Success requires an analytic all-n/all-T/all-H proof under precisely these published assumptions, correct Gaussian and area normalization, a justified canonical-area interface, and no hidden restriction to linear estimators. A finite numerical parameter sweep would not meet that criterion.

The paper expressly excludes a sharp constant, an exact normalized-error limit or distribution, either H endpoint, positivity uniform in H, arbitrary/adaptive meshes, unequal Hurst parameters, and correlated components. None was silently added or removed in this review.

## Strongest verified result and analytic mechanism

The full central finite-n lower bound, with the published explicit constant, is verified under its stated model and parameter range. The decisive artifact is `INDEPENDENT_DERIVATION.md`, corrected only as described in `INDEPENDENT_DERIVATION_ADDENDUM.md` for one excluded-endpoint review control. The first derivation and exact controls were sealed **before any submitted certifier implementation was read**. The structural reconstruction is as follows.

1. **Canonical left-sum interface.** From the established canonical polygonal construction P_m, cell integration gives P_m=L_m+Q_m, where Q_m=(1/2)sum Delta B^1 Delta B^2. Independence gives the exact variance T^(4H)m^(-4H)[m+2sum_(r=1)^(m-1)(m-r)rho_H(r)²]/4. The second-difference bound |rho_H(r)|<=H|2H-1|(r-1)^(2H-2) for r>=2 proves Q_m→0 in L², including the H=3/4 logarithmic boundary. Therefore L_m→X_T. No exact Euler coefficient, lower-rate hypothesis, or disputed v1 asymptotic enters this step.

2. **Independent tensor/conditioning interpretation.** A normalized real harmonizable Hilbert space realizes B_t^i=W_i(K_t), with K_t=D_H^(-1/2)(exp(itxi)-1)|xi|^(-H-1/2). Independent coordinates make J(u⊗v)=W_1(u)W_2(v) an isometry from the *unsymmetrized* tensor product, with no factor two. Left sums give a tensor tau representing X_T. If P projects onto the finite observation span, conditional expectation equals J((P⊗P)tau). The minimum error is ||tau-(P⊗P)tau||, and arbitrary nonlinear estimators have at least that error by conditional-expectation Pythagoras.

3. **Exact covariance bumps.** With the reader's Fourier convention, u_h=sqrt(D_H)|xi|^(H+1/2)conjugate(hat h)/(2pi) satisfies <K_t,u_h>=h(t)-h(0). The conjugate is essential. The zero extensions of f,g have zero traces through order two, belong to W^(3,1), and obey |hat r|<=min(||r||_1,||r'''||_1|xi|^(-3)). This gives both absolute Fourier inversion and the needed weighted L² membership. Scaled cell bumps r_j(t)=Delta^H r(t/Delta-j), Delta=T/n, vanish at **all** observations and belong exactly to the orthogonal complement of the observation span.

4. **Uniform upper Gram bound.** Scaling cancels Delta in their Gram matrices. Nonnegative periodization and Parseval give Gram(r_j)<=M_r I, M_r=D_H Pbar_r/(2pi), using the odd-series bound 1+1/[2(5-alpha)]. This is an upper Bessel bound for translated covariance bumps; it is not the false lower increment coercivity in the rough regime. Integer shifts explain the uniform-grid restriction.

5. **Positive deterministic pairing.** Let w=sum_j u_(f_j)⊗u_(g_j). Fixed-n left sums give <tau,w>=sum_j integral f_j g_j'=n a Delta^(2H)>0. This passage uses ordinary deterministic Riemann sums and L² continuity, with no joint m,n limit. If A,C are the two real PSD Gram matrices, ||w||²=tr(AC)<=nM_fM_g. This permits signed off-diagonal covariances and noncommuting matrices, and does not suppose different cells are independent. Duality yields exactly the stated c_H T^(2H)n^(1/2-2H).

Finite sums and the observation vector have the same joint law in any original standard fBm model; the L² limit preserves that joint law. Every observation-measurable estimator is a Borel function of the finite observation vector up to null sets. Thus the use of auxiliary isonormal directions does not assume those directions are path-measurable in the original model.

These steps establish the whole published central claim, rather than a conditional replacement that assumes an unproved lower-rate hypothesis. The imported canonical-area existence theorem is an established input, verified below from an actual primary body.

## Primary dependency and version check

The fresh author-institution journal-formatted copy of Neuenkirch–Tindel–Unterberger, *Discretizing the fractional Lévy area*, SPA 120 (2010), 223–254, is 1,211,802 bytes, SHA256 `3f7467eea58ebf6998981bf0337a579f45ad1db1c544273eb955507fe2e55c68`, from the [Purdue author publication link](https://www.math.purdue.edu/~stindel/publication/papers-online/discretize-levy-area.pdf). I checked the independent standard fBm assumptions and H∈(1/4,1) setup; Proposition 6, printed p229, supplies L^p analytic first/second-level convergence and Chen's identity; Remark 10, p230, identifies the linear-interpolation construction; Theorem 2, p226, concerns the actual trapezoid/polygonal integral, and its full proof, pp237–240, was read. Relevant construction pages were rendered and viewed. Publisher-delivered byte identity is not claimed.

The independent proof above only needs canonical existence and obtains the left-sum interface itself. It also checks the manuscript's coarse separated-cell covariance bound from the primary off-diagonal integral. Same-cell and adjacent-cell terms are handled by finite second moment and Cauchy–Schwarz, avoiding invalid singular-kernel integration across a diagonal.

The separate pinned [arXiv:0902.0497v1](https://arxiv.org/pdf/0902.0497v1) is 424,962 bytes, SHA256 `de4d91bff1cde45c02298d9f7f49f34790b6c4043232eb6ef5da999af3128ebf`. Its equation (26), p11, gives c_2>=H²(2H-1)²3^(4H-4)/4>0 for H≠1/2. The 2(m-2) lag-two pairs therefore survive after normalization by m^(1-4H). This contradicts that version's equation (27), p12, discarding every lag beyond one as little-o at that scale. The journal-formatted copy instead retains all fixed positive lags, with near lags through log n in equation (29) and only the tail beyond log n discarded in equation (30). I independently confirmed this precise version boundary. No broad journal-error allegation or exact-coefficient certification is justified or made.

## Falsification attempts, edge cases, and finite outputs

`independent_controls.py` was newly written using only Python's standard library and sealed before submitted-code inspection. It independently evaluates the rational pairing a=4/45045, L_f=1/128, L_g=1/630, both third derivatives and endpoint traces, and N_g=113/196 by polynomial factorization and exact quadratic-field reduction. It checks a Brownian RKHS/disjoint-support witness against the exact optimal scale, a signed noncommuting trace example, and the rough all-ones increment countercontrol. Its normal and optimized outputs agree exactly. These are finite controls supporting the written proof, not an enumeration proof of a universal theorem.

An error in **this review's** original excluded-H=1 comment/output was discovered after the first seal when inspecting the submitted checker: I had written E Q_m²=T^4/4. Direct exact recalculation gives T^4/(4m²). The reader is correct. Original sealed artifacts remain unchanged, with an explicit correction and new exact control in `INDEPENDENT_DERIVATION_ADDENDUM.md`, `endpoint_correction.py`, and `endpoint_correction_output.json`. The excluded endpoint still refutes extension of a positive lower bound because paths are linear and X_T=B_T^1B_T^2/2 is observed; D_H also diverges. The correction tends to zero there. All open-interval central proof steps and polynomial constants are unaffected.

Other boundary attempts:

- n=1 is covered by the same positive pairing, with no asymptotic interpolation. T>0 enters with the correct T^(2H) scale.
- At H=1/2, the conditional optimum is T/(2sqrt(n)). The theorem's conservative constant has the correct scale; the submitted finite float calculation gives c_(1/2)≈0.00093314, safely below 1/2. No sharpness is claimed.
- At H=3/4, the Q_m bound is O(T³m^(-2)(1+log m)); it still vanishes. No missing logarithm affects the target rate.
- At H=1/4, the Q_m diagonal is T/4 and this bridge does not tend to zero. That demonstrates failure of this interface at the excluded endpoint, not a claim about every renormalized or noncanonical area construction.
- At H<1/2, all-ones increment coefficients give variance/n=n^(2H-1)→0. An increment lower-coercivity shortcut would fail; the actual proof does not use it.
- Perfectly correlated components can make area recoverable from endpoints, so independence is essential. Nonuniform/adaptive and unequal-H models remain outside scope.
- The halved antisymmetric area equals X_T-B_T^1B_T^2/2 and has the same conditional residual because the product is observed. The unhalved difference doubles the residual. The proof uses X_T without silently changing normalization.

After complete static inspection, only `scripts/check.py`, its path-policy dependency, and its original finite checker were selected for execution. A byte-identical copy of the whole 225-member package was placed under this review's quarantine. The wrapper was run in normal and optimized modes with fresh outputs outside the quarantine package. Both returned code 0, empty stderr, and identical non-UTC original-checker results across normal/optimized modes; all quarantine files remained unchanged. Each run explicitly validated 115 exact nonfloat leaves, 34 exact float inputs, 25 derived-relative float values and 84 covariance-absolute values. Deliberate removal of Fourier conjugation, removal of the journal tail-cutoff marker, and replacement of the area pairing by zero were all rejected in both modes. Those lexical/schema guards are diagnostic controls, not independent mathematical proofs. Float envelopes are not interval arithmetic.

Actual receipts and outputs are preserved under `runs/`, with `runs/EXECUTION_RECEIPT.json` and `quarantine_copy_receipt.json`. No builder, installer, full historical runner, source-overwriting command, release, or external service action was executed. The original finite checker SHA256 is `444a7a29a35b29346f55ceb7ff33ee474f3ace8db11b76076485bb937c0910f1`.

## Attribution, limits, and follow-up

The exact target and vector observations match Neuenkirch's complete 2012 Oberwolfach contribution, printed pp2524–2525. That contribution supplies the historical conjecture and records the Brownian optimum; it is not evidence of worldwide current openness. The actual 14 July 2015 Neuenkirch–Shalaiko author mathematical text, including Theorem 1 and its lower-bound proof, restricts the matching normalized positive liminf/finite limsup to H>1/2. Theorem 3.3 of Shalaiko's primary thesis confirms that scope. The author-upload text is accessible as public HTML transcription; direct PDF access was blocked and identity with publisher bytes is unverified. The 2009 Dagstuhl item is a primary announcement of the smooth result, not a replacement proof.

Wu–Xiao's full Theorem 2.1 proof, author pp5–6, and Xiao's Theorem 3.1 with its stated proof, printed pp174–175, show clear Fourier bump/Hilbert conditional-projection antecedents. They should be credited, while their one-point/first-chaos conditional-variance estimates do not by themselves establish this paper's mixed quadratic-area pairing. I make no firstness, full novelty, general-method novelty, or worldwide current-open claim. Dickinson's inaccessible complete method bodies and Jackowski's incomplete access do not justify excluding broader prior implications. Those are attribution/access limits, not an unresolved step in the explicit analytic inequality proved here.

**Follow-up: null.** No generic extension or unverified open problem is proposed. The present scope and primary comparison do not establish a sufficiently strong case for a substantial new research follow-up.

## Independence, custody, and final accounting

No current sibling scientific report was opened or used. The first sealed derivation/control artifacts preceded submitted certifier inspection. The reader's section 6, historical proof headers, README and SUPPLEMENT contain statements about favorable old AI audits; those were encountered incidentally and are disclosed here, but no old verdict, seal, test PASS, or review narrative serves as mathematical authority. The deposited package's many historical administrative hold/readiness statements are retained as dated history, not treated as current scientific proof or as clearance for a website publication decision.

The strongest verified result is the full published finite-n inequality with its exact stated constant, for independent standard equal-H fBm and all literal quantifiers. **No substantive mathematical defect or remaining central gap was found.** No extended repair was undertaken. Final core source custody matches the initial receipt and archive bytes. Completion estimate: **100% of this analytic review**, not of the parent inventory or publication workflow.
