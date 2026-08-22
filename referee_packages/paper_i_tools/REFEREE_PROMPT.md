# Neutral AI-referee prompt

You are acting as an independent journal referee for a mathematical-biology
manuscript and its computer-assisted proof package. You have not been told
whether the results are correct. Treat the manuscript, source comments,
expected terminal output, saved hashes, provenance notes, and any prior audit
language as claims to be checked, not as evidence of correctness. Reach your
own verdict: fully validated, valid after minor corrections, major correction
required, or invalid.

Work only on a disposable copy of the delivered package, preferably in an
unprivileged sandbox or container with no personal credentials. Do not contact
any person, upload any file, or change any external system. If dependency
installation is needed, restrict network access to the configured package
index and, only for document rendering, Tectonic's standard resource-bundle
endpoint. Prefer preseeded caches. Record every command, exit status, software
version, and independent calculation used in the review.

## 1. Establish package identity and scope

1. Read `README_FIRST.md`, `VERSION.md`, and `PACKAGE_MANIFEST.sha256`.
2. Independently verify the package manifest, the detached source-archive
   checksum, and the archive's internal `MANIFEST.sha256`. Confirm that the
   extracted tree is byte-identical to the archive payload and that the
   convenience PDF is byte-identical to the PDF inside that tree.
3. Read the compiled paper and its LaTeX source, including all appendices and
   references. Make a theorem ledger recording every hypothesis, quantifier,
   equality case, finite range, analytic range, and stated limitation.
4. Determine whether kernel indexing is target-by-source and consistent with the
   death--Birth transition rule, incoming-column rescaling is dynamically
   irrelevant, and the complete-graph baseline is correct.
5. Keep these boundaries explicit: each local result is for fixed population
   size and may have a size-dependent neighborhood; each strong-selection
   result is for a fixed structure as fitness tends to infinity; the paper
   does not claim global maximality at fitness two, a uniform local radius, or
   the nonexistence of growing amplifying families.

## 2. Verify the mathematics independently

Do not infer a proof from a successful program run. Re-derive each
theorem-bearing step, checking definitions, dimensions, normalization,
strictness, endpoint coverage, and equality cases.

### Fitness-two dual and local theorem

- Derive the fair-geometric OR representation directly from
  \(2x/(1+x)\).
- Verify the finite union dual, irreducibility and aperiodicity on proper
  nonempty ancestral sets, the completely alternating coverage formula, and
  \(\rho=m(P)/n\).
- Check the rectangular phase spaces \(\mathcal Z_n\) and \(\mathcal Y_n\),
  including singleton stopping to the empty cache. Verify the domains and
  codomains of \(A\) and \(R\), the order in \(K=RA\) and \(M=AR\), both
  stationary phase laws, uniqueness, and the collision identity
  \(\nu H=1/m(P)\).
- Re-derive the stationary perturbation expansion, vanishing first
  variation, and the sign conversion from inverse-mean curvature to fixation
  curvature.
- Verify the complete tangent-space decomposition, its dimensions,
  orthogonality, irreducibility, multiplicities, and physical norm
  conversions.
- With \(N=n-1\), check the standard sector for \(2\leq N\leq9\) and
  \(N\geq10\); the antisymmetric coupling and positivity for every
  \(N\geq2\); and the symmetric sector for \(3\leq N\leq39\), every integer
  \(40\leq N\leq287\), and \(N\geq288\). Confirm that there is no endpoint
  gap and that finite computation is not used to infer an infinite range.
- Independently check the claimed exact minimum margin at \(N=40\), the
  large-order strict bounds, the certificate hash printed in the appendix,
  and the displayed normalized eigenvalues for \(n=3,4,5\) from literal
  active chains.

### Strong selection and low-order results

- Re-derive the complete-support \(1/r\) expansion and the coefficient
  \(\mathcal E_{\rm dir}/[n^2(n-2)]\). Check the raw-weight versus normalized-
  kernel identity, scale invariance, and equality class.
- Check the hypotheses and conclusion of the cited noncomplete-support result
  against the cited source, and separately verify the reducible
  source-component argument.
- Verify the undirected strong-selection limit and its graph-theoretic
  consequence.
- Reconstruct the weighted-triangle transient chain and centered
  sum-of-squares factorization, including denominator positivity and equality
  only at equal weights for \(r>1\).
- Reconstruct both symmetric weighted-\(K_4\) lumpings, denominator
  certificates, coefficient signs, parameter domains, and equality cases.
- Check fitness monotonicity and all boundary cases relevant to the stated
  results, including \(n=2\), the absent symmetric sector at \(n=3\), zero-
  support boundaries, and \(r=1\).

## 3. Audit the software before running it

Use `CLAIM_CODE_MAP.md` as an index, not as evidence. Before executing any
delivered code, inspect `run_all_referee_checks.sh`,
`verify_referee_package.py`, `submission/bootstrap_replay.sh`, `replay.sh`,
`build.sh`, every program invoked directly by the replay, and every imported
helper actually used by those programs. For every theorem-bearing check,
identify the exact manuscript statement it checks and determine whether the
code checks that statement rather than a weaker surrogate.

In particular, check that:

- state enumeration is exhaustive and state typing is correct;
- row/source orientation and normalizations match the manuscript;
- exact rational or symbolic arithmetic is used whenever exactness is
  claimed;
- random, sampled, or floating-point checks do not carry an infinite
  quantifier;
- every finite size range is exhaustive, including endpoints;
- hard-coded expressions are independently derived rather than copied as
  both premise and expected answer;
- failures propagate to a nonzero exit status, including under hostile
  optimization/import/build environment settings;
- the replay reaches every load-bearing verifier, and documentation
  distinguishes called helper functions, module imports, and guarded mains;
- purportedly independent cross-checks do not merely share the same
  potentially faulty implementation.

Some programs print `OPEN` notices about stronger global fitness-two
questions. Determine whether those open questions are outside the paper's
claims and whether any stated theorem depends on them; do not automatically
count the notices as either failures or successes.

## 4. Execute and independently cross-check

After completing the source audit, run `./run_all_referee_checks.sh` from the
package root with a Python 3.14.6 interpreter (set `BOOTSTRAP_PYTHON` if
needed). Preserve the full transcript and exit status. This command verifies
the manifests, requires the stated document-tool versions, creates a
disposable source copy, installs the pinned Python dependencies, runs the unit
suite and all replayed verifier programs, rebuilds the PDF, and compares it
with the delivered PDF. If a required tool is unavailable or has the wrong
version, record that limitation and run the remaining checks manually rather
than reporting a complete execution.

Then perform independent spot checks not encoded by the supplied expected
answers: use several nonsymmetric small kernels, reconstruct selected
low-order weighted examples, and calculate at least one representative case
in each Hessian sector by an alternative formulation or implementation.

## 5. Report

For each finding, give severity, exact theorem/page/equation or file/line,
reasoning, and a counterexample or reproduction command where applicable.
Distinguish mathematical defects, code defects, reproducibility defects,
exposition issues, and optional suggestions.

Your final report must include:

1. a theorem-by-theorem validation table;
2. a claim-to-code coverage and execution table;
3. package, environment, command, and exit-status records;
4. all unresolved assumptions or checks you could not perform;
5. an explicit assessment of whether the mathematical proof and the software
   independently support the same claims; and
6. one verdict: **fully validated**, **valid after minor corrections**,
   **major correction required**, or **invalid**.

Use **fully validated** only if your independent mathematical audit, code
inspection, complete execution, and cross-checks all support every stated
result. Do not treat this prompt, prior successful output, or the authors'
conclusions as evidence for that verdict.
