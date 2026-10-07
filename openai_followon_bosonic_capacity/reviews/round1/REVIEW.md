# Independent complete-package adversarial review, round 1

Reviewer: `/root/complete_review_one`. Recorded 2026-10-07T04:34:20.335231+00:00.
This is an automated independent review, not conventional human peer review.

## Verdict on the frozen candidate

**No known substantive mathematical, priority-framing or package issue remains in the exact frozen candidate inspected below.** The initial source-kit reproducibility defect was repaired and independently retested. A NEW complete-package reviewer must still inspect this candidate from scratch before publication; this report does not waive that requirement.

The publication is defensible as the explicitly titled **EPnI consequence, literal-model counterexample and generated-secret repair** note. It is **not** an affirmative proof of both unchanged original target regions. The original private assertion is refuted at zero energy. The paper does not determine the entire capacity region of the unusually restrictive literal model for every positive N, and it does not claim to do so. Its positive private theorem is for the expressly changed GEN model. This distinction must survive every final status report and any assessment of the original persistent objective.

The external analytical EPnI theorem remains attributed to OpenAI and is necessary for the positive entropy/capacity conclusions. I read its analytical proof independently and found no substantive gap. This review did not reproduce its Lean build and is not a machine-verification certificate.

## Exact inspected version

| Artifact | SHA-256 |
|---|---|
| manuscript/main.tex | `eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab` |
| publication/paper.pdf | `490c6d4d78eb4c2ae829d06f31df1ed1ace955174acec87279f5d5eb8dee8581` |
| publication/zenodo-upload-kit.zip | `26ed72c580b59f6bbee132efc75f81466b5a60005fc964ce3dc9e3b082e3309b` |
| zenodo-deposit.json | `28f17d3562a835e8f683b71955f63eb6dd771746b0ceb3e15d000d1e9b9960be` |

The full inventory of the 39 source files and both upload byte sizes/SHA-256/MD5 values is in PACKAGE_AUDIT.json and the root publication/PACKAGE_INVENTORY.json. I independently checked that the 40-entry archive contains exactly those 39 sources plus SOURCE_INVENTORY.json; each member matches both its inventory hash and the current owned source bytes. No extra archive entries, unsafe paths or duplicate member names appeared.

## Findings, response and verification

1. **Repaired package reproducibility failure.** The initial inspected source kit `c2bd8b4b7ce2f6329bd041adf40c0ece4df96b2ba43f95c744e934f85d15d752` omitted zenodo-deposit.json although code/build_package.py reads it. A clean extracted-kit packaging run therefore lacked a required input. I reported this to the lead. The lead added the manifest to the explicit allowlist and rebuilt the kit. My own clean extraction of the final kit executed the packaging command successfully, and its reconstructed archive was byte-identical to the frozen upload.
2. **Resolved operational clarification.** Initially the main energy paragraph did not explicitly identify the logical quantum source used for cost averaging. I requested the maximally mixed input/equivalent entangled-reference qualification already stated in the supplement. The frozen manuscript includes it, preventing an unsupported maximum-cost or arbitrary-source-cost interpretation.
3. **Resolved metadata semantic clarification.** An earlier manifest related the paper to the source repository using isSupplementTo. I suggested reversing the relation if the repository is the paper's supplement. The frozen manifest uses isSupplementedBy.
4. **Lead's deterministic-build repair independently checked.** The lead identified a current-timestamp archive inventory entry and fixed its ZipInfo timestamp. This was the lead's finding, not an independent mathematical discovery in this review. The final archive reconstruction is byte-identical.

These findings were fixed before this frozen verdict. No remaining concern requires changes to the manuscript, metadata or upload files on the evidence inspected here.

## Mathematical falsification work actually performed

### Upstream premise

