# Finite structure of the remaining one-active branch

## 1. Claim boundary

After the affine-infeasible branch is removed, exactly 1,227 residual
support pairs have a nonempty feasible failure set consisting only of
one-active descriptors.  They give 3,297 pair--descriptor incidences.
This note is a finite structural certificate for that table.  It does not
prove a stochastic service theorem, pair recurrence, or T3-2.

The executable certificate is
`src/one_active_remaining_structure.py`, with focused regression in
`tests/test_one_active_remaining_structure.py`.  It relabels the active
species to (C), quotients (A/B) exchange where possible, and freezes the
following hashes:

```text
rows     a05082a912f7629d107d14609a2ee65cae7b8eb997d7a17a4ac9934c1b66986d
payload  283c02163c6a57cb10e9c13a47ad84cb3457ce9d428276719cf9e69dd3343034
```

All analytic, pair-recurrence, and global flags remain false.

## 2. Three fast-phase architectures

The active-degree-one menu is

\[
 \{C,A+C,B+C\}.
\]

Stripping the common active molecule leaves a subset of the unimolecular
menu \(\{0,A,B\}\).  Every incidence has exactly one of these architectures:

\[
\begin{array}{c|r}
\text{architecture}&\text{incidences}\\ \hline
\text{one lower-only linkage and one mixed killed phase}&2030\\
\text{two mixed killed phases}&1045\\
\text{one open wholly-top phase and one mixed killed phase}&222
\end{array}
\tag{2.1}
\]

The order-sensitive executable split is

\[
 1784+246+1045+222=3297.
\tag{2.2}
\]

In all 222 wholly-top rows the stripped support is the single
immigration--death pair \(\{0,A\}\), up to inactive-species exchange.  No
conservative pair, open triple, branching phase, or second countable shape
occurs.

## 3. Initial access and promotion boundaries

At the exact inactive cap the initial physical access modes are

\[
\begin{array}{c|r|r}
\text{mode}&\text{incidences}&\text{pairs carrying at least one such row}\\ \hline
\text{mixed top source already enabled}&2471&917\\
\text{only a zero-source seed}&461&435\\
\text{a nonzero lower seed}&20&10\\
\text{open wholly-top countable phase}&222&74\\
\text{frozen face}&123&123
\end{array}
\tag{3.1}
\]

The frozen rows have no enabled reaction on the displayed face.  They are a
fixed-class alternative, not a uniform service episode.  Every nonfrozen
row records which of (A,B) can leave its bounded cross-section through a
fast stripped reaction and which can change somewhere in the full support.
The exact fast/full-coordinate histogram is

\[
\begin{array}{c|r}
A/A&24\\
A/AB&534\\
AB/AB&1940\\
B/AB&319\\
B/B&70\\
\varnothing/A&6\\
\varnothing/AB&364\\
\varnothing/B&40
\end{array}
\tag{3.2}
\]

No incidence has a full-network affine invariant with nonzero active
coefficient.  This zero count is forced by affine feasibility: with both
inactive coordinates capped, such an invariant would forbid (C\to\infty).
Thus the positive-coefficient invariant alternative has already been
removed before this 1,227-pair branch.

## 4. Canonical reflected-debt depth regression

For a finite kinetic diagnostic only, orient each linkage by the canonical
failing Hamilton cycle used by the tier obstruction certificate.  Project
onto (A,B), start at the exact cap, and update reflected active debt by

\[
 D^+=(D+\Delta C)^+.
\tag{4.1}
\]

A degree-zero reaction costs one kinetic level precisely when it fires while
an active-degree-one source is enabled.  Zero--one shortest paths are
computed in the fixed box (A,B\le7), (D\le8).  The first search records
positive-debt states with no fast clock; the second stops only at a genuine
surplus exit (D=0,\Delta C=-1).  This is a canonical-cycle regression, not
an arbitrary-strong-orientation proof and not a finite-box recurrence
argument.

The exact incidence split is

\[
\begin{array}{c|r}
\text{canonical word class}&\text{incidences}\\ \hline
\text{no positive-debt base reached}&2228\\
\text{zero-contest service from every reached debt base}&906\\
\text{both zero-contest and nested service bases}&32\\
\text{every reached debt base needs a slow-before-fast service}&131
\end{array}
\tag{4.2}
\]

Among the 1,069 rows with a positive-debt base, creation has strictly larger
kinetic depth than surplus service in 994.  Exactly 75 incidences on fifteen
pairs have equal depth; none has creation shallower than service and none
lacks a service word in the displayed box.  In every equality row,

\[
 D=1,\qquad m_{\rm create}=m_{\rm service}=2.
\tag{4.3}
\]

The fifteen-pair fingerprint is

```text
6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3
```

Each of the fifteen pairs contributes exactly five equality rows.  All five
use the same physical active coordinate (C) and the same physical linkage
\(\{0,A+C,B+C\}\); the linkage is not switched between relabelled axes.
Thus the 75-row equality family has one fixed shell coordinate
\(Q=C-A-B\) per pair and no multi-tube compatibility seam of its own.

After active-(C) normalization, every critical row has one linkage

\[
 \{0,A+C,B+C\},
\tag{4.4}
\]

