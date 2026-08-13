# Independent hostile audit of the hard one-active 1,104 theorem

**Verdict (2026-08-12 PDT): FAIL as written, with a small analytic repair
available.**  No orientation, history, or T3-2 counterexample was found.
The finite partition, the generalized-951 import, and the exact-48 label
repair survive.  The present proof does not, however, justify the claimed
fourth-power drift for the 99 direct rows (and makes the same unsupported
subpower-start extension in the six open rows).

The audited frozen bytes are

```text
note   b5a07c037546c6a792606389fc4dcdf4bfa1601b9ff3dfab848a921b27e22764
source 81c457cf9139fa709696df00cf876d8c843129e39603ce81b9d4aa086946bb63
tests  a7cfe50968cdb18255d366df049feab106d57b0bc1c395334a4b20570da9c67f
rows   b6b9d1afa9b153689220fbbda6cc0b020a9a6ee1fe8cfe99d746c5ea8d71a83b
payload 702cf1b1e37c7014268f683d147408d7e397d1463523a9bb650df0e5a87ed6c8
```

## 1. What passes

The executable replay gives the exact disjoint partition

\[
 1104=951+99+48+6
      =951+99+44+4+6.
\]

It reproduces the family histogram, the eight translated exact-Family-II
support types, the `40+8` inherited graph labels, and the repaired `44+4`
analytic routing.  The row and payload hashes match.  Every pair and global
flag remains false.

The 951 rows are exactly the incidences normalized by the generalized
146-template map: their incidence keys agree, their support union has 146
members, and the spectator-cap multiplicities are `317+317+317`.  Accepting
the separately returned strict PASS at the pinned generalized bytes, this
part composes under the same arbitrary fixed \(\ell\), actual endpoints,
and path-labelled boundary interface.

For the 48 exact-Family-II-labelled incidences, hostile translation gives
exactly eight support pairs.  In every pair:

1. the sole active-bearing source is \(q=V+I\) and the cofactor cap is zero;
2. both linkage supports have at least two vertices;
3. every vertex belongs to
   \(\{0,U,2U,I,2I,U+I,q\}\);
4. at least one linkage is mixed after deleting \(q\); and
5. the proper linkage is not an exact pair \(\{aU,q\}\).

These are the full hypotheses of the abstract mixed fast-Schur theorem, not
merely a signature match.  Thus its strong-cut inverse, killed spectator
Green estimate, one-sided terminal entropy majorant, physical duration, and
actual-endpoint estimates extend to the 44 nonfrozen incidences.

The four cap-zero alternatives are genuinely frozen.  At \(U=I=0\), every
source requires \(U\) or \(I\), including \(q\), and neither support contains
zero.  Such a state is an absorbing singleton if it lies in a closed
irreducible class, so its reachable reflected lift has zero debt.

The displayed five-edge word is physically correct.  On

\[
 \{I,U+I\},\qquad \{U,2I,2U,q\},
\]

it sends

\[
 (1,0,0)\to(0,0,2)\to(0,1,1)\to(1,1,1)
 \to(0,2,2)\to(1,2,0)
\]

in \((U,V-n,I)\)-coordinates.  Complete digraphs make both it and its
reverse physical, and unused initial \(U\)-molecules are slack.  Hence the
old eight-row no-history exclusion is false exactly where the candidate
says it is false.

The marked scope also passes.  On the reachable reflected lift,
\(D_V=0\) implies \(V=H_V\le x_V^\circ\).  Before the included first
crossing below \(n\), reflection is inactive, so that crossing services
actual incoming debt.  The stopping rules depend on the mark only through
this initial eligibility check.  The stated priority retains the causing
reaction, and only the path-labelled closed outer endpoint is a \(P\)
handoff; other open boundaries remain charged at their actual population.

## 2. The missing direct-phase implication

The theorem quantifies over

\[
                 u=n^{o(1)},
\]

not merely over a bounded or class-fixed inactive start.  Section 4 proves
an exponential Foster estimate for the stripped killed unimolecular phase
and invokes nested exponential weights for paid insertions.  Those facts do
give the aggregate killed phase, every fixed endpoint and duration moment,
and the sourcewise paid probability \(n^{-1+o(1)}\), provided their
dependence on the start is made polynomial.  They do **not** by themselves
give the first-order entropy estimate needed in (4.2).

