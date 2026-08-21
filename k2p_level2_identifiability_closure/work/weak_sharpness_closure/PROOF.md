# Weak-class sharpness over the principal K2P domain

## Statement

For every \(n\geq 3\), there are two nonisomorphic binary level-2
semi-directed networks on the same labelled leaf set which are weakly
tree-child but not strongly tree-child, are not related by an ordinary
triangle redirection, and whose strict continuous-time K2P images have a
common \((4n-3)\)-dimensional analytic germ.  Consequently the strong
tree-child hypothesis in the K2P identifiability theorem is sharp, already
inside the strict continuous-time subdomain.

## The three-leaf pair

Let \(W\) be the `theta0` core with the ordinary boundary leaf on the
\(V\to X\) segment, the incoming boundary leaf labelled 0, the segment leaf
labelled 1, and the sink child labelled 2.  Let \(W'\) be the bare `theta3`
core with incoming leaf 0 and its two sink children labelled 1 and 2.

Suppressing the displayed root while retaining reticulation arrowheads and
then enumerating every edge on which a root can be reinserted gives

\[
  (\#\text{ admissible},\#\text{ tree-child})=(5,2)\quad\text{for }W,
  \qquad (7,2)\quad\text{for }W'.
\]

Thus both networks are weakly tree-child and neither is strongly
tree-child.  Exact labelled mixed-incidence comparison finds neither an
isomorphism nor the ordinary-triangle relation between them.

## A common strict continuous-time point

Use the Fourier character order recorded in
`weak_sharpness_certificate.json`.  Put \(\delta=2^{-30}\).  For \(W\), set
every one of its seven internal edge classes to

\[
  (s_i,g_i)=(1/7,1/7),
\]

and put

\[
 (\lambda_0,\lambda_1)=(15996/16339,1/8).
\]

For its pendant arms at leaves \(0,1,2\), respectively, set \(s=g\) equal
to

\[
  \frac{86779}{80}\delta,
  \qquad \frac{320}{253}\delta,
  \qquad \frac{114373}{20240}\delta.
\]

For \(W'\), set every internal class to \((1/4,1/4)\), take
\((\lambda'_0,\lambda'_1)=(1/2,1/6)\), and set the three pendant pairs to

\[
  \frac{16}{3}\delta,
  \qquad \frac{32}{9}\delta,
  \qquad \frac{96}{5}\delta.
\]

Every displayed pair is positive and satisfies \(s^2<g<1\), so the two
points are strict continuous-time points and hence belong to
\(\mathcal D_+\).  Direct expansion of the four displayed-tree switch terms
gives the same tensor for both networks:

* \(q_{000}=1\);
* every one of the six two-nonzero-character orbit coordinates is
  \(\delta^2\);
* every one of the three all-nonzero orbit coordinates is
  \(\frac45\delta^3\).

At these exact parameter points the two normalized three-port Jacobians
both have rank 9.  The certificate contains nonzero rational \(9\times9\)
minors.  Multiplication by the nonzero pendant factors is an invertible
diagonal change in the nine nonconstant coordinates, so the full physical
maps also have rank 9.  The real-analytic submersion theorem therefore gives
a common open nine-dimensional germ at the displayed tensor.

## Cherry induction

Replace the same labelled leaf on both networks by the same pendant cherry.
In either the \(s\)- or \(g\)-sector, let the two new pendant eigenvalues be
\(u,v\).  Around a point where all relevant Fourier coordinates are
nonzero, two rational local observables can be chosen as

\[
  R=u/v,\qquad P=uv.
\]

Their Jacobian determinant is

\[
  \det \frac{\partial(R,P)}{\partial(u,v)}=\frac{2u}{v}\ne0.
\]

The two K2P sectors are independent, so the four-variable block determinant
is \(4u_su_g/(v_sv_g)\ne0\).  Each cherry therefore adds exactly four local
dimensions.  Starting at dimension 9 on three leaves gives

\[
  9+4(n-3)=4n-3.
\]

Choosing every added edge with \(s=g\in(0,1)\) keeps the construction in the
strict continuous-time cone.  A tree-child and a non-tree-child rooting of
each base graph lift through the cherry.  Conversely, pruning the newly
labelled cherry and suppressing its bivalent parent recovers the base graph.
Hence weak-not-strong membership persists.  The same pruning argument shows
that a labelled isomorphism or ordinary-triangle relation between the
extended pair would induce one between \(W\) and \(W'\), which has already
been excluded.

## Replay

Run `verify_weak_sharpness.py`.  It rebuilds the primitive graphs, performs
the complete rooting enumeration, compares the mixed graphs, expands both
K2P maps, checks the physical inequalities and common tensor, verifies both
rank minors, and checks the cherry determinant.  It opens no frozen atlas
pickle.
