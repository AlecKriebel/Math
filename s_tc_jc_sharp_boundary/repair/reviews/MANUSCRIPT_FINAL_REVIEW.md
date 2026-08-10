# Final adversarial manuscript review

Date: 2026-08-09  
Scope: `source/paper/main.tex` and the active sharpness-only reproducibility package  
Verdict: **HOLD**

## Executive verdict

The central mathematical construction survived adversarial replay. I found no
P0 defect in the four-leaf pair, the exact stochastic collision, the local
inverse-function argument, or the all-taxa construction as actually used.
Both exact implementations pass, and the independent output is byte-identical
to the locked certificate.

The submission is nevertheless **HOLD**, for three P1 items:

1. the advertised release replay fails because `MANIFEST.sha256` is absent;
2. Lemma 6.1 is false as stated when the set `X` is empty, although the
   all-taxa application satisfies the missing hypothesis; and
3. the strong-to-weak framing does not hold other hypotheses fixed, because
   the exhibited networks also contain a triangle.

No manuscript or release file was edited during this review.

## Evidence replayed

- Read completely: `source/paper/main.tex`,
  `docs/PRIOR_WORK_COMPARISON.md`,
  `docs/THEOREM_CERTIFICATE_CROSSWALK.md`,
  `repair/reviews/SHARPNESS_GATE_REVIEW.md`,
  `reproducibility/verify_primary.py`, and
  `reproducibility/independent/verify_sharpness.py`.
- Also checked the primitive graph instances and the complete locked
  independent certificate.
- The primary symbolic verifier passed under NetworkX 3.6.1 and SymPy 1.14.0.
- The independent verifier passed and regenerated the exact locked SHA-256
  `8d70b47f7ca6bd0b8ea87fab71bf2c6eefb254b410708bbb01ccd3dc0c10b40f`.
- A strict `sd_0` replay with no post-root degree-two cleanup gave, for each
  network, exactly five LSA-valid rootings and exactly two tree-child rootings.
  The sites were `A--B`, `A->C`, `A->F`, `B->C`, and respectively `B--L1` or
  `B--L4`.
- An isolated Tectonic build produced a ten-page PDF byte-identical to the
  active submission PDF, SHA-256
  `af2adac97ef6c53222f64b2acf56bc5db1ed655d6d7b2c72d2676744e30dd56f`.
  All pages were rendered and inspected; there were no undefined references,
  overflow/underflow warnings, clipping, or illegible mathematics.
- The public prior-work descriptions were checked against the version-locked
  local texts and current official metadata. The manuscript makes no
  categorical “first” claim.
- `python3 reproducibility/verify_release.py` exits 1 before running either
  verifier with `AssertionError: MANIFEST.sha256 is missing`.

## P0 findings

None.

## P1 findings

### P1.1 — The documented release replay is not executable

**References:** `source/paper/main.tex:656-657`;
`reproducibility/README.md:28-40`;
`reproducibility/verify_release.py:12-16,40-42`.

The manuscript says that hashes and exact commands are in the package
manifest, and the reproducibility README directs the reader to
`python3 reproducibility/verify_release.py`. The active package has no
`MANIFEST.sha256`, so that exact command fails immediately. The two component
verifiers pass when run directly, but the claimed fail-closed release replay
does not.

**Required repair:** after all submission contents are final, run
`python3 reproducibility/generate_manifest.py`, add the resulting root-level
`MANIFEST.sha256`, and rerun `python3 reproducibility/verify_release.py` until
its final line is exactly:

```text
VERIFIED: all sharpness-release gates passed
```

If a manifest will not accompany the submission, replace
`source/paper/main.tex:656-657` with the following and revise the README and
release driver consistently:

> The independent expected certificate is regenerated from source by the
> commands recorded in the accompanying reproducibility README.

### P1.2 — Lemma 6.1 omits a necessary nonempty-`X` hypothesis

**References:** `source/paper/main.tex:574-606`, especially lines 592-600.

The inverse recovers `u/v` by choosing a character tuple `g_X` with total
character `h`. Such a tuple need not exist when `X` is empty. In that case the
base tensor is a one-leaf tensor and the substituted two-leaf tensor determines
only `uv`; distinct positive pairs `(u,v)` with the same product have the same
image. Thus the stated embedding claim is false in that boundary case.

This does not damage Theorem 1.1: every use there has at least three other
leaves. It does require correction before submission. The phrase “positive
Fourier tensor” should also be qualified because all non-zero-total Fourier
coordinates are forced to zero by equation (1).

