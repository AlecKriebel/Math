# Literature Collision Map

**Search date:** 2026-07-28  
**Purpose:** distinguish the proposed deletion-order falsifier from established
machine-unlearning, auditing, path-dependence, metamorphic-testing, and
kernel-testing results.

Absence from this map is not evidence of global priority.

## Direct deletion-order collision

### Kumar, Nadimi, and Gogineni (2026)

- **Work:** *On the Path Dependence of Gradient Ascent-Based Unlearning*
- **URL:** https://openreview.net/pdf?id=4YNW5rZ2Vd
- **Collision:** directly studies different orders of the same forget samples,
  reports distinct forgetting/retention outcomes, and gives the familiar local
  second-order Hessian-gradient defect.
- **Consequence:** this project cannot claim to discover deletion-order
  dependence or the local commutator formula.

## Training-history path dependence

### Yu, He, Goyal, and Arora (2025)

- **Work:** *On the Impossibility of Retrain Equivalence in Machine Unlearning*
- **URL:** https://arxiv.org/abs/2510.16629
- **Collision:** proves that path-oblivious local unlearning cannot universally
  recover retrain equivalence across different original training-stage
  histories.
- **Distinction:** this project holds one trained checkpoint fixed and swaps
  post-training deletion requests.

## Existing retraining-free audits

### Ye et al. (2026)

- **Work:** *Auditing Machine Unlearning: A Systematic Research on Whether
  Models Truly Forget*
- **URL:** https://arxiv.org/abs/2606.16110
- **Collision:** claims a practical general-purpose audit without a full
  retraining baseline.
- **Distinction:** it trains and refines a verification model on a subset of
  retained data. The proposed permutation-cell audit trains no comparator and
  supplies only a sound rejection certificate.

### Ribero, Schrab, and Gretton (2026)

- **Work:** *Regularized \(f\)-Divergence Kernel Tests*
- **URL:** https://arxiv.org/abs/2601.19755
- **Collision:** develops level-controlled kernel tests and applies relative
  distribution tests to machine unlearning.
- **Distinction:** the proposed result uses a simple bounded-kernel MMD lower
  confidence bound on the distance between deletion-order laws, then converts
  that cell distance to a necessary common-target error. It does not claim a
  new two-sample test.

## Certified, sequential, and adaptive unlearning

### Guo et al. (2020)

- **Work:** *Certified Data Removal from Machine Learning Models*
- **URL:** https://proceedings.mlr.press/v119/guo20c.html
- **Collision:** Newton-style removal, influence interpretation, batch removal,
  and accumulated residual bounds.

### Neel, Roth, and Sharifi-Malvajerdi (2021)

- **Work:** *Descent-to-Delete: Gradient-Based Methods for Machine Unlearning*
- **URL:** https://proceedings.mlr.press/v132/neel21a.html
- **Collision:** long update sequences and formal deletion guarantees for
  convex models.

### Gupta et al. (2021)

- **Work:** *Adaptive Machine Unlearning*
- **URL:** https://arxiv.org/abs/2106.04378
- **Collision:** adaptive sequences of deletion requests and reductions from
  adaptive to non-adaptive guarantees.
- **Distinction:** adaptively selected requests may not be externally
  equivalent under permutation; the proposed cell test assumes a fixed,
  non-adaptive deletion set.

### Zhang et al. (2024)

- **Work:** *Towards Certified Unlearning for Deep Neural Networks*
- **URL:** https://proceedings.mlr.press/v235/zhang24l.html
- **Collision:** inverse-Hessian approximation and sequential unlearning.

### Chourasia and Shah (2023)

- **Work:** *Forget Unlearning: Towards True Data-Deletion in Machine Learning*
- **URL:** https://proceedings.mlr.press/v202/chourasia23a.html
- **Collision:** shows that cached computations and repeated releases create
  privacy issues and develops stronger deletion semantics.

### Izzo et al. (2021)