Write the inactive factorial-linear part as

\[
 B_\ell(a,b)=\log(a!)+\log(b!)+\ell_Aa+\ell_Bb.
\]

The active service contributes \(-\log n\) to \(\Delta G_\ell\), but the
candidate never proves

\[
 \mathbb E[B_\ell(A_\sigma,B_\sigma)-B_\ell(A_0,B_0);D]
                 =o(\log n).                         \tag{2.1}
\]

The exponential Lyapunov estimate displayed as (4.1) controls a weight
proportional to \(e^{\theta u}\) from a deterministic start \(u\).  This is
not \(n^{o(1)}\) for a general subpower sequence; for example,
\(u=\exp\sqrt{\log n}\) is \(n^{o(1)}\) but
\(e^{\theta u}\) is much larger than every power of \(n\).  Even a
polynomial endpoint bound only gives \(n^{o(1)}\), which need not be
\(o(\log n)\).  Thus it controls the quadratic through quartic Taylor
remainders, after division by the leading factor \(G\), but not the
first-order \(4G^3\mathbb E\Delta G\) term.

The sentence that a fixed correction changes each bounded physical jump by
\(O_\ell(1)\) does not close this gap: a killed unimolecular burst can make
an unbounded number of top conversions from a subpower initial cloud.
Those clean top-phase moves are not paid insertions.  Consequently the
endpoint-weighted paid remainder does not account for their accumulated
factorial-linear increment.

This is a proof gap, not evidence that the structural claim is false.  The
independent-particle/killed-cut structure strongly suggests the needed
one-sided estimate.  A sufficient repair is an aggregate terminal-entropy
lemma of the form

\[
 \mathbb E[B_\ell(Z_D)-B_\ell(z);D]
 \le C_\ell\log(2+|z|)+C_\ell,
 \qquad
 \mathbb E|\Delta B_\ell|^r\le C_{r,\ell}(1+|z|)^{C_r},       \tag{2.2}
\]

with the paid and boundary versions weighted by
\(n^{-1}(1+|z|)^{C_r}\) and the stopped third-order remainder.  Since
\(\log(2+u)=o(\log n)\), (2.2) gives (2.1), while the polynomial bounds give
all required orders \(q>8\), physical-duration integrability, and the last
three terms of the exact fourth-power expansion.  This lemma must retain
the actual killed endpoint and work for arbitrary fixed \(\ell\).

The pinned universal direct-phase proof starts its nested Green hierarchy
from a fixed base set; it does not state (2.2) for arbitrary
\(u=n^{o(1)}\).  Calling the present assertion the “premise-level universal
killed-phase theorem” therefore does not import the missing statement.

## 3. The same subpower seam in the six open rows

The six supports and their Poisson structure are correct:

\[
 \{C,A+C\},\qquad\{0,B,2B,B+C\}.
\]

The full countable theorem gives a fixed-positive service block, geometric
completion, an \(O(n^{-1})\) unresolved alternative, polynomial endpoints,
and physical-duration moments.  Its written entropy episode is for
bounded-moment inactive starts.  The present theorem again allows a
deterministic subpower start.  Polynomial endpoint moments alone do not
turn its inactive factorial-linear contribution into \(o(\log n)\).

The corresponding smallest repair is the one-dimensional analogue of
(2.2) for the stopped immigration--death service episode, including the
unresolved and moving-boundary weights.  Alternatively, the theorem could
be restricted to bounded/class-fixed inactive starts and every unbounded
spectator sequence could be routed by a separately proved actual-descriptor
coverage theorem.  The current frozen note does neither.

## 4. Reproduction

The focused and dependent replay ran 19 tests successfully, including the
1,104 certificate, generalized-146 certificate, and easy/common-potential
certificate.  The four countable-phase regression tests also passed.
Python compilation succeeded.  Pandoc produced both standalone HTML and
LaTeX renders without an error.  These finite and rendering checks do not
supply the missing one-sided entropy estimates.

Accordingly the correct strict status is: generalized 951 **PASS**;
direct 99 **analytic repair required**; exact 44+4 **PASS**; open six
**subpower entropy repair required**; unified 1,104 theorem **FAIL as
written**.  No pair or global flag may be promoted from this snapshot.
