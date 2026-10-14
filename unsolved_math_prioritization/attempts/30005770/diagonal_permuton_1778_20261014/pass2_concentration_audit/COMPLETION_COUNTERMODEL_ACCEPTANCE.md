# Independent audit of the repaired completion-bound countermodel

Date: 14 October 2026.

## Verdict and exact pins

Accepted in full within the explicitly abstract numerical scope:

- COMPLETION_BOUND_COUNTERMODEL.md, 11782 bytes, SHA-256 62b04f7890c2cf1490803739ba15576b4138e699961352b19213cdeba8f0878a.
- PREFIX_STATE_REDUCTION.md, 4175 bytes, SHA-256 09e523a949a25874f5587986ddecc55f2c8d51ad68ff1f5b7896075f1cad4c9f.

No mathematical correction was required. The first artifact proves that the stated scalar numerical tree bounds, including the full all-size binomial completion upper bound, do not imply the proposed completion-weighted frontier concentration. The second proves an additional exact state reduction for actual avoidance classes. Neither proves or disproves the universal permuton target.

## 1. What the repaired tree really satisfies

The preliminary rules give labels 1,2,3,4 at levels 0,1,2,3 and six A_4 vertices at level 3. All later A_L and B_L rules have exactly L children. Their sorted labels dominate 2,...,L+1 and their maximum is at most L+1. In particular the level-n maximum label is at most n+1, proving a_(n+1)<=(n+1)a_n and a_n<=n!.

The finite Catalan comparison embeds below every node because each comparison child can be assigned a distinct actual child of at least its label. This proves the lower bound B(L,t)<=D_t(v), including all preliminary nodes, and gives a_t at least the t-th Catalan number. Distinct children of the same named type are genuinely distinct vertices; none of the counting formulas incorrectly identifies them.

## 2. Generating functions, growth and positivity

For A_L, an initial run of r A-steps has multiplicity 3^r. The stop-or-B-exit contribution at its end is C^(L+r-3). Summing proves F_L=C^(L-3)/(1-3zC) as a formal power series, not an approximation. The preliminary levels then give A(z)=1+z+2z^2+6z^3 F_4.

The unique pole of F_4 inside |z|<1/4 is rho=2/9. Its principal coefficient is 3/4, since C(rho)=3/2, w'(rho)=3 and 1-3w has slope -9. Multiplication by 6z^3 gives root principal coefficient 4/81. Subtracting the pole leaves an analytic remainder on every smaller circle than 1/4. Thus the stated coefficient asymptotics and growth rate 9/2 follow.

The all-size supermultiplicativity argument is valid. The Jacobi matrix with diagonal 4,2,2,... and off-diagonal 1 defines a bounded self-adjoint operator. Its displayed quadratic form is exactly a sum of squares plus 3x_0^2, so positivity extends from finitely supported vectors by continuity. Deleting its first row and column leaves a stationary tail whose return series solves T=1/(1-2z-z^2T), with constant term 1; this is C^2. The initial return series is consequently 1/(1-4z-z^2C^2)=F_4.

Thus d_t is the moment sequence of a positive bounded spectral measure. Cauchy-Schwarz gives log-convexity for every t>=1. All moments are positive. The root ratios begin 1,2,3,4 and continue with the increasing d-ratios, so they are nondecreasing across the join as well. Their telescoping product proves supermultiplicativity at every pair of sizes. No finite positivity test is being substituted for this argument.

## 3. All-size upper completion bounds

Every node type is covered, including the small-depth boundaries:

- For B_L, expanding C^L over weak compositions bounds each product of Catalan coefficients by a_t, using Catalan domination and supermultiplicativity. Counting compositions gives binom(L+t-1,t)a_t.
- For A_4 and t>=3, a node at depth t-3 has label at most t+1. The final three generations therefore contribute at most (t+1)(t+2)(t+3) descendants per node. Since a_t=6d_(t-3), this is exactly the desired binomial factor. At t=0,1,2, the respective values 1,4,17 are bounded by 1,4,20.
- For A_L with L>4, F_L=C^(L-4)F_4. Coefficient convolution, a_u a_(t-u)<=a_t and the ordinary Vandermonde identity yield binom(L+t-1,t)a_t. The r=L-4=1 case is valid directly from c_u<=a_u and does not require an actual B_1 vertex to exist.
- For the label-2 preliminary node, t=0,1,2 are immediate, with t=2 equal to 6 on both sides. At t>=3, the final-one-generation bound is exactly d_(t-2)<=(t+1)d_(t-3).
- For the label-3 preliminary node, t=0,1,2 are immediate, with t=1,2 equal to 3 and 12 on both sides. At t>=3, the final-two-generation bound gives the stated factor (t+1)(t+2).
- At the root, the upper completion inequality is equality.

