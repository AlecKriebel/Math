# K3P cut-transfer adversarial audit

Date: 2026-08-24
Scope: `cut_recovery/adversarial/` only
Verdict: **SHORTCUT INVALID ONLY**

## Executive conclusion

The claimed identity on the subgroup \(H=\{0,C\}\) is correct, but the
inference from that identity to the full pointwise K3P cut theorem is not.
There is an exact strict-parameter two-active crossing for which the
\(H\)-restricted CFN flattening has the binary cut-threshold rank even though
the tested split is not a cut.

That counterexample does **not** refute full K3P cut recovery.  On the same
literal descendant-mask graph and with the same \(C\)-coordinates, an exact
strict continuous-time K3P extension has four character-block ranks

\[
(4,3,4,4),
\]

so its full Fourier flattening has rank \(15\).  An explicit nonzero
\(5\times5\) minor is

\[
\frac{11139160404356123}
{205680396636584911254472605806100480000000}.
\]

A second exact construction makes **all three** order-two projections attain
their binary cut-threshold ranks simultaneously, while the full K3P block
ranks are \((4,4,4,4)\).  Thus replacing the single projection by the three
projections does not repair the pointwise proof.

No strict full-K3P counterexample was found.  Generic cut recovery has a short
rigorous repair by restriction to the isotropic JC slice.  The stronger
pointwise statement throughout \(\mathcal D_{3,+}\) remains neither refuted
nor certified by the available package.

## 1. Provenance finding

The recovered file is exactly 3,077,509 bytes and has SHA-256

```text
b627df5b2dc8cf1eb21c2e08c974f9e54f5a0399043e4dd96ea95dc73c2c3350
```

It is byte-for-byte identical to

```text
s_tc_jc_landmark_closure/s_tc_jc_sharp_boundary/quarantine/
withdrawn_positive_v1.1.1/reproducibility/exact_release/
certificates/pointwise_cut_certificate.json
```

The containing historical release says `WITHDRAWN — DO NOT SUBMIT OR CITE AS
ESTABLISHED`.  Git binds that copy to commit
`a9a377d5e5d1af773ae161baf836cce37c5578b0` and blob
`cbfe1d486e3cc59e1839098149735714a0819797`.

This does not by itself falsify any algebra in the file, but it invalidates
the cloud package's treatment of the file as an unqualified current JC
theorem certificate.

The newer corrected JC cut certificate has SHA-256

```text
edbd4afe566ed0ed5d1c518ffe5b21f8f224d547b9c351cb4e1a8c1c613ac086
```

and contains literal graph witnesses.  Its record 26 realizes frozen endpoint
record 48 after zero-sum complement normalization and duplicate-row grouping.
The standalone verifier independently rebuilds its 12 descendant-mask rows
from the graph, checks the rooted binary DAG and tree-child conditions, and
checks the locked standard-strong mixed-graph criterion after one root
suppression.

## 2. Exact reconstruction of endpoint record 48

The frozen Python zero-based endpoint index is 48, the 49th record.  Its
literal reduced descendant-mask tensor is

```text
((0,0,0,4),
 (0,0,4,0),
 (0,0,4,4),
 (1,1,1,1),
 (1,1,1,5),
 (1,1,5,5),
 (2,2,2,2),
 (4,4,0,0),
 (4,4,4,4),
 (5,5,5,5))
```

It is recorded as `theta_incoming_active`, with the historical JC branch
`F_positive`.  In type-key order the normalized binary edge parameters are

\[
\left(\frac34,\frac9{10},\frac23,\frac13,\frac34,
\frac1{10},\frac12,\frac56,1,\frac12\right),
\]

and the inheritance parameters are \((1/6,1/2)\).  Row 8 is the normalized
central singleton-signature class.

Direct exact summation over the four switchings gives

\[
a=q_{011}=\frac1{160},\qquad
b=q_{101}=\frac{25}{288},\qquad
c=q_{110}=\frac{427}{3840},
\]

and hence

\[
a-bc=-\frac{3763}{1105920}<0.
\]

Join two identical normalized endpoints and take

\[
z=\frac{a}{bc}=\frac{6912}{10675}.
\]

For the wrong split \(13\mid24\), both binary character-block determinants
are exactly zero and the CFN Fourier flattening has rank 2, the true-cut
binary threshold.  A physical realization takes endpoint central scales
\(9/10\) and bridge scale

\[
\frac{z}{(9/10)^2}=\frac{1024}{1281},
\]

all strictly between zero and one.

Therefore the implication

```text
noncut in the graph  =>  projected CFN rank > 2 at every strict point
```

is false.  The projected model identity alone cannot imply full K3P rank at
least five.

## 3. Exact full-K3P computation on the same graph

Keep the displayed \(C\)-eigenvalue on every noncentral endpoint row and set
the other two eigenvalues to \(1/4\).  Restore each endpoint's central
incidence as

\[
(9/10,1/4,1/4)
\]

