# PR184 / 10300044: independent GV algebra and reproduction adversary

## Disposition

No mathematical falsification was found in this family's audit of the fixed-manifold theorem. The relative-collar construction, form signs, positive rescaling, global gluing, exact GV additivity, and single-circle tautness argument survive the checks below. The primary dependencies match the required input. This assessment concerns the literal printed Calegari target, and does not establish historical priority.

The original executable verification has a confirmed enforcement defect: both original check functions use Python assert, so optimized execution removes every scientific and digest guard while retaining advertised counts. Wrong GV signs and wrong frozen-candidate digests then return exit 0, and the original reviewer prints PASS. These control defects require correction in any promoted verification package, but they do not by themselves falsify the written mathematical proof.

## Independence and protected inputs

FIRST_ASSESSMENT.md and FIRST_READ_LEDGER.json were frozen before reading any original reviewer, independent_checks.py, stored receipt, imported report or sibling/root verdict. FIRST_SEAL.json was created at 2026-10-14T03:49:43.144315+00:00 and has SHA256 ce449e4bc8afb8710be865389f5639cabc74b62b44d796880d109dd80b5986fe. At that point only those three first-stage documents were mode0444; supporting code/receipts were0644. The additive FIRST_SEAL_MODE_PROTECTION_CORRECTION.json records their subsequent protection at 2026-10-14T03:53:27.160880+00:00, with no byte changes or rewritten first seal.

The candidate and scripts were run only from isolated private copies. The final original-file integrity scan confirms all 17 source-manifest hashes and sizes match, and every original remains0444. No Git command, local ref/index/checkout mutation, remote PR/tracker/Zenodo/release operation, external contact or outreach draft, or user-tab/editor operation was performed. Root campaign metrics were not edited. This family performed no repair of original files; repair work is separate.

## Mathematical checks and exact scope

For alpha=dz+p dx+q dy and eta=p_z dx+q_z dy, independently expanding exterior products gives

    alpha wedge d alpha = (q_x-p_y+q p_z-p q_z) dx dy dz
    eta wedge d eta = (q_z p_zz-p_z q_zz) dx dy dz.

Thus the author's signs are correct, and d alpha=alpha wedge eta requires the Frobenius coefficient to vanish. The author tests general polynomial identities rather than generating integrable foliations.

The separate integrable control takes F=z+x z^2+y z^3, D=F_z, alpha=dF/D. Exact rational Taylor jets check Frobenius, the defining equation, the independently derived rational GV density, and two positive compressions at eight rational points. The density equals

    [-6z^2-16xz^3-(8x^2+18y)z^4-12xy z^5] / D^4.

These 58 checks are reproducible with the standard library. The script has explicit conditional errors and retains enforcement under optimization: an injected false control exits1 in both modes. Local nonzero density is not a nonzero closed GV integral. The proof and source-backed suspension, rather than this local example, supply the latter.

For f>0, alpha'=f alpha and eta'=eta-d log f preserve the defining equation, and change the GV form by -d(log f d eta). Changing eta to eta+h alpha changes the GV form by d(h alpha wedge eta). The closed integral is therefore invariant. For the relative block the candidate fixes eta=0 on endpoint collars, so the relevant boundary terms vanish. It does not assume arbitrary relative primitives have invariant integrals.

For a positive slab length ell, alpha_new=ell h*alpha and eta_new=h*eta preserve the defining equation, product-collar normalization and coorientation. The top form scales with the positive 1/ell Jacobian; the integral is unchanged. Zero length is undefined and negative length reverses orientation. Only positive finite lengths are used. Every finite N admits separated slabs. No infinite stack, convergent sequence of forms, uniform derivative estimate or limiting foliation is required by the target. Each individual global normalized form has alpha(V)=1; an arbitrary initial positive defining form can be normalized smoothly on its compact block.

Compact support of finitely many surface-group generator maps gives a common identity neighborhood at each interval endpoint. Partition-of-unity averaging of increasing local fiber coordinates has positive vertical derivative and the same prescribed endpoint coordinates. It trivializes the interval bundle relative collars, without trivializing its interior flat foliation. The resulting forms glue exactly on open product collars, so no interface cross terms arise in the GV integral.

Global tautness is a written geometric certificate: a suspension leaf projects onto the connected base by complete path lifting for full interval diffeomorphisms. It meets the interval fiber over the fixed base point. Product-region leaves and interface leaves meet that same fiber. Choosing a disk-fixing monodromy representative closes it to one smooth embedded transverse circle through every leaf. This addresses the actual single-circle definition. Neither checker numerically or algorithmically certifies global tautness, and neither claims to do so.

## Primary-source verification

