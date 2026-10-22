# An explicit lattice–Schreier family for the closed handlebody Johnson kernel

## Result and attribution

For every integer g≥3, the construction below gives a countable, ordinarily generating family for

HK_g = H_g ∩ K_g,

where H_g is the handlebody subgroup of the mapping class group of the **closed, unmarked** boundary of a fixed genus-g handlebody, and K_g is the surface Johnson kernel. Every index is an unrestricted finite word over a specified finite ambient alphabet, an integer vector, and a sign. No index is selected by testing membership in HK_g.

This is an explicit application of the general Schreier kernel construction, using Omori's known normal generator, the known Johnson homomorphism, and an explicit section of its integral image. It is **not claimed to be a new geometric generator theorem**, a finite generating set, a finite normal generating set, a minimal family, or a presentation. Its usefulness is algebraic: it gives directly evaluable mapping-class words and integer coefficients, together with an exact generation proof. The image quotient itself is prior work: Holden, Proposition 7.3, attributes it to Morita. The elementary lift formulas below make this quotient usable without an unspecified choice of a lattice basis or lifts.

Genus two is excluded from this theorem because the Omori input used here is only authenticated for g≥3. The identity I_2=K_2 does not repair that input. Genus two is treated separately.

## 1. Fixed geometric and algebraic data

Write H=H_1(∂V_g;Z). Choose meridian curves with classes a_1,…,a_g and dual longitude curves with classes b_1,…,b_g, oriented so that a_i·b_j=δ_ij. The meridian Lagrangian is A=Z⟨a_1,…,a_g⟩. Set

ω=Σ_i a_i∧b_i,
E=Λ³H,
Q={x∧ω:x∈H},
J=E/Q,
W=ker(Λ³H→Λ³(H/A)).

Thus W has the evident integral monomial basis consisting of all ordered triples in a_1,…,a_g,b_1,…,b_g containing at least one a. In this note juxtaposition of three homology vectors means their exterior product.

We use the closed Johnson homomorphism τ:I_g→J. It is a homomorphism, it is equivariant under the ambient mapping class group, and its kernel is K_g. For a bounding pair with common homology class c and a genus-h side having symplectic basis u_l,v_l, its value is the class of c∧Σ_l u_l∧v_l, with the sign fixed by the order of the two twists. These are the standard Johnson facts used, not additional conjectures.

Choose the standard Omori genus-one homotopical bounding pair, with its genus-one side containing the first handle and common class b_2. Its two curves are C_1,C_2 in Omori Figure 1. Geometrically one can obtain this side by joining a punctured-torus neighbourhood of handle 1 to a longitude on handle 2 by an untwisted band in the planar part of the boundary. Compress the genus-one side along the first meridian disk, toward the handlebody; the resulting proper annulus has the same two boundary curves. They are nonmeridians. This verifies extension of their opposite-twist product.

Take h to be T_C1 T_C2^{-1}, or its inverse according to the Johnson sign convention, so that

τ(h)=[q],  q=a_1 b_1 b_2.

Fix this sign once. Changing the global sign of τ would have no effect on the kernel or the theorem. Omori's Theorem 1.2, followed by capping the boundary disk, gives

HI_g=H_g∩I_g=⟨w h^{±1} w^{-1}:w∈H_g⟩.

Here normal closure is taken in **H_g**. This does not assert ordinary cyclic generation.

### A finite ambient word alphabet

For fully discrete indices use Wajnryb's closed-handlebody alphabet

X=(A_1,S_1,R_12,T_1,U),

where A_i,B_i,E_i are twists about the curves α_i,β_i,ε_i in his Figure 1, D_12 is the twist about δ_12, and

S_1=B_1 A_1² B_1,
T_i=E_i A_i A_{i+1} E_i,
R_12=B_2 A_2 D_12 B_2,
U=T_1⋯T_{g−1}.

Wajnryb, Definition 3 and Theorem 19, proves that these five maps generate H_g for g>1. This result is used only for generation, not for the correctness of every relation in his longer presentation.

