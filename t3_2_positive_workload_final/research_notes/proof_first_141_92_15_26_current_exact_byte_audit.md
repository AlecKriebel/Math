# Consolidated hostile audit of the 141, 92, 15, and 26 pair branches

Audit date: 2026-08-12 PDT.

## 1. Scope, exact bytes, and separate verdicts

This is a proof-first exact-byte audit of the current theorem notes
*rank_one_no_promotion_pair_branch.md*,
*post_rank_one_one_active_repair.md*,
*critical_one_active_q_trace.md*, and
*prospective_26_candidate_pair_theorem.md*.

For each branch the audit fixes one support pair, arbitrary strongly
connected reaction graphs on its linkage supports, arbitrary positive
labelled rates, and one closed irreducible class. Constants may depend on
those fixed data. No orientations or populations are enumerated. Finite code
is used only to identify pair sets, descriptor menus, and disjointness.

The separate exact-byte verdicts are:

| branch | theorem SHA-256 | verdict |
|---|---|---|
| rank-one no-promotion 141 | adc325b740dd18bfa4cc9ee53c2a3632f3660df589369a14cc4d9c3ce16992c1 | **STRICT PASS** |
| post-rank-one one-active 92 | b4944d0bed95f92978a0eaf08336744813804ca7ddd6af0c4cd84005361c6113 | **STRICT PASS** |
| critical positive-\(Q\) 15 | 01a7827e96874171bc0f96be4fd05edb2a7ce607398be312b1378e762f62ea82 | **STRICT PASS** |
| prospective common-\(W\) 26 | c78e53f11aeb981b415a90a486583b409608ef2256b73b9e063db48ac8d4fc88 | **STRICT PASS** |

Each verdict proves standalone classwise positive recurrence at its exact
pair scope. A stronger common-potential episode interface is also proved
within each fixed pair, as recorded below. None is by itself a global T3-2
verdict.

The associated current executable bytes are:

~~~text
141 source  8775d572485532131de7616f28a92fb9cb551e48fe5f4ed9f71323eed1cefb41
141 test    e0ad02f9b403d0db33d858bb26937c4dd28810ad28df36f9e4f1698d42fd4d43

 92 source  fc43fb6e5089cb684ab673b2da8457f28ef1b47996470021de801bf33a1c7b17
 92 test    a231ab07f59efc5348bd8a04785253f8d2f68d853ad70e9ae514d55cfeaf7dc9
 92 payload 215acfa5c3c2e8009081f6999d8971357563f9ff3ea36ba6d46a4fb4ec40a7ab

 15 source  23a30baa3ff9b67a0ee174fd1183f846a607c046bc0201b07e3787ba8833d505
 15 test    008cb703b2fbad427442044d07f728f2987cfc7c33c9ff5b65be1a713536de31

 26 source  45e42904072bb1cd451a98fdfd2750c0bb8ed442e028a9a1198193f1b91abff5
 26 test    d770f7c723b9748cf2f25cd455bf6a630dfd5eeea8bff287ca72d3739b8ee896
 26 payload a1f528caffb63729d889e792ce8831b899865e70c1564b2a0a33d46f295a39da
~~~

## 2. Exact pair identities and disjointness

The support-only replay gives:

| branch | pairs | pair fingerprint |
|---|---:|---|
| 141 | 141 | bc3540674c5ec8eef96fe4272e15c1f3d220a06fe7ad890189d2f745e6c22e67 |
| 92 | 92 | ef71d06b7ca9b9f1ef9049f37cb8047f96eb6e4def93c031302b65847edf5c8c |
| 15 | 15 | 6ec74f95e50e39ecda002b988d8233ae74c040ff9bb3518892dfd980bfad06d3 |
| 26 | 26 | 393474671be0bf095868e66cbcbf3164d941b99191517f172a41f157e20b21af |

The 141 and 92 sets are disjoint and their union is exactly the 233-pair
no-promotion rank-one family. Every pairwise intersection among all four
sets is empty. Their 274-pair union has fingerprint

