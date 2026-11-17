# Own source-first hand derivations and controls

All calculations below were derived from the original manuscript definitions before support/native verifier/results/audits/current peers/foreign proofs were opened. This is mathematical working evidence, not a final acceptance. No mathematical program has run in this lane.

## 1. Pairing-independent matrix and actual word sums

Write A=1/(q+1)^2 and B=p^2. Classes have sizes (7,7,v-7). For a row t in E, bar(t) is an S letter: seven E successors have B; six S and v-7 O successors have A. For t in S, bar(t) is extra: six remaining extra successors have squared weight1/4, while all ordinary successors have B. For t in O, bar(t) is O: seven E successors have B, seven S have A and v-8 O have A. Thus M L = L Q for the class-lift L, with rows
(7B,6A,(v-7)A), (3/2,7B,(v-7)B), (7B,7A,(v-8)A).
This proof uses only the allowed pairing structure, so its vector inequalities hold for every pairing, not just a sampled inverse involution. For h>=1, summing the products of squared turn weights gives exactly 1^T M^(h-1)1. Inverse-containing words contribute0. At h1 the mass is |T|, not1; normalizing it as a probability would be an error.

For the lifted f=(1,13/5,1), Qf/f at q32 is independently obtained from v1057, A1/1089, B1089/1117249:
E: 7623/1117249+5328/5445 =95146189/96562235;
S: (3/2+5341*1089/(5*1117249))*5/13 =579417/592826;
O: 7623/1117249+5336/5445 =857592557/869060115.
The exact positive integers 987*d-1000*n for these three n/d ratios are respectively
160736945, 5702262, 169776505.
Therefore M f <=(987/1000)f, f>=1 and sum(f)=7+7*13/5+1050=5376/5. Iteration gives the claimed all-h bound. The weighted infinity norm gives rho(M)<=987/1000<1, without depending on rounded eigenvalues. At h1:1064<=5376/5; the slack is56/5.

For x=(193/500,1,194/500), derive before substituting q:
R_E=7B+A*(194v+1642)/193;
R_S=579/1000+B*(194v+2142)/500;
R_O=(1351/194)B+A*(194v+1948)/194.
Substitution at4,8,16 gives the following exact ratios and hand-cleared positive margins 500*n-503*d:

q4:
480733/303975, margin87467075;
26959/21000, margin2916500;
500011/305550, margin96313850.

q8:
10342603/9256473, margin515295581;
5726739/5329000, margin182882500;
10523789/9304434, margin581764198.

q16:
35146373/34932807, margin1984579;
3571543/3549000, margin624500;
2078707/2065518, margin397946.

For checkable substitution details: at4, R_E=25/63+5716/4825 and R_S=579/1000+74/105. At8 the E unreduced numerator/denominator are93083427/83308257 (divide9); S has numerator5726739 over5329000; O has94714101/83739906 (divide9). At16 E is4182418387/4157004033 (divide119); S150004806/149058000 (divide42); O4205224261/4178542914 (divide2023). These reproduce the table without reading the supplied verifier.

Since 0<x<=1 and Mx>=(503/500)x, nonnegative iteration gives mass >=(503/500)^(h-1)sum(x), and a weighted lower bound on spectral radius gives rho(M)>=503/500>1. C_q=(194v+3493)/500, namely7567/500,17655/500,56455/500 at4,8,16. No smaller dyadic order in the stated domain remains. This does not exclude other models or actual group examples at those orders. At q2, 3m-1 divisible4 requires m=3 mod4, whereas3(m-1) divisible4 requires m=1 mod4; the unchanged type prescription is infeasible and is explicitly out of domain.

## 2. Construction parameters: actual necessary controls, not a substitute for source proofs

At32, v=32^2+32+1=1057 and |T|=1064, so a fixed-point-free inverse pairing gives532 rose edges. v-7=1050 is even. For m=1 mod4, (33m-1)/4 and33(m-1)/4 are integers. In either vertex set, an ordinary point appears33 times per line-class multiplicity. Each extra belongs to four Fano complements, so its A total is1+4*(33m-1)/4=33m, and its B total is4*33(m-1)/4=33(m-1). These match its ordinary inverse-mate counts WITHIN the respective set. They would not match across A versus B; actual upstream matching definitions must be checked accordingly.

Seven Fano complements contain four points apiece. Each point lies in four; each pair lies in two (seven lines minus the five through at least one member). Distinct complements meet in2, identical ones in4, and the all-seven set meets a complement in4. Projective ordinary lines meet in1 unless equal, when they have33 points. Thus all those ordinary intersections are odd, and extra intersections are even except the distinguished all-seven self-intersection. Degrees are33,37,40. Handshaking gives an odd size for the A component containing the sole even-degree root and an even size for each all-odd-degree B component. This makes the necessary augmentation values a=b=1,c=0 over F2 consistent with ab=1,ac=0; identity coefficient1 for c is not an augmentation contradiction. It is still the protected-root/probabilistic proof that must show the actual ring identities and nonzero c.

