# Independent adversarial report: Gamma marking and all mesoscopic rates

Audit UTC: 2026-10-15 06:20:49. Assigned-family completion: **100%**.
Research target: frozen PR218/problem30006020 candidate, supplied head
`dc457c741c779fbf90fbfdcdc73f750b3716f561`.
Author: independent mathematical subagent
`/root/pr218_gamma_mesoscopic_adversary_20261015`.

**Finding:** no substantive correctness defect was found in the candidate's
Gamma marking, normalization, topology, endpoint, factorial-moment, or joint
moment arguments. The mesoscopic model proof covers every sequence
`q_n -> infinity`, `q_n/n -> 0`; it does not require either convergence to have
a specified rate. The actual-law moment transfer is valid with the stated
uniform latent density comparison and polynomial bad-event bounds. Those
conditions must be retained; total variation alone would not establish the
moment assertions.

The strongest result independently established in this audit is the model PPP
limit with all fixed joint compact-window count moments, together with a
precise sufficient transfer lemma. No claim about novelty or priority is made.

## Independence and scope

Before sealing `INDEPENDENT_DERIVATION.md`, I read only the frozen submitted
candidate, project instructions, and the read-only PDF skill. Its initial
SHA256 is
`539532ad88543f696acf0dc83696268fc23e9c4c51d122f13b351d4db2eeebad`.
I did not read an old independent review, checker, final disposition, sibling
report, or parent reconstruction/conclusion. After sealing, I downloaded the
full two primary papers into ignored `private_reading/`, extracted their text,
and visually inspected the relevant displayed formulas. No outside person
was contacted, and no Git index, branch, ref, commit, push, or provider state
was changed.

This family checks the probability argument and the requirements for its
geometric transfer. It does not reprove the credited large-genus intersection
number or geometric counting theorems from first principles, nor exhaustively
audit the identification of the principal-stratum sampling ensemble. The
parent's independent geometric/source families must cover that identification.

## 1. Exact model and falsifiable success criteria

The assembly has weights `a_j=zeta(2j)/(2j)` and coefficient `h_n` of
`H(z)=exp(sum a_j z^j)`. A selected component of size j receives an independent
`Gamma(2j,rate 1)` variable Y. The marks are divided by their common sum T.
For `q=ns`, the normalized scaled point is `nY/(qT)`.

The exact claim tested is convergence of this point process in the vague
topology on `(0,infinity)` to intensity `dx/(2x)`, and convergence of every
fixed joint count moment on finitely many compact windows. The central
adversarial targets were a hidden `q >> log n` assumption, amplification of
rare Gamma tails by `h_(n-j)/h_n` near n, loss of tightness under random
dilation, missing uniform integrability, or a missing actual-law hypothesis.

Boundary exclusions are essential: no tested compact touches zero or infinity;
the theorem assumes both `q -> infinity` and `q/n -> 0`; and the surface
sampling limits remain iterated in the order N then g. A microscopic q bounded
or a macroscopic q/n bounded below is not covered by this proof.

## 2. Uniform coefficient control and unmarked process

Factoring `H(z)=(1-z)^(-1/2)B(z)` with B analytic and nonzero on `|z|<4`
gives `h_n ~ sqrt(2/pi)/sqrt(n)`. Splitting the coefficient convolution at
`sqrt(n)` provides a direct proof. In particular,

    R(n,r) := h_(n-r)/h_n
       <= C sqrt((n+1)/(n-r+1)) <= C sqrt(n+1),

and `R(n,r) -> 1` uniformly for `r=o(n)`.

Removing specified components from the exponential assembly gives the exact
factorial identity (19). Each fixed joint factorial moment of compact
q-window counts selects total size `O(q)=o(n)`, so the ratio tends uniformly to
one. Harmonic summation gives the Poisson window means. Joint count laws are
identified by their independent Poisson moments; local first-moment bounds
give point-process tightness on compact exhaustion. The interval endpoints
have zero limiting intensity. Thus the unmarked PPP assertion is justified.

## 3. Gamma test error in all three ranges

For a nonnegative globally Lipschitz f supported in `[a,b]`, the candidate's
expected error is bounded by

    sum_(j=1)^n a_j R(n,j)
       E |f(Y_j/(2q))-f(j/q)|.

