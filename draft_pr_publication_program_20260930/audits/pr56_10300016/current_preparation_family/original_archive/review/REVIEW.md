# Independent review: self-splitting branched surfaces

**Verdict: PASS as an unresolved obstruction and source-scope package.**
The displayed algebraic lemma and controls are correct, the cited topological
results are accurately restricted, and the remaining geometric gaps are
identified explicitly. The full classification in Calegari's Question 7.1
remains **unsolved in this attempt**. No new classification, geometric
counterexample, or novelty claim is justified or made. No mandatory correction
is required.

Frozen OBSTRUCTION.md SHA-256:
**89b5ba65244c77309845060a4935caa41088f24ea8fce599c7635a300bcce920**.
Frozen author verifier SHA-256:
**f909d1dca555eaff4a5f2500366600029e274fab81f943f24d558b30d370bf3e**.
Review date: 2026-09-30. Separate adversarial AI reviewer: gpt-6-astra,
xhigh reasoning. This is not human peer review.

## Exact question and prior observations

I read [Calegari's primary problem list](https://arxiv.org/abs/math/0209081v1),
including Definition 1.9, Question 7.1, and both remarks on printed p. 13,
and visually checked that page. Question 7.1 asks which embedded branched
surfaces admit a nontrivial splitting to a homeomorphic copy. The triangulation
appears only in the subsequent discussion of iteration. It is not a hypothesis
restricting the classification question to branched surfaces arising from
triangulations or to a particular foliation class.

The source does not replace the return homeomorphism with ambient isotopy.
Nor does it give a separate formal definition of nontriviality there. The
package correctly avoids introducing such a stronger requirement. Identifying
weight spaces after a return requires compatibility with the branch structure;
a bare assertion about a cell complex does not supply that map.

The original remarks already contain the conditional invariant-measure
observation, pseudo-Anosov examples, and the warning about bounded splitting
injectivity radius and a merely partial lamination. The package credits
these observations. Its finite-sector algebraic route is explicitly narrower
than the unrestricted target, rather than silently assuming that every target
already carries a nonzero transverse measure.

## The cone lemma and its limitations

For a specified finite cone
\(C=\{w\ge0:Rw=0\}\), the hypotheses
\(A(C)\subset C\) and \(Aw\ne0\) for \(w\in C\setminus\{0\}\) suffice.
The slice \(K=C\cap\{\sum w_i=1\}\) is a nonempty compact convex set.
Its normalization denominator is continuous and strictly positive, so the
normalized map is continuous from \(K\) to itself. The finite-dimensional
fixed-point theorem applies in its affine span, including a singleton.
The resulting eigenvalue \(\sum (Aw)_i\) is strictly positive.

This proves an invariant ray for a map already supplied. It constructs
neither a legal splitting nor an embedded return map.

The two matrices in the text give the claimed limitations:

- For \(A=\left(\begin{smallmatrix}2&1\\0&1\end{smallmatrix}\right)\),
  a putative eigenvector with \(y>0\) forces eigenvalue 1 and then
  \(x+y=0\). Thus its nonnegative eigenray is confined to the boundary.
  Equivalently,
  \(\det((x,y),A(x,y))=-y(x+y)\).
- For \(U=\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)\),
  the only eigenvalue is 1 even though \(U\ne I\).
  Its powers are \(\left(\begin{smallmatrix}1&k\\0&1\end{smallmatrix}\right)\).
  Matrix nonidentity is not a definition of nontrivial geometric splitting.

The identity-map observation is also correct. These examples are explicitly
algebraic; the package does not assert their realization by embedded branched
surfaces or use them as counterexamples to a topological converse.

The exact missing converse is therefore accurately stated: branch equations
and an eigenray do not supply legal sheet order, admissible local splitting
moves, the ambient complementary data, or a compatible returned carrier.
The absence of a construction here is an unresolved gap, not a proof that
every such reconstruction is impossible.

## Restricted periodic-splitting theorems

