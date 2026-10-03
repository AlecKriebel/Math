# Corrected final adversary: sealed source-only proof stage

Author of audit: independent Codex subagent `/root/pr379_corrected_final_adversary`.
Stage timestamp: 2026-10-03 04:33:15 UTC. Initial-stage completion estimate: 85% (derivations and exact controls complete; sealing remains). Whole proposed-package audit completion estimate: 35% (no candidate content has been opened).

This stage is independent of candidate proofs, candidate code, prior verdicts, root derivations, sibling derivations, and historical audit artifacts. The parent's initial task disclosed the requested mechanism families and failure modes. Those names are an exposure and are not claimed as blind rediscovery. The mechanisms, equations, examples, proof details, code, and results below were independently constructed after reading the prescribed original sources. No external individual was contacted. No Git, index, repository-service, or acceptance action was taken.

## Literal source, claim, and exact boundary

The first external source opened was the exact supplied URL `https://ems.press/content/serial-article-files/46073`. The PDF was separately downloaded, text-extracted, rendered locally, and images of its printed pages 2588, 2589, and 2590 were visually read before any other primary paper or candidate content. Printed 2588 identifies Michael Davis, joint work with Jan Dymara, Tadeusz Januszkiewicz, and Boris Okun. Printed 2590 asks whether a virtually type FP group has finitely generated total cohomology with integral group-ring coefficients. The preceding filtration statement explicitly calls cohomology a right W-module.

The target hypothesis means: there is a finite-index subgroup H of Gamma for which the trivial LEFT ZH-module Z has a resolution of FINITE LENGTH by finitely generated projective left ZH-modules. This is Davis, `pdgroup.pdf`, printed 4, and `IGAP.pdf`, printed 229, section 7.2. The former also defines “virtually” on printed 2 as existence of a finite-index subgroup. This is stronger than a degreewise finite resolution of infinite length (FP-infinity); it is distinct from FP_1 or FP_2 and need not imply finite presentability. No normality of H is required.

For any left ZGamma projective resolution P of trivial Z, the complex Hom_ZGamma(P,ZGamma) has right action `(f r)(p)=f(p)r`. The total module is the direct sum over all cohomological degrees. The right action preserves each degree. Thus finite generation of the total module requires both finitely many nonzero degrees and finite generation in each degree. Virtual FP gives the finite degree range by the coinduction argument below. The original question is not merely a question about rational coefficients, finite generation as an abelian group, individual top cohomology, a selected Coxeter class, or arbitrary finite complexes over a group ring.

The prescribed 2006 AGT paper, printed 1289, explicitly defines cohomology with a LEFT coefficient module and the RIGHT action inherited from the group-ring bimodule. Its main Coxeter theorem is about a filtration and associated graded modules. Printed 1310, Example 5.2, warns that the abelian-group direct sum need not split as right modules. A correct integral abelian decomposition therefore cannot silently be promoted to a module decomposition. The prescribed Davis–Okun graph-products paper, Theorem 4.3, gives an acyclic flag-complex boundary for Bestvina–Brady FP groups; its section 9 explicitly includes torsion-freeness in the definition of integral duality. Sharifi's prescribed homological-algebra notes, Theorem 4.3.12, supplies the extension spectral sequence; Lemma 3.5.12 and Theorem 4.2.10 supply the flatness/Tor warning. All these are source-local meanings, not a certification of current global open status or priority.

## 1. Finite index with a genuinely nonnormal subgroup

Let R=ZG, S=ZH, and let H have finite index. Let pi_H:R->S retain exactly the coefficients supported on H. Define

`Theta(a)(u)=pi_H(u a)`, for a,u in R.

Here Coind_H^G(S)=Hom_S(R,S), with R a LEFT S-module, and its left G-action is `(g f)(u)=f(u g)`. Theta is left G-linear since `Theta(g a)(u)=pi_H(u g a)`. It is right H-linear since `pi_H(u a h)=pi_H(u a)h` for h in H. It is S-linear in its argument since `pi_H(h u a)=h pi_H(u a)`.

