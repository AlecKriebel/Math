# Contributing check: SL(2,5), p=2

## Outcome

The proposed counterexample passes this contributing mathematical check. All three indecomposable projective F2 G-modules satisfy the positive rational-reduction condition. The dimension-eight PIM cannot lift to Z_(2)G, so Z_(2)G is not semiperfect. The obstruction is global/real Schur descent, not failure of a 2-adic lift. This is author-turn support, not the campaign's final independent audit.

Exact arithmetic replay: `python check_character_data.py` (Python and SymPy). Output: `character_checks.json`. The replay tests the full ordinary character table and full decomposition matrix; it is not sampling groups, elements, or PIMs. Its input characters are justified by the representation construction below, not inferred to be characters solely from their norm.

## 1. Central filtration and projectivity

Put A=kG, k=F2, z=-I, t=z-1, and B=A/tA=k(G/<z>)=kA5. The ideal tA is square-zero and t is central. On the two-dimensional span of each coset pair g,zg, multiplication by t has equal kernel and image. Consequently ker(t:A->A)=tA. This equality passes to every direct summand of a finite free A-module. Therefore for each finitely generated projective P,

    0 -> tP -> P -> P/tP -> 0,
    P/tP -> tP, p+tP |-> tp,

is an exact sequence and a B-module isomorphism, respectively. In particular [P]=2[Infl(P/tP)].

Also P/tP is B-projective because tensoring a split direct-summand decomposition A^n=P+Q with B preserves the splitting. If P is indecomposable, P/tP is indecomposable. One proof: End_A(P) surjects onto End_B(P/tP) by projectivity of P. The kernel consists of maps into tP and is square-zero: any two such maps compose to zero by centrality and t^2=0. Since End_A(P) is local, its quotient is local. The heads agree, so P/tP is exactly the B-projective cover of the same simple. Conversely, every primitive B-idempotent lifts across the nilpotent ideal tA, giving all corresponding A-PIMs.

This argument does not assume that the generally non-exact coinvariant functor induces a homomorphism on G_0. The class identity is proved on each projective separately.

## 2. Every F2 PIM satisfies the monoid condition

Use the three F2 A5 simples 1, U, S, of dimensions 1,4,4. The module U has endomorphism field F4 and splits over F4 into the two distinct two-dimensional simple modules. S is absolutely irreducible, and is also projective over F2 A5. Johnston–Rumynin, Example 3.4, Table 2 and the displayed p=2 calculation, give the A5 PIM vectors (4,2,0), (4,3,0), (0,0,1) and reductions

    d(V1) = [1],  d(V4) = [S],  d(V5) = [1]+[U],

where V1,V4,V5 are rational simple quotient representations of the indicated dimensions.

The central lemma doubles the vectors for G:

    [P(1)] = 8[1]+4[U] = d(4V1+4V5),
    [P(U)] = 8[1]+6[U] = d(2V1+6V5),
    [P(S)] = 2[S]       = d(2V4).

Inflation preserves rational simplicity. Thus these are precisely allowed nonnegative combinations of reductions of rational simple G-modules. Their dimensions are 24,32,8. The regular-module dimension check is 24+2*32+4*8=120; the multiplier 2 for U is dim_F4 U, not its F2 dimension 4.

## 3. Exact ordinary and modular characters

An actual character construction is provided by Chung–Kostant–Sternberg, *Groups and the Buckyball*, Section 4: identify SL(2,5) with the inverse image of the rotation group A5 in SU(2), and restrict the symmetric powers of its natural two-dimensional representation. The first six degrees 1,2,3,4,5,6 are irreducible. Taking the other Galois conjugates and the quotient degree-four representation gives the full nine-character table. In particular chi_- is the actual symmetric-cube character, with degree 4 and nontrivial central action. The norm-one calculation therefore proves its irreducibility legitimately.

Write ordinary characters in the order

    1, 2a, 2b, 3a, 3b, 4+, 4-, 5, 6,

where 3a=Sym^2(2a), 3b=Sym^2(2b). With absolutely simple modular columns (1,2a,2b,S), restriction to odd-order classes gives the decomposition matrix

    1 0 0 0
    0 1 0 0
    0 0 1 0
    1 0 1 0
    1 1 0 0
    0 0 0 1
    0 0 0 1
    1 1 1 0
    2 1 1 0.

The opposite subscripts in the degree-three reductions are intentional. The exact checker calculates this by matrix inversion, rather than assuming the entries, and verifies the rows are nonnegative integers. By Brauer reciprocity the split PIM characters are

    Phi_1  = 1+3a+3b+5+2*6,
    Phi_2a = 2a+3b+5+6,
    Phi_2b = 2b+3a+5+6,
    Phi_S  = 4+ + 4-.

Their dimensions are 24,16,16,8. Over F2 the PIM characters are Phi_1, Phi_2a+Phi_2b, Phi_S. Thus the nonsplit U case is accounted for explicitly.

The split Cartan matrix is

    8 4 4 0
    4 4 2 0
    4 2 4 0
    0 0 0 2,

exactly twice that of A5. These calculations independently match the central-filtration result.

## 4. The dimension-eight PIM cannot lift

