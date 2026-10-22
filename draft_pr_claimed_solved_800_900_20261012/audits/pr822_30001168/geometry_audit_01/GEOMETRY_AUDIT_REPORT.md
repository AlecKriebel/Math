# PR 822 / 30001168: independent geometric and analytic audit

Decision: **CLEAR** for the mathematical counterexample in the frozen author's PROOF.md. No required mathematical repair was found. Audit completed 2026-10-14 04:49:09 UTC; best-guess completion of this audit is 100%.

Exact supplied original head: `c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c`. Reviewed proof: sibling `source/author/PROOF.md`, 12100 bytes, SHA256 `f95c74037c1d3bc3437c03ea8211fad796e374a93b462697f81a6c3e91a647cc`, matching the author manifest. Root is responsible for Git/PR provenance and exact-head eligibility; this subtask did no Git operation. The original central proof effort remains 1/5; this independent audit did not add an undisclosed proof-search turn.

## Strongest verified result and exact scope

The finite construction with L=10000 produces a smooth strictly positive W on the standard round S3, satisfying integral W^(3/2) dv_g0=2pi^2, for which

    (4a)^(3/2) Tr(exp(-(4a)Y_W))
        > 1106714561/1700054750
        > 13/20,

with a=(2pi^2/V_L)^(2/3). The round scaled trace is below 129/200 at every positive time. Both positive-time maxima exist. This is a strict counterexample to the universal n>=3 comparison, with the advertised threshold separation 1/200.

The independent read-only reconstruction of `queue.py show 30001168` matches review hash `0f73b6392b73ca2e1294a961a56b4729d60540884ab899fd488c8e11885a718c`. The original source was checked directly in the official report, section 9 item (16), Conjecture 1, printed pages 421-422: https://ems.press/content/serial-article-files/46205. Its definition of the weighted operator, normalization, and dimension range match the proof. No hidden geometric assumption was found in the original target. The source's separate n>=4 monotonicity conjecture is not being answered here.

Exact remaining mathematical gap for the negative answer to 30001168: **none identified**. The n>=4 restriction is unaddressed, as explicitly stated by the author; it is not a missing part of a counterexample to a statement quantified over all n>=3. This audit does not establish historical priority, literature completeness, journal publication, or independent human peer review.

## Independence and artifacts

`INDEPENDENT_RECONSTRUCTION.md` was saved at 04:44:17 UTC before any prior audit or second-review verdict was read. Those verdicts remain unread. The reconstruction supplies explicit cap chart formulas, a sign-checked conformal derivation, form-domain arguments, spectral bounds, and maximum attainment. The arithmetic checker was independently authored from those formulas; no candidate executable was run or imported.

`check_geometry_arithmetic.py` was inspected before execution. It passed normally and with Python optimization enabled, with exact fractions and integers in every acceptance comparison. `GEOMETRY_ARITHMETIC_RESULTS.json` preserves all 100 interval enclosures and the checker hash `92ae3ba76f008cd1385b251f53489f670fdd700e8412c26f12f73e29db608811`.

The original PDF was downloaded only to ignored `private_sources/`: 638962 bytes, SHA256 `a3ab668409f786c7c1783150d9f937b2d6e06471a48b76c5721b58a49bf3a683`. Both full relevant pages were rendered and visually inspected, as well as extracted in text. No source excerpt or PDF is being placed in the public findings. All outputs and source downloads were confined to this assigned audit folder. No source file was edited, no remote mutation occurred, and no outside individual was contacted.

## Adversarial checks and exact evidence

