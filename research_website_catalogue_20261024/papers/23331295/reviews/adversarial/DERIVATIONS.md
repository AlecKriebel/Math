# Row128 independent full-claim derivations and boundary controls

## All-order polynomial restriction, with topology kept in the domain

Fix m>=2 and L_n equal to the coherently oriented closure of sigma^(2n) with m-2 split unknots. For r designated crossings use a braid with2n initial positive crossings and r two-crossing blocks. In each block keep the first crossing positive and resolve the second positively or negatively. Positive gives sigma^2; negative gives sigma*sigma^-1=1. The resolved braid word therefore has exponent2n+2j when exactly j of the r choices are positive. Its closure has two braid components because this exponent is even; the extra split components stay fixed. Every chosen crossing is a transverse double point in the same immersed m-component link before resolution. Its total permutation has parity(2n+r)+r=0 mod2, so the singular domain does not silently change to a knot. The B2 group is infinite cyclic, so collecting exponents and ReidemeisterII cancellations is legitimate.

The alternating crossing-resolution sum is exactly

Delta^r a(n)=sum_{j=0}^r (-1)^(r-j) binom(r,j) v(L_{n+j}),

a(n)=v(L_n). If v has finite order<=d, this vanishes at r=d+1, for every n>=0, not merely at sampled n. Define

P_v(t)=sum_{r=0}^d binom(t,r)Delta^r a(0).

The polynomial binom(t,r) is defined by t(t-1)...(t-r+1)/r!, with all denominators invertible in characteristic0. It has the same initiald+1 values as a. Both satisfy the same orderd+1 forward-difference recurrence, which determines the next value uniquely since the leading recurrence coefficient is1. Induction gives all nonnegative n. This also works at d=0. An alternative uniqueness proof uses infinitely many distinct embedded integers in a characteristic-zero field. Increasing a chosen bound d does not change P_v.

For u,v each finite-order, their sum/product are again finite-order: on any crossing cube the unique multilinear representative of an orderd invariant has no coefficients above degreed, because each such coefficient is an alternating derivative of a singular link. Product followed by Boolean reduction x_i^2=x_i has degree at most the sum. Therefore P_(u+v), P_(uv), P_1 agree on infinitely many n with P_u+P_v, P_u*P_v and1, respectively. Polynomial uniqueness makes v->P_v a unital algebra homomorphism on every element of the whole union of finite-order spaces. No common cutoff or extension of a character from a smaller algebra is required.

## Genuine invariant and exact actual-link zero set

On a crossing cube keep component labels consistently through crossing changes. An indexed pairwise linking number changes by +/-1 only at an intercomponent crossing of that pair; self-crossing changes contribute0. It is thus affine in the cube variables. The sum g of its squares is degree<=2; f=4g^2-g is degree<=4. The order bounds are uniform in the component count because they are bounds on polynomial degree, not on the number of summands. Permuting labels only permutes the sum. Reversing a component changes each incident linking sign but not the squares. Thus g,f are genuine invariants in the oriented unordered, labelled and orientation-forgotten domains at issue.

For every actual link q=g(L) is a nonnegative integer. In characteristic0, q(4q-1)=0 implies q=0 because no integer equals1/4. Since q is a sum of integer squares, q=0 iff every pairwise linking number is0. This proves the full actual zero set, including all algebraically split links; these need not be geometrically split. The unlink proves nonemptiness. The principal ideal A=(f) has the same actual zeros as f because1 belongs to the algebra. Thus g lies in J_act(Z_act(A)). Any element of sqrt(A) lies there too: scalar fields have no nonzero nilpotents, so h(L)^N=0 implies h(L)=0.

The same arithmetic works over every characteristic-zero field. This uses the embedded integers and their external integer sum-of-squares property; it does not require an ordering of the coefficient field or assert that arbitrary sums of field squares are nonnegative. Neither positive characteristic nor m=1 is covered: for one-component links this particular g is identically0.

## All radical powers, not a bounded search over possible multipliers

On L_n the two intercomponent strands give2n positive crossings, hence lk=n, and all extra linking numbers vanish. Consequently P_g(t)=t^2, P_f(t)=t^2(4t^2-1). Evaluation at t=1/2 gives a character chi on the full algebra with chi(g)=1/4 and chi(f)=0. For every N>=1 and every possible finite-order h, g^N=fh would imply4^-N=0. This contradicts the characteristic-zero field axioms.

A second direct route eliminates character language. Restrict a hypothetical equality to every n>=0 and use the polynomiality already proved for arbitrary h. Polynomial uniqueness would force

t^(2N)=t^2(4t^2-1)P_h(t).

The right side vanishes at t=1/2 while the left does not. Equivalently, after cancellation in the polynomial domain,4t^2-1 cannot divide t^(2N-2). Exact Euclidean reduction modulo4t^4-t^2 gives, for all N>=1, the nonzero remainder4^(-(N-1))*t^2. The universal remainder follows by the recurrence t^(2N)=t^(2N-4)*t^4 congruent(1/4)t^(2N-2), baseN=1. This is a universal polynomial proof; the finite checks of powers are only diagnostics.

The character is not an actual-link evaluation, since every actual g-value is an integer. t=1/2 is a polynomial parameter, not the odd braid sigma whose closure has one component. The construction fails no classical Hilbert Nullstellensatz: actual links form the restricted evaluation set, while the full character spectrum includes the extra character.

## Whole-domain variants and separate ideal

Restriction from the all-component algebra V to the fixed m-component family is unital, and a global finite order bounds each restriction. Since g/f themselves have uniform orders<=2/4, the same contradiction proves the full all-component claim. This is not an assumption that every fixed-component invariant extends globally. For the orientation-forgotten theory, its finite-order invariants pull back to an orientation-independent subalgebra of the oriented theory, and chi restricts; the symmetric g is in that subalgebra. The labelled version uses the same braid family and sum.

In the labelled theory let B be generated by all indexed pairwise linking numbers. Then g belongs to B, f belongs to B, and A subset B. But chi(g)!=0 while chi(A)=0, so g is not in A and A!=B. Both have the algebraically split actual zero set. This does not show any inequality for sqrt(B) or decide whether J_act(Z_act(B))=B. Retaining that separate-ideal boundary is part of validating the original statement, not a narrowed replacement.

## Meaningful finite controls and excluded completion

Before native science code/results or foreign bodies, independent_controls.py checked3,366 exact predicates:27 entire signed braid-expansion cases through r=8;162 Newton evaluations;27 product evaluations;14 three/five-crossing g/f degree tests;1,092 integer zero-set vectors;440 orientation/permutation transforms;8 character-power evaluations and four pointed boundary controls. Outputs and source are bound by OWN_PROOF_RESULTS_SEAL. These checks cannot verify arbitrary-order topology or every invariant; the proofs above carry those quantifiers.

Four rejected extrapolations are concrete. Odd braid exponents do not belong to this two-component family. A complex scalar g=1/4 is not an actual integer linking-square value. Finitely many sampled values do not establish polynomiality: multiply a nonzero perturbation by t(t-1)(t-2)(t-3) to preserve the first four samples but change the next. Finally, in the illustrative formal power-series target K[[t]],4t^2-1 is a unit with inverse -sum_{k>=0}(4t^2)^k, so t^2 is a multiple of t^2(4t^2-1). The exact finite geometric identities verify this boundary. This is not a claim about every possible completion of V; it explains why polynomial restriction/evaluation at1/2 cannot simply be extended to arbitrary completed or infinite-order algebras. The manuscript explicitly excludes those variants.
