# Author turn 2: simple-factor orbit counting removes basicity

## 1. The positive class

Let G=S_1 times ... times S_m be a finite product of finitely generated nonabelian simple groups, with m>=1. Let H be Hopfian. More generally than the original regular action, let H act **faithfully and transitively** on a nonempty set X, and put

    W=G^(X) semidirect H,   B=G^(X).

**Theorem.** Every surjective self-homomorphism of W is basic and injective. In particular G wr H is Hopfian for every such G and every finitely generated Hopfian H, as asked in the original problem for this class of bases.

The conclusion applies to infinite as well as finite simple factors. The number m is finite. Both faithfulness and transitivity are retained in the extension to permutation actions. The theorem does not cover abelian bases or arbitrary centerless Hopfian bases.

The proof uses the normal-subgroup commutator mechanism credited in Bradford--Fournier-Facio Proposition5.1, and a finite count of conjugacy orbits of intrinsic simple factors. It does not assume that a surjection automatically preserves the base. No historical novelty claim is made.

## 2. Elementary facts about restricted sums of nonabelian simple groups

Let D be a restricted direct product (direct sum) of nonabelian simple groups S_i indexed by any set I. Every normal subgroup K of D is the restricted sum of a subfamily of the S_i.

Indeed, if some k in K has nonidentity i-coordinate a, choose u in S_i with [a,u] nontrivial; such u exists because a nonabelian simple group has trivial center. The commutator [k,u_i] is a nontrivial element of K intersect S_i. This intersection is normal in S_i, so it equals S_i. Thus every coordinate appearing in an element of K contributes its entire simple factor, proving the assertion. Consequently every quotient of D is the restricted sum of the surviving factors, and its minimal nontrivial normal subgroups are exactly those factors.

These observations also prove that a finite product of nonabelian simple groups is Hopfian: a proper quotient kills at least one intrinsic factor and has strictly fewer minimal nontrivial normal factors. It cannot be isomorphic to the original finite product. Thus both source factors in the regular-action corollary satisfy the Hopfian hypothesis.

For B=G^(X), write its simple factors as S_(i,x), with 1<=i<=m and x in X. Conjugation by a base element preserves each factor; conjugation by H moves x through its orbit and preserves i. Transitivity therefore gives **exactly m W-conjugacy orbits** on these intrinsic simple factors.

## 3. A non-basic normal subgroup contains the entire base

Each S_i is perfect, since its commutator subgroup is nontrivial and normal; hence G is perfect. Let N be a normal subgroup of W not contained in B. Choose (f,h) in N with h!=1. Faithfulness supplies x in X moved by h.

Use commutators [a,b]=aba^{-1}b^{-1}. For g,u in G, the commutator [(f,h),g_x] is supported on x and hx, with x-coordinate g^{-1}. A second commutator with u_x consequently gives

    [[(f,h),g_x],u_x] = [g^{-1},u]_x in N.                       (1)

These commutators generate G'_x=G_x. Conjugating by H and using transitivity gives every G_y<=N. Therefore

    N not contained in B  implies  B<=N.                       (2)

For the regular action this is precisely the perfect-base case of the known normal-subgroup mechanism. The same calculation proves (2) for the faithful transitive action; it would fail if the quotient element h acted trivially on X.

## 4. Basicity from a finite orbit budget

Let Phi:W->W be surjective and N=Phi(B). Then N is normal in W and is a quotient of the restricted sum B. By Section2 it is itself a restricted sum of some surviving nonabelian simple factors.

The kernel of Phi restricted to B is normal in W, so, for each i, either every S_(i,x) is killed or none is. Moreover the images of a surviving source orbit form one target W-conjugacy orbit: every target conjugator has a preimage under Phi, and source conjugation preserves i and acts transitively on x. Distinct source simple factors cannot be identified in the quotient, by the normal-subgroup description in Section2. Hence the number of W-orbits on the intrinsic simple factors of N is at most m.

Suppose N is non-basic. Then B<=N by (2). Since B is normal in N and N is a restricted sum of simple factors, B is the sum of a subset of N's intrinsic factors. Those factors already have exactly m W-conjugacy orbits, by the description of B. If N were larger than B, its additional factors would contribute at least one more orbit: conjugation preserves the subset belonging to B because B is normal in W. This would give more than m orbits in N, a contradiction. Equality N=B also contradicts the supposition that N is non-basic.

Thus N<=B. This automatic-basicity conclusion uses only surjectivity of Phi and the faithful transitive action; it has not used Hopficity of H.

## 5. Injectivity

Because Phi is basic, it induces a surjective self-map of H. Hopficity of H makes that map an automorphism. As in turn1, this implies Phi(B)=B and ker(Phi)<=B.

If ker(Phi) were nontrivial, its intersection with B would contain some S_(i,x), hence all factors of that type i by W-normality and transitivity. The quotient image Phi(B) would then have at most m-1 W-conjugacy orbits of simple factors, by the same orbit argument as above. But Phi(B)=B has exactly m such orbits. This contradiction proves injectivity.

This second proof does not require a convolution inverse or a ring-theoretic direct-finiteness theorem. It settles the full Hopficity assertion for the stated finite-product-of-simple-groups class, while leaving all other bases in the original question open in this packet.

## 6. Scope controls

A nonfaithful action need not have automatic basicity. Take X to be one point and G=H a nonabelian simple group acting trivially on X. Then G wr_X H is G times G, and the automorphism swapping its two factors is not basic. This is a failure of automatic basicity, not a non-Hopfian group.

Conversely the faithful transitive permutation-action extension above does not contradict Kochloukova's2026 example: its lamp group is abelian, whereas the present proof uses perfectness in (1) and a finite simple-factor orbit budget. Neither input is available for that abelian lamp group. The nontrivial stabilizer in the newer paper remains relevant to the original regular-action question.

The finite verifier checks the two-commutator support identity with an A5 times A5 lamp, the faithful natural S3 action, the normal-orbit subset count, and the nonfaithful factor-swap boundary. It does not infer the general theorem from finite examples.

## 7. Remaining task

Two genuine author turns are used. The original two-Hopfian-factor assertion remains unresolved. The next route will examine a perfect central extension of the simple-base class: the center can obstruct the direct-factor method, but perfectness may constrain its possible coordinate mixing more strongly than the general abelian case. Any use of existing central-extension results will retain their hypotheses and credit.