| Challenge | Resolution and checkable evidence | Remaining gap |
|---|---|---|
| Is the construction on S3 rather than an infinite cylinder or changed topology? | The twice-punctured round sphere has g0=sech(s)^2(ds^2+g_S2). Both polar ends are filled in the standard stereographic charts. | None. |
| Does abs(s) make u nonsmooth? | u is exactly one on abs(s)<L/2, so it is constant near the only nonsmooth point of abs(s). Flat step-function jets handle q=0 and q=1. | None. |
| Are the compactified caps smooth and strictly positive? | At either pole, g_L=4 exp(L)/(1+exp(L)rho^2)^2 times Euclidean polar metric and W_L=exp(L)(1+rho^2)^2/(1+exp(L)rho^2)^2. Both are smooth positive functions of Cartesian radius squared. Fixed finite L keeps exp(L) finite. | None; no numerical representability assumption is used. |
| Could transition curvature invalidate positivity? | The metric is conformal to the positive round Yamabe operator. q_W(psi)>=3/(4 max W)||psi||^2 supplies a positive spectral gap regardless of local scalar-curvature sign. | None. |
| Are the conformal powers or measure wrong? | Derivation with the positive Laplacian gives Y_h=W^(-5/4)Y0W^(1/4). dv_h=W^(3/2)dv_g0 and unitary U=W^(3/4) yield exactly W^(-1/2)Y0W^(-1/2). Wrong U=W^(1/2) produces powers -3/4 and -1/4 and is rejected by the independent control. | None. |
| Do derivative jumps in the trial functions create a surface penalty? | The sine values vanish at both interfaces. Zero extension of H1_0(D) lies in global H1; weak first derivatives have no delta. A jump in a normal derivative affects H2, not the quadratic form. The form is integrated directly and requires no seam integration by parts. | None. |
| Does min-max have the right direction and account for multiplicities? | The exact k-dimensional form matrix is diagonal with quotients 1/4+(pi j/L)^2. Full ordered closed-manifold lambda_k<=mu_k, so exponentials reverse the order and yield a heat-trace lower bound. No cap decoupling or spectral limiting assertion is used. | None. |
| Is passing to infinitely many trial modes legitimate? | First use finite partial sums. The global operator is positive and its heat trace is finite by smooth ellipticity, or by explicit comparison to the round Laplacian using q_W>=c||grad psi||^2-C||psi||^2. Monotone limits give the infinite inequality. | None. |
| Could cap volume be underestimated? | Integral u^3 per cap <=1+8/(3e^3)<2. The exact independent upper estimate lies in [1.132765519649,1.132765519650], much below two. V_L<=4pi(L+4) uses the correct direction in the trace prefactor. | None. |
| Has normalization changed the target time? | a^(3/2)V_L=2pi^2 and Y_(agL)=a^(-1)Y_gL. Selecting t_star=4a yields the exact identity F_W(t_star)=16pi^2/V_L Tr(exp(-4Y_gL)). V_L>=4pi L proves a<1, so an unscaled time of four cannot be silently substituted. | None. |
| Does the Gaussian sum estimate conceal a limit in L? | The decreasing-function integral comparison holds at the single L=10000 and gives sum exp(-4pi^2k^2/L^2)>=L/(4sqrt(pi))-1. A short-cylinder control cannot establish the target threshold. No L limit is needed. | None. |
| Does the round comparison miss some time, potential, or multiplicity? | The spectrum is j^2-1/4 with multiplicity j^2. Poisson summation handles (0,1]; 100 closed intervals cover [1,2]; each summand is nonincreasing beyond two. The independent interval replay has its largest upper bound in [0.643380136593,0.643380136594], on [1.89,1.90]. | None. |
| Are the inequalities genuinely strict? | The geometric rational lower bound is in [0.650987599664,0.650987599665], giving a margin above 0.65 greater than 0.000987599664. The minimum finite round interval margin below 0.645 exceeds 0.001619863406. Exact fractional comparisons, not the displayed decimal enclosures, determine acceptance. | None. |
| Are literal maxima present, rather than only suprema? | Normalized heat asymptotics give the same zero-time limit sqrt(pi)/4. The constructed value exceeds it; the first round eigenvalue at t=2 exceeds it because 128>pi e^3. Positive spectral gaps force large-time decay to zero. Continuity gives attainment inside positive compact time intervals. | None. |

## Finite versus mathematical obligations and imported dependence

The finite checker certifies the arctangent/Taylor enclosures for constants, the 100 round intervals, the final strict rational separation, and simple power/parameter controls. It does not prove smoothness, operator covariance, the Sobolev extension theorem, min-max, Poisson summation, or heat asymptotics. Those analytic obligations were separately verified in the reconstruction with their hypotheses stated.

Imported standard results are the local conformal transformation identities, the H1_0 zero-extension property on a smooth bounded domain, the spectral min-max theorem for compact elliptic forms, Gaussian Poisson summation, the round harmonics spectrum, and the leading local heat coefficient. The conformal identity is additionally derived algebraically from the local formulas; trace class is supported by an explicit form comparison; the maximum argument uses no assertion of a globally attained optimization over weights. None transfers the central difficulty to an unsupported equivalent conjecture.

No required fixes. Optional expository strengthening would be to display the pole metric coefficient and the explicit positive lower spectral bound, as done in the reconstruction, but the submitted proof already contains the necessary reasoning.
