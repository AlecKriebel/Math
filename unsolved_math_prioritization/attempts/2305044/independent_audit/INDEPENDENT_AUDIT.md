# Independent audit of Brannan coefficient scope and reproduction

Audit date: 2026-10-05 UTC. Target: 2305044 / AMR-022-5044, queue rank 681.

## Verdict

**PASS for the expressly limited result.** The package correctly records an attributed published resolution of the original β=1 problem and gives exact, self-contained counterexamples to the unrestricted positive-parameter extension. The authored odd-degree existence argument and sector partial result are mathematically sound. No blocking error was found.

This verdict does not certify the complete 2021 proof or addendum, the complete 2019 dependency chain, or Dunster's global numerical lower bounds. It does not establish novelty, scholarly peer review, full formalization, or complete equality to missing historical dataset records. The correct disposition remains attributed prior resolution with independently reproduced scoped mathematics, not a new solution.

## Frozen input and execution

The reviewed archive is `SAFE_AUDIT_PACKET.zip`, 21,085 bytes, SHA-256 `3d0a57a4fce83269bd76bf9f0d879ce02892f732a12d4088af9923c4f76adb2e`.

All 12 payload files match their manifest byte counts and SHA-256 hashes. The embedded and external `FROZEN_MANIFEST.json` are identical, SHA-256 `e66e5ab5db186297c965c68f1c073cfc3598bdf4f9c58c5efd8496f19c56d98b`. The corresponding supplied files also match the archive. The archive contains only these 12 files and its manifest. The review used a separate extracted copy and did not modify the frozen input.

All three supplied programs were executed successfully. Their outputs match the three supplied JSON outputs byte for byte:

- `verify_exact.py`: two rational witnesses; 616 cubic cases; 496 endpoint controls; 192 recurrence controls; 38 prior-construction identities.
- `check_bernstein.py`: the three claimed negative Bernstein minima.
- `check_sector_numerical.py`: 80 high-precision sanity checks, explicitly non-rigorous.

A separately written `independent_checks.py` imports no candidate code. It derives coefficients from the formal logarithmic-series recurrence

n A_n = Σ(k=1,…,n) [α(−1)^(k+1)x^k + β] A_(n−k), A_0=1.

The resulting computations pass 1,080 exact comparisons against direct coefficient convolution, symbolic cubic identities, the complete fifth-degree coefficient vector, 30 sign-change endpoint controls, and independently constructed Bernstein transforms. The universal claims rest on the written arguments audited below, not these finite checks.

## Exact problem and domains

