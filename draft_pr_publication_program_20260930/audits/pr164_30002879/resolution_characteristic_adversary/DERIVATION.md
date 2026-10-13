# Universal resolution and coefficient-map derivation

This is the final checkable derivation of the resolution / characteristic-map family. It does not use original author code or prior verdicts. The first assessment was independently sealed before any post-seal information from the root. Everything here holds for an arbitrary field K with 1+1=0.

## 1. Definitions and exact resolutions

Let A=K[x,y]/(x²,y²), M=A/(y) and B=[[A,M],[0,K]]. Use the A basis 1,x,y,xy and the M basis 1,x. Let f=[[1,0],[0,0]], e=[[0,0],[0,1]], E=Kf+Ke, I=BeB, and q:B->A the upper-left projection. M has scalar right K action. Source provenance fixes the nontrivial permutation module: g swaps the two arrows and h fixes both, so x=g-1 acts by a rank-one nilpotent Jordan block while y=h-1 acts by zero. Source category composition can place this on the right; opposite passage gives this specified left-module algebra, and all opposite signs disappear in characteristic two.

For D=K[t]/(t²), put D^e=K[l,r]/(l²,r²), s=l+r. The multiplication map epsilon:D^e->D is the augmentation. On the displayed basis,

    s·1=l+r,  s·l=lr,  s·r=lr,  s·lr=0.

Its kernel and image both equal K(l+r)+Klr. The augmentation has this same kernel; s²=0. Therefore the augmented complex with one free D^e summand in every nonnegative degree, each positive differential multiplication by s, is exact in all degrees. There is no induction whose base cases stop at a finite degree: every differential is the same explicit linear operator.

Tensor the x and y versions over K and totalize. Tensor homology over a field gives homology A in degree zero and zero in every positive degree. (Equivalently, split each augmented complex as K vector spaces into its homology and contractible two-term pieces; tensoring the pieces is contractible.) This yields a free A^e resolution P with generators e_(i,j), i,j>=0, and

    P_n = direct-sum_(i+j=n) A^e e_(i,j),
    d(e_(i,j)) = (x_L+x_R)e_(i-1,j) + (y_L+y_R)e_(i,j-1).

Terms with negative indices are absent. The total-complex sign on the y term is also 1 over K. Applying Hom_(A^e)(-,A) gives zero differentials, since left and right actions coincide and their sum is zero.

The module resolution Q_n=A, d_n multiplication by y for n>0, augmented A->M, is exact since

    y(a_0+a_x x+a_y y+a_xy xy) = a_0 y+a_x xy,
    ker(y:A->A)=K y+K xy=yA.

Hom_A(Q,M) has zero differential and one copy of M in each degree. For coefficient a mod y, use multiplication by a on every Q term as a lift; multiplication commutes with y. For the degree-one class eta represented by Q_1->M, 1->1, use the identity maps Q_(r+1)->Q_r as its comparison lifts. They commute with d, including the shifted-complex sign in characteristic two. Their compositions are identities in every degree. Thus

    Ext_A*(M,M) = (K[x]/(x²))[eta],  |eta|=1.

No eta^n vanishes: its coefficient cochain evaluates to 1 and the entire Hom differential is zero. A different arbitrary naming of a degree-one generator could change coordinates; the identity lifts just specified fix eta exactly.

## 2. Ambient Hochschild coordinates and higher normalization

Let bar(A)=A/K1. In the normalized bar resolution Bar_n(A)=A tensor bar(A)^tensor n tensor A, define an A^e-linear map sigma:P->Bar(A) by

    sigma(e_(i,j)) = sum over all words w of i x entries and j y entries of 1[w]1.

Each word occurs once with coefficient 1. Check its differential as follows. An internal product xx or yy vanishes. An internal product xy has a unique mate from the same word with the adjacent x,y interchanged; the two terms are identical after the merge and cancel. The output contains exactly one xy entry and the remaining entries are x or y, so there are no unaccounted multiplicities. The first-letter terms partition the shuffle words into x-first and y-first words, giving x_L sigma(e_(i-1,j)) and y_L sigma(e_(i,j-1)); the last-letter terms give the two right-action terms. This proves the chain identity in arbitrary total degree. In degree zero sigma lifts identity_A.

The derivations U=d/dx and V=d/dy are well-defined because the defining square relations have derivative zero. Let u=[U], v=[V]. The cochain U^cup i cup V^cup j evaluated on sigma(e_(k,l)), k+l=i+j, is 1 if (k,l)=(i,j), and zero otherwise. Only the single ordered word consisting of i x entries followed by j y entries contributes. Hence the coefficient cochain e_(i,j)->a is exactly the class a u^i v^j, with no degree-dependent unit, factorial, or binomial factor. Since the two resolutions are projective and sigma lifts the identity, standard lifting induction constructs homotopy inverse comparisons, so this computation indeed identifies their cohomology classes.

