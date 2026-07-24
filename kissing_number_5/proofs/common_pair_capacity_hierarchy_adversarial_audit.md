# Adversarial audit of the common-pair capacity hierarchy

## Verdict

The projection theorem in `common_pair_capacity_hierarchy.md` is correct,
including all closed endpoints.  However, the new five-node
pseudodistribution is **not** a barrier to the universal common-pair
capacity mechanism.  It passes only the cumulative threshold rows
implemented by the verifier.  Summing the same pointwise theorem over a
single base color gives two exact contradictions.

Thus the certificate's claim that the candidate satisfies every
common-pair capacity cut is false.  This objection does not alter the
projection theorem itself.

## Independent theorem audit

For a base pair with inner product \(q>-1\), the inverse base Gram matrix is
\[
 \frac1{1-q^2}\begin{pmatrix}1&-q\\-q&1\end{pmatrix}.
\]
All its entries are nonnegative when \(q\leq0\), so the coordinatewise
lower bounds \(c_x,c_w\geq(b,b)\) imply
\[
 \langle Px,Pw\rangle\geq\frac{2b^2}{1+q}.
\]
If \(p=2b^2/(1+a)>1/2\), nonzero residuals have
\[
 \frac{\langle x,w\rangle-\langle Px,Pw\rangle}
 {\|\xi_x\|\|\xi_w\|}
 \leq\frac{1/2-p}{1-p}.
\]
The inequality direction is valid: writing \(n\leq c<0\) and
\(0<d\leq1-p\), one has
\[
 n/d\leq c/d\leq c/(1-p).
\]

At \(p=3/4,2/3,5/8,1/2\), the residual bounds are respectively
\(-1,-1/2,-1/3,0\), with sharp models given by an antipodal pair, an
equilateral triangle, a regular tetrahedron, and the six-vector
orthoplex in \(\mathbb R^3\).  The strict/non-strict endpoint conventions
in the table are therefore correct.  The \(q=-1\) case follows directly
from \(y+z=0\).  The zero-residual subcase at \(p=1/2\) is also handled
correctly: equality would force both correlation vectors to equal
\((b,b)\), giving projected squared norm \(1/2\), contrary to a
unit vector with zero residual.

The Rankin argument uses a nonzero dependence among five augmented vectors
\((v_i,1)\in\mathbb R^4\); its coefficients have both signs, and taking
the inner product of the two positive combinations gives the required
strict contradiction.  The orthoplex trace proof retains determinant-zero
and inner-product-zero boundary cases.

## The omitted stratified inequality

The theorem is pointwise in the base pair.  Therefore it may be summed over
**any** selected collection of base pairs, not only a cumulative set
\(\{q\leq a\}\).  In the normalized pair/triple notation, for any
measurable \(B\subseteq[-1,0]\),
\[
 \int {\bf1}_{\{t\in B,\ u\geq b,\ v\geq b\}}\,d\nu
 \leq
 \int_B M\!\left(\frac{2b^2}{1+t}\right)\,d\alpha(t),
 \tag{1}
\]
where the integrand on the right is zero at \(t=-1\).  Equation (1) is
obtained simply by applying the proved capacity to each ordered base pair
before summing.

On a finite support, take \(B=\{s_i\}\).  If \(E_i\) is the number of
unordered edges of color \(i\), this yields
\[
 \sum_T c_{i,b}(T)n_T
 \leq M\!\left(\frac{2b^2}{1+s_i}\right)E_i.
 \tag{2}
\]
This is not derivable by subtracting two cumulative inequalities, because
their capacity constants can differ.

## Exact counterexample to the barrier claim

The candidate has
\[
 (E_0,E_1,E_2,E_3,E_4)=(85,3,131,326,275)
\]
and \(b=499/1000\).

For the singleton base color \(s_2=-11/25\),
\[
 p=\frac{249001}{280000}>\frac34,\qquad M(p)=1.
\]
The only occupied triangle with a color-2 base and two color-4 incident
edges has count
\[
 n_{244}=219.
\]
Equation (2) therefore requires
\[
 219=n_{244}\leq E_2=131,
\]
an exact violation by \(88\).

There is a second independent violation at \(s_3=-9/100\):
\[
 p=\frac{249001}{455000}>\frac12,\qquad M(p)=4,
\]
but
\[
 n_{344}=1424>4E_3=1304
\]
by \(120\).

The cumulative row at \(a=-11/25\) passes only because its right side is
\(E_0+E_1+E_2=219\), even though the 88 deeper edges of colors 0 and 1
have zero qualifying incidences and cannot donate capacity to a color-2
edge.  Likewise, the all-negative cumulative row lets stronger deep-edge
capacities subsidize color 3.

The seven-node all-harmonic witness also fails the corrected hierarchy.
For its exact base stratum \(t=-1/4\) and \(b=1/2\), one has
\[
 p=\frac23,\qquad M(p)=3.
\]
Independent summation of its rational orbit masses gives
\[
 L=\frac{722942322240113}{100000000000000},\qquad
 R=\frac{721699531533087}{100000000000000},
\]
and hence
\[
 R-L=-\frac{621395353513}{50000000000000}<0.
\]
The endpoint \(p=2/3\) uses capacity three, so this failure is not caused
by replacing a non-strict endpoint with a strict one.

## Independent machine reconstruction

`tests/test_common_pair_capacity_hierarchy_independent_audit.py` imports
neither the source verifier nor its helper functions.  It reconstructs:

- all pair and triple masses and every occupied \(3\times3\) Gram
  determinant;
- the factor of two between unordered base-edge incidences and fixed-slot
  ordered triples, including repeated edge colors;
- all implemented cumulative hierarchy rows;
- all four earlier source-witness failures and all seven exact
  all-harmonic cumulative rows, followed by all seven exact-stratum rows;
- the C047 normalized/spectral scaling and both centered-skew residuals;
- the endpoint equality patterns; and
- the two singleton-color contradictions above.
