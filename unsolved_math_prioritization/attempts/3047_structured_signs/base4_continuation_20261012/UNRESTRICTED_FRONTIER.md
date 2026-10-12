# What remains for the unrestricted partition sign problem

**Subsequent status note (12 October 2026).** The full base-four theorem, pending in the historical body below, has now passed [independent acceptance review](REVIEW_FULL_QUATERNARY.md). Its [complete proof](FULL_QUATERNARY_OBSTRUCTION.md) excludes that entire restricted class, including its binary subfamily, under global coefficient bound one. The earlier pending-status sentence is preserved to make the chronology explicit. The unrestricted problem remains unresolved. This dated update makes no claim of an explicit or sharp coefficient-only cutoff beyond the original combined search result.


## Current mathematical boundary

The original question asks for independent signs \(\epsilon_{m,j}\in\{-1,1\}\), with every constant term fixed at 1, such that
\[
P(q)=\prod_{m\ge1}\left(1+\sum_{j\ge1}\epsilon_{m,j}q^{mj}\right)
\]
has every coefficient in \(\{-1,0,1\}\). No construction or impossibility proof for that unrestricted array has been obtained in the present work.

The completed restricted obstructions concern at most two arbitrary active factors, binary-digit-multiplicative factors, one common arbitrary sign sequence in every factor, and the full ternary-digit-multiplicative class. A full base-four-digit obstruction is separately frozen and under independent acceptance review as this frontier is written. These statements restrict different aspects of the array and must not be substituted for the unrestricted question.

In particular, the ternary and base-four analytic searches use the global desired coefficient bound. Their empty combined frontiers at degrees 59 and 77 are not sharp unconditional coefficient-prefix obstruction degrees. A state failing a necessary Jensen inequality can still have good coefficients through those degrees or beyond.

## 1. Exact unrestricted degree-by-degree formulation

Let
\[
\mathcal D_N=\{(m,j)\in\mathbb N^2:mj\le N\}.
\]
A degree-\(N\) state assigns every sign indexed by \(\mathcal D_N\). It is feasible precisely if the product's coefficients through degree \(N\) have absolute value at most 1. The coefficient conditions only use these finitely many signs.

At degree \(n\), the fresh variables are
\[
\epsilon_{m,n/m},\qquad m\mid n.
\]
There are \(\tau(n)\) of them, where \(\tau\) is the divisor-count function. Set all fresh terms temporarily to zero and let \(A_n\) be the resulting residual coefficient. Each fresh term contributes only its own sign to degree \(n\), multiplying constants from every other factor. Products of two fresh nonconstant terms start in degree \(2n\). Thus every possible new coefficient has the exact form
\[
A_n+\sum_{m\mid n}\epsilon_{m,n/m}. \tag{1}
\]
All fresh assignments remain separately available; different labels can affect later coefficients differently even when their current sum agrees.

Every coefficient has parity \(p(n)\), independently of the chosen signs. Let \(\delta_n=p(n)\bmod2\). The allowed coefficient is 0 when \(\delta_n=0\), and either \(-1\) or \(+1\) when \(\delta_n=1\). The possible fresh sums are exactly
\(-\tau(n),-\tau(n)+2,\ldots,\tau(n)\). Since their parity is fixed, the one-step extension condition is
\[
\boxed{\quad |A_n|\le\tau(n)+\delta_n.\quad} \tag{2}
\]
When (2) holds, retain every fresh sign assignment attaining an allowed value in (1). This gives a complete finite recurrence for the original problem, with no digit-family restriction. It does not prove that every feasible state extends, or that there is a state at every degree.

A genuine unrestricted construction would need an infinite path in this tree, together with a proof that the path never terminates. A genuine finite unrestricted obstruction would be an exact empty frontier for this full tree or an equivalent finite certificate. Neither has been established here.

## 2. The valid compactness statement

The unrestricted sign space is a countable product of finite discrete sets. Equivalently, its degree-ordered assignment tree is finitely branching. Restricting a feasible degree-\(N\) state gives feasible states at every smaller degree.

Consequently, by the elementary infinite-path principle for finitely branching trees, an unrestricted solution exists **if and only if** feasible unrestricted prefixes exist for every degree \(N\). One can prove this directly by successively choosing a first-level branch with descendants at arbitrarily large degrees, then a second-level branch with the same property, and so on. Finitely many branches ensure such a choice at each step.

This principle does not allow a finite search prefix to be declared an infinite solution, and it does not allow absence of solutions in a restricted subtree to imply absence in the full tree. It requires either all unrestricted levels to be nonempty or an explicit finite unrestricted empty level.

