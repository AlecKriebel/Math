# D4-DN-3 clean-room lower audit log

## 2026-07-26T05:08:00Z — clean-room boundary fixed

The lower audit begins from only the already-audited contact atlas in
`d4_dn3_full_rebuild`.  Before freezing independent formulas, no file in
`d4_dn3_full_descent` and no lower script or note in
`delta_ge3_survivor_probe` will be read.

Frozen input:

\[
h=(p+q)^2,\quad P=hp^2,\quad Q=hq^2,\quad R=(p+q)^3.
\]

The two contact planes have

\[
c_\pm=(-4\pm2\sqrt2)/3,
\]
\[
U_1=\frac{4k-3(s+c_\pm k)}3p^2+
    \frac{4k-3s}3pq,\quad
V_1=(s+c_\pm k)pq+s q^2,\quad
T_1=k(p+q),
\]

with \(U=U_0+rU_1,\ V=V_0+rV_1,\ T=T_0+rT_1\).
Their intersection is \(k=0\), and the origin is \(k=s=0\).

Required independent charts:

1. \(c_+\), \(k\ne0\), arbitrary \(s\);
2. \(c_-\), \(k\ne0\), arbitrary \(s\);
3. \(k=0,\ s\ne0\);
4. \(k=s=0\).

No generic-only solved formula will be accepted as covering a boundary.

## 2026-07-26T06:03:00Z — clean-room formulas frozen

All four charts were closed before comparison:

- both \(k\ne0\) plane interiors are inconsistent at \(E_5\);
- the punctured intersection has two required \(E_4\) subcharts, and both
  force \(\det L=0\);
- the origin forces all nonlinear \(r\)-dependence to vanish and exits by
  Moh's unconditional degree-\(<100\) plane theorem.

Exact formulas and pivots were frozen in `PRECOMPARISON_FORMULAS.md`.

## 2026-07-26 — post-freeze comparison and strict verification

The frozen formulas agree with the independent PARI transverse and boundary
reconstructions.  Different valid pivot choices account for harmless scalar
and parameter-factor differences.  The clean-room derivation explicitly
covered the one parameter-dependent pivot boundary; the PARI replay also
found a global \(9s^2\) pivot.

The combined wrapper reached:

```text
D4_DN3_CLEANROOM_FULL_EXCLUSION_STRICT_PASS
```
