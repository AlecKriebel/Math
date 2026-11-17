# Actual source-first hand derivations and adversarial controls — row177

2026-11-17 UTC. Completed after the actual native448-line/seven-page manuscript reading and before any support/code/results/archived opinion/new foreign mathematical body/current peer finding. The manuscript supplies its proof and audit assertions; those exposures are disclosed. The calculations below are a checkable independent reconstruction and falsification family. Main existence/adaptation interfaces remain explicitly open pending actual primary proof reading after the source-first seal/checkpoint.

## 1. Inverse classes and the exact transfer quotient

For q=2^k≥4, v=q²+q+1 is odd, so v−7 is even and the stated fixed-point-free inverse pairing is possible. Let E be the seven extras, S their seven distinct ordinary mates, O the other v−7 ordinary letters. Inversion exchanges E and S and preserves O. Put a=1/(q+1), p=(q+1)/v. M_(t,u)=w(t,u)², zero for u=bar(t).

For t∈E, bar(t) is ordinary: seven E successors have p², six S successors a² and v−7 O successors a². For t∈S, bar(t) is extra: six E successors have1/4, all seven S successors p² and all O successors p². For t∈O, bar(t)∈O: seven E successors p², seven S successors a² and v−8 O successors a². These counts yield exactly

    Q = [[7p², 6a², (v−7)a²],
         [3/2, 7p², (v−7)p²],
         [7p², 7a², (v−8)a²]].

All entries are strictly positive for q≥4, and the quotient does not depend on which ordinary labels were chosen as mates or how O was paired. A positive Perron vector z of Q lifts to a strictly positive vector f on all actual letters with Mf=rho(Q)f. The weighted sup norm ||y||_f=max|y_i|/f_i gives ||M||_f≤rho(Q), while that value is an actual eigenvalue. Thus rho(M)=rho(Q), without an assumed symmetry, uniform row sum or accidental extra quotient eigenvalue. Even without invoking Perron for the full matrix, every explicit super/subvector lifts and supplies the stated power bounds directly.

There is no probability normalization of w: a row of class S has a contribution6/4=3/2 to the squared row sum before any other successors. Its maximum row sum therefore exceeds1 even at32; this does not refute spectral contraction of the non-symmetric matrix. Dividing rows to create probabilities would change the problem. Forbidden immediate inverses contribute zero to the sum over all T^h, so the identity sum P(W)²=1^T M^(h−1)1 holds, including h=1 with the empty product1. h=0 is outside the assertion.

## 2. Exact upper certificate, margins and h=1

At32, v=1057, |T|=1064, p=33/1057, a²=1/1089 and p²=1089/1117249. For f=(1,13/5,1) on E,S,O, direct row arithmetic is

    (Qf)_E = 7623/1117249 + 5328/(5*1089),
    (Qf)_S /(13/5) = [3/2 + (91/5+1050)*1089/1117249]/(13/5),
    (Qf)_O = 7623/1117249 + 5336/(5*1089).

These reduce to the displayed95146189/96562235,579417/592826,857592557/869060115. Strict comparison with987/1000 is independently checkable through positive integer numerators987D−1000N:

| Class | Positive cross-product numerator |
| --- | ---: |
| E | 160736945 |
| S | 5702262 |
| O | 169776505 |

Thus Mf≤lambda f with lambda987/1000<1. Since1≤f entrywise, M^n1≤M^nf≤lambda^n f. Summing gives the universal stated upper bound for every h≥1. The exact sum f_i is7+7*13/5+1050=5376/5; at h=1, actual mass1064=5320/5 is indeed below that constant, with gap56/5. This catches a missing class multiplicity or an invalid h−1 shift. The narrow O margin is positive, not a floating rounding decision.

For delta=−(1/4)log lambda, the bound C lambda^(h−1) is eventually at most exp(−2delta h): the ratio is C lambda^(h/2−1), which tends0. If the actual upstream statement uses another fixed factor in its decay exponent, choose the needed fixed fraction only after reading its exact interface; do not silently identify unlike normalizations.

## 3. Exact lower certificate and domain boundaries

For x=(193/500,1,97/250), all components are positive and at most1. Direct quotient substitution yields the manuscript's nine exact N/D ratios. Their strict lower comparison with503/500 is independently checked by500N−503D:

| q | E | S | O |
| --- | ---: | ---: | ---: |
| 4 | 87467075 | 2916500 | 96313850 |
| 8 | 515295581 | 182882500 | 581764198 |
| 16 | 1984579 | 624500 | 397946 |

