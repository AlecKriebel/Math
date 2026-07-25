# The six-support weighted branch

If a positive weighted spherical two-design in \(S^4\) has exactly six
support points, the sharp weight bound forces all weights to equal \(1/6\);
the support is a regular simplex
\[
\langle v_i,v_j\rangle=-\frac15\qquad(i\ne j).
\]

Let \(y\in S^4\) be any further code point and put
\[
a_i=\langle y,v_i\rangle.
\]
The simplex tight-frame identities and the kissing constraint give
\[
\sum_{i=1}^6a_i=0,\qquad
\sum_{i=1}^6a_i^2=\frac65,\qquad
a_i\leq\frac12.
\tag{1}
\]

## Exact negative-coordinate lemma

Every vector satisfying (1) obeys
\[
\boxed{
\min_i a_i\leq-\rho,\qquad
\rho=\frac{5+\sqrt{15}}{20}=0.443649\ldots .
}
\tag{2}
\]

To prove this, maximize \(\sum a_i^2\) over the polytope
\[
\sum a_i=0,\qquad -\rho\leq a_i\leq\frac12.
\]
A convex function attains its maximum at a vertex, where at most one
coordinate is not at an endpoint.  If \(k\) of the five fixed coordinates
are \(1/2\), the free coordinate is
\[
c_k=(5-k)\rho-\frac{k}{2}.
\]
Since \(1/4<\rho<1/2\), the cases \(k=0,1\) have \(c_k>1/2\), the case
\(k=2\) has \(-\rho<c_k<1/2\), and the cases \(k\geq3\) have
\(c_k<-\rho\).  Thus feasibility leaves only the endpoint pattern
\[
\left(\frac12,\frac12,3\rho-1,-\rho,-\rho,-\rho\right)
\]
up to permutation.  Its squared norm is
\[
\frac12+(3\rho-1)^2+3\rho^2
=12\rho^2-6\rho+\frac32=\frac65,
\]
because
\[
12\rho^2-6\rho+\frac3{10}=0.
\]
Strict convexity shows that every nonvertex has smaller squared norm than
the vertex maximum unless it is itself one of these vertices.  Thus (1)
forces at least one coordinate at or below \(-\rho\).  Equality
\(\min_i a_i=-\rho\) can occur only in the displayed pattern, up to
permutation.

Consequently, every extra code point lies in one of the six caps
\[
\langle -v_i,y\rangle\geq\rho.
\tag{3}
\]
This is an exact six-cap cover of the extension space.

## Why this is not yet an extension bound

The exact \(-1/50\) cap theorem applies to each cap in (3), but its bound 39
is far too weak to sum over six overlapping caps.  A completion of the
six-support stratum needs one of:

- a sharp occupancy theorem for height \(\rho\);
- compatibility bounds between different simplex chambers;
- an \(S_6\)-symmetry-reduced multi-cap SDP.

The retained file `simplex_chamber_cap_scan.json` records an attempted
floating-point scan that failed at the solver stage.  It supplies no
mathematical evidence and is not used by the proof.