The curve conventions are independently recoverable from his cut-open model: cut along the meridians α_i to obtain a sphere with boundary circles indexed −g,…,−1,1,…,g, with opposite-index circles glued by reflection. The longitude β_i is the arc joining the opposite circles ±i. The curve ε_i is represented by the two arcs joining i to i+1 and −i to −i−1. The standard δ_12 surrounds the two positive circles 1 and 2 as in Figures 9–10. These curve descriptions and the cited figures fix the isotopy classes; arbitrary winding around other holes is not allowed.

Let X^± be the ordered signed alphabet obtained by appending inverses. All products act from right to left. Let ρ:H_g→Sp(H) denote homology action. It is computed for the above words from the twist formula

T_c(x)=x+([c]·x)[c]

under the selected twist convention (replace every twist formula consistently if using the opposite convention). Curve homology can also be computed directly by signed intersections:

[c]=Σ_i(([c]·b_i)a_i−([c]·a_i)b_i).

The marked standard models are identified once so that the α_i and β_i give the chosen meridian–longitude basis and the seed is the standard two-handle HBP described above. Consequently ρ(w) is a finite, exact integer computation for every word w over X^±. No handlebody membership oracle is needed: all letters are already known to extend.

## 2. Completely specified ambient lifts of elementary matrices

The image ρ(H_g) is the full integral symplectic stabilizer of A. This is Omori Lemma 3.1 in the disk-fixed model; its matrices and surjectivity remain valid after capping.

For each permutation σ, let P_σ denote a handlebody word acting by a_i↦a_σ(i), b_i↦b_σ(i). For i≠j, let L_ij denote a handlebody word acting by

a_j↦a_j+a_i,  b_i↦b_i−b_j,

and fixing all other basis vectors. These maps may be realized by handle permutations and elementary handle slides. To remove any unstated lift choice, the following is the definition used here:

Enumerate words over X^± by length and then lexicographically, including the empty word. Multiply their homology matrices. Choose the first word whose matrix is the specified permutation or the specified block matrix diag(I+E_ij,(I+E_ij)^{-T}).

This search terminates by the preceding surjectivity theorem. It is a search for finitely many **ambient matrix lifts**, not an enumeration of the target group. Matrix equality is decidable over Z. It is permitted to replace these selected words by any explicit verified lifts; the resulting family still generates the same group. For an additional concrete anchor, Omori §3.1 gives an annulus-twist lift of the elementary matrix with A-block I+E_12.

Let M_i be the meridian twist, or its inverse if needed for the chosen sign convention, whose matrix sends b_i↦b_i+a_i and fixes every other basis vector. It is already an explicitly specified curve map.

For every pair i≠j, choose σ_ij to send 1↦i, 2↦j and to match the remaining labels in increasing order. Define

D(i,j)=P_σij h P_σij^{-1}.

Then τ(D(i,j))=[a_i b_i b_j]. For an ambient map f and z∈HI_g, put

Δ_f(z)=f z f^{-1} z^{-1}.

Equivariance and additivity give τ(Δ_f(z))=(Λ³ρ(f)−I)τ(z). All words built this way remain in HI_g.

## 3. Explicit word lifts of every monomial in W

The following formulas are expressions in concrete maps from Sections 1–2. The displayed identities of formal exterior vectors hold in Λ³H; applying the quotient map and closed Johnson equivariance gives the asserted Johnson values in J. No compatible disk-fixed lifts of the selected closed words are required.

### One meridian factor

For j≠k define Z(i;j,k) by

- D(j,k), if i=j;
- D(k,j)^{-1}, if i=k;
- Δ_Lij(D(j,k)), if i,j,k are all different.

In every case,

τ(Z(i;j,k))=[a_i b_j b_k].

In the third case L_ij fixes b_j,b_k and sends a_j to a_j+a_i, so the difference is exactly a_i b_j b_k. In the second case the inverse supplies the sign needed to reorder b_k b_j.

### Two meridian factors

For i<j define Y(i,j;k) by

- Δ_Mj(Z(i;j,k)), if k≠j;
- Δ_Mi(Z(j;i,j))^{-1}, if k=j.

Then τ(Y(i,j;k))=[a_i a_j b_k]. The second case is needed: it avoids attempting Z(i;j,j), which would have repeated exterior factors. Before inversion its difference is a_j a_i b_j, hence the stated sign.

