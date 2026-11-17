# Source-only independent scope derivations

Record23204810,row193. Written before opening supporting archives, OpenAI/HWW/Watanabe primary bodies, current peer findings or root mathematical findings. The actual native main TeX, five-page PDF and metadata are the sole paper inputs. This is an INITIAL conditional assessment, not acceptance of the external EGH claim or a final paper verdict.

## Exact target and sole nonstandard mathematical import

Let k be any characteristic-zero field, n≥0, and let A=k[x1,…,xn]/(f1,…,fn) with a proper homogeneous regular sequence of length n, all degrees di≥1, and each variable of degree one. The target is

    max_{all ideals I⊲A} dim_k(I/mI) = max_j dim_k A_j
      = max_j [t^j] product_i(1+t+…+t^(di−1)).

All ideals means zero, the unit ideal, and every nonhomogeneous ideal. If p is the last maximum degree, m^p is the stated witness, with m^0=A. There is no restriction that k be countable, algebraically closed or embeddable as a whole in C. There is no general nonstandard grading, nongraded complete-intersection or positive-characteristic claim.

The exact imported EGH assertion needed is only this: over C, for every full homogeneous regular sequence gi of degrees ai≥2 in q variables, every homogeneous Q containing that sequence has a homogeneous ideal Q' containing the corresponding variable pure powers and the same quotient Hilbert function in every degree. Sorted degrees may be used after permuting the regular sequence. No equality of minimal generator numbers, Betti comparison, Lefschetz assertion, or partial-length regular-sequence theorem is needed. The native attributions to OpenAI and HWW have not been authenticated from their actual primary bodies at this gate.

My scope mechanism is a sequence of functorial dimension comparisons, scalar extension/descent and finite Frobenius duality. It is not numerical reproduction or reliance on the supplement's historical audit conclusions. No peer approach has been inspected, so material distinction from the adversarial family is an intended mechanism choice, not a claim about that family's unseen work.

## Field scope proved as an interface reduction

Fix the one homogeneous Q under consideration. Polynomial-ring Noetherianity gives finitely many generators; all their coefficients and those of the gi generate a field k0 finitely generated over Q. Include gi among the selected generators so Q0 contains the displayed sequence over k0. The field extension k/k0 is faithfully flat. At each step of the regular sequence, a multiplication kernel over k0 tensors to the zero kernel over k, hence is zero. Thus regularity genuinely descends, not merely the Hilbert function.

A finitely generated characteristic-zero field embeds into C: choose a finite transcendence basis, map it to algebraically independent complex numbers, then extend the embedding of the finite algebraic field extension into the algebraically closed C. This does not embed an arbitrary large k into C. Apply the assumed complex EGH assertion to Q0 after that base change.

Even if the complex theorem only supplies a homogeneous Q' and does not explicitly promise it monomial, a graded term-order initial ideal of Q' preserves its Hilbert function and still contains each pure power. Its monomial exponents define the same monomial ideal over k0 and k. The numbers of standard monomials in each degree are independent of the coefficient field. Field-extension flatness separately preserves the Hilbert function of the original quotient from k0 to both C and k. This proves exactly the required Hilbert-counterpart statement over arbitrary k, conditional on the complex input, without coefficient descent of Q' or of arbitrary complex ideals.

An alternative sufficient scope route is to prove the all-ideal generator bound after one field extension and descend each base ideal: A_K has nilpotent maximal ideal m_K=mA_K and residue field K; (IA_K)/(m_K IA_K)≅(I/mI)⊗K. Thus mu is unchanged for each extended base ideal. This does not assert every ideal of A_K descends. The witness m^p is already defined over k.

## Linear generators and degenerate boundaries

Let r be the number of linear members. If they had rank smaller than r, the total ideal would have fewer than n generators and could not have height n. A graded coordinate change therefore makes them independent coordinate variables. Quotienting by these variables leaves q=n−r homogeneous images of the remaining forms, in q variables, with Artinian quotient. None of those q images can be zero: otherwise the remaining ideal would have height at most q−1. A nonzero homogeneous image retains the original degree, which is at least two. They form a homogeneous system of parameters in a polynomial ring; Cohen–Macaulayness supplies regularity. Sorting degrees is a permutation of a homogeneous system of parameters, so does not change the quotient or lose regularity.

