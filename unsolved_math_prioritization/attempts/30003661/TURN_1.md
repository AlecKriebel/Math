# Turn 1: a shared-output obstruction to flattening the twisted cube

**Partial result only.** The original strong Weihrauch equivalence remains unresolved. This first route tests a natural two-dimensional flattening of the known three-dimensional construction. The geometric obstruction below excludes that class of encodings, not all planar path-connected encodings, and no historical novelty is claimed.

## 1. Names matter: a necessary condition for any fixed preprocessing scheme

Consider closed choice on [0,1] as the source problem. Let a proposed preprocessor send each input name p of a nonempty closed set A to a negative name of a nonempty closed path-connected set B_p in [0,1]^2. Suppose a postprocessor H is to receive only an oracle-output Cauchy name, as required in a strong reduction.

**Shared-output lemma.** If p and q name disjoint source sets A and D, then B_p and B_q must be disjoint.

For if z belongs to both target sets, choose one Cauchy name r of z. An oracle realizer of planar path-connected choice can return this same r on both target input names, since r is a valid answer for each. Define its other outputs arbitrarily among valid answers; the reduction must work for every realizer, which need not be computable. The postprocessor receives the identical name r in both runs. Its output would therefore have to name a point in A intersect D, a contradiction.

This argument does not assume that H is an extensional single-valued function on geometric points. It works at the name level and specifically uses the universal quantifier over oracle realizers. It also does not assume that the preprocessor is extensional in the source set: it applies to each chosen pair of input names. The lemma need not hold for ordinary Weihrauch reduction, whose postprocessor can retain the source input.

## 2. The planarization family

For a nonempty closed A subset [0,1], let

    T(A) = (A x [0,1] x {0})
           union (A x A x [0,1])
           union ([0,1] x A x {1}).

This is the credited twisted-cube construction from Proposition 6.1 of the source paper. Its third coordinate distinguishes which original coordinate is a valid choice. We examine a computable continuous flattening

    F(x,y,z) = (phi(x,y,z), h(z)) in [0,1]^2,

where h:[0,1]->[0,1] is any continuous function and phi is continuous with

    phi(x,y,0)=x,
    phi(x,y,1)=y,
    phi(a,a,z)=a for all a,z.                   (1)

For example phi=(1-z)x+zy and h(z)=z satisfy all conditions. Let B(A)=F(T(A)). The geometric images are nonempty, compact and path connected. The computational input condition is also satisfied when F is computable: T is computable in negative closed-set representation, and a computable continuous image of a negatively given closed subset of a computably compact cube is uniformly negatively given.

For completeness, the last image assertion follows by semideciding finite covers. To enumerate an output basic ball V disjoint from the image, require its compact closure to be disjoint. This is equivalent to T(A) being contained in the computable open preimage of the complement of that closure. Negative information about T(A), together with a finite-cover search for the ambient compact cube, semidecides that containment. Enumerating all such V exhausts the complement of the compact image. No positive point in A has been computed in this procedure.

## 3. Every flattening in this family fails strong decoding

**Proposition.** No map F satisfying (1) can supply a strong reduction of closed choice on [0,1] to planar path-connected choice through the preprocessing A->B(A).

Choose rational r<a<s in [0,1], and use the disjoint source inputs A={r,s} and D={a}. The full segment (r,s,z), 0<=z<=1, belongs to T(A). The continuous function z->phi(r,s,z) has endpoint values r and s. The intermediate value theorem therefore gives z_0 with phi(r,s,z_0)=a. Hence

    (a,h(z_0)) = F(r,s,z_0) belongs to B(A).

On the other hand (a,a,z_0) belongs to T(D), and the diagonal condition gives

    F(a,a,z_0)=(a,h(z_0)) belongs to B(D).

The target sets intersect although the source sets are disjoint. The shared-output lemma is a contradiction. This proves the obstruction for every continuous interpolation phi in the class, including nonlinear and nonmonotone ones. Monotonicity of h, injectivity of h, and a computable value of z_0 are unnecessary.

In the affine example phi=(1-z)x+zy, one can choose explicitly

    z_0=(a-r)/(s-r).

Thus even the literal exact real-valued height coordinate h(z)=z does not repair the information loss caused by combining the two choice-bearing coordinates into one.

## 4. A more geometric barrier formulation

The same obstruction applies without a fixed flattening formula. Suppose a family of proposed planar outputs B(A) satisfies:

1. B({a}) contains the full vertical segment {a} x [0,1] for every a in [0,1]
2. For r<s, the connected set B({r,s}) has a point with first coordinate r and a point with first coordinate s

The first-coordinate image of B({r,s}) is connected, so it contains every a between r and s. The corresponding target point lies in the full vertical segment B({a}). Again the two source solution sets are disjoint, contradicting the shared-output lemma.

This version permits input-dependent constructions and does not need path connectedness beyond ordinary connectedness. Its extra vertical-fiber hypothesis is essential and is not imposed by the source problem. An arbitrary successful reduction could avoid that hypothesis, use a different geometric organization, and exploit admissible output-name behavior. No general nonreducibility theorem follows.

## 5. Boundary and uniformity checks

- The source sets used are finite, nonempty, closed and computable; the contradiction is about the strong decoder rather than difficulty constructing their names
- Strict r<a<s gives disjoint source sets and s-r>0; the endpoint cases a=r or a=s would not be counterexamples
- The overlap argument allows any Cauchy name of the common target point; no canonical or preferred naming convention is assumed
- The existence of a continuous path in a target is a promise only. No effective path is supplied to the oracle or decoder
- B(A) is a valid planar choice instance even when the proposed decoding fails. The defect is not a hidden failure of compactness or negative-name computability
- The known three-dimensional construction avoids the obstruction because it retains both original coordinates, rather than this scalar interpolation of them

`verify_turn1.py` checks exact affine and piecewise-linear collision certificates on modest rational families. Those checks are illustrations of the uniform intermediate-value proof, not a finite search for a solution or a proof of general separation.

## 6. Remaining gap

This attempted reduction is blocked: continuous height-preserving interpolation with diagonal preservation necessarily merges valid answers to disjoint source inputs. A positive result must use an essentially different planar organization, or a negative result must obstruct all permissible computable preprocessors. Neither is obtained here.

Estimated completion toward the full assigned strong-equivalence question: 5%, low confidence. One of five substantive turns is complete; four remain. Independent review is pending, and the ordinary/strong source distinction is unchanged.
