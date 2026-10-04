# Exact claim and scope

Let U be a nonempty connected open subset of C, let O(U) denote its holomorphic
complex-valued functions, and write G_h=h(U). A source sequence escapes when it
eventually avoids every compact subset of U. For U=D this is equivalent to
|z_n| tending to 1.

The L-property for h on that sequence says that h(z_n) eventually avoids every
compact subset of its **actual image** G_h. An ordered pair (f,alpha) has the
implication

\[
f\text{ has L}\quad\Longrightarrow\quad\alpha\text{ has L}.
\]

The direction is essential. A nonconstant alpha is an L-atom when, for every
f in O(U) satisfying that implication on every source-escaping sequence,
there is phi in O(G_alpha) with f=phi composed with alpha. Constants f are
allowed; they automatically descend and cause no exception.

## Results certified by the written proof

1. The original unit-disk equivalence: alpha is an L-atom if and only if alpha
   is injective. This is a reconstruction of the prior 2026 public proof.
2. The same equivalence for **all plane domains U**, using the compact-source-
   escape convention just specified. The separator lemma in PROOF §5 provides
   the additional step beyond the prior manuscript's bounded-domain corollary.
   This consequence is not promoted as historically novel.
3. Given any nonconstant alpha in O(U) and any b in O(U), a holomorphic H on
   G_alpha can be chosen so that H composed with alpha + b maps U onto C.
   H is permitted to depend on b. This is the prior construction reconstructed
   in PROOF §3.

No properness, finite valence, boundary regularity, simple connectivity,
boundedness of U, or absence of critical points is assumed.

## Explicit limits

- The open-ended words about more general domains do not uniquely specify a
  convention. Result 2 gives a precise answer for planar domains, including C,
  punctured, multiply connected and unbounded domains, under compact escape.
- No classification of arbitrary nonplanar open Riemann surfaces is asserted.
- No several-complex-variable theorem is claimed. The distinct Problem 2.56
  is used only as a related-source/prior-credit check; its queue entry is not
  changed.
- No effective Runge algorithm, growth bound, finite-order surjectivizer,
  infinite-valence result, or fully formalized analytic proof is claimed.
- One cannot fix H and then allow every analytic b: choosing b=-H composed
  with alpha makes the resulting function constant. The order is for each b,
  there exists H.
- A bounded subset of a proper image G_f need not be relatively compact in
  G_f. Surjectivity onto C is proved before using boundedness for orderedness.

## Success and disposition

The full unit-disk equivalence is established in the reconstruction. The
proposed queue disposition after independent approval is `already_solved`,
`1/5`, explicitly crediting the prior public source. The planar consequence
must be described separately from this prior-resolution classification.