~~~text
68eb9253de55c74713107ff4df91fcce66a0d48d3a1dc16c2155c6e6ccf8c40e
~~~

For the 92 branch, a support-only replay reproduced 272 one-active
incidences, twelve normalized profiles, the structural split \(200+72\),
and the initial-face split \(230+32+10\). No Hamilton-cycle table was run or
used. For the other branches, sixteen focused finite-identity tests passed.
These computations certify set identity and proof premises only.

## 3. Rank-one no-promotion 141: STRICT PASS

### 3.1 One potential per fixed pair

For a fixed pair, every rank-one failed phase has the same whole-top mask.
Use

\[
 {\cal F}_*(x)=K+\sum_i\log(x_i!)+\ell_*\cdot x,          \tag{3.1}
\]

where \(K\) makes the function nonnegative. Factorial growth dominates the
fixed linear correction, so \({\cal F}_*\) is proper.

If the common top is a reversible two-node support \(y\rightleftarrows z\),
the constraint

\[
 \ell_*\cdot(z-y)=\log(\kappa_{zy}/\kappa_{yz})           \tag{3.2}
\]

gives the exact discrete detailed-balance correction. For the directed
homogeneous triple, the fluid root fixes the same correction used in the
rank-one endpoint theorem. Whole-top compatibility makes this correction
literal across every failed active dimension of the pair.

The reversible discrete transfer is valid. If
\(\lambda=\kappa_{yz}(x)_{\underline y}\) and
\(\mu=\kappa_{zy}(x)_{\underline z}\), the factorial identity and
\(\log u\le u-1\) give

\[
\begin{aligned}
 \lambda\Delta_{yz}{\cal F}_*&\le\mu(x+z-y)-\lambda(x),\\
 \mu\Delta_{zy}{\cal F}_*&\le\lambda(x+y-z)-\mu(x).
\end{aligned}                                           \tag{3.3}
\]

The shifted falling-factorial differences have the certified
curvature-cofactor size. The discrete-continuous entropy difference has jump
\(O(\sum_{i:\zeta_i\ne0}(x_i\vee1)^{-1})\). Thus top correction costs are
\(O(\beta_n)\), while the forced lower exit divided by \(\beta_n\) tends to
\(-\infty\). This establishes the all-active reversible case for the same
\({\cal F}_*\), not merely for an asymptotically similar function.

### 3.2 All-clock rank-one episodes

The load-bearing corrected-factorial endpoint and its all-channel carrier
are current at

~~~text
4aa0297c6236eb80d565e2bdf76289ec23e34d79b137c3d484880a988230a615
af5516b5169047b0de069a5a49b8986875cc40926e1bf92d0d4abd2bbd35b110
~~~

For the 895 direct/top-activation incidences, every lower channel remains
present. Top clocks run inside conditioned occupation windows; the episode
stops at the prescribed actual lower target, a competing lower clock, or the
physical window endpoint. Its duration is \(O(a_n^{-1})\), and

\[
 \mathbb E\Delta{\cal F}_*\le-\pi g_n+C+o(1),
 \qquad g_n\to\infty.                                  \tag{3.4}
\]

This is a propensity-times-log estimate and remains valid for arbitrarily
slow subpower tier gaps.

For the 25 cap-zero incidences, constant-rate seed waits, all fast windows,
failed resets, and the additional unpaired service are retained. Attempt
counts are deterministically capped and shell exits are superpolynomial.
Thus

\[
 \mathbb E\Delta{\cal F}_*\le-c\log N+O(1),\qquad
 \sup_N\mathbb E\tau^q<\infty.                          \tag{3.5}
\]

The ten zero-boundary incidences are finite inside their fixed classes.
Physical duration is strictly lower order in both branches:
\(O(a_n^{-1})\) in (3.4) and \(O(1)\) against \(\log N\) in (3.5).
Exact endpoint moments remove localization.

