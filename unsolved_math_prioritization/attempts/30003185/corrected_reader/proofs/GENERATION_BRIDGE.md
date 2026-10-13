**Integrated reader status.** This is the FULL original conditional generation bridge, preserved without rewriting its body. Its former CR source gate is now bypassed by the [192-class theorem](CLASS_GENERATION.md), using exactly the closed strong balance range and c=192. The rest of this reduction remains active. Statements below that original PS2011 retrieval is required describe its historical status, not a current dependency. The original article remains unverified. See the [integrated theorem](../README.md) and [dependency map](../DEPENDENCIES.md).

# A generation bridge for the natural symplectic and orthogonal Bray bounds

Authored 13 October 2026. This document separates a proved reduction, a refinement of the orthogonal counting argument, and the published class-generation theorem on which the final conclusion depends. It does not claim a new proof of the latter theorem.

## 1. Conclusion, scope, and source qualification

For each exact natural matrix group

- G = Sp(V), with q odd and n = dim V even; or
- G = O(V), SO(V), or Ω(V), for a nondegenerate quadratic space over F_q, q odd,

let t be a strong involution, meaning that both t-eigenspaces have dimensions in [n/3, 2n/3]. Independently sample uniform g_1,...,g_M in this exact G, and set

z_i = inv(t t^{g_i}),  H = <z_1,...,z_M>,

where inv(y) = 1 for odd |y| and inv(y) = y^{|y|/2} for even |y|. Then H ≤ C_G(t): conjugation by t inverts t t^{g_i} and therefore fixes its unique involution whenever its order is even.

Subject to the class-generation theorem precisely recorded below, there are absolute constants c and d_0 for which the following holds. Set

κ = 1/40000 for Sp; κ = 1/10000000 for O, SO, Ω.

The orthogonal κ deliberately uses an additional spinor restriction, proved in Section 3; it does not change the separately audited 1/5000000 marginal theorem. Suppose

n ≥ max(49152, 3d_0) in the symplectic case,
n ≥ max(98304, 3d_0) in the orthogonal cases.

For any 0 < η < 1, set

L = ceil(κ^{-1} log n · log((2c+1)/η)),  M = (2c+1)L.

Writing a = dim E_−(t), b = dim E_+(t), one has

P(H contains C_G(t)'') ≥ 1 − η − q^{−a} − q^{−b} − 13q^{−2b²/9}.       (1)

One may designate either eigenspace as B; no ordering a ≤ b is needed for (1). In particular η = 1/20 gives success greater than 0.9 at the stated large-dimension cutoffs. For 0 < δ < 1, independently repeat this entire experiment

r = ceil(log(1/δ)/log 10)

times and retain all outputs. The resulting subgroup contains C_G(t)'' with probability at least 1−δ, using rM = O(log n · (1+log(1/δ))) random group samples. For δ fixed, the sample bound is O(log n). Sample count is not a bit-operation or field-operation bound.

All form types and odd orthogonal natural dimensions are included. There is no assertion for projective involutions whose lifts have order four, similitude groups, non-natural representations, arbitrary intermediate classical groups, or dimensions below the stated cutoffs. GL/GU logarithmic-sampling results remain credited prior literature.

**Source qualification.** Actual theorem text has been retrieved and inspected in the 2013 coauthored survey by Niemeyer–Praeger–Seress, Theorem 2.53, printed p.77, which explicitly attributes the result to Praeger–Seress 2011. The original 2011 full article has not yet been retrieved. Its publisher abstract alone is not being treated as a full-text inspection. Thus (1) is proved conditionally on the explicitly stated CR(Sp,Ω) input. The inspected author restatement supports that input but does not verify its exact Ω ambient scope; the original-source definition check is a material remaining gate. The deduction and all direct-product issues are proved here. No numerical value of the published c or d_0 is claimed.

## 2. Required class-generation input (CR) and its source status

The required statement CR is the specialization below, supported by the general all-classical wording of Niemeyer–Praeger–Seress, *Estimation Problems and Randomised Group Algorithms*, Lecture Notes in Mathematics 2070 (2013), 35–82, Theorem 2.53, DOI https://doi.org/10.1007/978-1-4471-4814-2_2 . It is attributed there to Praeger–Seress, *Probabilistic generation of finite classical groups in odd characteristic by involutions*, J. Group Theory 14 (2011), 521–545, DOI https://doi.org/10.1515/JGT.2010.061 . An author-uploaded full survey is available at https://www.researchgate.net/publication/267434148_Estimation_Problems_and_Randomised_Group_Algorithms .