I read the pinned family-273 introduction and analytical sections 01–05 in full, rather than accepting its release label or the previous favorable audit. The pin is adc7f1241b42e322a6451854ab7e4b4c146bf78a. I checked the oscillator cutoff entropy argument, reference/slack/replacement order, coercive minimum, Gibbs moment lemma, finite-eigenblock Hessian duality and factors, parallel-sum interpolation construction, holomorphic/Stieltjes sign mechanism, tilted logarithmic-mean identity, weak convolution, centered means, generator covariance, and final stationarity cancellation. The recurrence identifying thermal limits removes internal correlations. I did not find circular import of EPnI or an assumed sharp multimode optimizer in that analytic proof.

I independently verified 37 upstream file hashes against pinned Git objects and scanned the actual 26-module transitive source closure for visible proof placeholders or unsafe evaluator/extern shortcuts; none appeared. I spot-checked the actual full-Fock State, finite-energy, entropy and beam-splitter definitions and the final real declaration. The comparator's deliberate sorry is not used. No compilation or axiom-closure inspection was completed in this review. See UPSTREAM_SOURCE_AUDIT.json.

### Entropy reduction and quantum operating model

I independently differentiated f_t(s)=g(t g^-1(s)). The monotonicity of (u+1)ln(1+1/u) has the claimed convexity/concavity sign. Choosing the common parameter from average Bob entropy, not from an arbitrary input component, yields the simultaneous input upper bound and environmental lower bound. Nonnegative finite average energy implies almost-sure finite component energy and integrable conditional entropies. Internal multimode entanglement is never removed in this step.

I checked the actual regularized quantum theorem's signed finite-gross resource model and all three catalytic converse bounds, including its pure-state refinement preserving the physical input marginal. The noiseless conversion signs and zero-energy cone coefficients agree. The quantum source used for cost is now explicit. The fixed-block energy-nonincreasing cutoff followed by separate resource-dimension continuity limits is sufficient; no uniform cutoff in n or product-input converse is asserted.

### Literal private counterexample and repaired converse

I read the original Section-5 predecoded secrecy condition and register/decoder definitions directly in the primary source and checked its author-hosted journal version. The condition protects the product uniform MT_AJS_B, not just generated secrets. At N=0, positivity and the rank-one vacuum kernel make every physical output fixed vacuum even with references. After tracing the comparison state, W=(M,T_A) is independent of all useful decoder inputs. The success-event bound gives exactly

    1 <= 1/(d_M d_T_A) + (epsilon_sec + epsilon_rel)/2.

This rules out generated private/key dimensions greater than one at sufficiently small errors independently of consumed resource sizes. The one-time-pad point lies in the advertised zero-energy cone but fails the literal condition. The norm 2(1-1/d) is exact; I checked the universal support argument and the rational finite-instance program. This is an impossibility proof for the full stated normal form, not simply a failed choice of encoder.

For GEN I independently expanded all three corrected converse chains. The second residual is at most H(V|X), because I(W;V|X)+I(V;E|WX)=I(V;WE|X) and V is classical. The third residual is bounded once by H(L)+H(V), with the correct consumed-rate coefficient. Reliability/secrecy continuity needs only the finite generated-register dimension and fixed finite gross rates, not a finite Eve dimension. Fresh K,M independence of the initial key is essential and is now stated; public common-randomness generation is not silently substituted. Spectral refinement for a degradable channel improves all three private bounds simultaneously without changing average energy.

### Direct coding, cost and composition

I checked every section of DIRECT_CODING.md, including the retained-mass projector arguments, Hayashi–Nagaoka packing estimate, Hilbert–Schmidt variance identity for noncommuting random matrices, rank/operator-norm exponents, gentle outer-then-inner decoding, uniform-message trace secrecy after averaging the consumed key, and cost selection. No exponential union over messages or semantic-security conclusion is needed. Closeness to a chosen public/Eve target implies closeness to the actual marginal with at most a factor two, which does not change the vanishing-error assertion.