### Three meridian factors

For i<j<k set

F(i,j,k)=Δ_Mk(Y(i,j;k)).

Then τ(F(i,j,k))=[a_i a_j a_k].

These formulas prove that every integral monomial of W occurs as the Johnson image of an explicitly described HI_g word. Conversely q∈W, and the parabolic ρ(H_g) preserves W. Omori's normal generating family and equivariance therefore give

τ(HI_g)=W/Q.

The inclusion Q⊂W follows from the presence of an a in every summand of x∧ω. This recovers the known quotient with integral coefficients. Holden's notation has b_i as meridians; exchanging his a/b roles gives precisely this W/Q. No rationalization or saturation assumption enters the proof.

## 4. A fixed integral basis and an exact coefficient algorithm

Order the 2g basis vectors as e_1,…,e_2g=(a_1,…,a_g,b_1,…,b_g). Order wedge monomials by their increasing index triples. For i∈{1,…,g}, put ν(i)=i+1 if i<g and ν(g)=1.

For x=a_i or x=b_i, let

R_x=x∧ω,
p_x=the increasing-order monomial underlying x∧a_ν(i)∧b_ν(i),
ε_x=the coefficient of p_x in R_x, which is +1 or −1.

The supports of the 2g vectors R_x are disjoint. Indeed, any monomial appearing in one of them contains one complete handle pair a_j,b_j and a third basis vector x from a different handle. A three-element monomial cannot contain two complete handle pairs, so it determines x uniquely. In particular all p_x are distinct, and p_x occurs in no R_y with y≠x.

Let B=(v_1,…,v_r) be the ordered list of all W basis monomials except these 2g pivots. Then ([v_1],…,[v_r]) is an integral basis of W/Q. Explicitly, for v∈W set

red(v)=v−Σ_x (v[p_x]/ε_x)R_x.

Every coefficient v[p_x]/ε_x is an integer, and the resulting vector has all pivot coordinates zero. Its remaining coordinates are the unique coordinates of [v] in B. The supports argument proves both spanning and independence. It also proves that Q is primitive, rather than assuming that a rational basis suffices.

The rank is

r=binom(2g,3)−binom(g,3)−2g.

For each surviving monomial v_l choose the corresponding explicit lift p_l from Section 3: F for an aaa monomial, Y for an aab monomial, and Z for an abb monomial. Thus τ(p_l)=[v_l]. This selects a concrete word for every basis lift; no hidden existential lifting remains.

For n=(n_1,…,n_r)∈Z^r define the ordered section word

t_n=p_1^{n_1}⋯p_r^{n_r}.

It satisfies τ(t_n)=n in these coordinates and t_0=1. It need not be a homomorphism, and no commutativity of the p_l is asserted.

## 5. The ordinary generating family

For every finite word w over X^± and ε∈{−1,+1}, define

s(w,ε)=w h^ε w^{-1},
c(w,ε)=coordinates in B of red(ε · ((ρ(w)a_1) ∧ (ρ(w)b_1) ∧ (ρ(w)b_2))).

Define the family

G(n,w,ε)=t_n s(w,ε) t_{n+c(w,ε)}^{-1},

with unrestricted indices n∈Z^r, w∈(X^±)*, ε∈{−1,+1}.

This formula is the deliverable. Its curves, finite ambient alphabet, integer indexing, coefficient reduction, and section words have all been specified above.

### Membership

Each factor lies in H_g, so G extends over V_g. Each t_n and s(w,ε) lies in HI_g. Additivity gives

τ(G(n,w,ε))=n+c(w,ε)−(n+c(w,ε))=0.

The closed Johnson kernel theorem now gives G(n,w,ε)∈HK_g.

### Generation

Let f∈HK_g. Omori's ordinary ambient-conjugate family gives a finite expression f=s_1⋯s_m, with s_j=s(w_j,ε_j). Write c_j=c(w_j,ε_j), n_0=0 and n_j=c_1+⋯+c_j. Since τ(f)=0, n_m=0. Then exact group cancellation gives

f=Π_(j=1)^m [t_{n_(j−1)} s_j t_{n_j}^{−1}].

