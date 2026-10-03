> **Current priority reconciliation: already_solved, 1/5, no paper.** The valid mathematical PASS below is historical and remains scoped to the original reviewed proof. It does not establish novelty. The new independent mathematical families found no mandatory mathematical error; the priority audit establishes that a stronger prior Esterov theorem already supplies the requested equality by our explicit checked specialization. [Current qualifications](../GLOBAL_QUALIFICATIONS.md), [priority record](../PRIORITY_RECORD.md) and [specialization](../PRIOR_ART_SPECIALIZATION.md) supersede the old priority-pending disposition. This prefatory reconciliation is SOURCE synthesis by a reused preparer, not a third fresh mathematical review.

# Independent adversarial review: the Hurwitz/discriminant polytope comparison

**Verdict: PASS for the complete combinatorial comparison in the intended smooth, complete-embedding source regime.** The proof establishes both inclusions in
\(\pi\mathcal D(Q\times\Delta_{n-1})=\mathcal H(Q)\) for every dimension
and polarization covered by the cited Sano theorem. It contains a genuine
argument for the reverse inclusion, not merely the already-known geometric
equality. No mandatory mathematical correction is required.

The source regime and the use of established GKZ foundations must remain
visible in publication. This verdict does not certify a statement for arbitrary
singular or sparse configurations, a proof that reconstructs GKZ without
algebraic inputs, or historical novelty.

**Frozen artifact:** CANDIDATE.md, SHA-256
**4931eccbb464b53af07b90e24b72060e681b9a7f1769c0030a9d7090e59b129c**.
Review date: 2026-09-30. Independent reviewer: gpt-6-astra, xhigh reasoning.
This is separate adversarial AI review, not human peer review.

## 1. Source scope and the requested kind of proof

