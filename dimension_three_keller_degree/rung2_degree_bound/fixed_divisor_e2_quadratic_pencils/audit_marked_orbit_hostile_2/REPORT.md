# Second hostile audit of the marked-companion freeze

## Verdict

**PASS.** The exact candidate
`taxonomy_freeze/FROZEN_Q2_E2_MARKED_COMPANION_v1.md` at SHA-256

```text
27e5a4f894ef523156abea389f89c2d4481d58d243c756b70386fdea10e9e01f
```

agrees with the sealed independent derivation and the earlier clean-room
report. It has exactly three marked-pair types and thirteen stable strata:
\[
4+5+4=13.
\]
The middle `CTAU` entry is correctly a parameterized stratum containing
infinitely many inequivalent orbits, not one orbit.

This audit certifies the internal orbit taxonomy only. It does not exclude
the frozen row, promote its status, or certify any lower-identity
calculation. It is not peer review.

## Independence checkpoint

The derivation in `RESEARCH_LOG.md` was completed before either candidate
package was opened. Its sealed SHA-256 was

```text
bf62d6a11319f9d4214ede241c26f291b6651872f095cd57724f1964ed49e5d6
```

The subsequently read clean-room report was pinned at

```text
f5323cd2cc6e2133b7eae29b3d77d1f3dd820dac5b84332c6c71281ff536129a
```

No route absent from the sealed derivation was imported during comparison.

## Coordinate comparison

The sealed derivation used
\[
r_\theta=s+\theta t=x^2+\theta yz.
\]
The candidate uses \(h=s+t\) and
\[
r_{[u:v]}=u h+v s=(u+v)s+u t,\qquad \tau=v/u.
\]
Whenever \(u(u+v)\ne0\), normalization of the \(s\)-coefficient gives
\[
\boxed{\theta=\frac{u}{u+v}=\frac1{1+\tau}}.
\]
Thus the coordinate systems agree, with boundaries
\[
\begin{array}{c|c|c|c}
\text{candidate}&[u:v]&\tau&\text{sealed }\theta\\ \hline
\texttt{CH}&[1:0]&0&1\\
\texttt{CT}&[1:-1]&-1&\infty\\
\texttt{CS}&[0:1]&\infty&0.
\end{array}
\]
The candidate open condition \(uv(u+v)\ne0\) becomes
\(\theta\notin\{0,1,\infty\}\). No boundary is lost.

## Thirteen-stratum comparison

The exact stable suffix ledgers are:

| marked pair | suffixes | count |
|---|---|---:|
| `MD-P21-HR2` | `C0`, `CH`, `CS`, `CO` | 4 |
| `MD-P21-HSM` | `C0`, `CH`, `CT`, `CS`, `CTAU` | 5 |
| `MD-P3-HSM` | `C0`, `CH`, `CS`, `CO` | 4 |

They are disjoint. On the middle projective line the four predicates
\[
v=0,\qquad u+v=0,\qquad u=0,\qquad uv(u+v)\ne0
\]
are pairwise disjoint and exhaustive. The checker replays this partition
over two exact finite fields as a fault-sensitive regression.

Distinct `CTAU` values cannot merge. The marked-pair stabilizer fixes the
three intrinsic points \(s,t,h\), hence acts identically on the pencil
line. Source translations change the cubic jet only by a derivative of
the leading pair, which lies in the leading target plane; the normal
quotient kills it. A target basis change moves all pencil coordinates
simultaneously and preserves the cross-ratio. The unique annihilator of
the leading target plane permits only a scalar change of the normal
component.

## Exact comparison checker

`verify_marked_orbit_hostile_2.py` uses only the Python standard library.
It pins the frozen candidate, clean-room report, and sealed log; parses all
thirteen stable suffixes; verifies
\(\theta=1/(1+\tau)\); and checks every homogeneous boundary predicate.
The strict wrapper repeats the checker under optimized Python and rejects
four deliberate mutations:

```text
drop_stratum
wrong_conversion
overlap_boundary
merge_tau
```

Successful output ends with

```text
MARKED_ORBIT_HOSTILE_2_PASS_C4B821
MARKED_ORBIT_HOSTILE_2_STRICT_PASS_91A73E
```

No taxonomy defect was found.
