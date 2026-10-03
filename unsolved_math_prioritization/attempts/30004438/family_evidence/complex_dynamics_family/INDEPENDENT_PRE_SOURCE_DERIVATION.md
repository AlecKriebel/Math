# Independent complex-dynamical derivation, before candidate access

UTC: 2026-10-03 03:20 (first checkpoint). Estimated audit completion: 20%.

This note was written before opening the candidate scientific files or earlier reviews. Operator: Codex subagent `/root/pr46_complex_dynamics_adversary`. No external individuals contacted.

## Exact claim

For each integer d >= 2, Rat_d(R), the open resultant-nonzero locus in RP^(2d+1), contains a nonempty open subset all of whose complex periodic points of every positive period lie in RP^1. A periodic point is any z with f^n(z)=z for some n>=1, including infinity. Multiplicities and exact periods do not change this set-theoretic claim.

## Independently obtained mechanism

Use rational upper-half-plane self-maps with a strictly attracting real fixed point. They constitute an open, full-dimensional family when represented with d finite distinct real poles and residues of one strict sign:

f(z) = B + sum_{j=1}^d c_j/(p_j-z),

where p_1 < ... < p_d and c_j>0, B real. The denominator has degree d and numerator degree at most d; nonzero residues prevent cancellation. Thus f has degree d. For Im z>0,

Im f(z) = (Im z) sum_j c_j/|p_j-z|^2 > 0.

The lower half-plane is likewise invariant by conjugation. The d poles, d residues, and B give 2d+1 parameters.

Choose p_j=j, R=d+1, c_j=1/(10d), and B=R+sum_j c_j/(R-p_j). Then f(R)=R and

0 < f'(R) = sum_j c_j/(R-p_j)^2 <= 1/10 < 1.

The real fixed point is simple as a solution of f(x)-x=0, so it and its strict attraction persist under small real coefficient perturbations. All d real simple poles and strictly positive c_j likewise persist. This gives an actual open neighborhood in the denominator-monic rational coefficient chart, rather than a fixed-infinity codimension-one slice. The chart has numerator coefficients a_0,...,a_d and denominator coefficients b_0,...,b_(d-1), dimension 2d+1, and applies whenever the denominator degree is d.

## All-period proof without structural stability

Let r be the persisted attracting real fixed point, with 0<f'(r)<1. The real orientation-preserving Mobius map M(z)=-1/(z-r) maps the upper half-plane to itself. For g=M f M^(-1), infinity is a fixed point and the leading linear coefficient is a=1/f'(r)>1 (expand at r).

Every real rational map of the upper half-plane into itself has only real finite poles, all simple, with negative ordinary residues, and polynomial part az+b where a>=0 and b is real. For this specific family this elementary representation can also be checked by solving f(x)=r: f is strictly increasing between consecutive poles, the equation has d distinct real solutions, one is r, and conjugation produces d-1 finite real simple poles. Each ordinary residue is negative because g'(x)>0 on the real line away from poles; its local derivative is minus the residue divided by (x-p)^2. Consequently

g(z)=az+b+sum_{k=1}^{d-1} C_k/(P_k-z),   C_k>0,

and Im g(z)>=a Im z>Im z for Im z>0. Hence Im g^n(z)>=a^n Im z; no point in the upper half-plane is periodic, for any n>=1. By conjugation the same holds in the lower half-plane. All periodic points lie on RP^1. Poles and infinity are real and cause no missing nonreal case.

## Elementary proof of the representation used above

For a real rational H->H map, any nonreal finite pole is forbidden because the upper half-plane would contain a pole (or its conjugate). At a real pole, a term R/(z-p)^m must have positive imaginary part on every sufficiently small upper semicircle; for m>=2 its imaginary sign changes with the angle. Thus m=1 and R<0. Subtract these pole terms. The remaining real polynomial likewise has positive leading imaginary part in all sufficiently large directions only if its degree is <=1; its linear coefficient is nonnegative. Alternatively in our conjugated case, degree counting plus the d-1 known simple finite poles already makes the polynomial part linear. The infinity derivative calculation gives a>1 directly.

## Checks and failure modes to attack when reading candidate

1. Does its purported open family retain all parameters, rather than fix infinity?
2. Does it use one strict uniform inequality ruling out every period, rather than intersect countably many period-dependent neighborhoods?
3. Does it account for nonreal periodic points in attracting basins, poles, infinity, and degree cancellation?
4. Does an orientation-reversing half-plane map introduce period-two cycles? If the square has the required boundary attraction, the same proof can apply to its square, but attraction must be demonstrated.
5. Does it invoke hyperbolic structural stability with a verified real Julia set and verified attracting cycles? Merely real repelling cycles is insufficient.
6. Strict inequalities cannot be extended to the neutral boundary without additional argument.

Strongest verified result at this checkpoint: the advertised existence statement has an independent elementary proof. Remaining audit gap: candidate files, proof details, provenance, and whether the result is novel.