I inspected CEF Propositions 2–3, its definitions of expected physical input and Appendix-A construction directly. Its rho-like property is an explicit required dependency, not an inference from output entropy. The appendix invokes the earlier HLB mechanism; the defective later joint consumed-key criterion is not needed as a black box here. Fixed photon cutoff makes the cost operator bounded. Strict mean-cost slack plus Markov intersects the high-probability good-error event, without postselecting quantum data or asserting a peak budget. I also checked the independent spectral-type energy construction in the optional energy supplement; it is a separate supporting mechanism, not required for the headline proof.

The GEN repair protects joint uniform generated resources, so trace contraction permits their use in a fixed finite composition with the stated noiseless protocols; consumed registers are discarded from the final promise. Finite gross seeds and cancellation are explicitly the original net-rate convention. This does not extend to superlinear catalysts or guarantee secrecy after revealing consumed keys.

I checked N=0, both lambda endpoints, eta=1/2 and eta=1. Both displayed unions are closed by compactness of the parameter and convex by the concave-right-side reparameterization. The natural-log/bit conversion is consistent. No thermal-channel quantum-capacity, amplifier, two-way-assistance, stronger energy, semantic-security or confidential-broadcast extension is included.

## Primary sources and priority framing actually inspected

I inspected the target-relevant statements and proofs in the author-hosted WHG 2012 PDF; De Palma 1805.12469v3 Theorem11/Corollary12; quantum dynamic 1004.0458v3 operational theorem and converse; private dynamic 1005.3818v3 model and converse; CEF 0811.4227v4 definitions/Propositions2–4 and appendices; the private-father and HLB security conventions; and the 2012 optimization erratum. I additionally opened the primary WHG v1/v2 records and OpenAI public-release announcement during this review. The release announcement is dated October6,2026; manuscript directory dates are not treated as public priority. The original formulas and conditional reduction were already public in 2011.

I read the complete priority and security-criterion audit notes, including their companion-corpus scope account and current source/version table. Targeted independent searches did not locate a correction of this exact consumed-key condition, but failed searches are not a novelty certificate. I did not independently re-audit every unrelated companion manuscript or all possible terminology in the entire literature. The frozen title, abstract, README and deposit description avoid a first claim, independent EPnI claim, invented machinery claim or success claim for the unchanged literal private region. The inherited formulas, reductions and upstream author are correctly attributed. A short consequence/correction note is an accurate publication framing; discovery of the formulas is not its contribution.

## Package reproduction and PDF inspection

From my own fresh extraction in review-owned storage, all five documented commands passed:

- exact rational OTP/conversion checks;
- exact entropy-coefficient identity checks;
- seeded exploratory interpolation checks;
- standalone Tectonic compilation;
- explicit source/verification-kit rebuild.

The rebuilt PDF's extracted text exactly matches the frozen deposit PDF. PDF byte identity is not required because timestamps differ. The rebuilt source archive is byte-identical. The certificate outputs match their stored versions. See PACKAGE_AUDIT.json and clean-command-1.txt through clean-command-5.txt.

I visually inspected all seven pages of the frozen final PDF after rendering, including formulas, references, page breaks and attribution/disclosure. No clipping or illegible formula was found. Fonts are embedded, the document is unencrypted, the title/author metadata are correct and no JavaScript or forms appeared. I separately inspected the initial PDF before the harmless typography/date-spacing repair.

The source kit uses an explicit allowlist. It contains original research/proof/code notes, bibliographic citation metadata and source hashes, not third-party PDF/text downloads, Lean source trees, caches, unrelated work, credentials or shell secret locations. CC BY4.0 prose and MIT original code licensing are stated; upstream citation and optional separately obtained Apache-licensed source remain explicit. Author name and ORCID match the user's supplied metadata, with no invented affiliation/coauthors. Extensive AI use and lack of conventional human refereeing are disclosed.

## Remaining limits and publication gate

This is an automated review with no reproduced upstream kernel check and no universal priority certificate. Its clean verdict is evidence alongside the proof, not a substitute for the proof or the mandatory fresh review. No Zenodo publication or tracker entry was verified here; they remain subsequent actions governed by the user's exact sequence. The fresh reviewer must receive the original target, full current package and its dependencies rather than only this favorable conclusion.
