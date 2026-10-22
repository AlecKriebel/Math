# Independent audit: Converse Unitary Distinction Criterion

Problem 30001737 / OWR-4804-005, rank 835. Audit date: 2026-10-06 UTC.

## Decision

Accept the corrected derivative as a scoped nonresolution, literature-scope correction, and expository mathematical partial. Do not label the target solved, disproved, or newly partially solved by this package. No new distinction theorem is established. The original mathematical account passes this review; its startup-integrity claim required an actual correction. The immutable author freeze is preserved.

One mandatory executable correction was found, implemented, and rerun. No mandatory mathematical correction was found. Three substantive approaches are documented; source searches and this audit do not count as additional mathematical approaches.

## Identity and source review

The complete supplied problem record and associated research-report lookup were read. The lookup is absent, so its default value is the empty object. Recomputing default `json.dumps([complete_record, reports.get(problem_number, {})], sort_keys=True).encode()` gives 4,195 bytes and SHA-256 `8ba2836d652463cffa7f4d58ad97db568547c48217eb4dc4b6a77b326ff8336d`. The exact statement gives 291 bytes and SHA-256 `89d6225abbe19de7352c6960382ec2a36ca00cd192d8c48cfc3e743c072fe08e`. Both match the catalog. Complete dataset hashes and sizes are in CORPUS_ACCEPTANCE.json; dataset contents and the record are excluded.

The primary mathematical target was checked against Lapid's report, §2.3, Theorem 6 and Conjecture 2, printed p.732, one-based PDF page 12. The previous p-adic subsection was explicitly separated. The target is C/R, GL_n(C), U(p,q), ordinary Galois pullback, and labelled character occurrences counted with multiplicity. Its generic implication is already established. Source: [Oberwolfach Report 14/2011](https://publications.mfo.de/bitstream/handle/mfo/3229/OWR_2011_14.pdf?isAllowed=y&sequence=1).

