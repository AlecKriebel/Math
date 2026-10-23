# Independent mathematical review: rank-two common counterexample

Review date: 21 October 2026.

## Verdict

**PASS.** The equal-differences system

\[
x_1-x_2=x_3-x_4=x_5-x_6
\]

is a rank-two, six-variable common system over every finite field. It contradicts the literal rank-only formulation of Conjecture 16 printed on page 1229 of Oberwolfach Report 22/2022. It does **not** contradict the shortest-equation-length hypothesis in Kamčev–Liebenau–Morrison Conjecture 6.1 or the corresponding Altman–Liebenau result.

This review independently inspected the provided OWR text and rendered page 1229, the KLM manuscript text (arXiv:2106.08986v3), and the Altman–Liebenau manuscript text (arXiv:2404.18908v1). The conclusion concerns those inspected versions, not any assertion about authors' intended unpublished qualifications or the current publication status of a later version.

## 1. Exact normalization and proof

Let G = F_q^n, N = |G|, f:G→[0,1], and α = E_x f(x). Define

\[
h(s)=\mathbb E_{u\in G} f(u)f(u-s).
\]

The map

\[
(s,u,v,w)\longmapsto(u,u-s,v,v-s,w,w-s)
\]

is a bijection from G^4 onto the ordered solution set. Thus there are exactly N^4 solutions, and uniform averaging over solutions gives

\[
T(f)=N^{-4}\sum_{s,u,v,w}f(u)f(u-s)f(v)f(v-s)f(w)f(w-s)
    =\mathbb E_s h(s)^3.
\]

Since (s,u)↦(u,u−s) is a bijection of G², E_s h(s)=α². Nonnegativity and Jensen's inequality imply T(f)≥α⁶. Applying the same result to 1−f,

\[
T(f)+T(1-f)\ge\alpha^6+(1-\alpha)^6\ge 2(1/2)^6=2^{-5}.
\]

This is exactly the OWR functional benchmark 2^(1−k) for k=6, for every n and every q. It is stronger than merely asymptotic commonness. The proof works in every characteristic, including characteristic two, without division by two or any field-order exception.

## 2. Rank, coordinates, columns, and shortest induced equation

Use the coefficient matrix

\[
M=\begin{pmatrix}1&-1&-1&1&0&0\\0&0&1&-1&-1&1\end{pmatrix}.
\]

Its first and fifth columns are independent, so the row rank is two over every field. The scalar solution-space dimension is four; over F_q^n it is 4n over F_q.

Every row-space vector is

\[
(a,-a,b-a,a-b,-b,b).
\]

Its support has size twice the number of nonzero members of (a,b−a,b). A nonzero pair (a,b) cannot make two of these three members zero. Consequently every nonzero row-space vector has support at least four, and a defining row attains four. The shortest induced equation has length s(M)=4. In particular no row-space vector is e_i−e_j, so no two coordinates are forced equal. This verifies irredundancy in the KLM sense, including characteristic two.

There are no zero columns. In odd characteristic the six columns (1,0), (−1,0), (−1,1), (1,−1), (0,−1), (0,1) are pairwise distinct. They do form three proportional pairs, so this is not a generic/maximal-shortest-equation-length example. In characteristic two each opposite pair coincides; this does not create a forced coordinate equality and does not affect the proof.

For characteristic p>3, replacing the rows r₁,r₂ by r₁+2r₂ and r₁+3r₂ gives

\[
\begin{pmatrix}1&-1&1&-1&-2&2\\1&-1&2&-2&-3&3\end{pmatrix}.
\]

The row transformation has determinant one, hence gives exactly the same solution set. Every matrix entry is nonzero. Therefore an implicit requirement that both displayed equations use all six variables would not rescue the unrestricted conjecture for large primes. Distinct projective column directions, by contrast, would be a substantive additional hypothesis and would exclude this example.

Here “girth four” means the minimum support of a nonzero row-space vector, equivalently the shortest induced equation. It should not be confused with the girth of the column matroid of the displayed 2×6 matrix, whose proportional pairs are dependent two-element sets.

## 3. Distinct-coordinate convention

The displayed OWR functional definition averages over all solutions and imposes no distinct-coordinate condition. The proof above directly matches it.

For completeness, a collision x_i=x_j adds an independent scalar equation because e_i−e_j is not in the row span. Exactly N³ of the N⁴ solutions have this collision. A union bound over the 15 pairs therefore bounds the proportion of solutions with a collision by 15/N. Consequently removing collision solutions changes the all-solutions-normalized monochromatic count by at most 15/N, and commonness also holds under the usual asymptotic distinct-coordinate convention as n→∞ with q fixed. For fractional f, the monochromatic weight product(f)+product(1−f) is at most one, so the same error estimate applies. Normalizing instead by the number of collision-free solutions gives the same asymptotic conclusion whenever that denominator is nonzero.

This review does not claim an exact finite-n inequality with the unchanged constant for a differently normalized, distinct-coordinate-only definition. Such an inequality is unnecessary for the printed statement and for asymptotic commonness.

## 4. Scope of the inspected statements

On rendered OWR page 1229, the paragraph defining commonness and Conjecture 16 state the rank/dimension condition, even k≥6, and sufficiently large q. That displayed statement contains no maximal-shortest-equation-length, projectively distinct-column, or distinct-coordinate restriction. Nearby introductory discussion elsewhere in the report about nonzero coefficients for single equations is not a stated extra hypothesis for this separately displayed pair-of-equations conjecture. Even imposing nonzero entries in both rows would not exclude the dense equivalent matrix above for p>3.

