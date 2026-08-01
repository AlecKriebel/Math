# Active-cut test of the degree-three DTH Gamma-A cone

## Scope

This note records a floating-point discovery calculation for the degree-three
extension of the exact five-replica DTH pseudomoment.  It does **not** prove
that the extension is PPT, that the fixed marginal is PPT-extendible, or that
DTH holds.  Its purpose is to decide whether the first crossed defects are
affine obstructions and to provide a reproducible coupled-cone solver.

The source variable is the 171-component site-symmetric representation of a
positive degree-three Grassmann moment (T).  Its five-replica marginal is
fixed.  The second cone is

\[
T^{\Gamma_A}\succeq0.
\]

The prolonged support face need not be imposed separately: positivity of
the crossed moment and exact descent to the already constrained marginal
force that face automatically.

## Crossing and active pullback

For a local holomorphic type \(\lambda\), mixed type \(\mu\), and crossing
block \(L_{\mu\lambda}[p,q,a,d]\), reshape

\[
C_{(p,a),(q,d)}=L_{\mu\lambda}[p,q,a,d].
\]

The numerical Choi decomposition is

\[
C=\sum_h \gamma_h |K_h\rangle\langle K_h|.
\]

Every nonzero local block has retained Choi rank at most twelve.  Therefore
the three-site crossing of a source factor (F_{abc,k}) is evaluated as a
signed sum of Gram matrices rather than by the prohibitive raw six-index
contraction.  The largest local reconstruction error is

```text
6.481607690730902e-15.
```

For a negative mixed eigenvector (v_{prt}), the adjoint cut is obtained by

\[
y_{abc}^{h_1h_2h_3}
=\sum_{p,r,t}
K_{h_1}[p,a]K_{h_2}[r,b]K_{h_3}[t,c]v_{prt},
\]

followed by the signed sum of (yy^T), compression into each reconstructed
post-Omega source union, and the site-orbit adjoint.  All pulled-back cuts in
the calculations below replay their direct crossed eigenvalues to absolute
error below (6\times10^{-23}); the first seven replay below
(4\times10^{-24}).

## Coupled-cone iteration

For a finite cut list (g_j), the inner problem is

\[
T\succeq0,\qquad A(T)=b,\qquad \langle g_j,T\rangle\ge0.
\]

The implementation uses Dykstra projection for source PSD plus the cut
half-spaces and Douglas--Rachford splitting against the fixed-marginal affine
space.  After convergence, the candidate is crossed again; materially
negative eigenvectors become the next cuts.  At most the globally strongest
fifteen directions, with one direction per block, are added in each outer
round.  This cap prevents the finite-cut projection itself from becoming the
computational bottleneck.

## Numerical results through round six

The PSD-only Slater candidate first exposed four defects at mixed dimensions
at most one hundred:

\[
\begin{array}{c|c|c}
\text{block}&\text{dimension}&\lambda_{\min}\\ \hline
(1,2,9)&44&-7.51327984\,10^{-10}\\
(1,4,9)&55&-7.37392969\,10^{-10}\\
(0,2,5)&96&-4.68887150\,10^{-11}\\
(1,4,6)&100&-5.72589888\,10^{-11}.
\end{array}
\]

The four-cut problem is feasible numerically.  After adding three rotated
directions, the seven-cut candidate is source-positive and every block of
dimension at most one hundred is nonnegative to the material threshold
(10^{-15}).

The cap-500 crossing then reveals a larger family of negative blocks.  The
following table gives aggregate crossed defects after successive batches of
fifteen active cuts.  Eigenvalues below (-10^{-15}) are counted.

\[
\begin{array}{c|c|c|c|c|c}
\text{round}&\#\text{ cuts}&\#\text{ blocks}&\#\text{ eigs}
&\min\lambda&\|\lambda_-\|_2&\|\lambda_-\|_1\\ \hline
2&7&41&110&-7.96363\,10^{-9}&1.73397\,10^{-8}&1.02390\,10^{-7}\\
3&22&41&110&-4.32814\,10^{-9}&9.40388\,10^{-9}&5.77827\,10^{-8}\\
4&37&40&105&-2.99042\,10^{-9}&6.05871\,10^{-9}&3.57008\,10^{-8}\\
5&52&41&98&-2.08758\,10^{-9}&4.19662\,10^{-9}&2.45371\,10^{-8}\\
6&67&38&92&-1.33060\,10^{-9}&3.11569\,10^{-9}&1.75926\,10^{-8}.
\end{array}
\]

The consecutive contraction ratios for
((|\lambda_{\min}|,\|\lambda_-\|_2,\|\lambda_-\|_1)) are

```text
round 2 -> 3: (0.54349, 0.54233, 0.56434)
round 3 -> 4: (0.69093, 0.64428, 0.61785)
round 4 -> 5: (0.69809, 0.69266, 0.68730).
round 5 -> 6: (0.63738, 0.74243, 0.71699).
```

This is material numerical convergence, not a fixed eigenvector contraction.
For example, between rounds four and five the absolute overlaps of the
leading eigenvectors are `0.00685` in block `(2,9,9)`, `0.10419` in
`(2,3,9)`, and `0.07539` in `(0,8,9)`.  The corresponding negative
subspaces retain only partial overlap; their largest principal angles range
from roughly ten to fifty-one degrees in the leading blocks.

The refined round-five source has

```text
fixed-marginal residual       8.070002713975354e-21
source PSD defect             0
minimum source eigenvalue     9.041531151428900e-19
number of active cuts         52
minimum active-cut value      6.995733070000000e-18  (approximately)
```

The round-six source, after adding fifteen further rotated cuts, has

```text
fixed-marginal residual       8.773042012422509e-21
source PSD defect             0
minimum source eigenvalue     5.814069796976408e-19
number of active cuts         67
minimum active-cut value      1.864232250000000e-17  (approximately)
```

Thus the observed negative spectra have not produced an affine rigidity or
finite-cut dual obstruction.  They rotate while their aggregate size
decreases.

## Reproducibility and cache policy

The stable discovery entry points are:

```text
discovery/agent_dth_level2_cross_candidate_orbits.py
discovery/agent_dth_level2_active_cut.py
discovery/agent_dth_level2_two_cone_active.py
discovery/agent_dth_level2_multi_ppt_active.py
```

The last driver was developed on the parallel other-grouped-PPT track.  It
reuses the same active-cut core but tags cuts by crossing type; its inclusion
here records shared infrastructure, not a Gamma-z or Gamma-AA feasibility
claim.

Representative commands are

```text
python discovery/agent_dth_level2_cross_candidate_orbits.py \
  --candidate CANDIDATE.pkl --max-mixed-dimension 500 \
  --output SPECTRUM.pkl

python discovery/agent_dth_level2_two_cone_active.py \
  --resume CANDIDATE.pkl --spectrum SPECTRUM.pkl \
  --maximum-per-block 1 --maximum-new-cuts 15 \
  --iterations 300 --cone-cycles 4 --output NEXT.pkl
```

The large floating-point pickle caches are intentionally not committed.
Their names identify the outer round and crossed dimension cap.

## What remains

Even numerical feasibility of every Gamma-A block would only establish a
candidate for one grouped partial-transpose cone.  The Gamma-z and
Gamma-AA representatives remain, and exact rational reconstruction with
rigorous PSD margins would still be required.  A complete degree-three
pseudomoment would remain a relaxation result, not a physical DTH witness.

The next discovery step is to continue active cuts while the cap-500 defect
contracts.  Once its worst eigenvalue is below (10^{-12}), the solver
should target strict relative margins before increasing the block cap or
attempting exactification.
