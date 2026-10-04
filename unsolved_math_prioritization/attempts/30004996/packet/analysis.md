# Exact target and five approaches

## 1. Scope and conventions

Let Gamma be a countably infinite discrete group, let k >= 2 and q >= 1 be finite integers, and let S be an SFT in q^Gamma. Use the source's right-coordinate shift convention

    (g . y)(d) = y(d g),       pi_f(x)(d) = f(d . x).

The question assumes a Borel coloring f on X = Free(k^Gamma) whose coding map takes values in S and has trivial point stabilizers. It asks for some Borel coloring h with the same domain, q and S such that the closure of pi_h(X) is free. It does not require h=f or a local modification of f.

An SFT has finitely many local constraints up to translation. The compact free subshift in the conclusion need not itself be of finite type. No amenability, finite generation, torsion-freeness, or absence of finite normal subgroups is assumed in the full question. If q=1, its antecedent is impossible. Finite groups lie outside the stated source scope; for a finite group and finite q, every image is already closed, so the analogous implication is immediate.

Terminology matters:

- Pointwise freeness is trivial stabilizer of every coded point.
- Faithfulness only says the intersection of the coded points' stabilizers is trivial.
- Merely having infinite orbits is weaker than pointwise freeness. For example, the Z^2 configuration y(m,n)=1 if m=0 and 0 otherwise has an infinite orbit but is fixed by every vertical translation.
- A point whose orbit closure is free is often called hyper-aperiodic. The source's coloring definition is stronger: the closure of the entire image must be free, uniformly across source orbits.

In common symbolic-dynamics terminology a weakly aperiodic subshift has no finite orbits, while a strongly aperiodic subshift has no nontrivial point stabilizers. Terminology varies, so all claims here use explicit stabilizers. The problem assumes neither of these properties for every point of S.

## Approach 1. Compactify the image by uniform finite witnesses

### Lemma 1: exact finite-witness criterion

For any coloring f:X->q, the closure of pi_f(X) is free if and only if for every g != 1 there is a finite D_g subset Gamma such that

    for every x in X, some d in D_g satisfies f(d . x) != f(d g . x).       (1)

Proof. For fixed g, define U_d={y:y(d)!=y(dg)}. Each U_d is clopen. If the compact image closure K is free, the U_d cover K, and a finite subcover supplies D_g. Conversely, (1) says the image lies in the clopen set union_{d in D_g} U_d. Its closure does too, so no point of K is fixed by g. Apply this for each nonidentity g. This argument does not require S to be an SFT. QED.

Aperiodicity only gives the weaker quantifier order

    for every g != 1, for every x, there exists d.

The missing uniform finite D_g is the exact compactness gap. For Z and S=2^Z, take f(x)=x(0) on Free(2^Z), so pi_f is inclusion. This f is continuous and aperiodic but not hyper-aperiodic: shifts of the single-1 configuration converge to the all-zero fixed configuration. For every finite D and fixed g=1 in additive notation, place the single 1 outside D union (D+1), and all tested pairs agree. This disproves the strategy of retaining f and simply closing its image. It does not disprove the requested existence of another h; the full shift is a known affirmative case.

There is also a strict orbitwise-versus-global distinction. Let T be a nonempty compact free binary Z-subshift, whose existence follows from the known free-subshift theorem. For n>=1 and t in T, form D_n(t) by putting t(j) at coordinate nj and zeros elsewhere. Let T_n be the union of its n shift phases. This is compact and shift-invariant. If a point in T_n had a nonzero period p, one of its 1s shows p must be divisible by n, and its sampled sequence in T would then have period p/n. Thus T_n is free. Every point in A=union_n T_n has free orbit closure, but the closure of A contains all zeros: center increasingly long gaps between the n-spaced allowed positions. Therefore orbitwise freeness of closures cannot replace (1) uniformly across the image.

Outcome: rigorous equivalence and failed-route examples; no construction of h.

## Approach 2. Continuity transfer and Baire essential images