and its other linkage is drawn from \(\{A,B,2A,A+B,2B\}\).  The fifteen
original pairs collapse to nine normalized support templates after the
inactive-(A/B) exchange.  Both the exact fifteen-pair payload and the nine
templates are frozen by the executable certificate.  Thus exponent
comparison alone cannot close these fifteen pairs: the order-(N^{-2})
creation and service coefficients, endpoint factorial rewards, and rates
must be compared in one killed physical episode.

These fifteen pairs have 83 feasible one-active failures in total, not just
the 75 equality rows.  Their exact failure-count histogram is

\[
 \#\{P:\lvert\mathcal F_1(P)\rvert=5\}=8,\qquad
 \#\{P:\lvert\mathcal F_1(P)\rvert=6\}=6,\qquad
 \#\{P:\lvert\mathcal F_1(P)\rvert=7\}=1.
\tag{4.5}
\]

The eight additional rows consist of six direct-enabled rows with no
positive-debt base and two zero-source seed rows with zero-contest service
and strictly favorable creation/service depth.  Their complete descriptors
and templates are frozen in the payload.  None of the fifteen pairs belongs
to the already audited exact-92 selector, so these eight rows still require
composition even though their local routing types are simpler.

### 4.1 Exact shell-average identity for the critical support

The equality family has more structure than its word depths show.  Put

\[
 Q=C-A-B.
\tag{4.6}
\]

The mixed linkage \(T=\{0,A+C,B+C\}\) preserves \(Q\), is weakly reversible,
and has deficiency zero.  Let \(K_0,K_{AC},K_{BC}>0\) be its directed
matrix-tree weights and set

\[
 u=K_{AC}/K_0,\qquad v=K_{BC}/K_0,\qquad s=u+v.
\tag{4.7}
\]

On the shell \(Q=N\ge0\), its conditional product-form law is exactly

\[
 \pi_N(i,j,N+i+j)
 =\frac1{Z_N}\frac{u^i v^j}{i!j!(N+i+j)!},
 \qquad
 Z_N=\sum_{m\ge0}\frac{s^m}{m!(N+m)!}.
\tag{4.8}
\]

Consequently, for all nonnegative integers \(r,t\),

\[
 \mathbb E_{\pi_N}[(A)_r(B)_t]
 =u^r v^t\frac{Z_{N+r+t}}{Z_N},
\tag{4.9}
\]

and, writing \(k=r+t\),

\[
 e^{-s/(N+1)}\frac{N!}{(N+k)!}
 \le \frac{Z_{N+k}}{Z_N}
 \le e^{s/(N+k+1)}\frac{N!}{(N+k)!}.
\tag{4.10}
\]

Every one of the nine normalized lower supports contains total-degree-one
and total-degree-two complexes.  Strong connectivity therefore forces at
least one directed unary-to-quadratic edge.  If \(a_->0\) is the sum of its
rate-weighted unary monomials and \(a_+\ge0\) is the corresponding sum over
quadratic-to-unary edges, the exact stationary shell drift is

\[
 \overline{\mathcal L_RQ}(N)
 =-a_-\frac{Z_{N+1}}{Z_N}
  +a_+\frac{Z_{N+2}}{Z_N}<0
\tag{4.11}
\]

for all sufficiently large \(N\).  Indeed
\(Z_{N+2}/Z_{N+1}\le e^{s/(N+2)}/(N+2)\).  Formula (4.11) is an exact
finite-support check and identifies a promising \(Q^2\) regenerative
episode.  It is not, by itself, the killed-resolvent, endpoint-moment, or
common-potential composition theorem needed to promote the fifteen pairs.

## 5. Smallest analytic routing table

Retaining linkage order and exact caps gives 63 fine templates.  Quotienting
linkage order and then forgetting cap values after retaining the stripped
phase, initial access, canonical debt class, and fast promotion coordinates
leaves exactly **23** analytic templates.  Their complete machine-readable
payload is frozen in the certificate.  At a coarser proof-design level they
require only five mechanisms:

1. a finite-class argument for the 123 frozen faces;
2. a killed mixed-phase block for the 2,471 direct rows;
3. a seed-and-drain block for the 461 zero-source and twenty nonzero-source
   rows;
4. a Poisson occupation/killed-resolvent block for the 222 open phases; and
5. a coefficient-sensitive reflected-level episode for the 75 equal-depth
   incidences, with the remaining 994 debt rows having a favorable strict
   exponent separation in the canonical regression.

The fifth item is the first finite obstruction to a universal proof based
only on kinetic exponents.  Extra directed edges can change both favorable
and unfavorable coefficients, so no Hamilton-cycle count is promoted to an
arbitrary-orientation theorem by monotonicity.

## 6. What remains analytic

A valid one-active theorem must still retain every physical reaction and
prove, for arbitrary strong orientations and positive rates, one of:

1. a strict reflected-level decrease in finite mean time;
2. a controlled exit into a refined multi-active descriptor, with endpoint
   moments sufficient for common-entropy gluing; or
3. a genuinely finite classwise alternative.

For the fifteen critical pairs it must additionally compute the leading
order-(N^{-2}) coefficient rather than infer its sign from depth.  Until
those statements are proved, the 1,227-pair recurrence count and global
T3-2 remain uncertified.
