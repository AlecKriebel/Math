# Independent forest adversary: PR 1131 / problem 30005455

Audit date: 21 October 2026 UTC. Audited immutable head:
`bacae693a1f2a33c89565b0bd716620885831289`; supplied base:
`f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`.
The eight authored head files were obtained directly with `git show`; no
historical acceptance or checker was treated as mathematical evidence. The
entire head proof was read, including the whisker section and appendix, but
this independent family's adjudication concerns the forest mechanism only.

## Finding and exact scope

I did not find a counterexample or a defective inference in the cycle/Hessian
proof. It proves the following deterministic statement: on a finite simple
undirected loopless graph, at a WARM equilibrium whose positive support covers
every positive-rate vertex, an even support cycle forces a positive real
Jacobian eigenvalue for every alpha>1; an odd support cycle of length m does so
for alpha>sec²(pi/(2m)). Consequently all equilibria without a positive
Jacobian eigenvalue have forest support for alpha>4/3, for arbitrary positive
vertex rates. Chords, other cycles, positive attached edges, unequal supported
weights, critical directions elsewhere, and zero-weight ambient edges do not
invalidate the argument.

The published finite-graph convergence theorem and support-identification
proposition then give the asserted almost-sure stochastic forest statement
from unit initial counts. A short reachable-state argument below extends this
almost-sure conclusion to every prescribed vector of **positive integer**
initial counts. That extension is absent from the audited manuscript, whose
stated theorem is deliberately narrower. It is a small missing scope argument,
not a counterexample to its actual theorem. A claim encompassing arbitrary
positive noninteger initial counts needs an additional justification; the
integer reachability proof does not do that. The excluded endpoint alpha=4/3
has not been assigned a stochastic conclusion.

This is a mathematical family report, not a novelty, priority, publication,
or complete two-clause-problem verdict. In particular, the original question
asks for improvements of the then-known bounds. Its subsequent suggestion
that 4/3 might be sharp does not change the literal improvement request.
The separate equal-rate whisker proof requires separate adjudication.

## Primary-source reconciliation

