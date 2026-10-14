# Additional review of the four-known-deadlines proof

Reviewed artifact: `../pass3_deadlines/FOUR_DEADLINES.md`.

Frozen SHA-256:
`08de8b73684d080eacf1d1f558f126bccb1e8a500d6e71d3802cf715c1c678e8`.

Date: 2026-10-14. Review belongs to shared PASS3.

## Result and scope

No defect found in the analytic reduction, online composition, or the
matching exact-arithmetic implementation. A read-only replay of the
checker functions verified all 180 cases, with maximum cost
`34777/50976` at scales `(2,2,2)`. No frozen artifact was rewritten.
This replay reused the inspected checker functions; it is not described
as an independently implemented numerical verifier.

The result remains a computer-assisted theorem for four known allowed
deadlines, with an adaptive Devil. It is not an all-finite-set theorem
or a resolution of the unrestricted game.

## Analytic checks

- The exact concentration on each endpoint set is a valid bound for
  every adaptive translated update. The denominator reserves both the
  boundary announcement and maximum wait. Each phase ends strictly
  below its downstream hazard threshold, for every boundary choice.
- Exact concentration is no larger than the prior mass/peak bound.
  Inductively, larger denominators give pointwise smaller corresponding
  kernels, so the inherited one-stage and two-stage bounds apply.
- The mass/peak series bound follows by separating dyadic scales below
  and above `sqrt(beta/(9 alpha))`. Its constant `8/3` is valid, including
  the case where the crossover is below the smallest scale.
- Case A yields `4/9+15/a`, at most `263/288` for `a>=32`.
- In Case B, `b>=4a` makes the non-point peaks smaller than the delta's
  contribution at every scale up to `a`. The remaining envelope product
  is `5103/1000<25/4`, giving `83/84` when `b>=16`.
- Outside A and B, the dyadic restrictions imply `a<=16,b<=32`.
  In Case C, `c>=64` therefore gives `c>=2b,c>=4a`, making the far kernel
  unable to change either preceding normalization. The extra envelope
  gives `4/5+168/(25c)<=181/200`.
- The remaining rectangular list has exactly `5*6*6=180` triples and
  covers every gap-scale triple not already certified analytically.

## Infinite-tail and implementation checks

For `k>=1`, the one-dimensional endpoint set consists exactly of the
integers in its containing interval that are not divisible by four.
This follows from the disjoint translated recursion. A sufficiently
long translated endpoint window contains the entire finite kernel
support while allowing all four omitted residue alignments. Hence its
maximal mass is the total coefficient sum minus the smallest residue
sum. This is an exact identity, not a truncation estimate.

All kernels are separable outer products of nonnegative one-dimensional
convolutions. The maximal translated two-dimensional sum is therefore
the square of the maximal one-dimensional sum. The implemented
convolution agrees with correlation because the endpoint indicators
are symmetric. Sorting convolution-scale lists preserves the kernel.

The tail-start scale used by the checker is conservatively large enough
for the residue identity for every kernel. At all later dyadic scales,
the unnormalized maximal mass is constant, so the remaining cost is
exactly `4 mass/(9 b_start)`.

The replay explicitly checked positive denominators and costs below one
for each case using integer and rational arithmetic. The first deadline
remains unrestricted because the certificate controls the full infinite
profile series.

## Information boundary

Scales and denominators depend only on the four known deadlines. Hazard
values depend only on observed announcements. No traversal contains an
allowed intermediate lethal time; all four lethal moves and the
post-move boundary updates are included. Nothing in this review extends
the proof to an unbounded number of deadlines.
