# Independent analytic review: Intermediate-area cylinders in the principal quadratic stratum

**Verdict: supported at the literal stated mathematical scope.** The full marked point-process limit and every fixed joint compact-window count moment follow from the displayed argument and the exact published geometric interfaces inspected here. No central mathematical gap or required source correction was identified. This is a bounded AI-assisted analytic review, not human peer review, formal certification, an exhaustive priority result or publication clearance.

The actual seven-page reader, SHA256 `ad3a7dcbbcdb9a7c53bd1e63085644434132a556c9a09e8a1c16121073949f02`, and the complete sole TeX, SHA256 `7da26974ef1e8b15922bff398424954874177d20580cf5b0526cd998e34de6b8`, were read in full. All seven rendered reader pages were visually inspected. The source-ready seal is `9197446b4ea1837a688afd7d4492f4248328fe2b162b3c4b8c6aa06b9c3adef9`. This lane froze all 151 current source files before reading; it neither executed deposited programs nor changed the sources, site, shared core, Sheet, UI, Git or any previously sealed assignment.

## Independence and exact claim

The independent reconstruction in `INDEPENDENT_MECHANISM_NOTES.md` was fixed before external primary bodies, package history, sibling/current-root opinions or source-lane conclusions. Its fourteen bindings were sealed at **2026-10-25 06:56:51 UTC**, SHA256 `14b670068cf2198143feb9145266eec0f40b89af068b28c65d6e87591c851ff7`. No sibling/current-root/source scientific review report was read subsequently either. Later messages supplied raw primary paths, identities and acquisition information only. Complete primary bodies were independently hashed, and this lane made its own text extractions and critical-page renders.

The exact ensemble is fixed genus g≥2, principal holomorphic quadratic stratum Q(1^(4g−4)), uniform isomorphism classes of square-tiled half-translation surfaces with at most N squares, all cylinder heights allowed, each maximal horizontal cylinder counted once, and areas divided by total surface area. N→∞ is taken first at each fixed genus, giving ν_g; only then is g→∞ taken. The automorphism-weighted convention gives the same fixed-genus limit. No diagonal N(g), arbitrary-stratum or simultaneous all-direction conclusion is included.

For every deterministic s_g>0 with s_g→0 and g s_g→∞, the target is vague convergence on (0,∞) of Σδ_(X_i/s_g) to PPP(dx/(2x)), together with convergence of every fixed joint ordinary moment for finitely many disjoint compact-window counts. The intensity is locally finite away from zero. The special window [g^(−1/2),2g^(−1/2)] has limiting count Poisson((log2)/2), limiting mean and variance (log2)/2, and limiting void probability 2^(−1/2). The microscopic and macroscopic endpoints are excluded.

## The geometric comparison is justified at the required uniformity

Set n=3g−3, a_j=ζ(2j)/(2j), H(z)=exp(Σa_jz^j), and h_n=[z^n]H. The comparison model chooses a positive ordered composition (j₁,…,j_k) of n with probability (h_n k!)⁻¹∏a_(j_i), then independent Gamma(2j_i,rate1) variables and their normalized vector. This is a previously studied weighted-permutation/assembly law, not a newly introduced enumeration.

The published DL fixed-genus square-tiled theorem and its exact graph mixture identify the full normalized-area law needed here, rather than only its leading ranked components. The principal restriction is consistent with the published statement that nonprincipal lattice counts are negligible in the fixed-genus square-count limit. The OWR account also explicitly states that unweighted and automorphism-weighted limits agree. Unit versus half-unit square conventions rescale the bound N by a fixed factor and do not change normalized area fractions or the iterated limiting ensemble.

For one vertex of genus g−k and k loops, the graph automorphism group has order 2^k k!. DL's actual expansion is

    F_(g,k)(x)=A_(g,k) Σ_(j_i≥1,Σj_i=n) ctilde_(g,k)(j)
                                ∏ x_i^(2j_i−1)/(2j_i)!,
    A_(g,k)=(6g−5−2k)! 2^(3k−3)
                /((g−k)!(3g−3−k)!3^(g−k)).

All terms are positive. Eq.6.1 allows **any fixed C>0** in k≤C log(base genus), uniformly over the allowed degree data. Thus it applies at base genus g−k for k≤k_g=floor((3/5)log(2n)); the changed genus tends to infinity, and this logarithmic cutoff remains within a fixed-C range. The actual marked-point uniformity is not inferred from a weaker fixed-k statement.

