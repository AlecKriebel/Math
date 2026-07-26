# Research log — D4-DN-2C full rebuild

All timestamps are UTC.

## 2026-07-26T05:07:00Z

Started a fresh derivation for the fixed family
\(h=(p+q)^2,\ P=hp^2,\ Q=hq^2,\ R=h(p-2q)\).  No D4-DN-3 contact
formula was imported.

## 2026-07-26T05:18:00Z

Derived the reduced \(E_7\) contact row
\[
-3q\,\partial_rU+3(p+2q)\,\partial_rV+4q(p+q)\,\partial_rT=0.
\]
Exact block ranks are \(2,3,4\), yielding six nonbinary contact
coordinates and eleven free binary coefficients.

## 2026-07-26T05:29:00Z

The \(E_6,r^3\) equations force \(d=z=0\).  Eliminating the only two
lower variables in the \(r^1\) block gave
\[
\left(f,(2b+3y)^2\right).
\]
The radical splits over \(\mathbb Q(\sqrt{-2})\) into two planes meeting
along one line.

## 2026-07-26T05:40:00Z

Restored all 18 lower variables and found a complete four-chart atlas:
two rank-seven plane interiors, the rank-six punctured intersection line,
and the rank-five origin.  The first plane pivot vanishes exactly on the
geometric plane intersection, so no solver-denominator line has been
silently discarded.

## 2026-07-26T05:46:41Z

The self-contained exact verifier passed.  It solves each chart on its
displayed pivot and checks all 13 residual equations identically.  Scope
remains \(E_7/E_6\) only; no family exclusion is claimed.
