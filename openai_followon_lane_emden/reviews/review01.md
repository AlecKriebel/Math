# Complete-package adversarial review 01

Review checkpoint: **2026-10-06 21:45 PDT (2026-10-07 04:45 UTC)**.
Reviewer: independently assigned automated subagent `/root/complete_review_01`.
Assigned-review completion estimate: **100%**. This measures this review, not completed production publication, tracker registration, human peer review, or a reproduced Lean kernel proof.

## Verdict

**No substantive mathematical, publication-framing, license, render, or clean-reproduction defect found in the exact frozen candidate identified below. Two minor documentation consistency defects should be repaired before the final exact package is deposited.** The manuscript and its five-page PDF need no mathematical correction on the evidence of this review. The mathematical acceptance is based on independent examination of the analytic dependency and transfer arguments, not on earlier favorable audit verdicts or the existence of Lean sources.

The publication framing is appropriate **as a modest immediate-consequence/exposition note**. The source Liouville breakthrough is attributed to OpenAI; the conditional transfer mechanisms are attributed to PQS/QS; gradient and compactness statements use standard elliptic estimates. This is not an independently new proof of the base conjecture, a new transfer mechanism, or a first-priority certification. The current manuscript, abstract, README and deposit description consistently make those distinctions. Exhaustive priority remains unproved, and two subscription comparator theorem ranges remain an acknowledged literature-access gap. Those limits do not contradict the note's deliberately modest framing.

This review does not authorize a different or expanded theorem, certify the upstream weighted/radial classification beyond the required specialization, claim full formal verification, or verify a remote Zenodo record that did not yet exist at review time. After documentation repair, the changed archive must receive the required renewed/fresh review and its new exact identities must replace these v1 identities for publication.

## What was actually reviewed

I read the original `PROJECT_BRIEF.txt`; the complete follow-on `publication/main.tex`; `CURRENT_THEOREM.md`; `DEPENDENCY_LEDGER.md`; all six included audit prose files and the interval diagnostic script under `notes/`; publication README and licenses; the complete intended Zenodo manifest; both reproduction scripts; included formal lock, axiom-audit source, trust scan, failed elaboration log and formal hash manifest; the upstream root README, manuscript-specific README/citation and formal scope document.

I read **all six family370 analytic sections**, its main TeX file and bibliography, without accepting a prior audit conclusion as proof. I independently reconstructed the needed unweighted proof, including exact Newton potentials, universal source masses, localized virial signs, interval comparison, the energy-relative layer-loss estimate, and the final absorption/scaling contradiction. The included family370 files were compared byte-for-byte with the pinned Git objects; every comparison passed.

