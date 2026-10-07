# Turn 2: residual rigidity and the exceptional prime three

The attempted strategy is to recover the residual image from two unipotent branch generators, retaining the central sign discarded by projectivization.

Use K=Q(sqrt(5)), O=Z[w], w=(sqrt(5)-1)/2, so w^2+w-1=0. The change of parameter s=-t/2 identifies our family with C_1(s) in Darmon--Mestre, not with their different sextic family C_2(s). Their Proposition 2.1 gives the O-action over K and its Galois descent law. Their Proposition 3.1(1) gives, for every prime ideal lambda over a rational prime ell different from 2 and 5, geometric projective image PSL_2(O/lambda), except at ell=3, where it is A_5 inside PSL_2(F_9). These are credited prior results from 2000.

Here is the elementary passage back to linear images. In odd characteristic, a subgroup H of SL_2(k) whose projective image contains an involution contains -I: a lift h of a nontrivial projective involution satisfies h^2=-I. Indeed h^2=I would make h diagonalizable with eigenvalues in {1,-1}; determinant one would then force h=+/-I. Thus H is the entire inverse image of its projective image. At three this has order 120, index six in SL_2(F_9), and is the binary-icosahedral inverse image of A_5. At every other prime ideal covered by the proposition the linear image is SL_2(O/lambda).

For an independent finite control, consider U=[[1,1],[0,1]], V=[[1,0],[-(2+w),1]]. Their product has trace -w and (UV)^5=-I. Exhaustive closure over O/2 and O/3 gives orders 10 and 120 respectively. The latter has element-order counts 1:1, 2:1, 3:20, 4:30, 5:24, 6:20, 10:24. The submitted program verifies every determinant and the product relation. Its finite calculations support, but do not replace, the cited geometric theorem or an integral-lattice identification.

Outcome: ell=3 is a second established exceptional geometric level. Treating every odd unramified prime as maximal would be false. No equality for the complete 3-adic image follows merely from this residual calculation. No rational specialization is substituted for the generic geometric representation.

Citation: Henri Darmon and Jean-Francois Mestre, *Courbes hyperelliptiques a multiplications reelles et une construction de Shih*, Canadian Mathematical Bulletin 43 (2000), 304--311, Propositions 2.1 and 3.1; https://www.math.mcgill.ca/darmon/pub/Articles/Research/22.Mestre/pub22.pdf .