Therefore HH*(A)=R=K[x,y,u,v]/(x²,y²), with x,y degree zero and u,v degree one. The ring presentation is universal: in degree n its monomials give all 4(n+1) coefficient cochains, and their ordered cups have the established normalization. The Gerstenhaber generator calculations are

    [u,x]=[x,u]=1,  [v,y]=[y,v]=1,
    every other generator pairing=0.

They follow from evaluation of a derivation on a zero-cochain and commutators of U,V. The bracket is a biderivation of the cup product, so for arbitrary F,G in R,

    [F,G] = F_x G_u + F_u G_x + F_y G_v + F_v G_y.

The derivations of the polynomial quotient are well-defined because d(x²)=d(y²)=0. All grading signs evaluate to 1 in this field. This identifies the ambient bracket in the exact coordinates used by the characteristic computation.

## 3. The characteristic map in every degree

Augmented P is split exact as a complex of right A modules. Proof: its target A is right-A projective, so the first surjection splits; its kernel is then a direct summand of a free right-A module, and is projective. Split the next surjection onto that kernel and continue inductively. Tensoring over A with any left module preserves these split exact sequences. In particular P tensor_A M resolves M. Its terms are left-A projective because A^e tensor_A M is A tensor_K M, free of rank 2 over A.

Define the left-A-linear map j_n:Q_n->P_n tensor_A M by

    j_n(1)=e_(0,n) tensor 1_M.

For n>0,

    d j_n(1) = (y_L+y_R)e_(0,n-1) tensor 1
             = y e_(0,n-1) tensor 1
             = j_(n-1)(y)=j_(n-1) d_Q(1).

The equality uses y·1_M=0. In degree zero augmentation sends j_0(1) to 1_M. Thus j is an actual comparison lifting identity_M. Both complexes are projective resolutions, and any two such lifts are homotopic by the same degree-by-degree lifting argument; evaluating cocycles on j therefore computes the canonical characteristic action.

Represent a u^i v^j by the A^e-cochain F taking e_(i,j) to a and the other generators of that degree to zero. Tensoring it on the right with identity_M sends e_(i,j) tensor m to a m. On j_(i+j)(1), it is zero when i>0, and otherwise equals a·1_M. Hence, for every n>=0,

    chi_n(a u^i v^j) = 0 if i>0,
    chi_n(a v^n) = (a mod y) eta^n if i=0.

This is a full-degree chain-level computation, not an extrapolation. Every class 1 eta^n and x eta^n is hit by v^n and x v^n, respectively; chi_n is onto. The kernel is (y,u)R in all degrees. In particular ker chi_0=yA. Identity shifts and sigma rule out a higher-degree renormalization that kills chi(v²) or inserts a factorial. Such altered comparison maps cease to lift the same resolution map.

## 4. Original coefficient sequence, corners, and the zero-degree exception

The normalized E-relative bar complex is

    Bar_E,n(B)=B tensor_E (B/E)^tensor_E n tensor_E B.

Its augmented bar contraction is the usual insertion of 1 followed by the class of the old first outer factor; it satisfies dh+hd=identity on the augmented complex, using E balancing to cancel the E part. Also E^e=K^4 is semisimple. Each middle E-bimodule is projective over E^e, and induction B^e tensor_(E^e) (-) takes such projectives to B^e projectives. Thus this is an ordinary projective bimodule resolution, and its coefficient cochains calculate Ext_(B^e)(B,-), not just some relative invariant.

The corners of B/E are

    f(B/E)f=bar(A),  f(B/E)e=M,
    e(B/E)f=e(B/E)e=0.

A nonzero composable tensor is either all-A, or a string of A inputs followed by exactly one terminal M. It cannot contain two M inputs or an A input after M. Endpoint linearity dictates the output corner. Write

    C_A^n=Hom_K(bar(A)^tensor n,A),
    T^r=Hom_K(bar(A)^tensor r tensor M,M).

For n>=1, cochains with coefficients B are C_A^n direct-sum T^(n-1). Degree-zero cochains commute with E and therefore are A direct-sum K; the off-diagonal M is excluded. With coefficients A=B/I, only C_A^n remains, and degree zero is A. This identifies the whole quotient-coefficient complex with the normalized Hochschild complex of A. The coefficient map induced by q is projection onto this component.

For coefficients I, degree zero is K and degrees n>=1 are T^(n-1). The first differential K->T^0 is c->c identity_M. Subsequent differentials are the standard module bar differentials. To check the latter explicitly, for g in T^r,

    (d_T g)(a_1,...,a_(r+1),m)
       = a_1 g(a_2,...,a_(r+1),m)
         + sum_(k=1)^r g(a_1,...,a_k a_(k+1),...,a_(r+1),m)
         + g(a_1,...,a_r,a_(r+1)m).

This is Hom_A of the normalized A-module bar resolution A tensor bar(A)^tensor r tensor M. Products are interpreted linearly, and zero products vanish. Because the action is nonzero, the scalar map K->T^0 is injective. Its image is inside End_A(M); hence

    HH^0(B,I)=0,
    HH^1(B,I)=End_A(M)/K = M/K,
    HH^(n+1)(B,I)=Ext_A^n(M,M) for n>=1.

