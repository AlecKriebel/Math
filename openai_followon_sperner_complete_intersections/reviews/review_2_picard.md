# Independent Picard/curve/descent falsification pass

Checkpoint: 2026-10-07T05:39:56Z. Estimated completion of this assigned audit: 90%. This estimate concerns the source audit, not the underlying EGH research goal.

Scope: exact pinned `build/sections/05-curves.tex` and `06-descent.tex`; `07-index.tex` read only for the downstream interfaces. No existing reviews, research notes, or audit documents were read. No source modifications, commits, pushes, publication, or external communication were made.

Source SHA-256:

- `05-curves.tex`: `5cfe4627325738e6b311be9521afe2d8ab5fc3f2b9557bdecf162baad70a8774`
- `06-descent.tex`: `0f63e6a6cc362f49f582c1794291d97f1d2e1599b05ed4bb181655c0032e91dd`

## Exact target and finding

The target is the actual construction behind Proposition binary-curves and Proposition rank-to-euler, rather than merely their stated conclusions. I sought a counterexample or unsupported transfer at (1) formal monomials versus line-bundle sections, (2) genuine versus projective transport, (3) determinant correction and rank extraction, (4) Morita transport and coherent spreading, and (5) divisibility on a possibly singular quotient.

No substantive failure was found in these mechanisms. The strongest reconstructed conclusion is conditional on the geometric properties of the parameter variety stated at 06 lines 71–79: the curve data exists as stated; transport descends `End(E)` to a central simple algebra of the stated degree; every finite right module of reduced rank `r` gives a genuine equivariant coherent class `beta` with fiber Euler number `±r` and all twist Euler numbers divisible by `e0^2 e1` before matrix-idempotent reduction. These are precisely the two numerical inputs used by Section 07. This report does not certify the separate parameter-space connectivity theorem or the full Section 07 division proof.

## Reconstruction and countertests

### 1. The monomials are actual degree-b sections, not fictitious degree-one roots

05 lines 102–126 define the curve as the normalization of the coordinate-power preimage of a line. For `j=1,...,b-1`, valuation at `s=zeta^(-j)` of `(1-zeta^j s)/(1-s)` is one and those of the other ratios are zero. Thus a product of powers of these ratios is a b-th power only if all its exponents are zero modulo b. This gives the Kummer degree `b^(b-1)` also for composite b; no prime-power assumption enters.

The coordinate-power map is finite. Every projective component of the preimage has dimension at least one, hence dominates the line. An integral generic fiber therefore rules out an extra component hidden over a special fiber. Normalization gives a smooth connected curve.

At `s=1`, the simultaneous Kummer adjunction has local degree b, rather than a product of local degrees: all ratios are a uniformizer to exponent -1 times a unit, and all complex formal units have b-th roots. At each other branch point there is just a simple-zero ratio. The `s -> t=s^b` cover introduces only 0 and infinity. Thus the `t`-cover has the three stated branch values with index b. The cyclic auxiliary cover has valuations `(1,1,-1,-1)` at `(0,1,2,infinity)`. Any nontrivial intermediate auxiliary field ramifies at 2; the original G-cover does not. Their intersection is trivial. Local normalized base change removes the matching ramification at 0,1,infinity, proving `C -> T0` is étale.

The genuine linearization at 05 lines 189–199 uses `O(b)`, where the diagonal `mu_b` acts trivially. Consequently the degree-b monomials are sections of the pulled-back line L. The source explicitly treats the individual `p_j` as formal homogeneous-coordinate labels (05 lines 34–39), so it does not require non-existent sections of L whose b-th powers are the sections `p_j^b`. The relation `v^b = product_j(z-zeta^j u) = z^b-u^b` is an equality in `L^b`. Both pencils have no common zero; their pullback degrees give `deg L=e=b^b`.

Boundary checks: for b=2, C' is P1, G is C2 x C2, T0 and C have genus one, and `deg L=4`. Here theta vanishing excludes precisely A=O, as the source says. For b=3, C' has genus one, T0 genus two, C genus 28, and `deg L=27`; the same `deg(A L^(gT-1))=g(C)-1` calculation remains exact. The b=2 case does not require a faithful action on Pic0: a faithful auxiliary representation R later ensures the generic-field action is faithful.

### 2. Free graded module and transport

