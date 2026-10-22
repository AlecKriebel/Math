# Turn 5 — Arbitrary degree-zero maps and the remaining completed case

AI-assisted mathematical proof candidate; independent review pending. Fifth and final author turn. Original unresolved5/5. All targets below are the explicitly defined two-strand labelled-chord crossed products; no completion convention is silently imposed on Kohno's entire question.

## 1. Units of the finite-sum algebra

Let Σ have genus g≥2, Π=π1(Σ), H=Π×Π and R=Q⟨t_γ:γ∈Π⟩. Surface groups Π are bi-orderable, so H is bi-orderable. This is a classical theorem, credited below.

For a bi-ordered group H, a product of two finite nonzero crossed-product sums over H has a unique greatest support term, the product of their greatest supports. Its coefficient is nonzero because R is a domain and the H action is by automorphisms. Thus D_pol=R⋊Q[H] is a domain. As in turn1, its positive grading implies every unit has chord degree zero, hence belongs to Q[H]^×.

The units of Q[H] are exactly qh, q∈Q^×, h∈H. To prove this directly, let a,b be inverse finite group-algebra sums. Their greatest and least supports satisfy max(a)max(b)=min(a)min(b)=1. If max(a)>min(a), inversion reverses the order and gives max(b)<min(b), impossible. Thus a has singleton support, and similarly b. This argument uses a bi-order and makes no assertion of a general unit conjecture for arbitrary torsion-free groups.

Consequently D_pol^×=Q^××H. Likewise the degree-zero component of any unit in D_hat is of this form, because it is a unit in the degree-zero quotient Q[H].

## 2. Every map to a surface group kills the collision meridian

Retain the tangent-bundle map E=π1(UΣ)→G=P₂(Σ) from turn4 and denote its fiber generator/image by c. The oriented circle bundle has the classical central-extension presentation

E=⟨A1,B1,…,Ag,Bg,c : c central, Π_i[Ai,Bi]=c^e⟩,

where e=±(2−2g), the sign depending on the fiber convention. Only e≠0 matters. One obtains this relation by trivializing the circle bundle over the one-skeleton of a surface cell structure and reading the clutching degree on the attaching circle of its two-cell. For the unit tangent bundle that degree is the tangent Euler number, equal to the Euler characteristic by the classical Euler-class/Poincaré–Hopf theorem. The fiber's order2g−2 in first homology and this central-extension interpretation are also used in Bowden's primary paper cited below.

Let f:G→Π be any group homomorphism. If f(c)≠1, then f(E) lies in the cyclic centralizer of f(c), since c is central in E. All its commutators vanish. The bundle relation gives f(c)^e=1. Surface groups are torsion-free, so f(c)=1, contradiction. Therefore **every** f:G→Π kills c.

For any multiplicative θ:G→D_hat^×, its degree-zero component splits into a scalar character and a group homomorphism ρ=(ρ1,ρ2):G→Π×Π. The scalar character kills c because c is a commutator (turn4). Each ρi kills c by the preceding argument. Hence θ(c)=1+positive-degree terms even without the natural degree-zero normalization.

It follows immediately that no injective multiplicative map G→D_pol exists: all its units are degree zero, and every such map kills c. Together with turn1's torus argument, this proves uncompleted nonexistence for n=2 on every closed orientable positive-genus surface. It is not nonexistence for the completed target.

## 3. A stronger necessary condition on a completed embedding

Let θ:G→D_hat^× be arbitrary, and let L=ρ(E)≤Π×Π be its degree-zero group image on the tangent-bundle subgroup. If either coordinate projection of L is nonabelian, then θ(c)=1. Consequently any injective θ must have **both projections of ρ(E) cyclic or trivial**.

Here is the finite-orbit argument establishing this statement. Write the two projections as L1,L2. Suppose L1 is nonabelian. A nonabelian subgroup of a closed hyperbolic surface group has nonabelian finite-index subgroups and trivial centralizer. Indeed all nontrivial centralizers are cyclic. A virtually cyclic subgroup is cyclic in this torsion-free surface group: a finite-index cyclic subgroup has a hyperbolic axis, and its normalizer acts discretely on that axis without a torsion reflection. Thus a nonabelian subgroup cannot have a finite-index abelian (hence cyclic) subgroup.