and use the physical bridge

\[
(1024/1281,1/4,1/4).
\]

The resulting effective bridge triple is

\[
(6912/10675,1/64,1/64).
\]

Every physical edge, including all 12 arcs in the corrected literal graph,
satisfies both the strict principal-domain inequalities and

\[
c>gt,\qquad g>ct,\qquad t>cg.
\]

The verifier compiles all 16 endpoint coordinates from the literal physical
arc masks and independently from the reduced tensor; the two computations
agree exactly after restoring the central multiplier.

For \(13\mid24\), the exact ranks are

| character block | rank |
|---|---:|
| 0 | 4 |
| C | 3 |
| G | 4 |
| T | 4 |
| total | **15** |

The nonzero \(3\times3\) minor certifying rank 3 in the only singular block is

\[
\frac{109444956179346849}
{21525608961378488554199449600000}.
\]

This is decisive: endpoint type 48 is a counterexample to the CFN shortcut,
not a counterexample to the full K3P cut-rank conclusion.

## 4. Three projections still do not repair the proof

The verifier contains a second rational type-48 point.  All nine noncentral
edge triples, both inheritance parameters, both restored central incidences,
and the physical bridge satisfy the strict \(\mathcal D_{3,+}\) inequalities.
The effective bridge is chosen from the three exact ratios

\[
z_h=\frac{a_h}{b_hc_h},\qquad h\in\{C,G,T\}.
\]

At that point,

| restricted model | rank | binary cut threshold |
|---|---:|---:|
| \(\{0,C\}\) | 2 | 2 |
| \(\{0,G\}\) | 2 | 2 |
| \(\{0,T\}\) | 2 | 2 |

but the four full K3P block ranks are \((4,4,4,4)\), for total rank 16.
Consequently no argument based only on testing the three order-two principal
subflattenings can prove the full pointwise theorem.

## 5. Exhaustive deterministic falsification scans

At one deterministic exact strict continuous-time rational point per frozen
type, the standalone verifier checked:

- all 177 endpoint types;
- all 31,329 ordered pairs of endpoint types; and
- all 453 single-blob types.

Results:

| family | exact rank distribution |
|---|---|
| ordered endpoint pairs | all 31,329 have rank 16 |
| 421 noncut single-blob types | all have rank 16 |
| 32 displayed-bridge single-blob types | all have rank 4 |

This is an exact exhaustive structural-point scan over the frozen universe,
not a proof at every parameter point.  It found no full-K3P strict
counterexample.

The excluded all-identity edge boundary has block ranks \((1,1,1,1)\), hence
total rank 4.  This expected degeneration confirms that strictness matters.
Two other sampled boundary faces (one inheritance parameter equal to zero,
and identity effective bridge) retained full rank 16.

## 6. What is repaired, and what is not

There is a rigorous generic repair.

For a fixed topology and split, every \(5\times5\) flattening minor is a
polynomial in the K3P Fourier edge and inheritance parameters.  A true cut
makes every such minor vanish identically.  For a noncut split, restrict to
the isotropic slice

\[
(c_e,g_e,t_e)=(r_e,r_e,r_e),\qquad 0<r_e<1.
\]

This slice lies in strict \(\mathcal D_{3,+}\) and strict continuous time and
is exactly JC.  The corrected JC pointwise cut theorem gives a nonzero minor
there.  Hence the K3P minor polynomial is not identically zero, and rank at
most four characterizes cuts away from a proper algebraic exceptional set.

This proves **generic K3P cut recovery**.

It does not prove the claimed pointwise statement at every strict K3P point.
For source-open containment it immediately proves the inclusion

\[
\operatorname{Cut}(N')\subseteq\operatorname{Cut}(N)
\]

when the target is \(N'\): a target cut equation vanishes on the contained
source germ, and a source noncut has a nonzero pullback polynomial.  The
reverse cut inclusion still requires either a pointwise target obstruction
or a separate dimension/positivity argument.  It must not be silently
deduced from generic nonvanishing.

Accordingly:

- **shortcut invalid only** is the verdict on the discovered type-48 issue;
- the full K3P theorem is not refuted by this witness;
- generic cut recovery is repaired;
- pointwise K3P cut recovery throughout \(\mathcal D_{3,+}\) remains open in
  this audit; and
- the global one-sided containment proof must not cite the old transfer as if
  it supplied both cut inclusions.

## 7. Replay

From `/Users/alec/Documents/Math`:

```bash
python3 k3p_level2_identifiability_final/cut_recovery/adversarial/verify_cut_transfer_adversarial.py --check-audit-json >/dev/null
```

The full replay uses only the Python standard library and takes about nine
seconds on the M1 MacBook Pro.  A fast replay that skips the deterministic
universe scan is:

```bash
python3 k3p_level2_identifiability_final/cut_recovery/adversarial/verify_cut_transfer_adversarial.py --quick >/dev/null
```

The mutation suite has 13 targeted mutations; all are rejected.
