# Independent computation and adversarial reproducibility audit — PR909 / 30001345

Verdict: **the exact algebraic controls and historical outputs reproduce; no computational counterexample to the stated multibranch rough-invariant example was found.** The original integrity program has several permissive release-policy cases. A new standalone pinned verifier closes those cases for this exact immutable snapshot. This is not numerical proof of the analytic deformation, source interpretation, novelty, or the overall `claimed_solved` designation.

## Identity and independence

Bound original: Git head `d186dea31791cd3e8acf6829e0b65d01849623b8`, tree prefix `unsolved_math_prioritization/attempts/30001345/`. All28 snapshot files match the corresponding Git blobs byte for byte; no extra file is present. The outer manifest SHA-256 is `a8376fa67c497c4b31522364ac87163cdd6f5ec42961893981c44f0d95f0ee02`; proof SHA-256 is `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b`.

The initial `independent_exact.py` reconstruction used only the claimed equation/proof and charter before any historical checker or saved PASS/result was read. It uses SymPy radicals in Q(sqrt(-3)), canonical projective cross products, full incidence substitution and independent Jacobian substitutions, importing no original code. Later n2/generic-line additions were made after reading historical code and are explicitly supplementary. Original code, predicates, saved outputs and source metadata were then inspected. All executions of original programs and all mutations were in disposable copies under this family's explicit TMPDIR. The original snapshot was never executed or modified and was compared again against Git after reproduction.

## Exact reconstruction

Put omega=(-1+sqrt(3)i)/2. For each pair of the nine projective line coefficient vectors, compute its cross product, normalize its last nonzero coordinate to1, and substitute the point into every line. This yields twelve distinct points, every one on exactly three lines, and exactly36 line pairs. Nine points have nonzero coordinates; three are coordinate vertices. The linear functional X+2Y+4Z is nonzero at every point. Its substitution into each projective line yields nine different spatial normal directions, with nonzero x coefficient in every case.

The nine displayed linear forms multiply exactly to the three displayed cubic factors of F; no approximation is used. The coefficient of x^9 is -65. At t=1, F, Fx and Fy vanish at each independently enumerated point. Pair enumeration and the fact that a reduced union of distinct smooth lines is smooth away from pair intersections prove completeness; merely checking a finite list of gradient zeros would not prove completeness by itself.

The twelve squared chart norms are, as a multiset,

`{0,1,1/4,2/49,2/31,2/31,2/19,2/19,2/13,2/13,2/7,2/7}`.

Thus their maximum is1, stronger than the proof's bound2. Scaling by any complex t scales squared norms by |t|²; for |t|<1/4 all singularities lie inside radius1/4, hence certainly inside radius1/2. The exact squared distance coefficients for the nine affine component lines are `{0,0,0,1/37,1/13,1/13,1/29,1/17,1/17}`. Multiplying each by |t|² gives its squared distance to the origin, strictly less than1 on the stated disk. These exact line-distance controls support the geometric bound; the analytic boundary-isotopy argument still requires the written geometric proof.

Using the ordinary-point formulas delta_r=r(r-1)/2 and rough_M_r=r-2 gives central(36,7), nearby totals(36,12). The resolution derivation of these formulas is a separate proof obligation handled by the invariant family. My computations apply, rather than assume a machine certification of, that derivation.

Falsification controls: infinity X=0 contains intersection points; perturbing the last projective line changes the model to20 intersection points (twelve doubles and eight triples); removing a line leaves only28 pairs; n=2 has three doubles/four triples with zero rough excess; nine generic lines have36 nodes and rough total0. The central model has nine branches and therefore fails a unibranched hypothesis. Fine-M behavior is not computed or inferred.

## Universal Fermat extension versus finite computation

The all-n mechanism is checkable independently of any finite loop. Let zeta have exact order n≥3. Distinct A_i meet at one coordinate vertex, and likewise for B and C; these have multiplicity n. An A_i–B_j pair meets at [zeta^(i+j):zeta^j:1], a point also on exactly C_(-i-j). The third coordinate1 makes distinct j and then distinct i distinguish the n² points, none of which is a vertex. Every cross-group pair occurs exactly once in these triples, and every same-group pair occurs at its group's vertex. Hence all pairs are exhausted and multiplicities are exactly as claimed. The modulus bound |zeta^(i+j)+2zeta^j+4|≥1 is uniform for all n. The polynomial leading coefficient of the analogous scaled equation is (-1)^n 4^n-1, always nonzero for n≥1; the same graph-component reasoning can therefore be used in the analytic proof.

The exact symbolic identities are

`3*n*(n-1)/2 + 3*n² = (3*n)*(3*n-1)/2`,

`3*(n-2) + n² - (3*n-2) = n²-4`.

They establish invariant arithmetic for the structural incidence argument. The original range3…100 is only a finite regression diagnostic, not a proof of the universal quantifier. The strictly positive excess begins at n=3; n=2 is a useful zero-excess boundary control.

## Actual checker predicates and arithmetic

The author checker uses Fraction pairs in Q[omega]/(omega²+omega+1), dictionary sparse polynomials and explicit `require` predicates; its 1,515,405 recorded checks include repetitive finite-Fermat pair controls and deliberate negative-predicate invocations, not that many independent theorems. It checks incidence, direction determinants, infinity, rational squared norms, polynomial identity, integer coefficients, degree/leading coefficient and invariant totals. Its ordinary-point helper does not prove the resolution formula.