The assignment density7*33/(4*1057)=33/604<1. Distributing each extra-type count among1057 line classes with floor/ceiling discrepancy leaves at most7 rounding slots per line, so sufficiently large m leaves disjoint capacity after reserving the root. This verifies the elementary capacity interface, not the random graph theorem.

For c0=1/100:2|T|/p=2249296/33<2^17, hence c0 log(2|T|/p)<17/100 using log2<1. Also40<2^6 gives2c0 log40<12/100. Thus r_n=O(log n+n^(2c0 log40))=o(n). The minimum positive turn weight is1/33, while p=33/1057 is a slot density; these roles must not be conflated in the upstream transfer. Both are fixed positive constants.

If the claimed source prescription bound yields (C3(k/n)^(29/2))^k, a fixed eta with C3*eta^(29/2)<1/2 makes the split sum elementary: k<=sqrt(n) has base <=C3*n^(-29/4)=a_n->0, so sum<=a_n/(1-a_n); k>sqrt(n) has sum<=2^(1-sqrt(n)). The exponent29/2 equals33/2-2. Also ceil(33k/2)<=17k for k>=1. For eta10^-6, 17eta<p/4 follows71876<33000000, but the asserted numerical C3 certificate remains unopened. Existence of some eta for finite C3 is not a numerical matching witness. Conditioned switching/path/correlation/sphere estimates and the exact order of choosing unpaired fraction versus other fixed bounds remain critical unverified primary interfaces at this seal.

## 3. HNN and finite classifying-space checks

In B=G*F(x,y), the conjugates x^-i y x^i (including i0) are free basis elements in the exponent-x kernel. The proposed v_i project under killing G to y^-i x y^i, another independent free basis subset. Thus no relation among v_i can survive its free image; both HNN associated subgroups are free on the specified bases. Conditional on the usual normal-form embedding theorem, G embeds. Relation0 gives y=t x t^-1. Solving relation i gives
 g_i=x^-1 y^i t^-1 x^-i y x^i t y^-i.
Substitute y^i=t x^i t^-1 to obtain
 W_i=x^-1 t x^i t^-2 x^-i t x t^-1 x^i t^2 x^-i t^-1,
including adjacent t^-1*t^-1 and t*t that produce the printed squares. This is an actual word derivation, not a finite-group test.

The graph-of-spaces has vertex X wedge a2-rose, edge an(s+1)-rose, and cylinders of dimension2. Its Euler characteristic is (chi(G)-2)-(-s)=(1-s+r-2)+s=r-1, matching a two-generator r-relator presentation. A tree of contractible vertex/edge covers with mapping-cylinder cofibrations is contractible by finite-tree homotopy pushouts; compact sphere images reduce to finite subcomplexes. To justify the stated presentation, collapse g_i/cell pairs only in the subcomplex of defining HNN cells, then y/cell0; carry the original relator attachments along the retraction. Arbitrary Tietze moves would not prove asphericity. These are the precise classical interfaces to authenticate after the checkpoint, not an upstream proof-body reading. Torsion in an HNN extension is conjugate into the base by cyclically reduced normal forms; free products of torsion-free groups are torsion-free by the same word-length control.

## 4. Ring handedness and boundary controls

From ab1, f=ba satisfies f^2=f, hence e=1-f satisfies e^2=e in every characteristic. ec=c-bac=c!=0 proves e!=0. If e1, ba0 gives a=a(ba)=0, contradicting ab1 in a nonzero ring. Compute ae=a-aba=0 and eb=b-bab=0; the opposite-handed identities are not assumed. For p in eR, ep=p. The explicit RIGHT-linear maps Phi(r)=(ar,er), Psi(u,p)=bu+p compose to r and(u,p), respectively. eR is a cyclic direct summand, nonzero because e in it. K0 group completion cancels classes, so [P]0 despite P!=0; projective cancellation fails, not group completion. Augmentation splits K0(field)=Z back off the group algebra, so this cannot imply K0(group algebra)0.

A concrete handedness control is End_F2(V) on a countable basis: b shifts right, a shifts left with a(v0)=0, and c projects to span(v0). Then ab=I, ac=0, c!=0 and1-ba=c. This is an infinite-dimensional RING control, not a group-algebra or matching example. No finite-dimensional square-matrix representation can realize all three relations, since abI makes a invertible and forces c0. This checks why the existential target is not certified by a small matrix computation.

For a group embedding G->H, distinct basis elements remain distinct in K[H], so the induced scalar group-ring map is injective. For char(K)=2, the unital F2->K map similarly preserves coefficient support, e and e-1 nonzero. No such map goes to odd/zero characteristic. At most one torsion-free group generator yields the trivial or infinite cyclic group, whose field algebra is a domain, so no proper scalar idempotent exists there. None of these elementary consequences verifies the central random-cone existence/adaptation on its own.