### 3.3 Descriptor exhaustion and recurrence

The 141 selector has no feasible one-active failure. A divergent feasible
descriptor is a rank-one two-active failure, an all-active failure, or a
passing descriptor. These are handled by the same \({\cal F}_*\). A
zero-active sequence is finite, and a zero-boundary-only incidence is
confined to one finite top shell in its fixed class.

The bad-sequence lemma yields finitely many exceptions. Common-potential
physical-time gluing then gives finite mean target hitting. Population-
increasing reactions have only constant or affine propensities, so the
binary network is nonexplosive. Adding one class reference state if needed
makes the target nonempty; local finiteness gives a finite mean positive
return. This proves standalone positive recurrence and the stronger
pair-fixed episode interface.

## 4. Post-rank-one one-active 92: STRICT PASS

### 4.1 Arbitrary-orientation ordering

From any enabled active complex, strong connectivity supplies a simple path
to its first lower target. The residual-plus-current-complex lift makes the
path physically executable. Preterminal sources have active degree one, and
the first lower target gives reward \(-1\), with no slow-before-fast contest.

If no active complex is enabled, both inactive populations are zero. Without
a zero source, no reaction is enabled and the state is an absorbing
singleton. With a zero source, a simple path from zero to a nonzero lower
vertex either creates a cofactor or enters and exits the active set.
Simplicity prevents the cancelling exit from returning to zero; the
surviving cofactor supplies one further active exit. Conversely, a
zero-contest primitive return cannot leave unresolved positive active
reward. This proof uses strong connectivity, not a Hamilton-cycle regression.

### 4.2 Countable phase, interruption, endpoint, and time

After stripping the active molecule, the retained phase is a nonbranching
immigration/conversion/death process killed on its first active exit. Every
closed retained component has a route to killing. The independent-particle
construction gives exponential killed duration and endpoint moments, plus

\[
 \mathbb E\int_0^{\widehat\tau}
 (1+|E_s|)^q\{1+\log(1+|E_s|)\}\,ds<\infty.             \tag{4.1}
\]

This occupation estimate controls the size-biased law at a lower
interruption. Since lower propensities are at most quadratic in the inactive
phase and physical active time is scaled by \(N^{-1}\),

\[
 \mathbb P\{\hbox{lower interruption}\}=O(N^{-1}).       \tag{4.2}
\]

Every lower clock remains present and the episode stops at its first such
interruption. That interruption has bounded population jump and expected
positive factorial cost \(O(\log N/N)\). On the complementary priority
endpoint the active population falls by one. With the same correction
\({\cal F}_*\) used in the multi-active theorem,

\[
 \mathbb E[{\cal F}_*(X_\tau)-{\cal F}_*(x)]
 =-\log N+O(1),\qquad \sup_N\mathbb E\tau<\infty.        \tag{4.3}
\]

Lower-only seed waits, failed returns, and active windows are included. Seed
attempts are geometric with a positive rate-dependent success parameter. No
finite phase box is asserted.

### 4.3 Composition

Along a genuinely one-active sequence, inactive integer populations are
eventually fixed. If either is unbounded, even subpower relative to the
active coordinate, refined source-rate extraction routes the sequence to an
already proved multi-active descriptor. The 92 pairs use one pair-fixed
\({\cal F}_*\) on one-active episodes, rank-one episodes, all-active cones,
and passing regions. Equation (4.3) pays duration with a diverging margin.
Frozen rows are absorbing singleton classes. Bad-sequence gluing,
nonexplosion, and finite-target return therefore give standalone positive
recurrence and the stronger pair-fixed episode interface.

## 5. Critical positive-\(Q\) 15: STRICT PASS

### 5.1 Exact sign for arbitrary rates and orientations

Put \(M=A+B\) and \(Q=C-M\). The linkage
\(L_0=\{0,A+C,B+C\}\) preserves \(Q\). On \(Q=N\), its deficiency-zero
stationary law is

