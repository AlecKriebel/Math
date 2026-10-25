# Independent adversarial mathematical review — Zenodo 23203100

Completed 2026-10-25 UTC. Reviewer assignment: GPT-6.1 Sol, Ultra; independent adversarial family, no descendants. Completion estimate for this assigned review: **100%**. This is an AI mathematical review, not conventional human peer review, a novelty determination, or publication clearance.

**Finding:** No substantive defect was found in the downstream capacity reduction, the zero-energy secrecy obstruction, or the repaired generated-secret accounting under the manuscript's explicit operational conventions. The strongest global capacity equalities established by this review are **conditional on the sharp finite-energy multimode vacuum entropy bound**. This review does not independently establish the entire upstream EPnI proof, and does not turn an imported theorem label, historical audit report, or numerical check into such a proof.

## Exact object and custody

The object is Alec Kriebel, *Pure-loss bosonic dynamic capacities: EPnI consequences and consumed-key secrecy accounting*, Zenodo record 23203100, DOI 10.5281/zenodo.23203100, catalogue row 78. Zenodo supplies no version field; no version label is invented. The declared publication date is 2026-10-06; the record creation time is 2026-10-07T04:42:47.312983Z. Those are different metadata facts.

Reviewed PDF SHA-256:

`490c6d4d78eb4c2ae829d06f31df1ed1ace955174acec87279f5d5eb8dee8581`

Reviewed ZIP SHA-256:

`e9f9adb0dca6f7776b215672ab97b7f8922aae415d2d9f73afd631259ca40fab`

I read the entire actual seven-page PDF's freshly extracted text and the entire submitted `manuscript/main.tex`, checked all seven rendered pages in the contact sheet, and inspected pages 4–5 individually at readable size. Fresh PDF extraction is byte-identical to the intake text. The TeX SHA-256 is `eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab`.

The ZIP has **40 regular members**: 39 inventory entries plus `SOURCE_INVENTORY.json`. I independently matched every inventory hash and byte count, every member against its extracted copy, and the exact member-name set. There are no hidden members, symlinks, directory members, nested archives, or additional PDF readers. All 92 source files, including all 16 cached raw primary PDF/text pairs, have identical before/after hashes. See `custody_before.json` and `custody_after.json`.

Archived review, priority, verdict, acceptance and route-report bodies were not used as evidence. Source receipt/ledger metadata was used for source identification and locators. Historical summary prose embedded in necessary mathematical support was disregarded; its concrete proofs and equations were checked afresh. The submitted programs located under old review-named directories were read as code, not as inherited verdicts. No original source was edited, imported, executed, rebuilt or recompiled.

## Models and quantifiers actually checked

The channel is the one-mode pure-loss channel with independent vacuum environment, identical across uses, transmissivity **eta in [1/2,1]**, and finite mean input number N. The photon budget is averaged over classical messages, encoder randomness and consumed key; for quantum communication it applies to the maximally mixed logical input, equivalently half of a maximally entangled reference state. Arbitrary entanglement across physical channel uses is permitted. There is no per-codeword or peak-energy guarantee, no free feedback, no two-way assistance, and no optical energy charge on noiseless side resources.

All gross input/output resource registers have logarithmic dimension O(n), at fixed finite gross rates. Reliability and secrecy errors vanish along the coding sequence. The quantum reliability interface is the full joint trace criterion of QDC Eq. (4), including classical correlations, entanglement transmission and generated ebits. The private source's reliability interface is PDC Eq. (13). The repaired secrecy criterion is the manuscript's Eq. (11): uniform joint generated W=(M,T_A) is trace-close to independent of X=(K,L) and Eve's channel environment, while V=(J,S_B) is consumed and may correlate with W and X. Eve is not separately handed the consumed key. Generated communication messages are fresh and initially independent of the preshared key; arbitrary public common randomness is not counted as communication.

These restrictions do real work. Finite-register conditional-entropy continuity gives I(W;XE^n)=o(n) from trace secrecy without bounding Eve's dimension. A superlinear gross-secret register would invalidate that inference: revealing a 2^(n^2)-valued uniform secret with probability 1/n gives vanishing trace error but mutual information n. The review includes that exact negative control. Net zero consumption does not promise zero gross seed input; the finite catalytic convention allows the seed to be charged and later returned/generated. No catalyst-elimination claim beyond that convention is required.

## Unconditional claims verified

**Literal-model refutation, Proposition 4.** At N=0 positivity of the number operator forces every positive-weight input, and therefore Bob's physical output, to be vacuum. Under the literal PDC secrecy target, uniform W is independent of Bob's entire nonvacuum input LV. Any decoder succeeds with probability at most 1/d_W in the ideal comparison state. Trace contraction and reliability therefore give

    1 <= 1/d_W + (epsilon_sec+epsilon_rel)/2.