All are positive, including all close order16 margins. Hence Mx≥mu x with mu503/500>1, and M^n1≥M^nx≥mu^n x. The lower prefactor is

    C_q = [194v+3493]/500,
    C_4=7567/500, C_8=3531/100, C_16=11291/100.

At h=1 each is below the corresponding alphabet size28,80,280, as x≤1 requires. The growth bound forces rho(M)≥mu>1, by the finite-dimensional spectral-radius formula or weighted subeigenvector bound. Together with the upper32 bound it proves **least dyadic order**, since4,8,16 are exactly the earlier dyadic possibilities in the stated domain. It does not prove a uniform gap below1 or monotonic behavior for every larger q, and neither is needed for “least”.

As q→infinity, the quotient tends to [[0,0,1],[3/2,0,1],[0,0,1]], whose spectral radius is1. In particular a fixed contraction constant987/1000 cannot simply be advertised for every large q from this certificate. The actual theorem only supplies it at32. Non-dyadic orders and changed type weights are outside this threshold statement. Lower failure of squared-word decay is not a proof that no good matching or idempotent can exist there by another mechanism.

At q=2, the unchanged extra counts would require3m−1 and3(m−1) both divisible by4. Their difference is2, so this is impossible; equivalently m would have to be both3 and1 modulo4. The quotient also has an empty O class there, so extending the three-positive-class argument to2 would be illegitimate. At q≥4 the alphabet pairing and class positivity have no such degeneracy.

## 4. Slot totals, parity and integer/capacity controls

At32, every point of PG(2,32) is on33 lines, every line has33 points, and two different lines meet once; equal lines have33-point intersection. All these intersection sizes are odd. Take m≡1 mod4, m large, m vertices per ordinary line class in A and m−1 in B. Put A_c=(33m−1)/4 and B_c=33(m−1)/4 for each of the seven four-element Fano-line complements. Both are integers and A_c−B_c=8.

The seven-point Fano plane has seven lines of size3. Each point is outside exactly four lines and each pair is outside exactly two. Therefore every extra occurs4A_c+1=33m times on A (including the distinguished all-seven vertex), and4B_c=33(m−1) times on B. Each ordinary letter likewise occurs33m and33(m−1) times because it lies on33 ordinary lines. Consequently all inverse labels have exactly equal slot populations within each side for every permitted pairing. This is an actual exact-balance calculation, not an appeal to approximate frequencies.

Every non-distinguished vertex has33 or37 outgoing letters, both odd; the distinguished A vertex has40, even. Intersections of two four-element Fano complements have size4 if equal and2 if different; empty sets and the seven-set have the corresponding even intersections except the distinguished self-intersection7. Ordinary/extra labels are disjoint. Thus any two outgoing sets have odd intersection, except the distinguished A self-pair which has40 and is even. On the B side every vertex degree is odd; every connected component therefore has even vertex count by the handshake lemma. The A component containing its unique even-degree distinguished vertex has odd vertex count. Hence the necessary augmentation constraints epsilon(a)=epsilon(b)=1, epsilon(c)=0 agree with ab=1, ac=0 and a protected identity coefficient1 in c.

More generally, once the graph-cone relations identify each edge x--t-->y with w_x t=w_y in the quotient group, the value w_x w_y^−1 is constant on a synchronized product-graph component. In A'×A', product vertex degrees have the odd/even pattern just computed: every product vertex odd except(x_A,x_A). Handshake makes every component even-sized except the one containing that exceptional pair, which has odd size and value1. Therefore the summed scalar product ab is1 over F2, even if different product components map to the same group element. In A'×B', all product vertices are odd, so every component has even size and ac=0. This reconstructs the characteristic-two parity-to-scalar mechanism without assuming an injective correspondence between all product components and group elements. Nonzero c still needs the genuine root-protection input; parity alone cannot prevent cancellation at its identity coefficient.

The total extra-assignment leading capacity fraction per ordinary line class is7*33/(4*1057)=33/604<1. A bounded rounding overhead per class can be absorbed for large m if “evenly” means counts differing by at most a bounded amount, as is usual in such a finite-type asymptotic construction. But **literal equal counts in every line class on both sides are impossible**: both1057|A_c and1057|B_c would imply1057|8. This is a precise wording/interface check to retain, not an implemented repair. The actual upstream assignment hypotheses and its permitted rounding errors must be read after INITIAL before accepting the complete adaptation. Exact global slot totals above do not themselves settle every local conditioning/frequency hypothesis.