Feigon–Lapid–Offen was checked at §§1.3 and 3.2, Lemma 3.3, §6.5, Corollary 12.3, Remark 13.13, and Appendix B. The smooth Fréchet moderate-growth category and continuous functionals are appropriate. Conjecture 6.12 includes this target. Generic, finite-dimensional, spherical, unitarizable, and compact-signature cases are already covered. Theorem B.1 explicitly gives an upper bound for both the standard module and its Langlands quotient, under the standard real-exponent ordering. Source: [published paper](https://www.numdam.org/item/10.1007/s10240-012-0040-z.pdf).

Gurevich's ladder result uses p-adic E/F, GL_n(F) distinction, and conjugate-contragredience. It cannot establish the complex unitary target. This scope exclusion was checked at the primary abstract, not claimed as a full-paper audit. Source: [arXiv:1411.2420v2](https://arxiv.org/abs/1411.2420v2).

Zou's supercuspidal result uses a nonarchimedean local field of odd residual characteristic. A complex coefficient field does not change that local field to C. Again, this exclusion rests on the primary abstract and version metadata. Source: [arXiv:1909.10450v4](https://arxiv.org/abs/1909.10450v4).

Beuzart-Plessis's §3.5.1 imposes the nonarchimedean assumption carried into §3.5.9; Theorem 3.22 is restricted to generic representations. It supplies no resolution for arbitrary nongeneric complex Langlands quotients. Source: [2025 survey](https://arxiv.org/html/2509.18062v1).

The bounded current search did not locate a full exact-target resolution. This supports only the package's bounded-search statement, not an exhaustive or definitive claim that the problem is open. A January 2026 revision on local-global principles was also screened at abstract level; it did not supply an applicable theorem for the present target. Source: [Matringe–Offen–Yang](https://arxiv.org/abs/2509.00441v2). Search and inspection limits are recorded in SOURCE_REVIEW.json.

The two supplied PDFs were independently hashed and freshly text-extracted; the extractions agreed byte-for-byte with the supplied text. Rendered p.732, and Feigon–Lapid–Offen pp.246, 295, and 308 were visually inspected. Source documents, source extracts, and rendered pages are not in either public-safe archive.

## Mathematical review

### Target normalization

For the Euclidean modulus, chi_(k,s)(z)=(z/|z|)^k |z|^(2s) is a smooth character for integer k and complex s. Pullback by z -> conjugate(z) sends (k,s) to (-k,s), with no conjugation of s. This preserves standard ordering by real exponents. For nonfixed characters, equal multiplicities of chi and chi^tau are required. Thus s_0 is the sum of their common multiplicities, not the number of distinct two-element character types. The report introduces no erroneous parity condition.

### Approach 1: upper-bound expansion

The involution condition is coordinatewise on labelled occurrences. Nonfixed characters must be paired with their tau partners; a block of b copies on each side has b! matchings. A fixed block of a labels with u transpositions has a!/(2^u u! (a-2u)!) arrangements. These blocks are disjoint. Their transposition counts add, leaving n-2s_0-2u fixed labels and the signature factor choose(n-2s_0-2u,p-s_0-u). Multiplication and summation give the reported closed expression.

If the multiset is unstable, no compatible involution exists. In the stable case every nonzero term requires s_0 <= min(p,q). Conversely the all-u_i-zero term is positive under precisely that inequality. This proves positivity of the combinatorial bound, not positivity of a period dimension. In particular a positive upper bound permits dimension zero. No unjustified equality with period multiplicity appears.

Independent testing used a bitmask dynamic program counting compatible pairings together with signs on unmatched fixed labels. It does not enumerate involution permutations or use the factorial/binomial formula. It reproduced the author's 174 patterns and 1,266 signatures, then agreed on 3,002 multisets and 23,594 signatures, including 2,828 unstable multisets, through n=8. Extra examples use more distinct fixed or nonfixed blocks. The all-size proof is the block-counting argument; these finite tests are regression evidence only.

### Approach 2: rank one and radial twists

On U(1), chi_(k,s) restricts to the kth angular character. Its invariant functional exists exactly for k=0. For every h in U(p,q), taking determinants in h*Jh=J gives |det h|=1. Therefore the radial determinant character is trivial on H, and the two Hom spaces coincide on the same topological vector space. A common radial twist shifts every exponent equally and preserves all character equalities, tau pairs, and standard ordering. These are valid elementary known consequences, with no claim of new cases beyond known results and their twists.

### Approach 3: quotient descent

The continuous Langlands quotient map between Fréchet spaces is open and its kernel is closed. An H-invariant continuous functional on the standard module descends if and only if it annihilates that kernel. Pullback is injective, and the kernel of restriction to K is exactly its image. Surjectivity onto Hom_H(K,C) is not claimed.

For the toy C^times action diag(1,z), invariance at z=2 forces the second coefficient of a functional to vanish; restriction to K=C e_0 then kills no nonzero invariant functional. Thus the quotient is not distinguished despite a distinguished ambient module. The report correctly identifies this as a general quotient-descent warning, not a Langlands-quotient counterexample. No actual nonzero functional annihilating the target Langlands kernel has been supplied. The stated stopping point is mathematically honest.

## Mandatory startup correction and actual acceptance

The original verify.py imports argparse, hashlib, importlib.util, json, and pathlib before examining the payload inventory. A benign unlisted argparse.py created a sentinel before the verifier failed, under both normal Python and -O. Nonzero exit status therefore did not imply rejection before untrusted code execution. ORIGINAL_BOOTSTRAP_FINDING.json records this reproduced defect.

The corrected derivative adds a built-in-sys-only startup guard before nonbuiltin imports in every entry point, requiring `-I -S -B`. Child invocations in audit_checks.py retain those flags. More importantly, the separately reviewed isolated_bootstrap.py runs in isolated, no-site, no-bytecode mode, checks the external manifest pin and complete strict inventory, rejects aliases and nonregular entries, reads every payload, validates all payload hashes, then executes only those validated bytes from a private snapshot. It does not execute a potentially tampered verifier to ask whether that verifier is trustworthy.

This is an integrity gate under a trusted Python interpreter, standard library, operating system, bootstrap, and externally supplied manifest pin. It is not a hostile-code sandbox. Running arbitrary package code directly, using a bootstrap taken from the untrusted payload without an external pin, or starting Python without the required flags is outside the accepted procedure. The direct guard cannot retroactively prevent interpreter startup hooks; isolated launch prevents those hooks from being selected.

Actual correction artifacts, not hypothetical instructions, are supplied in ISOLATED_STARTUP_CORRECTION.patch and the corrected archive. Applying the patch to the original extracted package reproduced the corrected bytes exactly. The original ZIP remains unchanged. VERIFICATION.json inside the derivative is explicitly marked as historical author evidence, and its historical pins are not presented as patched-code acceptance.

ACCEPTANCE.json and ACCEPTANCE_OPTIMIZED.json record actual normal and optimized runs, including original/corrected/relocated bootstrap replays, 22 hostile-control families, complete-corpus replays, and byte-mutation rejection for each corpus. All passed. These controls include local import shadows, modified verifier/math code, hostile PYTHONPATH/PYTHONHOME/PYTHONSTARTUP and cwd, symlinks at root/ancestor/leaf, hardlinks, FIFO, missing files, cache directories, duplicate manifests, and pre-import direct-entry guards. The original failure remains explicitly recorded, not relabeled a pass.

The author's reviewed suite was independently rerun on both original and corrected packages. The patched suite passed 13 semantic mutation families and 10 integrity mutation families in both normal and optimized child execution, plus original and relocated valid runs. Full source-document claims and arbitrary prose truth are not machine-verified: mathematical review by the independent AI auditor, rather than JSON flags, supports the mathematical acceptance.

## Accepted scope and remaining limits

- Accepted: exact target identity, literature-scope correction, the all-size combinatorial identity, elementary twist/rank-one reasoning, honest quotient-descent obstruction, and the tested corrected integrity procedure.
- Not established: the unrestricted converse, a target counterexample, a novel distinction theorem, complete literature/repository-history coverage, or formal verification of the cited analytic proofs.
- Publication eligibility is limited to authored audit/correction material and public verification metadata. No publication was performed by this audit.
