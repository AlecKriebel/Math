# Torsion for arbitrary subsets of R³: a compact-witness and neighborhood-kernel reduction

Problem3415 / OPG-37151. **Unsolved**. The question concerns a nonidentity element of finite order in an ordinary fundamental group of an arbitrary subset of R³. No manifold, local contractibility, or semilocal simple connectivity hypothesis is part of that target.

## Source audit and necessary correction

The [Open Problem Garden post](https://www.openproblemgarden.org/op/torsion_for_subsets_of_mathbb_r_3) matches the pinned problem. However, its blanket homology sentence must not be used as a theorem about arbitrary singular homology. In the [original expert discussion](https://mathoverflow.net/questions/4478/torsion-in-homology-or-fundamental-group-of-subsets-of-euclidean-3-space), the author explicitly acknowledges overstatement after the distinction between singular, Čech and Steenrod theories is raised. Consequently this package does not assert that any hypothetical torsion must lie in the commutator subgroup without an additional valid singular-H₁ theorem.

The same discussion contains Moishe Kohan's 2021 proof that semilocally simply connected subsets have torsion-free fundamental groups. Its small-loop filling step uses that hypothesis; it is not an unrestricted solution. The finite disk-image and neighborhood reasoning below is closely related to that posted argument and is not claimed as new.

For the ambient open-set input, [Kauranen–Luisto–Tengvall, arXiv:1904.12645](https://arxiv.org/abs/1904.12645), Proposition3.4 in the downloaded version, states that domains in R³ have torsion-free fundamental groups, attributing this to Papakyriakopoulos. The journal version is *Bull. London Math. Soc.*54(2022),145–160, DOI10.1112/blms.12565; its numbering differs. We use precisely the domain statement, not a theorem for arbitrary subsets.

## 1. Every possible counterexample has a compact Peano witness

**Proposition1.** If some X⊂R³ has an element of order n>1 in π₁(X,x₀), then a compact path-connected locally path-connected subset Y⊂X has an element of exactly that order. Indeed Y can be chosen as the image of one disk map.

Proof. Represent the element by a loop γ:S¹→X. Let q_n:S¹→S¹ be the degree-n map. The equality [γ]^n=1 supplies a continuous h:D²→X with boundary γ∘q_n. Set Y=h(D²). Since q_n is onto, the entire image of γ lies in Y. Thus γ is a loop in Y and γ^n is nullhomotopic there. If any smaller positive power were trivial in Y, its image would be trivial in X, contrary to the exact order n. Therefore γ still has order n in π₁(Y,x₀).

The set Y is a compact metrizable connected space. A continuous surjection from [0,1] onto D², followed by h, is a surjection onto Y. The Hahn–Mazurkiewicz characterization makes Y a Peano continuum, hence locally connected and locally path-connected. These statements do not imply local simple connectivity, an ANR property, or existence of a regular neighborhood. ∎

So noncompactness and total disconnectedness are not essential escape routes. The unresolved question persists among compact Peano continua embedded in R³.

## 2. Any torsion witness is invisible in every ambient neighborhood

Let Y be the compact witness above and U_k={z∈R³:dist(z,Y)<1/k}. Each U_k is open and path-connected: it is a union of balls around the path-connected set Y, and each point can first be connected to a point of Y. It contains the basepoint and all of Y.

**Proposition2.** The class [γ] maps to the identity under every inclusion π₁(Y,x₀)→π₁(U_k,x₀).

Proof. Its image has order dividing n because γ^n bounds the same disk h in U_k. The domain theorem makes π₁(U_k) torsion-free. Hence its image is trivial. ∎

Define the neighborhood map

J:π₁(Y,x₀)→lim← π₁(U_k,x₀)

using inclusions and the fixed basepoint. The inverse limit is torsion-free: a finite-order element has finite-order coordinates in torsion-free groups, so every coordinate is the identity. Proposition2 says more explicitly that all torsion of π₁(Y) lies in ker J.

**Corollary3.** If J is injective, π₁(Y) is torsion-free. In particular, a counterexample must have a nontrivial neighborhood-invisible finite-order loop. Proving only that all neighborhood groups are torsion-free does not prove J injective or its kernel torsion-free.

This formulation avoids assuming that singular fundamental groups commute with inverse limits. It also does not assert that a nontrivial kernel necessarily contains torsion.

## 3. Why the common approximation steps are insufficient

For each k, γ bounds a disk in U_k. These disks need not have any uniform continuity modulus, bounded complexity, or coherent choice as k varies. Merely taking smaller neighborhoods supplies no convergent disk map into Y. Such convergence would be the missing conclusion, not a consequence of compactness of the images alone.

If Y retracts from an open neighborhood U, inclusion induces an injection on π₁ because the retraction is a left inverse. The domain theorem then rules out torsion. This verifies the neighborhood-retract case directly, but no such retraction exists by definition for an arbitrary subset.

The Griffiths twin cone illustrates why replacing the kernel by zero is a substantive error. [Jeremy Brazas's description](https://wildtopology.com/bestiary/griffiths-twin-cone/) records an embedded compact locally path-connected example with nontrivial fundamental group and trivial shape. It also records its group as torsion-free, so this example does not answer the question affirmatively. We use it only as a published expert example warning against automatic injectivity, not as a newly audited infinite-word construction.

## Exact surviving problem and controls

It is enough to construct a compact Peano continuum in R³ with a nonidentity finite-order element in its neighborhood-map kernel, or to prove that such kernels contain no finite-order elements. This package does neither. Two substantive routes were examined: compact disk-witness reduction and ambient-neighborhood approximation. Both stop at that exact kernel problem. Proposed status: unsolved,2/5 approaches.

No numerical experiment is offered as evidence for a wild embedding or torsion-freeness theorem. The accompanying verification checklist distinguishes the proved reductions, imported domain theorem, posted semilocal theorem and unresolved assertions. Source-audit/reduction completion100%; full target completion0%. No novelty or human peer review claim. Runtime: inherited runtime, exact model identifier not exposed; no model/reasoning switch made.