**Exact replacement for `source/paper/main.tex:574`:**

> Let $X$ be nonempty, and let $P$ be a normalized Fourier tensor on
> $X\cup\{a\}$ whose zero-total coordinates are strictly positive.

With that replacement, the choice at lines 596-600 exists and the stated
positive analytic inverse is valid.

### P1.3 — The framing does not isolate a strong/weak tree-child boundary

**References:** `source/paper/main.tex:80-83,110-117,135-147,630-643`;
`docs/PRIOR_WORK_COMPARISON.md:27-32,49-60`.

The pair is exactly certified to lie in `W_TC \ S_TC`, but it also contains a
triangle. The cited Englander et al. theorem assumes both triangle-freeness and
strong tree-childness. Consequently, this construction proves failure over the
full weakly tree-child level-2 class, even modulo ordinary triangle
redirection, but it does not show that replacing “strongly” by “weakly” while
retaining triangle-freeness destroys identifiability. The current abstract
wording can be read as making that stronger inference.

**Exact replacement for `source/paper/main.tex:80-83`:**

> The result supplies an exact negative instance among same-type four-leaf
> level-2 comparisons and proves that generic identifiability fails over the
> full weakly tree-child level-2 class, even modulo ordinary triangle
> redirection.

**Exact replacement for `source/paper/main.tex:110`:**

> The pair's location in the tree-child hierarchy is important for the scope
> of the result.

**Exact replacement for `source/paper/main.tex:642-643`:**

> The construction settles neither identifiability inside $\TCs$ nor
> identifiability in the triangle-free subclass of $\TCw$; both remain outside
> the scope of this paper.

## P2 findings

### P2.1 — The independent reducer implements a broader operation than the manuscript's `sd_0`

**References:** `source/paper/main.tex:168-188`;
`reproducibility/independent/verify_sharpness.py:513-519,543-566`;
`repair/reviews/SHARPNESS_GATE_REVIEW.md:69-76`.

The manuscript explicitly forbids post-root degree-two cleanup. The
independent implementation suppresses unlabelled ordinary degree-two vertices
exhaustively. For the accepted binary rootings this loop is inert: strict
replay produced the same census of five rootings, two of them tree-child. The
theorem is therefore unaffected, but the implementation does not literally
implement the claimed convention on arbitrary inputs.

**Repair:** change the reducer docstring to end after binary-root suppression,
delete the cleanup loop at lines 543-566, regenerate the expected certificate,
and update all locked script/certificate hashes. Alternatively, document and
machine-check the invariant that the loop executes zero times; deleting it is
cleaner.

### P2.2 — The all-`n` family is underspecified relative to its certificate

**References:** `source/paper/main.tex:609-627`;
`reproducibility/independent/verify_sharpness.py:1518-1669`;
the locked certificate field `all_n.explicit_family`.

The independent certificate repeatedly replaces leaf 2 and preserves the
leaf-1 triangle-adjacency separator. The manuscript says only to replace “the
same labelled leaf” and then argues that the substituted block itself changes
triangle attachment, which instead suggests replacing leaf 1 or 4. Either
construction proves existence, but the submitted proof should name the same
family as the certificate.

**Exact replacement for `source/paper/main.tex:610-613`:**

> The case $n=4$ is \cref{prop:topology,prop:overlap}. For
> $m=5,\ldots,n$, replace leaf $2$ in both networks by a cherry whose children
> retain label $2$ and receive the new label $m$. Equation \eqref{eq:cherry}
> carries every common base distribution and every common pair $(u,v)$ to the
> same enlarged distribution.

**Exact replacement for `source/paper/main.tex:623-625`:**

> Leaf $1$ remains adjacent to a triangle vertex in $N_n$ and to a
> nontriangle vertex in $N'_n$. This labelled property is preserved by
> mixed-graph isomorphism and by $\Tmove$.

### P2.3 — The reconstruction cross-reference names only the last displayed line

**References:** `source/paper/main.tex:417-425,549-553`.

The `align` environment assigns equations (11)--(13), but
`\label{eq:reconstruction}` is attached only to equation (13), the formula for
`O`. The overlap proof then says equation (13) forces five coordinates. The
five formulas collectively do so.

**Exact replacement for the sentence at `source/paper/main.tex:551-553`:**

