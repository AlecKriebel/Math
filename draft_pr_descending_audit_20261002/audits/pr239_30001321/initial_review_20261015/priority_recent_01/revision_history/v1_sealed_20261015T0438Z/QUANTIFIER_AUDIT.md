# Quantifiers and implication checks

Independent recent-literature lane, PR239 / 30001321. Written 2026-10-15 UTC.
These deductions audit implications between statements. The countermodels below
are countermodels to proposed logical implications, not random-environment
counterexamples to the submitted result.

## 1. The target and the negative conjecture

For a fixed environment law ν on (0,1), let μ_N^ω be the quenched endpoint law of
the walk with increments ±1, and α_N its expectation. For an equal-interval
partition Π(M,a), put

    L(N,M,a) = sum_{I in Π(M,a)} |μ_N^ω(I) - α_N(I)|.

Write A(ν) for this full assertion:

    for each deterministic M_N→∞, each deterministic alignment a_N,
    each ε>0 and each K>0, there are C,N_0<∞ such that
    P_ν(L(N,M_N,a_N)>ε) ≤ C N^{-K}, N≥N_0.

The threshold can depend on the sequence. Constants need not be uniform as ν
approaches the deterministic-arrow boundary. The submitted target is ∀ν A(ν).
The source's dimension is the transverse dimension, so its d=1 means this
one-dimensional endpoint space, not a one-dimensional static environment.

The one-sentence negative conjecture on OWR 38/2009 printed p.2151 does not
spell out an additional distributional quantifier. At least two readings must
therefore be kept separate:

1. **Failure of the general theorem:** ¬[∀ν A(ν)], equivalently ∃ν ¬A(ν).
   This is the literal negation of extending the preceding universal theorem.
2. **Universal one-dimensional failure:** ∀ν in a specified nondegenerate class,
   ¬A(ν). An affirmative result for one nondegenerate law refutes this stronger
   negative reading, while leaving reading 1 unresolved.

A deterministic fixed probability p is already an elementary A(ν) example,
because μ_N^ω=α_N identically. It would be unreasonable to advertise that fact
as a new substantive resolution of the source problem. The source does not
explicitly exclude such laws in the theorem. This is another reason to state
the exact full positive theorem rather than assign an undocumented universal
failure interpretation to the negative sentence.

The audit therefore records two separate priority questions: (F) earlier full
coverage ∀ν A(ν), and (S) earlier nontrivial law-special A(ν), which may already
answer reading 2. Neither is inferred from a result for a correlated,
nonelliptic environment outside the source model.

## 2. What the 2024/2026 percolation coarse comparison really implies

