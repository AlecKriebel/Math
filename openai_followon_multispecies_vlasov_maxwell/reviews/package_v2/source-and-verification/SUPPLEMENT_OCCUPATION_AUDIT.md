# Independent occupation, selection, and bootstrap audit

Audit timestamp: 2026-10-07T04:23:19Z (2026-10-06 in America/Los_Angeles).
Upstream input: pinned family 362 manuscript, commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.

This audit is a check of a distinct mechanism: residence time, angular occupation,
exact selected-range exponents, and simultaneous momentum closure. It is **not**
an unconditional proof of global relativistic Vlasov--Maxwell existence, nor a
certification of the upstream formalization. The decisive force identity and its
multispecies normalization remain an explicitly external input to this audit.

Checkpoint estimate for the full original research objective: mathematical
resolution 5%; publication package 0%. These numbers are planning judgments, not
evidence. The strongest result below is a conditional, checkable finite-species
extension of the occupation-and-closure mechanism. No publication or tracker
operation was performed.

## Files actually read

Paths in the following table are relative to the pinned manuscript's
`build/sections` directory.

| File | SHA-256 | Principal passages |
| --- | --- | --- |
| setup.tex | 40a7d4abe6fa5d9dc96a6ffd689e602a10bb7a1cf3bd9fd8f0caa70cf72a9cf7 | 27--46, 69--114 |
| occupation.tex | c9bd0387061b620018c710dd9f660564adf8c38ff2385ee134923f86bf8d3307 | 64--122, 145--179, 203--300, 302--416 |
| direct.tex | aed0cd43a04c66b5ffb4bb30de2377dafa1eaa58a6c5e7d0c40865662f9e6de1 | 37--136, 138--243, 245--428 |
| direction.tex | aeab95505df9a9d2b8bca153832ea69039eb0fa078788775ea15e34fb8531432 | 22--209, 222--371 |
| selection.tex | 1ece8e662bff978906fbc1ddc578ea09a89322accee598d043aa3a7403583445 | 40--103, 105--270, 272--488 |
| closure.tex | 499230223647c95c6e9d536c78e9cd5dd098a011d9213b733daaab3d8bba8e89 | 8--87 |
| retarded.tex | eedf365c0be2cefacecc93c2825b4991ccad1d32826d83aa24eb4b63ccf37be2 | 19--87, 103--145, 342--428 |
| cancellation.tex | 6b615a3b4ba0fbb6d04ea2e88b441dabdd51f6b33fc976b23407413fc9ae162a | 10--102, 113--270, 278--339 |

Also read `AGENTS.md` and `lean/docs/362.md`. No Lean build was run by this
auditor. The scope prose in `362.md` is a claim, not validation evidence.

## Conditional proposition being verified

Let there be a fixed finite set of species, with positive masses `m_a` and real
charges `e_a`. Use units with light speed and Maxwell coupling normalized as in
the upstream manuscript. Let `p_a` be physical momentum, and write

\[
 W_a=p_a/m_a,\quad q(W)=\sqrt{1+|W|^2},\quad
 u(W)=W/q(W),\quad c_a=e_a/m_a,\qquad
 g_a(t,x,W)=m_a^3 f_a(t,x,m_aW).
\]

On a compact interval of classical existence assume compact phase support,
phase-volume preservation for every species, nonnegativity, the positive energy
identity

\[
 \mathcal H_0=\int\frac{|E|^2+|B|^2}{2}\,dx
       +\sum_a m_a\int q(W)g_a\,dx\,dW,
\]

and its backward-cone inequality with particle term
`sum_a m_a q(W) (1-n.u(W)) g_a`. Assume the signed source/receiver pair identity
and the direct, projected, and cutoff majorants from the upstream manuscript
hold for each pair, with the coefficient factors recorded below.

Then the upstream occupation, angular-direction, selected-range, and continuity
closure arguments imply one signed increment estimate for **all** species
simultaneously:

\[
 |W_a(t_2)-W_a(t_1)|\le MP\sqrt{t_2-t_1}
       +A(t_2-t_1)P^2\log(2+P)/w,
\]