Changing width w_i to area x_i=m_iw_i contributes m_i^(−2j_i) to the monomial measure. Summing all integer heights produces ζ(2j_i). Integrating on the unit simplex contributes ∏Γ(2j_i)/Γ(2n). Hence (2j_i)! cancels to 1/(2j_i), giving the composition weights above and the exact conditional Dirichlet(2j₁,…,2j_k) kernel. The graph weight adds D_(g,k)=A_(g,k)/2^k. Direct cancellation gives

    D_(g,k+1)/D_(g,k)
     =12(g−k)(3g−3−k)/((6g−5−2k)(6g−6−2k)).

Its logarithm is O((k+1)/g) at the logarithmic cutoff, so D_(g,k)/D_(g,1)=1+O((log g)²/g), uniformly. Combining this with the uniform ctilde estimate and normalizing the positive weights gives a relative density 1+o(1) on the latent good events: one vertex and K≤k_g geometrically, and K≤k_g in the model. The common Dirichlet kernel preserves that bound after marking and forgetting latent labels.

The actual DGZZ Theorem1.12 applies to the same geometric total-count law for |t|<8/7. At t=11/10 it gives E t^K=O(n^((t−1)/2)). Markov yields

    P(K>k_g)=O(n^(−η)),
    η=(3/5)log(11/10)−1/20>1/220.

The strict inequality follows already from log(11/10)>1/11. Summing the same exponential Markov tail after a sufficiently large multiple of log n gives E K^r=O((log n)^r) for every fixed r. This uses a generating-function bound, not just concentration of K/log n.

DGZZ Theorem5.2's first relative-volume estimate is exactly O((log g)^25 g^(−1)2^k), uniformly for k≤log g/log(9/4). The cutoff lies in that range for all sufficiently large g, and (3/5)log2<1. Consequently the multivertex contribution below the cutoff and the large-K contribution above it together have polynomially small probability. The model has the same cutoff and count-moment bounds by the coefficient estimate below.

Thus the full multiset laws have total variation o(1). More strongly, their conditional good laws have a uniform relative-density error ε_g→0, and in either law

    E[K^r;bad]≤(E K^(2r))^(1/2)P(bad)^(1/2)=o(1).

These stronger statements are what make the unbounded-moment transfer valid.

## Complete intermediate-scale probability argument

### Assembly coefficients and unmarked counts

Summing ordered compositions with weight 1/k! gives the count-vector law h_n⁻¹∏a_j^(C_j)/C_j! under Σj C_j=n, equivalently independent Poisson(a_j) variables conditioned on total size n. Shifting selected component counts gives the exact factorial identity

    E∏(C_j)_(r_j)=(h_(n−R)/h_n)∏a_j^(r_j),
    R=Σj r_j≤n,

and zero for R>n. This positive-weight identity can be derived directly without invoking a combinatorial theorem for integer numbers of objects.

The zeta expansion factors H=(1−z)^(−1/2)B(z), with B=∏_(m≥2)(1−z/m²)^(−1/2) analytic in |z|<4. The telescoping product at1 gives B(1)=√2. Convolution with central-binomial coefficients gives

    h_n∼√(2/π)n^(−1/2),
    c₁(n+1)^(−1/2)≤h_n≤c₂(n+1)^(−1/2),
    h_(n−R)/h_n≤C√((n+1)/(n−R+1)).

The ratio tends uniformly to one for 0≤R≤R_n=o(n). For every fixed t>0 the same convolution with exponent t/2 gives [z^n]H^t∼2^(t/2)n^(t/2−1)/Γ(t/2), establishing the model's count generating-function bound.

Write q=n s_g. The hypotheses are exactly q→∞ and q=o(n). For fixed 0<a<b<∞,

    Σ_(a q≤j≤b q)a_j→(1/2)log(b/a).

In each fixed joint factorial moment of compact q-scale window counts, the total selected size is O(q)=o(n), so the coefficient ratio is uniformly 1+o(1). The resulting factorial moments are those of independent Poisson variables. Poisson moment determinacy gives their joint law; bounded expected counts on each compact interval give local tightness and the unmarked vague point-process limit.