> Positivity forces the same value $L=+\sqrt{BEH}$, and the five
> reconstruction formulas in the proof of \cref{lem:geometry} force
> $J,K,M,N,O$.

### P2.4 — One rendered compound has an unintended space

**Reference:** `source/paper/main.tex:125-126`.

The source line break renders as “stacked- reticulation.”

**Exact replacement:** replace `stacked-` followed by the source newline and
`reticulation` with `stacked-reticulation`.

### P2.5 — “Stable ancestor” is used but not defined locally

**Reference:** `source/paper/main.tex:158-166`.

The implemented LSA test is correct: a nonroot vertex is stable for all leaves
exactly when deleting it makes every leaf unreachable from the root. The prose
defines “lowest” through stable ancestry but never defines “stable ancestor.”

**Exact insertion before the LSA requirement at `source/paper/main.tex:163`:**

> A vertex is a stable ancestor of $X$ if it lies on every directed path from
> the root to each labelled leaf.

### P2.6 — Two supporting-review details are stale

**References:** `repair/reviews/SHARPNESS_GATE_REVIEW.md:617-628`;
`docs/PRIOR_WORK_COMPARISON.md:17`.

- The gate-review reproduction command points to the former
  `repair/independent/sharpness/` location. The active files are under
  `reproducibility/independent/`.
- The version-locked Sullivant PDF itself is stamped
  `arXiv:2507.23056v2, 14 Jul 2026` and the manuscript is dated 15 July 2026;
  the comparison table says “dated 2026-07-16.”

**Replacement command for the gate review, run from the release root:**

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 reproducibility/independent/verify_sharpness.py --instance reproducibility/independent/instance.json --output /tmp/stc-jc-sharpness-certificate.json
```

**Exact replacement for `docs/PRIOR_WORK_COMPARISON.md:17`:**

> arXiv:2507.23056v2, submitted 2026-07-14 (manuscript dated 2026-07-15)

### P2.7 — A primary-verifier comment gives the wrong cycle rank

**Reference:** `reproducibility/verify_primary.py:103-106`.

The code and certificates correctly obtain cycle rank two and simple-cycle
lengths 3, 5, and 6. Only the comment says “Cycle rank is three.”

**Exact replacement:** `# Cycle rank is two; in this theta graph the three simple cycles have`

## Mathematical findings that passed

The following requested attack points passed against both implementations and
the locked certificate:

- the rooted bidegrees, acyclicity, LSA condition, tree-child witnesses, and
  compatible retained-edge root insertion;
- exact membership in `W_TC \ S_TC`, with five admissible rootings, two
  tree-child and three non-tree-child;
- standard mixed-graph recovery, one level-2 theta blob, cycle rank two,
  unique triangle, labelled nonisomorphism, and non-ordinary-`T` separation;
- root suppression and the exact product
  `x_AC=x_(rho,A)x_(rho,C)`, with strict positive factorizations;
- Klein-four XOR, all six group automorphisms, all fifteen zero-sum JC orbits,
  and completeness of the fourteen nonconstant representatives;
- all six symbolic identities on both complete parameterizations;
- localized reconstruction on `BE != 0`, irreducibility of
  `L^2-BEH`, dimension eight, and smoothness of the positive sheet;
- the exact smaller root `beta`, its rational isolating interval, every
  `Theta_0` inequality, all fourteen orbit values, all 256 Fourier entries,
  all 256 inverse-Fourier probabilities, and strict pattern positivity;
- both factored rank-eight Jacobian minors and the inverse-function argument:
  the first eight coordinates give overlapping open neighborhoods, positivity
  selects the same `L` sheet, and the reconstruction formulas force the
  remaining coordinates;
- the conclusion that ambiguity has a Euclidean-open preimage in the source
  parameter space and is not confined to a proper algebraic exceptional set;
- the cherry formula, its positive analytic inverse under the repaired
  nonempty-`X` hypothesis, the `+2` dimension increment, and induction to
  dimension `2n`;
- persistence of binary level two, weak-but-not-strong tree-childness,
  labelled nonisomorphism, and non-`T` separation for all `n`; and
- the restrained instance-level prior-work comparison. No unsupported global
  priority or complete-classification claim was found.

## Final binary verdict

**HOLD**

The central theorem appears mathematically correct, but the package is not
submission-ready until all P1 items are repaired and the fail-closed release
command passes. The P2 items should be corrected in the same finalization pass
because several concern exact correspondence among manuscript, verifier, and
certificate rather than mere style.
