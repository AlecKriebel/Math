# Hostile audit: line-\((2,2)\) finite-companion F/G package

**Verdict:** **FAIL as a full-moduli/exhaustive-boundary package.**

**Narrow verdict:** **PASS for the theorem on the chart where both outer
critical points are finite.**  I found no algebraic error, lost
specialization, or in-chart counterexample in the \(F=0\) or \(G=0\)
argument.

The failure of the original full-row claim is a scope error.  The actual stabilizer of
\(\langle x^2,yz\rangle\) cannot move the point \(u=\infty\), so the
normal form with finite \(a,b\) does not represent every outer double
cover.  An entire one-critical-point-at-infinity chart is absent.  In
addition, at audit time both supplied Python certificates failed open under
`python -O`.

**Post-audit remediation (2026-07-25T06:06:25Z):** the theorem was narrowed
to the finite-outer-critical chart, the omitted infinity chart and corrected
frontier were recorded, both Python verifiers gained fail-closed
`__debug__` guards, and the optimized-mode fault test now verifies those
guards.  The narrow PASS verdict is therefore release-ready; the FAIL
verdict remains in force for any claim to have closed the whole row.

## 1. Audited material

- `WORKING_LINE_22_FULL_MODULI.md` (subsequently renamed
  `WORKING_LINE_22_FINITE_OUTER_CRITICAL.md`)
- `WORKING_LINE_22_FG_RESONANCE.md`
- `verify_line_22_full_moduli_sympy.py` (subsequently renamed
  `verify_line_22_finite_outer_critical_sympy.py`)
- `verify_line_22_full_moduli_pari.gp` (subsequently renamed
  `verify_line_22_finite_outer_critical_pari.gp`)
- `verify_line_22_fg_resonance_sympy.py`
- `verify_line_22_fg_resonance_pari.gp`
- `run_verify_line_22_fg_resonance_pari.sh`

I also reconstructed the finite F-chart and the omitted infinity chart in
two independent exact scripts in this audit directory.

## 2. Finding A — the stabilizer statement is right, but its consequence is
not

Put \(p=x^2,q=yz\), and let a source linear map preserve their pencil.
The unique rank-one member of the pencil is \(p\).  Hence, if
\((X,Y,Z)\) are the transformed linear coordinates, then
\[
X=\alpha x.
\]
Because the induced pencil map is invertible,
\[
YZ=\nu x^2+\mu yz,\qquad \mu\ne0.
\]
Restrict to \(x=0\).  Unique factorization in
\(\mathbb C[y,z]\) gives, up to interchanging \(Y,Z\),
\[
\bar Y=\beta y,\qquad \bar Z=\gamma z.
\]
Write \(Y=r x+\beta y\), \(Z=sx+\gamma z\).  The \(xy\) and \(xz\)
coefficients of \(YZ\) force \(s=r=0\).  Therefore \(\nu=0\), and the
full stabilizer is
\[
(x,y,z)\longmapsto(\alpha x,\beta y,\gamma z)
\]
together with the \(y,z\) interchange.  It induces only
\[
u=p/q\longmapsto\lambda u.
\]

This proves the stabilizer claim in the note.  It also proves that
\(u=\infty\) is fixed.  A target automorphism changes branch values, not
critical points in the source of the outer cover.  Consequently:

- if both critical points are finite, the displayed form
  \[
  ((p-aq)^2,(p-bq)^2,0)
  \]
  is valid;
- if one critical point is infinity, the additional form is
  \[
  \boxed{H_4=((p-aq)^2,q^2,0).}
  \]

Thus the sentence “every degree-two outer map” in Section 1 of the
full-moduli note is false as written.

## 3. Finding B — exact classification of the omitted chart

For finite companion, the missing joint form is
\[
H_4=((p-aq)^2,q^2,0),\qquad
R_3=x(p-cq).
\tag{A}
\]
The stabilizer acts by common scaling
\[
(a,c)\longmapsto(\lambda a,\lambda c).
\]
Hence the nonzero orbits retain the genuine modulus
\([a:c]\in\mathbb P^1\), and \((a,c)=(0,0)\) is a separate fixed orbit.

