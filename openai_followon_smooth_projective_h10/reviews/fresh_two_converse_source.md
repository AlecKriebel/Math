# Fresh direct-source check of the pointwise two-converse dependency

Checkpoint: 2026-10-07 06:28 UTC. Completion estimate: 100% of this assigned
direct-source adversarial pass. This percentage describes the review scope,
not proof of the whole upstream theorem or the H10 claim.

Pinned upstream commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a` in
`/Users/alec/Desktop/math`. No candidate source, upstream source, Git state,
or remote state was modified. No external individual was contacted.

## Target and order of inspection

The initial brief named Family067 and a two-converse without a unique path.
I first read the pinned Goldfeld two-converse source directly, before reading
any earlier audit conclusions. The parent then identified the actual
candidate dependency: `manuscript/main.tex` 228–277 uses the non-CM, full
rational two-torsion branch of the pointwise two-converse. I pivoted to that
source. Goldfeld is only a comparison and is not used as a substitute
dependency.

The required upstream root is:

`preprints/A-pointwise-2-converse-for-elliptic-curves-with-rational-two-torsion-September-24-2026/build/sections/`.

Directly inspected at the pinned commit:

- `cyclotomic.tex`, all 788 lines.
- `coefficients.tex` 1–230 and 530–920, concentrating on 644–886.
- `pointwise.tex` 1–125 and 551–840, concentrating on the nonempty split witness.

For comparison, directly inspected all of Goldfeld's `04-cyclotomic.tex`,
`05-coefficients.tex`, `06-traces.tex`, and `02-binary-algebra.tex`, and its
exact cyclotomic theorem hypotheses in `01-arithmetic-transfer.tex`.
Only after these direct reads did I compare the reconstructable derivations
in `agent_notes/coefficient_trace_audit.md`.

## Exact scope and outcome

No substantive mathematical gap was located in the cyclotomic specialization,
integer coefficient normalization, integral trace/level interface, or deeper
split-witness mechanism checked here. The source has the relevant restrictions
in place: odd good newly added primes; a fixed curve before auxiliary families;
fixed sign and local squareclasses; full Selmer corank, rather than Mordell–Weil
rank, at the unknown base; and finite precision chosen after the finite
operator/division requirements. This is a scoped outcome, not certification
of every analytic and ring-class input of the upstream theorem.

## Cyclotomic checks

1. `cyclotomic.tex` 65–114 explicitly distinguishes the completed localization
   `O` from the rational power-series ring. Central evaluation is never made
   as a map `O -> Q_2`. Characterwise membership in `Lambda[1/2]`, together
   with pre-character integrality in `O[G]`, yields the original uniform
   power-of-two denominator coefficientwise. Rational Fourier inversion has
   a factor `|G|`, but intersection occurs after the already fixed integral
   bound, so this factor is not charged to the final bound.
2. The positive cone is the ordinary-real cone (186–243), and retains the
   invariant real line. The residual growth argument (245–311) only needs
   bounded support/class-group terms for each fixed ramification set, then
   kills them by inverting `t`; it does not claim a support-independent
   generator count. The resulting rank-two freeness introduces no growing
   determinant index.
3. The coefficient push is integral and unaveraged (341–361). Smoothing
   parameters vary with tame conductor but have fixed central valuations
   (363–389). Reciprocity (391–421) uses the fixed modular-form period line
   and tracks every varying unused Euler factor. I did not replace this by
   a varying-newform period comparison.
4. The unused-prime convention correction is already present in the pinned
   source (574–595). Direct algebra gives
   `P(Z) - Z^2 P(Z^-1) = ((q-1)/q)(1-Z^2)`.
   Since `q` is odd and the denominators are units in `O[G]`, the ratio is
   `1 mod 2`; the correction `1 + ((r-1)/2)(1+g_q)` is integral before
   character evaluation, equals `1` on active characters, and equals `r`
   on unused characters. At the latter central values `Z = +/-1`, it
   equals `1`. Thus no two-denominator is charged per prime.
5. Central specialization (629–748) requires Selmer corank zero. Put
   `i = length(L_2/J)`. The free global-line valuation is
   `v(exp* z) - i + O(1)`, while the degree-two torsion length is
   `s - i + sum local torsion lengths + O(1)`. In the inverse determinant
   the latter is subtracted, so `i` cancels. At unused good primes local
   torsion cancels reciprocity's point-count factors; active primes supply
   exactly `2w(h)`. These include the old factors of the base. If the central
   value vanishes, the class lands in the zero rational finite Selmer group.
   Constant rational cohomology rank then specializes the same determinant.
6. The missing-vertex proof (763–788) applies the forward theorem at the
   nonzero vertices only. A fixed precision exceeding the uniform valuation
   bound gives a nonzero companion to the zero address. No injective family
   parameterization is assumed: a character trivial on the actual universal
   image already gives the conclusion (181–184).

## Coefficient, trace, and level checks

The even same-filter comparison in `coefficients.tex` 82–135 is a comparison
of coefficient functionals on the whole eigenspace, not merely one chosen
eigenvector. The local squareclass condition permits phase removal and
makes nonzero squarefree valuations integers. This integer property is
used by the extra-depth and unary-divisibility steps; it is not inferred
from membership in a ramified valuation ring.

For `b_0=1`, `b_1=a-kappa`, `b_(s+1)=a b_s-p b_(s-1)`, I independently
checked the two square-shell assertions used at 700–761:

- If `kappa=0`, `b_s-b_(s-1)` is odd.
- If `kappa=+/-1` and `a=p+1 mod 4`, every
  `(b_(s+1)-b_s)/2` has the same residue mod 2.

The truncated odd-stage estimate at 720–734 pays every fixed division on
a bounded weight range; the coarse global estimate pays the remaining
indices. Integral recurrence multipliers keep errors in the same precision
ideal through arbitrarily many square-shell iterations. This gives an actual
integral form at that stage without asserting an infinite-precision lift.

The trace module at 789–849 is generated by integral Fourier expansions and
their good-Hecke/diamond translates. Injective finite coefficient evaluation
places it inside a finite free module; hence it is finite and closed. On a
fixed finite-dimensional eigensystem span, sufficiently accurate simultaneous
Frobenius approximation preserves this lattice, including any fixed spectral
projection denominators. No saturation is needed.

I independently checked the two external local hypotheses against primary
texts:

- [James–Ono, Proposition 3, p. 4](https://uva.theopenscholar.com/files/ken-ono/files/043.pdf)
  confirms that these exact half-integral-weight `U_p` and `V_p` definitions
  land at level `Mp`, with character multiplied by `(4p/.)`. Thus a fresh
  odd prime has exponent one and primitive ramified quadratic character.
- [Carayol, Theorem (A), §§0.3–0.7](https://www.numdam.org/article/ASENS_1986_4_19_3_409_0.pdf)
  supplies local compatibility at every finite odd `p` for coefficient prime
  `2`, in weight two over `Q`. The additional finite discrete-series
  hypothesis belongs to even field degree and is not a restriction here.

Conductor exponent one plus ramified determinant excludes monodromy and
forces an unramified line and a ramified quadratic line. In the arithmetic
normalization, the `U_p` eigenvalue is the unramified Frobenius eigenvalue
`lambda`. With `rho(tau)=diag(1,-1)` and `rho(phi)=diag(lambda,mu)`, the
two inertia differences have lower-right contributions `-2z mu` and `-2z`.
The identity at 851–885 is therefore `-2z lambda mu` on both sides.
On genuinely unramified old multiplicity spaces both differences vanish;
the proof does not incorrectly make their `U_p` scalar.

## The full-two-torsion split witness

For `pointwise.tex` 585–840, assume the ordinary all-`K`-split minimum has no
nonempty witness. Integer valuations then give
`v(a(D)) >= omega(D)+1` at every such nonempty allowed squarefree `D`.

The source's mod-8 calculation needs the unraised unary term treated
separately. Let `R=theta B_p`, `C_0=theta B_p[1] Theta_empty`,
`C_p=theta B_p[p] Theta_p`, and `f=(R-C_0-C_p)/2`.
On the ramified summands,
`U_p^2 t(phi)=U_p^3+d(phi)U_p` follows from
`lambda^2(lambda+mu)=lambda^3+lambda^2 mu`. On `C_0`, use the ordinary
good-prime coefficient identity. Both yield
`(t(phi) f)[p^2] = f[p^3] + (d(phi) f)[p]`.

The determinant cancellation at 683–684 remains valid after division:
if its eigenvalues on `R,C_p` and `C_0` are `delta_p,delta_0`, then
`d(phi) f = delta_p f + ((delta_p-delta_0)/2) C_0`.
The quotient of their characters is quadratic, so the divided difference
is integral. Also `f[p]=0 mod 2`; `Theta_empty[p]=0`, and its product with
theta has an even coefficient at nonsquare `p`, so `C_0[p]` is even.
Both terms vanish mod 2. This is the denominator check behind the source's
short statement and agrees with the later independently reconstructable
audit note.

A fresh prime matching `phi_p` on the trace and support tests is split in
`K`, and `pp'` is square at every old support place even if `p` alone fails
the total filter. The extra depth kills the left coefficient. Direct
recurrence/subtraction gives

