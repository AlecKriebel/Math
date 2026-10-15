# PR 445: independent reproduction and integrity review

**Verdict: one verification repair required; no central mathematical gap found in this family.** The exact frozen finite outputs reproduce, and independently authored exact controls agree with the claimed geometry, correlation algebra, normalization and suspension formulas. Both supplied checkers nevertheless emit false success under inherited `PYTHONOPTIMIZE=1` for materially wrong calculations and failed integrity/replay conditions. This is a defect in executable verification evidence, rather than a refutation of the analytic construction.

- PR: 445; problem: 30002737; frozen head: `3242c84e06db7e99012c7fe581adde5c3f89fc89`.
- Reviewer: `/root/pr445_reproduction`; family: independent reproduction, controlling-code adversarial tests and provenance.
- Review date: 2026-10-12 UTC. Original proof-search attempts performed: zero.
- Blocking findings in this review: **1**; required repair items: **1**; central mathematical gaps found: **0**. The blocking finding concerns promoting the supplied executable checks as reliable PASS evidence across their advertised Python environment. It does not assert that the mathematical claim is false or independently settle a narrower one-dimensional problem.

## Corpus and provenance

I read `SOURCE_RECEIPT.json`, the complete PR metadata, selected queue row, and all twelve original package artifacts: the README, clarifications, source gate, release manifest, research log, independent audit/script/results, author manifest, proof turn, author checker and its saved results. No current peer findings were supplied or consulted before the checks. The three frozen author files, twelve receipt entries and both manifests match their recorded SHA-256 digests and byte lengths. The review did not edit any frozen source, queue, PR, gate, index, Git state or remote resource.

The twelve files were also retrieved read-only from the exact GitHub commit URL. Every remote blob matches the receipt, including all proof and executable artifacts; see `records/frozen_remote_provenance.json`. This supplements the local receipt check rather than assuming a receipt labels the correct contents.

The OWR report, Baake–Grimm paper and van Enter precursor were downloaded independently from primary URLs. Their hashes exactly match the three hashes in the frozen independent audit:

| Source | Bytes | SHA-256 |
|---|---:|---|
| OWR report | 286194 | `23b89a2f8f2ac139fc32feb347ae05724ec3dd22aed540c59c24f8477ed7b3af` |
| RS paper v2 | 143996 | `637b2eb51d7b75ca0e2f73392bf79b232f445e23cacd88bfb7476a01e64e5734` |
| Precursor v2 | 123459 | `d34826964104fd26d1f05ca852f2e40c0b8d99a6a549114977b8263d29011291` |