KLM Conjecture 6.1, in the inspected manuscript, adds s(L)=k−1 and specifies large odd q. Altman–Liebenau Conjecture 1.1 reproduces the shortest-equation condition, and Theorem 1.2 proves an appropriate result for sufficiently large primes and containing systems. Here k−1=5 whereas s(M)=4. Accordingly the later result addresses a genuine restricted conjecture, not the literal broader OWR formulation. The evidence does not establish why the wording differs; describe it as a scope mismatch, not a claim of intentional omission or author error beyond the mathematical printed statement.

## 5. Prime-field and extension-field transfer

For a fixed coefficient matrix with entries in F_p, commonness over F_p and over F_(p^r) are equivalent, when each means the functional property for every ambient dimension. This statement keeps p and the prime-field matrix fixed; it is not a general transfer for coefficients outside F_p.

Choose an F_p basis of F_(p^r). Then a solution over (F_(p^r))^n is precisely an F_p solution in ambient dimension rn, with a bijection preserving uniform averages. Thus commonness over F_p implies commonness over the extension.

Conversely, if a function f₀ on F_p^m witnesses uncommonness, choose n with rn≥m and pull f₀ back through a surjective F_p-linear projection F_p^(rn)→F_p^m. Uniform solutions project uniformly onto the smaller solution set, with fibers of equal size: in a basis adapted to the projection, all extra scalar-coordinate solution blocks are freely chosen. Therefore both product averages, and the strict violation, are preserved. This yields an uncommonness witness over the extension. Padding dimensions is essential here; identifying extension dimensions only with multiples of r would otherwise leave a gap.

For the present integer-coefficient counterexample, the direct proof already establishes commonness over every field, so this transfer is auxiliary rather than needed for the counterexample.

## 6. Auxiliary equal-sums certificate

The originally proposed equal-sums system x₁+x₂=x₃+x₄=x₅+x₆ is independently valid as well. Replace h(s) by E_u f(u)f(s−u) and the parametrization by (u,s−u,v,s−v,w,s−w). Rank, normalization, Jensen's inequality, and shortest induced equation length four follow exactly. Its repeated columns in odd characteristic make the equal-differences version a cleaner main certificate against incidental column-distinctness concerns; neither certificate satisfies projective column distinctness or s=5.

## Acceptance boundaries

- Accepted: exact all-solutions functional commonness, every characteristic, rank two, six variables, irredundancy, no zero columns, shortest induced equation length four.
- Accepted with stated qualification: pairwise distinct columns in odd characteristic; dense equivalent coefficient matrix for p>3; asymptotic collision-free commonness; prime-field coefficient transfer to extensions.
- Rejected as an inference: that rank alone implies s=k−1, that the later generic theorem covers this example, or that this refutes the restricted KLM/Altman–Liebenau statement.

## 7. Final artifact review

Independently reviewed REPORT.md, SOURCE_CITATIONS.md, PROOF_CHECKS.py, and PROOF_CHECKS.json after completion. **PASS: no mathematical correction to the report is required.** The analytic argument remains the universal certificate; finite checks are correctly described as supplemental.

### Attribution and theorem scope

Independently opened [Kamčev–Liebenau–Morrison, Towards a characterisation of Sidorenko systems, arXiv:2107.14413v3](https://arxiv.org/html/2107.14413v3), specifically the graph-template definition immediately before Theorem 1.3 and Theorem 1.3 itself. The blocks (x₁,x₂), (x₃,x₄), (x₅,x₆), with block form ℓ(u,v)=u−v, give defining forms ℓ(block 1)−ℓ(block 2) and ℓ(block 2)−ℓ(block 3). The template is the three-vertex path, hence a tree. The attribution is therefore directly applicable, not merely an analogy. The report appropriately disclaims novelty; the elementary Jensen argument is an independent certificate of an instance of established Sidorenko theory.

Independently opened [Dong–Li–Zhao, Uncommon linear systems of two equations, arXiv:2404.17005v2](https://arxiv.org/html/2404.17005v2), checking Definitions 1.1–1.3, Definition 1.7, and Theorems 1.8–1.9. The report correctly preserves integer coefficients, irredundancy including nonzero columns, maximal shortest-equation length, and a threshold depending on the fixed matrix. Its distinction between large characteristic and large cardinality is necessary and correct. The claim of an omitted genericity condition is explicitly presented as a reasonable interpretation, not as established speaker intent. No priority, unpublished-intent, or unrestricted extension-coefficient theorem is claimed.

The extension-field transfer in the report is valid with its prime-subfield coefficient restriction. The counterexample itself works over all finite abelian groups, as the report states: its parametrization and Jensen argument require only addition, subtraction, and uniform finite averaging.

### Reproducibility and test limitations

Reran PROOF_CHECKS.py independently and compared its output against PROOF_CHECKS.json with a byte-for-byte comparison; they agree. All seven listed group cases pass, totaling 1,316 function test instances. The script uses explicit exception checks rather than Python assertions, so the checks are not disabled by optimized interpreter mode.

Counting precision: the 1,316 instances include 60 duplicate indicator cases, because the half-grid enumeration contains its indicator-function endpoints. Thus there are 1,256 distinct (group, function) cases. This is not an error in the JSON's computation or the report, which does not claim 1,316 distinct functions. Any short summary should say “1,316 exact test instances,” not “1,316 distinct functions.”

Direct six-factor parametrized-density summation is checked for three functions per group, totaling 21 instances; the remaining function instances test the correlation mean and Jensen/commonness inequalities. These direct checks use the first three indicator functions in enumeration, hence only sparse functions, and do not exhaustively compare the raw constrained six-variable sum for all functions. The independent injectivity, equation, rank, and collision checks are correct. None of these finite checks alone establishes the universal result, and the report explicitly avoids that inference.

This review did not re-audit the full proofs of the cited literature, verify journal metadata, or perform publication, queue editing, or any external mutation.