For n=0, A=k and the only ideals are0,k. Their minimal generator numbers are0,1, so the maximum is1, the empty product is1, and the last maximum degree is0. For all di=1 the same conclusion follows after eliminating all variables. No EGH statement in zero variables or with degree-one inputs is needed. For one remaining variable of degree d≥2 the Hilbert list is all ones through degree d−1; p=d−1 and every ideal of k[z]/(z^d) is principal. This checks the last-maximum and long-plateau boundary rather than silently taking the first peak.

## Matching has only a Hilbert-function demand

Let B=k[z1,…,zq]/(z1^a1,…,zq^aq). Its monomial basis is a product of finite chains, ranked by total degree. I checked the native rectangle construction directly: for 0≤i≤a,0≤j≤b,a≤b, chain r starts at(r,0), moves vertically to(r,b−r), then horizontally to(a,b−r), for0≤r≤a. Each point belongs to precisely one chain: either it is on the vertical segment with r=i and j≤b−i, or it is on the horizontal segment with r=b−j<i. Endpoint ranks are r and a+b−r. The chains are saturated and symmetric.

Inducting on a product of chains, treat each existing symmetric chain times the new factor as such a rectangle, swapping its two axes if necessary. If the old chain begins at rank r and has length ell, the new endpoint sums are 2r+ell+b, the same total socle rank for every old chain. Therefore the full product has a symmetric saturated chain partition. At a rank j with h_j≤h_(j+1), no chain meeting j ends there: below the middle symmetry prevents an end; above the middle there are no new starts, so an end would force a strict drop. This includes equality plateaus above the middle. Empty ranks are vacuous.

For W⊂B_j, echelonize using a multiplicative monomial order on surviving monomials. If a variable multiple of a leading monomial survives the pure-power quotient, it remains the leading term of the corresponding product; killed multiples are simply not part of the upper shadow. The chain successors inject the distinct leading monomials into that shadow. Hence dim W≤dim B1W whenever h_j≤h_(j+1). No binomial coefficient, characteristic-zero division, or linear Lefschetz element enters this step.

For V⊂A_j, the ideal AV has degree-j part V and degree-(j+1) part A1V. An EGH Hilbert counterpart J in B satisfies dim J_j=dim V and dim J_(j+1)=dim A1V because A and B have the same Hilbert function. Its ideal property gives B1J_j⊂J_(j+1). Combining the preceding inequality yields dim V≤dim A1V on every nondecreasing Hilbert step. This transfer uses only two adjacent ideal dimensions; it never transfers generator counts through EGH.

## A checkable abstract graded Frobenius lemma

The downstream implication can be isolated from EGH: let A be a finite standard graded Frobenius algebra with symmetric unimodal Hilbert function, socle degree c and last maximum p, and suppose the matching inequality holds whenever j<p. Then every homogeneous ideal has at most h_p generators.

