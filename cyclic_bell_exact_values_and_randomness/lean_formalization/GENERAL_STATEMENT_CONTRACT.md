# All-dimensional continuation statement contract

Recorded before new proof source. Status: intended statements and scope, not certification.
Canonical manuscript blob remains `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
The incoming d=4 physical definitions, score constants, endpoints, and pins are retained.
No manuscript or qubit-project change is part of this continuation.

## Index and Fourier contract

For arbitrary d >= 2 use ZMod d (all residues, not prime d). The character is
Mathlib's actual `ZMod.stdAddChar`, equal to exp(2*pi*i*j/d). Our forward
transform has the manuscript's PLUS sign; Mathlib `ZMod.dft` has MINUS sign.
The bridge is `fourier q m = ZMod.dft q (-m)`. No primality or field hypothesis
is permitted. Autocorrelation is R(t)=sum_j q(j+t) conjugate(q(j)).
Power spectrum is |fourier q m|^2, and R(t)=d^-1 sum_m P(m) chi(-m*t).
The target table uses m=-(a+b), not a-b, with prefactor d^-3.

## Physical model and construction contract

Local spaces are arbitrary finite complex coordinate spaces, represented by
finite types with computational bases. Mixed states are PSD trace-one matrices;
measurements are d orthogonal PSD idempotents summing to identity, including
zero effects. Encoded observable is sum_a chi(a) M_a. Tensor placement and Born
rule are the entry formulas of the existing model, generalized in dimension.
The constructive space is indexed by ZMod d. Phi_d has amplitude 1/sqrt(d) on
the diagonal. u_a(j)=chi(-a*j)/sqrt(d). Given unimodular cycle weights of product
one, q_0=1 and q_{j+1}=w_j q_j; projectors are those of diag(q)u_a.
Validity does not include a score bound, optimality, or a prescribed table.

## Intended theorem families

1. `eq:weighted-cycle`, `eq:q-sequence`: arbitrary-d weighted-cycle construction,
   order d, explicit projectors and their observable encoding.
2. `eq:target-table`: Born/DFT identity; normalization, uniform marginals,
   Fourier/autocorrelation equivalence; fixed-pair guessing obstruction.
3. `eq:R2`, `thm:biased`: final-two swap, canonical flatness, nonzero lag-two
   autocorrelation, quantitative probability gap; do not infer maximality from
   these distribution facts alone.
4. `thm:permutation`: first-harmonic permutation invariance and constructive
   attainment under the theorem's actual unimodular/product hypotheses. Separate
   this from the universal polar-linear bound and its physical instantiation.
5. `eq:second-sos`: dimension-independent SOS with coefficient normalization,
   then actual lambda coefficient bridge and physical witness instantiation.
   A theorem assuming normalized coefficients is a generic helper, not the
   actual-family endpoint unless that assumption is explicitly discharged.
6. `lem:scalar`, `thm:exact`, `cor:first-augmented`: scalar roots-of-unity extremum,
   equality set, arbitrary-strategy operator and physical bound. A scalar lemma
   or conditional spectral/certificate lemma is not the whole value theorem.
7. `eq:support-cancellation`, `thm:support-rigidity`, `lem:reflection-rank`:
   preserve support cancellation, state-induced invariance, kernel-safe polar
   cancellation, spectral restriction, adjacency-to-reflection, order-d on
   support, and the rank argument as distinct milestones. The rank argument
   alone never certifies the support-multiplicity endpoint.
8. `thm:binary-benchmark`, `lem:private-mub`, `prop:one-input`, operator-valued
   Fourier inversion: preserve physical purification/Eve interfaces; do not
   replace operator privacy with scalar uniformity.
9. `prop:mub`: scoped coefficientwise exposure obstruction only; no broader
   setting-complexity no-go is claimed.

## Certification and audit contract

All new proofs are source candidates pending Lean 4.19.0 + exact Mathlib pin.
No sorry/admit/custom mathematical axiom/native_decide/unsafe proof evaluation.
No claim of clean rebuild or executed #print axioms. Standard choice/propext/
Quot.sound are allowed only as reported by the future kernel audit.
Every source declaration in the production graph gets an axiom query, and all
claimed endpoints and statement audit files must be reachable from the standard
build. Unfinished routes remain separate, explicitly conditional, or outside
that graph; coverage may not hide unresolved mathematical hypotheses.

Update at the end of this source pass: separate arbitrary-Hilbert first and
second operator/PVM upper-bound candidates are now written in GeneralCommuting
and GeneralSecondCommuting. They do not depend on finite-dimensional bounds.
However, the complete q/qa/qc behavior-set embedding, closure and supremum
assembly remains unwritten. Complete maximizing-face classification and
worst-case guessing optimization remain unclaimed. Finite witnesses alone
are not used to infer upper bounds in the larger models. Manuscript open questions are
not formalization targets to be silently promoted to theorems.


## End-of-pass source status (not a new certification)

The current coverage map includes physical all-d finite counterexamples,
actual-support rigidity, arbitrary-Hilbert PVM upper bounds, physical Eve
interfaces, binary saturation privacy, one-input perfect guessing, sufficient
private-MUB composition and computational-MUB exposure. Every such statement
is still uncompiled. `COVERAGE.md` is authoritative for remaining mathematical
source gaps and conditional-versus-unconditional statement boundaries.
