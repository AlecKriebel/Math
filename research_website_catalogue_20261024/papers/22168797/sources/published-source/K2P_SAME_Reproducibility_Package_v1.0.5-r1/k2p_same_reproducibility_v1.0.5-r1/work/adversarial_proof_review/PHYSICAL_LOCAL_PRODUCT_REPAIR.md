# Physical saturation needed by the local product chart

The incidence anchors by themselves construct a slice only on the ambient
positive component-tensor locus.  The following serial-edge lemma supplies
the additional physical step.

Fix a physical bridge pair `(S,G)` in `D_plus` and put

\[
M=\max\{S,G,2S-G,0\}<1,
\qquad
r=1-\frac{1-M}{4}.
\]

Bernoulli's inequality gives

\[
r^2\ge 1-2\frac{1-M}{4}=\frac{1+M}{2}>M.
\]

Hence all three pairs

\[
(r,r),\qquad (S/r^2,G/r^2),\qquad (r,r)
\]

lie in `D_plus` and their coordinatewise product is `(S,G)`.  Interpret the
outer factors as component-side half-edge factors and the middle factor as
the residual bridge.  The three-edge path suppresses to the original bridge,
so it has exactly the same observable model and standard semi-directed
topology.

Every defining inequality is strict.  Therefore the left outer pair, right
outer pair, and residual middle pair remain in `D_plus` when the two outer
pairs vary independently in a sufficiently small four-dimensional open
neighborhood and the middle pair is adjusted to preserve the two effective
products.  Thus both K2P sectors at both bridge incidences are locally
physical directions, not merely ambient tensor gauges.

Choose the anchor slice through the given physical point, so its incidence
normalizer is the identity there.  Nearby normalizers are close to the
identity.  The split representation above realizes those nearby endpoint
normalizers physically.  Combining this local physical saturation with the
full-rank marked/pair anchor matrices and positive rank-one extraction gives,
at every positive regular point, an analytic physical product germ of sliced
projective local tensor germs and two effective bridge coordinates per
bridge.  The normalized slice representative itself need not be a physical
unsplit component tensor.

The same argument works simultaneously on every bridge because there are
finitely many strict inequalities and the bridge quotient is a tree.  Shrink
to the minimum of the finitely many open neighborhoods.

For strict continuous time one may use coordinate cube roots instead:

\[
(S^{1/3},G^{1/3})^3=(S,G),
\]

and `S^(2/3)<G^(1/3)` is equivalent to `S^2<G`.  Strictness again gives the
required independent local neighborhoods.