Let E=P(S). On odd-order elements, its Brauer character is 2 times the quotient character chi_+. If E lifted to a projective Z_(2)G-lattice, the generic-fibre ordinary character Psi would vanish on every even-order element. One can prove the vanishing without a character-table assumption: restrict to the cyclic subgroup generated by such an element, extend to a complete 2-adic DVR containing the required odd roots of unity, split the odd cyclic part into eigenblocks, and observe that each block is projective, hence free, over the local group ring of the 2-part. A nontrivial 2-part element has trace zero on each regular summand.

The two degree-four characters, organized by element order, are

    order          1   2   3   4   5   6   10
    total count    1   1  20  30  24  20   24
    chi_+          4   4   1   0  -1   1   -1
    chi_-          4  -4   1   0  -1  -1    1.

The two order-five classes and the two order-ten classes agree within each of these rows. Their sum is exactly 2 chi_+ on odd-order elements and zero on even-order elements. Thus all element values force Psi=chi_++chi_-.

For chi_-, the Frobenius–Schur sum is

    (4+4+20-120-24+20-24)/120 = -1.

For example, the thirty order-four elements square to z, accounting for -120. A complex irreducible of indicator -1 occurs with even multiplicity in the complexification of every real representation. Psi contains chi_- once, a contradiction. A rational generic fibre would be real after scalar extension, so it cannot exist. Semiperfectness would lift every modular PIM, and hence would lift E. Therefore Z_(2)G is not semiperfect.

This proof only needs the global real obstruction and does not need any local Schur-index classification. It applies to every possible projective integral lift, not just the positive witness 2V4.

## 5. Splitting fields and local/global Schur-index distinction

For an independent arithmetic cross-check, Eisele–Kiefer–Van Gelder, Section 5.2, gives the rational Wedderburn decomposition

    QG = Q + M4(Q) + D1 + M2(D2) + M5(Q) + M3(D3) + M3(Q(sqrt5)),
    D1=(-1,-1)/Q(sqrt5), D2=(-1,-3)/Q, D3=(-1,-1)/Q.

The faithful degree-four character belongs to M2(D2). Thus its rational Schur index is 2. D2 is ramified at 3 and infinity, and split at 2. At 2 the odd-unit Hilbert-symbol formula gives (-1,-3)_2=+1; at 3, -1 is a nonsquare unit and the second parameter has odd valuation, giving -1. Its 2-adic Schur index is therefore 1, consistent with the existence of the PIM8 lift over Z2.

The faithful degree-six character has division algebra D3, ramified at 2 and infinity; its rational and Q2 Schur indices are both 2. The faithful degree-two pair has field K=Q(sqrt5), quaternion algebra D1, and global Schur index 2. Its only ramified places are the two real places: the place over 2 has local degree 2, which kills the Hamilton algebra's invariant 1/2. Thus the faithful degree-two local index at 2 is 1.

A convenient characteristic-zero global splitting field is Q(sqrt5,i). A convenient splitting 2-modular system has fraction field Q2(sqrt5), its ring of integers, and residue field F4. Here Q2(sqrt5)/Q2 is the unramified quadratic extension, since the integral golden-ratio polynomial X^2-X-1 is irreducible modulo 2. The quadratic extension splits all the remaining local quaternion factors. The modular field F4 realizes 1, the natural SL2(4) two-dimensional module, its Frobenius twist, and their Steinberg tensor product, so is a splitting field. Q2 alone is not a splitting field for the whole group algebra, despite affording chi_-.

Supplement: the F2 PIM of dimension 32 also has odd quaternionic multiplicities, namely one copy of each faithful degree-two constituent, and likewise cannot be the generic fibre of a rational lift. The dimension-eight obstruction is already sufficient.

## 6. Source caution: Proposition 3.3

The proof above does not use Johnston–Rumynin Proposition 3.3. Its asserted blanket isomorphism between integral and reduced Ext^1 groups fails without additional hypotheses. For trivial lattices over R=Z_(2), G=C2,

    Ext^1_RG(R,R)=H^1(C2,R)=0,
    Ext^1_F2G(F2,F2)=F2.

The central filtration of E even has both quotients S=d(V4), so it is of the stated Brauer–Humphreys form. Any extension of two inflated V4 lattices has z unipotent of finite order in characteristic zero, hence z acts trivially. But z acts nontrivially on E, because tE has dimension 4. Thus the particular extension cannot be obtained by the lifting step claimed there. This matters when auditing apparently contradictory literature assertions; it does not alter the counterexample argument.

## Sources

- D. Johnston and D. Rumynin, *On a question by Roggenkamp about group algebras*, arXiv:2507.21316v2, Proposition 1.4, Example 3.4, and caution concerning Proposition 3.3. https://arxiv.org/html/2507.21316v2
- F. R. K. Chung, B. Kostant, S. Sternberg, *Groups and the Buckyball*, Section 4, symmetric-power construction and full character table. https://fanchung.ucsd.edu/wp/groupb.pdf
- F. Eisele, A. Kiefer, I. Van Gelder, *Describing units of integral group rings up to commensurability*, J. Pure Appl. Algebra 219 (2015), 2901–2916, Section 5.2. https://openaccess.city.ac.uk/id/eprint/13180/1/commens.pdf
- Tim Dokchitser's GroupNames table provides a separate row-by-row check, with faithful quaternionic labels. https://people.maths.bris.ac.uk/~matyd/GroupNames/97/SL(2,5).html