`H_p[p^3] = unit * (a-1)(a-p-1)/4`.

Full rational two-torsion makes `a` even. Its vanishing mod 2 forces
`a=p+1 mod 8`. This justifies the next integral division by 4. For the
all-square case the mod-8 recurrence gives `b_s=p^s mod 8`; in the other
cases an extra-depth scalar or at least two inert factors supplies the
needed second power of two. Leading multipliers are not divided by and
may be zero.

The deeper bit uses only contractions with nonempty output. Two fresh
`K`-split traces vanish on the entire reduced orbit, so elementary
factorization and primary isolation hold. Finally, fresh ramification
makes `K` independent of `Q(E[8])`. An inert prime trivial on `E[8]` has
`p=1 mod 8` and twisted trace `a=-2 mod 8`; on the empty deeper form,
the squared trace at coefficient 1 is
`unit * (a-1-p)/4 = 1 mod 2`.
Its square lies in `G_K` and is trivial on every rational quadratic
support character. A fresh matching split prime is therefore an allowed
nonempty witness.

## Limits of this pass

The internal specialization, quantifier, local-operator, and integer-division
checks above found no unresolved inference in the assigned scope. I did not
independently reprove Kato's global divisibility, the complete Nekovar duality
formalism, Waldspurger's packet theorem, the full weighted-theta bridge, the
analytic rough nonvanishing theorem, or the ring-class construction. Their
applications are explicit in the source; the parent assigned those other
arithmetic components separately. This report must not be promoted to a
verification of those unreviewed components or of the complete unrestricted
Goldfeld theorem.