If d_W>=2 the error sum is at least one. Thus every sufficiently large block in a vanishing-error sequence has d_W=1, regardless of consumed resources. This attacks the literal operational capacity theorem itself, not just a particular code.

For d-symbol OTP, with independent uniform M,S and L=M+S mod d, generated-message secrecy is exact. Its distance to an independent uniform **pair** (M,S) times any comparison public distribution is exactly 2(1-1/d). The arbitrary-marginal minimization is proved by summing the d valid and d^2-d invalid pairs within each public block. The displayed N=0 private cone contains (-1,1,-1), so that cone cannot describe the literal model. The primary source actually prints the consumed registers in its secrecy target; this is not an inferred interpretation. The optimization erratum does not change that target.

**Corrected converse.** I independently derived all three gross-rate information bounds. The first uses initial I(KM;S_B)=0 while allowing encoder-generated L,J to depend on messages. The second has the exact remainder

    I(W;V|X)-I(V;B|X)+I(V;E|WX),

whose positive terms sum to I(V;WE|X)<=H(V|X), since V is classical. The third has the exact remainder

    -I(LV;B)+I(KW;LV)+I(V;E|KWL),

whose latter terms equal I(KW;L)+I(V;KWE|L)<=H(L)+H(V). Charging the consumed register dimensions gives the claimed net-rate entropic outer region. No inference of joint secrecy of WV is made. Deliberately removing the consumed-key term or its cost fails exact OTP witnesses.

Spectral refinement is valid for degradable channels: the extra private-information difference is nonnegative by data processing, and pure conditional BE states have equal B,E entropies. The first mutual information increases by I(Z;B|XY)>=0. This reduces the three bounds to at most H(bar B), H(B|X)-H(E|X), H(bar B)-H(E|X), for the refined ensemble. No Gaussian optimizer conclusion is used at this step.

**Achievable regions and cost.** The finite cq direct proof was checked through its typical-projector estimates, Hayashi–Nagaoka packing, independent key-indexed satellite table, Hilbert–Schmidt covering estimate and gentle outer decoding. Bob knows the key and packs only private messages; Eve averages that unknown key. Covering requires key rate above I(Y;E|X), private packing a rate below I(Y;B|X). Noncommuting sampled matrices cause no missing cross terms in the variance estimate. Average uniform-source secrecy needs no union over exponentially many messages. The supplement first uses a target marginal depending on the public word; contraction and the triangle inequality give the actual-marginal Eq. (11) with at most a factor two in the error.

The original CEF rho-like expected-input property, including its Appendix A/B expurgation argument, supports the quantum average-cost selection for the operational maximally mixed logical input. After fixing a finite cutoff, the cost operator is bounded and trace-closeness controls cost. Strict N'<N slack ensures that the positive-probability good-cost event intersects the high-probability good-error/secrecy event. An exact adversarial control shows that equality of expected cost to N alone would not suffice for that selection; the manuscript uses a strict margin. The limits are ordered correctly: finite ensemble/cutoff and energy slack fixed; n tends to infinity; approximants converge; N' rises to N; closure. No uncontrolled unbounded-observable continuity estimate or postselection on unknown quantum data appears.

The quantum and repaired-private displayed unions are therefore unconditional **inner bounds**, using the cited finite-dimensional coding theorems plus the checked approximation argument. Their entropic outer regions are unconditional. The two zero-energy conversion cones are exact. At eta=1, both full regions are exact without EPnI because Eve is vacuum. At eta=1/2, the full repaired-private region is exact without EPnI: lambda=0 dominates, and degradability gives P+S<=0.

## Conditional sharp capacity claims verified

The precise needed external premise is, for every finite n, every finite-energy n-mode state rho, and t in [0,1],

    H(L_t^(tensor n)(rho))/n >= g(t g^{-1}(H(rho)/n)).

The first input may be entangled internally; only the vacuum port must be independent. The pinned OpenAI Theorem 1.1 and Corollary 1.2 state a sufficient premise with exactly these hypotheses, in natural-log units. Dividing both entropy and g by ln 2 gives the correct bit-rate form. Its Lemma 2.2 supplies the finite-energy cutoff/entropy-continuity proof, which was read and checked. Neither a one-mode result, a Gaussian-only result, nor the weaker quantum EPI implies the required all-block sharp inequality.

The scalar function f_t=g(t g^{-1}) is convex for t<=1 and concave for t>=1; the derivative sign follows from the strictly decreasing function (u+1)ln(1+1/u). The reference calculation in `FRESH_PROOFS.md` includes the complete positive denominator. Setting s=H(B|X)/n and using the thermal maximum chooses **one common lambda** with s=g(eta lambda N). Degradation and Jensen then lower-bound H(E|X)/n by g((1-eta)lambda N); applying the eta inequality and Jensen before inversion upper-bounds H(input|X)/n by g(lambda N). Integrability follows from finite average energy and concavity of the thermal maximum.