for each supported receiver of any species with `w/8 <= q(W_a) <= 8w` on the
entire interval, where `P >= 1024 max_{a,z,t} q(W_a(t,z))` is dyadic. The
constants can depend on the fixed finite species list and data, but not on the
compact endpoint or `P`. With the matching bounded-momentum continuation
theorem this excludes finite-time momentum blowup. This proposition deliberately
does not replace the force-identity assumption with an unverified assertion.

## Normalization and charge bookkeeping

The normalized phase equations are

\[
 \dot Y_a=u(W_a),\qquad
 \dot W_a=c_a(E+u(W_a)\times B).
\]

The divergence of the normalized phase vector field is zero, since multiplying
the Lorentz force by the constant `c_a` does not change the identity
`div_W(u x B)=0`. Maxwell's charge and current are

\[
 \rho=\sum_a e_a\int g_a\,dW,\qquad
 j=\sum_a e_a\int u(W)g_a\,dW.
\]

Kinetic work is `m_a q'(W_a)=m_a c_a u.E=e_a u.E`, precisely canceling the
Maxwell work term. No signed energy sum is used. In particular

\[
 \int q g_b\le \mathcal H_0/m_b,\qquad
 \|g_b\|_\infty=m_b^3\|f_b(0)\|_\infty.
\]

For receiver `a` and source `b`, the retarded field kernel gets source factor
`e_b`; receiver normalized force gets factor `c_a`. Thus the entire signed pair
kernel, its transport piece, primitive, and central/receiver residual carry
`c_a e_b`. The source acceleration inside the representation is

\[
 b_b=u_b'=c_b q_b^{-1}(I-u_b\otimes u_b)(E+u_b\times B).
\]

Hence its direct source-field majorants and source-cutoff derivative majorants
also have a factor `|c_b|`. The receiver term contains
`a_t=(I-a\otimes a)K_a/q_a`, with `K_a=W_a'` the **full coupled acceleration**;
there is no additional `c_a` to insert into this formula. It is multiplied
externally by `c_a e_b`. Fixed factors never need to be small. Every majorant
constant can depend on their finite maximum or finite sum, and final `M,A`
are chosen after those constants. This avoids an erroneous independent
one-species bootstrap.

## Occupation checks

The exact geometric identities in occupation.tex:66--71 contain only the common
normalized velocity law. The same lower angle deficits `theta >= 1/p`,
`phi >= c/w`, `sigma >= c/min(p,w)` hold for every pair. Phase-density cap bounds
hold source by source with `||g_b||_infinity`.

For fixed source time `s`, the spatial change `(t,n) -> X_a(t)-(t-s)n` remains
injective and has Jacobian `r^2 D`. It uses only receiver timelikeness. Passing
to species `b` initial labels gives

\[
 \mathsf M_{ab}=\int g_{b,0}(z)\,dz\int_{\text{hits}}ds.
\]

The retarded branch has `dt/ds=d/D` and `ds/dt=D/d`. Thus the crude bounds become
`M_ab <= C_b max(I,h)/p` and
`M_ab <= C_b I phi^2/theta^2`, with fixed constants. The collision-null-set
argument in retarded.tex:412--419 is sound: a time grid of mesh `zeta` covers
colliding labels by `O(1/zeta)` spatial balls of volume `O(zeta^3)`, giving
label mass `O(zeta^2)`. It works separately for each source species against
each receiver species; it does not assume independent charges.

Assume the signed bootstrap **for every species**. With

\[
 \lambda^{-1/2}=C_1\frac Pm
       \left(\frac M\omega+\sqrt{\frac{AL}\omega}\right),
 \qquad m=\min(p,w),
\]

the stopping argument bounds each source and receiver momentum increment on a
cell by `epsilon m omega`, independent of its force law, because it uses the
common bootstrap directly. This proves all stability assertions in
occupation.tex:223--250 with one `C_1`. Actual bins have fixed projected
relative speed at least `c omega` on a cell, so residence time is at most
`C h (1+phi/omega)`. Their label mass at any common time is at most `C_b/p`.
This gives the stable-cell bound (occupation.tex:254--300).