This verifies the claimed upper bound for every label and depth. The earlier coarse model's isolated 51>50 defect has genuinely been repaired; it is not merely absent from a finite checked range.

## 4. Exact marked law and failure of the proposed weighted criterion

Marking only A-to-A steps multiplies each such transition by u and leaves B continuation weights unchanged. The resulting F(z,u)=C/(1-3uzC) is correct. Its unique nearby pole is rho(u)=(3u-1)/(9u^2), and the coefficient of its principal part is

    K(u)=3u(3u-2)/(3u-1)^2.

This agrees with K(1)=3/4. A fixed circle strictly between 2/9 and 1/4 separates this pole from the other singularities for u in a sufficiently small complex neighborhood of 1. The uniform analytic remainder justifies coefficient differentiation and logarithmic cumulants. The first two leading cumulants are t/2 and 3t/4, with bounded remainders.

Every level-n vertex, n>=3, is a descendant of exactly one of six identically structured A_4 vertices. Uniform sampling from the full level therefore induces precisely the coefficient ratio used in the proof, with relative depth t=n-3. It does not impose a separate sampling law on spines. Chebyshev gives S/n->1/2 in probability.

On a long A-spine, the ancestor at absolute level j has label j+1. The interval of such ancestor levels supplies the lower bound 1/2-epsilon for the averaged probabilities of labels at least epsilon n. The uniform ancestor marginal is exactly D_(n-j)(v)/a_n by disjoint descendant counting. Therefore the proposed completion-weighted tail condition fails in this tree despite all the stated numerical hypotheses.

## 5. Essential exclusion of actual avoidance classes

The statement's boundary is mathematical, not merely a disclaimer. Its counts equal n! through n=4 but have a_5=102. A principal class avoiding a fixed pattern of length at most 4 would already differ earlier; length 5 would give 119 at n=5, and a longer pattern would give 120. Hence this model cannot be any principal avoidance class. Its B_2 states also fail the literal first-hit interpretation for alpha of length at least 3.

The accepted conclusion is restricted to the enumerated numerical assumptions. It does not prohibit proofs using hereditary restriction compatibility, exact alpha-dependent transitions, geometry of first-hit prefix states, or a different route to weak concentration.

## 6. The actual prefix-state companion

The prefix-state lemma is correct for every fixed nonempty alpha, including alpha=1. If the first alpha occurrence ends at L, every subsequently inserted minimum must appear before the still-surviving original occurrence's endpoint. That endpoint shifts to the right but always precedes every original suffix entry. Consequently the earliest alpha occurrence can never depend on the discarded suffix.

Standardizing the original prefix preserves all relevant order relations, and every inserted minimum is below every retained original entry. Induction therefore gives identical first-hit endpoints and allowed gap sets after every finite insertion history. The correspondence preserves gap indices and is bijective, proving equality of complete continuation trees and all D_t counts. In the absent case the entire original permutation is retained, with a separate flag; the nonexistent sentinel position is not treated as an entry.

The two explicit containing-state counterexamples were checked directly:

- For alpha=132, states 1342 and 2143 both have L=4, but child labels are (5,5,5,5) and (3,5,5,5), so D_2 is 20 versus 18.
- For alpha=312, states 1423 and 2413 both have L=4, but child labels are (5,5,4,5) and (5,4,4,5), so D_2 is 19 versus 18.

All four parents avoid their indicated target patterns. Thus the containing/absent flag plus scalar L still does not determine completion weights. The full standardized prefix is a valid state; no finite-state, positive-recurrence or uniform-law conclusion follows from that fact alone.

## 7. Finite verification boundary

The supplied checker implementations use explicit runtime failures rather than optimization-disabled assertions. The repaired-tree normal, -O and -OO reports have identical mathematical records and match the frozen proof/checker hashes. They report 4,960 A-recurrence checks, 10,287 node completion inequalities for labels through 64 and depths through 80, 861 exact weighted-ancestor identities, independent Jacobi multiplication and exact marked-spine calculations through n=400.

These are finite regression results from the completed checker runs, not independent asymptotic evidence. The proofs above establish the all-size assertions. The separate prefix-state report checks complete depth-two continuation trees for 32 alpha classes at explicitly bounded parent sizes, together with both scalar-state examples. Optimization-mode receipts are recorded separately as they complete. No existing accepted proof file was changed by this audit.