An explicit bound, with constants depending on f,a,b but not q,n, is

    C q^(-1/2)
    + C log(q+2) exp(-a(1-log 2)q)
    + C sum_(j>2bq) exp(-c j)/j
    + C sqrt(n+1) exp(-c n/2),

where `c=2 log(3/2)-1/2=0.3109302162... > 0`.

- For `aq/2 <= j <= 2bq`, `R(n,j)` is bounded eventually, and Gamma variance
  gives `E|Y/(2q)-j/q| <= sqrt(2j)/(2q)`. Summing with `a_j<=C/j` gives the
  first term.
- For `j<aq/2`, the unmarked f value is zero. Chernoff parameter `+1/2`
  gives `P(Y>=2aq)<=exp(-aq)2^(2j)` and hence the second term.
- For `j>2bq`, Chernoff parameter `-1/2` gives
  `P(Y<=2bq)<=exp(bq)(3/2)^(-2j)<=exp(-cj)`. Below `n/2` the ratio is bounded;
  above `n/2` its possible `sqrt(n)` amplification is absorbed by the last
  exponential term. One may split the sum into these two ranges to avoid
  counting the last term twice; the displayed expression is an upper bound.

Every term vanishes for every permitted sequence q. In particular, summing a
first-moment error rather than a union bound over all K components avoids the
unjustified rate `q/log n -> infinity`. Nonnegative compact Lipschitz tests
determine the Laplace functional; their approximation and the local mass
bounds also establish the required local tightness.

## 4. Random normalization and window independence

Conditional on every composition, `T~Gamma(2n,1)`, so `U=T/(2n)->1` in
probability. No independence of T and the unnormalized marked process is
required. The map `(mu,d) -> D_d mu`, moving each atom x to dx, is jointly
continuous for `d>0` in the vague topology. To check it, supports of the tests
`f(d_n x)` lie in one compact set when `d_n->d>0`; the tests converge uniformly
there, and vague convergence bounds the corresponding positive masses by a
continuous envelope. Slutsky then proves the normalized process limit.

The limiting intensity is diffuse, so fixed window counts are almost surely
continuous observables of the limiting process. Disjoint-window independence
is consequently preserved in the PPP limit. The source window has limiting
mean and variance `(log 2)/2` and zero-count probability `exp(-log 2/2)=1/sqrt(2)`.
The factor `2n` in the Gamma total is consistent with normalized mean part
size `j/n`; no microscopic scale substitution is used.
The candidate explicitly flags the OWR report's printed microscopic factor
`4g-4`, which differs from the exact DL total `6g-6`. This audit does not
silently correct that printed microscopic assertion or claim to recover it;
the mesoscopic window law here uses the exact DL mixture and is unchanged.

## 5. Marked factorial moments and all normalized joint moments

Let `p_j=P(Y_j/(2q) in [a,b])`, `w_j=a_j p_j`. The same three ranges give
`sum w_j <= C_(a,b)` uniformly. Independent marks and component removal give

    E(M)_r = sum_(j_1+...+j_r<=n)
          R(n,j_1+...+j_r) product_i w_(j_i).

Repeated integer part sizes are allowed: the falling factorial counts
distinct components, so the formula has no missing diagonal correction.
For selected total at most `n/2`, the coefficient ratio is bounded. For a
larger total, some selected size exceeds `n/(2r)`. For each fixed r,
`q=o(n)` eventually puts that size above `2bq`; its mark probability is at
most `exp(-c n/(2r))`. Even the crude bound

    C_r sqrt(n+1) exp(-c n/(2r)) (log(n+1))^r

then vanishes. This proves all fixed factorial and ordinary marked moments
are uniformly bounded. The eventual threshold may depend on r; the claim
does not assert uniformity for r growing with n.

On `1/2<=U<=2`, normalized `[a,b]` counts are bounded by marked `[a/2,2b]`
counts. The complement contributes at most `2 n^r exp(-c_0 n)`, where one may
take `c_0=min(2log 2-1,2-2log 2)>0`, because `K<=n` and Gamma Chernoff bounds
apply. Each fixed normalized count moment is uniformly bounded. To infer
convergence at order r, the bound at order r+1 supplies uniform integrability;
the proof is not relying on a same-order bound. A mixed monomial of degree r
is bounded by the r-th power of the count on the finite union, and its order
r+1 bound proves convergence of every mixed moment as well.

## 6. Actual-law transfer and primary-source checks