Bernshteyn's published continuous-input theorem applies if the supplied coding map is continuous and faithful. Under the current aperiodicity assumption, faithfulness is automatic, but continuity is not. Refining the source topology to make f continuous does not produce a continuous map on the specified free shift with its original topology, so it does not establish that theorem's input.

Likewise, restricting a Borel function to a comeager continuity set does not automatically supply a compact invariant set there. Already for Z, let C be the binary configurations other than all zeros that contain arbitrarily long zero blocks. This is an invariant dense G_delta subset of the full shift. Every point of C is free: a nonzero periodic configuration has a bounded zero-run length. Every orbit closure of a point in C contains all zeros, so C contains no nonempty compact invariant subset. This example obstructs that general inference, not all possible choices of continuity set.

A more careful Baire argument does give a restricted partial result.

### Lemma 2: centralizer-minimal source

Let Gamma act continuously on a nonempty compact metrizable space M. Suppose that for every g != 1 the action of the centralizer C_Gamma(g) on M is minimal. If psi:M->S is a Borel equivariant map whose image is free, then S contains a nonempty compact free subshift K. Here S can be any finite-alphabet subshift.

Proof. Let B be the countable family of all clopen subsets of S. Define

    K = S minus union{U in B : psi^{-1}(U) is meager in M}.

It is closed. The preimage of the removed union is meager, so K is nonempty by the Baire category theorem. Equivariance and preservation of meagerness by homeomorphisms imply K is Gamma-invariant.

Fix g != 1. Freeness of psi(x) says the countable Borel sets

    A_d = {x : psi(x)(d) != psi(x)(dg)},       d in Gamma,

cover M. At least one A_d is nonmeager. By the Baire property there is a nonempty open V on which A_d is comeager. Minimality of the centralizer action and compactness supply finitely many h_1,...,h_r in C_Gamma(g) such that union_i h_i^{-1} V=M. Consequently union_i h_i^{-1} A_d is comeager in M. On h_i^{-1} A_d, equivariance gives

    psi(x)(d h_i) != psi(x)(d g h_i) = psi(x)(d h_i g).

Thus the preimage of the clopen set

    U_g = {y in S : some i has y(d h_i) != y(d h_i g)}

is comeager. The complement of U_g is one of the removed meager-preimage clopen sets. Hence K subset U_g. Every y in K is moved by g, for every g != 1. QED.

### Corollary: restricted nonempty-free-subshift consequence

Assume every nonidentity element of the countably infinite Gamma has infinite centralizer. Then the antecedent of the target implies that S contains a nonempty compact free subshift.

Indeed, Bernshteyn--Frisch, arXiv:2509.03139v2, Theorem 1.3 and Corollary 1.11, provide a nonempty free compact metrizable Gamma-flow M simultaneously minimal under the countably many infinite sets C_Gamma(g). Seward--Tucker-Drob supplies a Borel equivariant map M->Free(2^Gamma). Include the two symbols in k and compose with pi_f. This is the psi required by Lemma 2.

The group condition includes torsion-free groups (the infinite cyclic group generated by g lies in its centralizer) and infinite abelian groups. It does not cover an arbitrary group with a finite centralizer. More importantly, the conclusion is only existence of K. The proof yields psi(x) in K on a comeager invariant subset of M, not a Borel map from all of Free(k^Gamma) into K. The latter is exactly the remaining universality issue. This deduction is not asserted to be novel.

Outcome: a restricted compact-subshift result; no full Borel uniformization.

## Approach 3. Add an independent free coordinate

There is a valid alphabet-doubling variant. Let b:X->2 be a known Borel hyper-aperiodic coloring, and put h(x)=(f(x),b(x)). Its target alphabet has size 2q. The image closure L lies in

    S x T,       T=closure(pi_b(X)),

because both coordinate projections are continuous and S is closed. A group element fixing a point of L fixes its T coordinate and is therefore the identity. The first-coordinate constraints still define the SFT S x 2^Gamma over the larger alphabet. Thus every Borel S-coloring, even without the assumed aperiodicity, can be made hyper-aperiodic after adjoining an unrestricted binary coordinate.