I read the actual [Calegari v1 paper](https://arxiv.org/pdf/math/0209081v1), including Definition1.1, printed p25 Question10.6 and its entire remark, and section13.1. I rendered and inspected p25. The target imposes no minimality condition; its regularity setting admits the smooth subclass used by the candidate.

[Tsuboi1981](https://aif.centre-mersenne.org/item/10.5802/aif.828.pdf), printed pp1–3 and6, explicitly supplies the surjective smooth GV map, compact-support real-line group, H2-to-H3 isomorphism and commutative suspension diagram, and representation by closed oriented surfaces. I read the relevant text and visually inspected printed pp1,3,6. The diagram has the required barred classifying-space convention. These statements provide the nonzero compact-support suspension input; an arbitrary S3 example would not suffice. The stronger genus-reduction sentence is unnecessary.

[Tsuboi2013](https://tsuboiweb.matrix.jp/faculty-html-gf2013/abstract_files/gf2013_195-200.pdf), printed pp195–200, was fetched directly with HTTP200 despite a web-tool access failure. Theorem2.1 and printed196–197 corroborate the compact-support setting. Their images were inspected.

[Thurston's mapping-torus preprint](https://arxiv.org/pdf/math/9801045) Theorem0.1, Proposition2.6 and section5 give the required hyperbolization for the fixed pseudo-Anosov mapping class. Those locations were read and visually inspected. Penner's original publisher PDF returned403. I independently fetched [Fathi's primary proof](https://www.numdam.org/article/BSMF_1992__120_4_467_0.pdf), read definitions and theorem on printed467–468 and inspected468; its twist criterion supplies the required mapping class and permits the elementary support argument leaving a disk fixed.

These are authenticated theorem inputs, not independent reconstructions of all classical proofs. This review did not conduct an exhaustive literature or priority search. Full private PDFs, extracts, renders and access metadata are excluded from the publication allowlist. SOURCE_VERIFICATION.json supplies exact hashes, pages, access limits and URLs without republishing the source bodies.

## Fresh reproduction and adversarial results

Normal fresh runs reproduce both stored receipts byte-for-byte, after execution rather than by accepting stored PASS: author2660 check calls; reviewer1641 check calls with SymPy1.14.0. Every scientific/control execution records exact argv, absolute working/output paths, actual UTC start/end, exit status, stdout/stderr files and SHA256 bindings. Runtime versions are separately recorded.

| Isolated control | Normal | Optimized | Implication |
|---|---:|---:|---|
| Original author baseline | 0 | 0 | Counts alone do not reveal enforcement |
| Author injected false check | 1 | 0 | Optimized guard removed; reports2661 |
| Author wrong density sign | 1 | 0 | False algebra accepted under optimization |
| Author theorem text Na changed to0 | 0 | Not needed | Printed proof hash is informational, not an expected-hash gate |
| Author source comment changed | 0 | Not needed | Printed source hash is informational |
| Original reviewer baseline | 0 | 0 | Fresh normal receipt matches |
| Reviewer wrong GV sign | 1 | 0 | Optimized script still prints PASS/1641 |
| Reviewer theorem text Na changed to0 | 1 | 0 | Frozen proof guard also disappears |
| Reviewer expected proof digest replaced byzeros | 1 | 0 | Wrong expected digest accepted under optimization |
| Reviewer source comment changed | 0 | Not needed | Source itself is not hash-gated or recorded by original receipt |
| Own injected false control | 1 | 1 | Own explicit errors retain enforcement |

Natural arithmetic exceptions may still abort optimized runs, since check arguments are evaluated. The defect is removal of every check function's enforcement, not removal of every computation.

The actual author generator has period11 in its seed. Its120 polynomial pairs contain11 distinct pairs;360 affine-rescaling iterations contain33 distinct pair/compression combinations;50 potentials contain11 distinct values. The2660 total is a correct call count, not a count of2660 independent scientific cases. The reviewer's1641 calls include343 sampled positivity points and343 sampled equation evaluations, general symbolic identities,120 polynomial-density integrations,220 abstract weight/derivative checks,600 slab/mass bookkeeping checks, and one proof hash. Neither program constructs the nonzero holonomy representation or a hyperbolic metric.

A separate exact counterexample demonstrates the finite-grid limitation. Let P(x)=product(i=0..6)(x-i/7)^2, K=2/P(1/14), and Phi=z+x z^2+y z^3-K zP(x). Its vertical derivative is positive at all343 reviewer grid points (minimum1), but equals -62/63 at (1/14,0,1/9), inside the grid box. Continuity forces a zero denominator. This falsifies the inference from finite sampled positivity to global nonsingularity, not the candidate theorem. For the original specific local F on nonnegative coordinates, positivity follows analytically from D>=1; no numerical grid is needed.

## Repair recommendations and remaining limits

Use explicit conditional errors in all scientific and digest guards, and retain negative controls under normal and optimized execution. State distinct-case counts separately from repeated call counts; replace the repeating generator where broader coverage is intended. Bind expected proof/source digests in a trusted external manifest or clearly label printed hashes as informational. Preserve the original frozen proof and scope: algebraic checks do not realize the classical suspension or prove hyperbolicity/global tautness.

No weaker target is proposed. The full printed target remains addressed by the source-backed geometric argument. There is no unresolved algebraic/global-gluing gap identified by this family. The remaining limits are the imported classical theorem proofs, absence of an explicit computable holonomy instance, and unestablished priority; none was silently promoted to a finite-computation result. Root's subsequent repair package is outside this family's original audit and seal.

Own-review completion estimate:100%. This is completion of the assigned audit, not an estimate of independent foundational reproof or historical novelty.
