# Independent audit of low-twist optimization

Date: 20 October 2026. Scope: the plane branch-integrality results in `RESEARCH_REPORT.md`, the proof in `HIGHER_ORDER_AUDIT.md`, and the exact-rational sample calculations. The recovered authentic-source boundary in `SOURCE_GATE.md` is retained.

## Verdict

**The stated low-twist mathematical core passes independent audit, subject to its explicit hypotheses.** The full proof was available and inspected before this verdict. In particular, the finite search is over all positive symmetric orders, not merely one fixed order. The smooth irreducible absolute minimum and the SNC first-order minimum are correct. A genuine polynomial-remainder implementation bug was found by coordinate controls and repaired before acceptance. All 49 final saved search cases in all 12 examples were independently reproduced by a different coefficient model; every saved witness and search coverage was also checked. See Section 7 for the regression and independent methods.

This is not acceptance of a complete solution to the original open-ended surface question, nor a novelty claim. The pencil-cover geometry has its separate audit and is not certified here merely because it is included in the synthesis. The literature/source gate is not independently reopened by this calculation audit. No queue or publication action was taken.

## 1. Hypotheses and interpretation

The symmetric order is an integer r≥1, the base has characteristic zero, and B is a nonempty reduced divisor of total degree b≥1. Integrality means vanishing after pullback to the normalization and its cotangent line, equivalently generic tangential vanishing. Requiring all ambient tensor coefficients to vanish, or requiring vanishing in the possibly torsion-bearing Kähler differentials of a singular branch, would be different conditions.

Exact effectivity requires finitely described algebraic coefficients. Such coefficients lie in one computable number field, so exact division and linear algebra terminate. The supplied implementation uses QQ only. There is no asserted implementation for general algebraic coefficients, and no computability claim for arbitrary unspecified complex coefficients.

Repeated components must be removed before using the gradient test. Distinct reduced irreducible equations are sufficient. A squarefree reducible equation is also valid: on a component F_i=0, the gradient of F is the gradient of F_i times the product of the other equations, which is generically nonzero. Duplicating factors across inputs does not change the geometric problem but overcounts the recorded total degree; pairwise coprimality avoids that ambiguity.

## 2. Incidence-polynomial model

Euler and the rank-two determinant identity give

0 → O(−1) → O³ → Ω¹(2) → 0.

The map from O³ is represented by the three components of x×dx, whose relation is x·(x×dx)=0. Taking the r-th symmetric power of a quotient by a line subbundle gives an exact sequence

0 → Sym^{r−1} C³ ⊗ O(d−1)
  → Sym^r C³ ⊗ O(d) → Sym^r Ω¹(2r+d) → 0.

The first map is multiplication by x·a. Since H¹(P²,O(n))=0 for every integer n, taking global sections introduces no additional classes. Thus sections are exactly biforms P(x,a) of bidegree (d,r), modulo (x·a)Q. For d<0 there are no sections. For d≥0, their dimension is

(r+1)(d+1)(r+d+2)/2.

In particular k≥2r is necessary. The single polynomial x·a is a Gröbner basis for its principal ideal under any term order; with leading monomial x₀a₀, monomials not divisible by x₀a₀ form the stated basis. The cross-product choice uses a fixed volume form; changing this identification does not change existence or kernel dimensions.

## 3. Branch test and invariance

At a smooth point x of F_i=0 and a nonzero projective tangent direction represented by v, the vectors x and v are independent and both annihilated by ∇F_i. Hence x×v is a nonzero scalar multiple of ∇F_i. Homogeneity in a proves

B_i integral for P(x,x×dx) ⇔ F_i divides P(x,∇F_i).

The converse and forward direction use vanishing on the dense smooth locus and reducedness. Regularity on normalization then gives vanishing everywhere there. Euler's identity x·∇F_i=deg(F_i)F_i shows that adding an incidence relation changes the evaluation only by a multiple of F_i. Therefore the test is well defined on the quotient.

The construction is projectively intrinsic. In addition to the proof, a nontrivial invertible coordinate substitution was checked independently for the five-tangent-line example and preserved its one-dimensional order-two, twist-four kernel.

## 4. Termination and actual global minimum

For a reduced equation F of degree b, choose a linear form ℓ such that

α = ℓ dF − b F dℓ