## 5. Displayed probabilistic exponents and unresolved proof interfaces

The declared fixed constants satisfy the elementary inequalities without decimals. At32,

    2|T|/p = 2249296/33 < 2^17,
    log2<1, so (1/100)log(2|T|/p)<17/100<1;
    40<2^6, so (2/100)log40<12/100<1.

Thus the displayed exponent beta=2c0 log40 is strictly below1 and logn+n^beta=o(n). This verifies the numerical replacements if the actual switching proof requires just these quantities; it does not certify that those are all of its hypotheses.

For k≥1, ceil(33k/2) lies between16.5k and17k. A union bound with two-set choices of order(n/k)^(2k) and r prescribed edges carrying a bound of order(Ck/n)^r has the claimed minimal exponent r/k−2≥29/2. This reconstructs the origin of that exponent but leaves the actual conditional edge-prescription theorem to be checked at its source.

Assuming a fixed finite C3 independent of n,k in the stated range, take eta small with17eta<p/4 and C3 eta^(29/2)<1/2. For k≤sqrt(n), each summand is at most(C3 n^(−29/4))^k, so its sum tends0. For sqrt(n)<k≤eta n it is at most(1/2)^k, whose tail tends0. The concrete eta=10^−6 satisfies17eta<p/4 because17*4228=71876<33000000; the separate claimed conservative C3 certificate is not yet opened. Deleting at most two edges leaves minimum degree33−2=31≥3, so the advertised elementary short-closure inequality has margin. Total graph vertex count is2vm−v=2n−v with fixed v, not2n exactly; constants and asymptotics can absorb that fixed difference only if the actual source proof does so.

The strongest remaining issue is not the handful of rational inequalities. It is whether the actual pinned proof of conditioned matching existence, girth switching, edge prescriptions, path multiplicities, diameter, planar/spherical reduction and deterministic cone/root protection carries **all** needed constants and quantifiers to32. In particular: the conditioning event must be nonempty; finite-type local frequencies/rounding and arbitrary inverse pairing must fit the model; the unpaired fraction/fixed comparison/path bounds must be chosen in the correct order before n; first-moment estimates must not assume false independence between dependent stages; and root protection must imply c≠0 in the actual quotient. No native audit verdict or successful finite plane/checker can certify these universal probability/topology claims. These are open interface gates in this INITIAL, not a narrowed replacement theorem or an accepted equivalent unsupported assertion.

## 6. HNN word, embedding and finite2-dimensional classifying space

Condition on a finite aspherical presentation G=<g_1,...,g_s | R_1,...,R_r>. In B=G*F(x,y), the words u_0=y,u_i=x^−i y x^i are a finite free-basis subset of the kernel F(x,y)→Z sending x to1. Killing G sends v_0=x,v_i=y^−i x g_i y^i to a free-basis subset with x,y exchanged. Any reduced nontrivial word in the v_i has nontrivial free-group image, so they too freely generate. Thus mapping u_i to v_i is an isomorphism of free subgroups; the classical HNN embedding/Britton interface applies without requiring G to have a solved word problem or the g_i to be nonidentity.

From t^−1 y t=x, obtain y=t x t^−1. For i≥1, the relation t^−1 x^−i y x^i t=y^−i x g_i y^i gives

    g_i=x^−1 y^i t^−1 x^−i y x^i t y^−i
       =x^−1 t x^i t^−2 x^−i t x t^−1 x^i t² x^−i t^−1.

This is exactly the printed W_i. The i=0 defining relation eliminates y, not a nonexistent g_0; inserting i=0 into the formula would reduce to1 and must not be treated as an additional generator. H is generated by x,t. The preliminary presentation has s+3 generators and r+s+1 relators, hence deficiency2−r, consistent with two generators and r relators after the specific eliminations.

Topologically, vertex space X∨R2 is a finite K(B,1), and the edge rose of rank s+1 injects on both ends. Its mapping cylinder has dimension2. The Bass–Serre universal-cover tree of contractible vertex/edge spaces has contractible homotopy pushouts on finite subtrees; compact sphere maps land in finite subcomplex/subtree, so all homotopy groups vanish, and CW Whitehead gives contractibility. The standard finite-order HNN conjugacy theorem reduces torsion to the base free product; alternatively finite cohomological dimension already precludes finite cyclic subgroups. The exact classical interface will be read after INITIAL, not assumed from a blanket “all Tietze moves preserve asphericity” statement.

