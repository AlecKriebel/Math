# Turn 2: finite-residual descent and a fixed-point reservoir

**2594 / KOU-21.85. Substantive author turn 2/5. Original implication remains unresolved.**

This turn separates two mechanisms: an unconditional reduction of the possible counterexample class, and an exact reservoir conversion whose missing relative-error estimate is identified. The first does not depend on any unproved stability permanence theorem.

## 1. Approximate actions descend when their kernel vanishes asymptotically

Let π:G→Q be a surjective homomorphism of countable groups with kernel N, and let s:Q→G be a set-theoretic section with s(1)=1. No computability or homomorphism property of s is required. Let f_j:G→Sym(X_j) be asymptotically multiplicative, pointwise for every fixed pair. Suppose

    d_{X_j}(f_j(r),1) → 0   for every fixed r∈N.             (1)

Define a_j(q)=f_j(s(q)). These maps form an asymptotic homomorphism of Q. For fixed q,u∈Q, write

    r(q,u)=s(q)s(u)s(qu)⁻¹ ∈N.

With Δ_j(g,h)=d(f_j(g)f_j(h),f_j(gh)), bi-invariance and the triangle inequality give

    d(a_j(q)a_j(u),a_j(qu))
      ≤ Δ_j(s(q),s(u))
          + Δ_j(r(q,u),s(qu)) + d(f_j(r(q,u)),1) → 0.       (2)

Indeed, s(q)s(u)=r(q,u)s(qu), so the two intermediate permutations are f_j(s(q)s(u)) and f_j(r(q,u))f_j(s(qu)). Every group element appearing here is fixed as j varies.

For a fixed g∈G, put r_g=g s(πg)⁻¹∈N. The same argument yields

    d(f_j(g),a_j(πg))
      ≤ Δ_j(r_g,s(πg)) + d(f_j(r_g),1) → 0.               (3)

Thus an exact same-size repair of a_j, pulled back along π, repairs f_j. The analogous assertion for flexible repairs also follows: use the same enlarged sets, and combine the pointwise comparison (3) with the enlarged-action discrepancy on X_j. The added-point term is unchanged.

## 2. The maximal residually finite quotient

Define the finite residual

    R=⋂{ker θ : θ is a homomorphism from G to a finite group},

and put Q=G/R. This is a normal subgroup. It also equals the intersection of all finite-index subgroups: the kernel of the action on G/H is a finite-index normal subgroup contained in any finite-index H. By construction every finite action of G factors uniquely through Q.

The group Q is residually finite. If gR≠R, some finite homomorphism θ has θ(g)≠1; since R⊂ker θ, that homomorphism factors through Q and separates gR. If G is finitely generated, so is Q.

### Proposition 1: transfer to Q

If G is permutation-stable, respectively flexibly permutation-stable, then Q has the same property.

**Proof.** Given a challenge a_j:Q→Sym(X_j), pull it back to f_j=a_j∘π. Apply the assumed stability of G. Each genuine repairing action of G on a finite set kills R and therefore factors through a genuine action of Q on that same finite set. The discrepancy for a fixed q is exactly the discrepancy evaluated at any fixed lift s(q), and all size conditions are unchanged. ∎

Unlike a general quotient-permanence claim, this proof uses the defining fact that **every** finite action kills R. It does not require R to be finitely generated as a group or as a normal subgroup.

### Proposition 2: kernel annihilation

If G is flexibly permutation-stable, then every source challenge f_j of G satisfies (1) with N=R.

**Proof.** Choose flexible exact repairs ρ_j:G→Sym(Y_j), X_j⊂Y_j. For r∈R, ρ_j(r) is the identity on all of Y_j. The flexible closeness condition on X_j therefore says exactly d(f_j(r),1)→0. The added-point penalty is irrelevant for this assertion. ∎

### Theorem 3: exact reduction within the flexible class

For a flexibly permutation-stable finitely generated G,

    G is permutation-stable  ⇔  G/R is permutation-stable. (4)

Moreover G/R is itself flexibly permutation-stable and residually finite.

**Proof.** The forward implication and the final flexible assertion are Proposition 1. Conversely, Proposition 2 ensures that any challenge f_j of G satisfies kernel annihilation; Section 1 descends it to a challenge a_j of Q. If Q is strictly stable, repair a_j on X_j and pull the action back to G. Equation (3) proves pointwise closeness to f_j. Residual finiteness was proved above. ∎

Consequences:

- If a counterexample to KOU-21.85 exists, one exists among finitely generated residually finite groups. This is an existential reduction; it does not construct one.
- If G is flexibly stable and its maximal residually finite quotient G/R is amenable, then G is strictly stable. Here Q is flexibly stable by Proposition 1, and the **credited** amenable equivalence is Ioana's Lemma 3.2(1); then apply (4). G itself need not be assumed amenable.
- Hence a residual-finite counterexample would have to be nonamenable. Finite or amenable maximal residual quotients cannot account for the gap under the flexible hypothesis.

The preceding conclusions do not say that ordinary stability of Q alone implies ordinary stability of an arbitrary G. Kernel annihilation is an essential intermediate hypothesis, here supplied by flexible stability of G. Nor do they say that all residually finite or all nonamenable groups are flexibly stable.

## 3. Compression is nonexpansive before normalization

For a finite set V and nonempty W⊂V, use the first-return compression c_W from Turn 1. For any permutations p,q of V,

    |{x∈W : c_W(p)(x)≠c_W(q)(x)}|
       ≤ |{v∈V : p(v)≠q(v)}|.                             (5)