[Agol, Theorem 3.5](https://arxiv.org/abs/1008.1606v2), pp. 6–7, begins with
a pseudo-Anosov map and a measured train track suited to its stable lamination.
It gives eventual periodicity modulo that supplied map and rescaling by its
dilatation. The package preserves these hypotheses and does not reverse the
theorem into a classification of all self-splitting branched surfaces.

I checked the relevant statements and surrounding definitions in the full
published [Landry–Tsang paper](https://msp.org/gt/2025/29-9/gt-v29-n9-p02-p.pdf),
*Geometry & Topology* 29 (2025), 4531–4663:

- Theorem 7.10 assumes an atoroidal sutured manifold equipped with a depth-one
  foliation and constructs a veering carrier for the associated unstable
  Handel–Miller lamination
- Theorem 9.22 concerns a veering carrier compatibly carrying that prescribed
  lamination; its positive boundary train track determines it up to isotopy
- Definition 8.3 requires full carrying and both boundary/dynamic orientation
  compatibilities
- Lemma 9.21 derives its suspension description inside that same setup

Thus the restricted uniqueness statement cannot stand in for the original
classification without an additional reduction. No such reduction is given
in the package, and it correctly records this as a gap. The paper's discussion
of failure of full-support invariant measures likewise does not convert the
package's elementary matrix examples into geometric realizations.

This is a check of the cited source hypotheses and coverage, not an assertion
that every proof in the 133-page Landry–Tsang article was independently
reverified.

## The splitting-radius criterion

I checked Definitions 3.1 and 3.3, Lemma 3.4, and Theorems 3.2 and 3.5 in
[Agol–Li, pp. 293–295](https://www.maths.tcd.ie/EMIS/journals/UW/gt/ftp/main/2003/2003-8.pdf).
Their splitting complexes are embedded in the fibered neighborhood, transverse
to its interval fibers, locally contained in transverse surfaces, and satisfy
the required boundary condition along the pared locus. Their splitting surface
is complete and has the stated discrete fiber intersections and neighborhood
properties.

The radius is specifically

\[
R(c)=\max\{k:B_k(p(B),c)\cap\partial c=p(B)\}.
\]

It measures separation from the remaining boundary in the induced cell
structure. Theorem 3.5 gives the stated equivalence between a sequence of
admissible complexes with radii tending to infinity and a splitting surface.
The finite-cell compactness argument retains vertical sheet order and the
allowed gluing data. Theorem 3.2 then produces a fully carried lamination
in the sense of that paper.

The candidate does not confuse this radius with the number of iterations or
growth of a transition matrix. Applying the theorem to a particular return
would still require construction of the admissible complexes and the unbounded
radius estimate in the theorem's finite-cell framework. Neither is established
by the reported attempt.

Even obtaining some fully carried lamination by this criterion would not
automatically show that the specific partial lamination mentioned by Calegari
extends to it. The package correctly keeps that stronger extension problem
separate. Bounded-complex enumeration supplies no unstated finite bound for
self-return witnesses.

## Reproduction and independent controls

The author's **191 exact assertions** replayed with **byte-identical JSON**.
All four source PDF hashes and byte counts match the manifest.

Run the separate checker from this review directory:

    python3 independent_checks.py

It passes **1,141 exact standard-library assertions**, including closed formulas
for both matrix powers through exponent 30, determinant tests for their
eigenrays, cone preservation on the extreme rays of \(x+y=z\), the normalized
interval map \(t\mapsto1/(1+t)\), and an exact eigenvector over
\(\mathbb Q(\sqrt5)\). A nilpotent nonnegative matrix checks that the
nonannihilation hypothesis cannot simply be dropped.

These are algebraic controls only. They do not test a splitting realization,
prove radius growth, or classify any embedded branched surface.

## Disposition

The package is ready as a reviewed, explicitly unresolved attempt. It gives
a correct credited necessary-data calculation and identifies the exact missing
geometric realization and completeness steps in two routes. The current-source
search found no verified general characterization, but that negative search
is not proof of absence throughout the literature. Retain the status
**unsolved**, both route gaps, and the no-novelty qualification.
