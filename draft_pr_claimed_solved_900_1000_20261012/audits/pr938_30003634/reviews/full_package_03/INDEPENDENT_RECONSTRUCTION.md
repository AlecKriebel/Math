# Reviewer03 reconstruction of the exact mathematical implication

This verifies the mechanism already in frozen candidate03. It introduces no proof-search response. The original proof at immutable PR938 head2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b makes the explicit n=1 claim; the separately counted stronger proof makes the each-finite-depth claim below. Earlier PASS records and hash seals are not premises of this deduction.

## Exact theorem and boundaries

For every integer m>=3 and each finite integer k>=1 there exists a braid gamma in the ordinary kth-derived subgroup P_m^(k) whose standard oriented closure is outside the integral smooth 1-solvable filtration. Consequently P_m^(n+2) is not contained in F_n^m for every m>=3 and integer n>=1. The braid may depend on k; neither a witness in the infinite derived intersection nor an explicit arbitrary-depth construction is claimed. P1=1 and P2=Z have trivial positive derived terms. The proof does not concern rational solutions, half-level replacements, Whitney towers, lower-central terms, power subgroups or surface braids.

## Universal pointwise signature obstruction

Use [Otto's published Definition2.3](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf), printed2631–2632/PDF5–6, including the paragraph defining string-link solvability by standard closure. Let W be a compact smooth integral 1-solution of the zero surgery M_L on an algebraically split m-component oriented link. Its integral H1 is Z^m by the actual boundary inclusion, and its integral H2 is free on framed embedded surfaces L_i,D_i, i=1,...,r, with just one transverse positive dual intersection per pair. Both families' fundamental groups map into pi1(W)'.

The all-meridian character to {+1,-1}, assigning -1 to every meridian, is defined on H1(M_L)=Z^m and extends along the inverse H1 isomorphism over W. It gives a real rational rank-one local system Q_alpha. A compact smooth W has finite CW type. Its universal-cover cellular matrices evaluate to integer signed matrices under alpha. Reducing modulo2 gives the ordinary F2 cellular matrices, because both signs become1. An F2-nonzero minor has odd determinant and remains nonzero over Q. Thus each twisted rational differential rank is at least the ordinary mod2 rank. Equal cell counts give

    dim_Q H2(W;Q_alpha) <= dim_F2 H2(W;F2) = 2r.

The equality uses integral UCT: H2(W;Z) tensor F2 has dimension2r and Tor(H1(W;Z),F2)=0. Replacing mod2 homology by ordinary rational homology without that UCT check would be invalid in the presence of 2-torsion.

The character is trivial on each basis surface. Its oriented fundamental cycle therefore gives a twisted absolute class after choosing a parallel coefficient section. Normal framings give zero self-intersection. All cross-pairings vanish except the prescribed single intersections; the single local contribution is a unit±1. Rescale one class in each pair to obtain blocks [[0,1],[1,0]]. Their invertibility proves independence of all2r classes even before ambient nonsingularity is known. The upper dimension bound forces them to span the whole twisted H2. There is no hidden ambient radical or extra signature summand. For r=0 the upper bound directly makes twisted H2 zero. Ordinary and twisted forms both have signature0. Complexification preserves these signatures and gives Toffoli's unitary rank-one convention.

In [Toffoli's actual publisher typeset online version](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf), formula1.1/PDF1 gives rho_alpha(M_L)=sign(W)-sign_alpha(W)=0. Remark4.25, formula4.21/PDF31, gives the one-colour surgery expression. At omega=-1, theta=1/2, the entire zero-framed linking matrix is zero: its signature and the coefficient-sum correction both vanish. Therefore rho_alpha(M_L)=-sigma_L(-1). The source's domain is the unit circle with1 excluded; neither an Alexander-polynomial nonroot assumption nor averaging is present. Its radical convention concerns the absolute-to-relative intersection form and is compatible with the above saturation argument. Hence sigma_L(-1)=0 pointwise, including at roots. This conclusion uses no homomorphism claim for signature on all string links.

## Nonhomomorphic homogeneous signature on P3

Let s(beta) be the ordinary signature of the oriented braid closure, with positive trefoil signature-2. [Gambaudo–Ghys2005](https://www.numdam.org/item/10.24033/bsmf.2496.pdf), TheoremA and Remarks1–3/printed544–545, concern links and identify the defect with minus the Meyer cocycle. In B3 its defect has the safe bound6. Their printed575 explicitly establishes q(beta)=lim s(beta^j)/j, homogeneity, and |q-s|<=6. No knot-closing convention or limit extrapolation from finitely many powers is substituted.

Write x=sigma1, y=sigma2 and let a=x²,b=y²,h=yx²y^-1,z=(xy)³. All four are pure. The Artin relation gives

    ahb = x² y x² y = x(xyx)xy = x(yxy)xy = (xy)³ = z.

Two-strand signatures s(x^ell)=1-ell for ell>=1, split third-strand extension, and conjugacy imply q(a)=q(b)=q(h)=-2. The three-strand specialization of GG Lemma4.1/printed568–569 is s(alpha Delta3^4)=s(alpha)-8. Since z²=Delta3^4, s(z^(2j))=-8j, so q(z)=-4. A homomorphism on P3 would instead give q(z)=-6. Thus the restriction to P3 is nonhomomorphic. Nonhomomorphy on B3 alone would not prove this needed restriction statement.

## Persistence, amenability, and the essential power

For any homogeneous real quasimorphism f and normal N on which f vanishes identically, (gu)^j=g^j u_j with u_j in N implies

    |j f(gu)-j f(g)| <= D(f).

Only one application of the defect inequality is involved. Dividing by j proves exact constancy on cosets, so f descends to a homogeneous quasimorphism on G/N. For N=G^(k), the quotient is solvable of derived length at most k and is amenable. [Calegari, scl, Proposition2.65/printed33](https://math.uchicago.edu/~dannyc/books/scl/scl.pdf) proves amenable homogeneous quasimorphisms are homomorphisms; printed27 lists solvable amenability. One can verify the required rigidity by taking a right invariant mean of the bounded functions f(hg)-f(h). It yields a homomorphism within D(f) of f, and homogeneity on powers eliminates that bounded difference. The contradiction shows q is nonzero somewhere on every finite positive P3 derived term.

This general group fact is prior. [Kawasaki etal2025 Lemma7.12/printed1207/PDF40](https://msp.org/agt/2025/25-2/agt-v25-n2-p15-s.pdf) proves the stronger defect identity D_G(f)=D_N(f|N) when G/N is solvable. It is credited as such, not presented as a new group theorem or an earlier identified complete braid-solvability answer.

Choose v in P3^(k) with q(v)!=0, then an integer j>6/|q(v)|. The inequality |s(v^j)-j q(v)|<=6 forces s(v^j)!=0. Taking a power is required: q(v)!=0 alone says nothing decisive about s(v) for that representative. The power remains in the same derived subgroup. Every pairwise linking number is a homomorphism on P3, so it vanishes on P3' and all positive derived terms. The closure is algebraically split. The universal obstruction proves v^j outside F1^3.

Adding geometrically separated vertical strands is a braid homomorphism P3→P_m. It preserves derived membership and makes a split union with unknots on closure, preserving ordinary signature. The same obstruction applies with m meridians. Otto's decreasing filtration gives F_n^m⊆F1^m for n>=1. Taking k=n+2 proves the source consequence. No change of target or extra proof response is involved.

## Finite example and computational interpretation

The separately preserved expression c=[a,b], d=a^-1ca, e=b^-1cb, u=[c,d],v=[d,e], beta=[u,v] lies in P3''' by normality and commutators. Free cancellation gives104 Artin letters. Its closure has identity strand permutation and all pairwise linking0. The complete planar rotation system has104 vertices,208 edges,106 faces and48 bounded black regions; crossing incidence produces the actual48x48 Goeritz form, not merely a claimed matrix. In the calibrated convention its inertia is(23,25,0), determinant-7154819319988224 and correction0. Thus its ordinary signature is-2.

The exact Meyer reconstruction uses E=im(A^-1-I)∩im(I-B) and the source form Omega(x+y,e). The pullback to ker[A^-1-I,-(I-B)] has the same positive/negative inertia with only a fibre radical added. It never inverts a singular A-I. All104 terms, lifts, kernels, forms and degeneracies agree with the preserved complete output:50 positive,48 negative,6 zero, sum2 and signature-2. The final Burau determinant is1. Empty forms, zero blocks and off-diagonal2x2 pivots are covered by the exact code and controls.

Erle's actual printed164 off-diagonal sign refers to the previous block, while the diagram and crossing derivation use the current block. The actual witness has even B-block lengths, so the wrong formula is sign-congruent there and matching inertia alone cannot validate the correction. The retained mixed-parity example has geometric inertia(2,1,0) versus literal inertia(1,1,1). Independent crossing geometry and the separate Meyer theorem close that issue. The finite beta proves n=1 only; it is not the arbitrary-depth proof.
