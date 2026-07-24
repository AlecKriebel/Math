# Independent adversarial audit of the rigidity soft-mode artifacts

## Verdict

The stored coordinate maxima, hashes, best-run selections, and improvement
flags are correct.  The principal numerical structural claims also reproduce
under a different tangent-space formulation:

- the 35-vertex N=41 active core is numerically infinitesimally rigid modulo
  rotations;
- N=43 is full rank modulo rotations but has three well-resolved soft
  singular directions; and
- N=44 has one numerical nonrotational null direction and a separate
  near-null direction.

The top-level label
`NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE` is appropriate.  These artifacts
do not produce a configuration at the kissing threshold.

There is one material checker-coverage gap: `rigidity_verify.py` verifies
coordinate records, their hashes and maxima, and the final Boolean flags, but
it does **not** verify the rigidity `structure` records, mode ranks/residuals,
or the baseline coordinates against their named source artifacts.  A test
changed the claimed N=41 core rank to zero, a claimed N=43 mode rank to zero,
and the N=43 baseline maximum to 0.6; the checker still returned
`all_checks_passed: true`.  This does not falsify the stored claims, because
they were independently recomputed below, but “all checks passed” must not be
read as a structural verification.

## Independent coordinate audit

The audit did not import `rigidity_softmode_search.py`.  It independently
renormalized every one of the 102 trial coordinate arrays and all four stored
best arrays, reconstructed every unordered inner product, and recomputed each
literal-coordinate SHA-256 hash.

All hashes and maxima agree with the result JSON.  An 80-digit Decimal
enumeration of the normalized binary64 best arrays gives:

| N | independently recomputed maximum | improvement from baseline |
|---:|---:|---:|
| 41 | 0.5149946525121658411544387801870467625 | 0 |
| 42 | 0.5182411558622623199256249658599895568 | 0 |
| 43 | 0.5247096018290191490779720653565218140 | 0.0000148751855034712 |
| 44 | 0.5274577123235321672934858964600345984 | 0.0000134802124251987 |

The N=43 best array is exactly the stored trial
`N43_tail1_sign-1_scale0.15`; the N=44 best is exactly
`N44_tail3_sign1_scale0.01`.  For N=41 and N=42 the retained best arrays are
the independently loaded baselines.  The `beat_baseline` flags
`false,false,true,true` and all four `reached_half: false` flags are correct.

The diagnostic maximizing pair should not be treated as unique or
high-precision data.  In N=41, for example, the Decimal-best pair differs from
the NumPy diagnostic pair by only \(5.82\times10^{-17}\); N=43 has a similar
\(2.80\times10^{-17}\) ordering change.  The maximum values themselves remain
correct at the precision claimed.

There is one unsuccessful SLSQP trial:
`N44_tail1_sign-1_scale0.1`, status 8, “Positive directional derivative for
linesearch.”  Its failure is present in the JSON, it is not selected as a
best result, and its coordinates and recomputed maximum are internally
correct.  The independent checker does not require solver success; this is
harmless for checking the returned coordinates but should be remembered when
summarizing the optimization run.

## Independent rigidity computation

For each point \(x_i\), the audit constructed an independent orthonormal
\(5\times4\) tangent basis \(B_i\).  For every active edge \(ij\), it formed
the tangent derivative row

\[
  (x_j^\mathsf{T}B_i)\,u_i+
  (x_i^\mathsf{T}B_j)\,u_j.
\]

It then explicitly generated the ten ambient rotational velocities,
orthonormalized their span, and restricted the derivative matrix to its
orthogonal complement.  This is mathematically equivalent to, but
implemented differently from, the search program's ambient-coordinate
matrix with norm and rotation rows.

### N=41

At the stated active tolerance \(10^{-8}\), there are 153 active edges, all
on vertices 0 through 34; vertices 35 through 40 have active degree zero.
For the 35-vertex core:

- the tangent derivative has shape \(153\times140\);
- its rank is 130, with precisely the ten rotational null directions;
- after quotienting rotations, its shape is \(153\times130\), its rank is
  130, and its smallest singular value is
  \(0.13258015741904078\).

This strongly confirms numerical infinitesimal rigidity at the selected
coordinates and active threshold.  All eight stored edge-release choices
delete 24 distinct valid core edges.  Their retained \(129\times130\)
quotient matrices independently have rank 129, hence one nonrotational
tangent flex.  The stored augmented shapes \(174\times175\), ranks 174, and
nullities one agree.

### N=42

There are 173 active edges and exactly two active-degree-zero vertices.  The
rotation-quotiented derivative has shape \(173\times158\), rank 150, and
nullity eight, agreeing with the interpretation that the two inactive points
supply eight tangent motions after rotations are removed.

### N=43

There are 172 active edges and no inactive vertices.  The quotient derivative
is \(172\times162\) and has full rank 162.  Its three smallest singular values
are approximately

\[
4.2303591\times10^{-8},\quad
1.2973768\times10^{-7},\quad
2.8711587\times10^{-7}.
\]

They are far above roundoff yet far below the next singular value
\(0.18538\), so “soft modes” is a fair numerical description.  They are not
exact flexes.

### N=44

There are 182 active edges and no inactive vertices.  The quotient derivative
is \(182\times166\), with numerical rank 165.  Its smallest singular value is
\(5.16\times10^{-16}\), followed by
\(1.5052612\times10^{-6}\), while the next is \(0.02303\).  This independently
reproduces one numerical nonrotational null direction and one separate soft
direction.

## Checker attacks

The checker correctly rejected each of the following independent mutations:

- changing one stored coordinate without updating its hash;
- changing a coordinate hash;
- changing a reported maximum by \(10^{-5}\);
- flipping `reached_half`; and
- flipping `beat_baseline`.

It intentionally or inadvertently accepted mutations to:

- `run["structure"]`;
- every `trial["mode"]` claim; and
- a baseline maximum when `beat_baseline` was changed or remained
  consistently true.

It also does not bind each `origin` locator to a source-file hash.  A stronger
artifact verifier should load and hash the four baseline sources and
independently rebuild the active graphs and quotient rigidity matrices.

## Labeling cautions

The result's global numerical-only status prevents a mathematical
overclaim.  Two local phrases nevertheless require care:

1. “contact” means within \(10^{-8}\) of the *current minimax maximum*
   (roughly 0.515–0.527), not an actual kissing contact at inner product
   \(1/2\);
2. “rigid” and “genuine null mode” are binary64 statements about one
   tolerance-defined active graph, not exact algebraic rigidity theorems,
   jamming statements, or obstructions to motions that change the active
   graph.

With those qualifications, the method and result labels are sound.

## Reproduction

From the repository root:

```text
./.venv/bin/python \
  experiments/four_point_depth_projection/construction_active_search/audit_rigidity_tests.py -v
```

All seven audit tests pass.  One of the seven is deliberately a checker-scope
test showing that structural tampering is currently accepted.

Audited artifact hashes:

- `rigidity_softmode_results.json`:
  `3dfbaf1cc27c504d53412490031307ee50a6e7065bfdb6fe02789f9c9d495c78`;
- `rigidity_verification.json`:
  `2a4ca72f4a0694cdb54152d40ec4ae677694f32aec4e34eb8b7728e4e05004c1`.