A direct reconstruction of all \(E_7\) weight blocks gives
\[
\det E_{7,\pm2}\ \sim\ (3a-c)(3a-2c)
\]
and
\[
\gcd(\text{maximal minors of }E_{7,\pm1})
\ \sim\ c(3a-c)(3a-2c).
\]
The two missing mixed-companion resonances are therefore
\[
\boxed{c=3a,\qquad c=\frac32a.}
\]
Equivalently, in the ratio \(a/c\), they are \(1/3\) and \(2/3\).
They are also the projective limits
\[
\frac{F}{b}\longrightarrow3a-c,\qquad
\frac{G}{b}\longrightarrow3a-2c
\]
as the second finite critical point tends to infinity.

The exact raw \(E_7\) ranks are:

| Orbit type | Normalized condition | Weight ranks \(-3,\ldots,3\) | Raw rank |
|---|---:|---:|---:|
| generic mixed, including \(a=0,c\ne0\) | \(c(3a-c)(3a-2c)\ne0\) | \(2,3,4,0,4,3,2\) | 18 |
| first resonance | \(c=3a\ne0\) | \(2,2,3,0,3,2,2\) | 14 |
| second resonance | \(2c=3a\ne0\) | \(2,2,3,0,3,2,2\) | 14 |
| noncritical triple | \(c=0,a\ne0\) | \(2,3,3,0,3,3,2\) | 16 |
| marked-critical triple | \(a=c=0\) | \(1,1,2,0,2,1,1\) | 8 |

The companion-at-infinity form \(R_3=xq\) supplies two more outer-infinity
orbits, according as \(a=0\) or \(a\ne0\) (normalize \(a=1\) in the
latter).

## 4. Exact counterexamples to the exhaustion claims

These are counterexamples to chart exhaustiveness, not claimed Keller
maps.  In every case set the first two cubic components and all of \(H_2\)
to zero.  Direct expansion gives \(E_8=E_7=0\).

1. A generic omitted finite companion:
   \[
   H_4=((p-q)^2,q^2,0),\qquad R_3=x(p-2q).
   \]
   This refutes “every degree-two outer map” and is in none of the three
   boundaries listed in Section 6.

2. The omitted projective \(F\)-resonance:
   \[
   H_4=((p-q)^2,q^2,0),\qquad R_3=x(p-3q).
   \]
   Here \(3a-c=0\).

3. The omitted projective \(G\)-resonance:
   \[
   H_4=((p-q)^2,q^2,0),\qquad
   R_3=x\left(p-\frac32q\right).
   \]
   Here \(3a-2c=0\).

4. An omitted noncritical triple endpoint:
   \[
   H_4=((p-q)^2,q^2,0),\qquad R_3=x^3.
   \]

5. Omitted companion-at-infinity endpoints:
   \[
   H_4=((p-q)^2,q^2,0),\quad R_3=xq,
   \]
   and
   \[
   H_4=(p^2,q^2,0),\quad R_3=xq.
   \]

The already listed
\[
H_4=(p^2,q^2,0),\qquad R_3=x^3
\]
is only the single orbit \(a=c=0\) inside this much larger chart.

## 5. Correct exhaustive frontier relative to the audited chart theorems

For the results presently encoded in the two notes, the remaining frontier
should be grouped as follows.

1. **Rank-two-restriction pencil, both outer critical points finite,
   companion at infinity:**
   \[
   H_4=((p-aq)^2,(p-bq)^2,0),\quad a\ne b,\qquad R_3=xq.
   \]
   This includes the limiting resonances
   \(2a+b=0\) and \(a+2b=0\).

2. **Rank-two-restriction pencil, one outer critical point at infinity,
   every companion orbit:**
   \[
   H_4=((p-aq)^2,q^2,0).
   \]
   For finite companion \(R_3=x(p-cq)\), retain the common-scaling orbit
   of \((a,c)\).  Its strata are:

   - generic \(c(3a-c)(3a-2c)\ne0\);
   - \(c=3a\ne0\);
   - \(2c=3a\ne0\);
   - \(c=0,a\ne0\) (noncritical triple);
   - \(a=c=0\) (marked-critical triple; see the current-worktree update
     below);
   - \(a=0,c\ne0\) is a marked-critical outer cover but belongs to the
     generic raw-rank stratum.

   For companion at infinity \(R_3=xq\), retain the two orbits \(a=0\)
   and \(a\ne0\).

3. **The rank-one-restriction pencil**
   \[
   p=x^2,\qquad q=y^2+xz,
   \]
   until its claimed full joint-moduli raw \(E_7\) certificate is actually
   recorded.

This corrected three-family list absorbs the old separately listed
marked-critical triple orbit into item 2.  The original three-item list is
not exhaustive.

