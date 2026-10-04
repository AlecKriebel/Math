# Self-splitting branched surfaces: source audit and unresolved converse

**Target:** 10300016 / AMR-102-0016, Calegari's Question 7.1 (Agol).
**Outcome:** unresolved. Two approaches stop at explicit geometric gaps.
**Novelty:** none claimed. In particular, the invariant-measure observation is
already in the original source.

## 1. Exact question and scope

> Characterize branched surfaces embedded in 3-manifolds which can be
> non-trivially split to a homeomorphic copy of themselves.

This is Question 7.1 on printed page 13 of
[Calegari (2002)](https://arxiv.org/abs/math/0209081). The heading about
triangulations does not impose a triangulation or foliation hypothesis on the
question. Definition 1.9 uses a branched two-complex with a well-defined tangent
plane and generic branch locus. The question does not explicitly restrict the
ambient manifold to an atoroidal, fibered, or sutured setting.

The wording does not specify that the return homeomorphism extends to an ambient
isotopy, nor give a separate formal definition of nontriviality. No such stronger
interpretation is imposed here. A return map on transverse measures additionally
requires a compatible identification of the branched structures, not just an
unexplained identification of their underlying cell complexes.

The following source remarks already discuss projectively invariant measures and
pseudo-Anosov examples. They also warn that repeated splitting may produce only
a partial lamination, and ask separately about extending it to a carried
lamination. Those observations are prior work, not conclusions of this attempt.

## 2. Approach 1: the transverse-measure cone

For a finite sector decomposition, let

\[
 C=\{w\in\mathbb R^s: w_i\geq 0,\ Rw=0\}
\]

be the cone of transverse weights, where the rows of \(R\) are the branch
equations. The finite-sector hypothesis is part of this particular route; it is
not a new restriction on the target question. A geometric splitting together
with a compatible return identification can be studied through its linear
carrying map on weights. Such a map is extra data to be constructed or verified.
It must not simply be postulated because \(C\) exists.

Here is the precise finite-dimensional fact used by the route.

**Lemma (standard projective fixed-point argument).** Suppose \(C\ne\{0\}\),
\(A\) is a linear map with \(A(C)\subset C\), and
\(Aw\ne0\) for every \(w\in C\setminus\{0\}\). Then there are
\(w\in C\setminus\{0\}\) and \(\lambda>0\) such that \(Aw=\lambda w\).

**Proof.** Write \(\ell(w)=\sum_iw_i\). The set
\(K=C\cap\{\ell=1\}\) is nonempty, compact, and convex. For every \(w\in K\),
\(Aw\in C\setminus\{0\}\), so \(\ell(Aw)>0\). Thus

\[
 F:K\longrightarrow K,\qquad F(w)=\frac{Aw}{\ell(Aw)}
\]

is continuous. Brouwer's fixed-point theorem, applied in the affine span of
\(K\), gives \(F(w)=w\). Hence \(Aw=\ell(Aw)w\), with
\(\lambda=\ell(Aw)>0\). This also covers the case that \(K\) is a single point.
\(\square\)

This proves a statement about a **specified** cone-preserving map. It is an
explicit version of the already-known source observation, not a criterion
constructing a geometric self-splitting.

### Exact failures of stronger algebraic shortcuts

The following examples are only linear-algebra controls. No claim is made that
they are realized by a particular embedded branched surface.

1. Let \(C=\mathbb R_{\geq0}^2\) and
   \(A=\left(\begin{smallmatrix}2&1\\0&1\end{smallmatrix}\right)\).
   This map preserves \(C\) and kills no nonzero point of \(C\). If
   \(w=(x,y)\) were a strictly positive eigenvector, the second coordinate would
   give \(\lambda=1\), whereas the first would give \(x+y=0\), a contradiction.
   The nonnegative eigenray is \((1,0)\), with eigenvalue 2. Thus the lemma does
   not yield full support.
2. For
   \(A=\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)\), the same
   cone hypotheses hold, and \(A\ne I\), but the characteristic polynomial is
   \((t-1)^2\). Therefore nonidentity of a matrix does not imply an invariant
   weight with eigenvalue greater than 1. Nontriviality of a *geometric*
   splitting cannot be silently replaced by nonidentity of this matrix.