Choose a transversal T for the left cosets H\G. A map f in Hom_S(R,S) is determined by its values f(t). Its inverse under Theta is `sum_(t in T) t^{-1} f(t)`: in `pi_H(t t'^{-1} f(t'))`, only t'=t can survive, since `t t'^{-1}` belongs to H exactly when Ht=Ht'. Finiteness of the index is essential for this finite group-ring sum. No quotient group G/H, averaging denominator, or normality has been used.

Shapiro is verified at the resolution level: restrict a projective left R resolution P of Z to S (R is free over S), and use

`Hom_R(P,Hom_S(R,S)) -> Hom_S(P,S), F -> (p -> F(p)(1))`.

The inverse is `(f -> [p -> (u -> f(u p))])`. These maps commute with differentials and the right H-action. Consequently `H^*(G,R)|_H` and `H^*(H,S)` are right S-isomorphic. This also applies to the total direct sum.

If a right R-module M is finitely generated over R, it is finitely generated over S: expand the finite R-generating coefficients in a finite right S-basis of R, adjoining finitely many translates of the original generators. The converse is immediate. Thus the property in the question reduces equivalently to a finite-index subgroup, with no normality assumption. If H has a length-d resolution, H^i(G,R)=0 for i>d even when G has torsion and has infinite ordinary integral cohomological dimension.

The exact control uses S3 and H=< (12) >, a nonnormal subgroup of index 3. Theta is a 6 by 6 integral permutation matrix, hence unimodular, and all 432 basis cases test the identities above. A wrong alternative `pi_H(a u)` fails left G-equivariance on an explicit noncommuting triple. The norm of S3 projects to the norm of H with coefficient 1. For the finite-group boundary H={1}, this gives H^0(G,ZG)=Z (right trivial action) and higher degrees zero, rather than treating the infinite length ordinary resolution as evidence of unbounded group-ring cohomology.

## 2. What top-syzygy control proves, and why FP_1 is insufficient

Let C^{d-1}->C^d be the end of a cochain complex of finitely generated projective RIGHT R-modules and D=coker(delta). Then H^d=D is finitely generated without a coherence assumption. There is an exact sequence

`0 -> K -> C^{d-1} -> C^d -> D -> 0`, with K=ker(delta).

If D is FP_2 as a right module, K is finitely generated: compare this projective partial resolution with one having finite projectives in degrees 0,1,2. The generalized Schanuel comparison identifies K plus finite projectives with the second kernel plus finite projectives; the latter kernel is generated by the finite degree-2 image. Then H^{d-1}, a quotient of K, is finitely generated. FP_1 of D only controls im(delta), not K. Iterated downward arguments need the appropriate higher FP conditions at each successive syzygy. “Top cohomology is finitely generated” alone does not control the degree below it.

A genuine integral group-ring negative example is available inside a type F ambient group. Let

`G=F(a,b) x F(c,d)`, `height(a)=height(b)=height(c)=height(d)=1`, `H=ker(height)`.

Put x=b a^{-1}, y=c a^{-1}, z=d a^{-1}. These lie in H. The cross-factor commuting relations show a commutes with y,z and `a^{-1} x a = y x y^{-1}`. Thus the subgroup generated by x,y,z is normalized by a. Since G is generated by a,x,y,z and the quotient by this subgroup is the infinite cyclic height quotient, it equals H. In particular H is finitely generated.

The Salvetti space for G is the product of two two-petal roses. Its universal cover is a product of trees, so its height cover is K(H,1). Over A=Z[t,t^{-1}] the height-cover cellular chains have C_2=A^4, C_1=A^4, C_0=A and

`d_1=(t-1)[1,1,1,1]`, `d_2=(t-1)B`,

where, in the orders a,b,c,d and ac,ad,bc,bd,

`B=[[-1,-1,0,0],[0,0,-1,-1],[1,0,1,0],[0,1,0,1]]`.

The equations Bv=0 say v_ac=-v_ad=-v_bc=v_bd. Since t-1 is not a zero divisor in A, ker(d_2)=A*(1,-1,-1,1). There are no 3-cells. Hence `H_2(H,Z)=A`, an abelian group of infinite rank. H cannot be FP_2 over Z: tensoring any resolution with finite degree-2 projective modules by trivial Z would make H_2 a subquotient of a finitely generated abelian group. This is an exact infinite argument, not an inference from a truncated rank.

Use RIGHT group-ring modules. S=ZH has a finite map S^3->S, `(u,v,w)->(x-1)u+(y-1)v+(z-1)w`, whose cokernel is trivial Z. Thus Z is FP_1 over S. Its kernel K_H is not finitely generated, since otherwise this presentation extends to a resolution finite through degree 2, contradicting the preceding homology computation.

Induce to R=ZG. R is free and faithfully flat as a left S-module, so the kernel of the same 1 by 3 matrix over R is `K_H tensor_S R`. It is not finitely generated. To check descent here without assuming it, suppose a finite generating set of `K_H tensor R` exists, expand each generator into a finite sum of simple tensors, and let K_0 be the S-submodule generated by their finitely many first factors. Then `(K_H/K_0) tensor R=0`. Freeness of R on cosets forces K_H/K_0=0, a contradiction. The induced cokernel `Z tensor_S R` is cyclic and finitely presented over R, hence FP_1, but is not FP_2. This is an ACTUAL integral group-ring matrix over an ACTUAL type F group ring with non-finitely-generated kernel.

It is not a counterexample to the printed question. The two-term cochain complex R^3->R just used is not Hom of the trivial G augmentation resolution. The actual augmentation resolution for G has ranks 1,4,4 and square-cell coefficients `(1-c)e_a+(a-1)e_c`, etc. The independent exact code verifies each actual boundary-square cancellation and all augmentations. It does not substitute the bad matrix for those boundaries.

For completeness, the actual H^1(G,R) is zero. A finite rank free group F has the tree resolution; its dual begins `ZF -> (ZF)^2`, `r -> ((a-1)r,(b-1)r)`. It is injective because a finite supported element cannot be invariant under infinite-order left translation a. Its cokernel is torsion-free: if p divides both coordinates of this image, reduction modulo p and the same finite-support argument show p divides r; this proves the image is p-saturated for every prime. Thus H^*(F,ZF) is concentrated in degree 1 with a Z-flat module. Tensor the two tree complexes for the direct product. Integral Kunneth gives cohomology only in degree 2, whose module is a cokernel with finite target. Therefore the ambient group's actual cohomology passes the target property even though its ring supports the bad matrix above.

## 3. Height injection: exact scope and two traps

Let B be an abelian group split as `direct sum_(h in Z) B_h`. Suppose an additive map phi sends each B_h into `direct sum_(k>h) B_k`, with each individual image finite supported. Then 1-phi is injective. A nonzero element has a least occupied height h; phi cannot contribute to its height h component, so that component survives in (1-phi)v. Neither coefficient invertibility nor a scalar model is required.

The exact integral control uses two-dimensional height slices and transport `A=[[1,1],[0,1]]` to the next height. For seven finite supported input slices, retaining all eight output slices, the 16 by 14 matrix I-shift*A has rank 14. This is a checked finite instance of the least-height proof. A periodic-height version has a one-dimensional kernel. In the completed product over ALL heights, the nonzero constant sequence (1,0) is fixed by the shift and transport A. Thus finite-support cochains cannot be replaced by completed cochains. A nonascending reflection h->-h fixes the height-0 slice and gives another kernel. An argument about a stable letter must prove its actual map strictly raises the chosen grading, rather than assuming all HNN situations behave like an ascending shift.

Injectivity alone says nothing about finite generation of the resulting cokernel as a module under additional group actions. That extra property must be proved from the actual action. Likewise, an endomorphism or arbitrary matrix toy must not be asserted to occur as a cohomology differential of a virtual FP group without a realization theorem.

## 4. Integral tensor, Tor, and Bockstein

For a complex C of Z-flat groups, tensoring `0->Z --p->Z -> F_p ->0` gives the cohomological universal-coefficient exact sequence

`0 -> H^n(C) tensor F_p -> H^n(C tensor F_p) -> H^{n+1}(C)[p] ->0`.

The right map is the Bockstein, represented by lifting a mod-p cocycle v and dividing delta(v) by p. There is an integral tensor Kunneth sequence with tensor terms at total degree n and Tor terms from degrees summing to n+1. One cannot drop Tor just because the chain groups, rather than their cohomology, are free abelian. Finitely generated group-ring projective modules are Z-flat (indeed underlying direct summands of free abelian groups), but their cohomology need not be torsion-free.

An exact non-diagonal matrix control is `D=[[2,1],[0,3]]` in degrees 0->1. Its determinant is 6, so its rational cohomology vanishes. Integral unimodular matrices `U=[[1,0],[3,-1]]` and `V=[[0,1],[1,-2]]` give `UDV=diag(1,6)`. Therefore H^1=Z/6. The quotient is explicitly detected by `(u,v)->3u-v mod 6`. Mod 2, the kernel vector (1,0) lifts to Dv=(2,0), and its Bockstein is (1,0), class 3 of order 2. Mod 3, (1,1) lifts to Dv=(3,3), and its Bockstein is (1,1), class 2 of order 3. These are actual integral cocycles and quotient classes.

Tensor this non-diagonal complex with itself. The exact code constructs the integral degree-0,1,2 total matrices of ranks 4,8,4 and checks the composition is zero. The unimodular reduction decomposes each factor into a contractible 1-complex and `Z --6-> Z`. The remaining tensor factor has degree-0 image vector (6,6) and degree-1 differential (-6,6). Its degree-1 kernel is Z*(1,1), modulo 6*(1,1), and degree-2 cokernel is Z/6. Thus H^1=Tor_1(Z/6,Z/6)=Z/6 and H^2=Z/6 tensor Z/6=Z/6. Dropping Tor loses a real cohomology degree.

A genuinely negative module example for rational-only finite-generation detection is `direct sum_(n>=1) Z/2`, with trivial action of any chosen group. Its rationalization is zero. Any finite collection of integral elements has bounded combined support; all elements generated by their group-ring action stay in that support. Hence the integral module is not finitely generated. This is a genuine module negative example, not a claimed group-cohomology realization. The rational test therefore cannot establish the integral target, and no realization has been assumed.

## 5. Nonsplit extension: quotient concentration, flatness, and exact action

Consider `1->N->G->Q->1`, with N type FP and Q a dimension-d integral duality group whose dualizing module D_Q is torsion-free (Z-flat). For each q write `V_q=H^q(N,ZN)`, a right ZN-module. There is a canonical left G semilinear transport tau_g on V_q, induced on cochains by

`tau_g f(n_1,...,n_q)=g f(g^{-1} n_1 g,...,g^{-1} n_q g) g^{-1}`.

It satisfies `tau_g(v n)=tau_g(v)(g n g^{-1})`, `tau_g tau_h=tau_(gh)`. For n in N, the compensated inner conjugation on cohomology is the identity, giving `tau_n(v)=v n^{-1}`. This identity is essential. Tau need not factor through Q. It records the extension's nonsplit cocycle through the N right action.

Since N has finite projectives in each degree, its cohomology commutes with the coset direct sum in ZG. More precisely

`H^q(N,ZG)=V_q tensor_ZN ZG`.

Its commuting left Q-action is `bar(g) . (v tensor u)=tau_g(v) tensor g u`, independent of the lift since tau_n(v)=v n^{-1}. The explicit bimodule map

`v tensor g -> tau_(g^{-1})(v) tensor bar(g)`

identifies this with `V_q tensor_Z ZQ`. It is well defined under `(v n) tensor g = v tensor n g`, and it identifies the left Q-action with the regular action on ZQ. Its RIGHT G-action is

`(v tensor z).g = tau_(g^{-1})(v) tensor (z bar(g))`.

This is an honest right G-action: the first-factor transformations compose in reverse order, exactly as a right action requires, and the second factors compose normally. It requires no chosen splitting. The left Q and right G actions commute.

Apply the prescribed Hochschild–Serre spectral sequence. A finite projective resolution for Q shows `Hom_ZQ(P,V_q tensor ZQ) = V_q tensor Hom_ZQ(P,ZQ)`. The quotient dual complex has cohomology concentrated in degree d and equal to D_Q. Its integral Kunneth Tor terms vanish because D_Q is Z-flat. Thus the E_2 page is zero unless p=d, and its remaining terms are `V_q tensor D_Q`. All later differentials and extensions vanish because there is a single p column and a single q for each total degree. The result is a right G-module isomorphism

`H^{d+q}(G,ZG) = V_q tensor_Z D_Q`,

with the right action `(v tensor d).g=tau_(g^{-1})(v) tensor (d bar(g))`.

If each V_q is finitely generated over ZN, this formula gives finite generation over ZG because D_Q is finitely generated over ZQ. Given generators v_i and d_j, expand d as a finite sum of d_j bar(g), express tau_g(v) in the v_i over ZN, and use the diagonal right action to express v tensor d in the finite family v_i tensor d_j. This is a sufficient closure statement, not a converse without additional faithfulness/detection arguments.

The control is the nonsplit integral Heisenberg extension. Use triples with product `(a,b,c)(A,B,C)=(a+A,b+B,c+C+aB)`. Its quotient is Z^2 and central kernel is Z. The quotient section has cocycle `(u,v)->u_1 v_2`; exact tests check 15,625 cocycle triples and 19,683 group associativity triples. Every lift of the two quotient generators has commutator z, independent of central corrections, so no section homomorphism exists. This does not obstruct the formula: N and Q have flat dualizing module Z and concentrations in degrees 1 and 2, yielding H^3(G,ZG)=Z and vanishing elsewhere.

To test the action, use the actual Klein-bottle extension `1-><x>->G-><y>->1`, `y x y^{-1}=x^{-1}`. Its group law is `(a,b)(c,d)=(a+(-1)^b c,b+d)`, so it has actual noncommuting words. The aspherical Klein-bottle augmentation resolution has Fox degree-2 coefficients `y+x^{-1}`, `1-x^{-1}`. Multiplying them by the degree-1 coefficients x-1,y-1 gives zero exactly. Its top cohomology is

`ZG / ((y+x^{-1})ZG+(1-x^{-1})ZG) = Z`,

with RIGHT x acting +1 and RIGHT y acting -1. Indeed the right ideal is also generated by x-1 and y+1, so reduction of normal forms gives the signed augmentation quotient. The diagonal extension formula gives precisely this orientation action. A claimed trivial right action is falsified by the Fox coefficient y+x^{-1}, whose ordinary augmentation is 2 but signed augmentation is 0.

The hypotheses are real boundaries. If Q is merely type F, take N trivial and Q=Z^2 * Z, with the aspherical wedge of a torus and circle. Its actual finite cell ranks are 1,3,1; delta^1(u,v,w)=(1-b)u+(a-1)v. H^1 contains (0,0,1): if it were delta^0(r), (a-1)r=0 would force r=0 by finite support, contradicting its third coordinate. H^2 is nonzero because augmentation survives the image of delta^1. There is no quotient concentration. Omitting Z-flatness produces the real Tor degree in section 4. Omitting N's finiteness can invalidate commutation with direct sums: for N a countably generated free group with trivial coefficients, the map sending generator n to coordinate n of direct sum Z lies in H^1(N,direct sum Z), but not in direct sum H^1(N,Z).

## 6. Finite graph-of-groups boundary

A finite graph of groups with appropriate FP vertex and edge groups can be treated by a finite cellular/Mayer–Vietoris construction; the graph's finiteness is necessary for finite generation in that argument. An arbitrary INFINITE graph of trivial stabilizers is not automatically FP. Take one vertex and countably many loop edges, all groups trivial. Its fundamental group is free of countably infinite rank, whose H_1(-,Z) is the direct sum of countably many Z. A finite generating set would have finite total support in abelianization, missing another loop. It is not even FP_1. The exact code includes finite graph controls with 1,3,10 loops, but the infinite negative conclusion follows from the support proof rather than extrapolated numerical ranks.

## Strongest verified result and exact remaining gap

Verified in this independent stage: exact original claim and conventions; integral nonnormal finite-index reduction; top-degree automatic finite generation; FP_2-controlled next-degree finite generation and an actual group-ring FP_1/non-FP_2 obstruction; an actual augmentation-resolution control preventing false realization; strict-height finite-support injection and genuine omitted-hypothesis negatives; integral Tor and Bockstein effects; nonsplit duality-quotient formula with exact diagonal right action under stated hypotheses; and finite versus infinite graph boundaries.

No general positive or negative answer to the original virtually FP question has been established by this stage. The bad ring matrix and rational invisible module are not asserted to be realized as the required group cohomology. The missing general mechanism is control of lower cochain kernels, or an actual virtual FP group's augmentation-resolution counterexample. Before any package verdict, the exact repaired candidate manifest/head must be received; all five proofs, all included executable code, nested/wrapper provenance, and the full replay must then be examined against this sealed baseline. Historical findings are not current-head bindings. No acceptance, merge, current global open-status, or priority certification is authorized or asserted.
