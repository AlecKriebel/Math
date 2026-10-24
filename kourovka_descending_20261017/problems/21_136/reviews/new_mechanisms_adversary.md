# Fresh adversarial audit: metabelian locality and ambient power coding

Checkpoint: **2026-10-24T17:30:46Z**. Independent AI reviewer, not an author of either mechanism. Review-task completion estimate: **100%**. The construction route estimates unrestricted discovery at 12%; neither this estimate nor this review signifies a solution.

Reviewed:

* `../lie_adversary/strong_subclass/metabelian_locality.md`;
* `../lie_adversary/metabelian_adversarial_audit.md`;
* the new power-coding lemma and its stated consequences in `../approach_constructions.md`, Section 3.

The governing AGENTS instructions were read. No external individuals were contacted. No Git, queue, PR, tracker, or publication operation was performed.

## Verdict and strict limits

**PASS, with no substantive mathematical objection remaining, for both exact claims:**

1. A virtually metabelian pro-p group satisfying P0 has finite exponent and is locally finite. Here P0 means that every open subgroup contains some open coset of bounded exponent; it is not a condition on arbitrary closed subgroups.
2. A profinite group containing an abelian torsion subgroup of unbounded exponent has at least continuum many ambient conjugacy classes of infinite-order elements. The abelian subgroup need not be closed or normal.

The proofs below were reconstructed independently, rather than accepting the earlier review as evidence. Neither mechanism resolves unrestricted 21.136, and no first-priority, publication, formal-verification, or human-review claim follows.

## 1. Metabelian P0 theorem

### Inheritance and rationalization

P0 is inherited by open subgroups directly from its quantifier. It is inherited by continuous quotients because the preimage of an open subgroup is open, quotient maps of compact groups are open, and the image of a bounded-exponent coset has exponent dividing the original bound.

For an abelian pro-p group B, one P0 coset xU of exponent m=p^n makes U itself exponent dividing m: x^m=(xu)^m=1 and commutativity give u^m=1. B/U is a finite p-group, hence also of bounded exponent, so B has finite exponent. This does not claim B is finite; infinite elementary abelian products remain valid examples.

In the metabelian case fix A=the closed commutator subgroup of G and B=G/A. A is a closed abelian pro-p group, with its natural continuous Z_p-module structure. Set V=A tensor over Z_p with Q_p. The abelian quotient B has exponent q=p^e by the preceding argument. Conjugation acts linearly on V, all action operators commute, and every action operator has exponent dividing q: a qth power of any group element lies in A, which centralizes A.

At later stages an open subgroup H need not contain A. This causes no gap. For each open U in G, A intersection U has finite p-power index in A and contains p^r A for some r. Therefore it spans all of V after localization. The proof does not apply P0 directly to A unless A happens to be open.

### Norm identity and the exact exponent drop

Let xU be a selected coset in an open H, with exponent dividing m. For b in xU and a in A intersection U, both b and ba lie in xU. Expanding (ba)^m with A abelian and using b^m=(ba)^m=1 gives N_m(alpha_b)a=0, where N_m(T)=1+T+...+T^(m-1). Since A intersection U spans V, this norm vanishes on V. Reversing the conjugation convention only multiplies the norm by an invertible operator.

If the action of H has exponent dividing q, enlarge m to M=lcm(m,q). The coset identity remains valid at exponent M. Since alpha_b^q=1,

    N_M(alpha_b) = (M/q) N_q(alpha_b).

The scalar M/q is nonzero and therefore invertible in Q_p, even if divisible by p. Thus N_q(alpha_b)=0. No invalid reduction of an exponent identity in the original integral group is being performed; the division takes place only on V.

Fix u in U. The two operators alpha_x and alpha_u commute and have orders dividing q. They generate a **finite** abelian group, of order at most q^2. Over a field containing all qth roots of unity, its finitely many Fourier idempotents decompose V after scalar extension, whether or not V has finite dimension. No character decomposition of an infinite compact acting group is invoked.

On each nonzero simultaneous character space, let xi and eta be the eigenvalues of alpha_x and alpha_u. Norm vanishing for x u^i, for every integer i, says xi eta^i cannot equal 1: on a qth root of unity, N_q is zero away from 1 and equals the nonzero scalar q at 1. If eta had exact order q, its powers would be all qth roots, including xi^-1. Therefore eta has order at most q/p. The p-power hypothesis is used here: every proper divisor of q divides q/p. Thus alpha_u^(q/p)=1 on all character spaces and hence on V. Faithful extension of scalars returns the conclusion to Q_p.

This verifies the exact exponent-drop lemma with no finite-dimensionality assumption. The restriction to commuting actions is essential. The Q8 representation in the source is a valid control: in its faithful two-dimensional complex representation the coset i<j> has no eigenvalue 1, while <j> still has exponent 4.

### Iteration and uniformity

Apply P0 first in G, then in each selected open subgroup U. Openness in G persists through this finite iteration. The action stays commuting, while the uniform action exponent drops successively from p^e to 1. Keeping A and V fixed is legitimate because each new intersection with A still spans V. At exponent 1 a final bounded-torsion coset makes its norm equal to a nonzero scalar times the identity, so V=0. The case e=0 uses this final step immediately; V=0 from the start is harmless as well.

Localization V=0 means each individual a in A is killed by some p-power. It does not by itself mean one exponent kills A. The latter follows separately by compactness and commutativity: A is covered by the closed subgroups A[p^n]; Baire makes one open, and its finite quotient supplies a uniform exponent for A. Combining the bounds on A and B gives a finite exponent for G.