Fix α = 1/4 and β = 3/4. There exist positive integers c and d_0 such that, for q odd and a natural classical group J = Sp(U) or Ω(U) with e = dim U ≥ d_0, the following is true. Given any prescribed sequence of c J-conjugacy classes of involutions whose fixed-space dimensions r satisfy αe < r < βe, independently choose one uniform element from each class. Their generated subgroup contains J with probability at least 1−q^{−e}.

Here d_0 may be increased so that the survey's strict dimension condition e > n(α,β) holds and all groups are quasisimple. We apply the theorem only to the perfect groups J = Sp(U), Ω(U); their generalized Fitting subgroup is J itself. Therefore the survey's ambiguous use of the generalized Fitting notation for larger groups (it informally identifies that subgroup of GL with SL, omitting some central scalars) has no effect on this application. We do not apply an unqualified version to O, SO, GL, or GU.

This input supplies a uniform guarantee for every fixed class sequence, not only for a random choice of classes or for repeated samples from one class. The c samples must be mutually independent. Conditioning on their individual classes is therefore legitimate only after independence and class-uniformity have been established. Sections 4 and 7 do exactly that.

Using (1/4,3/4) avoids any endpoint issue in the survey's strict balance convention: every strong involution with both eigenspaces in [e/3,2e/3] satisfies it. The input requires e ≥ d_0 for each factor, hence the factor 3 in the final ambient cutoff. The c,d_0 depend only on these two fixed fractions, not on q, e, t, or the class sequence. The survey does not explicitly enumerate Ω in this theorem; its earlier Table 2.1 belongs to different results and is not its ambient-group definition. Direct inspection of the original 2011 Ω ambient conventions remains a documentary gate. The proof below is unconditionally a reduction under the stated CR(Sp,Ω) hypothesis, and its literature-based conclusion retains that source qualification.

## 3. An orthogonal refinement with both restrictions in Ω

The independently audited orthogonal marginal proof establishes, for each selected t-eigenspace U, P(z|_U strong) > 1/(5000000 log n), for n ≥ 98304 and G separately equal to O, SO, or Ω. We now refine its actual counted construction, rather than infer that spinor norms are independent of that event.

Use its notation V = A ⊥ B, dim A = a ≤ b = dim B, and t = −I_A ⊕ I_B after its justified orbit reduction. A counted graph F:A→B has K = F*F with squarefree characteristic polynomial f = f_* f_0. The distinguished factor f_* has degree k divisible by a power of two d ≥ 4, the remainder has degree a−k ≥ a/6 > 8, and the distinguished eigenvalue block has strictly largest order 2-part. Therefore z has negative space U_* in A and F(U_*) in B, each of dimension k, and is positive on all other blocks. The distinguished factor also satisfies χ(det(K|_{U_*})) = +1.

For each of the s irreducible primary factors, the self-adjoint construction offers two trace-form square classes. Changing its trace coefficient by a nonsquare changes its F_q-discriminant by a nonsquare. Exactly 2^{s−1} of the 2^s choices give the specified total discriminant of A; each operator orbit has the same centralizer order 2^s. Because f_0 has positive degree, s ≥ 2. Impose in addition

χ(disc(U_*)) = +1.

Exactly one trace-form choice for the distinguished factor has this sign. Among the remaining s−1 factors exactly 2^{s−2} choices have the complementary total discriminant. Thus this extra requirement retains exactly half the previously counted K, for each individual admissible polynomial f. It does not alter the embedding count for F, the signs of det K and det(I+K), or the probability mass of each surviving K orbit.

The forms on U_* and F(U_*) have discriminants related by det(K|_{U_*}), a square. Their discriminants are therefore both squares. Since k is divisible by 4, in particular even, each restriction z|_A,z|_B has determinant (−1)^k = 1. On a k-dimensional negative space W with an orthogonal basis, the spinor norm of −I_W is the product of its basis Q-values, namely 2^{−k}disc(β|_W) modulo squares. As k is even, 2^{−k} is a square. Hence both spinor norms are trivial. This proves

z|_A ∈ Ω(A),  z|_B ∈ Ω(B).

For either separately selected target eigenspace U, the same construction therefore gives

P(z|_U strong AND z ∈ Ω(A)×Ω(B)) > 1/(10000000 log n).              (2)