Lift F in C_A^n to the all-A component of the B coefficient cochains. Its mixed Hochschild differential has the additional terminal term

    h(F)(a_1,...,a_n,m)=F(a_1,...,a_n)m.

For n>0, this is precisely the tensor-bar definition of chi_n. For n=0, h(a) is the action operator on M, whose class is taken modulo scalar operators because of the preceding K term. Thus the connecting map in the **original** coefficient sequence is chi_n for n>=1 and A->M/K, a->(a mod y) mod K, in degree zero. This proves exact agreement with gamma in the OWR question, without equating two sequences solely because their terms have similar dimensions.

The degree-zero connecting map is onto and has kernel K+yA. Every positive connecting map is onto. In the coefficient long exact sequence, the preceding connecting map therefore forces the incoming map from HH^n(B,I) into HH^n(B) to vanish. Consequently gamma_n is injective for all n; its image is K+yA for n=0 and ker chi_n for n>=1. Independently, the center computation gives the same result: an element centralizing f,e is diagonal (a,c); centralizing M requires a mod y=c. Thus a=scalar+y-term+xy-term, c=that scalar, and the projection is injective. In particular x does not belong to the image in degree zero.

Finally e is stratifying: eBe=K, multiplication Be tensor_K eB -> I is an isomorphism onto the three-dimensional upper-right/lower-right ideal, and every higher Tor over K vanishes. Thus the original hypotheses apply. The original coefficient gamma is now fully identified with this explicit restriction and agrees with the derived quotient map in OWR Lemma 4.

## 5. Structural compatibility and final result

The ordinary normalized bar resolution maps to the E-relative one by quotienting each middle input modulo E and balancing over E. Its differential commutes with this quotient: terms created by an E input cancel using the adjacent balancing relation. This map lifts identity_B between projective resolutions, so its cochain inclusion is a quasi-isomorphism. The inclusion identifies relative operations with the ordinary Hochschild cup and insertion operations: a relative cochain already vanishes when an inserted input lies in E. Consequently the relative bracket used below is the actual ordinary Gerstenhaber bracket.

Relative normalized cochains can be viewed as E-balanced cochains vanishing on E input slots, with insertions taking an output modulo E when used as a later normalized input. On all-A input slots, every positive-degree intermediate output lies in fBf=A by its endpoints. If an inserted cochain has degree zero, its output is a diagonal pair (a,c); only a contributes to f-endpoint inputs, and its Kf part is normalized exactly as the scalar part of an A cochain. The e component cannot contribute. Therefore all insertions, including zero-degree insertions, restrict to the ordinary normalized insertions in A. The same endpoint argument applies to the cup product; projection on the diagonal degree-zero corner is multiplicative as well. This proves compatibility of the actual gamma with the Gerstenhaber bracket and product.

Its image in every degree combines to

    L=K·1+(y,u)R.

For n>=1 its basis comprises x^a y^b u^i v^j with a,b in {0,1}, i+j=n and either i>=1 or b=1. The dimension is 4n+2; degree zero has basis 1,y,xy. Transporting the ambient formula through the injection specifies the bracket in every degree. Closure is also direct: (y,u) is closed under the bracket with itself, since removing either y or u by differentiating one factor leaves a y or u factor supplied by the other, and [y,u]=0. Scalars bracket to zero. For arbitrary monomials the candidate's formula follows by formal differentiation, with coefficients reduced modulo two and square-zero x/y terms removed.

The coefficient sequence is sufficient once its maps and structural compatibility are computed. Its bare vector-space dimensions would not, by themselves, determine a Lie algebra. No extra finite-field assumption, hidden scalar division, corner omission, homotopy ambiguity, or high-degree normalization is needed in this derivation. The stronger squaring and higher brace structures are not computed here.

## 6. Diagnostic scope and reproducibility

Run `python3 run_diagnostics.py` in this folder. All correctness gates explicitly raise exceptions and remain active under `python3 -O`. `TEST_RUNS.json` pins checker and harness bytes and contains all 16 runs. In each mode the original mechanism passes 2,277 checks. The independent finite calculations build P and P tensor M through differential degree 10, Q through degree 10, shuffle/ordered-cup and characteristic comparisons through degree 10, and direct normalized relative coefficient complexes yielding cohomology through degree 4. F4 calculations exercise coefficients outside F2 and confirm the finite matrices' ranks. These are bounded diagnostics; Sections 1-5 prove the arbitrary-degree and arbitrary-field claims.

Seven deliberately broken mechanisms each fail with a named DiagnosticFailure in both modes: trivial M, exchanged module generator, omitted right x action, comparison killed from degree two, factorial-weighted shuffle, omitted lower scalar corner, and characteristic-three constant differential. An initially wrong expected rank list in this new checker was itself caught and corrected: the exactness recurrence is rank(d_n)+rank(d_(n+1))=16(n+1), so rank(d_n)=8n+4 when d_0 is the rank-four augmentation. That checker correction and initial output are preserved privately and do not indicate a submission failure.

Sources and exact input hashes are separately preserved in the manifests. Full source texts, headers and renderings are private and excluded from public outputs.