**Current-worktree update.**  During this audit, a separate provisional
package was added under `line22_marked_critical_infinity/` for the single
orbit
\[
H_4=(p^2,q^2,0),\qquad R_3=x^3.
\]
That new proof is outside this audit and has not been hostile-audited here.
If its provisional conclusion is accepted, delete only the point
\((a,c)=(0,0)\) from item 2 above.  The generic mixed infinity chart, both
resonances, the noncritical triple endpoint, the marked mixed point, and
both companion-at-infinity orbits remain outside the audited F/G package.

## 6. Finite-critical F/G chart — PASS

Assume now that both outer critical points are finite.  On \(F=0\) with
\(c\ne0\), \(a\ne b\):

- \(b=0\) would force \(a=0\), a contradiction;
- \(a=0\) is likewise impossible;
- scaling \(b=1\) is therefore valid.

Writing \(a=t\) gives
\[
c=\frac{3t}{2t+1}.
\]
The specialization accounting is complete **inside this affine chart**:

| Value | Exact disposition |
|---:|---|
| \(t=-1/2\) | \(F=-3/2\) for every finite \(c\), so there is no \(F=0\) point |
| \(t=0\) | forces \(c=0\), the finite-other-critical marked triple endpoint |
| \(t=1\) | gives \(a=b\), outside the degree-two outer stratum |
| \(t=1/2\) | a gauge degeneracy only; the alternate \(V_3\)-translation gauge is exact |

The missing value is not another finite \(t\); it is the separate
projective chart \(b=\infty\) described above.  Thus “no parameter value was
lost” must be qualified to “no value in the finite-\(a,b\) chart was
lost.”

### Raw \(E_7\) rank and complete kernels

- The raw matrix is \(36\times26\), has rank \(14\), and nullity \(12\).
- A fixed rank-14 minor is a nonzero rational multiple of
  \[
  \frac{t^6(t-1)^6}{(2t+1)^{14}}.
  \]
- In the generic gauge, the six \(W_2\) parameters and \(A,B\), together
  with two target-shear and two source-translation directions, give twelve
  independent raw kernel vectors.  An independent 12-by-12 direction
  minor is a nonzero rational multiple of
  \[
  \frac{t^4(t-1)^4(2t+1)^4}{(2t-1)^2}.
  \]
  This proves the converse: the displayed family is the whole kernel.
- At \(t=1/2\), the alternate gauge again gives twelve independent raw
  directions, while the raw rank remains \(14\).  The displayed numerical
  rank minor \(-387420489/256\) is correct.

### Raw \(E_6\) rank and square obstructions

The \(E_6\) lower-unknown matrix has exact rank \(8\).  In the generic
gauge, direct coefficient combinations give, up to the displayed signs,
\[
-\frac{16}{3}(t-1)(2t+1)m^2,\qquad
\frac{16}{3}(t-1)(2t+1)n^2,
\]
then after \(m=n=0\),
\[
-\frac{8t(t-1)^2(2t+1)}{3(2t-1)^2}r^2,\qquad
\frac{8t(t-1)^2(2t+1)}{3(2t-1)^2}s^2.
\]
Every scalar factor is nonzero on the generic chart, so
\(m=n=r=s=0\).  At \(t=1/2\), the alternate gauge gives nonzero multiples
of \(m^2,n^2,r^2,s^2\) directly.  No square mode survives.

After those four modes vanish, the complete rank-eight \(E_6\) solution is
\[
\begin{aligned}
[xy]U_2&=-\frac43(t-1)(2t+1)\ell_{32},\\
[xz]U_2&=-\frac43(t-1)(2t+1)\ell_{33},\\
[y^2]U_2&=[z^2]U_2=0,\\
[xy]V_2&=[xz]V_2=[y^2]V_2=[z^2]V_2=0.
\end{aligned}
\]
Substitution kills every \(E_6\) coefficient, and the fixed rank-eight
minor is a nonzero rational multiple of
\[
\frac{t^4(t-1)^4}{(2t+1)^8}.
\]
Thus this is a converse, not merely a necessary partial solution.

### Lower \(E_5\) column-kernel exit

The two vectors
\[
(\ell_{12},\ell_{22},\ell_{32})^T,\qquad
(\ell_{13},\ell_{23},\ell_{33})^T
\]
lie in the same \(3\times3\) homogeneous kernel.  Its upper-left
\(2\times2\) minor is exactly
\[
-\frac{36t(t-1)}{(2t+1)^2}\ne0.
\]
The common kernel therefore has dimension at most one, so those two
columns are proportional and \(\det L_0=0\).  This argument does not divide
by any entry of \(L_0\).

