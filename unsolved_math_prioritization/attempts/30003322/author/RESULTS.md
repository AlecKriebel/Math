# Set sized models of initial surreal substructures

## Outcome and scope

Problem 30003322 / OWR-15181-014 remains unresolved in this attempt. Five distinct approaches were tried. The results below are proved reductions and counterexamples to tempting intermediate assertions, not a solution of either requested universal theorem. No novelty claim is made.

The intended target is understood for consistent first-order theories, identified up to deductive equivalence. The group language is {0,+,<=}; the field language is {0,1,+,*,<=}. An initial copy must preserve the indicated algebra and order, and its image must contain every simplicity predecessor of each of its members. It is not enough to have an order embedding or an ordinary field embedding. No exponential, analytic, differential, or named-constant expansion is part of the target.

The question is whether the following implications have proofs in NBG using set-universe models: if every set model of a consistent theory extending nontrivial densely ordered abelian groups has an initial group copy in No, the theory is equivalent to the complete theory of nontrivial divisible ordered abelian groups; analogously, for ordered fields, the theory must be equivalent to the complete theory of real-closed ordered fields. Consistency excludes a vacuous inconsistent-theory objection, and equivalence excludes artificial differences between axiom lists.

## Primary source alignment

Kaplan's contribution to the Oberwolfach report, printed page 3358, Theorem 6 and Question 2, separates a theorem allowing class models from the question about using only set universes. Ehrlich and Kaplan's full paper gives the corresponding Theorem 8.1 and Question 8.1 in Section 8. Its proof builds an ordinal-length elementary chain whose union has a proper-class universe. Replacing that union by a set stage is precisely the point that needs justification.

The definitions, Hahn-group criterion (Theorem 5.1), field criterion recalled in the introduction, and the explicit open question were inspected in the authors' PDF. The later exponential-field paper concerns an expanded language and does not establish this set-model converse. The Rangel–Mariano paper studies a different algebraic/categorical set-theory programme. No later primary resolution was located in this search.

## Approach 1  Truncate the class saturation proof

For an infinite cardinal kappa, say that an ordered set has the kappa-cut property if every pair L<R of subsets of size less than kappa has an element strictly between them; either side may be empty. Write No_{<kappa} for sign sequences of ordinal length less than kappa.

**Proposition 1.** If an initial subclass G of No has the kappa-cut property, then No_{<kappa} is contained in G.

**Proof.** Induct on the length alpha<kappa of a sign sequence s. Every proper prefix of s belongs to G by induction. Partition these prefixes into L, those smaller than s, and R, those larger than s. Both have size less than kappa. The cut property gives y in G with L<y<R. In the sign-sequence tree, s is a prefix of every sequence strictly between all its left and right prefixes. To check this directly, the first disagreement before alpha would violate the inequality with the prefix at that disagreement; termination before alpha would equal one of the required strict bounds. Thus s is a prefix of y. Initiality puts s in G. This includes alpha=0, when the cut is empty on both sides. QED.

First-order kappa-saturation of a densely ordered structure implies this order-cut property: the inequalities form a finitely satisfiable type over fewer than kappa parameters. Proposition 1 therefore applies to an initial image of such a model.

**Exact obstruction.** The conclusion is containment, not equality. The image may have elements with birthdays at least kappa. For a set G the function assigning birthdays has set range, so the birthdays are bounded by an ordinal, but that bound depends on the image; it is not forced below the preselected saturation cardinal. At a missing node of length at least kappa, its full predecessor cut can require at least kappa parameters. Saturation over smaller parameter sets does not apply. Making a new model more saturated gives a new embedding with a new birthday bound. No uniform bound, coherent embedding system, or legitimate fixed point was obtained.

**Control.** Finite prefix-closed trees exhibit the elementary distinction between containing all levels below a bound and being closed under nodes at the bound. The finite check supplied with this note tests this distinction only; it is not evidence of a set-theoretic independence result.

## Approach 2  A dyadic subgroup obstruction and omitted types

Let D=Z[1/2] denote the additive group of dyadic rationals.

**Proposition 2.** Every nontrivial dense initial subgroup G of No contains the canonical D.

**Proof.** Some positive element lies in G. The one-sign sequence +, representing 1, is its prefix or is that element, so 1 belongs to G. Suppose 2^{-n} belongs to G. By density choose x in G with 0<x<2^{-n}. The sign sequence for 2^{-n} is a plus followed by n minuses. Every positive sequence smaller than it begins with a plus followed by at least n+1 minuses: an earlier plus, or earlier termination, would make it at least 2^{-n}. Therefore 2^{-(n+1)} is a prefix of x and belongs to G. Induction and additive closure give D. QED.

Consequently an abstract dense ordered abelian group admitting an initial copy has a nonzero element divisible by every power of 2, and in fact contains a subgroup isomorphic to D. The preimages of 2^{-n} provide a compatible division tower. Torsion-freeness makes the tower unique once its first element is fixed.

**Corollary 2.1.** For an odd prime p, the ordered group Z[1/p] is not isomorphic to an initial subgroup of No.