For the displayed presentation complex, first collapse the subcomplex consisting only of the HNN defining cells: each g_i appears once in its own such cell, then y once in the remaining zeroth cell. Retract that subcomplex to the x,t rose and transport the original R_j attaching maps by homotopy invariance. The resulting r cells attach by R_j(W). This justifies the specific homotopy equivalence despite g_i also appearing in the original R_j; it would be wrong to call it a free-face collapse of the entire original complex without this qualification. Euler control: chi(B)=chi(G)−2=−1−s+r, edge chi=−s, hence chi(H)=r−1=1−2+r, exactly the final presentation count.

An embedding G→H induces an injective group-algebra map over every field because distinct group elements remain basis elements. It transports scalar identities and nonzero coefficients, not a computed smaller support. A torsion-free group with at most one generator is trivial or Z; its group algebra is a field or Laurent polynomial domain and has no nontrivial scalar idempotent. Thus2 is a genuine lower boundary **if** the existential example is verified, while532 is only the explicit random-cone rose count:1064 signed letters/2 inverse pairs=532.

## 7. Ring, handedness and actual cancellation controls

In a nonzero unital ring with ab=1, ac=0 and c≠0, put f=ba,e=1−f. Then f²=b(ab)a=f; (1−f)²=1−2f+f²=e without any commutativity or characteristic assumption. Also ec=c−b(ac)=c≠0, so e≠0. If e=1 then ba=0 and a=a(ba)=0, contradicting ab=1. Complementarity gives R_R=fR direct-sum eR; the intersection is zero because an x=fr=es satisfies x=fx=fes=0.

Since b=bab, fR=baR=bR. **Left** multiplication by b is a right-module isomorphism R_R→bR with inverse left multiplication by a. The inverse maps on R_R and R_R⊕eR are

    Phi(r)=(ar,er),    Psi(u,p)=bu+p.

Here ae=0,eb=0,ep=p give PsiPhi(r)=(ba+e)r=r and PhiPsi(u,p)=(u,p). All maps are right-linear by associativity. Right multiplication by a,b instead would not generally be right-linear; this is a meaningful handedness check. The same identities show ker L_a=eR and c∈eR.

P=eR is nonzero (contains e), cyclic and a direct summand of R_R, hence finitely generated projective. Its absorption R≅R⊕P gives [P]=0 in the Grothendieck group of f.g projective right modules, but does not identify P with zero. R⊕0≅R⊕P while0 is not isomorphic to P is exactly projective cancellation failure.

Actual abstract control: on the vector space with basis u_0,u_1,..., let b be right shift and a left shift killing u_0; in R=End(V), ab=I, ba=I−pi_0, c=pi_0, ac=0 and e=pi_0 nonzero. The maps above work in every characteristic, and demonstrate why nonzero absorption/[P]=0 is algebraically consistent. This is an **infinite-dimensional endomorphism-ring** control, not a torsion-free group-ring witness. In every finite-dimensional square matrix algebra over a field, ab=I forces ba=I and ac=0 forces c=0. Thus a finite matrix test or a torsion-containing small example cannot certify the required scalar group-ring construction.

For characteristic-two K, the unique unital field inclusion F2→K and the group basis give an injection F2[H]→K[H]; e and e−1 remain nonzero and the same a,b,c identities persist. The quantifier is one same H/e over F2 working for every such K, not separately chosen H_K. There is no unital coefficient map F2→a characteristic-zero/odd-characteristic field. A group algebra's augmentation has epsilon(a)epsilon(b)=1, epsilon(c)=0 and epsilon(e)=0, consistent with the slot/parity controls above. The field inclusion/augmentation maps split off K0(K)=Z from K0(K[H]); vanishing of this one [P] does not make all K0 vanish. No self-adjointness, analytic projection or characteristic-zero/odd-characteristic conclusion follows.

## Source-only outcome and remaining gap

The local spectral theorem, printed ring identities and conditional explicit HNN mechanism have actual checkable source-first derivations and meaningful edge controls. The complete full-original existence claim still hinges on the actual pinned random-cone/probability/asphericity/root-protection argument and its32-parameter transfer. It is deliberately not certified by the source's old audits, metadata or a prospective finite run. Original results/code/foreign bodies remain unopened at this seal. After the requested checkpoint hold, inspect those precise primary and native interfaces; document a substantive unresolved gap and defer rather than silently retaining only the easy spectral/ring subclaims. No repair, narrower substitute or generic follow-up is proposed.