The unmarked conclusion is prior assembly theory as credited in the paper. For Poisson(a_j), the uniform logarithmic condition in ABT holds with parameter1/2: j E Z_j=ζ(2j)/2, the one-component probability differs from1/2 by O(1/j), and the probabilities of l≥2 are bounded by O(1/j) times factorially summable constants. ABT Theorem3.1 covers all cutoffs b_n=o(n), not only a fixed power rate. The explicit factorial proof above supplies an independent route in this model.

### Gamma marking requires no additional rate condition

Let Z_n=Σδ_(Y_i/(2q)). For compactly supported nonnegative Lipschitz f, supported in [a,b], the expected absolute difference from the unmarked test integral is at most

    Σ_(j=1)^n a_j(h_(n−j)/h_n)
                       E|f(Y_j/(2q))−f(j/q)|.

For a q/2≤j≤2b q, the coefficient ratio is bounded and the mean absolute Gamma displacement is at most √(2j)/(2q). Summing a_j≤C/j gives O(q^(−1/2)). For j<a q/2, the unmarked test is zero and

    P(Y_j≥2a q)≤e^(−a q)2^(2j)
                  ≤e^(−a(1−log2)q).

Its weighted sum is O(log(q+2)e^(−c_aq)). For j>2b q,

    P(Y_j≤2b q)≤e^(b q)(3/2)^(−2j)≤e^(−c j),
    c=2log(3/2)−1/2>0.

The coefficient ratio is bounded through n/2 and at most C√n beyond; both exponential sums vanish. Thus this expected-sum comparison tends to zero for **every** q→∞, q=o(n). It avoids a union bound over K=O(log n) marks and therefore avoids an unsupported q≫log n restriction. The Lipschitz Laplace-functional inequality transfers vague convergence to Z_n.

For every composition, T=ΣY_i has exactly Gamma(2n,1) distribution, since Σ2j_i=2n=6g−6. Hence T/(2n)→1 in probability. Since

    (Y_i/T)/s_g=(Y_i/(2q))(2n/T),

Slutsky and continuity of positive dilation in the vague topology give the normalized model limit. Independence of T and Z_n is not required.

### All fixed joint moments are uniformly integrable

Let p_(n,j)=P(Y_j/(2q)∈[a,b]). The same three regions give Σa_jp_(n,j)≤C_(a,b). Independent marking of the distinct selected components yields

    E(M_n)_r=Σ_(j₁+…+j_r≤n)
                 (h_(n−Σj_i)/h_n)∏a_(j_i)p_(n,j_i).

Repeated sizes are handled by falling factorial selection. If Σj_i≤n/2, the coefficient ratio is bounded and the sum is bounded by a fixed multiple of C_(a,b)^r. Otherwise at least one j_i≥n/(2r), whose mark has lower-tail probability e^(−c_r n), because q=o(n). The remaining weight sums are at most O(log n), and the largest possible ratio is O(√n). This makes the entire remaining contribution o(1), including the residual h₀ boundary. All fixed ordinary moments of M_n are bounded; the argument also covers a finite union of compact intervals.

On 1/2≤T/(2n)≤2, a normalized count in [a,b] is bounded by the marked count in [a/2,2b]. The complementary probability is O(e^(−c n)) by Gamma Chernoff bounds. Since K≤n, its contribution to the r-th moment is at most n^rO(e^(−c n)). All normalized compact-window moments are therefore uniformly bounded. Applying a higher moment gives uniform integrability of every fixed power. Mixed powers are bounded by a power of the count on the finite union. The limiting process has no atoms at fixed endpoints, so joint count convergence upgrades to convergence of every fixed joint ordinary moment.

### Transfer to geometry and the order of limits

Total variation transfers bounded point-process observations under any deterministic genus-dependent rescaling. For unbounded count moments, use the good-event relative density and the separate o(1) bad-event K^r estimate. The model compact-window expectation is O(1); hence the relative o(1) error is multiplied by O(1), rather than a potentially diverging power of log n. Removing either cutoff costs o(1). This proves the geometric moment conclusion without an invalid total-variation-to-expectation inference.

At fixed sufficiently large genus the window endpoints lie below1. Mixture components with at least two cylinders have continuous simplex densities; the one-cylinder atom is at1. Thus the fixed-genus N→∞ convergence passes to these counts at null boundaries. The deterministic bound K≤3g−3 gives convergence of their fixed moments at that fixed genus. Taking g→∞ only afterward proves the stated iterated result. Nothing supplies a rate allowing diagonal N(g) sampling.