The factor one half is exact on the counted part, including all discriminant sectors and the a=b case. This is a new elementary refinement of the audited proof, not a claim that all Bray outputs satisfy (2)'s spinor restriction. It remains valid under uniform sampling in each exact O, SO, Ω because the audited t-conjugacy orbit is the same in all three groups.

In the symplectic case every restriction already lies in Sp of its eigenspace; use the accepted marginal theorem with κ = 1/40000. We call an output admissible if it belongs to L_A×L_B, where L_U = Sp(U) in the symplectic case and L_U = Ω(U) in the orthogonal case. Both cases now have the common bound

P(z admissible AND z|_U strong) > κ/log n.                          (3)

## 4. Centralizer-invariant sampling and product classes

Put C = C_G(t), D = D_A×D_B, where D_U = Sp(U) in the symplectic case and D_U = O(U) in the orthogonal case. Then C ≤ D. A matrix centralizing t must preserve its distinct eigenspaces, even if a=b; there is no factor-interchanging element in C.

For c∈C, the substitution g→gc sends t t^g to its c-conjugate, and hence sends z(g) to z(g)^c. Uniform g is invariant under this substitution. The law of z is consequently constant on C-conjugacy classes, including its atom at the identity.

In the symplectic case C=D, so its conjugacy class on a pair (u,v) is exactly u^{D_A}×v^{D_B}.

In the orthogonal case C is respectively D itself, the kernel of the total determinant on D, or the kernel of the total determinant and spinor norm on D. Fix any involution z∈C (the identity is allowed here). Since t and z commute, V decomposes orthogonally into their four joint eigenspaces. The centralizer C_D(z) is the product of the O groups on these nondegenerate joint eigenspaces. One of their dimensions is at least n/4 ≥ 3. A quadratic space of dimension ≥3 over F_q, q odd, has a hyperbolic plane and represents every nonzero field element. Reflections supported in that joint eigenspace realize both quotient pairs

(det,θ) = (−1,square), (−1,nonsquare).

These generate the full determinant/spinor quotient. Hence D = C C_D(z), for either of the two kernel-defined C. It follows that z^C = z^D. This is a proof for these commuting involutions; it makes no claim of nonsplitting for arbitrary elements.

Thus in every family, conditional on the pair of component D_U-conjugacy classes, the two components of z are independent and each is uniform in its class. This remains true after conditioning on any event determined by those two classes, including admissibility and strongness on either specified factor.

Finally, if u∈Ω(U) is strong and dim U is large, its O(U)-class is already a single Ω(U)-class. Indeed C_{O(U)}(u)=O(E_+(u))×O(E_−(u)), and at least one, in fact both, eigenspaces has dimension ≥3. The same reflection argument gives O(U)=Ω(U)C_{O(U)}(u). Consequently the selected strong restrictions in (3) are class-uniform in the exact J to which Section 2 is applied.

## 5. The exact second derived subgroup

At the stated dimensions, Sp(U) and Ω(U) are perfect and their quotients by their centers are nonabelian simple. These standard facts follow from Taylor, *The Geometry of the Classical Groups*, Theorems 8.7–8.8 and 11.47–11.48; the author-hosted corrected text is https://www.maths.usyd.edu.au/u/don/papers/gcg.pdf . The natural factor dimensions here greatly exceed every listed exception. Taylor Theorems 11.45 and 11.51 identify O(U)' = SO(U)' = Ω(U) = ker(det)∩ker(θ). Thus D_U' = L_U, and D_U/L_U is abelian.

The block-diagonal product L=L_A×L_B is contained in C in every case, including G=Ω(V): both block factors have determinant and spinor norm one. Since C/L is abelian, C'≤L. Since L is perfect and L≤C, one also has L=L'≤C'. Therefore

C' = C'' = C^∞ = L_A×L_B.                                        (4)

In the symplectic case even C=L. Equation (4) is justified in these large-dimensional natural groups only; it is not assumed universally for all centralizers or representations.

## 6. A precise subdirect-product lemma and its probabilistic escape

Let K≤D have projections containing L_A and L_B. Since each D_U/L_U is abelian and L_U is perfect,

K' ≤ L_A×L_B,  π_U(K')=L_U.

Write Z_U=Z(L_U), S_U=L_U/Z_U, and Z=Z_A×Z_B. By Goursat's lemma, the image of K' in S_A×S_B is either the full product or, if S_A and S_B are isomorphic, the graph Δ_φ of an isomorphism φ:S_A→S_B. This can also be seen directly: the two projection kernels in a subdirect product are normal in the simple factors and hence either trivial or whole.

