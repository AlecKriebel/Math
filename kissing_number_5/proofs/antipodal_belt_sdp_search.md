# Antipodal-pair belt SDP search — numerical report, not a proof

## Conditional target

If a kissing code contains an antipodal pair \(\{\pm e\}\), every other point
\(x\) has
\[
-\frac12\leq\langle e,x\rangle\leq\frac12.
\]
Indeed, the constraints against \(e\) and \(-e\) give the two inequalities.
Thus the remaining points form a code in the closed belt
\[
\mathcal B=\{x\in S^4:|\langle e,x\rangle|\leq1/2\}.
\]

Let \(B_{\rm belt}\) be the largest size of such a belt code.  The \(D_5\)
configuration, after fixing any antipodal root pair, leaves 38 points in the
belt, so \(B_{\rm belt}\geq38\).  An exact proof \(B_{\rm belt}\leq38\)
would be sharp and would show that every five-dimensional kissing code
containing an antipodal pair has at most 40 points.

The scoped search
[`../experiments/search_antipodal_belt_sdp.py`](../experiments/search_antipodal_belt_sdp.py)
uses the same positive axisymmetric kernels as the certified hemisphere
bounds.  It seeks PSD blocks with sampled off-diagonal value at most \(-1\)
on
\[
-1/2\leq u,v\leq1/2,\quad -1\leq t\leq1/2,\quad
1+2uvt-u^2-v^2-t^2\geq0,
\]
while minimizing one plus the sampled diagonal maximum.  A rigorously
verified objective below 39 would imply \(B_{\rm belt}\leq38\).

## Sampling audit

Every run explicitly samples:

- both determinant-zero sheets;
- the contact sheet \(t=1/2\);
- both belt walls \(u=\pm1/2\);
- the equatorial axis \(u=0\);
- the same-sign symmetry plane \(u=v\);
- the mixed-sign symmetry plane \(u=-v\);
- full interior \(t\)-segments on all those lower-dimensional surfaces;
- deterministic random interior points biased toward both determinant
  boundaries.

The post-solve audit independently samples random feasible points, both
determinant sheets, a 10,001-point diagonal grid, and dense grids on all
listed special surfaces.  These are numerical screens only; they do not
cover the continuous domain and cannot certify an upper bound.

## Results

| degree | sampled objective | largest audited off value | audited rescaled objective |
|---:|---:|---:|---:|
| 6 | 44.624984581701 | -0.977844287869 | 45.613436043730 |
| 8 | 43.144783982023 | -0.991733297187 | 43.496129981694 |
| 10 | 42.648026420919 | -0.897001149718 | 47.430293200604 |

All three Clarabel runs returned `optimal` on their sampled problems.  The
best independently screened value was the degree-8 value
\[
43.496129981694>39.
\]
It therefore supplies no candidate for exactification.

The degree-10 run illustrates why the special-surface audit is essential.
Although its sampled objective decreased, the audit found a narrow violation
on the mixed-sign ridge at approximately
\[
(u,v,t)=(-1/2,1/2,0.455),\qquad F\approx-0.89700115,
\]
far above the imposed sample value \(-1\).  Rescaling by this actual sampled
maximum makes the bound worse, not better.  No numerical solver status or
mesh result is promoted to a theorem.

The temporary source matrices had SHA-256 hashes

- degree 6:
  `f1451470f1e1fa8bd04db388940deda20c07501c8d587a4166f292f8756d4a07`;
- degree 8:
  `289d1076e84a6f1eb9f39b805a8956a4d431e0141c192c31a0411d76cae7323d`;
- degree 10:
  `fd0e7694ea54e08e08d17ff80a6989d7dc4d64814dd6925548abd96751c4a8de`.

They are discovery artifacts in `/tmp`, not proof dependencies.  Each run is
reproducible from the corresponding degree and seed (`521006`, `521008`,
and `521010`) using the commands and defaults encoded by the search script.

## Status

The route is **active but presently numerically weak**.  No rational
certificate was attempted because no audited objective was below 39.  A
future continuation would need adaptive cutting planes on the
\((-1/2,1/2,t)\) ridge and a materially stronger dual degree or
normalization; merely rationalizing any candidate above would prove nothing
new.