**Proof.** It is dense: powers p^{-n} yield arbitrarily fine rational meshes. If a nonzero a=m/p^r were divisible by 2^n inside Z[1/p] for every n, the equation a=2^n b/p^s would force 2^n to divide m, since p is odd. This is impossible for nonzero m. Apply Proposition 2. QED.

This recovers the odd-prime example already noted by Ehrlich and Kaplan; it is not a new solution.

**Conditional model-theoretic reduction.** Consider the partial one-variable type
p_2(x)={x>0} union {there exists y with 2^n y=x : n>=1}.
If a consistent complete countable theory U extending the dense ordered-group axioms has this type inconsistent or nonprincipal, then U has a countable model with no initial copy. In the inconsistent case every model omits it. In the nonprincipal case apply the standard countable Omitting Types Theorem and Proposition 2. The same supplies a countermodel to any weaker T contained in U.

**Exact obstruction.** In a 2-divisible theory the type is isolated by x>0; it cannot be omitted. D itself is initial and not 3-divisible. Thus the obstruction does not cover theories already imposing 2-divisibility but failing another divisibility axiom. The assertion that every relevant theory has a suitable nonprincipal type was not proved.

## Approach 3  Coefficients and truncations do not imply divisibility

Here is an explicit family refuting a possible shortcut through the Hahn description.

Put t=omega^{-1}, H=R[t] considered only as an additive group, and x=sum_{n>=0} t^n. For any additive subgroup A of R define
G_A=H+A x.
These are Hahn series, or equivalently their canonical surreal normal forms. The expression x is well-defined because 0,-1,-2,... is a decreasing sequence of exponents.

**Proposition 3.** G_A is a set-sized dense initial subgroup of No. Every one of its monomial coefficient groups is R. As abstract additive groups, G_A/H is isomorphic to A. In particular G_Z is not divisible, while G_D is 2-divisible but not 3-divisible.

**Proof.** A series belongs to G_A precisely when its coefficient sequence on exponents 0,-1,-2,... is eventually constant with eventual value in A. Arbitrarily chosen finitely many exceptional coefficients may lie in R. This proves additive closure.

The exponent set Gamma={-n:n>=0} is initial in No: every prefix of the negative integer -n is another such integer (or 0). All real scalar monomials r t^n lie in H. Every proper normal-form truncation of a member of G_A has finite support, unless the member already has finite support, in which case the same conclusion holds. Indeed a nonzero eventual coefficient produces support of order type omega, whose proper initial segments are finite. Thus G_A is truncation closed and cross sectional. Its coefficient groups are R, which are initial and contain D. Ehrlich–Kaplan Theorem 5.1 now proves initiality.

For positive g in G_A with leading term c t^k, c>0, the monomial (c/2)t^k lies strictly between 0 and g. Translation proves density.

The eventual-coefficient map G_A -> A is a surjective homomorphism with kernel H, so the quotient claim follows. H is divisible. More explicitly, the only possible solution of n y=x in the ambient Hahn group is x/n; it belongs to G_A exactly when 1/n lies in A. For A=Z this fails for n=2. For A=D every element can be halved, but x cannot be divided by 3. QED.

The quotient here is an algebraic quotient; H is not claimed convex.

**Exact obstruction.** Even full real coefficient groups, all monomials, initiality, and truncation closure leave a divisibility defect in a completed infinite support. Finite truncations of x/n are all in H although x/n need not be in G_A. It would be invalid to promote coefficientwise divisibility to closure under the entire resulting series.

These examples are not asserted to be saturated as ordered groups or even to have any uncountable order-cut property. No assertion that all models of Th(G_A) admit initial copies follows.

## Approach 4  Residue fields and divisible value groups do not imply real closure

Consider the directed union
F=union_{n>=1} R(omega^{1/n}) inside No.
It is a field since the terms indexed by n and m both lie in the term indexed by lcm(n,m).

**Proposition 4.** F is an initial subfield of No with coefficient field R and exponent group Q, but F is not real closed.

**Proof.** Its canonical Hahn embedding is into R((t^Q)), where powers are ordered by decreasing exponent. It contains every omega^q, q rational. Each element is a rational function in u=omega^{-1/n} for some n. Its Laurent expansion at u=0 has integer exponents bounded below, so in descending surreal exponent order its support is finite or of order type omega. Every proper truncation is a finite Laurent polynomial and lies in R(u), hence in F. Thus F is truncation closed and cross sectional. Q is an initial subgroup of No: it contains D, and the simplicity predecessors of a real number are dyadic rationals (with the dyadic case terminating at finite length). The initial-field criterion recalled in Ehrlich–Kaplan therefore makes F initial.

Suppose F contained a square root of 1+omega^{-1}. That root would lie in R(omega^{1/n})=R(u) for some n, so 1+u^n would be a square in R(u). The polynomial 1+u^n is squarefree: its derivative is n u^{n-1}, and no common nonconstant divisor is possible because its constant term is 1. It is nonconstant and has an irreducible factor with exponent one. The order at that factor of a square rational function must be even, contradiction. The element 1+omega^{-1} is positive, so F is not real closed. QED.

