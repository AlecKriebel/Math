# Exact support obstruction for the 64-atom K5 product extension

## Statement

Let \(\mathcal S\) be the union of the \(S_5\)-orbits of the 64
quarter-grid K5 atoms in
`../k5_product_audit/centered_quarter_k5_product_extension.json`.
There is no seven-edge-colored complete graph on six labeled vertices for
which all six induced K5 faces belong to \(\mathcal S\).

Consequently, the 64-atom symmetric K5 distribution is not the K5 face
marginal of any nonnegative symmetric K6 distribution. This conclusion
does not require Gram positivity or a rank bound, and in particular rules
out a lift using the available 137,296-atom rank-five K6 pool.

## Complete finite reduction

Label the possible K6 vertices \(0,\ldots,5\). If a supported K6 existed,
its face obtained by deleting vertex 5 and its face obtained by deleting
vertex 4 would both be labeled elements of \(\mathcal S\). These two K5
faces agree on their common K4 with vertices \(0,1,2,3\).

Conversely, take any ordered pair of labeled supported K5 faces agreeing
on that common K4. Together they assign 14 of the 15 K6 edges. The only
unassigned edge is \(45\). Trying its seven possible quarter-grid colors
therefore enumerates every colored K6 needed for the existence test. The
remaining four K5 faces can then be checked by exact tuple membership in
\(\mathcal S\).

The exact counts are:

- 64 distinct unlabeled K5 support orbits;
- orbit-size histogram \(3\cdot30+19\cdot60+42\cdot120=6270\)
  labeled supported K5s;
- 3,888 labeled common-K4 keys;
- 14,874 compatible ordered pairs of supported K5 faces;
- \(7\cdot14{,}874=104{,}118\) final-edge color trials;
- zero trials whose six K5 faces all belong to \(\mathcal S\).

All operations are permutations, integer tuple comparisons, and exact
counts. There is no numerical tolerance and no omitted boundary case.

## Distribution corollary

The target 64-atom K5 distribution has positive mass on every orbit in
\(\mathcal S\) and zero mass outside \(\mathcal S\). Suppose a
nonnegative K6 distribution induced it. A positive K6 atom with even one
face outside \(\mathcal S\) would contribute positive mass to an outside
K5 orbit; nonnegative weights cannot cancel that contribution. Thus every
face of every positive K6 atom would have to lie in \(\mathcal S\), which
the exhaustive enumeration has shown impossible.

As a redundant pool-specific check, the verifier also scans all 137,296
authenticated rows of `direct_k6_5000.csv`. The numbers of pool atoms with
respectively \(0,1,2,3,4\) supported K5 faces are

\[
136359,\quad897,\quad38,\quad1,\quad1,
\]

and no pool atom has five or six supported faces.

## Interpretation

This obstruction eliminates the particular 64-atom K5 mixture, not the
pair/triple pseudodistribution. The separate exact 74-atom K6 certificate
in this folder induces a different K5 marginal and passes all 560 current
product rows. Hence K6 face consistency strictly removes the earlier K5
witness, while the present local constraints still leave another
rank-exact-five K6 witness.

## Reproduction

From the repository root:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k6_product_audit/verify_k5_support_no_k6_lift.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k6_product_audit.test_k5_support_no_k6_lift \
  -v
```