## Primary interfaces, attribution and honest limits

The full primary/read ledger gives exact paths, hashes and reading extents. Existing ignored primary PDFs were bound in place, including the68MB slide deck, rather than duplicated. Own extractions and renders remain wholly ignored. This review checked the specified interfaces; it did not read all39 DL pages, all102 DGZZ pages, the whole thesis or every slide.

| Actual body and location inspected | Interface outcome |
|---|---|
| Published DL, Theorem1.4; §§2.3,3; Eq6.1 and Lemma6.4/proof | Exact surface law, graph-mixture density, height summation, corrected graph automorphism bookkeeping, uniform logarithmic coefficient range and displayed prefactor match. |
| Published DGZZ, §§1.2,2.1–2.5 and relevant selected statements; Theorems1.7,1.12,5.2; Lemma3.6 and one-vertex proof | Same cylinder-count law and fixed-genus sampling, negligible nonprincipal contribution, exact2^k k!, pre-existing weighted permutation measure, fixed t generating-function control and uniform low-k relative volume bound match. |
| AT author arXiv retyping, physical pp.49–50, Lemma5/(126); journal reprint metadata through web PDF | Exact selected-component identity matches its positive-weight specialization. The local retained body is the2013 arXiv retyping, kept distinct from the1994 journal reprint. The identity is independently derived here. |
| ABT actual published author-hosted PDF through web, pp.1623 and1630 | Uniform logarithmic hypotheses and Theorem3.1 cover every b_n=o(n). Local ordinary retrieval returned403; no local PDF body is falsely claimed. This theorem is an antecedent, since the unmarked step has its own proof. |
| Official OWR2024 report, printed2384–2387 | Principal ensemble, N-first order, automorphism-weight footnote, exact highlighted window and separate diagonal Problem3 match. |
| Liu2022 thesis, printed21–23; actual Durham2025 slides26,193–195 | Microscopic all-multiplicity announcement and normalization in the thesis are distinct from the primitive conjectural slide version. They are credited prior intellectual contributions, not silently treated as a proved growing-window theorem. |

The OWR microscopic statement prints4g−4; the thesis uses6g−6, and the exact monomial/Gamma calculation has total6g−6. These yield different fixed microscopic laws and are not identified. The current proof uses its exact geometric normalization and makes no claim to correct the short report. A fixed microscopic window theorem and the1/(2x) tail of its limiting density do not by themselves justify a window growing with genus; uniformity is supplied separately here.

The full announced small-components manuscript was not obtained or read. Aggarwal's deep underlying intersection-number/volume results, Mirzakhani and the other geometric counting dependencies were not independently re-proved in this lane; the exact forms used were checked in published DL/DGZZ. The bounded source reading does not establish absence of an earlier full intermediate theorem, worldwide current openness or first priority. The paper already credits the weighted model, classical unmarked approximation and microscopic announcements and retains the unavailable-project uncertainty. I identified no mandatory attribution correction on the bodies read, while withholding priority/publication clearance.

## Meaningful exact controls and completion

`independent_exact_checks.py` is newly written code with standard-library exact rational arithmetic. It checks seven generic positive rational-weight composition normalizations,147 selected-component identities,21 independently marked count-PGF identities, and5913 separately enumerated labelled permutations to verify the cycle factor. It checks693 simplex mass/moment identities by polynomial Beta integration, including the2j factorial cancellation and a rejected halved-shape control. It checks147 exact prefactor ratios and certifies the cutoff/tail exponent inequalities using rational logarithm-series lower/upper bounds. The incorrect unconditioned-Poisson shortcut is rejected. These finite checks validate algebra/transcription controls, not all-genus geometry, arbitrary-rate limits or priority.

The final custody checker rehashes all151 source bindings, all14 immutable early bindings, the complete externally retained primary bodies, own ignored extractions/renders, final manifest and final seal. It recomputes only this lane's newly authored exact controls without overwriting the recorded result. No deposited or foreign verification program is executed, and no network access is used by that checker.

Completion is **100% of the bounded independent analytic assignment**. The strongest supported statement is exactly the specified intermediate-scale marked process and every fixed joint compact-window moment in the N-first principal quadratic ensemble. No remaining central mathematical gap or requested source repair is identified. Root retains adversarial convergence, editorial/Sheet/publication authority, and the broader research program remains outside this completion claim.