Consider a positive-degree monomial t_(γ1)…t_(γd)(a,b) with finite L orbit. Choose a finite-index normal subgroup N of L fixing every term in that orbit. The projection N1 is finite index in L1, so is nonabelian. Fixing the first chord means uγ1v⁻¹=γ1 for every(u,v)∈N; hence N2=γ1⁻¹N1γ1 is also nonabelian. Fixing the bead term forces a∈CΠ(N1), b∈CΠ(N2), so a=b=1. Fixing all chords gives γrγ1⁻¹∈CΠ(N1), so all γr=γ1. There is at most one possible such γ1 for N.

Normality of N implies each L-translate of the monomial is also N-fixed. The uniqueness just proved forces the entire orbit to be a singleton. Moreover two different finite-orbit monomials in the same degree cannot occur: use a common finite-index normal subgroup fixing both and repeat the uniqueness argument. Therefore the finite-support invariant subspace in degree d is either zero or the one-dimensional span of t_(γ0)^d with identity beads. The scalar quotient χ sending all chords to z and all beads to1 is injective on that subspace.

If θ(c)≠1, take its first nonzero homogeneous term f_d. Centrality of c in E makes f_d invariant under L, because positive-degree corrections to θ(E) do not affect this first term. The commutator identity for c gives χθ(c)=1. Thus χ(f_d)=0, contradicting injectivity of χ on the invariant subspace. This proves the assertion when L1 is nonabelian; the other projection is symmetric. Since abelian subgroups of Π are cyclic or trivial, the necessary condition follows.

## 4. The remaining gap is real

The preceding restriction does not eliminate degree-zero representations whose two E projections are cyclic or trivial. In that case the invariant homogeneous subspace may have dimension greater than one and may contain nonzero terms annihilated by χ. No proof is supplied that every completed map has natural degree zero, that such low-rank degree-zero images are impossible for an injection, or that a completed embedding exists in those remaining cases.

Thus the final scope is:
- completed two-strand torus: explicit rational injections, including a strictly filtered one with natural degree-zero part and proper graded image;
- uncompleted two-strand targets, all positive genera: no injection;
- completed two-strand genus≥2 with natural normalization, or more generally nonabelian degree-zero projection on E: no injection;
- unrestricted completed genus≥2, higher strand numbers and the full source convention: unresolved.

This is neither a proof nor a refutation of Kohno's whole original question. The source's finite-type context and the2003/2004 full-braid obstruction must remain credited, with their extra conditions distinguished. There is no novelty certification and no claimed correction to prior literature.

## 5. Primary inputs and finite controls

Bi-orderability: Boyer–Rolfsen–Wiest, Orderable3-manifold groups, Ann.Inst.Fourier55(2005),243–288, Theorem1.4, https://numdam.org/item/10.5802/aif.2098.pdf. The surface centralizer/axis fact is also explained with proof in Lurie, https://math.mit.edu/~lurie/937notes/937Lecture36.pdf, Lemma1; its local download returned404 but the complete primary PDF was read through the web tool. Circle-bundle Euler extension and fiber homology: Bowden, Flat structures on surface bundles, AGT11(2011),2207–2235, printed2213–2214, https://msp.org/agt/2011/11-4/agt-v11-n4-p12-p.pdf. The algebra and pure commutator inputs remain González–Meneses–Paris and Bellingeri–Funar as cited in earlier turns. Classical ingredients are not claimed as new.

`python turn5/check_euler_boundary.py` checks432 exact nonzero-Euler leading-power cases and ordered-support bounds, with1,305 assertions. It does not prove the infinite-group facts or the general finite-orbit lemma; those are analytic arguments above. All earlier frozen files are unchanged.

Original unresolved5/5. Informal completion estimate55%. Five genuine author turns are complete; no sixth author search. Full independent source/proof review is required before any final disposition or PR.