For each fixed base, the digit-sign space is also finitely branching and compact. Thus a proved impossibility for that full fixed-base class implies that some finite coefficient-only obstruction exists in that class. The analytic searches above do not identify its sharp degree; the displayed combined search degrees are different quantities.

## 3. Why the fixed-base results do not exhaust arbitrary sign sequences

Binary, ternary, and base-four digit multiplicativity impose exact relations between coefficients. A series can violate all of these relations at once. For example, the prefix
\[
f(z)=1+z+z^2-z^3+z^4-z^5+\cdots
\]
violates:

- binary digit multiplicativity, which would require the coefficient of \(z^3\) to be \(\epsilon_1\epsilon_2=+1\);
- ternary digit multiplicativity, which would require the coefficient of \(z^4\) to be \(\epsilon_1\epsilon_3=-1\);
- base-four digit multiplicativity, which would require the coefficient of \(z^5\) to be \(\epsilon_1\epsilon_4=+1\).

The displayed prefix is only an example of a factor outside those families. It is not asserted to participate in a successful partition product. Its purpose is to show explicitly that the restricted sign models do not cover the original admissible factors.

There is a further subtlety if one considers *all* integer bases. For any fixed finite prefix through degree \(N\), a base \(b>N\) digit block has independent signs at all multiplicity indices occurring in that prefix. Thus the union over unbounded bases can realize every finite sign-array prefix and is dense in the full product space. Even a hypothetical separate impossibility proof for every fixed base would not by itself prove the unrestricted impossibility: a dense union may miss a closed nonempty solution set, and a convergent sequence can leave every fixed restricted family. No uniform finite obstruction for arbitrarily large bases is available here.

## 4. What the general zero theorem does and does not force

Write \(f_m(z)=1+\sum_{j\ge1}\epsilon_{m,j}z^j\), with no digit restriction. A successful product must satisfy
\[
\sum_{m\ge1}\sum_{f_m(\zeta)=0}
(-\log|\zeta|-mt)_+
\le-\frac12\log(1-e^{-2t})\qquad(t>0), \tag{3}
\]
counting analytic zero multiplicities, including repeated roots in different factors. The companion [general zero theorem](../continuation_20261012/INTERIOR_ZERO_BOUND.md) proves convergence, zero persistence, and the inequality.

In particular, for every fixed \(0<\rho<1\), the total number of zeros in \(|z|\le\rho\) among \(f_1,\ldots,f_N\) is at most logarithmic, with
\[
\limsup_{N\to\infty}\frac{Z_\rho(N)}{\log N}
\le\frac1{2\log(1/\rho)}. \tag{4}
\]
This forbids a positive-density family of uniformly interior-zero factors. It leaves several substantial possibilities untouched:

- many factors may be zero-free inside the unit disk;
- factors with inner zeros may be sufficiently sparse;
- their zeros may approach the unit circle with the factor index;
- an arbitrary sign series need not have a digital polynomial factorization whose zeros can be counted from a few discrete defects.

A finite sign prefix alone does not certify a zero of the completed infinite factor. A future argument using prefix information would need a valid persistence estimate, such as a proved contour bound for every admissible tail. One must not import the exact zeros of a truncated polynomial into an arbitrary infinite completion without such an argument.

Zero-free signed series are not known here to be exhausted by geometric or binary-digit products. For example, products of the cyclotomic ternary blocks \(1\pm z^{3^j}+z^{2\cdot3^j}\) give additional zero-free signed series. No classification theorem is assumed.

The fixed positive real radius remains insufficient for a general finite-active-factor impossibility proof: known constructions of signed series allow finitely many arbitrary factors to suppress partition-scale radial growth. Any renewed analytic attack must control the coefficients or enough additional complex-plane information.

## 5. Precisely scoped continuation options

The remaining mathematical goals, rather than further claims from the present results, are:

1. Prove indefinite feasibility in the full recurrence (1)–(2), by a rule or invariant that controls every future residual and preserves an extendible branch; or derive an exact finite obstruction for all its independent signs.
2. Strengthen (3) for arbitrary signed series in a way that excludes the remaining zero-free, sparse-zero, or near-boundary-zero possibilities. A classification result would need to be proved or cited with its exact hypotheses, not inferred from the solved digital examples.
3. Analyze genuinely non-digit correlations in a candidate construction, verifying both that every original factor coefficient is \(\pm1\) and that all output coefficients meet the target. Checking a long finite prefix alone would remain insufficient.
4. Investigate arbitrary finite active sets of size at least three without claiming that the radial argument excludes them. The accepted two-factor result does not extend automatically to this case.

These are distinct open directions. The present work supplies exclusions and necessary conditions, not an infinite construction or a full negative answer.