For a homogeneous ideal I with initial degree alpha<p, put I'=I_{≥alpha+1}. Standard grading implies (mI)_j=A1 I_(j−1). In the sum of dimensions of I_j/(mI)_j, truncation deletes dim I_alpha at degree alpha and restores dim A1I_alpha at degree alpha+1; higher pieces do not change. Thus

    mu(I')−mu(I)=dim A1I_alpha−dim I_alpha≥0.

Iterate until I is replaced by I∩m^p. This includes I=A (initial degree0) and I=0 (already bounded).

For I⊂m^p, set J=Ann(mI). Let lambda be the socle functional. Perfect graded multiplication pairings imply the full pairing lambda(ab) on A is nondegenerate. For every ideal U, its orthogonal complement equals Ann(U): if a is orthogonal to U, then for every u∈U and b∈A one has lambda((au)b)=lambda(a(ub))=0, since ub∈U. Nondegeneracy forces au=0. Therefore dim Ann(U)=dim A−dim U. Also mJ⊂Ann(I), giving

    mu(J)≥dim Ann(mI)−dim Ann(I)=dim I−dim mI=mu(I).

Perfect graded pairings give Ann(m^u)=m^(c−u+1), including u=0 and c+1. Since mI⊂m^(p+1), one obtains J⊃m^(c−p)⊃m^p; the last inclusion uses c−p≤p. The annihilator reverses inclusions, and the direction is essential here. Applying the truncation inequality to J gives mu(J)≤mu(J∩m^p)=mu(m^p)=h_p. This closes the homogeneous implication without an unproved ideal-generator comparison.

For a complete intersection, the Hilbert series follows by repeated regular-sequence multiplication exact sequences. Its socle and perfect pairing statement are the usual Koszul/Frobenius complete-intersection input. Those standard algebraic facts are identified inputs; this INITIAL is not a complete independent construction of canonical modules. Product-of-chains symmetry and unimodality match that same Hilbert product.

## Nonhomogeneous ideals: direction and a strict-containment control

Filter I and mI by intersections with m^j. Since m^j=A_{≥j}, gr_m A≅A, and J=gr I is a homogeneous ideal. If a degree-one factor times an initial form survives, it is the initial form of the product in mI; if it is zero, there is no nonzero form to include. Thus mJ⊂gr(mI)⊂J. Finite filtrations preserve total dimensions, so

    mu(I)=dim J−dim gr(mI)≤dim J−dim mJ=mu(J).

Here is a hand control showing why equality of those subspaces must not be assumed. In A=k[x,y]/(x^3,y^5), let I=(x^2+y^3). Multiplying its generator gives a basis

    x²+y³, x²y+y⁴, x²y², xy³, xy⁴, x²y³, x²y⁴.

Its initial ideal is J=(x²,xy³), of dimension7. The monomial xy³=x*(x²+y³) belongs to mI and hence to gr(mI), but does not belong to mJ. In fact dim gr(mI)=6 whereas dim mJ=5; mu(I)=1 and mu(J)=2. This confirms the required inequality direction and the possibility of strictness, using an actual nonhomogeneous ideal in a characteristic-zero Artinian complete intersection. It does not test or prove general EGH.

## Boundary controls and noninferences

For degrees(1,2,4), eliminating the linear member gives Hilbert product(1+t)(1+t+t²+t³)=1+2t+2t²+2t³+t⁴. The last peak is p=3, not1; m³/m⁴ has dimension2. The annihilator exponent is c−p=1, with m¹⊃m³. This explicitly checks the long plateau and inclusion direction. Eight quadrics have the binomial row with middle coefficient C(8,4)=70; such coefficient arithmetic is not evidence for EGH.

The monomial matching proof works in every characteristic. As a logical stress control, over F2 the monomial complete intersection in three square-zero variables still has the matching/Sperner mechanism, but every linear form ell satisfies ell²=0. Multiplication A1→A2 by a nonzero ell has ell in its kernel, so cannot be a rank-three isomorphism. This shows the mechanism does not secretly use a Lefschetz operator. It is not a counterexample to a characteristic-zero assertion or a positive-characteristic extension of the general EGH import.

## Remaining interfaces before any final scientific disposition

The strongest source-only result is a hand-checked conditional implication from the exact complex full-length EGH Hilbert-counterpart assertion, together with the stated standard complete-intersection/Frobenius facts, to the full target including all ideals and arbitrary characteristic-zero fields. The external EGH theorem remains an assumption until its actual primary is inspected. The native claimed HWW/Watanabe attribution, theorem scopes, OpenAI theorem numbering/commit/body, release-date claims and companion Betti assertions likewise remain unverified primary interfaces. No first-priority, new EGH, new Lefschetz or publication conclusion is drawn.

This conditional closure is not a final target PASS. If the actual upstream body lacks the required all-Q/full-degree Hilbert statement, or relies on a central unsupported inference, the route is blocked at that exact input; the monomial, descent and annihilator arguments cannot substitute for it. Finite examples or an archived successful audit would not close that gap. No upstream body, archived audit opinion, supporting scientific program or current peer mechanism was opened in this INITIAL.