\[
 \pi_N(a,b,N+a+b)
 =Z_N^{-1}{u^av^b\over a!\,b!\,(N+a+b)!}.              \tag{5.1}
\]

Unary inactive occupation is \(O(N^{-1})\), while quadratic occupation is
\(O(N^{-2})\). Any strongly connected partner support containing unary and
quadratic complexes has a directed unary-to-quadratic edge. Hence

\[
 a_-=\sum_{\text{unary }y\to\text{quadratic }z}
       \kappa_{yz}r_y>0                                \tag{5.2}
\]

for every positive rate vector, and the \(T\)-drift of \(Q\) is
\(-a_-/N+O(N^{-2})\). No rate choice reverses the leading sign.

### 5.2 Full stopped cycle

The physical cycle retains every \(T\)-reaction and stops at the first
positive return to \(M=0\), \(M\ge\rho N\), \(Q\le N/2\), or \(Q\ge2N\).
The multiplicative particle corrector has drift \(-cCM\); quadratic label
changes cost \(O(M^2)\). A rate-dependent \(\rho\) absorbs that cost.

The proof suppresses slow creators only to expose comparison blocks; the
actual stopping time retains them. At block endpoints, the particle count is
dominated by a subcritical nearest-neighbor walk, including path
multiplicity. The exact identities

\[
 M=1+I_0+U_T-D_T-D_0,\qquad Q-N=-U_T+D_T              \tag{5.3}
\]

show that either \(Q\)-boundary requires order-\(N\) creation blocks.
All duration and normalized endpoint moments are bounded, while boundary
probability is superpolynomial.

Kac's identity, coupled to the full cycle until its first \(T\)-event, gives

\[
\begin{aligned}
 \mathbb E(Q_\tau-N)&=-{a_-\over\Lambda N}+O(N^{-2}),\\
 \mathbb E(Q_\tau-N)^2&={a_-\over\Lambda N}+O(N^{-2}).
\end{aligned}                                           \tag{5.4}
\]

Two \(T\)-events and a quadratic-to-unary first event are \(O(N^{-2})\);
physical boundaries are included in the remainder.

### 5.3 Common squared factorial and return

Choose one fixed linear correction and

\[
 F_\ell=K+\sum_i\log(x_i!)+\ell\cdot x,\qquad V=F_\ell^2.
\]

This is proper. At the base \(F_\ell(z_N)=N\log N+O(N)\), and (5.4) gives

\[
 \mathbb E[V(X_\tau)-V(z_N)]
 =-{2a_-\over\Lambda}(\log N)^2+O(\log N),              \tag{5.5}
\]

which pays bounded physical duration.

The eight companion rows use the same \(V\). Direct rows have a killed
countable immigration/death phase with exponential endpoint moments; their
successful endpoint loses one active molecule, while noncarrier clocks act
for \(O(X^{-1})\) time. The two zero-source rows use geometric resets and the
same all-clock carrier. Their exceptional squared-factorial cost is lower
order.

Every other feasible descriptor passes. For bounded jumps,

\[
 {\cal L}V=2F_\ell{\cal L}F_\ell+
   \sum_r\lambda_r(\Delta_rF_\ell)^2,                   \tag{5.6}
\]

and the carré term is little-oh of the strict first term. The \(M\)- and
\(Q\)-boundaries are generator-good, macroscopically favorable, or
superpolynomially rare and endpoint-weighted. Restarting at a new positive
\(Q\)-level uses the same \(V\). The \(75+8\) menu is exhaustive.
Bad-sequence gluing, nonexplosion, and random-time Foster give standalone
positive recurrence and the stronger pair-fixed episode interface.

## 6. Prospective common-\(W\) 26: STRICT PASS

### 6.1 Pair-fixed correction and one-active kernel

Every failed all-active descriptor of a fixed pair has the same two-node
whole-top support. Its strong orientation is bidirectional. Choose one
\(\ell\) satisfying

