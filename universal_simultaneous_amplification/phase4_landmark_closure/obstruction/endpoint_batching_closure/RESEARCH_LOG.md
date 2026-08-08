# Research log: endpoint batching closure

## 2026-08-08 -- hostile search and exact event--Palm reduction

- Reconstructed the endpoint target

  \[
  m_D/m_C\le R_n,
  \qquad
  R_n={n-1\over n}{1-(2/3)^n\over1-(2/3)^{n-1}}.
  \]

- [NUMERICALLY OBSERVED] The true ratio stayed below the complete value on
  the frozen endpoint hostile corpus, including the exact dB-amplifying
  three-blade windmill.  It also stayed below the complete value on grouped
  clique--pendant rays, random dense three-class reversible blow-ups, and
  multi-scale weighted stars.  These screens are not proof.

- [PROVED] Introduced exact marked operators $J,H,S,N$.  The C pre-neutral,
  C post-neutral, and D locked-burst kernels are

  \[
  K_C=N_CR_C,
  \qquad K_R=R_CN_C,
  \qquad K_D=pJ(I-qS)^{-1}N,
  \]

  where $R_C=p(I-qJSH)^{-1}$, $p=2/3$, and $q=1/3$.

- [PROVED] If $\alpha_C,\alpha_D$ are the size-biased event Palm laws and
  $\beta_C=\alpha_CN_C$, then

  \[
  \beta_CK_R=\beta_C,
  \qquad \alpha_C=\beta_CR_C,
  \]

  and the locked-versus-refreshed difference has the full marked resolvent
  factorization

  \[
  K_D-K_R=pqJ(I-qS)^{-1}S(I-HJ)(I-qSHJ)^{-1}N.
  \]

- [PROVED] With $f(A)=1/|A|$ and the centered $K_R$-Poisson potential
  $g$, the batching inequality is equivalent to the single sign

  \[
  \alpha_D(K_D-K_R)g
  +\beta_C\{f-R_n^{-1}R_Cf\}\ge0.
  \]

  This retains all multi-rank burst jumps and cleanly separates target
  persistence from pre-/post-neutral timing only at the identity level.

- [EXACTLY FALSIFIED] The persistence term is not nonnegative.  The integer
  weighted four-vertex graph in `EVENT_PALM_RESOLVENT.md` makes it strictly
  negative over $\mathbb Q$, while the combined endpoint gap is positive.

- [EXACTLY FALSIFIED] The timing term is not nonnegative.  A small integer
  weighted five-vertex graph makes it strictly negative over $\mathbb Q$,
  while the persistence term and combined endpoint gap are positive.

- [OPEN] The paired sign itself.  The exact witnesses show that any closure
  must control cancellation between target-mark dispersion and event timing;
  neither contribution admits the natural separate sign.

- [PROVED REDUCTION / PRECISE OPEN CLASSICAL INEQUALITY] Applied the
  directed matrix-tree expansion to the recurrent nonfull event kernels.
  If $\tau_R,\tau_D$ are their positive rooted-arborescence cofactors,
  $\zeta$ is the normalized tree-root likelihood ratio, and
  $c=R_C(1/|A|)$ is the full resampled geometric-coverage cost, the target is

  \[
  \operatorname{Cov}_{\beta_C}(\zeta,1/|A|)
  \ge R_n^{-1}\mathbb E_{\beta_C}c
       -\mathbb E_{\beta_C}(1/|A|).
  \]

  Equivalently it is one comparison of two positive cofactor partition
  sums.  This is the irreducible surviving sign after the bounded closure
  cycle.

- [EXACTLY FALSIFIED] Rootwise positivity of the cofactor--coverage
  integrand.  Even on $K_4$, the integrand is $47/1092$ on a singleton and
  $-58/1365$ on a three-set, while its arborescence-root average is zero.
  Thus any tree proof must transport mass between roots; a root-preserving
  termwise injection is impossible even at equality.

- Extended verify_event_palm_resolvent.py.  It verifies the marked
  resolvent, stationary Palm transformations, Poisson identity, every
  directed-tree cofactor on the exact witnesses, the rootwise sign failure,
  both rational split failures, and an independent exact forward-chain
  reconstruction.
