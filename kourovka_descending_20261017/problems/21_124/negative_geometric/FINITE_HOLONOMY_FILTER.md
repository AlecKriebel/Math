# A finite-holonomy filter for a CAT(0) rank-three family

UTC: 2026-10-24T22:22:00Z. Status: proposed rigorous partial deduction, awaiting independent adversarial review. **This does not solve Kourovka 21.124.** No originality claim or publication authorization gate is satisfied by this note.

## Exact eligible family

For an integer k>0, put

G_k = <a,b,c,t | tat^-1=a, tbt^-1=ba^k, tct^-1=caba^-1b^-1>.

Thus the free fiber is F(a,b,c), and the monodromy is triangular. Here [a,b] means aba^-1b^-1, explicitly. The automorphism has inverse a↦a, b↦ba^-k, c↦c phi^-1([a,b])^-1. In particular the presentation is genuinely free-by-Z and a has infinite order.

Delage, *Which F_3-by-Zs are CAT(0)?*, arXiv:2602.08759v3, Theorem4.1, proves this group is CAT(0): for w=aba^-1b^-1 the b-level weights are N_0=1, N_1=-1, starting level0, so the first inequality is 0 < 2k. This uses the corrected paper, rather than Samuelson's erroneous general theorem. Source: https://arxiv.org/html/2602.08759v3#S4 .

## Proposed theorem: translation part killed

If k>2 and rho:G_k→R^n⋊Q is a homomorphism, Q is finite and acts linearly, and the finite part of rho(a) is identity, then rho(a)=identity. Discreteness and injectivity of rho are not assumed. The dimension n is arbitrary finite.

Proof. Average an inner product over Q, so that all its matrices are orthogonal. Write rho(a)=(A,1), and write B,C for the orthogonal linear parts of rho(b),rho(c). Choose a positive integer m killing the finite part of rho(t), and write rho(t^m)=(T,1). Commuting t and a gives t^m a^km = (T+kmA,1). From b^-1 t b= a^k t we obtain

B^-1 T = T + km A.                                      (1)

The element beta=bab^-1 is fixed by the monodromy, hence commutes with t. The element w=aba^-1b^-1=a beta^-1 also commutes with t. Because rho(a) is a translation, rho(beta)=(BA,1) and rho(w)=(A-BA,1). The relation c^-1 t c=w t then gives

C^-1 T = T + m(A-BA).                                   (2)

Substituting mA=(B^-1-I)T/k from(1) into(2) yields

C^-1 T = (1-2/k)T + (BT+B^-1T)/k.                        (3)

For k>2 all three coefficients on the right are strictly positive and sum to1. The vectors T,BT,B^-1T have equal Euclidean norm. The left side also has that norm. Strict convexity of the Euclidean norm, or expansion of the squared norm of a convex combination, forces T=BT=B^-1T. Equation(1) then gives A=0. This includes T=0. QED.

The k=2 boundary cannot be included: the coefficient of T vanishes and equality may merely give BT=B^-1T=-T. The k=1 boundary also fails. Explicit finite-cover characters below witness that both omissions are necessary.

## Consequence: a is invisible in all normal covers containing a

Let k>2. If H is a finite-index normal subgroup of G_k containing a, then the image of a in H_ab⊗Q is zero.

Proof. Given a homomorphism f:H→R, induce it to the finite-dimensional permutation module V=R[G_k/H]. Explicitly choose coset representatives r_q and write g r_q=r_{gq} h(g,q), h(g,q)∈H. The coordinate functions f(h(g,q)) form a crossed homomorphism G_k→V, with the appropriate permutation convention; equivalently one may use the standard coinduced module and inverse indices. This yields a homomorphism rho:G_k→V⋊(G_k/H). Its restriction to H has identity finite part, and the coordinate belonging to the identity coset of rho(a) is f(a), after normalizing r_1=1. Apply the theorem to conclude f(a)=0. As H is finitely generated, this is equivalent to [a]=0 in H_ab⊗Q. QED.

The same conclusion holds for a finite-index H whose coset action kills a, even if H is not normal, because this condition means its normal core contains a and restriction/transfer of characters suffices. In particular it holds for every finite abelian-monodromy cover after taking a power a^e lying in the kernel: in an abelian quotient a need not itself vanish when k>1, so a further argument is required for this latter assertion. See the next paragraph; do not silently infer it just from a∈H.

For arbitrary finite abelian quotient q:G_k→Q, q(a)^k=1. On the induced character module, the nonzero evaluation of a^e can only lie in the q(a)-fixed subspace: average over <q(a)>. This subspace is Q-invariant because Q is abelian. Projecting the crossed homomorphism onto it gives a finite-holonomy homomorphism in which q(a) acts trivially; the theorem's proof only requires that linear action be identity, not that a's abstract finite label be identity. Applying the theorem kills this projected translation, hence f(a^e)=0. Thus **every power of a lying in the kernel of every finite abelian quotient is rational-homologically zero for k>2**. This projection argument and its exact conventions remain subject to adversarial audit.

## Consequence: not RFRS, with virtual scope explicitly open

Using the normal-chain definition in Wu–Ye2504.14192v2 §7, G_k for k>2 is not RFRS. Indeed a∈ker(G_k→H_1(G_k;Q)), since the b relation gives k[a]=0. If G_k=H_0≥H_1≥... is an RFRS chain with every H_i normal in G_k, then induction gives a∈H_i: a∈H_i implies [a]=0 in H_1(H_i;Q) by the preceding normal-cover theorem, hence a∈H_(i+1). The intersection therefore contains nontrivial a. This is a contradiction.

This is **not** a proof that G_k is not virtually RFRS. A finite-index subgroup may omit a while containing a^e, and its quotient action can give a a nontrivial linear part. The argument above only excludes the finite-label-trivial case, or the separate abelian-label case. Wu–Ye already give a different CAT(0) free-by-cyclic group which is not RFRS but is virtually RFRS; therefore non-RFRS alone cannot settle the target. Source for exact definition and warning: https://arxiv.org/html/2504.14192v2#S7 .

## Checkable sharp small-parameter witnesses

For k=1, map G_1 onto C_4 by b↦1,c↦2,a↦0,t↦0. On vertices i mod4, assign the oriented a-edges the weights A=(1,0,-1,0), t-edges T=(0,0,1,1), and b,c edges weight0. The lifted b relators have weight T_i-T_(i+1)-A_(i+1)=0, while the c relators have weight T_i-T_(i+2)+A_(i+3)-A_(i+2)=0. The a relators have weight0. Thus this is an integral cellular1-cocycle evaluating nontrivially on the lifted a-loop at vertex0.

For k=2, use C_2 with b,c↦1 and a,t↦0; take A=(1,-1), T=(0,2), b,c weights0. The same formulas with c-shift1 and k=2 vanish. These are characters of the cover fundamental groups, not asserted RAAG embeddings or full virtual retracts of all cyclic subgroups.

## Exact remaining gap and prohibited promotion

The family is genuinely CAT(0), and k>2 is a plausible negative target, but the outstanding central difficulty is arbitrary finite holonomy with rho(a) having nontrivial linear part. Replacing it by the unsupported claim that every virtual-retraction character can be chosen with a trivial finite part would merely transfer the problem. Nonabelian finite quotients with a nontrivial must be searched and the general case independently analyzed. No result in this note rules out a virtually special finite-index subgroup. No paper, Zenodo upload, or tracker entry is justified.