If the image is the full product, K'Z=L_A×L_B. Because Z is central and L_A×L_B is perfect,

L_A×L_B = (K'Z)' = K'' ≤ K'.

So K already contains L. This step rules out hidden central-cover obstructions.

Otherwise the image is one fixed graph Δ_φ. If H_1=<K,z> still does not contain L, the same argument applied to H_1' shows that its image is a graph. It contains Δ_φ, so its graph is exactly Δ_φ. Since z normalizes H_1', its induced componentwise action on S_A×S_B normalizes that already fixed graph. If a_U(z_U) denotes conjugation by z_U on S_U, this requires

a_B(z_B) = φ a_A(z_A) φ^{−1}.                                   (5)

No union bound over automorphisms, no lift of φ to the quasisimple groups, and no assumption that K itself is a literal diagonal subgroup are needed. This argument works whether or not the factor dimensions/types differ; a nonisomorphic pair simply has no graph case.

The kernel of the conjugation map D_U→Aut(S_U) has size at most two. To see this, let h induce the identity on S_U. For x∈L_U, hxh^{−1}=x f(x) with f(x)∈Z_U. Centrality makes f:L_U→Z_U a homomorphism. Perfectness implies f=1, so h centralizes L_U. Its natural linear centralizer consists of scalars, and the scalars in the isometry group are ±I. An elementary verification of the scalar-centralizer assertion is given in Section 9.

Now fix K with successful projections and not containing L. Take a new independent admissible output z for which z_B is strong. Conditional on its pair of component classes, z_A and z_B are independent uniform elements, by Section 4. For any fixed z_A, equation (5) permits at most two values of z_B. Thus the conditional probability of failing to obtain L after adding z is at most

2/|z_B^{D_B}|.                                                   (6)

This bound uses the class of the strong B component. No simultaneous strongness of z_A and z_B is required, nor any relation between their negative dimensions.

## 7. Uniform lower bound on the extra class size

Let e=dim B, let s be the negative dimension of the strong z_B, so e/3≤s≤2e/3. Its isometry-group centralizer is the product of the isometry groups of its two eigenspaces.

For Sp, write |Sp(e,q)|=q^{e(e+1)/2}ψ_{e/2}, where 7/8≤ψ_j≤1. The quotient order gives

|z_B^{Sp(B)}| ≥ (7/8)q^{s(e−s)} ≥ (7/8)q^{2e²/9}.

For O, write |O(W)|=q^{dim(W)(dim(W)−1)/2}η(W). The audited uniform order bounds for positive-dimensional W are 7/6≤η(W)≤8/3. Both eigenspaces are positive-dimensional, so

|z_B^{O(B)}| ≥ [(7/6)/(8/3)^2]q^{s(e−s)}
             = (21/128)q^{s(e−s)} ≥ (21/128)q^{2e²/9}.

Consequently (6) is at most (16/7)q^{−2e²/9} in the symplectic case and (256/21)q^{−2e²/9} in the orthogonal case. Both are strictly less than the convenient uniform bound

13q^{−2e²/9}.                                                     (7)

These are class counts in the actual natural groups. In particular no quotient class-size loss has been omitted: the possible two central lifts are already allowed by the numerator two in (6).

## 8. Independent sample blocks and success calculation

Partition the M samples in Section 1 into 2c+1 disjoint blocks of length L. Label c blocks A, c blocks B, and the last block B-extra. In an A-block select the first admissible output strong on A, if one occurs; use the analogous rule for B-blocks and B-extra. The probability that any specified block fails is at most

(1−κ/log n)^L ≤ exp(−κL/log n) ≤ η/(2c+1).

A union bound shows that every block supplies its required output with probability at least 1−η. This uses the two separate marginal bounds and never a simultaneous event.

Condition on this collection event. Blocks remain independent, because the event is the intersection of events concerning disjoint independent blocks. Within one successful block, the selected output has the distribution of a single output conditional on that block's target event. For example, conditioning on its first success being at index j imposes target failure on earlier independent samples and the target event at j; the output at j therefore has precisely the target-conditioned law. Averaging over j changes nothing.

The c selected strong A restrictions are consequently independent, and conditional on their prescribed component classes each is uniform in its L_A-class. Section 2 gives that they generate L_A with conditional probability at least 1−q^{−a}. Likewise the c selected B restrictions generate L_B with probability at least 1−q^{−b}. The resulting subgroup K generated by the 2c complete outputs therefore has both required projections except with conditional probability at most q^{−a}+q^{−b}.

The selected B-extra output is independent of K after the block-success conditioning. If K already contains L, there is nothing to prove. Otherwise Section 6 and (7) show that adding B-extra fails with conditional probability at most 13q^{−2b²/9}. These selections are only devices for the proof; the actual output H retains all M outputs and requires no successful-selection certificate. All selected outputs are among those M originals, so their generated subgroup is contained in H. Combining the three possible failure sources proves (1).

For the explicit fixed confidence, both a,b≥n/3≥16384 throughout the symplectic scope and ≥32768 throughout the orthogonal scope, and q≥3. In particular q^{−a}+q^{−b}+13q^{−2b²/9}<1/20. With η=1/20, (1) gives success >0.9. Independent repetitions have probability at most (1/10)^r≤δ that none succeeds. If any succeeds, the subgroup generated by all repetitions contains L=C_G(t)''. No recognition or certification test for which repetition succeeded is required for this probabilistic containment statement.

## 9. Elementary scalar-centralizer verification

This section avoids relying on an unstated representation-theoretic absolute-irreducibility assumption.

For Sp(U), for every nonzero vector u the transvection T_u:x↦x+β(x,u)u lies in Sp(U). The image of T_u−I is the line <u>. A linear operator centralizing Sp(U) preserves this image for every u, hence fixes every one-dimensional subspace. A linear map fixing every line is scalar, as follows by applying it to basis vectors and their pairwise sums.

For Ω(U), use a Witt decomposition U=H_1⊥...⊥H_m⊥W, with m≥2 and W anisotropic, and hyperbolic bases e_i,f_i with β(e_i,f_i)=1. The large dimensions under discussion ensure m≥2. For singular u and v∈u^⊥, Ω(U) contains the Siegel transformations

ρ_{u,v}(x)=x+β(x,u)v−β(x,v)u−Q(v)β(x,u)u.

Their membership follows directly from Taylor Theorems 11.24 and 11.46 (also θ(ρ)=1 in the spinor calculation). Their common fixed space, as v varies in u^⊥, is exactly <u>. Indeed, if β(x,u)≠0 choose v outside <u>; the component of ρ(x)−x modulo <u> is then nonzero. Thus any common fixed vector satisfies β(x,u)=0, after which the fixed equations say β(x,v)=0 for all v∈u^⊥, and nondegeneracy gives x∈<u>.

A linear operator h centralizing Ω(U) must preserve each such common fixed space, so it fixes every singular line. The singular lines through e_i,f_i, e_i+e_j, and e_i+f_j for i≠j force h to be a common scalar c on the entire hyperbolic summand. If w∈W is nonzero, the two vectors

e_1+w−Q(w)f_1,   e_1−w−Q(w)f_1

are singular. They are independent, and their sum is the nonzero vector 2(e_1−Q(w)f_1) in the hyperbolic summand. Their h-eigenvalues must therefore both equal c. Subtracting yields h(w)=cw. Hence h is scalar on U. If h is an isometry, c²=1, proving the required kernel bound.

## 10. Attribution and remaining boundaries

The actual class-random generation theorem is prior work by Praeger–Seress. The strategy of adding an independent balanced output to defeat a diagonal obstruction already appears for GL/GU in Glasby–Praeger–Roney-Dougal, *Involution centralisers in finite unitary groups of odd characteristic*, J. Algebra 545 (2020), 245–299, Section 11.1, DOI https://doi.org/10.1016/j.jalgebra.2019.09.009, preprint https://arxiv.org/abs/1812.01362v2 . The present proof makes the simple-quotient/central-cover argument explicit rather than copying a claim that a proper quasisimple subdirect product must itself be a literal graph. It also uses disjoint success blocks to avoid an omitted factor of two in a two-marginal union bound.

The authored contributions here are the natural-group bridge with explicit sample bookkeeping and subdirect repair, plus the half-mass orthogonal spinor refinement. They are deductions from the accepted marginal counts and the published class-generation theorem, not a proof that no other author has obtained them. No worldwide novelty certification is asserted.

The original PS2011 full article remains a specific documentary check to complete. The inspected 2013 author restatement does not unambiguously verify the exact Ω ambient scope required by CR, and it supplies no inspected numerical c,d_0 values. Accordingly the main consequence remains explicitly conditional on CR(Sp,Ω); only the reduction is unconditionally established by this packet. Retrieval and inspection of the original theorem and its ambient definitions remain a material source gate. This packet does not establish an unconditional all-classical resolution. The mathematical proof does not assume an answer to that retrieval problem.