The supplied Hayman–Lingham PDF was checked against its stated hash, and printed page 102 was inspected in text and rendered form. Problem 5.44 explicitly has 0<α<1, β=1, |x|=1, and coefficient index 2n+1 with n≥2. Thus its unresolved index range starts at five; degree three is mentioned separately as already known. The subsequent question permits arbitrary positive α and β and separately highlights degree three. The original right-hand absolute value and the later degree-three expression are distinguished in the candidate. [Primary statement](https://arxiv.org/pdf/1809.07200v2).

The finite coefficient formula follows from the normalized analytic germs and their absolutely convergent product for |z|<1. In particular, the coefficient parameter x can be on the unit circle without requiring convergence of the generating series on |z|=1. Setting x=−1 legitimately combines the powers into (1−z)^(α−β).

Consequently the fifth-degree witness is directly within the odd index range n≥2 of the generalized question. Its α=3/2 is outside the original one-parameter domain and the unit square; it cannot refute either narrower assertion. This distinction is maintained throughout the packet.

## Exact counterexamples and existence proof

The separate logarithmic-series computation reproduces, at α=3/2, β=1/32,

A_5(1)=2997183/268435456,
A_5(−1)=3171231/268435456,
|A_5(−1)|−A_5(1)=5439/8388608>0.

Every one of the six displayed coefficient-vector entries agrees. Both endpoint coefficients are positive, so the same witness refutes the extension even when the right side is interpreted with an absolute value. The degree-three witness at β=1/14 also agrees exactly: the gap is 1/98. Reusing β=1/14 at degree five does not work, as the packet correctly warns.

For each fixed odd j=2m+1≥3, the existence proof's P(β) is a genuine polynomial, with P(0)<0 and P(1/2)=2 binom(2m,m)/4^m>0. It is nonzero, so its roots are finite. After its largest root r in (0,1/2), positivity follows by the absence of another root and the positive value at 1/2. Throughout this interval, 3/2−β lies between one and 3/2, making Q(β)=−binom(3/2−β,j)>0. In particular Q(r)>P(r)=0. Continuity and rational density supply the claimed rational β immediately to the right of r with 0<P(β)<Q(β). No uniform-in-j β is claimed or proved.

The general negative result is properly credited to the earlier DannyExperiments public research artifact. Its source manuscript states and proves the stronger every-integer-index result. The publicly retrievable proof, citation, manuscript, and README Git blob IDs all match the frozen manifest. Its release date, version, DOI, and absence of human specialist review are recorded in the source. This is attribution to a public research artifact, without elevating it to a refereed paper or establishing absolute priority. [Prior artifact](https://github.com/DannyExperiments/generalized-brannan-counterexample), [citation record](https://github.com/DannyExperiments/generalized-brannan-counterexample/blob/main/CITATION.cff).

## Endpoint and sector proofs

For β=1 and 0<α<1, the endpoint identity S_j(−1)=Π(r=1,…,j)(1−α/r) is positive and below one. The odd Taylor truncation at x=1 lies strictly above 2^α because the next derivative is negative on the real segment. These give the claimed endpoint comparison and justify removing the right-hand absolute value in the original domain.

The sector argument has the correct Taylor-remainder sign and factor αB. The segment avoids the branch point for θ<π. The key inequalities are valid throughout y=−cos θ∈[1/2,1):

- D(t)≥(1−t)^2 implies I_j≤I_1 for j≥1.
- D(t)≤1 implies D(t)^(α/2−1)≤D(t)^−1.
- Integrating the derivative term gives (1−r^α)/α with the stated sign.
- The substitution u=sqrt((1−y)/(1+y)) gives C(y)=u(π/2−arctan u), increasing on the stated interval.
- Its maximum π/(3sqrt(3)) is strictly below log 2.

The resulting bound |S_j(x)|<2^α<S_j(1) closes the full stated outer sector, for every odd j≥1. It does not close the middle sector. At θ=π, use the explicit endpoint formula already proved in section 4; strictness need not be inferred from continuity alone. The written package therefore has no endpoint gap. The method's attribution to Deniz–Çağlar–Szász is appropriate, while the standalone derivation is what supports this audit. [Method source](https://arxiv.org/pdf/1906.09498v1).

## Failed sufficient certificate

The Bernstein conversion is algebraically correct. An independent construction of the squared-modulus difference and bivariate basis change returns minima −2, −7, and −332/15 at degrees three, five, and seven. Negative Bernstein coefficients defeat this particular sufficient certificate; they do not prove that the underlying polynomial becomes negative. The packet observes this distinction and does not overstate the failed route.

## Literature status and certification limits

The publisher's current indexed record confirms Barnard and Richards, JMAA 493(2), 124534, dated 15 January 2021, with an analytic proof of the β=1 conjecture. The author's institutional publication list corroborates the paper and a 2021 addendum. Direct publisher/full-text retrieval remained unavailable in this audit. The article's β=1 title is authoritative over the institutional list's α=1 typo. This supports the literature-status correction while leaving full-proof inspection explicitly incomplete. [Publisher record](https://www.sciencedirect.com/science/article/pii/S0022247X2030696X), [institutional list](https://www.math.ttu.edu/~rbarnard/vita.html).

Dunster's inspected v2 record is dated 17 July 2026 and lists no journal reference for part II. The theorem covers the unit square and all odd degrees at least three. Section 6 describes boundary-biased parameter grids, stationary-point searches, high precision and cross-quadrature checks, with an auxiliary finite search cutoff supported numerically. Those descriptions do not themselves supply a global interval certificate across continuous parameters. The packet fairly distinguishes the manuscript's claim from an independent numerical certification, and does not infer that the conjecture or manuscript is false. PDF theorem numbers 1.1–1.4 correspond to HTML theorem numbers 1–4. [Record](https://arxiv.org/abs/2606.11621v2), [theorem and numerical method](https://arxiv.org/html/2606.11621v2).

## Nonblocking clarifications and preserved limits

For later republication, two tiny wording improvements would make the boundaries easier to see: cite Dunster as “PDF Theorem 1.1 / HTML Theorem 1”; and describe the θ=π sector endpoint as following directly from section 4. Neither is a mathematical blocker and neither requires changing the frozen packet.

This audit independently recomputed the four supplied public-source PDF/HTML byte counts and hashes. It did not reconstruct or rehash the missing historical problems/reports corpora, and did not independently re-run every repository-history or duplicate-search claim. The candidate's explicit limits on those points must remain. Do not turn this scoped pass into a raw-source-readiness attestation.

The one combined research response and four approach-family accounting is coherent with the supplied ledger. This fresh audit is not a fifth new proof approach, and no queue command was executed. No remote write, external publication, source redistribution, or new DOI action was performed. Only the authored audit and code plus verification metadata are included in the audit deliverables.
