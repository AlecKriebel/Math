# Checkpoint 3 — Results, Applications, and Formal Verification

**Status:** accepted as formal verification after two adversarial reviews;
not empirical validation.

This checkpoint asks a narrower question than the rejected novelty gate:
does the proposed NCS framework make coherent, reproducible formal
comparisons and prospective falsifiable consequences across genuinely
different response mechanisms?

## 1. What survived the foundations audit

The following are retained as the common NCS modeling layer:

1. a presented category of externally equivalent intervention paths;
2. a stateful response functor into partial Lipschitz maps;
3. a directional empirical signature
   \[
   (A_\mu^+,A_\mu^-,C_\mu,V_{\mu,M});
   \]
4. explicit reset-versus-carry semantics;
5. a physical intervention-amplitude calibration;
6. presentation-conditioned exactification questions.

None of these is asserted to be a previously unknown mathematical ingredient.
The field-level proposal is that they form a useful common protocol theory for
questions now split among comparative statics, rewriting, variational
analysis, hybrid systems, online algorithms, and recourse.

## 2. Reproducible self-consistency checks

`examples/verify_revised_foundations.py` performs deterministic checks with a
fixed random seed. Its machine-readable output is
`examples/results/revised_foundation_checks.json`.

The verified statements are:

- **Partial guard robustness.** 7,447 randomly generated pairs met the strict
  margin premise; none changed guard membership. In a four-point
  distribution, actual downstream asymmetry and the two-sided state-dependent
  exposure were both \(0.25\).
- **Affine noninvertible rectification.** A square with zero linear parts on
  two edges had relation residual \(-0.42\). Moore--Penrose rectification
  reduced the residual norm to \(1.11\times10^{-16}\). One one-dimensional
  full-affine-gauge instance and split-weight duplicate-cell invariance were
  checked.
- **Configuration carry response.** At scale \(\lambda=2\), the two
  route endpoints were \((3,1)\) and \((2,2)\), with defect \(\sqrt2\).
  At truncation scale \(M=2\), the full point-mass signature was
  \((A_\mu^+,A_\mu^-,C_\mu,V_{\mu,M})=(0,0,0,1/\sqrt2)\).
- **Downstream failure conversion.** The constructed guard
  \(y\ge3/2\) rejected \((3,1)\) and accepted \((2,2)\). Both endpoint
  margins were \(1/2<\sqrt2\), satisfying the two-sided guard-exposure
  condition.
- **Online allocation.** The declared finite fibers and edge maps were
  evaluated.
  \(A\)-then-\(B\) failed, \(B\)-then-\(A\) succeeded, and the directional
  signature at the empty state was
  \((A_\mu^+,A_\mu^-,C_\mu)=(0,1,0)\).
- **Scaling sectors.** The script now constructs the smooth transport,
  sequential projection, and explicit constant-jump protocols. Estimated
  response orders were \(1.99505\), \(1\), and \(0\), respectively. The
  normalized smooth vector converged to \((-2,1)\), and fixed changes of
  state and amplitude units left its order unchanged.

These checks validate the formulas and implementation. They are not empirical
evidence from a deployed system and do not establish novelty.

## 3. Prospective tests and falsifiers

### Configuration protocol

One prospective experiment would calibrate the Euclidean edit cost and
single-policy carry maps at \(\lambda=1\), then withhold \(\lambda=2\) and
the final guard action. The model predicts

\[
AB:(3,1)\mapsto\text{guard failure},\qquad
BA:(2,2)\mapsto\text{guard success}.
\]

A different endpoint would falsify Euclidean projection or homogeneous
scaling. A different guard outcome would falsify the stated validation rule.
This split has not been performed on empirical data here.

### Allocation protocol

Compatibility, preference, and nonpreemption are declared protocol
assumptions in the worked model. A prospective calibration would require
forced-unavailability trials for compatibility and sequential trials for
nonpreemption, with the target pair withheld. The model predicts failure only
for the order in which the flexible job occupies server 1 first. Under an
explicit reservation policy that places \(A\) on server 2, or a migration
policy that moves \(A\) there when \(B\) arrives, both orders succeed. These
experiments have not been run here.

### Smooth protocol

For the constraint \(z-b_1x-b_2y=0\) and initial internal state \((1,2)\),
minimum-norm transport predicts the normalized two-order difference
\((-2,1)\). Numerical integration converges to that vector at second order.
A different limit falsifies the stated connection or transport convention.

## 4. Cross-domain value

The same four-part signature now distinguishes:

- finite carry residue with both routes feasible;
- conversion of that residue to a downstream one-sided failure;
- immediate one-sided failure in a discrete admission protocol;
- quadratic smooth holonomy versus linear active-set residue when the
  signature is measured as an amplitude-indexed family.

This supports formal cross-domain compatibility of a shared vocabulary. It
does not establish empirical portability or show that a dedicated field is
mathematically necessary.

## 5. Unresolved mathematical program

A novelty-bearing NCS result must go beyond the imported baselines. The most
promising targets are:

1. stability/rectification theorems for genuinely domain-changing partial
   functors;
2. dependence-sensitive laws for transported boundary exposure along
   competing paths;
3. regular-guard asymptotics linking value-defect order to
   failure-probability order;
4. invariance or controlled distortion under weighted presentation
   refinements;
5. inference bounds for learning a response assignment from open paths.

## 6. Checkpoint claim

Checkpoint 3 claims **reproducible arithmetic coherence, prospective
falsifiability, and formal cross-domain compatibility**. It explicitly does
not claim empirical validation, portability, or a new theorem beyond the
mapped literature. Advancement to the paper checkpoint requires a second
adversarial audit of the examples, implementation, and strength of these
claims.
