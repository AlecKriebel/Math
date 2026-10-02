# Final five-turn result: scaling in the standard addition model

**Original intended physical question: unsolved5/5.** Full independent review
of the new physical partials is pending. No claimed-solved promotion is proposed.
The exact displayed normalization in the source has a separately reviewed
counterexample; that correction is not a resolution of all correctly normalized
physical regimes.

## Two distinct dispositions

1. **Literal source normalization:** COUNTEREXAMPLE.md disproves the displayed
   universal scaling at p=1/4,alpha=1,omega=0 using actual infinite solutions
   and a time-integrated fixed-ray mass contradiction. It works under both
   the printed birth coefficient and the primary standard addition coefficient.
   The independent verdict in independent_review_turn1/ is
   PASS_COMPLETE_LITERAL_DISPLAYED_NORMALIZATION_COUNTEREXAMPLE. Its proof,
   original manifest and seven review files are unchanged.
2. **Intended standard physical model:** the continued four substantive turns
   prove the scoped analytic results below. They do not settle the source's
   full parameter/initial-data range or establish a universal corrected
   formulation. This is the reason for the final unsolved5/5 disposition.

## Actual physical partials

The standard model uses birth(j-1)^p and loss j^p, with p<1 and input
alpha t^omega, alpha>0,omega>-1/2. Put beta=omega+1 and d=beta(1-p).

- TURN_2.md derives the exact exponential-sum transport representation in the
  monomer clock. Conditional on f(tau)~C tau^(-r), it proves the off-front
  profile with size sigma=[(1-p)tau]^(1/(1-p)), unweighted amplitude exponent
  q=p+(1-p)r and normalization1/[C(1-p)^r]. It does not assume or prove the
  nonlinear monomer asymptotic for all parameters.
- TURN_3.md proves the actual nonlinear constant-input, zero-data regime
  1/2<p<1, including a finite positive limiting cluster number, the monomer
  asymptotic, off-front profile and weak leading-mass front atom. It is a
  special case of the next result, retained as its own substantive turn.
- TURN_4.md proves the strict **finite-cluster regime**0<p<1,d<1/2 for zero
  data. TURN_5.md extends it to every nonnegative finite-support initial datum.
  Write kappa=alpha/beta and let N_infinity be the limiting higher-cluster
  number, including initial higher clusters. Then

      0<N_infinity<infinity,
      sigma(t)~(kappa/N_infinity)t^beta,
      c_1(t)~alpha^(1-p)beta^p N_infinity^(p-1)t^(d-1).

  The off-front exponent is r=1/d-1 and the amplitude exponent is
  q=2p-1+1/beta. Leading mass concentrates weakly at the front. This is an
  actual-solution theorem, obtained through a finite monomer-bound bootstrap,
  cohort moments and scalar ODE comparison, not an assumed scaling ansatz.
- TURN_5.md proves the **critical constant-input case p=1/2**, also extended
  to finite-support initial data:

      N(t)~sqrt(2alpha log t),
      c_1(t)~2^(-1/4)alpha^(1/4)t^(-1/2)(log t)^(-1/4),
      sigma(t)~sqrt(alpha/2)t/sqrt(log t).

  Along j/sigma(t)->eta!=1, t c_j(t) tends to
  eta^(-1/2)/(1-sqrt(eta)) for0<eta<1 and to0 for eta>1.
  Leading normalized mass converges weakly to a front atom. The proof does
  not integrate that singular bulk profile through eta=1.
- Finite-support data also give a precise memory obstruction: in the strict
  regime N_infinity is at least the initial higher-cluster number, so a single
  initial-data-independent positive size coefficient cannot fit all such data.
  This does not refute data-dependent self-similarity, which is proved there.

These analytic partials are author deductions pending full independent audit.
No historical novelty or source-author acceptance is claimed. The model, prior
constant-kernel results and source context retain their published credit.

## Remaining gaps

The region d>1/2 outside credited known cases, the rest of the critical line
and the source's full infinite polynomial-tail initial-data class are not
settled. A pointwise front-layer theorem is also open but is **not required**
by the source's eta!=1 claim. The reported formal parameter range and implicit
constants cannot be silently repaired into an unproved global theorem.

The exact final scope and proof dependencies are in PROOF_COLLECTION.md.
FINAL_FROZEN_MANIFEST.json is the aggregate freeze. FROZEN_MANIFEST.json,
README.md and REVIEW_REQUEST.md are preserved first-turn artifacts, not the
current disposition. The numbered turn manifests and ledgers preserve the
chronology, including the explicitly documented administrative event-field copy.
All five genuine substantive turns are recorded; no sixth proof turn is proposed.

Only portable research files are included. Complete primary PDFs remain in the
separate reading cache. Final publication requires independent review and the
publication gate, with one draft PR and only this target's QUEUE row changed.
