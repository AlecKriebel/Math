# Exact phase split in the two-active promotion gate

This note records a finite reduction, not a recurrence theorem.  Among the
1,416 affine-feasible two-active promotion incidences,

\[
 1,366+50=1,416.
\]

The first 1,366 have no linkage wholly contained in the global top D-tier.
Every top component is therefore killed on reaching its linkage's lower
part.  This is the exact support premise for a finite killed-carrier/debt
argument at the separated top/lower source scales.

The remaining 50 incidences, on 50 support pairs, have one wholly-top
linkage.  Their support histogram is

\[
\begin{array}{c|r}
\text{whole-top support}&\text{incidences}\\ \hline
\{B,2A\}&16\\
\{B,A+C\}&10\\
\{A,B+C\}&10\\
\{A,B\}&6\\
\{A,B,A+C\}&4\\
\{A,B,B+C\}&4.
\end{array}
\]

The first four rows are finite rank-one shells, totaling 42 incidences.
In the last two rows the cap-zero dynamics consists of an \(A\leftrightarrow
B\) conservative shell coupled to a one-dimensional, active-scale
immigration--death cofactor.  These eight rows are the only countable phase
left in the promotion table; no generic two-dimensional countable
environment is hidden here.

There are 803 promotion support pairs.  The no-whole-top rows occur on 766
pairs and the whole-top rows on 50 pairs, with 13 pairs appearing in both
incidence modes.  The exact row fingerprint is

```text
3e3616f8099b93ccd860db2e3320cd90300c8adf896f12127cae1a32f7d7bfe5
```

The intended analytic split is now exact:

1. generalize the audited mixed killed-carrier theorem from active
   coordinate \(X\) to the integer descriptor workload \(H_w\), using the
   lower/top source-scale ratio for the unresolved-arrival error;
2. use the audited rank-one shell endpoint estimate on the 42 finite-phase
   rows; and
3. use the one-dimensional Poisson corrector on the eight open rows.

Each step must prove drift for the common corrected factorial potential and
retain every physical reaction.  The executable deliberately leaves the
analytic certification flag false.
