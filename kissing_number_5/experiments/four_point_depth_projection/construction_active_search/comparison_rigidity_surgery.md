# Independent comparison of rigidity and hard-surgery endpoints

## Status and method

This is a floating-point cross-audit, not a construction certificate or an
upper bound.

The coordinate arrays in `rigidity_softmode_results.json`,
`surgery_best_configurations.json`, and the original round-9/round-6 inputs
were read independently of both discovery programs.  Every row was
renormalized, and all pair products were rescanned directly.  The comparison
then used:

- the sorted multiset of all off-diagonal Gram entries;
- the five eigenvalues of \(X^{\mathsf T}X\);
- active graphs at \(10^{-8},10^{-6},10^{-4}\) below each array's own
  maximum, including degree multisets, component sizes, and triangle counts;
- color refinement and exact backtracking on the active graph when an
  isometry remained plausible;
- orthogonal Procrustes after the recovered vertex assignment.

Here “the same” means numerically identical up to the displayed errors.  It
does not assert an exact-real isometry.

## Main conclusions

1. The rigidity and surgery \(N=43\) endpoints are the **same numerical
   configuration up to relabeling and an \(O(5)\) reflection**.  Two
   materially different searches independently reached the same basin.
2. The recovered \(N=43\) configuration is not isometric to the original
   stored \(N=43\) input.
3. The surgery \(N=44\) endpoint is exactly the original stored input after
   canonical normalization.  The rigidity \(N=44\) endpoint is a **distinct,
   better numerical basin**.
4. The \(N=41\) edge-release experiment shows that 48 particular
   one-dimensional release trajectories return to the same 35-point core.
   Its scope is far too narrow to imply a universal local or global
   obstruction.

## Independently recomputed objectives

The hexadecimal fields specify the literal binary64 results of the direct
rowwise scan.

| \(N\) | endpoint | maximum | binary64 hexadecimal |
|---:|:---|---:|:---|
| 43 | stored input | 0.5247244770145227 | `0x1.0ca8afc8604bep-1` |
| 43 | surgery | 0.5247096018292908 | `0x1.0ca6bca7820a7p-1` |
| 43 | rigidity | 0.5247096018290192 | `0x1.0ca6bca781718p-1` |
| 44 | stored input | 0.5274711925359574 | `0x1.0e10b4430c512p-1` |
| 44 | surgery | 0.5274711925359574 | `0x1.0e10b4430c512p-1` |
| 44 | rigidity | 0.5274577123235322 | `0x1.0e0eeff0e7b44p-1` |

The rigidity improvements over the stored arrays are

```text
N=43  1.4875185503582244e-05
N=44  1.3480212425198701e-05
```

The \(2.716\times10^{-13}\) difference between the two recovered \(N=43\)
objectives is solver-level variation within one configuration, as the full
isometry audit below demonstrates.

## \(N=43\): the recovered endpoints coincide

At tolerance \(10^{-8}\), the stored and recovered graph invariants are:

| endpoint | edges | degree histogram | components | triangles |
|:---|---:|:---|:---|---:|
| stored | 172 | \(5^8 6^6 7^8 10^{20} 12^1\) | \(43\) | 132 |
| surgery | 169 | \(5^8 6^{12} 7^2 9^6 10^8 11^6 12^1\) | \(43\) | 126 |
| rigidity | 169 | \(5^8 6^{12} 7^2 9^6 10^8 11^6 12^1\) | \(43\) | 126 |

The surgery and rigidity graphs remain identical under the same assignment
at \(10^{-6}\).  At \(10^{-4}\), both have 175 edges and again agree exactly.

Color refinement followed by adjacency-preserving backtracking found the
following permutation, mapping rigidity vertex \(i\) to surgery vertex
\(p_i\):

```text
[7, 1, 28, 42, 3, 4, 14, 29, 0, 8, 19, 10, 22, 18, 16,
 5, 31, 13, 17, 12, 9, 20, 21, 11, 23, 24, 25, 27, 26,
 2, 6, 30, 15, 32, 33, 40, 37, 34, 36, 41, 39, 35, 38]
```

After this relabeling:

```text
active-graph symmetric difference, 1e-8     0
active-graph symmetric difference, 1e-6     0
active-graph symmetric difference, 1e-4     0
maximum absolute Gram discrepancy            3.829436767688321e-13
RMS Gram discrepancy                         1.388162737489115e-13
Procrustes coordinate RMS                     7.537053927377429e-14
maximum Procrustes row residual               2.396243078861255e-13
determinant of fitted orthogonal map          -0.9999999999999991
```

The reflection determinant is harmless because spherical-code isometry
allows all of \(O(5)\), not just \(SO(5)\).

