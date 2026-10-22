# Root analytic reconstruction and source scope

This is a current candidate-aware root review of the immutable submitted
proof, not a blind discovery or a historical-priority certificate. The
claim is a negative answer to universal **pointwise multiplication**:
for every fixed nonconstant complex polynomial p, the functions F in HC(D)
with pF outside HC(D) form a dense subset of H(C), even near each given
f in HC(D). A single F defeats all positive monomials, while no assertion
of one F defeating all nonconstant polynomials is made.

## Original target and inputs

Root freshly fetched the actual 50-page2008 Oberwolfach report, matched its
identity against the submitted source data, and rendered/visually inspected
the whole printed330/PDF34 page. Definition4 defines the dense derivative
orbit with n=0,1,... on H(C). Question5 is the pointwise polynomial product
question, with f in HC(D) and p nonconstant. Theorem6 guarantees a residual
positive class for all nonzero p; it does not quantify over every f in HC(D).
Dense negative examples can be disjoint from that residual set. These are
direct source-scope checks, not an inference of present openness.

The seven nonself submitted manifest bindings and all eight Git blob/byte
identities pass. Original PROOF SHA256 is
3479117bbe24e0829a31a9ac616c305028ad571aa41647d28b3e7016311f8fe6.
Original bytes and historical audit records remain immutable.

## Infinite arguments

The existence argument is complete. H(C) is complete and metrizable under
disk seminorms by compatible locally uniform limits and the Weierstrass
theorem. Gaussian-rational polynomials are a countable dense family.
Differentiation is continuous by Cauchy estimates. For each polynomial target
P=sum b_k z^k, its n-fold primitive with zero low coefficients has terms
b_k k! z^(n+k)/(n+k)!; each tends to zero uniformly on any fixed disk, and
its nth derivative is P. Adding this primitive to an approximating polynomial
Q, with n large enough that D^n Q=0, proves every required orbit-approximation
open set dense. The countable Baire intersection supplies HC(D) densely.
There is no unsupported appeal to a printed explicit hypercyclic sequence.

Every tail of a dense orbit is dense: remove the finite closed initial set
from any nonempty open set. A nonempty open subset of H(C) contains infinitely
many distinct small constant translates, so the remainder is nonempty/open.
One can therefore choose increasing approximation indices. An entire h with
D^n h tending to zero preserves hypercyclicity on addition along those indices.
This is a null-orbit statement, not a claim that all small perturbations work.

For derivative-normalized coefficients c_k tending to zero,
h(z)=sum c_k(z-alpha)^k/k! is entire and
sup_(|z-alpha|<=R)|h^(n)(z)| <= exp(R) sup_(j>=n)|c_j| tends to zero.
The domination proves normal convergence and termwise differentiation.
Disks centered at any fixed complex alpha exhaust C. The normalization by
k! is essential and is used consistently.

For p=z, replacing only those normalized coefficients a_k with modulus less
than eta/(k+1) by the positive real eta/(k+1) changes them by at most
2eta/(k+1). Equality belongs to the unchanged branch. Thus the correction is
null-orbit and can be arbitrarily small on each fixed compact as eta tends
to zero. The new b_k all have modulus at least eta/(k+1). For n>=1,
(zF)^(n)(0)=n b_(n-1) has modulus at least eta, whereas the zeroth value
is zero. The entire orbit misses the evaluation ball centered at eta/2 of
radius eta/4. This includes all derivative orders and all complex phases.
With eta=1, for each m>=1 the monomial product's high-order modulus is at
least (k+m)!/[k!(k+1)]=product_(j=2)^m(k+j)>=1, and all lower orders vanish.
The same fixed F and missed evaluation ball work for every positive monomial.

For arbitrary fixed nonconstant p, choose a root alpha of multiplicity m>=1
and write p(alpha+w)=sum_(j=m)^d q_j w^j, q_m nonzero. The product's
(k+m)th derivative at alpha depends on the current correction only through
A_k c_k, where A_k=q_m(k+m)!/k! is nonzero. All other correction indices
are strictly below k. If the already determined S_k has modulus at least eta,
choose c_k=0; otherwise choose (eta-S_k)/A_k, making the product derivative
exactly eta. In both cases
|c_k|<=2eta k!/(|q_m|(k+m)!). This decays for m>=1, independently of all
previous large or cancelling terms, so no hidden recursive accumulation is
transferred to an unsupported convergence claim. Later corrections cannot
change a derivative already fixed. The convergent Taylor-product formula is
sum q_j n! b_(n-j)/(n-j)!, including empty sums/base k=0 correctly.

Orders n<m vanish, all orders n>=m have evaluation modulus at least eta,
and the same evaluation-ball argument excludes hypercyclicity. The uniform
bound |h|_(R,alpha)<=2eta exp(R)/(|q_m|m!) lets eta be chosen before running
the recursion to satisfy any given neighborhood of f. It does not assume
continuous dependence of the recursively chosen coefficients on eta.
F remains hypercyclic by the null-orbit lemma. Density of HC(D) then gives
density of the fixed-p negative set in all H(C). Choice of alpha/corrections/F
may depend on p; the proof never interchanges those quantifiers.

Nonzero constant multiplication is a homeomorphism commuting with every D^n,
so it preserves all HC(D). The zero multiplier fails, and every nonconstant
p fails by the preceding theorem. The classification is complete.

## Supporting exact diagnostics and current conclusion

The separately written root Gaussian-rational driver imports no submitted or
source-author program. It tests complex threshold/equality cases and the
triangular correction on finite synthetic jets. A second finite oracle
expands both polynomials into ordinary coordinates at z=0, multiplies them,
and evaluates derivatives at a rational nonreal alpha, checking the rooted
product formula without importing the submitted recurrence. It also checks
earlier derivative preservation, low-order root vanishing, monomial factors
and factorial-tail monotonicity. Three actual changed algorithms (no
correction, wrong leading factorial, dropped cross terms) fail the real
evaluation-exclusion check. Normal/-O/-OO results are byte-identical.
ROOT_EXACT_DIAGNOSTICS.json and ROOT_REPLAY_RECEIPT.json record current runs.

These finite tests are algebra corroboration only. Entire convergence,
every derivative order, null-orbit convergence, hypercyclicity and density
are justified by the analytic deductions above. Root finds no mathematical
gap at this checkpoint. Independent source-question reconstruction and a
separate candidate-aware analytic/source adversary remain in progress;
no final math, priority, preprint or publication gate is asserted here.
