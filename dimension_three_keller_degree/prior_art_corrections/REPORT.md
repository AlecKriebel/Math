# Prior-art correction audit: Rung 1 and the plane exits

**Audit frozen:** 2026-07-25T19:37:25Z  
**Scope:** source attribution and theorem applicability only.  
**Status:** source-specific audit; not peer reviewed and not a guarantee of
worldwide priority.

## Executive corrections

1. Vistoli's published theorem is stated over a fixed **algebraically closed
   field of characteristic zero**.  It says that an étale polynomial
   self-map of \(\mathbb A^3\) of total polynomial degree \(3\) is an
   isomorphism.  Together with the separately known degree-\(\leq2\) case,
   this gives the total-degree-\(\leq3\) floor.  The statement descends to
   every characteristic-zero base field by faithful flatness, but that
   descent is an inference, not Vistoli's stated base-field hypothesis.

2. Vistoli attributes the earlier full dimension-three, degree-three result
   jointly to T. T. Moh and A. Sathaye as an **unpublished computer
   calculation** whose printout was about 100 pages.  This is not the
   published Moh plane-degree paper and is not Vistoli's reference [9].

3. The unconditional plane input actually stated and used by Vistoli is:
   an étale polynomial map
   \(\mathbb A^2\to\mathbb A^2\) of
   \(\max\{\deg P,\deg Q\}\leq12\) is an isomorphism, over the ambient
   algebraically closed characteristic-zero field.  Vistoli says Moh's
   cited paper proves the stronger ceiling \(\leq100\), but Vistoli uses
   only \(\leq12\).  It should not be called a theorem for an unspecified
   “bounded degree.”

4. Trushin's arXiv:2605.26390v1 predates the Rung 1 note and contains both
   the square-root construction and the singular-locus/branch-divisor
   mechanism.  Rung 1 Section 3 is a short self-contained specialization,
   not a prior-art-independent argument.

5. Gallagher's archived preprint proves a uniform weighted-lift theorem for
   **every** generic fiber degree \(n\geq3\).  The degree-\(3\)-through-\(100\)
   computations are explicitly regression/collision certificates, not the
   basis of the all-\(n\) result.

## 1. Vistoli, Moh--Sathaye, and the total-degree floor

### What Vistoli actually states

Vistoli begins on journal p. 79:

- the ground field \(\kappa\) is fixed, algebraically closed, and of
  characteristic zero;
- “degree” means the maximum of the coordinate degrees;
- degree \(2\) is already known; and
- the object under study is an étale polynomial map.

The main theorem is the unnumbered theorem on p. 80:
\[
F:\mathbb A^3_\kappa\longrightarrow\mathbb A^3_\kappa,\qquad
\deg F=3,\qquad F\ \text{étale}
\quad\Longrightarrow\quad
F\ \text{is an isomorphism}.
\]
For polynomial self-maps in characteristic zero, the Keller condition with
nonzero constant determinant is exactly the displayed étaleness condition.
Thus Vistoli plus the degree-\(\leq2\) result excludes total degrees
\(1,2,3\) in dimension three.

This is not merely a complex-topological theorem.  In Lemma 12 on p. 85,
Vistoli says that one may use topology after taking \(\kappa=\mathbb C\), or
étale cohomology over the general algebraically closed field; he chooses the
first presentation only for notation.

### Extension to a nonclosed characteristic-zero field

Let \(K\) be any characteristic-zero field and let \(F\) be a Keller map over
\(K\) of total degree at most three.  Base change to an algebraic closure
\(\overline K\).  Vistoli's theorem (and the degree-\(\leq2\) theorem) makes
\(F_{\overline K}\) an isomorphism.  Since
\[
K[x_1,x_2,x_3]\longrightarrow K[x_1,x_2,x_3]
\]
becomes an isomorphism after the faithfully flat extension
\(K\subset\overline K\), it was already an isomorphism.  Hence the certified
floor \(\deg F\ge4\) is valid over every characteristic-zero field, although
the paper itself states the theorem over an algebraically closed field.

### Exact Moh--Sathaye attribution

Immediately after the main theorem on p. 80, Vistoli says that T. T. Moh and
A. Sathaye had already proved it together by computer calculation, with
printouts “about 100 pages,” and marks the work unpublished.  There is no
Moh--Sathaye paper in Vistoli's bibliography.

Two nearby references must not be conflated with that attribution:

- Vistoli's reference [8] is Moh's **plane** paper,
  *On the Jacobian conjecture and the configurations of roots*,
  J. Reine Angew. Math. 340 (1983), 140--212.
- Vistoli's reference [9] is D. Wright's 1993 paper on linear
  triangularization for **cubic homogeneous** maps in dimension three.