I freshly downloaded the exact [PQS author-hosted primary PDF](https://www-users.cse.umn.edu/~polacik/Publications/pqs1.pdf) into owned scratch. It is 217,910 bytes with SHA256 `3c647b8f01e277812a2d3c7974d48ddb91695b7aa350d19f52a6449d15811ee6`, matching the included identity. I examined Theorems 4.1–4.3, Lemma 5.1, Proposition 7.1, Theorem 7.3, Remark 7.4 and their pertinent proofs. I separately checked [QS v2](https://arxiv.org/html/2407.04154v2)'s strong-solution convention, Theorem 4.1(ii), Remark 4.1(ii) and Section 7.2 in the primary arXiv HTML. I spot-checked current primary [Li–Li–Wei](https://arxiv.org/html/2510.06613v1) and [Li–Souplet](https://arxiv.org/abs/2408.17007) sources and the [OpenAI release announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/), and ran independent current literature searches. Search absence was not used as proof of novelty. Remote upstream HEAD still returned the pinned commit during this review.

For formal-status consistency I inspected actual pinned `Main.lean` and `Model.lean`, reproduced the optional source extraction into owned scratch, checked all **96** resulting module hash pairs against the included manifest, and independently repeated its textual source-hole scan. These passed. I did **not** read every line of all 96 formal proofs, elaborate the target theorem, run Comparator, fetch a full Mathlib artifact cache, or print its transitive axioms. No such success is claimed anywhere in the reviewed publication material.

I extracted the **actual intended uploaded archive**, checked all 34 member names, byte counts, modes and SHA256s, and confirmed every member matches its corresponding current project file. There are no absolute/traversal names, symlinks, caches, unrelated research files, or third-party PQS/QS full texts. A targeted credential/private-key/token-pattern scan returned no hits; the scripts were also read. I checked the upstream Apache license against the pinned root license and checked the split original CC BY / MIT / retained Apache attribution.

I rendered and visually inspected **all five pages of the actual intended uploaded `paper.pdf`**, including equations, theorem spaces, references, margins, page breaks and glyphs. No clipping, overlap, missing formulas, broken references or inappropriate metadata appeared. Its PDF metadata names Alec Kriebel and the correct title and subject. A clean rebuild's extracted text is byte-identical to the deposit PDF's extracted text; changed build timestamps are correctly disclosed as possible PDF-byte differences.

## Independent mathematical falsification work

### Unweighted input: source bounds and potential representation

For a positive entire classical pair, write `f=u^q`, `g=v^p`. Newton comparison gives `u >= c M_g` and `v >= c M_f` on the unit ball, whence `M_f >= c M_g^q` and `M_g >= c M_f^p`. Their combination yields an **upper**, not lower, universal mass bound because `pq>1`. The source assignments under scaling are `f_R=R^(beta+2)f(Rx)` and `g_R=R^(alpha+2)g(Rx)`; no swap occurs.

Positive-superharmonic representation gives `u=c_u+K*g`, `v=c_v+K*f`; the nonnegative harmonic remainders are constants. A positive constant would contradict the centered source bounds as the radius grows, so both constants vanish. Dyadic tails are summable since `alpha,beta>0`. Consequently the source and truncated-potential bounds needed later are obtained **before** any uniform energy estimate. The proof does not assume finite total energy or a universal amplitude bound.

### Virial, interval geometry and the pivotal layer loss

The signs in `-integral f X.grad u` and its partner agree with the displayed virial identity. The cutoff is compactly supported, separate kernel-gradient integrals are absolutely integrable, and Taylor errors on close pairs are bounded by the two actual finite energy marginals. On far pairs the exponents `4n+7`, `3n+5` and `3n+8` are positive, so the already proved source/tail bounds yield additive solution-independent constants.

For the interval comparison I independently obtain

`2A-E_I-E_J=(n-2)(D-d_0 T)`.

The overlap density is the nonincreasing trapezoid centered at `d_0`. Pairing positive and negative longitudinal differences gives `d_0 T>=0`; for `c=min(c_I,c_J)` the exact weighted slack is

`(n-2)c d_0 T+(c_I-c)E_I+(c_J-c)E_J>=0`.

This covers disjoint or unequal intervals and equal-midpoint equality cases. At most one positive coefficient makes the inequality pointwise. Thus an unbounded partner with zero coefficient causes no invalid infinity subtraction, including the logarithmic dimension-three tail. The excluded coincident-line set is null; endpoint potentials are recovered before finite subtraction and are bounded by finite marginals.

The long-layer event contains a ray segment of length `ell/2`. Polar integration bounds its probability by source mass divided by `t ell^n`, requiring no information about the unknown energy. Multiplication by the cap supremum and the threshold `t>=P d^(-k)` produces `C_(kappa,delta) P^(-1)d^N` exactly because `k=n(m+1)`. Low levels use the exact angular normalization and the already bounded integral of `u` or `v`. The resulting loss is an arbitrarily small multiple of `E` plus a constant. Choices of `kappa`, then `delta`, then `P` have the required independence. Endpoint values are exactly `t^(1/q)` and `t'^(1/p)` in the needed unweighted specialization.

The strict gap is `gamma=n(a+b)-(n-2)>0`. Localization and pressure absorb the marginal mismatch and bound `E` uniformly. The scaled positive energy grows by `R^(alpha+beta+2-n)`, whose exponent is positive, giving the final contradiction. At the critical hyperbola this step stops; no endpoint conclusion is imported. This examination found no unsupported equivalent central claim or circular estimate.

### Matching classes, pointwise, gradient, exterior and half-space

A nonnegative nonzero pair on a connected domain has both components positive by the strong minimum principle; a zero component forces its partner to vanish by its equation. This handles the zero solution and supplies exactly the bounded nonnegative entire hypothesis of PQS without an extra assumption.

The gauge `u^(1/alpha)+v^(1/beta)` has inverse-length scaling; the doubling ball lies inside the domain and grows to all of Euclidean space after normalization. Local bounded sources, interior `W^{2,r}`, a larger Sobolev exponent, locally Lipschitz powers and interior Schauder estimates give a bounded nonzero `C^2_loc` limit. Constants are independent of the domain and particular solution, but may depend on the fixed `n,p,q`; no uniformity as exponents approach an endpoint is asserted.

Gradient rescaling contributes one additional inverse length. The exterior implication uses the correct lower bound `d(x)>=|x|-R>=|x|/2`; it introduces no domain-dependent decay constant. Proper domains, arbitrary boundary geometry and the zero solution are covered; the entire domain is excluded explicitly.

PQS 4.2 **actually** excludes arbitrary nonnegative classical zero-Dirichlet half-space pairs, bounded or not, from the same bounded-entire hypothesis. Its exact class is continuous on the closure and classical inside. The manuscript does not substitute the weaker strip-bounded class of modern comparators, nor rely on a distance estimate that diverges at the boundary. PQS's bounded-half-space reduction to a lower-dimensional entire solution is compatible with the same-dimension entire hypothesis by lifting one coordinate.

### Fixed-domain bounds and precise strong compactness

A bounded `C^2` domain has uniform `C^{1,1}` charts. A classical pair continuous on its compact closure is individually bounded; solving the linear Dirichlet equation at a sufficiently large exponent and applying uniqueness upgrades it to global `W^{2,r}` with zero trace. No zero-normal-derivative condition is inadvertently imposed.

A hypothetical unbounded sequence, normalized at its global gauge maximum, has values at most one. The interior case gives a forbidden entire limit. In the boundary case, nearest-point normal coordinates are valid in the fixed domain's tubular neighborhood, and scaled graphs tend to zero in `C^2` on fixed compact sets. Uniform boundary `W^{2,r}` estimates and larger Sobolev exponents give convergence through the boundary. This requires no unjustified uniform Hölder bound on second graph derivatives. At normalized height zero the zero trace contradicts normalization; at positive height PQS half-space nonexistence contradicts normalization. Thus a genuine global Dirichlet bound follows.

After that bound, sources converge uniformly under a suitable `C^{1,gamma}` subsequence, and the global Poisson estimate on **differences** gives strong `W^{2,r}` convergence for each finite `r`. Closure of the solution set follows from the limiting equations and zero trace. Compactness in any indicated `C^{1,gamma}`, `gamma<1`, uses a strictly larger available embedding exponent. Uniform `C^{2,theta}` norms are justified only under the stated `C^{2,theta}` boundary hypothesis; compactness is claimed only below `theta`. No `r=infinity`, Lipschitz-gradient endpoint, or global `C^2` regularity from a merely `C^2` boundary is advertised.

## Reproduction results

Owned scratch: `validation/reviewer01/extracted`.

- `python3 verify.py`: exit **0**, with **13 included source identities**, **648 rational scaling/hyperbola cases**, **614 finite interval diagnostics** and **2,456 overlap samples**. Numerical output matches the included diagnostic JSON, including the `1.2861234820972956e-13` largest midpoint-identity scaled discrepancy. These are floating-point falsification diagnostics, not certified interval computations or PDE proof.
- The README's exact sequence `mkdir -p build` then `tectonic -X compile main.tex --outdir build --keep-logs`: exit **0** from the extracted root. The standalone bibliography resolves. Python **3.14.6**, Tectonic **0.16.9**.
- Rebuilt PDF text exactly matches the intended paper PDF's text. The actual deposit PDF has **five** pages and **73,988** bytes; it has no encryption, forms or JavaScript.
- The optional `formal_prepare.py` extraction: exit **0**, **96** pinned modules. Hash manifest and textual trust scan independently agree. A kernel build remains explicitly **unverified**.

## Concrete findings

1. **Minor, current-status inconsistency — `CURRENT_THEOREM.md`, item 4.** The section heading says the core claims are established, but item 4 says the exact `W^{2,r}`/`C^{1,gamma}` compactness and stronger boundary requirements remain to be verified. The manuscript and transfer proof already supply and justify these spaces. Replace the stale sentence with the exact established conclusions, including the `C^{2,theta}` boundary requirement. This file is inside the reviewed archive, so the repair changes the archive identity even though it leaves manuscript/PDF mathematics unchanged. The root independently flagged the same stale sentence while this review was running; I verified it directly against the frozen file.

2. **Minor, self-containment/provenance clarification — archived audit notes refer to absent local artifacts.** `notes/priority_audit.md` and `priority_modern_check.md` refer to local capture/source-identity manifests; `notes/transfer_proofs.md` names local downloaded PQS/QS files; `notes/formal_input_audit.md` names an ignored `validation/formal_build/README.md`. These do not exist in the extracted archive. The README appropriately explains that third-party full text and ignored build artifacts are excluded, and primary URLs/pinned identities let a reader reconstruct the needed evidence; the mathematical reproduction succeeds. Nevertheless, explicitly label those references as historical local evidence that is not bundled, and consider preserving the small non-copyright source-identity manifests or putting the necessary optional recipe directly in the package. Do not solve this by redistributing third-party full texts without permission.

No substantive findings require manuscript repair. Neither issue changes the theorem or its attribution. No private credentials, unauthorized third-party full-text copies, mismatching source bytes, failed mandatory numerical/build check, or unsupported headline claim was found.

## Exact reviewed identities

All SHA256 values below were computed independently from the actual reviewed bytes, not copied only from a favorable receipt. The four candidate upload/metadata identities agree with `receipts/candidate_v1.json`.

| Project-relative file | Bytes | SHA256 |
|---|---:|---|
| `publication/main.tex` | 16157 | `a42fed44cc32b314857963c2abbf525b30fc5cc52827eab16c61a4cb397cea61` |
| `publication/README.md` | 3894 | `207417c85876fbfebc82d86a58b554206d7d8bb4224af09d8fee54991be4d6ba` |
| `publication/LICENSES.md` | 2516 | `d0b051c23b14225b5b267bcb7445402cc54d25b76097b836bc527ae5c097c3e7` |
| `publication/paper.pdf` | 73988 | `5dfd859739d34d77eb97680ec11bb94439d793238d852bf6b99ab18d68281209` |
| `publication/source-and-verification.zip` | 496841 | `31e0b8d339bd7b75ca4793bb104756845730490d2179bbc50285548bd932174e` |
| `zenodo-deposit.json` | 2568 | `31f34df650e3f4085d3311417e2e056f385de490754585b72fd16719de6b15a7` |
| `DEPENDENCY_LEDGER.md` | 4417 | `c13848871e3f30938f1b4bd28df6ed4b03e8ed5956da6c384a6396ab1da761e4` |
| `PROJECT_BRIEF.txt` | 15893 | `9b62540be0809dcfb60b2a1b47f2ac5965b8b8d9c8fabd8fb4b5deb21abffc34` |
| `sources/SOURCE_HASHES.json` | 2404 | `fc59bb4ceb1a9ad8cd9e2b09cfec13ccf4b7ad9c5d95c0832ad1dbe1df88fdf2` |

The archive's **34 complete members**, each ordinary mode `0644`, were independently checked against their current project counterparts:

| Archive member | Bytes | SHA256 |
|---|---:|---|
| `CURRENT_THEOREM.md` | 2220 | `8692cc782839bb668db257c7515ab929a4635f86ef8cef5149949fe189e6da2e` |
| `DEPENDENCY_LEDGER.md` | 4417 | `c13848871e3f30938f1b4bd28df6ed4b03e8ed5956da6c384a6396ab1da761e4` |
| `LICENSES.md` | 2516 | `d0b051c23b14225b5b267bcb7445402cc54d25b76097b836bc527ae5c097c3e7` |
| `README.md` | 3894 | `207417c85876fbfebc82d86a58b554206d7d8bb4224af09d8fee54991be4d6ba` |
| `main.tex` | 16157 | `a42fed44cc32b314857963c2abbf525b30fc5cc52827eab16c61a4cb397cea61` |
| `notes/formal_input_audit.md` | 10503 | `66cb02a68e9e8498b7d3c09069fa966efed71bd34fdd42d91b1ee51c5c68a819` |
| `notes/priority_audit.md` | 14376 | `8b794e930f6cbe2fe9e3a8ae7f672c3fcadc5f82d1b5da0515835ea06c1c5259` |
| `notes/priority_modern_check.md` | 12618 | `e9124870c01ee88583de8f953427b123547d29951260cc7319f504b9b1181bcd` |
| `notes/transfer_proofs.md` | 19427 | `de4c2a098be077f1976533118c92d65376148723e2eb2848476cfca1299becdd` |
| `notes/upstream_interval_checks.py` | 9435 | `7833932f7326ca31b63588a25268265d65ed507f4633f01e7aaf0990078adf29` |
| `notes/upstream_interval_review.md` | 8042 | `57ae308cfd4deb2f95268a8c8c6222c5c62bb9a274addcedbb3da67ab84b4b4f` |
| `notes/upstream_mathematical_audit.md` | 12286 | `b5932e86677af58ed647580819f52605b929c3eed9c6a9ca555ea20316af6350` |
| `sources/370.md` | 961 | `46f3228957de33d7c417826c135802ac463c584d876b3a00d9a9b6de87a8da08` |
| `sources/SOURCE_HASHES.json` | 2404 | `fc59bb4ceb1a9ad8cd9e2b09cfec13ccf4b7ad9c5d95c0832ad1dbe1df88fdf2` |
| `sources/UPSTREAM_LICENSE` | 11357 | `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` |
| `sources/UPSTREAM_README.md` | 4131 | `af984f110f6583ba57ec1af907dc989bfce86713161e9c8b0543b052a138ff64` |
| `sources/family370/README.md` | 586 | `82b6bd9b3f71a2178a7f525b1969eda265e3ede67cc1f8add1100ed3a0825b1c` |
| `sources/family370/build/main.tex` | 3658 | `cb5f91b0eb64814971e7ea4593a04730756ca5a3029706ec02db387b2e634d2d` |
| `sources/family370/build/references.bib` | 6356 | `2d741df4010f92a2005be14dd5da15424f9d876382a462ebd7554cfd22f8c67a` |
| `sources/family370/build/sections/01-introduction.tex` | 6942 | `6f100de228636b2ef102573e58febceb2a40df4590c1597731e93edc3699b608` |
| `sources/family370/build/sections/02-preliminaries.tex` | 13100 | `9a510ee55bd758d481b57cd3e2160a4bdff7f7059d6a9bd4ed32d4584f69767b` |
| `sources/family370/build/sections/03-localization.tex` | 8204 | `a27394bbcb068cf24301f75840ec4eadb5b02ec87bf3c1edea79cb88902c41b0` |
| `sources/family370/build/sections/04-intervals.tex` | 5731 | `dc02167e2d6e2388d1c69e0c37817f8eb9468047a6c9ca02df145d8b2e012ef2` |
| `sources/family370/build/sections/05-pressure.tex` | 14892 | `5a35f793eef0c4d21029b4d0f0b0c860f2ea1b33f4b4a569ed38182467079f79` |
| `sources/family370/build/sections/06-conclusion.tex` | 5489 | `99c8d2df276b477178d163949c85a1fbc16fda4ab7dcdc9afecf62ef883fedb3` |
| `sources/family370/paper.pdf` | 406257 | `bb18015a30854675bec22e3183996625dac9be5046f81838c0bf9fbfa88806dc` |
| `validation/formal_AxiomAudit.lean` | 313 | `cec51ae7942f5c31105b10f5fb6eb2cdff1d60c68fbad0e9ba019b5819670616` |
| `validation/formal_lean_dependency_lock.json` | 3153 | `4aa8b01a11ed34de463651ed6396d9da61f365cccfd158e82e96bbd17bcb14bc` |
| `validation/formal_model_elaboration_attempt.log` | 1495 | `2d2f9cf13d4d293fac8842e3033306f89c001f61a4508ad26b364aa8f8495550` |
| `validation/formal_prepare.py` | 3229 | `a5ffc7dee6be2faaa8fd85be1461ee5c067fe5743291537ba6cc013f7fae1044` |
| `validation/formal_source_hashes.json` | 27758 | `948800f9ddf7035e315d0962de1f6e853f245b89710e44d3330317f084978ddd` |
| `validation/formal_source_trust_scan.json` | 569 | `f121ad89d33d50e270ec86af36bd90bca5fe76bc5792370f3a64d5d441e2fb76` |
| `validation/interval_diagnostics.json` | 2256 | `be1dd76f928f84b067d9eb70f12b5692f937d081307863ca931d5356f9ad8209` |
| `verify.py` | 1789 | `486fbed38831c290560a6ca486dfd39c301a9b8a7d9cd14906600dc6e739834e` |

Review artifacts (fresh PQS download, rendered page PNGs, rebuilt PDF/log, verification JSON, extracted package and optional prepared source closure) remain in owned `validation/reviewer01/` scratch. Candidate sources were not modified. No branch change, commit, push, publication, tracker operation, external individual communication, or outreach preparation was performed by this reviewer.