The transfer needs: a polynomial bad-event probability; actual and model
logarithmic K-moment bounds; and a uniform multiplicative density ratio
`1+o(1)` for the actual good-event law versus the cutoff model law on the
latent space. The density comparison must include all compositions and their
Dirichlet marks. These conditions imply that every bad r-th count moment is
`o(1)` by Cauchy-Schwarz, while the uniform density error multiplies a bounded
good-event model moment. They also handle observations depending on n.

For `t=11/10`, the cutoff Chernoff exponent is

    eta = (3/5)log(11/10)-1/20
        = 0.00718610788259... > 1/220.

A fixed `E t^K=O(n^alpha)` bound implies `E K^r=O((log n)^r)` by summing
the exponentially decreasing tail above `A log n`, for sufficiently large A.
The graph excess at the chosen cutoff is
`O((log g)^25 g^(-1+(3/5)log 2))`, with positive decay exponent
`1-(3/5)log 2=0.5841116916...`. Thus no quantitative rate for the uniform
coefficient approximation is needed once the bounded model moment is known.

Primary-source checks, with full PDFs stored privately:

- [DL, final JEMS paper](https://ems.press/content/serial-article-files/51451?nt=1):
  PDF pp.5, 13-14 describe the fixed-genus area-law and polynomial-mixture
  ingredients. Visually checked PDF pp.24-25 show (6.1), (6.2), the
  height-summed density (6.3), and the monomials `x_i^(2j_i-1)/(2j_i)!` with
  `sum j_i=3g-3`. These support Gamma shapes `2j_i` and total `6g-6`.
  The candidate's prefactor matches the displayed monomial expansion.
  Independently dividing consecutive prefactors gives its equation (8), and
  summing logarithms gives the needed `O((log g)^2/g)` prefactor variation.
- [DGZZ, final Inventiones paper](https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf):
  Theorem 1.7 identifies the cylinder-count law. Visually checked PDF p.15
  gives Theorem 1.12 for `|t|<8/7`, so `t=11/10` is valid. Visually checked
  PDF p.83 gives Theorem 5.2's uniform low-k relative excess with factor `2^k`
  for `k<=log g/log(9/4)`. The proposed `0.6log(2n)` cutoff lies within this
  range for large g. The proof therefore need not invoke the stronger-looking
  unrestricted Corollary 5.3; no conclusion here relies on that corollary.

For the final fixed-genus `N -> infinity` window-count step, the argument
requires endpoint-nullness and bounded K at that genus. All at-least-two-part
Dirichlet mixtures have continuous coordinate marginals. The one-part atom
is at area one, outside the shrinking source window for large g. A fixed-genus
`K<=3g-3` bound also transfers fixed moments before the outer g limit. This
does not imply a diagonal finite-square-count theorem.

## 7. Fresh reproducible finite-n diagnostic

`diagnostic.py` uses only the standard library and has no dependency on an
earlier checker. It computes h by its differential recurrence, independently
enumerates integer partitions for `n<=12`, and compares factorial counts
against component removal for orders 1,2,3. The largest observed discrepancy
was `2.22e-16`. It then evaluates expected marked and normalized `[1,2]`
counts using integer-shape Gamma/Poisson and Beta/binomial identities, with
stable probability recurrences, for `n=64,...,16384` and three scale families.
The output and its rounding limitations are recorded in
`diagnostic_results.json`; these are floating-point diagnostics, not validated
interval computations and not an asymptotic proof.

At `n=16384`, the normalized mean is about `0.3485441` for `q=sqrt(n)`, versus
the limit `0.3465736`. For `q=log log(n+exp(e))` it is about `0.3717982` while
q is only `2.27`; for `q=n/log log(n+exp(e))` it is about `0.6078235` while
q/n is still `0.44`. The latter two examples deliberately illustrate slow
approach to the hypotheses. Their finite-n discrepancy is not a
counterexample to a theorem that asserts no convergence rate.

## Exact remaining gap and disposition within this family

There is **no unresolved model-probability gap** found in the assigned route.
All-rate Gamma marking, random normalization, compact-window independence,
and every fixed joint moment are independently justified above. The
actual-law conclusion follows if the candidate's credited mixture and
uniform latent-density identifications match the stated geometric ensemble;
the source range and numerical constants needed for its tail and moment
transfer have been verified. Exhaustive geometric ensemble validation and
novelty/priority remain outside this independent family's scope. No general
PR disposition is assigned here.