\[
 \ell\cdot(z-y)=-\log(\kappa_{yz}/\kappa_{zy}),
\]

and set

\[
 F_\ell=K+\sum_i\log(x_i!)+\ell\cdot x,\qquad
 G=1+F_\ell,\qquad W=G^4.                               \tag{6.1}
\]

Factorial growth makes \(W\) proper. The same \(\ell\) works on every
all-active cone and in the one-active kernel.

The 30 one-active rows have a physical active source, a resistance-zero
origin service, or an absorbing no-history origin. Simple strong-graph paths
give a resistance-zero old-debt reduction in the first two cases. A positive
primitive origin return cannot occur at zero resistance. Thus

\[
 p_D(n)\ge a,\qquad p_U(n)\le b/n,\qquad
 \mathbb E\sigma_n\le T.                               \tag{6.2}
\]

The phases are killed nonbranching immigration/conversion/death systems.
Ordered compensation sums neutral loops and controls size-biased endpoints.
A moving boundary \(L_n=n^{1/8}\), including simultaneous terminal ties, has
the stopped endpoint-weighted three-interruption remainder. The fixed linear
correction changes each jump only by \(\ell\cdot\zeta\); at the boundary its
extra cost is \(O(L_n+J)\), absorbed by proved \(J\)-moments above order
eight. Repetition through neutral bases gives

\[
 \mathbb E[W(X_\tau)-W(x)+\tau]\le-1                  \tag{6.3}
\]

with every physical clock retained. A boundary sequence has at least two
active coordinates and is generator-good for this selector.

### 6.2 Discrete all-active fourth-power drift

For the bidirectional top, write

\[
 A=\kappa_{yz}x_{\underline y},\qquad
 B=\kappa_{zy}x_{\underline z},\qquad
 {\cal D}=(A-B)\log(A/B)\ge0.
\]

The exact factorial ratio gives

\[
 \Delta_{yz}F_\ell=-\log(A/B)+\varepsilon_+,\qquad
 \Delta_{zy}F_\ell=\log(A/B)+\varepsilon_-,
\]

where

\[
 |\varepsilon_+|+|\varepsilon_-|
 \le C\sum_{i:(z-y)_i\ne0}x_i^{-1}.                    \tag{6.4}
\]

Certified curvature cofactors imply \((A+B)/x_i\le C\beta\), with
\(\beta\) the maximal lower-source propensity. Therefore

\[
 {\cal L}_TF_\ell\le-{\cal D}+C\beta,\qquad
 \sum_{r\in T}\lambda_r|\Delta_rF_\ell|^k
 \le C({\cal D}+\beta),\quad 2\le k\le4.                \tag{6.5}
\]

The lower linkage gives
\({\cal L}_RF_\ell\le-\beta a_n\), \(a_n\to\infty\), and \(k\)-th jump
moment \(O(\beta\{1+\log^k R_n\})\). In the exact fourth-power identity, the
negative \(-G^3({\cal D}+\beta a_n)\) term absorbs top curvature and every
lower Taylor remainder. Thus \({\cal L}W\to-\infty\) on all 94 failed
all-active cones. Passing cones satisfy the same powered estimate, and there
is no two-active failure.

### 6.3 Marked target and recurrence

Use deterministic reflected marks

\[
 D_i^+=(D_i+\zeta_i)^+,\qquad H_i=X_i-D_i.
\]

Then \(0\le D_i\le X_i\), and every \(H_i\) is nonincreasing. In a
divergent one-active tube, \(D_X=0\) would force \(X=H_X\le H_X(0)\), so
every reachable divergent tube has positive old debt. The down endpoint in
(6.3) reduces that debt.

When every debt is zero, \(X_i=H_i\le H_i(0)\), so the marked target has
finite physical projection. Generator-good motion, one-active episodes, and
moving-boundary endpoints all use the same \(W\). The all-debt target
theorem is current at