- **Work:** *Approximate Data Deletion from Machine Learning Models*
- **URL:** https://proceedings.mlr.press/v130/izzo21a.html
- **Collision:** influence approximations, batch deletion, and exact quadratic
  Sherman--Morrison--Woodbury updates.

### Warnecke et al. (2023)

- **Work:** *Machine Unlearning of Features and Labels*
- **URL:** https://mlsec.org/docs/2023-ndss.pdf
- **Collision:** influence-based sequential updates and intermediate Hessian
  recalculation.

## Influence functions and second-order effects

### Koh and Liang (2017)

- **Work:** *Understanding Black-box Predictions via Influence Functions*
- **URL:** https://proceedings.mlr.press/v70/koh17a.html
- **Collision:** scalable influence-function calculations using gradients and
  Hessian-vector products.

### Basu, Pope, and Feizi (2020)

- **Work:** *Influence Functions in Deep Learning Are Fragile*
- **URL:** https://proceedings.mlr.press/v119/basu20b.html
- **Collision:** higher-order and group influence issues limit any novelty
  claim for symmetric second-order corrections.

## Auditable definitions and oracle limits

### Thudi et al. (2022)

- **Work:** *On the Necessity of Auditable Algorithmic Definitions for Machine
  Unlearning*
- **URL:** https://www.usenix.org/conference/usenixsecurity22/presentation/thudi
- **Collision:** parameter/output proximity cannot alone prove that data were
  absent from a training trajectory.
- **Consequence:** a zero permutation defect cannot certify forgetting.

## Metamorphic testing

### Segura et al. (2016)

- **Work:** *A Survey on Metamorphic Testing*
- **DOI:** https://doi.org/10.1109/TSE.2016.2532875
- **Collision:** oracle-free testing through relations among multiple program
  executions is established.
- **Distinction:** this project does not claim oracle-free relational testing
  as new. NCS identifies the Boolean-cube path presentation, supplies the
  failure-aware signature, and connects a relation-cell defect to a sharp
  common-target lower bound.

### Yang and Yeung (2026)

- **Work:** *Unlearning as Distribution Restoration: A Controlled
  Counterfactual Study, a Validated Selective Screen, and the Limits of
  Oracle-Free Certification*
- **URL:** https://arxiv.org/abs/2607.19442
- **Collision:** independently emphasizes that oracle-free consistency checks
  are generally necessary screens rather than sufficient certificates.
- **Consequence:** this supports, but does not originate, the project's
  one-sided warning.

### RULER (2026)

- **Work:** *RULER: Representation-Level Verification of Machine Unlearning*
- **URL:** https://arxiv.org/abs/2605.27569
- **Collision:** provides an oracle-free representation diagnostic.
- **Distinction:** it does not compare deletion permutations or derive a
  common-center radius bound.

### Kernel tests of equivalence (2026)

- **Work:** *Kernel Tests of Equivalence*
- **URL:** https://arxiv.org/abs/2603.10886
- **Collision:** MMD tolerance/equivalence testing is already current prior
  art.
- **Consequence:** the stochastic result must be positioned as the NCS
  conversion of a valid lower confidence bound, not as a new kernel
  equivalence test.

## Kernel two-sample distance

### Gretton et al. (2012)

- **Work:** *A Kernel Two-Sample Test*
- **URL:** https://www.jmlr.org/papers/v13/gretton12a.html
- **Collision:** MMD, characteristic-kernel two-sample testing, and
  finite-sample analysis are established.
- **Consequence:** the project derives only the concentration constant needed
  for its NCS target-error conversion; it does not claim a new kernel test.

## Surviving positioning gap

No mapped primary source was found that combines all of the following:

1. two or more orders of the **same fixed deletion set** as an NCS relation
   cell starting from one checkpoint;
2. the sharp Chebyshev/half-diameter lower bound against **every common
   retraining target**;
3. a level-controlled distributional rejection rule derived from that bound;
4. an affine-basis completeness audit for all-order affine deletion operators;
5. explicit one-sided language that agreement supplies no positive deletion
   certificate.

This is a promising positioning gap, not proof of priority or of publishable
depth.
