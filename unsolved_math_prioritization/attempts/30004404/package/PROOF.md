# A zero-filling obstruction to persistent free subgroups

Problem 30004404 / OWR-17471-010. Author candidate, 4 October 2026.
Status: complete negative answer to the literal universal question, subject to independent review. This is a short deduction from classical surgery facts, not a priority or novelty claim.

## 1. Exact assertion addressed

Let E(K) be the exterior of a knot K in S^3. Fix its meridian μ and preferred longitude λ. For a reduced rational slope r=p/q, put

N_r = normal closure in G(K)=π₁(E(K)) of μ^p λ^q.

Dehn filling and van Kampen give the quotient map

q_r : G(K) → π₁(K(r)),     ker(q_r)=N_r.

The assertion under test is: for every hyperbolic knot K with no finite nonmeridional surgery, there is a subgroup H≤G(K), H≅F₂, with

H ∩ (⋃_{r∈Q} N_r) = {1}.                                    (1)

The union is important. Condition (1) is equivalent to injectivity of q_r|H for every rational r. Indeed, an element is in the intersection in (1) exactly when it lies in H and is killed by at least one q_r. In particular, (1) implies injectivity at r=0. The excluded meridional slope is ∞, not 0. These conventions and the universal formulation are checked against Motegi's printed OWR abstract, pp.491–493 [S1].

## 2. Elementary obstruction lemma

**Lemma.** If q:G→Q is a homomorphism to a metabelian group Q (meaning [Q,Q] is abelian), no subgroup H≤G isomorphic to F₂ can have q|H injective.

**Proof.** Let a,b be a free basis of H. Use [u,v]=uvu⁻¹v⁻¹. Set

c=[a,b],     d=aca⁻¹,     w=[c,d].

Both q(c) and q(d) lie in the abelian subgroup [Q,Q], so q(w)=1. On the other hand, replacing a,b by the free letters x,y and capitals X,Y by their inverses, free reduction of w is

xyXYxxyXYXyxxYXX.

This is a nonempty freely reduced word of length 16: none of its adjacent letters is an inverse pair. Since a,b are a free basis, w≠1 in H and hence in G. Thus 1≠w∈H∩ker(q). □

In fact this proves H''≤ker(q|H), with the displayed word certifying that H'' is nontrivial. No computational group presentation or finite search is needed for the lemma.

## 3. A torus-bundle group is metabelian

If M is the mapping torus of a homeomorphism of T², the bundle T²→M→S¹ yields

1 → Z² → π₁(M) → Z → 1.

The left injection follows from π₂(S¹)=0 in the homotopy exact sequence. Since the quotient Z is abelian, π₁(M)' lies in the kernel Z², which is abelian. Therefore π₁(M)''=1.

Equivalently, π₁(M)≅Z²⋊_A Z for A∈GL(2,Z). Its elements are pairs (v,n), with product

(v,n)(u,m)=(v+A^n u,n+m).

This extension is infinite, since it surjects onto Z. In particular, solvable or metabelian does not mean finite.

## 4. Verification of the figure-eight hypotheses

Let K=4₁, the figure-eight knot. The following imported topology facts are classical; their precise sources and access limitations are recorded in SOURCES.md.

1. E(4₁) is hyperbolic. Thurston constructs its complete structure using two ideal tetrahedra [S2, §§4.1–4.3].
2. The rational fillings outside {0,±1,±2,±3,±4} are hyperbolic [S2, Theorem 4.7; S3, Theorem 1.1(4)].
3. The fillings at 0,±4 are toroidal [S3, Theorem 1.1(4)]. Thus their groups contain Z² and are infinite. Independently, the zero filling is a torus bundle over S¹ [S2, p.70; S4, §3.1, printed p.524].
4. The fillings at ±1, ±2, ±3 are Seifert fibered with base orbifolds S²(2,3,7), S²(2,4,5), S²(3,3,4), respectively [S5, §9.4, p.71; amphichirality is also explicit in S2, p.61]. Their fundamental groups surject onto the corresponding orbifold groups.

Here is why these facts verify **all** rational slopes, not just a sample. For any rational r outside the nine displayed slopes, the closed hyperbolic manifold K(r) has infinite fundamental group: otherwise its universal cover H³ would be a finite cover of a compact manifold and hence compact, a contradiction. For 0,±4, the Z² injection already proves infinitude. For the remaining six slopes, the orbifold Euler characteristics are

χ_orb(S²(2,3,7)) = 1/2+1/3+1/7−1 = −1/42,
χ_orb(S²(2,4,5)) = 1/2+1/4+1/5−1 = −1/20,
χ_orb(S²(3,3,4)) = 1/3+1/3+1/4−1 = −1/12.

Each is negative. More explicitly, a hyperbolic triangle with angles π/a,π/b,π/c exists when 1/a+1/b+1/c<1; the orientation-preserving subgroup of its reflection group is an infinite realization of the triangle group Δ(a,b,c). Hence each orbifold group, and consequently each surjecting three-manifold group, is infinite. This uses the classical triangle-group construction, not a numerical volume test.

These cases exhaust Q. Thus 4₁ has no finite nonmeridional surgery, exactly as required. The meridional S³ filling is irrelevant because ∞∉Q.

## 5. Counterexample and conclusion

By §4, 4₁ satisfies the question's two hypotheses: hyperbolicity and absence of finite rational surgeries. Its zero filling is a torus bundle, so Q=π₁(4₁(0)) is metabelian by §3. Apply §2 to q₀:G(4₁)→Q.

For every subgroup H≤G(4₁) isomorphic to F₂ there is a nonidentity w∈H∩ker(q₀). Since ker(q₀)=N₀ and 0∈Q,

{1} ≠ H∩N₀ ⊆ H∩(⋃_{r∈Q}N_r).

Consequently no such H satisfies (1). This gives a negative answer to the literal universal question in OWR-17471-010. □

The argument needs only one rational filling. It does not assert that every hyperbolic knot fails, and does not address a modified question that permits excluding finitely many slopes or assumes every filling group contains F₂.

## 6. Relation to later literature and limits

Ito–Motegi–Teragaito's April 2026 preprint defines a persistent subgroup by requiring every nonidentity element to survive every nonmeridional filling. Its §7.1 reports no known hyperbolic examples and again asks about rank-two persistent free subgroups [S6]. The elementary counterexample above rules out a universal affirmative statement with only the printed OWR hypotheses. It does **not** decide the different existential problem of whether some hyperbolic knot has such a subgroup. We do not silently interpret the later authors' intended scope, nor claim to settle that broader existence problem.

Cyclic persistent subgroups are compatible with this obstruction: an infinite metabelian group can contain infinite cyclic groups. Persistent individual generators likewise do not imply an injective map on the subgroup they generate.

No directly stated earlier negative answer to this exact OWR question was identified in the bounded search. Nevertheless, the figure-eight filling classification, the torus-bundle description, and the elementary group-law obstruction are established mathematics. First discovery and historical priority are not claimed. The topology inputs are cited theorems, not formally verified or re-proved here. The included exact controls check arithmetic and algebra only. Independent review remains required before acceptance or publication.