is nonzero. Such a choice always exists: identically zero would make F a scalar multiple of ℓ^b. For a single line, avoid its equation. The Euler contraction of α is zero, its twist is b+1, and its tangent restriction to each component of F vanishes. Multiplying by any r−1 nonzero sections of Ω¹(2) gives a nonzero branch-integral section of order r and twist b+2r−1; nonvanishing follows in the symmetric algebra over the function field.

Consequently the fixed-order search is bounded by 2r≤k≤b+2r−1. More importantly, an absolute minimizer over all r satisfies

2≤k≤b+1 and 1≤r≤floor(k/2).

Every test is a finite exact linear system. Increasing k, and testing all the indicated r, therefore yields the absolute minimum, together with a nonzero certificate. There is no hidden unbounded-order search. The empty divisor would need the separate answer k_min=2 rather than the displayed b+1 bound; it is explicitly excluded here.

## 5. Sharp first-order and smooth all-order results

For an SNC divisor B, the first-order kernel is Ω¹(log B)(−B). This is checked locally at a crossing xy=0: both sides are generated by y dx and x dy. Twisting the residue sequence by t=k−b gives no sections for t<0. At t=0, the connecting map from the componentwise constants to H¹(Ω¹)=C is (a_i)↦Σ b_i a_i. Thus the dimension at twist b is c−1 for c components. For c≥2 this proves the first-order minimum b. For c=1 it excludes twist b; α above realizes b+1. For a line the two-dimensional twist-two space is consistent with the same calculation. The order-one residue/Chern-class boundary is essential, not optional.

For one smooth irreducible nonlinear branch, set q=r−1≥1. The symmetric conormal quotient yields

0 → Sym^r Ω¹(k−b) → K_r(k)
  → i_*[O_B(k−b)⊗Sym^q(Ω¹|_B)] → 0.

Euler embeds the last term into O_B(k−b−q)^N, which has no sections if k<b+r−1. At equality its sections would be constant tensors T∈Sym^q C³ with contraction x⌟T=0 for every x∈B. A nonlinear irreducible plane curve spans P², so every contraction vanishes; characteristic zero and q>0 imply T=0. The left term also has no sections when k≤b+r−1, because k−b≤r−1<2r. Therefore k≥b+r for r≥2. A line is covered by the stronger ambient bound k≥2r.

Together with the separate order-one result, this proves k_min(B)=b+1 for every smooth irreducible plane curve. The argument does not apply the degree-positive tensor endpoint to r=1, does not replace the higher-order kernel by an incorrect logarithmic symmetric power, and does not extend the smooth conclusion to singular divisors.

## 6. Threshold slope and its limited meaning

At k=2r the model consists of homogeneous dual polynomials H(a). Nonlinear branches require divisibility by their dual-curve equations; line branches require vanishing at the corresponding dual points. Multiplying these equations and, if necessary, further factors through the remaining points gives a nonzero threshold form for every reduced B. Thus the minimum normalized slope k/r is 2 and is attained.

This is not a low absolute-twist result and does not produce a sufficient ramification budget. For a smooth degree-b branch the direct dual curve has degree b(b−1), whereas absolute twist b+1 is already achieved in order one. The distinction between the two objectives is maintained in the synthesis.

The conic-tangent order-two form and the envelope conic are already present in Garcia-Fritz–Urzúa 2020, §4/Corollary 4.3, as identified by the source review. No novelty is assigned here. The envelope must remain in the integral locus. The broader surface criterion is not settled by this example, the normalized-slope observation, or the finite plane optimization alone.

## 7. Independent computation and implementation boundary

The original code uses the incidence quotient. The independent checker instead uses a polynomial W(x,u) with x-degree k−r and u-degree r, imposes Euler horizontality

Σ x_i ∂W/∂u_i = 0,

and evaluates along all three tangent vector fields

(0,F_z,−F_y), (−F_z,0,F_x), (F_y,−F_x,0).

Their values span the tangent cone plane at a smooth point; the Euler condition removes the radial direction. Remainders modulo the reduced equation therefore impose precisely generic tangent vanishing. This constructs a different, larger linear system rather than reusing the incidence basis or its rank calculation.

Artifacts:

- `checks/audit_independent_model.py`: independent horizontal-tensor implementation with its own sparse lexicographic normal-form routine, not SymPy's remainder or Gröbner implementation.
- `checks/audit_independent_results.json`: 14 structural/sample comparisons, including the failing transformed-conic regression and a nonreduced-input rejection, all passing.
- `checks/audit_division_free.py` and its results JSON: coefficient-block divisibility constraints E(P)−FQ=0, using no polynomial-division algorithm; validates transformed conics, multiple branches, and altered/zero witness controls.
- `checks/audit_saved_cases.py` and `checks/audit_saved_results.json`: all 49 final saved search pairs in all 12 examples, independently reproduced; all 12 saved witnesses and complete search coverage checked. The receipt records the exact source-results SHA-256 and byte count.

This includes the ten-line arrangement x+t y+t⁴z=0 for t=1,…,10: minimum twist 7, with its first stored witness in order 2. Order 3 also has sections by the separate dimension count, but the saved minimum search stops at its earlier order-two success. The exact computations support the finite examples, not untested asymptotic or generic-rank claims.

### Found and repaired normal-form defect

The initial implementation used SymPy `Poly.rem`. With several variables, that operation need not give the linear multivariate normal-form map required for assembling coefficient constraints. For F=xz−y²−yz−z², take E₁=xy+xz and E₂=−xy. That routine returns E₁ and E₂ unchanged, but sends their sum xz to y²+yz+z². Therefore its output is not additive as a polynomial-valued map. Building a matrix from those individual outputs is invalid.

The original main coordinate control consequently found dimension 2 instead of 3 for a transformed smooth conic at (r,k)=(1,3). The initial independent horizontal model shared that remainder primitive, so its agreement on the special saved examples did not expose this shared dependency. The old acceptance was suspended rather than retained after this finding.

The main computation was changed to a genuine Gröbner normal form. This audit's horizontal model was changed to an independently written sparse lexicographic division routine that transfers indivisible leading terms to the remainder and continues. A third check encodes divisibility by auxiliary homogeneous quotient coefficients and exact coefficient comparison, avoiding both remainder algorithms entirely. The transformed conic now has the required dimensions 3 and 1 at (r,k)=(1,3) and (2,4), respectively. Current acceptance and receipts refer only to the regenerated outputs.

### Enforced input and mutation controls

Input assumptions were only preconditions in the first inspected script. They are now executable guards. A decisive historical negative test is F=z² at (r,k)=(2,4): the unguarded gradient rule admitted all six ambient dimensions, while the reduced line F=z has dimension five. This is not a counterexample under the reducedness hypothesis, but it demonstrates why silently accepting nonreduced input was wrong. The current implementation rejects that input.

The current controls also reject repeated/shared components, nonhomogeneous equations, constant or empty branch data, zero order, an altered nonintegral witness, and a zero incidence-class witness. They verify agreement between a squarefree product and split factors, and six coordinate transformations of three sample arrangements. `checks/validation_controls.json` records the main controls. The independent division-free and sparse-division checks avoid relying solely on that file's assertions.

The reported editorial reference mismatch was corrected: the synthesis now points to `PENCIL_COVER_AUDIT.md`.

## 8. Local ramification and numerical budget scope

The local formula γ=min_j{e m_j+j(e−1)} is correct in the declared product model x=u^e,y=v. Different j give independent symmetric differential monomials, so there is no cross-j cancellation. Integrality supplies m₀≥1 and hence gain at least e−1, not r(e−1); the stated dx(dy)^{r−1} counterexample to multiplying the gain by r is valid.

The conditional budget statement is also correctly bounded. For g≥1, k+2r(g−1)<a implies k−a<0. For a noncontracted curve, the integer H·Γ≥1 then bounds the target degree by k−a+2r(g−1)<0, using the given nefness certificate for R−aH. Contracted curves are explicitly excluded from that step. The combination k≥2r and the strict budget bounds r and k, making the stated sufficient-criterion search finite. For g=0, k≤a is a valid sufficient uniform condition. No unjustified upper bound on H·Γ, general algorithm for nefness, or universal multiplication of the ramification gain is asserted.

## Acceptance boundary

The finite optimization, sharp subclasses, and exact sample claims are accepted at the stated scope. No counterexample to those claims was found. The authentic source remains an open-ended existence/usefulness problem requiring upstairs positivity, correct exceptional-divisor control, and integral-curve completeness. Those extra conclusions cannot be inferred from a plane kernel or from its minimum absolute twist alone.