05 lines 252–293 start with a generic line of degree `g-1` outside the theta locus, so both H0 and H1 vanish by Riemann–Roch. For `V=pi_*(A L^gT)`, projection formula gives `H*(V(-1))=0`. On P1 each point q has `O(-q) ≅ O(-1)`. Evaluation therefore identifies H0(V) with every rank-e fiber. Its global evaluation map is an isomorphism, proving `V ≅ E_A tensor O` and the multiplication isomorphisms in every nonnegative degree. This proves the matrix construction over the field of definition as well, since the map becomes an isomorphism after algebraic closure.

Commutativity is a statement about the polynomial endomorphisms `M_a`, because they are multiplication on this common free section module. It does not entail pairwise commutativity of their separate U and V coefficients. The source explicitly preserves this distinction at 05 lines 314–315.

A normalized universal line exists because the curve is constant and has a chosen rational point. On the non-effectivity open, higher cohomology vanishes and the section dimensions are constant; the multiplication maps are therefore algebraic there. Under simultaneous parameter and curve transport, the two universal lines represent the same Picard class and differ by a line from the parameter base. At the generic point any choices of identification differ by a nonzero scalar. The same scalar acts on source and target section spaces, so conjugation on endomorphisms is independent of it. Successive choices produce only another scalar, which again cancels. Thus the semilinear action on `End(E)` satisfies the group law exactly even though E need not carry a genuine H-linearization.

Transporting the multiplication map also transports u and v to `chi(g)u` and `psi(g)v`; this gives exactly `M_(g_*a)(U,V)=(g_coeff M_a)(chi(g)U,psi(g)V)`. There is no character assigned to a fictitious section p_j of L.

### 3. Pic1 freeness and character maps

05 lines 357–366 give a complete cyclic test: if an element of order r fixes a degree-one line class, an isomorphism of its transports has r-fold composite a scalar. Over C one can rescale by an r-th root to obtain genuine cyclic linearization. Étale descent then makes the degree-one line a pullback from the cyclic quotient, forcing `1=r deg(V0)`. This excludes every nonidentity stabilizer separately and proves freeness of the full group action on Pic1. It makes no incorrect claim that every full-group invariant line has a full-group linearization.

For a character xi, lift its monodromy class in `H1(T;Z/b)` to integral H1, using the free abelian integral H1 of a compact oriented surface. The form `q*alpha/b` has integral periods on C because every projected closed loop has trivial covering monodromy. Its integral over a path from c to gc is the specified character modulo Z. Its G-invariant harmonic form extends uniquely to a translation-invariant integral form on the Pic1 torsor through the Abel map's integral H1 isomorphism. The ratio of its exponentiated integrals under g has differential zero and is constant; the Abel image fixes that constant to xi(g). This proves the continuous equivariance statement, not an unneeded algebraic equivariance assertion.

### 4. CSA descent, Morita dimension, and spreading

06 lines 77–94 ensure K is a field and H acts faithfully through R. The finite-group fixed-field theorem makes `K/F` H-Galois. Exact semilinear descent of multiplication and the unit identifies `End_K(E)^H` with a central simple F-algebra whose scalar extension is `End_K(E)` and whose degree is `dim E=e1`. This establishes central simplicity only; division requires the subsequent numerical argument.

For a right Delta-module of dimension `(e0 e1) r`, tensoring over `End(E)` with its left standard module E gives dimension `e0 r`. The right Delta0-action commutes with the End(E)-action, so it survives this tensor product. If a chosen identification of one universal A-line is multiplied by lambda, the transport of this Morita module is multiplied by lambda: its weight is +1, as required later.

The Hom-line `J_g` at 06 lines 159–177 exists on all T because the simultaneous transports represent identical curvewise Picard classes; normalization makes their difference pulled back from the base. Evaluation and composition give the associative cocycle `J_g tensor g_*J_h -> J_(gh)`. The original module has genuine descent, so the only remaining projective factor belongs to these line identifications.

For coherent spreading, finitely many rational generators and their Delta0 basis multiples give a coherent subsheaf of rational sections. The corrected transports of this finite set of coherent subsheaves remain coherent (locally finitely generated modules inside a rational vector space). Their finite sum is stable under corrected transport because it permutes the summands through the actual associative J-composition. Generic fiber, Delta0-action, and composition law are preserved. This does not assume flatness over R.

### 5. Determinant cancellation and rank extraction