**Proof.** Partition the p-cycles meeting W into the forward path segments starting at x∈W and ending at their next W-point. If p and q agree at each departure vertex of the p-segment starting at x, following q gives the same segment and the same first return, so the compressed maps agree at x. Each x where they disagree must therefore have a departure vertex v on its p-segment with p(v)≠q(v). The segments' departure-vertex sets are disjoint for distinct x, so choosing one such v gives an injection into the global disagreement set. Cycles lying entirely outside W do not contribute. ∎

The bound is in unnormalized cardinalities. Its normalized form is d_W(c_W(p),c_W(q))≤(|V|/|W|)d_V(p,q), not a normalized 1-Lipschitz claim across different dimensions.

## 4. Creating a small fixed-point reservoir

Let f:G→Sym(X), |X|=n, be any set map, not necessarily an action. Choose A⊂X with a=|A|<n and define

    T_A f(g) = c_{X\A}(f(g)) on X\A,
               identity on A.

For every g,

    d_X(T_A f(g),f(g)) ≤ 2a/n.                             (6)

There are at most a disagreements inside A and at most a outside points mapped by f(g) into A. Elsewhere compression makes no change.

Furthermore, for every g,h,

    Δ_{T_A f}(g,h) ≤ Δ_f(g,h) + 2a/n.                     (7)

On X\A, insert the intermediate permutation c_{X\A}(f(g)f(h)). Turn 1's compression-product inequality contributes at most 2a disagreements, and (5) contributes at most nΔ_f(g,h). On A both products are identities. Division by n proves (7).

Therefore if f_j is a source challenge and a_j/n_j→0, the reservoir-modified maps T_{A_j}f_j are still a source challenge, and remain pointwise close to f_j.

## 5. An exact reservoir absorption criterion

Fix a nonempty finite symmetric generating set S for G. Suppose a map ψ:G→Sym(X) fixes every point of A for every s∈S. Let ρ:G→Sym(Y) be an exact action with Y⊃X, |Y|=n+k, and define generator disagreement counts

    e_s = |{x∈X : ρ(s)x ≠ ψ(s)x}|,    E=Σ_{s∈S} e_s.

If

    k + E ≤ |A|,                                           (8)

then ρ can be converted to an action τ on exactly X satisfying

    |{x∈X : τ(s)x ≠ ψ(s)x}| ≤ e_s+k  for every s∈S.        (9)

**Proof.** At least |A|−E points of A are fixed by every ρ(s). Because S generates G, these are global fixed points of the whole action. Select a set Z of k such points. Its complement Y\Z is invariant and has exactly n points.

Choose a bijection θ:X→Y\Z that is the identity on X\Z and maps Z bijectively onto Y\X. Put τ(g)=θ⁻¹ρ(g)θ. This is a genuine action on X. For x∈X\Z with ρ(s)x=ψ(s)x, the common image lies in X\Z: ψ(s) fixes each point of Z and is a permutation, so a point outside Z cannot enter Z. Thus τ(s)x=ψ(s)x. All other disagreements outside Z are counted by e_s; at most k occur on Z. This proves (9). ∎

Apply this with ψ=T_Af. Combining (6) and (9) gives

    d_X(τ(s),f(s)) ≤ (e_s+k+2a)/n.                         (10)

In a sequence, if a/n→0 and the flexible repairs of the reservoir-modified challenges satisfy (8), strict repairs follow from (10) and the fixed-word telescoping argument of Turn 1.

## 6. Where this attempted proof of the full implication stops

Flexible stability of G applied to T_Af supplies

    k/n → 0,   E/n → 0.

The reservoir argument needs the stronger **relative** control k+E≤a, while also a/n→0. The former limits alone do not imply that inequality. For example, the scalar scales a/n=η² and (k+E)/n=η both vanish as η→0, but violate (8). This is only a diagnostic of an unsupported inference, not an actual group counterexample.

The choice of a affects the challenge itself: (7) introduces an error of order a/n. One cannot first obtain a flexible repair, choose a to dominate its cost, and then reuse that same repair after changing the input map. Nor is it justified to assume a flexible correction modulus is smaller than a prescribed multiple of its argument. Even if an available correction bound were √t, substituting t=Δ+2a/n would give no absorption inequality for small positive a/n.

Thus the reservoir construction is a valid exact conversion **conditional on (8)**, but it does not prove that such repairs can always be selected. Merely adding more fixed points outside the original domain is also insufficient: returning to the original cardinality requires deleting the whole added reservoir plus the repair's further extra points, whereas closeness guarantees only slightly fewer than the reservoir's original number of fixed points.

## 7. Prior-work boundaries and controls

The finite residual is a standard tool in permutation approximation. Becker–Lubotzky–Mosheiff, *Testability in group theory*, Section 1.2, uses it for BS-rigidity (Proposition 1.23), and Proposition 1.24 states stability transfer through a normal subgroup assumed finitely generated as a group. Those are distinct statements; this turn proves directly the restricted flexible-class implication (4), relying on annihilation of R, and does not infer arbitrary quotient permanence. No historical novelty is certified.

The finite checker tests (2)–(3) in small quotient models, the full unnormalized contraction (5) through five-point permutation pairs, the exact reservoir inequalities, and their relabeling construction. The finite quotient models are algebra controls, not examples with a nontrivial finite residual: a finite group's own finite residual is trivial. Source-wide infinite sequence and quantifier assertions are justified by the written proofs, not extrapolation from those tests.

**Turn outcome:** the possible gap can be restricted to finitely generated residually finite nonamenable groups; the amenable-quotient positive consequence is a credited corollary. The reservoir route stops at an explicit relative-cost selection problem. **Original target: unresolved, 2/5 consumed.** A subsequent turn must address the residual-finite nonamenable case or establish a genuinely stronger selection mechanism.
