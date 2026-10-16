# Claim and evidence scope

## Exact analytical claim

Let G be a locally compact, second countable, Hausdorff Abelian group. Let an arbitrary measurable ambient space Omega carry a jointly measurable G-action, let Q be sigma-finite, and let xi be a measurable, covariant, locally finite Radon random measure that is nonzero Q-almost everywhere. Then **full ambient invariance under every invariant, xi-preserving, xi-only measurable Markov transport kernel is equivalent to joint mass-stationarity of (Q, xi)**.

Here a Markov kernel has row mass one, not merely a bounded row mass. Its dependence is measurable with respect to sigma(xi) times the Borel sigma-field of G. Full ambient invariance means that for every nonnegative measurable ambient test f,

    integral Q(domega) integral T(omega,0,dt) f(theta_t omega)
      = integral Q(domega) f(omega).

The conclusion is joint mass-stationarity on the full ambient state, and in particular the joint Mecke reversal identity for every nonnegative measurable g on Omega times G:

    integral Q(domega) integral xi_omega(dt) g(theta_t omega,-t)
      = integral Q(domega) integral xi_omega(dt) g(omega,t).

The claim imposes **no standard Borel assumption on Omega, no sigma-finiteness assumption on the marginal law of xi, and no finite-intensity assumption**. Q(Omega) and xi(G) may be infinite. Atomic, diffuse, mixed, and periodic measures are included. The zero random measure, non-Abelian groups, and measures lacking local finiteness are outside this statement.

The analytical proof is distinct from these computations. Its mechanisms are finite-Q ambient tests and finite product-measure uniqueness using oriented xi-only gates away from measure periods, followed by normalized transports on the closed period subgroup and Haar invariance to obtain the remaining ambient reversal. Classical Mecke/Palm and mass-stationarity equivalences complete the argument. The project has recorded internal analytical acceptance of this exact claim; that record is not human refereeing, formal verification, or publication clearance.

## What the unchanged scripts check

| Script | Exact finite scope | Assertions |
| --- | --- | ---: |
| checks/turn1_checks.py | Cyclic groups of orders 1 through 5; nonzero counts in {0,1,2}; symmetric gates, Markov rows, spatial balance, exact rank determining the canonical Palm root law, stabilizer inversion. | 18,814 |
| checks/turn2_checks.py | Cyclic finite controls of marked ambient states and period kernels, plus historical isolated-pair matching and symbolic intensity-background Cox balance. | 75,172 |
| independent_review/independent_check.py | Independently constructed controls on Z2 x Z2 and Z3 x Z2; full marked orbits, all finite subsets in period kernels, multiplicities, historical symbolic Cox balance and Poisson coefficient identities. | 186,869 |

The last two scripts contain **legacy intensity-background Cox checks**. Their matching gates may see the background intensity measure as well as the count configuration. Those checks do not certify deterministic allocations that must see only the inserted Cox count configuration with xi erased, and do not establish that narrower converse. The general Markov theorem and that stricter Cox-allocation question have different test classes. No non-discrete strict allocation converse, arbitrary-auxiliary-state strict Cox theorem, or general sigma-finite strict Cox Markov extension is claimed by this package. The scripts remain byte-identical, so this explanation corrects interpretation rather than altering historical code or stdout.

Finite examples cannot prove the measure-theoretic identities for arbitrary measurable ambient spaces or infinite locally compact groups. The package contains no Lean, Coq, Isabelle, or other formal machine proof. It does not claim to settle every question in the Oberwolfach report.

## Credit and status

Author: **Alec Kriebel**, ORCID [0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). Discovery, checking, and manuscript preparation were extensively AI-assisted. The work remains unrefereed and has not received human peer review. No worldwide-firstness assertion or certification that the source question is currently open is made. This local candidate requires fresh whole-preprint reviews and project-owner integration before promotion.

The source credit below is inherited from the accompanying manuscript's checked bibliographic record, not a new literature audit by this package:

- J. Mecke, *Stationare zufallige Masse auf lokalkompakten Abelschen Gruppen*, 1967: classical background on Palm/Mecke identities.
- G. Last and H. Thorisson, *Invariant transports of stationary random measures and mass-stationarity*, Annals of Probability 37 (2009), 790–813, [doi:10.1214/08-AOP420](https://doi.org/10.1214/08-AOP420), checked electronic reprint [arXiv:0906.2062v1](https://arxiv.org/abs/0906.2062v1): joint Mecke/Palm equivalence (2.7), transport invariance Theorem 4.1, Palm/mass-stationarity Theorem 6.3, bounded weighted-kernel characterization Theorem 7.2, and the exact Markov question Problem 7.3. The present analytical contribution derives joint Mecke reversal from the restricted Markov hypothesis; these antecedents are credited inputs.
- G. Last and H. Thorisson, *Characterization of mass-stationarity by Bernoulli and Cox transports*, 2011, [doi:10.31390/cosa.5.2.01](https://doi.org/10.31390/cosa.5.2.01): important discrete and aperiodic partial predecessors (Propositions 3.6 and 3.8), periodicity qualification (Remark 3.11), and a separate averaged-Cox question (Remark 4.8).
- G. Last and H. Thorisson, *Construction and characterisation of stationary and mass-stationary random measures on R^d*, retained author version [arXiv:1405.7566v2](https://arxiv.org/abs/1405.7566v2): positive-density partial result (Theorem 6) for the joint pair ((X,Z),xi), under its line-integrability and half-line divergence assumptions; this citation is not an xi-only test characterization. The complete final journal body was not checked in the underlying audit and is not asserted identical.
- *New Perspectives in Stochastic Geometry*, Oberwolfach Report 47/2008, [doi:10.4171/OWR/2008/47](https://doi.org/10.4171/OWR/2008/47): distinct general Markov discussions at pp. 2692, 2694 and narrower deterministic Cox-allocation question at p. 2673.

This preparation makes no claim of a complete priority search. Primary-source PDFs and private audit evidence are deliberately outside the public payload.