**Proposition 4.1.** F has an explicit integer part.

Let I consist of all finite sums c+sum_i r_i omega^{q_i}, with c in Z, r_i in R, and positive rational exponents q_i. Then I is a subring of F; positive nonconstant elements exceed every integer, and positive constant elements are positive integers. Hence 1 is its least positive element.

For a in F, the Laurent expansion has only finitely many positive surreal exponents. Write a=P+c+epsilon, where P is its positive-exponent part, c is real, and epsilon is infinitesimal. If c is not an integer, put z=P+floor(c); then z<=a<z+1. If c is an integer and epsilon>=0, use z=P+c. If c is an integer and epsilon<0, use z=P+c-1. In each case z belongs to I and brackets a as required. QED.

**Exact obstruction.** Real coefficients, a divisible exponent group, and an integer part do not force a particular initial field to be real closed. The known integer-part obstruction can exclude certain theories only when one constructs a model of that exact theory without an integer part. Neither the examples here nor the cited n-real-closed-field results provide such a model for every non-RCF theory. Henselian/algebraic closure and preservation of the original complete theory remain unproved steps.

## Approach 5  Closure, reflection, and compactness

**Proposition 5.** Every set S of surreal numbers is contained in a set-sized initial subfield of No.

**Proof.** Start with S_0=S union {0,1}. Given the set S_n, adjoin all simplicity predecessors of its elements, all sums, differences and products of pairs of its elements, and all inverses of its nonzero elements. Each predecessor collection is a set. Replacement and Union therefore show that S_{n+1} is a set. The union K over n<omega is a set, is closed under field operations, and is initial: an element appearing at some stage has all its predecessors at the next stage. QED.

The analogous construction with additive operations produces a set-sized initial subgroup. This proposition concerns containment, not an initial representation of a specified structure.

**Failure of elementary preservation.** Take the canonical group Z[1/3]. Its smallest initial additive overgroup is Z[1/6]. Indeed it must contain D by Proposition 2, and the subgroup generated by D and Z[1/3] is Z[1/6], by Bezout's identity for powers of 2 and 3. Conversely Z[1/6] is initial because it contains D and lies in R. The hull is 2-divisible, whereas Z[1/3] is not. Hence even this simple initial-hull procedure does not preserve the first-order theory.

**A precise possible repair.** Suppose an ordinal-indexed elementary chain (M_alpha) is accompanied by initial embeddings f_alpha into No that agree on earlier structures. Their union is an embedding of the union structure, and its image is initial: every member of the union image already occurs in one initial stage. At a proper-class index this additionally requires the chain and compatible maps to be available as classes in NBG.

The hypothesis in the target supplies embeddings separately, not embeddings extending previously selected maps. A theorem giving that compatibility was not proved. Nor does compactness by itself guarantee the external well-foundedness of a proposed simplicity/rank relation. Finite satisfiability can coexist with an externally infinite descending chain: take the first-order linear-order axioms together with constants c_i and inequalities c_{i+1}<c_i; every finite subset has a finite well-ordered model, while a model of the whole set has that descending sequence. This is a warning about the method, not an interpretation of this finite-order example as a surreal group.

**Exact obstruction.** Reflection/conservativity cannot replace the hypothesis “all class models admit initial copies” with “all set models admit initial copies” without proving a transfer principle. The two hypotheses have different quantifiers. Initial hulls alter theories, and arbitrary separate embeddings do not automatically form a compatible system.

## What remains open

A full positive solution needs, for every consistent non-DOAG group theory or non-RCF field theory in the stated languages, a set model that has no initial copy. A negative solution needs one such theory together with a proof for all its set models. No result here supplies either universal quantifier. No independence, consistency-strength, or large-cardinal conclusion is claimed.

## References

1. A. Berarducci, P. Ehrlich, S. Kuhlmann, organizers, Mini-Workshop: Surreal Numbers, Surreal Analysis, Hahn Fields and Derivations, Oberwolfach Reports 13 (2016), 3313–3372; published 2017. Kaplan contribution, printed 3356–3358, especially Theorem 6 and Question 2. https://doi.org/10.4171/OWR/2016/60
2. P. Ehrlich and E. Kaplan, Number Systems with Simplicity Hierarchies II. Author PDF, Section 5, introductory field criterion, Section 8. https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf ; preprint record https://arxiv.org/abs/1512.04001
3. P. Ehrlich and E. Kaplan, Surreal ordered exponential fields, arXiv:2002.07739v3. https://arxiv.org/abs/2002.07739
4. D. R. Rangel and H. L. Mariano, An algebraic (set) theory of surreal numbers, I, arXiv:1911.12726. https://arxiv.org/abs/1911.12726

This note uses source theorems as stated dependencies and supplies new expository proofs of the controls and reductions. It does not re-prove the Hahn embedding criteria or the Omitting Types Theorem. All downloaded scholarly documents and extracted source text are excluded from the distributable folder.