Every bracketed factor is G(n_(j−1),w_j,ε_j). This proves equality of the ordinarily generated subgroup with HK_g, not merely inclusion or generation of its quotient.

A normalized representative t_n need not be a prefix-closed Schreier transversal. The displayed telescoping identity is the entire proof, so no hidden transversal hypothesis is needed.

## 6. Optional equivalent normal-family description

Inside HI_g, one may instead take the normal closure of

s(w,ε)t_{c(w,ε)}^{-1}

for all w,ε, together with all [p_i,p_j] for 1≤i<j≤r. These words lie in the kernel. In the quotient by their normal closure the p_i commute, and every s(w,ε) equals the specified p-word. Hence that quotient is generated by commuting p_i. Their images under τ are an integral basis, so there are no additional relations, and the quotient is exactly Z^r. This proves the same kernel equality.

This is **infinite normal generation in HI_g**, with a finite additional commutator list. It is not a claim of finite normal generation in HI_g or H_g. The family in Section 5 is an ordinary generating family and requires no normal-closure interpretation.

## 7. Closed/bordered and scope safeguards

Capping the fixed boundary disk is surjective from the disk-fixed handlebody group to the closed handlebody group. One can isotope a handlebody representative near its boundary to fix the selected disk; equivalently use the usual disk/point-forgetting comparison. Capping induces an isomorphism on first homology, so the preimage of closed HI_g is exactly the disk-fixed HI group. Thus Omori's normal-closure theorem descends to the stated closed theorem. Hensel §3 and Holden §6.2 provide independent literature comparison for this transfer.

For the Johnson map the targets are different: the bordered target is Λ³H, and the closed target is Λ³H/(H∧ω). All membership and generation assertions here use the latter. We do **not** assume that the bordered Johnson kernel surjects onto the closed kernel. In fact that assumption is precisely what the quotient calculation avoids.

The theorem covers the Johnson-kernel branch for g≥3. It makes no genus-two conclusion, no separating-meridian generation assertion, no statement that HK_g has trivial Out(F_g)-action, and no claim about a finite ordinary or finite normal generating set. The construction is compatible with, but does not by itself settle, any stronger geometric-generator problem.

## 8. Verification and source ledger

The authored script verify_lattice.py checks every lift identity, the disjoint pivot supports, exact reduction, integral rank, and preservation of W and Q under elementary parabolic matrices for g=3,…,8 using exact Python integers. VERIFICATION.json records all passes. These finite checks support formula transcription; the uniform proofs above establish the arbitrary-genus claims. They do not independently prove Omori, Wajnryb, or Johnson's topological theorems.

Public source links:

1. Genki Omori, *A small normal generating set for the handlebody subgroup of the Torelli group*, arXiv:1607.06553v1, Theorem 1.2 and Figure 1; Lemma 3.1 and §3.1 for homology image and elementary lift. https://arxiv.org/pdf/1607.06553v1
2. Bronisław Wajnryb, *Mapping class group of a handlebody*, Fundamenta Mathematicae 158 (1998), 195–228, Definitions 2–3, Figures 1,9–10, and Theorem 19 (printed p.213). https://matwbn.icm.edu.pl/ksiazki/fm/fm158/fm15831.pdf ; https://doi.org/10.4064/fm-158-3-195-228
3. Andrew Putman, *The Johnson homomorphism and its kernel*, arXiv:0904.0467v4, §1/Theorem A for the closed kernel and §2.4 for the bounding-pair formula and target comparison. https://arxiv.org/pdf/0904.0467v4
4. Annie Holden, *Abelianizations of finite-index subgroups of the handlebody group*, arXiv:2607.07587v1, §6.2 for the closed Omori statement and Proposition 7.3 for the integral image quotient, attributed there to Morita. Her meridian convention is opposite to ours. https://arxiv.org/pdf/2607.07587v1
5. Sebastian Hensel, *A primer on handlebody groups*, §3 for the disk/point-forgetting comparison and Theorem 7.1 for the parabolic homology image. https://www.math.lmu.de/~hensel/papers/hno4.pdf

No claim is made that these searches exhaust prior constructions. In particular the general kernel method is classical, and the image quotient has an identified prior attribution. Only authored exposition and public verification metadata are included here; copied source documents are excluded.