Moh's own Purdue overview independently recounts that he and Sathaye checked
the three-variable, coordinate-degree-\(\leq3\) case by computer and obtained
roughly 100 pages of output.  It is corroboration of the unpublished
attribution, not a substitute publication.

**Required wording in program artifacts:** “Vistoli gave the published
conceptual proof; Moh and Sathaye had an earlier unpublished computer
calculation.”

Primary source:
[Vistoli, DOI 10.1016/S0022-4049(98)00040-1](https://doi.org/10.1016/S0022-4049(98)00040-1),
especially pp. 79--80 and p. 85.

## 2. The plane theorem: exact range, hypotheses, and permissible uses

### The theorem Vistoli invokes

On p. 80 Vistoli states, as an unnumbered theorem:
\[
\boxed{\quad
\text{If }G:\mathbb A^2_\kappa\to\mathbb A^2_\kappa
\text{ is étale and }\deg G\le12,\text{ then }G\text{ is an isomorphism.}
\quad}
\]
Here \(\kappa\) remains the fixed algebraically closed
characteristic-zero field from p. 79, and
\(\deg G=\max\{\deg G_1,\deg G_2\}\).
Vistoli then says that Moh [8] proves the result through degree at most
\(100\), while degree at most \(12\) is all that Vistoli will use.

The uses inside Vistoli are concrete:

- p. 81, Lemma 1: a restriction to an affine plane has degree \(3\), so the
  degree-three plane case makes that restriction an isomorphism;
- p. 85, Lemma 11: composing a degree-three \(F\) with an inverse
  parametrization of degree at most \(4\) produces a plane étale map of
  degree at most \(12\).

Moh's published paper itself works throughout over an algebraically closed
field of characteristic zero.  Vistoli reports the inclusive ceiling
\(\leq100\).  Guccione--Guccione--Horruitiner--Valqui likewise write
\(\max\{\deg P,\deg Q\}\le100\) in their 2022 introduction, while also
noting that Moh supplies a detailed proof only for the smallest case in his
case analysis.  The literature's shorthand “lower bound 100” should not be
used to blur the exact inequality needed here.

### Base change for the program's \(\mathbb C(r)\) exits

The plane theorem legitimately applies to a map over
\(K=\mathbb C(r)\) provided all of the following have first been proved:

1. it is a **polynomial** endomorphism of \(K[p,q]\), not merely a rational
   map;
2. its two-by-two Jacobian lies in \(K^\times\);
3. its maximum degree in the plane variables is at most the cited ceiling;
4. the reduction really gives a square plane map.

Base change to \(\overline K\) then puts the map under Moh's hypotheses.
An inverse over \(\overline K\) descends to \(K\) by faithful flatness
(equivalently, by uniqueness of the inverse).  No assertion of the full
plane Jacobian Conjecture is involved.

### Current project reductions within the valid range

The following recorded ceilings are all at most Vistoli's explicitly used
ceiling \(12\); they do not need a vague appeal to the full bound \(100\).

| Project reduction | Plane ceiling | Applicability verdict |
|---|---:|---|
| `WORKING_RANK_ONE_PRIMITIVE_EXIT.md`, coordinate exit | \(12\) | Exactly at Vistoli's invoked ceiling; valid after the coordinate automorphism and fiber-Jacobian checks |
| `WORKING_QUADRATIC_COMPONENT_EXIT.md` and dependent rank-one/line-net exits | \(8\) | Within range |
| fixed-quadratic exceptional power-fibre exits | \(6\), \(9\) | Within range after base change from \(\mathbb C(w)\) |
| fixed-linear exceptional power-fibre exits | \(6\), \(10\) | Within range after base change from \(\mathbb C(w)\) |
| fixed-cubic, fixed-quadratic, fixed-linear, nodal/cuspidal binary plane-plus-shear exits | usually \(4\) | Within range once polynomiality and the square Keller block are established |

Two boundaries remain important:

- The registry's **plane degeneration** route is still blocked.  A generic
  slice of a threefold map is not automatically a square plane Keller map,
  so no numerical degree ceiling makes Moh's theorem applicable.
- The **Vistoli compactification** route may now be reopened because the
  full primary paper is accessible.  Its quartic extension is not supplied
  by Vistoli: one must separately construct an appropriate plane étale map
  and certify its degree.  The cubic-surface and cubic-plane-pencil
  arguments cannot simply be cited for quartic surfaces.

Primary sources:
[Moh, DOI 10.1515/crll.1983.340.140](https://doi.org/10.1515/crll.1983.340.140);
[Moh's author overview](https://www.math.purdue.edu/~ttm/jacobian.html);
[Guccione et al., arXiv:2204.14178](https://arxiv.org/abs/2204.14178).

## 3. Trushin and the Rung 1 singular-locus proof

### Verdict: direct prior overlap

Trushin's v1 was posted on 25 May 2026, two months before the Rung 1
artifact.  The paper works over an algebraically closed field of
characteristic zero and defines degree as the function-field degree.

The overlap is stronger than a general degree-two citation:

- Proposition 3.2.2 uses the chain rule for
  \(H(\varphi)=h^2h_0\), observes that \(\nabla H\) vanishes only on the
  singular locus of the reduced target hypersurface (dimension at most
  \(n-2\)), and concludes that a branching divisor forces the Jacobian to
  vanish.
- Proposition 3.3.3(3) and Corollary 3.3.5 state that Keller pullback
  preserves square-free polynomials.
- Lemma 4.2.1 constructs, for every degree-two map, a polynomial
  \(s\in K[x]\) and a square-free target polynomial \(S\) with
  \[
  \tau(s)=-s,\qquad S(f)=s^2.
  \]
- Corollary 4.2.2 concludes that a degree-two map cannot have constant
  nonzero Jacobian.

Rung 1 Section 3 makes the same construction in UFD language:
\(L=K(\sqrt h)\), integrality puts \(g=\sqrt h\) in the source polynomial
ring, and differentiation sends \(V(g)\) into
\(\operatorname{Sing}V(h)\).  Its quasi-finite dimension contradiction is
a concise repackaging of the same branch/singular-locus obstruction.

The section remains useful as a self-contained proof, but “independent”
should mean logically independent of the Campbell--Razar--Wright Galois
theorem, not independent of prior literature.  It should cite Trushin
Proposition 3.2.2, Lemma 4.2.1, and Corollary 4.2.2 prominently.  Trushin
also notes that square-free pullback preservation was already in
de Bondt--Yan (2016), so even that intermediate principle is older.

Primary source:
[Trushin, arXiv:2605.26390v1](https://arxiv.org/abs/2605.26390),
Sections 3.2, 3.3, and 4.2.

## 4. Gallagher's weighted lifts

### Verdict: a uniform theorem for all degrees, not finite examples

Gallagher's two-page archived preprint contains:

- Theorem 1, p. 1: for every seed satisfying the three endpoint/integral
  conditions, the weighted lift is polynomial and has constant Jacobian
  \(bc\).
- Proposition 1, p. 2: a seed of degree \(d\) gives generic fiber degree
  \(d+1\), with generic reconstruction and no extraneous generic roots.
- Lemma 1 and Corollary 1, p. 2: one explicit seed for each
  \(n\ge3\), producing \(F_n:\mathbb C^3\to\mathbb C^3\) with
  \(\det JF_n=1\) and generic fiber degree exactly \(n\).

The preprint expressly separates the proof from the finite verification:
the exact \(n\)-point fibers for \(3\le n\le100\) are accompanying
certificates.  The all-\(n\) conclusion is uniform.

The formula in the Rung 1 note is an immediate specialization of
Gallagher's general Theorem 1 and Proposition 1.  For desired generic
degree \(d\ge3\), take \(b=c=1\) and the seed
\[
p(w)=\frac{2w-dw^{d-1}}{d-2}.
\]
It has seed degree \(d-1\), satisfies the endpoint and integral conditions,
and gives
\[
a=-\frac d{d-1},
\]
which is exactly the note's \(\gamma=1-\frac d{d-1}xy+x^2z\).
Gallagher's displayed all-\(n\) seed is different, so the note may describe
its compact formula as a specialization, but it must not present the
existence of all generic degrees as new or as inferred only from examples.

Primary sources:
[Gallagher preprint, DOI 10.5281/zenodo.21479195](https://doi.org/10.5281/zenodo.21479195);
[canonical `RESEARCH.md`](https://github.com/algal/jacobianfun/blob/main/RESEARCH.md),
especially Sections 3 and 5;
[public explainer](https://jacobianfun.org/jacobian-explained),
Sections 7 and 9.

## 5. Exact edits recommended for the current Rung 1 artifact

1. Keep the no-novelty banner, but replace “short independent quadratic
   proof” with “short self-contained quadratic proof, independently of the
   Galois-case theorem,” followed immediately by the Trushin theorem
   numbers above.
2. Replace the Gallagher bibliography placeholder with the Zenodo DOI and
   cite Theorem 1, Proposition 1, Lemma 1, and Corollary 1, pp. 1--2.
3. State that the note's displayed \(F_d\) is a specialization of
   Gallagher's general weighted lift; do not imply that finite checks prove
   the all-\(d\) claim.
4. State Vistoli's original field hypothesis and add the one-sentence
   faithful-flat descent to arbitrary characteristic-zero fields.
5. In every Rung 2 plane exit, replace “the established plane low-degree
   bound” with the exact ceiling being invoked, preferably:
   “Moh's plane theorem (in the degree-\(\le12\) form quoted by Vistoli).”