This is not the original result. Projection back to q symbols can restore periods. With f the inclusion coloring from Approach 1, the paired coloring has free compact image closure, but its first-coordinate image closure is the entire binary full shift. There is no general same-alphabet, S-preserving encoding or retraction established here. An injective alphabet map cannot compress all 2q pairs into q letters.

Outcome: a rigorously proved modified statement; fixed-alphabet gap remains.

## Approach 4. Enforce separating constraints by finite type

Enumerate Gamma minus {1} as g_1,g_2,... and tentatively choose finite witness sets D_i. For n>=1 put

    S_n = {y in S : for every i<=n and every h in Gamma,
                     some d in D_i has y(dh) != y(d g_i h)}.

Each S_n is an SFT: for each i there is just one finite-window constraint, translated by h. They are nested. If all S_n are nonempty, compactness gives a nonempty K=intersection_n S_n, and the constraint at h=1 makes K free. This is a legitimate finite-type approximation scheme.

Two pieces are absent. First, the assumed pointwise aperiodic Borel map does not yield consistent uniform D_i preserving nonemptiness. Second, even successfully obtaining K would not alone provide the required Borel map into K. Choosing separate Borel maps into every S_n also does not create a coherent pointwise limit: the choices need not agree and an equivariant Borel limiting selection has not been supplied.

### Lemma 3: compact freeness is not Borel universality

Let T be any nonempty compact free binary Z-subshift, and let P be the two-point orbit consisting of the alternating binary sequences. Then K=T x P is a compact free subshift over four symbols. Nevertheless there is no Borel Z-equivariant map Free(2^Z)->K.

Proof. Composing such a map with the P coordinate would give a Borel map a:Free(2^Z)->{0,1} with a(sigma x)=1-a(x). Equip the binary full shift with fair product measure mu; its free part is conull. A={x:a(x)=0} would be invariant under sigma^2 and have measure 1/2. But sigma^2 is ergodic (in fact mixing), contradicting ergodicity. Mixing follows first for finite-coordinate cylinder sets by independence after sufficiently large even translations and then for measurable sets by approximation. QED.

K is not claimed to be an SFT, to receive the original f, or to be a counterexample to the target. It proves that compact-subshift existence is a strictly weaker intermediate goal, including in the restricted corollary of Approach 2.

Outcome: finite-type reduction and exact second obstruction; no Borel factor construction.

## Approach 5. Search for a counterexample with escaping interfaces

Consider the one-dimensional SFT

    S_mon = {y in 2^Z : the adjacent word 10 never appears}.

Its configurations are all zeros, all ones, and the single interfaces b_t given by b_t(n)=0 for n<t and 1 for n>=t. The interfaces form one free orbit. Any nonempty closed invariant set containing an interface also contains fixed points, by translating its interface off to infinity. Thus S_mon has free points but has no nonempty compact free subshift.

This looks like a possible negative example, but it fails the problem's antecedent. If pi:Free(k^Z)->{b_t:t in Z} were Borel equivariant, let A=pi^{-1}({b_0}). Under the uniform Bernoulli probability measure on k^Z, the free part is conull and the translates of A are a countable partition into sets of equal measure. Positive measure would make their total infinite; zero measure would make the total zero. Both contradict total measure one. Hence S_mon admits no Borel aperiodic S_mon-coloring of the required source.

More generally, an equivariant Borel map pushes forward every invariant probability measure, including Bernoulli measure. Any proposed target whose free part supports no invariant probability measure is therefore eliminated immediately. A countable union of infinite orbits has no invariant probability measure: all point masses on each infinite orbit are equal and hence zero. This blocks the entire countable-free-part counterexample family, not just this SFT.

Outcome: an explicit candidate SFT is rigorously rejected; it is not a counterexample.

## Exact remaining gap

No approach gives a Borel h into the original q-symbol SFT together with one finite D_g per nonidentity g satisfying (1) on every source point. No SFT meeting the antecedent and forbidding every such h was constructed. The restricted compact-subshift deduction, larger-alphabet construction, and invalid-route counterexamples do not settle that question. Classification remains `unsolved`.