Define the two energy indicators exactly as in occupation.tex:319--340 but with
source `g_b` and receiver `X_a`. Their overlap is bounded in `p,phi` for each
`b`. For any fixed receiver,

\[
 \sum_{b,p,\phi}\mathcal E^{ab}_{p\phi}
       \le C\sum_b\mathcal H_0/m_b<\infty.
\]

The enlarged source-time interval `J*` has length `O(I)` independent of species
because all speeds are below one and the bin's `r/h` constant depends only on
the fixed horizon. Cell averaging and the direct spatial hit estimate give
the refined occupation bound without adding an angular logarithm. There is no
use of neutrality.

## Direction counts and their dependency order

The direction proof uses the signed bootstrap, baseline occupation, direct
force estimates, and projected pair identities; it does **not** use the
improved direction-based occupation estimate. See direction.tex:73--82,
135--151. This excludes that particular circularity.

On a receiver of species `a`, `w xi_t = Pi K_a` remains exact. Sum the pairwise
identities over `b` before bounding. The projected receiver coefficient becomes
`C_species L^2/w`; the absolute force remains
`C_species sqrt(w) [P sqrt(I)+(M+sqrt(A)) I S(w)]`. Therefore the receiver terms
cost `C_species(M,A) sqrt(w) L^3`. The weight derivatives cost
`C_species L^2 N_c`. Disjoint direction intervals share one upper time length
`I`, so the nonnegative bulk terms do not incur an erroneous extra factor
`N_c`. Absorbing the latter weight cost uses
`w delta >= P^(6/25)` and gives the same count `C_species(M,A) L^6/delta`.

The improved occupation proof then subdivides source and receiver directions
separately. Bad hits straddling a receiver boundary have source-time duration
`O(h)` per boundary; the proof never assumes `dt/ds` is bounded there. For good
hits, equal-time separation is `O(h phi)` and projected relative speed is
`Omega(phi)` on each common refinement interval. The refinement count is the
sum, not the product, of the two partition counts. These features survive for
opposite accelerations and arbitrarily different fixed masses.

In the window `p,w >= P^.7`, `j^(-.49) <= phi <= j^(-.16)` for both momenta,
the bound `phi^(-.16) >= P^(56/3125)` absorbs
`C_species(M,A) L^7` into the final exponent `beta=29/25`. Consequently the
improved-occupation constant is independent of `M,A` after enlarging the
threshold `P_*(M,A, species)`. This independence is essential for closure and
was preserved, not assumed.

## Selected-range rational audit

The selection uses the exact representative entries, with occupation constants
outside the definition of `M_*`. Fixed species constants enlarge majorant
constants, rather than changing the power inequalities. Set

\[
 p=P^{1-\alpha},\quad w=P^z,\quad c=1-z,\quad
 p\theta=P^b,\quad\phi=P^{-y},\quad h=P^{-H},
 \quad\Delta=10^{-5}(\alpha+b+y+H).
\]

The manuscript's near inequality is exactly
`2 alpha + H/2 + 2y < z+Delta`. Pure energy far selection gives
`b < H/2-alpha+Delta` if `H <= 2c`, otherwise
`b < H-c-alpha+Delta`. These imply `Delta < (4/99995)z < .001z`.
Unsafe receiver coefficients imply simultaneously

\[
 b>2H/3+z/6-\Delta/3,\qquad
 b<H+2y-z/2+\Delta.
\]

The case `H <= 2c` contradicts `H+z+6alpha < 8Delta`; the other case implies
`H > z/2+3(alpha+c)-4Delta`. This forces actual velocity separation before
any constants are absorbed into powers of `P`.

Baseline occupation then yields the improved window as claimed. In particular
`H < .8076z` and `alpha+c < .105z`, hence `z>200/221`, `1-alpha>.895`.
The angle satisfies
`.16 max(z,1-alpha) < y < .49 min(z,1-alpha)`.