The complete Sano contribution in
[Oberwolfach Report 19/2025, pp. 919–921](https://ems.press/content/serial-article-files/51856)
was read, including the displayed theorems and the question. Its subject is
the comparison of the discriminant and Hurwitz weight polytopes within the
GKZ framework. It expressly contrasts its analytic derivation of the
Hurwitz-vector description with the discriminant description available
through GKZ. Merely repeating the Cayley identification would not address
the requested comparison.

The report initially writes a general lattice configuration and abbreviates
the later characteristic-vector theorem. Its reference [6],
[Sano, *Weight polytopes and energy functionals of toric varieties*](https://arxiv.org/abs/2302.09801v1),
makes the hypotheses explicit:

- \(X\) is a smooth irreducible polarized toric variety
- the embedding is given by the complete very ample linear system and is
  linearly normal
- the degree is at least two
- \(A\) consists of every lattice point of the Delzant momentum polytope
- only massive boundary simplices contribute to \(\eta_{T,n-1}\)

These statements occur in the introduction, Definition 1.3, and Theorem 1.4.
They match the candidate exactly. The complete-lattice and smoothness
conditions have not been silently replaced by unimodularity of every
triangulation.

**Scope judgment.** Restoring these hypotheses is justified when interpreting
the OWR question as the comparison of its cited characteristic-vector
theorem with the GKZ discriminant model. The candidate fully handles that
intended comparison; it is not merely a surface or special-polytope case.
The report's unqualified introductory configuration language should not be
used to advertise a stronger arbitrary-configuration theorem. That stronger
literal reading is outside this verdict. The candidate already states
this boundary prominently.

**Proof-type judgment.** Comparing the two explicit combinatorial models
using established GKZ vertex and fan theorems is a legitimate combinatorial
answer in the framework explicitly invoked by the source. The candidate's
comparison itself does not use Sano's K-energy argument, the desired equality,
or a Cayley identity. Sano's theorem supplies the established interpretation
of the right-hand model. This is not a claim that the entire algebraic
identification of the Hurwitz form has been rebuilt from elementary
combinatorics.

[Ogusu–Sano](https://arxiv.org/abs/2302.09792v1), Proposition 3.5, already
proves the corresponding vertical-prism vector identity in dimension two
and uses it for one inclusion. The candidate properly credits this. It
does not claim the stronger triangulation/vertex bijection appearing in
that paper's Conjecture 4.5, nor does it assume that all projections of
discriminant vertices are vertices.

## 2. Weight space, lattice normalization, and GKZ input

The projection \(\pi\) is essential. The discriminant's full coefficient
torus has one coordinate per point of
\(B=A\times\operatorname{Vert}(\Delta_{n-1})\), whereas the source Hurwitz
weight space uses the ambient diagonal torus with one coordinate per point
of \(A\). Its action on the second Segre factor is trivial. Restriction of
characters therefore sums the \(n\) coordinates above each \(a\), exactly
as in (1). This agrees with Ogusu–Sano Section 2.3. It is neither the smaller
intrinsic toric action nor an unmentioned quotient by scalar weights.

This projection is restriction of torus characters on the polynomial
representation. It is not evaluation that identifies coefficient variables;
there is consequently no possible cancellation of distinct monomials from
such an evaluation.

All lattice normalizations are consistent. At a vertex of a Delzant face
\(F\), its primitive edge directions form a basis of its induced face
lattice. Because \(A=Q\cap\mathbb Z^n\), the adjacent primitive lattice
points are included. Thus \(A\cap F\) generates the full affine face lattice.
The standard simplex has unimodular faces, and a product face has the product
lattice. No lattice-index correction is omitted.

I checked the full statements and proofs on printed pp. 361–363 of
[GKZ, *Discriminants, Resultants and Multidimensional Determinants*](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/gelkapzel.pdf),
Chapter 11, against the scan. Theorems 3.2 and 3.4 apply under the stated
simplicity and face-index conditions, which hold here. The text explicitly
identifies the regular determinant with the ordinary discriminant in the
smooth case. The Segre product is smooth, and its configuration is exactly
\(B\); the standard simplex has no other lattice points.

The normal-fan assertion is not inferred from a mere list of vertices.
Chapter 11, Theorem 3.4(a) proves that the regular determinant's Newton
polytope is a Minkowski summand of the principal determinant's Newton
polytope, and hence that its normal fan is coarser than the secondary fan.
Chapter 10, Theorem 1.4 supplies the principal-determinant monomial label;
the alternating face-determinant formula in the proof of Chapter 11,
Theorem 3.2 gives the label \(m_U\) for that same height cone.

GKZ Chapter 7 uses an upper, concave envelope with maxima. Replacing the
height by its negative gives the lower convex envelope and minima used in
the candidate. The sign is correct. An independent explicit control is the
quadratic discriminant \(b^2-4ac\): lower heights \((0,1,0)\) select its
\(ac\) exponent \((1,0,1)\); lower heights \((0,-1,0)\) select
\((0,2,0)\). Both are minimizers for the stated heights.

These are general pre-existing discriminant results. None requires the
Hurwitz formula or the equality being proved.

## 3. The product-face calculation

Every \(k\)-face of \(P=Q\times\Delta_{n-1}\) is a unique product \(F\times E\)
with dimensions \(j,l\) and \(j+l=k\). A massive \(k\)-simplex belongs to
a unique such \(k\)-face. It cannot be counted in two different faces of
that same dimension.

For a \(j\)-simplex \(\sigma\subset F\), normalized volume gives

\[
\operatorname{Vol}_{\mathbb Z}(\sigma\times E)
=\frac{(j+l)!}{j!\,l!}\operatorname{Vol}_{\mathbb Z}(\sigma).
\]

For a vertex \(a\) of \(\sigma\), its barycentric coordinate has average
\(1/(j+1)\) on the product. On a \(k\)-simplex \(\tau\) in any vertex
triangulation of \(\sigma\times E\), the average equals the number of
vertices projecting to \(a\), divided by \(k+1\).
Additivity of volume-weighted centroids therefore gives

\[
\sum_\tau \operatorname{Vol}_{\mathbb Z}(\tau)
        \#\{\text{vertices of }\tau\text{ above }a\}
=\binom{k+1}{j+1}\operatorname{Vol}_{\mathbb Z}(\sigma).
\]

The coefficient is integral and correct; no extra factorial survives.
This argument permits nonunimodular simplices and arbitrary refinements,
including those not supplied as staircase triangulations.

The vertex restriction is necessary and is present in the proof:
a vertex of a refined product cell must project to a vertex of the relevant
simplex of \(T\). An unused lattice point interior to that simplex cannot
be introduced while applying this identity. Section 5 guarantees that
restriction for the refinements it actually uses.

Restricting to \(F\times E\) and summing over the top simplices of \(T|_F\)
does not double-count lower-dimensional common boundaries: those have
zero \(k\)-volume. There are \(\binom n{l+1}\) simplex faces \(E\).
This proves (6), including \(j=0\), \(l=0\), unused coordinates, and the
top-dimensional case.

## 4. Cancellation and the vector identity

With \(r=l+1\), the sign in (9) becomes
\((-1)^{n-j}(-1)^{n-r}\). The added \(r=0\) term is zero because
\(\binom j{j+1}=0\). The remaining sum is the \(n\)-th finite difference
of the degree-\(j+1\) polynomial
\(r\mapsto\binom{j+r}{j+1}\), at zero.

It vanishes for \(j\le n-2\). For \(j=n-1\) the finite difference is 1,
with negative sign. For \(j=n\) it equals
\(\binom n1=n\), with positive sign. Thus

\[
\pi m_U=n\eta_{T,n}-\eta_{T,n-1}
\]

is proved for every permitted product refinement. In dimension one,
\(P=Q\), and the formula becomes the expected
\(\eta_{T,1}-\eta_{T,0}\); there is no missing lower range in the sum.

## 5. Regular refinements and the reverse inclusion

The equal-column lower envelope is indeed independent of the second
coordinate. Any representation of \((x,y)\) projects to a representation
of \(x\), giving the lower bound \(g_w(x)\). A minimizing representation
of \(x\), multiplied by simplex barycentric coordinates for \(y\), realizes
that bound. The maximal old cells are therefore
\(\sigma\times\Delta_{n-1}\) with \(\sigma\in T\).

A fixed sufficiently generic perturbation gives a regular triangulation
refining those cells for all sufficiently small positive perturbation
parameters. There are only finitely many circuit inequalities; the ones
nonzero at the original height retain their signs, and generic perturbation
breaks the remaining ties. Points strictly above the old lower hull retain
a positive gap. Since the base height is generic, those are precisely the
points unused by \(T\), so the necessary vertex restriction holds.

The same triangulation \(U\) can be fixed as the perturbation tends to zero.
GKZ height compatibility then implies that \(m_U\) minimizes at the
unperturbed equal-column height as well. Projecting and using the vector
identity proves equation (15) with the correct minimum direction.

This establishes the required support value for every generic test
functional on \(\mathbb R^A\). It does not assume an arbitrary triangulation
of \(P\) has a vertex projection. For every regular \(T\), a regular
refinement yields its Hurwitz vector in \(\pi\mathcal D(P)\), proving one
inclusion. For a generic functional, the minimum on that larger polytope is
attained at one of these vectors in \(\mathcal H(Q)\), proving equality of
the minima. Density of generic heights, continuity of finite-polytope
support functions, and convex separation give equality for all functionals
and hence the other inclusion.

Neither an analytic inequality nor the known Cayley equality enters this
step. The support argument closes the specific gap left by the earlier
surface inclusion.

## 6. Independent exact verification

The author's checker reproduced **1,227 assertions** and its saved JSON
output **byte-for-byte**. The hashes and byte counts of all five cited
source PDFs match the provenance manifest.

Run the independent checker from this review directory:

    python3 independent_checks.py

It passes **8,093 exact assertions**, using Python's standard library.
Its triangulations are computed from rational lower supporting hyperplanes,
rather than supplied by the author's staircase construction:

- 80 generic-height product triangulations across the square, double
  triangle, and \(2\times1\) rectangle
- 32 equal-column refinements, checking every massive-vector level,
  unused vertices, the projected vector, and the exposed support value
- 112 tests of the GKZ minimizer label against every other sampled massive
  vector in the same configuration
- ten distinct regular refinements of the five-dimensional product
  \(2\Delta_3\times\Delta_2\), embedded in its complete 30-point configuration;
  its six unused base lattice points remain unused, and each of the four
  nonzero projected coordinates equals 12
- the finite-difference identity through dimension 30 and explicit
  discriminant checks for the minimum/maximum convention
- negative controls detecting the wrong sign convention and incorrectly
  including interior edges in the massive boundary sum

Four sampled triangulations of the cube project to nonvertices of the
projected segment. This independently confirms that the proof must not
rely on an all-projections-are-vertices assertion. Exact saturated face
volumes are computed from integer minors, including nonunimodular cells.

These are bounded diagnostics. They do not enumerate every regular
triangulation and do not replace the general argument or the GKZ theorem.

## 7. Attribution and final disposition

The geometric equality, Sano's analytic characteristic-vector theorem,
the general GKZ descriptions, and the Ogusu–Sano surface inclusion are
prior results. The bounded literature check, including
[Borovik–Briand's 2026 paper](https://arxiv.org/abs/2607.17966v1) on
degenerating discriminants, does not establish priority for this specific
comparison. That paper's higher-associated-hypersurface treatment uses
geometric degeneration and Cayley methods; no full independent proof audit
of it is asserted here.

**The frozen candidate is mathematically complete for its explicitly stated
smooth complete-embedding hypotheses and gives the requested comparison by
a combinatorial argument within GKZ.** Its existing scope and novelty
qualifications should be retained in the draft PR and any status description.
No mandatory proof revision remains.
