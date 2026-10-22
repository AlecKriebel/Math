# Narrow adversarial audit of independent_controls_01.py

Audit completion: 100% of the assigned finite-checker review. This percentage
does not estimate progress on the geometric or asymptotic research claim.

The audited program SHA-256 is
`a054d758170017c270430d39b8bca28fe81103e1e3c3cbd5ab10b9bccb439180`.
The submitted receipt and frozen DVV comparator pins are in AUDIT_RECEIPT.json.
All three inputs remained unchanged. No source, frozen file, public package,
branch, remote, provider record, or other chat was changed. All audit outputs
are in this directory.

## Finding

No defect was found in the exercised finite formulas, the full count-law
inversion, or the KdV evaluator. The original receipt was reproduced exactly
apart from its newly generated UTC timestamp. The source still provides finite
controls only. It does not verify the geometric correspondence, uniform
high-genus input, asymptotics, novelty, or case completion.

There is one API-hardening limitation outside the declared and exercised
domain: the helpers do not reject invalid shape/threshold arguments. For
example, lower_orthant(3,(2,),(-1/2,)) returns 3/4 although the actual survival
probability is 1. Every submitted call has nonnegative rational endpoints in
[0,1], so this counterexample does not invalidate a submitted finite result.

## Independent derivation of the survival formula

Let the selected positive integer Dirichlet shapes be a_1,...,a_m, total
shape T, residual shape b=T-sum(a_i)>=0, and thresholds t_i>=0. Put
R=1-sum(t_i). For R<0 the event is empty. For R>=0, translation x_i=t_i+y_i
and binomial expansion of each x_i^(a_i-1) give

    P(X_i>=t_i for all i)
      = (T-1)! sum_{0<=k_i<a_i}
          R^(T-1-sum(k_i))/(T-1-sum(k_i))!
          product_i t_i^k_i/k_i! .

For b>0 this follows by integrating the residual coordinate's Dirichlet
density. For b=0 it follows by integrating on sum(y_i)=R with m-1 free
coordinates. Both integrations give the same denominator and exponent; no
fictitious positive residual shape is needed. At R=0 and m>=2 all exponents
are at least m-1>0, giving probability zero. For b=0,m=1 the distribution
is the atom X_1=1; the formula correctly has a zero-exponent contribution
at t_1=1. This also explains why the explicit atom branch in rectangle is
needed to implement closed rather than half-open windows.

Inclusion-exclusion computes lo_i<=X_i<hi_i. On every non-atomic marginal
the boundary difference has measure zero, including when all components
have been selected. The only remaining atom, the one-component law, is
handled explicitly. The three submitted full-selection examples are correct.

The audit independently integrated the Dirichlet density by convolution of
truncated powers, using B_j(x)=x_+^j/j! and B_j*B_k=B_(j+k+1). Interval
densities are expanded at their actual endpoints and convolved at total
mass 1. This reference does not use lower_orthant, rectangle, the archived
rectangle integrator, or the DVV comparator. It agrees in 2,032 rectangle
comparisons and 889 survival comparisons across 127 shape parameter families
with T<=8, up to three selected components, odd and even shapes, zero-width
windows, full selection, and atoms. Counts are raw scheduled comparisons;
some endpoint schedules coincide.

## Exact full count distributions

For N<=n and F_r=E[(N)_r], the finite identity

    E[z^N] = sum_{r=0}^n F_r (z-1)^r/r!

gives precisely the implemented inversion

    P(N=k) = sum_{r=k}^n (-1)^(r-k) F_r/[k!(r-k)!].

The literal subset sum supplies the factorial moments of the declared
partition/Dirichlet assembly model. Its ordered selector sum has the correct
multiplicity: r! times unordered distinct component subsets equals ordered
selection, and removing the selected sizes leaves the coefficient h[n-sum(j)].

The audit computed the count generating polynomial directly: for every
component it assigned a factor z on the window and 1 on both complementary
intervals, then convolved their polynomial densities. It did not use
factorial moments, the subject's rectangle helper, or inversion. For all 66
partitions of n=1,...,8 and both windows, all 132 conditional count laws had
nonnegative coefficients and total mass 1. After applying the declared
assembly weights, every coefficient of all 16 submitted distributions agreed
exactly with this independent calculation. The one-component atom was
treated directly.

Some original assertion families are consistency checks rather than new
ground truth: normalization and reconstruction of the first two moments
follow algebraically from the finite inversion and F_0=1. Nonnegativity and
the new direct-convolution comparison are substantive additional controls.

## KdV independence and termination

The KdV evaluator reads no DVV value, cache, factor, or output. The DVV
function is introduced only after the KdV evaluator has been defined, in a
separate namespace, for final comparison. There is no computational circularity.
Both evaluators still assume standard intersection-number identities; their
agreement is not an independent proof of those identities or the candidate's
geometric interpretation.

Increasing the target tuple's largest degree by one and applying string to
the first-KdV left-hand side yields the target plus exactly the correction
terms appearing in the code. A well-founded rank for valid states is

    (genus, number_of_marks, total_degree-largest_degree), lexicographically.

String lowers the number of marks. Every correction keeps genus and mark
count fixed and strictly raises the largest degree. The genus-reduction term
lowers genus. In a split of a positive boosted tuple, a genus-zero factor
with k selected degrees would require their sum to be k-1, whereas positivity
forces their sum to be at least k. Consequently any split retaining the
parent genus is dimension-invalid and returns immediately. Every nonzero
split therefore lowers genus. The one-point case has no correction terms,
and genus zero is explicit. No valid recursive call can cycle or increase
this rank.

An instrumented execution checked this rank on 10,395 valid recursive edges
(4,402 genus reductions; 4,943 mark reductions; 1,050 largest-degree steps),
covering 5,315 cached states including invalid terminal states. Extended
checks covered 663 stable degree multisets through genus 6, tested dilaton
(not used by the subject's KdV evaluator) on all of them, and matched the
one-point formula through genus 12. They all passed.

## Receipt scope

The original 1,158 assertions comprise raw check invocations, not 1,158
independent theorems or geometric cases. In particular there are 244 KdV/DVV
comparisons over degree multisets: genus 0 through 10 marks (45), genus 1
through 8 marks (66), genus 2 through 6 marks (66), genus 3 through 4 marks
(41), and genus 4 through 3 marks (26). The original one-point closed-form
check is through genus 10. The 16 count distributions cover n=1,...,8 and
only the two stated windows. All source limitations remain necessary.
