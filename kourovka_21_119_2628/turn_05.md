# Turn 5/5: test an infinite-dimensional wreath-product construction

## Attempt

Replace the non-finitely-generated infinite product from turn 2 by a finitely generated permutational wreath product. The intended mechanism is to make a character kernel have finitely many orbits on tuples through size n, and infinitely many at size n+1, so its finiteness length is exactly n. The argument below shows why this natural mechanism cannot work in an F_∞ ambient wreath product. It does not exclude every possible wreath-product construction.

## 1. The proposed ambient group and the exact theorem being used

Let Q act on a nonempty set X and form W=Z≀_X Q=Z^{(X)}⋊Q. Theorem B of Bartholdi–de Cornulier–Kochloukova, *Homological finiteness properties of wreath products*, Q. J. Math. 66 (2015), 437–457, https://arxiv.org/abs/1406.5261 , states in this case that W is F_m exactly when Q is F_m, Q has finitely many orbits on X^i for 1≤i≤m, and every stabilizer of such an i-tuple is FP_{m−i}.

In particular W is F_∞ if Q is F_∞, its action has finitely many orbits on every finite Cartesian power, and all finite-tuple stabilizers are FP_∞. Conversely F_∞ of W forces those properties. An action with finitely many orbits on every finite Cartesian power is called oligomorphic. Such an action can package infinitely many lamp factors into an F_∞ group, and so genuinely evades the direct-product failure from turn 2.

Let H≤Q have finite index and ψ:H→Z be nonzero. The group W_H=Z^{(X)}⋊H has finite index in W. For the character χ:W_H→Z that vanishes on the lamps and equals ψ on H, its kernel is

K=Z^{(X)}⋊N=Z≀_X N,    N=ker ψ.

The same theorem applies to K. A plausible way to force K to be F_n but not FP_{n+1} would be to arrange that N acts with finitely many orbits on X^i for i≤n, but infinitely many on X^{n+1}. We now test this rather than assume it.

## 2. Exact orbit-count formula

Fix a finite tuple x∈X^i and let S=Stab_H(x). The H-orbit of x is H/S. Since N is normal, its orbits in H/S correspond to double cosets N\H/S, equivalently to cosets of ψ(S) in ψ(H). Thus

number of N-orbits inside Hx = [ψ(H):ψ(S)].

As ψ(H) is infinite cyclic, this number is finite if and only if ψ(S)≠0. It is countably infinite when ψ(S)=0. The proposed mechanism therefore requires a character that vanishes on one sufficiently large tuple stabilizer but not on smaller tuple stabilizers.

## 3. Oligomorphicity forbids that vanishing

**Lemma.** If H acts oligomorphically on X and ψ:H→Z is nonzero, then ψ(Stab_H(x))≠0 for every finite tuple x. Consequently ker ψ also acts oligomorphically on X.

**Proof.** Suppose S=Stab_H(x) lies in ker ψ, with x of length i. The diagonal H-orbits on (Hx)×(Hx) are parametrized by S\H/S. The map

S h S ↦ ψ(h)

is well defined because ψ(S)=0, and is onto the infinite group ψ(H). Therefore S\H/S is infinite. But (Hx)×(Hx) is an H-invariant subset of X^{2i}; oligomorphicity says it has only finitely many H-orbits. This is a contradiction. The orbit-count formula then shows that each of the finitely many H-orbits in X^i splits into only finitely many ker ψ-orbits, for every i. ∎

Finite-index passage does not help. If Q acts with finitely many orbits on X^i and H≤Q has finite index, each Q-orbit splits into at most [Q:H] H-orbits. Thus H is also oligomorphic, and the lemma applies to every virtual character.

There is a useful broader version: if H/N is finitely generated abelian, N is again oligomorphic. Indeed, if the image of some tuple stabilizer S had infinite index in H/N, the finitely generated abelian quotient (H/N)/image(S) would admit a nonzero map to Z. Composing with H would give a nonzero integral character vanishing on S, contradicting the lemma. Finite index of image(S) then gives the same finite orbit splitting.

## 4. What remains of the wreath construction

For the lamp-killing characters under consideration, the orbit part of the finiteness criterion is automatic. Any finite finiteness-length threshold must instead come from the F_m properties of N or the FP_{m−i} properties of its tuple stabilizers

Stab_N(x)=ker(ψ|_{Stab_H(x)}).

Thus a successful construction would need a controlled hierarchy of character-kernel finiteness properties in those stabilizers, while keeping Q and the ambient wreath product F_∞. No such hierarchy is constructed here. Simply substituting an oligomorphic action and asserting a first orbit-count failure is impossible by the lemma.

This does not analyze characters that are nonzero on the lamp subgroup, nor arbitrary finite-index subgroups of W which are not of the displayed W_H form. It also does not rule out the stabilizer-finiteness mechanism. Those are genuine remaining possibilities, not negative conclusions.

## Final outcome after five substantive attempts

No group meeting all requirements of KOU-21.119 has been constructed, and no universal impossibility proof has been obtained. The question remains unresolved in this investigation.

The proved reductions and exclusions are:

1. Any solution is F_∞; maps may be surjective and their finite-index domains nested and normal. The virtual fiber spectrum is a commensurability invariant, and virtual first Betti number at most one is impossible.
2. Products of M nonabelian finite-rank free groups have exactly the finite virtual fiber lengths 0,…,M−1; explicit infinite-cyclic-cover homology cycles certify the upper failures.
3. Finite virtual cohomological dimension is incompatible with an unbounded spectrum.
4. Thompson F has only finite virtual fiber lengths 0 and 1; its many other subgroups do not meet the finite-index character-kernel condition.
5. In an oligomorphic action, kernels of virtual integral characters stay oligomorphic. The attempted wreath-product orbit-splitting construction therefore fails, with stabilizer finiteness and lamp-nonzero characters left open.

These are research notes based on credited standard results and elementary deductions. They are not a solution, a novelty claim, or a peer-reviewed mathematical result.
