# Equivariant integration: a global-smoothness obstruction and exact pole cancellation

Status: the literal demand for a globally smooth Lie-algebra value together with the source's fixed-point-only localization formula is inconsistent. This is a standard source-level obstruction, not a new discovery or a solution of all repaired noncompact integration problems. Two substantive approaches; separate review pending.

## 1. Exact primary statement and its neighboring convention

AIM's *Moment Maps and Surjectivity in Various Geometries*, Question6.7 (M. Libine), printed p.9, asks for a geometric integration of equivariant forms on a noncompact real-algebraic symplectic manifold with a compact Hamiltonian torus, proper semialgebraic moment map and compact fixed set. Parameter dependence is smooth semialgebraic, not necessarily polynomial. It asks that localization hold and describes values as smooth functions on the Lie algebra. Source: https://aimath.org/WWN/momentmaps/momentmaps.pdf .

Immediately before this question, Definition6.4 defines rationalized equivariant cohomology by tensoring with Q(u), and defines integration as the sum of fixed-component contributions divided by their equivariant normal Euler classes, explicitly valued in Q(u). Comment6.5 mentions a distributional interpretation. Theorem6.8 and Definition6.9 in the dataset are spillover into subsequent context, not additional hypotheses of Question6.7. In particular the question is not restricted to compactly supported forms or to hypercompact hyperkähler manifolds.

We interpret “localization” in the explicit fixed-point-only sense given there. The no-go statement below does not apply to a different formula with additional terms at infinity, a function defined only at regular parameters, or a distributional target. Those are meaningful alternatives but change the literal requested package.

## 2. All hypotheses hold on the complex line

Let M=C=R^2 with omega=dx wedge dy and let S^1 act by rotations. This is a real-algebraic manifold and algebraic group action. Its generator is V=-y partial_x+x partial_y, and i_V omega=-d mu for the polynomial moment map mu=(x^2+y^2)/2. We adopt this Hamiltonian sign convention. The map mu:R^2->R is proper: inverse images of compact subsets are closed and bounded. The fixed set is the single point0, hence compact.

Take alpha=1. It is smooth, polynomial and semialgebraic in both coordinates and parameter, invariant, and equivariantly closed under d_u=d-u i_V. Thus it satisfies even the polynomial subcase of the question; ambiguity in defining semialgebraic maps into an infinite-dimensional form space cannot exclude this constant example.

Normalize the equivariant parameter u so that the Euler class of the weight-one complex line is u. The fixed-point prescription of Definition6.4 then forces

I(alpha)(u)=1/u, for u nonzero.

With a differential-form convention inserting nonzero 2pi or imaginary constants, the numerator changes by a fixed nonzero constant; the pole argument is identical.

**No-go theorem.** There is no assignment on all the forms in Question6.7, valued in C-infinity of the whole real Lie algebra, that agrees at every regular parameter with the stated fixed-point-only localization formula.

**Proof.** For the admissible example above the output would be a smooth function F:R->C satisfying u F(u)=1 for every u nonzero. Continuity at0 would give0=1 by taking u to0. This is impossible. No linearity, ordinary convergence or cohomology axiom is needed for the contradiction. QED.

The same obstruction is already visible in the elementary rationalized-cohomology definition. No priority is asserted. The ordinary top-degree integral of the zero-form1 is not used as a substitute for the proposed regularized integration, so the proof does not assume ordinary cutoff convergence.

## 3. Exact smooth-extension criterion for positive weighted representations

Let M=C^n, n>=1, with a circle action of positive integer weights w_1,...,w_n. The symplectic form is the sum of the standard coordinate forms, and mu=(1/2)sum w_j|z_j|^2 is proper, polynomial and bounded below. The fixed set is0 and its equivariant Euler class is c u^n, c=product w_j nonzero.

For any smooth equivariant form alpha, its restriction to the fixed point is a smooth scalar a(u); only its differential-degree-zero component survives. The fixed-point expression is

L_alpha(u)=a(u)/(c u^n), for u nonzero.

**Proposition.** This expression extends smoothly to the entire real Lie algebra if and only if

a^(j)(0)=0 for j=0,...,n-1.

When it exists the extension is unique. If a is polynomial, the condition is exactly divisibility of a by u^n in the polynomial ring; the extension is polynomial. The proposition concerns extension of the localized expression, not the existence of every proposed geometric integration construction.

**Proof.** If F is a smooth extension, the identity a(u)=c u^n F(u) extends to0 by continuity. Differentiating proves the required vanishing jets. Conversely Taylor's formula with integral remainder, using these zero jets, gives for all real u

a(u)=u^n/(n-1)! times integral_0^1 (1-s)^(n-1) a^(n)(s u) ds.

The coefficient on the right is smooth in u: every derivative may be passed under the integral on its compact interval, locally uniformly in u. Dividing that coefficient by c defines the required extension. Values off0 determine it uniquely by continuity. The polynomial statement follows by examining coefficients of u^0,...,u^(n-1). QED.

For instance the unit form has a=1 and fails the first jet condition for every n. The coefficient-only equivariant forms a(u)=u^n b(u), with b smooth semialgebraic, do pass; their localized values are b(u)/c. Such examples remain noncompact and are not compactly supported in M. Nothing in semialgebraicity alone forces these vanishing conditions.

## 4. Published regularization and the remaining repaired questions

Libine, *Integrals of equivariant forms over non-compact symplectic manifolds*, Journal of Symplectic Geometry8 (2010),299–321, https://arxiv.org/pdf/math/0411638 , explicitly arose from the AIM workshop. Its framework uses subanalytic Hamiltonian data, a proper moment map, polynomial equivariant forms and an added no-zeroes-at-infinity condition. Theorems10 and13 give regularized distributional formulas represented by fixed-point expressions on a dense open strongly regular parameter set. They do not state that every such expression extends smoothly through the singular parameters. The published distributional framework is therefore compatible with the example above, not contradicted by it. We verified these theorem statements and conventions, not every analytic estimate in their proofs.

The imported prior research report for this record already described ordinary cutoff divergence and boundary transgressions on C. Those are different from the simple global-extension incompatibility used here. No imported claim of novelty is adopted. A construction with a boundary-at-infinity correction could cancel a pole only by changing the fixed-point-only value off the singular set; a distribution can also have singular behavior. Neither possibility supplies a smooth extension of 1/u while retaining its values for u nonzero.

The original literal conjunction has the obstruction of Section2. A full theory for arbitrary nonpolynomial semialgebraic parameter dependence, a precisely specified renormalization or distribution space, and allowed boundary terms remains outside this package. No compact-support replacement, missing properness condition, or implicit chamber restriction is inserted to claim those repaired problems solved.

## 5. Verification boundary

The exact checker verifies weighted Euler factors and moment-map coercivity constants, polynomial jet/division equivalence over rational coefficients, and the Taylor-remainder integral identity for test polynomials. These are finite algebra controls. Global no-go follows from continuity, and the all-smooth extension theorem follows from the written integral remainder argument. No numerical convergence experiment or independent proof of Libine's analytic theorem is claimed.
