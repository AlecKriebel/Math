# Independent boundary proofs for PR 53

Written 2026-10-03 11:07 UTC. These elementary deductions check the original author's distinctions. They are not a reconstruction of Gabber's examples, a new general answer, or a claim of novelty. Rings here are commutative and unital.

## Compatible families suffice

Put A_r=A/m^r and B_r=B/n^r. An abstract ring isomorphism f_r:A_r→B_r carries the unique maximal ideal m/m^r onto n/n^r, hence carries each power onto the corresponding power. It therefore induces quotient isomorphisms at every lower order. Suppose the chosen f_r additionally satisfy π^B_{r+1,r} f_{r+1}=f_r π^A_{r+1,r}. For a sequence (a_r) in lim A_r, set F((a_r))=(f_r(a_r)). Compatibility makes this a sequence in lim B_r; componentwise operations make F a unital ring homomorphism. Multiplying the compatibility equation by f_r^{-1} and f_{r+1}^{-1} proves compatibility of the inverses, so F is an isomorphism. The canonical maps A→lim A_r and B→lim B_r are isomorphisms by completeness and separatedness of the maximal-ideal topology. Thus F gives A≅B. In the usual complete local Noetherian setting these are the intended canonical maps; this proof does not assume a coefficient field or equicharacteristic. It actually uses only the stated completeness/separatedness and the compatible isomorphisms.

An abstract isomorphism A→B in this local setting automatically carries m^r onto n^r, so it is continuous for these topologies. The problem is existence, not a distinction between a ring isomorphism and a continuous ring isomorphism.

## Why levelwise existence does not give compatibility

Let I_r=Iso_ring(A_r,B_r). Restriction defines maps I_{r+1}→I_r, because maximal ideals and their powers are intrinsic. The hypothesis says I_r is nonempty for every r. It supplies no surjectivity or eventual stabilization for these restriction maps. Nonempty sets alone do not imply a nonempty inverse limit: the sets S_r={j∈N:j≥r}, with inclusion transition maps S_{r+1}→S_r, are all nonempty but admit no compatible element, since compatibility would require one integer j≥r for all r. This is an inverse-system illustration, not an asserted ring counterexample or Gabber construction. Invoking strong approximation or an unstated extension property at this point would transfer the central difficulty to an unsupported assertion.

## Finite residue fields give a separate affirmative boundary

Assume additionally k=A/m≅B/n is a finite field. Since A is Noetherian, each m^i/m^{i+1} is a finite-dimensional k-vector space: m^i is finitely generated and its quotient is annihilated by m. It is a finite set. The filtration of A/m^r by these r layers then shows A/m^r is a finite set; the same holds for B/n^r. Hence every I_r is finite. Build a rooted tree whose depth-r vertices are isomorphisms in I_r, with edges given by restriction, and a single formal root at depth 0. Each level is finite and nonempty; a vertex can always be restricted down to the root. The finitely branching tree has arbitrarily large depth, so König's lemma gives an infinite branch (or recursively choose a child with descendants at arbitrarily large depth). The branch gives compatible isomorphisms. The preceding proof yields A≅B. This argument requires no lifting-surjectivity assumption. It fails for general infinite residue fields because levels of the tree need not be finite. This verifies a special case of the credited positive theorem, without proving its full algebraic-residue-field version.

## If one ring is Artinian, the other must match

Suppose m^N=0 for A and that the full hypothesis holds. Consider the isomorphism A≅B/n^{N+1}, obtained at r=N+1. The N-th power of the unique maximal ideal on the right is zero, since it corresponds to m^N. Thus n^N⊆n^{N+1}, giving equality. Noetherianity makes n^N a finitely generated B-module. Nakayama's lemma applied to n^N=n·n^N gives n^N=0. Consequently B/n^{N+1}=B, and the same isomorphism gives A≅B. The symmetric argument applies when B is Artinian. This is consistent with counterexamples requiring more than an Artinian ring on either side; it does not prove which dimensions or nilpotents Gabber's examples have.

## No bounded list of quotient matches suffices in general

For any field k and integer N≥1, take A=k[[x]], B=k[[x]]/(x^N). Both are complete local Noetherian rings. For every 1≤r≤N their r-th quotients are k[[x]]/(x^r), hence are isomorphic, including r=N. But A and B are not isomorphic: the maximal ideal of B is nilpotent and the maximal ideal of A is not (for N=1, B is a field and A is not). At r=N+1, the quotients have lengths N+1 and N, respectively. These are universal symbolic examples defeating any fixed-order or bounded computation as a substitute for the original all-orders hypothesis. They are not counterexamples to that hypothesis.

## Finite length is not finiteness of the underlying set

For k infinite, k[[x]]/(x^r) has finite composition length r, but contains the image of k, so its underlying set is infinite. Its k-linear automorphism family already includes x↦a x for every nonzero a∈k when r≥2. Thus neither finite length nor Noetherianity by itself supplies a finite tree of quotient isomorphisms.

Completion estimate: 55% of this independent audit. These proofs remove the main logical shortcuts but leave the historical general counterexamples imported from literature.