The exact swap of outer components sends \(F\) to \(G\), so the same chart
proof applies to \(G=0\).

## 7. Division audit — PASS on the finite-critical chart

Every denominator is accounted for:

- \(b\) is inverted only after proving \(b\ne0\);
- \(2t+1\) is inverted only after excluding \(t=-1/2\);
- \(t\) is inverted only after excluding \(t=0\);
- \(2t-1\) appears only in the generic gauge, while \(t=1/2\) has a
  separate exact chart;
- \(t-1\) is never inverted without the standing \(a\ne b\) condition;
- the square deductions use nonzero scalar factors and do not divide by a
  mode;
- the lower exit uses a rank minor and a common-kernel argument, not a
  division by a linear-part coefficient;
- the marked-critical \(\Delta=0\) subcase in the full-moduli script uses
  the exact \(E_3\) squares and does not divide by \(\Delta\).

No illegal algebraic division was found in any certified finite-critical
branch.

## 8. Supplied executable behavior

### Ordinary runs

All four supplied CAS scripts pass in ordinary mode.  The independent audit
scripts pass as well.

### Python optimized-mode fault injection — corrected to PASS

At audit time both supplied SymPy files used `assert` as their certificate
mechanism but had no `__debug__` guard.  Under `python -O`, Python removed
the assertions; both files returned zero and printed their success sentinel.

Both now contain the required guard near the top:

```python
if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")
```

The success-sentinel text is also narrowed to the finite-critical chart.
The corrected fault-injection test confirms that both scripts return
nonzero for the intended reason under `python -O`.

### Fake GP diagnostic — PASS

The fake `gp` in this audit directory prints a `***` diagnostic, then the
exact expected success sentinel, and exits zero.  The supplied strict runner
still exits nonzero with

```text
FAIL: PARI/GP emitted a parser or runtime diagnostic
```

Thus the supplied PARI runner fails closed for the injected diagnostic.  It
also requires the sentinel to be the exact final line.

## 9. Required corrections and disposition

1. **Critical scope correction — applied:** replace “every degree-two outer map” by
   “every degree-two outer map whose two critical points are finite,” and
   add \(H_4=((p-aq)^2,q^2,0)\).
2. **Critical theorem correction — applied:** qualify the open, \(F\), and \(G\)
   theorems as statements on the finite-outer-critical chart.  The present
   calculations do not certify the projective infinity chart.
3. **Critical boundary correction — applied:** replace the original remaining-boundary
   list by the exhaustive three-family list in Section 5 of this report,
   subtracting the single \((a,c)=(0,0)\) orbit only if the separate new
   marked-critical-infinity package is accepted.
4. **Critical endpoint correction — applied:** replace “no parameter value was lost”
   by “no finite affine \(t\)-value was lost”; explicitly record
   \(b=\infty\), with resonance limits \(3a-c=0\) and \(3a-2c=0\).
5. **High-priority executable correction — applied:** add an optimized-mode rejection
   guard to both supplied SymPy scripts.
6. **Documentation consistency correction — applied:** the original SymPy
   docstring says “four boundary pieces listed in Section 6,” whereas that
   section currently enumerates three.  Make the count agree with the
   corrected frontier.
7. **Sentinel/scope wording correction — applied:** avoid success messages saying all
   finite-companion resonances are excluded; say the finite-critical
   \(F/G\) chart is excluded.

No correction is required to the displayed finite-chart ranks, kernels,
square identities, lower \(E_5\) singularity, \(F\leftrightarrow G\)
symmetry, or strict PARI diagnostic handling.

## 10. Reproducible audit artifacts

- `audit_fg_chart_exact.py`: independent direct-determinant proof of the
  finite F-chart ranks, complete kernels/converses, square obstructions, and
  lower common-kernel exit.  It rejects `python -O`.
- `audit_outer_infinity.py`: independent exact reconstruction of the
  omitted chart, resonance factors, ranks, and all leading witnesses.  It
  rejects `python -O`.
- `test_supplied_python_optimized.sh`: verifies that both corrected supplied
  Python scripts fail closed under `-O`.
- `test_supplied_runner.sh` and `fakebin/gp`: verify that both supplied
  strict PARI runners reject an injected diagnostic despite a forged
  success sentinel.