For degrees `(deg A,deg V)=(0,1)`, Euler characteristics are `(1-g,2-g,2-g)`. The determinant product

`D = det RΓ(A V)^(-1) tensor det RΓ(A) tensor det RΓ(V)`

has scalar weights `(-chi(AV)+chi(A), -chi(AV)+chi(V))=(-1,0)`. It cancels the +1 weight of the Morita module. Dependence on an identification of V cancels by itself. Functoriality of determinant of cohomology and associative composition of J identify sequential and composite transport, so the resulting equivariance is genuine, not merely projective. A fixed determinant-of-cohomology line for O_C can carry an ordinary group character, but that already satisfies the group law and affects no Chern-class calculation.

The coordinate origin R=0 is fixed. Its finite equivariant Koszul resolution makes derived restriction a coherent equivariant class even if X is singular. Over the smooth open, F is perfect of constant rank `e0 r`; derived restriction preserves alternating rank. After splitting Delta0 and taking a primitive right idempotent, rank becomes r. Its fiber over x is `pr_B*gamma_x tensor D`, with `rank gamma_x=r`.

By GRR on the curve projection, `c1(D)=-q_*(a v)`. The signed exponential sum has zero degree-two term and degree-four term `-a v`; the constant term meets no degree-four Todd term on a curve. Normalization removes pure base components; degree A=0 removes a pure curve term; the degree-one curve term of v cannot multiply the mixed a-term nontrivially. Thus c1(D) is entirely in `H1(B) tensor H1(P)`.

The universal mixed classes identify each Picard integral H1 lattice with the curve lattice via the Abel map. Contracting a and v uses the unimodular symplectic intersection form. The resulting mixed pairing has determinant ±1, rather than an extra factor of two. In a symplectic basis the paired terms use each B variable and each P variable once; expansion of `theta^(2g)/(2g)!` produces exactly the determinant. Products of curves give separate unimodular blocks. Picard tangent bundles are trivial. Any top-degree term on P from exp(theta) already uses top degree on B, so positive-degree Chern-character terms of gamma vanish. Hence the fiber Euler number is exactly `±rank gamma`, with fixed sign.

An independent subagent was assigned this numerical and scalar test directly from source, with no existing-review context. Its completed report is `reviews/review_2_determinant.md`. It independently obtained the same coefficient-one determinant calculation, unimodular pairing, scalar weights, and singular-quotient Euler identity. Its genus-one expansion is `theta=t1 wedge s2-t2 wedge s1`, with `theta^2/2=-t1 wedge t2 wedge s1 wedge s2`; thus even the smallest admissible genus gives a unit, not an extra factor of two or four.

### 6. Divisibility for a singular quotient

The free action on P implies the action on `Z x X` is free. Its projective finite-group quotient is a scheme and the map is a finite étale H-torsor. Genuine equivariant coherent sheaves, including each term of beta and each twist, descend with their commuting Delta0-actions. The cohomology of every descended term is a finite right module over the division algebra Delta0, hence its dimension is divisible by `e0^2`.

The torsor Euler lemma at 06 lines 353–385 is valid on a singular projective base. Put `d=[delta_*O]-a` in vector-bundle K0. Its action lowers dimension of support on coherent G0 because the two equal-rank bundles are isomorphic on a dense open of each integral support. Thus this action is nilpotent. Pullback d is zero on the torsor, and projection formula gives `(a+d)d=0`. Rationally `a+d` is invertible by its finite nilpotent expansion, so d acts as zero on `G0 tensor Q`. Euler characteristic kills torsion, yielding exactly `chi(delta*alpha)=a chi(alpha)`, with no smoothness or perfectness assumption on alpha.

Consequently every twist has `chi(Z x X,beta(l)) in e0^2 e1 Z`. Flat field extension preserves finite coherent cohomology dimensions, and primitive idempotent reduction over C divides them by e0. This establishes the integer inputs stated in Proposition rank-to-euler.

## Remaining boundary of this pass

The division conclusion still depends on the independent parameter-space geometry and the Section 07 comparison between the two Euler inputs. No unsupported equivalent claim was encountered inside the assigned Picard/descent mechanism. No full-theorem claim follows merely from the absence of a counterexample in this bounded pass.

Final checkpoint: 2026-10-07T05:42:03Z. Assigned audit completion estimate: 100%. No substantive issue found within this scope; the numerical core also passed an independent source-only adversarial subcheck.