Those simultaneous bounds prove all three CQE photon inequalities and all three repaired-RPS photon inequalities. They apply to each finite block before regularization, including entangled inputs. Thus **conditional on the stated sharp premise**, Theorems 3 and 5 give the exact displayed regions for the stated energy/resource/security models. The generic capacity theorems and corrected operational proof, rather than an unsupported generic additivity or optimization assertion, supply the interface.

The remaining dependency is exact: this review did **not** independently establish Sections 3–6 of the 32-page upstream EPnI argument or execute its Lean kernel build/axiom report. It did not read historical EPnI audit reports as substitutes. An unconditional assertion of those global equalities cannot be attributed to this review alone. This is a stated dependency boundary, not a demonstrated counterexample to EPnI.

## Boundary, orthant and closure attacks

Both noiseless resource cones were inverted algebraically, not merely tested on generators. For a quantum displacement (c,q,e), the teleportation/superdense/distribution coefficients are -(c+q+e)/2, -(q+e)/2, -(c+2q)/2. For a private displacement (r,p,s), the OTP/private-to-public/private-to-key coefficients are -(r+p+s), -(p+s), -(r+p). Nonnegativity is exactly the respective three facet inequalities. This establishes the translated cone in every sign orthant, including resource discarding.

The father corners saturate the correct three facets; no factor of two or entanglement/key sign error was found. At N=0, the exact vacuum and conversion arguments avoid inversion or division by zero. At lambda=0/1 zero-variance Gaussian components are point masses. At eta=1/2, Bob and Eve entropies coincide; at eta=1, Eve is vacuum and lambda=1 dominates. Eta=0 is outside both main capacity theorems: their degrading-parameter proof must not be extended through division by eta. The paper's brief excluded confidential-broadcast remark supplies no additional theorem being certified here.

Converse cutoffs can be chosen separately for each fixed block and finite resource dimensions, making all relevant trace and entropy errors arbitrarily small before the coding limit. There is no fixed-cutoff uniformity claim as n grows. On fixed N and eta, the sharing parameter is compact; convergent rate triples have a convergent parameter subsequence, proving the unbounded-rate union closed. In the entropy parameter s, the facet right sides are concave, proving convexity by hypograph projection. No interchange with an infinite-energy limit or a uniform eta-to-one limit is used.

Two minor wording points are non-substantive: “increasing” at t=0 in Lemma 2 means nondecreasing; and the first refinement bound gains I(Z;B|XY), while the last two gain the displayed B-minus-E difference. The mathematical inequalities needed in the proof remain valid. No source repair was made.

## Independent checks, supporting reproduction and limits

`FRESH_PROOFS.md`, `fresh_controls.py` and `fresh_controls_results.json` were sealed in `FRESH_ARTIFACT_SEAL.json` **before any submitted-code reproduction**. The independent checks give zero formal entropy-polynomial residuals, 210 exact OTP comparisons over arbitrary rational public marginals, exact cone inverses at 2,197 rational triples per cone, and 10,000 exact GF(2)-linear classical remainder witnesses. Mutation controls reject omitted consumed-key terms/costs, a flipped OTP key sign, conflating generated-only and literal secrecy, eliminating strict cost slack and allowing superlinear gross registers. These tests supplement the universal derivations; they do not validate EPnI or replace quantum data processing.

All **five** submitted Python programs were read statically before execution/import of any of them. The package builder writes a publication folder and reads manuscript/source material; it was not run. The Lean harness exports Git objects and creates a build project; it was not run. The interpolation sampler tests a separate upstream ingredient numerically; it was not run and cannot certify a universal theorem. Only `verify_certificates.py` and `symbolic_checks.py` were reproduced, using byte-identical copies inside this review's quarantine after the fresh seal. Both exited zero. Their original source paths were never executed/imported. `CODE_REVIEW.json` records hashes and exact execution locations; all emitted files remained in this review folder. These author reproductions only corroborate the already-sealed proof checks.

`PRIMARY_READ_LEDGER.json` records actual raw-primary body extents, not a blanket assertion that downloaded PDFs were fully read. It includes the pinned EPnI statements/cutoff proof, both early WHG versions, final WHG formulation, QDC operational theorem and full catalytic converse, PDC literal condition and converse/refinement, De Palma's exact conditional premise, CEF's input-distribution proof, PEPF's consumed-key target, HLB's generated-message target, Devetak's code mechanism, Hayashi–Nagaoka's complete operator-inequality proof, Winter's energy assumptions, and the joint erratum's scope. All 16 primary PDF hashes were independently checked against transport receipts.

The review's strongest unconditional and conditional results, exact gap, source custody and artifact hashes are machine-readable in `verdict.json` and the final `ARTIFACT_SEAL.json`. No Git, spreadsheet, website, deployment, release or external communication action was taken by this reviewer.