For local finiteness, any finitely generated abstract F in G has finite image in bounded-exponent abelian B. Schreier's theorem makes F intersection A finitely generated; it is torsion abelian and therefore finite. Thus F is finite. This proof does not confuse abstract finite generation with topological finite generation or invoke the general compact-torsion theorem.

Finally, an open metabelian subgroup inherits P0 and the conclusions. Its open normal core has bounded exponent. The finite quotient gives bounded exponent for G. Intersecting any finitely generated abstract subgroup with the metabelian subgroup gives a finitely generated finite-index subgroup, which is finite, proving local finiteness of the extension.

The theorem does not cover arbitrary pro-p groups, arbitrary prosoluble groups, or the noncommuting action needed for general derived length at least three.

### Comparison with the already checked soluble class-bound result

The parent's additional clarification also passes. A compact torsion soluble group of finite derived length has finite exponent: induct on that length, using the last nontrivial closed derived subgroup A, which is compact abelian torsion and therefore of finite exponent by Baire. The torsion quotient has shorter length and finite exponent by induction; multiplying the two bounds bounds the group's exponent. Such a group is locally finite as well. A finitely generated abstract soluble torsion subgroup F has finite abelianization, so its abstract derived subgroup has finite index and is finitely generated by Schreier. Induction on derived length then makes the derived subgroup, and hence F, finite. Finite extensions preserve finite exponent and local finiteness by the core and finite-index arguments already given.

Thus under the original small-class hypothesis, the previously checked finite-derived-length soluble torsion conclusion already strengthens to finite exponent and local finiteness. The new metabelian theorem is valuable because **P0 is a weaker hypothesis**; it must not be counted as settling an additional metabelian case of the original problem beyond that soluble result.

## 2. Power coding in an arbitrary profinite ambient group

Let T be an abelian torsion subgroup of G with no finite exponent and put A=closure(T). Continuity of the commutator map makes A abelian. T is not assumed closed, and no class-count property is inherited from G to A.

For every open normal N of G, T intersection N has no finite exponent. Indeed T/(T intersection N) embeds in the finite group G/N. If that finite quotient has exponent d and T intersection N had exponent m, every element of T would have order dividing dm, contradiction. This step remains valid even if N meets T densely or T has arbitrarily large cardinality.

Inductively take N_0=G and finite-order b_i in T. At stage i define

    E_i = lcm(i!, order(b_1), ..., order(b_(i-1))).

Since T intersection N_(i-1) has no finite exponent, choose b_i there with b_i^E_i nontrivial. Residual separation by finite continuous quotients gives an open normal N_i contained in N_(i-1) that excludes this power. The choice requires no finite generation, countable base, or normality of T.

For a subset S of the positive integers, let q_k be the finite product of those b_j with j<=k and j in S. The nonempty compact subsets q_k(A intersection N_k) of A are nested: the possible new factor b_(k+1) lies in A intersection N_k. Compactness supplies x_S in their intersection. This proves existence without asserting convergence of an infinite product or uniqueness of the intersection.

For each fixed i, the image of x_S in G/N_i is q_i N_i. Commutativity within A and the definition of E_i kill every earlier factor, giving the exact tests

    x_S^E_i in N_i        if i is not in S;
    x_S^E_i not in N_i    if i is in S.

Future stages never alter this fixed quotient coset. The second alternative is detected by the chosen nontrivial image of b_i^E_i. Thus the bit test is well defined for every possible choice of x_S in the compact intersection.

Because N_i is normal in the full ambient G, membership of x^E_i in N_i is invariant under **ambient** conjugacy. Two distinct subsets S therefore produce nonconjugate elements, even if G fuses many other classes inside A. This is the point that prevents the proof from accidentally reverting to conjugacy only in A.

For an infinite S and a proposed finite order L of x_S, choose i in S with i>=L. Then L divides i! and hence E_i, contradicting the selected-bit test. Therefore each infinite S gives an infinite-order element. There are continuum many infinite subsets of the positive integers, and this argument gives continuum distinct ambient classes without CH. It provides a lower bound only; G may have larger cardinality or more classes.

### Consequences checked

Under the strict class bound, every abelian torsion subgroup has some finite exponent depending on that subgroup. A product of finite cyclic groups of unbounded orders contains their abstract direct sum, to which the lemma applies. More generally, a product of finite groups of unbounded exponents has cyclic subgroups of unbounded orders in distinct factors: otherwise all element orders in all factors would be bounded, which would bound every exponent by one factorial. Those cyclic subgroups commute across factors and generate a suitable T. Hence the product is excluded even if ambient conjugators do not preserve its factors.

The same reasoning validates the stated arbitrary-overgroup obstruction for W_p and the infinite unitriangular group: disjoint finite-depth odometers, respectively disjoint finite Jordan blocks, give commuting finite-order elements of unbounded orders. This does not depend on an ambient tree or matrix action being preserved.

The lemma makes no uniform-exponent assertion about all torsion elements of G, which need not commute or even form a subgroup. It also makes no assertion that an arbitrary abelian subgroup is torsion; the torsion assumption on T is needed to kill all previous factors with a finite E_i.

## 3. Remaining mathematical and priority gaps

No argument supplies an unbounded-exponent abelian torsion subgroup in every possible non-torsion profinite group under the original hypotheses. No argument extends the commuting exponent-drop lemma to the required general nonabelian actions. Merely asserting either missing property would transfer the central problem to an unsupported claim.

These are exact partial mechanisms with self-contained proofs, not experimentally inferred results. The audit did not perform an extensive priority search for them, and elementary appearance or failed bounded searches cannot certify originality. Unrestricted 21.136 remains **unsolved by this work**; solved_verified or published labels are not justified.