~~~text
c87aa83b798e2a69bcc94f8de885b5b6bb403dd0898caaf9b6dfd43c26519e8a
~~~

and gives finite mean target hitting. Linear population-growth rates give
nonexplosion; the finite trace plus irreducibility gives positive recurrence.
This proves both the standalone theorem and its stronger marked
common-\(W\) episode interface.

## 7. Sequential coercivity and common-potential interfaces

There is no cross-pair Lyapunov-switching problem. The four selectors are
disjoint, so a physical network belongs to at most one branch. Within one
fixed pair:

* the 141 and 92 branches use one corrected factorial \({\cal F}_*\);
* the 15 branch uses one squared corrected factorial \(V\); and
* the 26 branch uses one fourth power \(W\).

Every divergent classwise sequence has an exact descriptor subsequence. An
affine-infeasible descriptor cannot occur in that class. Passing and
all-active-good descriptors have pointwise coercivity. Every remaining
failure has the displayed physical episode. Episode boundaries are charged
before stopping and are favorable descents, rare endpoint-weighted exits,
generator-good higher-active states, or restarts where the same potential is
used again.

Thus no clock is discarded and no potential-switching toll is hidden. The
common-potential gluing lemma used by the first three branches is current at

~~~text
7550c81b6a2a3085a34deaa9654517b7b00bb46bbd9e76898ee2220f6d53d194
~~~

The 26 branch uses its marked finite-target specialization. These interfaces
give finite mean hitting, not merely almost-sure hitting. Adding a reference
state makes the target nonempty; local finiteness and irreducibility yield a
finite mean positive return.

## 8. Hostile counterexamples checked

The audit tried and ruled out:

1. arbitrarily slow subpower gaps in the rank-one endpoint;
2. a lower clock firing during an enabled active phase in the 92 branch;
3. an unbounded inactive endpoint hidden behind a finite phase box;
4. a strong orientation with no unary-to-quadratic edge in the critical
   family;
5. quadratic label changes destroying the critical block comparison;
6. a \(Q\)-boundary reached without order-\(N\) creation blocks;
7. reversible top curvature overwhelming fourth-power drift in the 26
   branch;
8. a moving-boundary endpoint charged with bounded-endpoint moments;
9. incompatible corrections between active dimensions; and
10. an empty or infinite classwise recurrence target.

No counterexample survives the stated hypotheses.

## 9. Mechanical derivatives and qualifications

Two executable descriptions are stale, but neither is load-bearing.

* The opening docstring of *src/one_active_kinetic_depth.py* calls the file
  claim-neutral and says it certifies finite word geometry only, while its
  current payload sets the scoped 92-pair analytic and recurrence flags true.
  The theorem contains the analytic proof and the payload is explicit, so
  this does not change the PASS verdict. The docstring should be updated
  before treating the source as publication prose.
* The 141 source says the complementary 92 interfaces remain open. That is
  historically correct for the exact 141 snapshot but stale after the
  separate 92 theorem. It neither enlarges nor weakens the exact 141 claim.

No derivative-order or scaling mismatch was found in the theorem proofs.
All physical duration terms are strictly below their negative potential
margins, and every powered-potential Taylor or carré term is absorbed at the
stated order.

## 10. Replay boundary and dependency hashes

The 141-, 15-, and 26-pair focused suites passed sixteen tests. The 92 pair
set and twelve profiles were replayed directly without calling its
Hamilton-cycle regression. No orientation or population enumeration was
performed or used as analytic evidence.

Additional exact load-bearing dependency bytes are:

~~~text
global refined-weight interface   3b80734707dcac833621770c881da2be9782efc5658605179cd18e327a3c07d9
arbitrary-orientation graph proof c86bea36ccbdf6319e259fd397023ba69a0fb31346c6ffe8d51261ef9bd7d625
fourth-power one-active interface 9d4239f4fc6b45a9522b94b09523c9f98ac7a3b089c919bd9594f12409c78cc2
~~~