Audit A uses a second Fraction-pair field class and assertion predicates, including guards inside arithmetic operations. Under direct -OO, an injected false assertion disappears and its hardcoded `all_assertions_passed: true` still prints: **direct optimized audit A is invalid**. This limitation is already documented in the package. `run_audit_a.py` explicitly rejects -O/-OO and inherited optimization; the supported full verifier clears PYTHONOPTIMIZE/PYTHONPATH and invokes the guarded checker with isolated normal Python. An injected false assertion in a copied audit A propagates through the child and makes `replay()` fail even when the parent is -OO with PYTHONOPTIMIZE2. The original author predicate corrupted to false still fails under -OO.

Audit B uses exact SymPy QQ(sqrt(-3)), affine determinant solving, exact polynomial/gcd/gradient checks and explicit `verify` predicates. It has248 recorded checks, exact rational norm expressions and original perturbed/scope controls. Its child author invocations are part of the historical byte replay. No original mathematical predicate depends on floating tolerance, numerical roots, randomized sampling or mpmath precision. mpmath1.3.0 is imported/version-checked by the publication verifier but is not an arithmetic engine for this proof. Wall-clock seconds in my logs are diagnostic floating values only.

## Reproduction and runtime claims

The entire original verifier passed under normal, -O, -OO and a genuinely inherited PYTHONOPTIMIZE2 invocation (the latter parent was not isolated, so the environment setting took effect). Each full run reproduced byte-identical author outputs, guarded normal audit A, and normal/optimized audit B, and tested rejected optimized audit A launch. Output hashes match the original saved hashes. The original mutation suite detected35 controls, covering each payload, manifests/checksum, missing/unlisted/symlinked files, optimization guards and a real false count assertion.

Current retained runtime: CPython3.14.6, SymPy1.14.0, mpmath1.3.0. Historical documents record Python3.12.14. This audit confirms cross-version output reproducibility on3.14.6; it does not recreate or authenticate the historical Python3.12.14 process. The package pins the two dependency versions by exact string, but does not enforce a Python-version pin. No new environment was installed. Source metadata dates/hashes are retained historical attestations; computations do not authenticate the original HTTP retrievals or visual source inspections. In particular, the metadata openly distinguishes equal extracted text from the30-byte PDF trailer-ID differences, and openly states that one attribution PDF was not redownloaded in audit B. Fresh source authentication belongs to the source/scope family.

## Newly tested integrity boundaries

The original program rejects malformed JSON with a valid recomputed checksum, string schema version, duplicate manifest items, path escaping, internal file/directory symlinks, listed/unlisted FIFOs and an unlisted Unix socket. Special-file tests have three-second timeouts and none hangs. A modified proof plus recomputed outer manifest is rejected by its fixed child manifest. Rewriting proof, child manifest and outer manifest together is still rejected by the hardcoded child-manifest SHA.

The following pass the original integrity-only verifier after an outer checksum rewrite where needed: duplicate JSON schema keys with the valid one last; schema true or1.0; floating problem ID30001345.0; floating byte lengths equal to integers; an extra empty directory; root symlink/.. aliases; arbitrary rewritten scope text; and a rewritten unanchored README paired with its updated outer manifest. These are release-policy/schema gaps, **not a disproof of the mathematics**. The README already states that a trusted commit/manifest digest is required against whole-package rewriting. Root aliases are chiefly an identity-policy choice, not an escape around the internal file allowlist. The outer scope text is not a mathematically certified statement. The core frozen proof/checker remain anchored in the original program unless one also changes the trusted program itself.

## Separate hardened verifier and limits

`hardened_verify.py` embeds all28 fixed Git-authenticated byte lengths/SHA-256 values, including the outer manifest, wrappers, proof, checker and metadata. It admits exactly the three expected child directories and exact files; rejects empty extra directories, any symlink/special entry, relative roots, explicit dot/dotdot root components and escaping paths; rejects symlink roots/ancestors by resolved-path comparison; accepts trailing slashes and repeated separators after pathlib normalization; and uses O_NOFOLLOW/O_NONBLOCK plus a regular-file check before reading. Its JSON parser rejects duplicate keys, NaN/Infinity and malformed JSON; manifest integer fields reject booleans/floats. Its predicates use explicit raises and survive optimization. Optional `--replay` executes the pinned original verifier in an isolated normal child with a180-second limit, then checks pinned inventory/bytes again.

All31 focused controls passed (the original29 plus two spelling-policy controls), including baselines under normal/-O/-OO/inherited2, full replay under optimized parent, schema/manifest rewrites, file and directory negatives, aliases, FIFOs/socket without hangs, and strict-parser negatives. The two added controls confirm accepted trailing-slash and repeated-separator roots without changing verifier behavior. The first sealed16-artifact receipt and manifest digest are preserved in `FIRST_SEAL_HISTORY.json`; the wording refinement changes no mathematical/source-integrity finding. Pinning prevents any modified manifest from redefining the trusted artifact. Original files were left unchanged.

Trust limits: this verifier's reviewed bytes and manifest/source pins must themselves be obtained from a trusted record; it does not create a digital signature, cryptographic identity of the author, configured CI result or proof-assistant certificate. It trusts Python/OS/dependencies and SHA-256, executes the authenticated historical Python, and is not a sandbox. It does not promise defense against a malicious concurrent process racing directory/ancestor replacement or unbounded resource exhaustion. It checks the original release, not arbitrary future edits; future legitimate changes need a new reviewed pin set.

## Remaining gap and disposition

Computational/reproducibility gate: PASS for the exact frozen example and expected arithmetic scope, with a separately supplied hardening remedy for fixed-release verification. No new author proof-search turn or priority literature search was performed. Analytic flatness, finite simultaneous normalization, locality/boundary topology, local invariant convention and primary-source exact-target binding must be accepted only through the independent proof/source families. No claim of newness, present-day openness, unibranched/fine-M resolution or overall acceptance is made by this computation report.