Primary source: Bethuelsen–Birkner–Depperschmidt–Schlüter,
[arXiv:2410.14302](https://arxiv.org/abs/2410.14302), v1 printed p.19 and v2
printed p.21, Lemma 4.1, equations (4.1)–(4.2). Its coarse error bound is of
the form

    L_perc(N,M) ≤ C M^{-c} + C N^{-c}

outside an event of probability at most

    C̃ N^{-c̃ log N} = C̃ exp[-c̃(log N)^2].

The positive constants in this statement are uniform in N and M, after fixing
the model parameters. The preceding fixed-power mesoscopic comparison,
Theorem 3.2, is not the strongest relevant statement: Lemma 4.1 carries the
comparison to general M. The same lemma and bound are present in v1 of
2024-10-18, not first introduced by the 2026 revision. This audit verifies that
the statement occurs in both versions; it does not independently certify the
correctness of every proof step in the earlier version.

Here is the exact implication. Fix ε>0 and a deterministic M_N→∞. Eventually
C M_N^{-c}+C N^{-c}<ε, so

    P(L_perc(N,M_N)>ε) ≤ C̃ exp[-c̃(log N)^2].

For any fixed K, c̃ log N≥K eventually. Thus the right side is at most
C̃ N^{-K}. No lower rate for M_N is required. The time threshold may depend
on M_N. Thus this is a genuine all-diverging-scale, superpolynomial prior
result in one spatial dimension for its own model. A claim that all previous
one-dimensional dynamic-environment results stop at M=N^γ would be false.

Why this is not yet F or S: the underlying iid variables are Bernoulli site
variables, whereas the transition kernel is a function of whether sites have
open paths to infinite future time. The transition kernels are therefore
correlated, can vanish, and allow holding. Their exact equation (2.2) is not
the target's iid pair (p,1-p) on increments ±1. A proof for this model does not
become a proof for arbitrary iid transition probabilities simply by calling
both underlying media iid. No exact coupling or comparison with errors of the
required order was found. The fact that the authors suggest extensions to
other models is not such a theorem.

Even a two-step target skeleton does not give the percolation environment:
two-step kernels from adjacent same-parity starting sites share intermediate
environment variables. The skeleton can handle parity in a general flow
framework, but it does not identify its law with the percolation backbone law.

## 3. Why fixed-power mesoscopic results cannot be diagonalized for free

A theorem for every fixed γ>0 at M=N^γ does not imply a theorem at arbitrary
M_N→∞. For M_N=ceil(log log(N+e^e)), every fixed N^γ eventually exceeds M_N.
The target quantifies over one fixed deterministic sequence, including this
one. Setting γ=γ_N in a theorem with constants and thresholds depending on γ
is invalid without uniformity.

Similarly, a failure bound exp[-c(log M)^2] at block size M does not imply
O(N^{-K}) for arbitrary M_N. With M_N=ceil(log log N), its logarithm is of
order -(log log log N)^2, not -K log N. This distinction concerns the
environmental failure probability, even if the deterministic coarse error
tends to zero at every divergent M_N.

The percolation Lemma 4.1 is stronger precisely because its failure exponent is
in N while its deterministic error is separately controlled by M.

## 4. Why weak/distributional convergence misses small coarse cells

Consider probability measures on [0,1] with densities

    f_N(x)=1+b sin(2π k_N x),  0<b<1,
    k_N=ceil(N^{3/8}),

and the uniform reference density 1. They have total mass one. For each C^1
test function φ, integration by parts gives

    |∫_0^1 φ(x)(f_N(x)-1)dx|
      ≤ b(2||φ||∞ + ||φ'||∞)/(2π k_N).

Consequently the pairing still tends to zero after multiplication by
N^{1/4}, since N^{1/4}/k_N→0. This is stronger than unscaled smooth-test
convergence.

Now choose equal cells of width h_N=1/J_N with

    J_N=ceil(sqrt(N)/log(N+e)).

In original microscopic coordinates these cells have width
sqrt(N)/J_N∼log N→∞. Since k_N/J_N→0, the sign of the sine changes only in
O(k_N) cells. Away from those cells, the absolute value of its integral equals
the integral of its absolute value. The total lost integral in sign-changing
cells is at most 2b k_N/J_N→0. Hence

    sum_cells |∫_cell (f_N-1)| → ∫_0^1 b|sin(2π k_N x)|dx = 2b/π.

This explicitly shows that even a smooth-test discrepancy invisible at
N^{1/4} can retain a nonvanishing coarse L1 discrepancy at a logarithmically
diverging microscopic width. Therefore the distribution-valued bulk
fluctuation theorem of arXiv:2510.22155 cannot by its statement alone supply
the target's all-cell L1 conclusion. It may contain useful estimates for a
separate argument; that argument must actually be proved.

## 5. Why convergence in mean, probability, or almost surely is insufficient

Let B_N be events with P(B_N)=N^{-2}, and let a nonnegative discrepancy be
Z_N=1_{B_N}. Then E Z_N=N^{-2}→0, Z_N→0 in probability, and the first
Borel–Cantelli lemma gives Z_N→0 almost surely. Nevertheless
P(Z_N>1/2)=N^{-2}, which is not O(N^{-3}). Thus none of these convergence
modes yields the target's every-K environmental tail without additional
quantitative input. This countermodel even has a summable failure sequence.

All moments at a fixed block scale do not repair the issue if their time
dependence is absent. E Z_{N,M}^r≤C_r M^{-rη} gives only
P(Z_{N,M_N}>ε)≤C_r ε^{-r}M_N^{-rη}. For a sufficiently slow divergent
M_N this is not a bound of order N^{-K}, for any fixed choice of r.

## 6. Random-corrector local limits and the missing tail upgrade

A local limit μ_N(x)≈α_N(x)U_N(x), with stationary E U_N(x)=1, leaves two
separate quantities to control:

    L(N,M) ≤ sum_x |μ_N(x)-α_N(x)U_N(x)|
             + sum_I |sum_{x in I} α_N(x)(U_N(x)-1)|.

Convergence of the first term merely in mean or probability and an ergodic
theorem for U averages may yield convergence in probability at diverging
coarse scales; section 5 shows that this does not produce arbitrary-K tails.
The second term additionally needs block averaging and control of the
variation of α_N inside each block. A random density factor cannot simply be
replaced by its expectation pointwise.

For example, suppose a one-dimensional continuous model supplies the uniform
mean-square pointwise error

    sup_x E|u(t,x)-G_t(x)U(t,x)|^2 ≤ C t^{-4/3} log t.

On |x|≤R sqrt(t), Cauchy–Schwarz and integration imply only the immediate
bound

    E∫_{|x|≤R sqrt(t)}|u-G_tU|dx
       ≤ 2RC^{1/2} t^{-1/6}sqrt(log t).

Markov's inequality gives a fixed polynomial failure bound. Higher
environmental concentration is not a consequence of that L2 estimate. If
|Cov(U(x),U(y))|≤C/(1+|x-y|), a block average has variance at most
C log(2+M)/M; this again gives a useful averaging statement but no tail in N
at arbitrarily slow M. These calculations concern the structure of the
Dunlap–Gu theorem, not an asserted transfer of its continuous diffusion to
the discrete target.

## 7. Static uniform ellipticity does not survive the directed embedding

The space-time lift of the target has increments (1,1) and (1,-1). After
rotating coordinates this is an up-right walk on Z^2. It assigns probability
zero to both backward directions. Static RWRE theorems requiring a positive
lower bound for every nearest-neighbor direction therefore do not apply to
this lift, even when the original p is bounded away from 0 and 1.

Adding a small backward probability changes the model. Sending that
probability to zero after invoking a theorem would require uniform estimates
as the static ellipticity constant vanishes, as well as an error comparison
for endpoints up to time N. Neither is supplied by the theorem's stated
hypotheses. The merely elliptic target law also permits no finite inverse
moments of p or 1-p. Results requiring such moments do not cover every target
law without a further truncation argument with quantitative errors.

## Status

The percolation implication in section 2 is a verified positive implication.
The candidate transfers rejected in sections 3–7 have exact identified gaps.
No argument in this note proves absolute novelty. No source was found in this
lane that establishes F, or a nontrivial target-law S with every scale and
the required environmental tail.