The original [Oberwolfach report](https://ems.press/content/serial-article-files/47008),
PDF pp.15–18, printed pp.653–656, describes prescribed initial counts and
positive vertex firing rates. Printed p.655 asks to improve the forest
threshold 2 and, separately under equal rates, the whisker threshold 25. It
then gives the triangle obstruction below 4/3 and proposes 4/3 as a possible
sharp value. The finite-graph restriction occurs in the supercritical section;
the following infinite-graph questions are separate. The displayed general-rate
Lyapunov formula on printed p.654 omits the firing-rate factors; direct
differentiation requires them, and the audited proof supplies them correctly.

[Hirsch–Holmes–Kleptsyn 2023](https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf)
defines unit integer counts on PDF p.3 / printed 3014. Theorem 1 on PDF p.5 /
printed 3016 applies to finite graphs, alpha>1 and arbitrary positive rates:
the scaled counts converge almost surely to stable or critical equilibria;
each strictly stable equilibrium has positive probability. Proposition 1 on
PDF p.10 / printed 3021 identifies infinite reinforcement with positive
asymptotic growth under bounded degrees and bounded positive rates. These
conditions are automatic in the present finite setting. The normalization
footnote on printed 3015 allows the sum of rates to be set to one. These are
imported published results, not reconstructed foundations. Its even-cycle
Lemma 2 on PDF pp.25–26 is also consistent with the even-cycle argument here.

[Holmes–Kleptsyn 2017](https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf)
states the earlier structural threshold 2 in Theorem 3 / Corollary 1,
and the uniform-rate whisker bound in Theorem 2(a). Remark 1 on manuscript
p.4 says positive initial counts may be normalized to one for that paper's
purposes. Lemma 4 / Corollary 7 on pp.19–20 supply the credited least-weight
idea. Example 1 on p.9 exhibits the failure of unrestricted-rate whisker
conclusions. Its older stochastic assertions should not replace the stronger
2023 theorem. None of these source statements is a proof of a new odd-cycle
bound.

The primary PDFs and local text extractions remain private. Their exact
identities are bound in the companion manifest. OWR SHA-256 is
`320d7e903924249d1f57536cdf67491b3b5f89de8401c9a7c07800b09ee750c7`;
the 2023 and 2017 PDF hashes are respectively
`ea5801394f0f50c8a6fd28296787091d9607b50deb7931ad3b3a068092d001cd`
and `4c0376677b4aceaa17b88fb8631bf559a4e95e6694296292746e21f9d875199b`.

## Independent derivation

Write a_e>0 on the retained support H, S_v=sum_{e~v} a_e^alpha, and
lambda_v>0. At an equilibrium,

    F_e(a) = -a_e + sum_{v~e} lambda_v a_e^alpha/S_v = 0.

Define L=-sum_e a_e+(1/alpha)sum_v lambda_v log S_v. On this positive face,
F=diag(a) grad L. Thus the Jacobian at equilibrium is diag(a) Hess L and
is similar to the symmetric matrix diag(sqrt(a)) Hess L diag(sqrt(a)). A
positive Hessian direction gives a positive real eigenvalue even if other
eigenvalues vanish. No claim of hyperbolicity is needed.

Set y_e=a_e^alpha. The transformed potential is

    Phi(y) = -sum_e y_e^(1/alpha)
             + (1/alpha)sum_v lambda_v log(sum_{e~v} y_e).

Its gradient vanishes at the same equilibrium. Therefore the two Hessians
are related by congruence; the additional coordinate-change term involving
the gradient is zero. Direct differentiation yields, for every real w,

    alpha² Hess Phi[w,w]
      = (alpha-1)sum_e D_e w_e²
        - alpha sum_v c_v (sum_{e~v} w_e)²,
    D_e = a_e^(1-2alpha),   b_v=lambda_v/S_v,
    c_v=lambda_v/S_v²=b_v/S_v,
    a_e^(1-alpha)=b_u+b_v   (e=uv).

This is an ascent potential: a positive direction, not a negative direction,
certifies instability. All D_e and b_v are strictly positive.

Choose a simple support cycle e_0,...,e_{m-1}, with v_i incident to
e_{i-1},e_i, and put A_i=a_{e_i}^alpha. Then

    sum_i D_{e_i}
      = sum_i b_{v_i}(1/A_{i-1}+1/A_i).

At every cycle vertex,

    c_{v_i} = b_{v_i}/S_{v_i}
      <= b_{v_i}/(A_{i-1}+A_i)
      <= (b_{v_i}/4)(1/A_{i-1}+1/A_i).

The second inequality is exactly (A_{i-1}-A_i)²>=0 after multiplication
by positive denominators. Hence 4 sum_i c_{v_i}<=sum_i D_{e_i}.
No equal-rate or equal-weight assumption entered this calculation.

Use perturbations equal to zero off the selected cycle. For even m, set
w_{e_i}=(-1)^i. The two cycle contributions cancel at each cycle vertex;
all other vertex sums are zero. The quadratic form is then
(alpha-1)sum_i D_{e_i}>0.

For odd m, put theta=pi-pi/m. Because m theta=(m-1)pi is a multiple of
2pi, the two real vectors u_i=cos(i theta), w_i=sin(i theta) are cyclically
consistent, including at v_0. Their combined edge squares equal one, and
their combined squared vertex sums equal 4sin²(pi/(2m)). Adding their
quadratic forms gives

    alpha² (Hess Phi[u,u]+Hess Phi[w,w])
      >= [alpha cos²(pi/(2m))-1] sum_i D_{e_i}.

Under the strict stated threshold this is positive, so at least one of the
two real vectors is a positive direction. The proof never needs either
particular direction to be positive individually. For odd m>=3 the largest
sec²(pi/(2m)) is 4/3 at m=3. Every finite simple nonforest has an even or
odd simple cycle, completing the deterministic exclusion.

The calculations concern the unconstrained positive face. This does not
create a spurious positive direction normal to the total-mass simplex:
sum_e F_e=Lambda-sum_e a_e, so 1^T DF=-1^T. Any eigenvector for a positive
eigenvalue lies in sum_e h_e=0. The radial scaling mode has eigenvalue -1.

## Chords, boundary, and stochastic transfer

A positive chord or attached edge increases S_v but does not enter the
chosen perturbation. It consequently strengthens the local c_v upper bound.
Chords whose endpoints lie on the cycle cause no additional perturbation
sum because their own perturbation coordinates are zero. The cycle need not
be an induced cycle, and H may have several connected components.

At an almost-sure limiting vector supplied by the convergence theorem,
sum_{e~v} a_e>=lambda_v: the corresponding incident count sum always
dominates the number of firings at v, and the latter divided by time tends
to lambda_v. Thus no retained vertex denominator vanishes. For alpha>1,
the derivative of z^alpha at z=0 from the nonnegative side is zero.
Consequently a zero-edge row of DF is its own -1 coordinate and zero
elsewhere; a supported row has zero derivatives in zero-edge coordinates.
The full derivative is the support derivative direct-summed with -I. It is
C1 at such boundary points, even for 1<alpha<2; a full boundary Hessian of
L is unnecessary. A positive support eigenvalue is therefore a positive
full-system eigenvalue. Nonhyperbolic equilibria elsewhere are excluded
whenever this strictly positive direction exists.

Let Lambda=sum_v lambda_v, p_v=lambda_v/Lambda and a=Lambda x. Directly,

    F_lambda(a)=Lambda F_p(a/Lambda),
    DF_lambda(a)=DF_p(a/Lambda).

This reconciles the counts-per-time convention with probability-normalized
sources and preserves the support and eigenvalue signs. The independent
Poisson clocks have total firing rate Lambda, so the embedded jump times
also have the requisite asymptotic time scale. Proposition 1 identifies
the infinitely reinforced support with the positive-growth support; the
forest conclusion is not restricted merely to positive limiting proportions.

## Positive integer initial counts: a complete scope repair

Fix n=(n_e) with every n_e a positive integer. In the embedded jump chain,
start from all-one counts and prescribe n_e-1 reinforcements of each edge e,
in any fixed order, for K=sum_e(n_e-1) steps. Choose either endpoint v_e
as the reinforcing vertex for each prescribed reinforcement. Each such
vertex has positive probability lambda_{v_e}/Lambda, and each prescribed
edge choice has positive probability because all current counts are
positive. The finite product is therefore strictly positive, and the state
after the Kth step is exactly n.

Conditioning on this finite event, the future jump chain has exactly the
law of the chain started from n. Independent Poisson increments and the
memoryless property give the corresponding continuous-time future law.
If a tail property fails with positive probability from n, it therefore
fails with positive probability from all-one counts. An almost-sure tail
property from all-one counts must hold from n. Both forest support and
convergence to the permitted equilibrium set are tail properties: a finite
number of increments and a finite random time shift do not change which
counts diverge, nor the limiting count/time vector. This proves the desired
integer-count extension with no new stochastic approximation theorem.

The same reasoning transfers every proved almost-sure whisker conclusion,
once that conclusion is independently established, but this family does
not adjudicate its algebra. Unit-count stable attainability alone does not
automatically transfer *every* stable target to every n by this one-way
argument. For the fully supported triangle target it can be transferred:
on convergence to a strictly positive vector every edge count eventually
exceeds n; some reachable dominating integer state k then has positive
conditional attainment probability. That k is reachable from n with
positive probability, yielding positive attainment from n as well.

Noninteger positive counts are not reachable from unit counts by integer
increments, so that case requires an explicit extension of the imported
stochastic theorem or a different comparison argument. Zero counts are
also not silently admitted: x^alpha=0 makes such edges unavailable, and a
vertex with only zero incident counts has an undefined choice rule unless
a convention is added. If every vertex has a positive integer incident
edge, removing initially zero edges reduces the model to the proved case,
but this is an additional explicitly stated convention. Negative counts
do not define the stated reinforcement model.

## Sharpness, endpoint, and graph conventions

For an equal-rate unit triangle, a=(1,1,1) and lambda=(1,1,1). The direct
Jacobian has diagonal alpha/2-1 and off-diagonal -alpha/4, so its spectrum is

    {-1, 3alpha/4-1, 3alpha/4-1}.

It is strictly stable for 1<alpha<4/3 and is positively attained by the
published theorem. All three edges survive there. This supplies the known
sharp lower obstruction to any smaller universal strict forest threshold;
the calculation is not offered as new. At alpha=4/3 two eigenvalues vanish,
so the strict-stability attainment clause is inapplicable. Neither this
report nor the manuscript claims its stochastic fate.

The argument even gives a useful endpoint diagnostic: at alpha=4/3 a
triangle with nonuniform retained weights or any positive attachment gives
strict slack in the summed inequality, and hence instability. Every longer
odd cycle and every even cycle is already strictly unstable. The remaining
cyclic non-linearly-unstable candidate components are therefore isolated
uniform triangles; their equilibrium equations force the three vertex
rates to be equal. This is only a deterministic diagnostic and does not
settle the stochastic endpoint.

The original OWR introduction uses the word graph without separately spelling
out a loop/multigraph convention in the inspected model passage. The PR
explicitly assumes finite simple undirected loopless graphs, which is a
legitimate explicit scope restriction. Do not extend it silently. A graph
with one vertex and one loop, reinforced once at each firing, retains its
loop forever; it disproves any forest claim if that convention is included.
The formula summing over two distinct endpoints also needs modification for
loops. For loopless multigraphs, a pair of parallel edges has the same
alternating cancellation as a length-two cycle, so the deterministic proof
extends if parallel edges are distinct choices and multigraph acyclicity
counts a parallel pair as a cycle. The stochastic theorem's applicability
must still be stated through its finite-WARM formulation rather than
assumed from a bare graph label. No such extension is needed for the PR's
stated claim.

## Exact adversarial controls and remaining gap

The new, read-only companion verifier reconstructs equilibrium and Jacobian
matrices using rational arithmetic, independently compares direct field
differentiation with the Hessian congruence, and checks:

* a nonuniform unequal-rate alpha=2 triangle with extra incident edges;
* an alpha=2 four-cycle with a chord and attachments, including exact
  alternating cancellation;
* an attached equal-weight triangle at alpha=4/3, with summed scaled
  Fourier form 1/9>0;
* the boundary triangle with support weights (3/2,3/2) at alpha=2, whose
  full Jacobian is [[-2/3,-1/3,0],[-1/3,-2/3,0],[0,0,-1]];
* the bare-triangle spectra at alpha=5/4, 4/3 and 3/2;
* an explicit positive-probability finite path from unit to nonunit integer
  counts, and a length-two parallel-edge cancellation control.

For reproducibility, the unequal-weight triangle control has summed scaled
Fourier form 638279304/5076169 and cycle-inequality slack
180106104/5076169. The chord/attachment even-cycle form is 530; the parallel
pair form is 250. The prescribed unit-to-(2,4,3) path has exact probability
1/1591200. All arithmetic uses rational numbers, with the triangle sine
vector handled by a rational vector times sqrt(3)/2 and its quadratic
coefficient 3/4.

Negative controls reject a reversed Hessian sign, an odd-cycle assertion
below 4/3, strict stability at the critical triangle, a dropped attachment
denominator, a zero-count reachability claim, and a loop-as-forest claim.
These finite checks corroborate the analytic proof; they do not establish
the published foundational theorem, quantify all equilibria by computation,
or serve as a formal proof certificate. Reproduction runs use fresh copies
in ordinary, -O and -OO modes and do not execute captured scripts.

No central mathematical gap remains in the forest theorem as actually
stated for unit counts, finite simple loopless graphs, positive rates and
alpha>4/3. To match prescribed positive integer counts, add the finite-path
conditioning paragraph. Any claim to arbitrary positive real counts must
add its own stochastic bridge. Any claim including loops must be withdrawn
or reformulated. The equality endpoint and infinite-graph conclusions are
outside the accepted forest claim. Novelty, priority, and whisker correctness
are outside this family's finding.