I extracted relevant pages and inspected rendered OWR PDF page 10 (printed 2996), RS pages 2–3 and precursor pages 2–3. The [OWR conjecture](https://ems.press/content/serial-article-files/46543) gives the absence-of-AC implication without a printed one-dimensional restriction. The [precursor](https://arxiv.org/pdf/1310.0267v2) supplies a d-dimensional context. The [RS paper](https://arxiv.org/pdf/0810.5750v2) supplies strict ergodicity, balanced signs, the two-sided recursion, delta two-point correlations and the ambient-plane classification of line-supported diffraction. These source checks support the frozen package's stated interpretation; they do not establish novelty or historical priority.

My current exact catalogue request failed with **HTTP 429**, preserved in `records/catalogue_access.json`. The earlier reported 403 is a historical record, not the status of this request. The live catalogue statement was not obtained. Cached catalogue content, historical text extracts, source workflow files and the earlier excluded manuscript are not present in the twelve-file corpus, so no claim of replaying those missing historical artifacts is made. Fresh matching primary PDFs verify the cited source content directly.

## Baseline replay

Runtime: CPython **3.14.6**, macOS arm64. Both supplied scripts use only the standard library; the independent script's `int.bit_count()` requires Python 3.10 or later, consistent with the README. The audit's `python3` child resolves to the same installed interpreter. Poppler **26.08.0** was used for source extraction/rendering. Exact executable paths and version output are preserved in `records/integrity_environment.json` and `records/tool_versions.json`.

Each source script was run in its own complete private package copy. For ordinary runs the inherited optimize environment variable was removed. For optimized runs `PYTHONOPTIMIZE=1` was passed through the environment, including to the independent checker's author replay subprocess. The frozen source directory was checked again afterward.

| Checker | Normal return code | Optimized return code | Saved output bytes |
|---|---:|---:|---|
| Author | 0 | 0 | Identical to original in both runs |
| Independent | 0 | 0 | Identical to original in both runs |

The normal author replay confirms its reported 1,296 motif-pair, 81 weighted-correlation and 935 overlap controls. The normal independent replay confirms 262,144 substitution sites, 8,192 bilateral sites, 64 marker cases, 351 finite physical-pair comparisons and 334 rational section controls. Raw stdout/stderr, exit codes and elapsed times are in the four `records/baseline_*.json` files. The same output under optimization does **not** mean that the same validations executed: Python removes each `assert` statement and its expression.

## Finding R1: optimized execution fabricates successful verification

The author checker contains **9** controlling assertion nodes; the independent checker contains **12**. Relevant locations in the frozen source are author lines 26–28, 61, 74–76, 85 and 92–93, and independent lines 13, 20, 26, 37, 48–50, 61, 93, 100, 113 and 119–120. Their unconditional success records are author lines 95–110 and independent lines 121–123. The independent author subprocess at line 118 inherits the optimization variable.

This was tested by actual changed private input/code copies and real subprocess executions. It was not inferred solely from seeing an `assert`. Each row below has one normal run and one optimized run:

| Deliberate invalid variant | Normal | Optimized |
|---|---:|---:|
| Author marker changed to `(1/6,0)`, causing an extra marker pair | rejects, rc 1 | false `pass`, rc 0 |
| Author mean motif weight changed from `1/2` to `1/3` | rejects, rc 1 | false `pass`, rc 0 |
| Author occupancy denominator changed from 2 to 3 | rejects, rc 1 | false `pass`, rc 0 |
| Author triangle target offset by `1/10` | rejects, rc 1 | false `pass`, rc 0 |
| Independent one-sided sign coding changed from `ab` to `ac` | rejects, rc 1 | false `PASS`, rc 0 |
| Independent direct physical count incremented by one | rejects, rc 1 | false `PASS`, rc 0 |
| Independent section correlation doubled | rejects, rc 1 | false `PASS`, rc 0 |
| Author-script hash in the manifest replaced by all zeros | rejects, rc 1 | false `PASS`, rc 0 |
| Saved author density changed to 300, with its manifest hash updated | rejects, rc 1 | false `PASS`, rc 0 |
| Saved author results file missing, while still manifest-listed | rejects, rc 1 | rejects, rc 1 |

Totals: **20 source negative runs; 10/10 normal rejections; 1/10 optimized rejections; 9/10 optimized false successes.** Every raw record, including failures, is retained in `records/`; private mutant sources stay in `private/replays/`.

The bad marker output explicitly lists `(0,1)` and `(1,2)` while reporting `pass`. The wrong-weight output reports density `17/6`, zero autocorrelation `103/36` and origin Bragg mass `289/36` while reporting `pass`. The optimized replay-result mutant claims “identical results” even though the expected saved result says density 300. A deliberately missing expected file still raises `FileNotFoundError` during the unguarded hash comprehension; this observed failure is counted as rejection, not successful mathematical verification.

Required repair **RR1**: preserve the frozen artifacts and add a supported verification entry point whose controlling comparisons use explicit exceptions. Alternatively, explicitly reject optimized execution before any output or count is emitted, force the child interpreter into an unoptimized environment, and make that protected runner the documented interface. Pin the child's interpreter, rather than selecting an unrelated `python3` from PATH. Include wrong-marker, wrong-correlation, wrong-flow, hash-mismatch and saved-result-mismatch negatives in both environment modes; issue PASS only after those mathematical and integrity checks actually execute. A wrapper that merely checks the subprocess return code while inheriting optimization does not repair the defect.

## Independently authored exact controls

`exact_controls.py` imports neither supplied checker. It represents occupancies as finite sign polynomials, reduces squared signs algebraically, applies only the stipulated first/second RS moments, and factors x/y moments according to the independently translated product action. Thus it does not assume IID positions within either RS sequence. Its explicit `require` exceptions remain active under optimization.

It checks:

- The directed residue marker and minimum squared slot separation `1/50`; all 256 choices of four row and four column signs, after the noninteger translation `(-7/30,11/30)`, decode exactly their anchors and signs.
- 2,704 motif-pair moment identities over integer offsets from −6 to 6, 169 weighted identities and 169 product-observable identities.
- Density `3`, physical self-pair mass `3`, decomposition self-pair mass `3` and origin Bragg mass `9`, computed through separate expressions.
- 3,007 rational times using exact equal-length phase bins rather than the triangle overlap expression, 289 direct planar section integrations and 3,249 suspension cocycle checks. Negative time, integer time, seam-adjacent phase bins and time addition are included.

`run_exact_controls.py` runs the checker normally and with inherited optimization. Both pass with identical stdout. Five deliberate bad variants—ambiguous marker, wrong mean input, wrong normalization, wrong floor shift and wrong cocycle—are rejected in both modes, for **10/10 actual negative rejections**. `records/independent_exact_controls.json` preserves all stdout/stderr and return codes.

## What is and is not established mathematically

The source's finite physical samples have densities 3.125, 3.125 and 3.0625. These are not the exact limiting density 3. Its finite count comparison keeps the boundary and mean terms, and its errors relative to the infinite formula are honestly reported. I found no finite/infinite substitution or normalization contradiction.

The author's sign enumeration is legitimate for the particular degree-two occupancy products: balanced binary variables with zero pair correlation have the needed two-variable moments. It does not justify arbitrary higher-order independence, and the proof does not require that stronger premise. Independent coordinate translations justify the product measure even when chosen deterministic x/y sequences coincide.

The algebra gives the same autocorrelation: periodic motif autocorrelation plus `1/4` times each coordinate-axis comb. Fourier transformation exchanges a coordinate delta at zero with Lebesgue measure in that coordinate, so the physical continuous terms lie on countably many horizontal/vertical lines. Ambient two-dimensional Lebesgue measure gives that union measure zero. The marker identifies the anchor phase and signs, preserving the product observable on the physical hull. Exact section integration gives `(1-|t|)_+`; its interval-indicator convolution has Fourier transform `sinc²`. The product density `sinc²(k1)sinc²(k2)` has total mass one by Parseval and is positive almost everywhere. These analytic observations agree with the proof, rather than being conclusions of a finite sample.

The infinite ingredient still comes from strict ergodicity and the RS correlation theorem, freshly checked in its cited primary source. No finite 262,144-site test proves it. The source recurrence provides a finite seed argument (`b1=b1/4`, `a1=-b1/4`) and then smaller-index induction for the vanishing coefficients; the bilateral substitution/recursion bridge agrees with the supplied controls. The hull conjugacy and unique-ergodicity arguments were checked for compatibility with the concrete marker/action formulas, but this family does not claim a universal counterexample search, exhaustive historical survey or proof of a one-dimensional conjecture.

No additional central mathematical gap was identified by this family. The exact remaining repair is the reliability of the executable success/integrity claims under optimization. No outside individual was contacted, and no outreach, publication or remote mutation was performed.

## Replay and seal

From this review directory:

```text
python3 run_reproduction.py
python3 run_exact_controls.py
python3 download_sources.py
python3 fetch_frozen_blobs.py
```

Source downloads and mutant package copies are private and excluded from the positive public manifest. `PUBLIC_FILES.json` positively enumerates only authored report/result/log/code and generated audit records, with their byte lengths and SHA-256 hashes; it excludes itself to avoid a circular digest. The report's 100% checkpoint means this assigned review is complete, not that the discovery is novel or externally certified.