3. Every cone \(C\) admits the identity map, and every nonzero point is an
   eigenvector for it. Merely asking for a nonnegative cone-preserving matrix
   with a nonnegative eigenvector therefore supplies no geometric return data.

**Gap after Approach 1.** No converse reconstructs a legal nontrivial splitting,
an embedded returned carrier, and its required homeomorphism from these
equations. The cone also omits the ordering of sheets in interval fibers and
the complementary embedding data. Moreover, the original question does not
assume \(C\ne\{0\}\). The lemma cannot characterize all objects in its scope.

## 3. Approach 2: periodic splitting and a limiting lamination

One could try to reduce every self-splitting carrier to a periodic train-track
construction, then use a classification in that more structured category.
The relevant primary results require hypotheses that this reduction has not
provided:

- [Agol, Theorem 3.5](https://arxiv.org/abs/1008.1606) starts with a
  pseudo-Anosov surface map and a measured train track suited to its stable
  lamination. Maximal splitting is eventually periodic modulo that map and
  measure rescaling. This is a construction in a supplied dynamical setting.
- [Landry–Tsang, Theorem 7.10](https://doi.org/10.2140/gt.2025.29.4531)
  constructs an unstable veering carrier for the unstable Handel–Miller
  lamination of a depth-one foliation on an atoroidal sutured manifold.
  Theorem 9.22 determines such a veering carrier up to isotopy from its positive
  boundary train track, assuming it **compatibly** carries the prescribed
  lamination. Compatibility includes full carrying and orientation conditions
  (Definition 8.3). Lemma 9.21's suspension description occurs within this setup.

Neither cited theorem supplies the missing assertion that an arbitrary embedded
self-splitting branched surface has this dynamical structure. No proof of that
assertion or counterexample to it is supplied here. Applying the restricted
classification without the reduction would be circular.

There is a second precise obstacle to using the infinite repetition directly.
[Agol–Li, Section 3](https://doi.org/10.2140/gt.2003.7.287) gives a
combinatorial radius \(R(c)\) for a splitting complex: it measures how far the
pared locus is from the remaining boundary. Their Theorem 3.5 identifies the
existence of a splitting surface with the existence of splitting complexes
whose radii tend to infinity. Theorem 3.2 associates to a splitting surface a
lamination fully carried by the original carrier. These statements use their
precise splitting-surface and splitting-complex definitions.

To invoke this mechanism for a prescribed self-return, one must construct
admissible complexes from the iterates and establish the required unbounded
radius. Counting iterations, or showing that a matrix power grows, is not that
estimate. It also would not by itself prove the stronger extension statement
about the *particular* partial lamination in the source remark. No radius
estimate or compatible extension construction was obtained.

**Gap after Approach 2.** There is no reduction from the unrestricted embedded
problem to the hypotheses of the known periodic-suspension results, and no
argument that repetition supplies the completeness needed by the splitting
surface theorem. An enumeration of more finite splitting sequences would not
remove either gap without additional geometric information or a proven bound.

## 4. Reproducible checks and stopping point

`verify_cone_controls.py` uses exact rational arithmetic to check the displayed
matrices and the normalization map on a separate three-coordinate branch cone.
It is a small consistency check, not a test for self-splitting and not a proof
of a topological classification. The fixed-point lemma is proved above.

The literature search through 30 September 2026 located the restricted results
just described, but no verified general characterization. This is a report of
the search, not a certificate that no later theorem exists. With both routes
blocked at geometric realization/completeness, the attempt stops. The full
source target remains **unsolved in this attempt**.