The permutation-free sorted Gram comparison gives maximum discrepancy
`3.795574965437254e-13` and RMS discrepancy
`1.389005263600500e-13`.  These errors are roughly eleven orders of
magnitude smaller than the changes from the stored input:

```text
recovered versus stored sorted-Gram max       0.0139596928593
recovered versus stored sorted-Gram RMS       0.00336390888825
recovered versus stored frame-spectrum max    0.000912957909
```

Thus the two recovered arrays are numerically isometric, while the stored
array is not.  Both searches began from the stored array and converged to
the same more fully equilibrated endpoint.

The independently recomputed frame spectra are:

```text
stored
8.398831498874175  8.411565372183214  8.411565372183516
8.411565372184365  9.366472384574724

surgery
8.397918540964284  8.411148321509099  8.412113667976128
8.412113667982014  9.366705801568475

rigidity
8.397918540964914  8.411148321507017  8.412113667979616
8.412113667979625  9.366705801568827
```

## \(N=44\): rigidity reaches a distinct basin

The surgery-selected array and the stored round-6 input have zero Gram and
sorted-Gram discrepancy after identical normalization.  Their Procrustes
coordinate RMS is `4.07e-16`; the maximum row residual is `1.34e-15`.
Consequently the surgery output is simply the stored endpoint, up to
normalization roundoff.

The rigidity endpoint is not isometric to it.  Already the \(10^{-8}\)
active degree multiset rules out graph isomorphism:

| endpoint | edges | degree histogram | components | triangles |
|:---|---:|:---|:---|---:|
| stored/surgery | 182 | \(6^4 7^4 8^{16} 9^{16} 10^4\) | \(44\) | 80 |
| rigidity | 190 | \(6^4 7^2 8^8 9^{24} 10^4 11^2\) | \(44\) | 96 |

These graphs and counts are unchanged at \(10^{-6}\) and \(10^{-4}\).
Permutation-independent continuous invariants also separate the arrays:

```text
sorted-Gram maximum discrepancy       0.012082915325551946
sorted-Gram RMS discrepancy           0.002740170456917198
frame-spectrum maximum discrepancy    0.0007369463592965531
```

The frame spectra are:

```text
stored/surgery
8.591207584335592  8.638240736552042  8.638240736552044
9.059275580015976  9.073035362544353

rigidity
8.591432450170487  8.637649209469162  8.637649209469167
9.059496821987537  9.073772308903649
```

Hence the rigidity soft-mode perturbation crossed from the 182-contact
stored basin to the better 190-contact basin.  The hard-surgery portfolio
did not make that transition.

## Scope of the \(N=41\) edge-release negative result

The extracted \(10^{-8}\) graph has a 35-vertex, 153-edge core and six
isolated vertices.  After adding 35 tangency rows and ten rows fixing the
ambient rotational gauge, the core rigidity matrix has numerical rank 175
and nullity zero.

Each of eight deterministic trials deleted exactly 24 of the 153 contact
rows.  The retained matrix then had shape \(174\times175\), numerical rank
174, and a one-dimensional gauge-fixed nullspace.  Both signs and the three
scales `0.03`, `0.15`, and `0.40` were tested, giving 48 trajectories.
All 48 direct epigraph SLSQP calls reported success.

Independent rescanning found:

```text
baseline maximum                         0.5149946525121660
smallest refined trial maximum           0.5149946525121667
largest refined trial maximum            0.5149946525121771
initial escaped maxima                   0.5264313630009032
                                      to 0.8838904743915191
selected null residual 2-norm            1.26e-15 to 5.91e-15
```

After polishing, every 35-point core returned to its original labeled Gram
matrix to within `4.44e-14`; the worst Procrustes row residual was
`3.54e-14`.  The full 41-point arrays did not all return to one isometry
class: their six rattlers moved substantially, producing whole-code sorted
Gram discrepancies as large as `0.05391`, and some acquired additional
near-active contacts.  Thus the experiment supports the narrow statement
that these 48 released directions snap the active core back to the same
numerical core while allowing rattler rearrangement.

It does **not** establish that:

- all contact-row releases fail—there are
  \[
  \binom{153}{24}
   = 6500547004806930858853932225
  \]
  raw deletion sets, of which only eight were sampled;
- deleting a different number of rows, using a higher-dimensional released
  space, or combining several modes cannot escape;
- a nonlinear or second-order direction invisible to the selected
  first-order null vector cannot improve;
- a different active threshold gives the same framework;
- the binary64 ranks and singular vectors are exact;
- a successful local SLSQP return excludes another local or global basin;
- every hypothetical 41-point code contains this 35-point core.

Moreover, the 24 omitted contacts were restored as constraints in the final
epigraph problem.  The deletion therefore defines only an initial escape
direction; it is not a relaxation of the actual spherical-code problem.
The result is useful basin evidence, not a rigidity theorem or an
obstruction to 41 points.
