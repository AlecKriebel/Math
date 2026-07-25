# Frozen marked-companion taxonomy inside `Q2-E2-A2-B1-D1-N1`

**Candidate recorded (UTC):** 2026-07-25T23:22:00Z.

**Status:** freeze candidate.  A blinded clean-room derivation and an exact
comparison agree.  A second hostile reconstruction is still pending.  Until
that audit passes, this file fixes the candidate identifiers but does not
authorize lower-identity exclusion.

This is an internal parameterized stratification of one inclusive row in
`FROZEN_TAXONOMY_v1.md`.  It neither changes the global denominator of
fourteen rows nor certifies an exclusion.

## 1. Intrinsic object

On the nonzero all-vertical frontier, the certified top theorem gives
\[
H_4=(h^2,hs,0),\qquad
s=\ell^2,\qquad
G=(H_3)_3=\ell r,
\]
where \(V=\langle h,s\rangle\) is a minimal quadratic pencil, \(s\) is its
unique double-line member, and \([r]\in\mathbb P(V)\).  This file freezes
the missing marked-distinct locus
\[
[h]\ne[s].
\]
The zero companion \(G=0\) is retained as `C0`.  For \(G\ne0\), the
classification object is the ordered projective configuration
\[
\bigl(V;[s],[h],[r]\bigr)
\]
under source \(\operatorname{PGL}_3(\mathbb C)\).  A target change of pencil
basis changes coordinates on \(\mathbb P(V)\) but does not move these
intrinsic points.

## 2. Three marked-pair types

There are exactly three ordered marked-pair orbits:

| Stable pair ID | \(s\) | \(h\) | pencil type |
|---|---|---|---|
| `Q2-E2-A2-B1-D1-N1-MD-P21-HR2` | \(x^2\) | \(yz\) | discriminant partition \(2+1\), rank-two marked member |
| `Q2-E2-A2-B1-D1-N1-MD-P21-HSM` | \(x^2\) | \(x^2+yz\) | discriminant partition \(2+1\), smooth marked member |
| `Q2-E2-A2-B1-D1-N1-MD-P3-HSM` | \(x^2\) | \(y^2+xz\) | discriminant partition \(3\), smooth marked member |

They are separated by the discriminant multiplicity of the pencil, the
rank of \(h\), and the rank of \(h|_{x=0}\).

## 3. Frozen companion strata

Append the following suffixes to the stable pair ID.

### 3.1 `MD-P21-HR2`

The residual torus has exactly three nonzero orbits:

| suffix | companion point | representative \(G=\ell r\) |
|---|---|---|
| `C0` | \(G=0\) | \(0\) |
| `CH` | \(r=h=yz\) | \(xyz\) |
| `CS` | \(r=s=x^2\) | \(x^3\) |
| `CO` | \(r\notin\{h,s\}\) | \(x(x^2+yz)\) |

### 3.2 `MD-P21-HSM`

Put
\[
s=x^2,\qquad t=yz,\qquad h=s+t,
\]
and use homogeneous companion coordinates
\[
[u:v]\in\mathbb P^1,\qquad
r_{[u:v]}=u h+v s,\qquad
G_{[u:v]}=x r_{[u:v]}.
\]
The marked-pair stabilizer acts trivially on this projective line.  Hence
distinct parameter values are inequivalent.  The frozen boundary and
parameter strata are:

| suffix | homogeneous condition | affine \(\tau=v/u\) | companion |
|---|---|---:|---|
| `C0` | \(G=0\) | -- | zero companion |
| `CH` | \([u:v]=[1:0]\) | \(0\) | \(r=h\) |
| `CT` | \([u:v]=[1:-1]\) | \(-1\) | \(r=t=yz\) |
| `CS` | \([u:v]=[0:1]\) | \(\infty\) | \(r=s\) |
| `CTAU` | \(uv(u+v)\ne0\) | \(\tau\in\mathbb C\setminus\{0,-1\}\) | \(r=h+\tau s\) |

Every `CTAU` branch key must carry its actual `tau=<value>` field.  `CTAU`
is one parameterized stratum, not one orbit.  Any calculation on the
affine chart \(u=1\) must rebuild the \(u=0\) boundary and homogenize every
denominator.

### 3.3 `MD-P3-HSM`

The residual torus has exactly three nonzero orbits:

| suffix | companion point | representative \(G=\ell r\) |
|---|---|---|
| `C0` | \(G=0\) | \(0\) |
| `CH` | \(r=h=y^2+xz\) | \(x(y^2+xz)\) |
| `CS` | \(r=s=x^2\) | \(x^3\) |
| `CO` | \(r\notin\{h,s\}\) | \(x(x^2+y^2+xz)\) |

Thus the marked-distinct frontier has thirteen stable strata:
\[
\boxed{4+5+4=13},
\]
one of which (`CTAU`) is a punctured parameter line containing infinitely
many inequivalent orbits.  The nonzero orbit-space shorthand is
\[
\boxed{3+\mathbb P^1(\mathbb C)+3}.
\]

## 4. Completeness and boundaries

After \(s=x^2\), write
\[
h=a x^2+2xv^Tu+u^TCu,\qquad u=(y,z)^T.
\]
Coprimality gives \(C\ne0\).  Rank two of \(C\) produces precisely
\(h=yz\) and \(h=x^2+yz\); rank one either creates a forbidden second
double line or gives \(h=y^2+xz\).  The induced actions on the pencil line
are respectively a torus, the identity, and a torus after fixing \(h\).
Their orbit decompositions are exactly those in Section 3.

The parameter divisors
\[
u=0,\qquad v=0,\qquad u+v=0
\]
are frozen boundaries.  A newly discovered lower-identity pivot divisor
refines one of the thirteen strata; it does not append a fourteenth
internal stratum silently.  It must be recorded as a new freeze version or
handled by a division-free calculation.

## 5. Frozen evidence

The clean-room reconstruction was completed without reading the candidate
slice package or the earlier readiness report.  At candidate freeze time:

```text
f5323cd2cc6e2133b7eae29b3d77d1f3dd820dac5b84332c6c71281ff536129a  audit_marked_orbit_reconstruction/REPORT.md
f800d30ab9ee2d594c36a62cf1750d101df43c5aebf205dfed47e44110cdb7b6  audit_marked_orbit_reconstruction/verify_marked_orbits_exact.py
b14987bbc1f804b787ef955986e56f7093b86a9a8f6f987762f3743d8aa72bef  marked_h_distinct/FREEZE_READINESS_COMPARISON.md
```

The dependency-free checker reports:

```text
PASS: 3 marked-pair types, discriminants, unique double lines, and residual companion actions verified
```

The separate \(E_7/E_6\) calculations are deliberately not inputs to the
taxonomy proof.  They show that every value of the middle
\(\mathbb P^1\)-modulus survives through \(E_6\), but they neither exclude a
stratum nor certify the orbit classification.

This freeze candidate was produced with substantial AI assistance.  It is
not peer reviewed.  Exact checks are evidence about the encoded algebra and
finite-field stabilizer regressions, not peer review.