After applying improved occupation, compare its far inequality with the first
unsafe inequality. Keeping the exact rational constants gives

\[
 \beta y>H/3+z/3+2\min(\alpha,c)-8\Delta/3,
 \qquad
 \beta y<29z/50-29H/100+(29/50)\Delta.
\]

Since `Delta <= z/1000`, they force
`H/z < 37487/93500`. Earlier inequalities force `H/z > 62/125`.
The strictly positive contradiction margin is exactly `8889/93500`.
The executable rational certificate in `checks/occupation_bootstrap` checks
these values and the manuscript's intervening rounding claims. This is a
check of the algebra, not a numerical simulation or proof of the kinetic PDE.

I checked the spatial-transition balancing in selection.tex:324--385. The
common multiplier cutoff cancellation is essential; its proof does not cancel
different kernels. `R` is independent of `theta,h` at the point where the
geometric tails are summed. The time-weight bound for `h>I` in
selection.tex:421--440 follows from near selection and
`P theta sqrt(h)<W^{-1}`, and has positive radial/angular exponents. No extra
time-piece count or logarithm was identified in these passages.

## Simultaneous closure and continuation implication

Take the maximum of the normalized momentum over the finite union of species
label sets. Assuming all pairwise majorants, the weighted force constant
`C_eta` is fixed by species and initial data. Choose in order `eta`, then
`M>=max(32,8C_eta)`, then
`A>=max(1,16C_eta M,256C_eta^2)`, then the large-`P` threshold. Edge restoration
uses the same receiver's signed increments, not an absolute-force bound. It
gives the strict half-bound for all species at once.

The bootstrap set is closed under truncation; it is relatively open because on
the fixed compact solution interval the full coupled normalized force is
uniformly bounded across the **finite** species set and compact labels. That
temporary bound does not enter `M,A,P0`. Thus there is no failure of endpoint
uniformity in closure.tex:61--87.

Let `Q(t)=max_{a,z} q(W_a(t,z))`. If momentum were unbounded at finite time,
choose its first dyadic hits `t_n` and a maximizing species-label at each hit.
The label's last time `s_n` at half-energy satisfies `s_n>=t_(n-1)` regardless
of whether the maximizing species changes with `n`. It remains within the
required energy range on `[s_n,t_n]`. The simultaneous signed estimate gives
`t_n-t_(n-1) >= c/log(2+1024*2^n)`. The harmonic divergence excludes finite
time. Bounded normalized momentum is equivalent to bounded physical momentum
for a fixed finite family with positive masses.

## Boundary cases and limits of this audit

* Equal masses and charges `+1,-1`: relative acceleration can change sign,
  but occupation uses the simultaneous increments and timelike geometry, so
  no sign appears in its proof. Pair force signs must still be independently
  checked in the exact identity.
* Zero charge: `W_a'=0`; such receivers obey the estimate trivially. Such
  sources have zero Maxwell contribution. Their positive kinetic energy and
  support remain legitimate, and they may be included in `Q` without issue.
* Coinciding species: each positive phase density can be handled separately;
  bounded overlap in species only costs the fixed species count. No distinct
  trajectories or distinct charges are required.
* One species: constants reduce to the upstream normalized ones when
  `m=e=1`; this consistency check does not independently certify upstream.
* Extreme fixed positive mass ratios: `1/m_b`, `|c_b|`, and normalized initial
  `L^infinity` norms can be large. Every constant is allowed to depend on
  these fixed values. There is no uniform massless limit and none is claimed.
* No neutrality is used in occupation, cone budgets, coefficient selection,
  closure, or momentum doubling. Initial field compatibility and continuation
  remain separate inputs requiring audit.

No counterexample to the audited occupation or selected-exponent assertions
was found. The exact remaining obstruction to an unconditional result here is
the independently verified multispecies retarded pair identity with all
source, receiver, initial-boundary, and cutoff majorants, followed by the
appropriate local/continuation theorem in the stated regularity class. If
either fails, the conditional proposition must not be promoted to a full
solution. Nothing in this audit establishes priority or authorizes publication
of a claimed full solution.
