# Independent audit: adjoint bound and line-arrangement reduction

Date: 2026-10-02. Independent AI mathematical audit of the submitted candidate.

## Verdict and scope

**PASS for the adjoint lemma over C and the resulting characteristic-zero line-configuration theorem**, subject to the precise arguments below. The naive assertion that every repeated factor gives a contradiction has the essential coplanar exception F=P^2; the subsequent derivative reduction handles it correctly.

**SOURCE-SCOPE BLOCKER:** Janssen's original preprint explicitly works over an algebraically closed field of arbitrary characteristic, and asks this same non-ACM question. The Oberwolfach summary does not explicitly narrow its section to characteristic zero. The present vanishing-based argument therefore must not be labeled a complete arbitrary-characteristic resolution. No positive-characteristic replacement for its vanishing step is verified here. An earlier field-convention assumption was corrected; the original target is retained as unresolved.

## Primary-source checks

1. Michael Janssen, *On the Fattening of Lines in P^3*, https://arxiv.org/pdf/1306.4387. Opening of section 1, PDF p1: algebraically closed field of arbitrary characteristic. Question 3.1, PDF p8, asks the non-ACM question. Lemma 2.4 establishes the coplanar ACM case; Proposition 2.6 establishes pseudostars are ACM. The Oberwolfach counterpart is printed p514, https://ems.press/content/serial-article-files/46557. The general reduced-curve question is separate and is not being claimed here.
2. Esnault–Viehweg, *Lectures on Vanishing Theorems*, Corollary 5.12(c), printed pp48–49: for a nef line bundle of positive top self-intersection in characteristic zero, the inverse bundle has no cohomology below dimension. https://page.mi.fu-berlin.de/esnault/books/esvibuch.pdf. Applied on a smooth surface, this gives H^1(O_X(-H))=0; Serre duality gives H^1(omega_X(H))=0.
3. Kollár, with appendix by Dao, *Duality and normalization, variations on a theme of Serre and Reid*, Definition 46 and equation (48.1): conductor is Hom(nu_*O_Y,O_S), and finite normalization duality gives nu_*omega_Y=Hom(nu_*O_Y,omega_S). https://arxiv.org/html/1811.00042v2. Here S is a hypersurface, hence Gorenstein, and its normal surface normalization is Cohen–Macaulay, so these are usual canonical/dualizing sheaves, not a substitute for a missing dualizing object.
4. For the canonical-sheaf inclusion, Brion's *Lectures on the geometry of flag varieties*, near Proposition 2.2.5, records the injective trace q_*omega_X -> omega_Y for normal Y: https://www-fourier.ujf-grenoble.fr/~mbrion/lecturesrev.pdf (search-extracted text; direct web PDF open failed). The argument below proves the required injection directly from reflexivity, without requiring this failed direct fetch. Ruppenthal–Samuelsson Kalm–Wulcan, https://arxiv.org/pdf/1211.3660, Theorem 1.2 and section 3.3 also discuss canonical inclusion for singular hypersurfaces, but Y need not be a hypersurface, so this theorem is not substituted for the general normal argument.

## 1. Adjoint lemma, with every map justified

Let S be an integral surface of degree e>=2 in P^3_C. Let nu:Y->S be its finite normalization and q:X->Y a projective resolution that is an isomorphism over the regular locus U of Y. Set f=nu q and H=f^*O_S(1). X is a smooth integral projective surface.

H is globally generated and nef. Its self-intersection is e, by projection formula and the birational degree of f. Thus H is big as well as nef. The stated vanishing theorem applies to give H^1(X,O_X(-H))=0 and, by Serre duality, H^1(X,omega_X(H))=0.

Choose a general divisor C from the pulled-back hyperplane system. This system is basepoint free, so characteristic-zero Bertini makes C smooth. It is connected: H^0(O_X)=C, H^0(O_X(-H))=0, and H^1(O_X(-H))=0 imply H^0(O_C)=C from the divisor sequence. The vanishing of H^0(-H) follows, for example, because an effective divisor linearly equivalent to -H would have negative intersection -e with the nef H. A smooth connected curve is integral. Its H-degree equals H.C=e. Write g for its genus.

Adjunction and the divisor sequence give

0 -> omega_X(H) -> omega_X(2H) -> omega_C(H|C) -> 0.

H^1(omega_X(H))=0 makes the restriction on H^0 surjective. On C, Serre duality gives H^1(omega_C(H|C))=H^0(O_C(-H))^*=0 because deg(H|C)=e>0. Riemann–Roch therefore gives h^0(omega_C(H|C))=g+e-1>=1. Consequently H^0(X,omega_X(2H)) is nonzero. Notice the e>=2 condition is essential: a plane has e=1,g=0 and this count is zero.

The inclusion q_*omega_X -> omega_Y requires no rational-singularity or canonical-singularity assumption. A section of omega_X over q^{-1}(V) restricts to a regular top form over V cap U, since q is an isomorphism there. It is determined by this restriction, because a regular section of a line bundle on an integral smooth scheme vanishing on a dense open is zero. Thus q_*omega_X injects into j_*omega_U. Normal Y has singular locus of codimension at least two, and its canonical sheaf is reflexive, so j_*omega_U=omega_Y. This is the needed inclusion, not an equality assertion.

Finite duality yields nu_*omega_Y=Hom_S(nu_*O_Y,omega_S). Since omega_S=O_S(e-4) is invertible, this is c tensor O_S(e-4), where c is the conductor ideal. Projection formula and the preceding injection identify a nonzero section of omega_X(2H) with a nonzero section of a subsheaf of c(e-2). Therefore H^0(S,c(e-2)) is nonzero.

For clarity, the conductor identification can also be seen locally. If A is an integral coordinate ring and B its finite normalization inside Frac(A), then every A-linear map B->A becomes multiplication by a rational function t after tensoring with Frac(A). Since 1 lies in B, t lies in A. The condition is tB subset A. Thus Hom_A(B,A) is exactly the usual conductor {t in A:tB subset A}. A conductor element which is a unit at a point forces B=A there. Hence c vanishes set-theoretically at every nonnormal point.

Every singular curve of S has nonnormal generic point. Indeed its generic local ring is one dimensional and singular; a one-dimensional normal Noetherian local domain is a DVR and regular. Over C regularity is equivalent to smoothness. Thus c is contained in the prime ideal of every singular curve, and each section of c(e-2) vanishes on that entire reduced curve. Isolated normal singularities do not need to be covered by this assertion.

Finally the hypersurface restriction sequence is

0 -> O_{P^3}(-2) -> O_{P^3}(e-2) -> O_S(e-2) -> 0.

H^1(P^3,O(-2))=0 lifts the nonzero conductor section to a homogeneous polynomial A_S of degree e-2. Its restriction is nonzero, so the lift is nonzero and is not divisible by the equation of S. It vanishes on every reduced singular curve. This proves exactly the proposed lemma.

## 2. Repeated factors of a minimal symbolic-square witness

Let L be a nonempty finite reduced union of lines, I=I(L), a=alpha(I), and alpha(I^(2))=a+1=d. Choose a nonzero homogeneous F of degree d in I^(2). For each line ell with linear prime p_ell, F lies in p_ell^2: powers of a line ideal are primary and symbolic powers equal ordinary powers.

The squarefree radical R of F vanishes on every line because each line prime contains some factor of F. If F has any repeated factor and deg R<=d-2, this contradicts alpha(I)=d-1. The only remaining repeated-factor pattern has d-deg R=1, so exactly one linear factor P occurs twice and every other irreducible factor occurs once: F=P^2 G, with G squarefree and coprime to P.

If G is constant, d=2 and all target lines lie in the plane P=0; this is the coplanar exception, not a contradiction. Otherwise choose a nonzero partial derivative D G (possible in characteristic zero). For any target line not contained in P, P is a unit at its generic point, so G belongs to p_ell^2 after localization and, since this ideal is primary, globally. Every partial derivative of G then lies in p_ell. Hence P D G vanishes on all target lines, including those contained in P, and has degree 1+(d-2)-1=d-2. It is nonzero. Contradiction. This argument does not require first excluding nonlinear factors of G.

Thus a noncoplanar L forces F to be squarefree.

## 3. Nonlinear reduced components are impossible

Suppose squarefree F=S_0 Q, where the irreducible equation S_0 has degree e>=2 and is coprime to Q. Take the degree e-2 adjoint polynomial A supplied above, and put B=A Q. This nonzero polynomial has degree d-2.

For each target line ell, if Q vanishes identically on ell then so does B. Otherwise Q is a unit at the generic point of ell, so S_0 is in p_ell^2. In coordinates p_ell=(x,y), this forces all first partials of S_0 to vanish on ell. Thus ell is contained in the singular locus of the integral surface S_0=0, and is a singular curve. A vanishes on ell, so B does too. Therefore B belongs to I in forbidden degree d-2. Contradiction.

Consequently F is a product of d distinct linear forms P_1,...,P_d.

## 4. The distinct-plane arrangement is complete and has no triple line

At the generic point of any target line, the order of F is the number of P_i containing that line. Since F lies in its symbolic square, every target line is the intersection of at least two of the planes.

Fix i<j, and ell_ij=V(P_i,P_j). If ell_ij is not among the target lines, then F/(P_i P_j) vanishes on every target line: any target line avoiding all remaining factors would have to be ell_ij. This is a forbidden polynomial of degree d-2. Thus every pair intersection is included.

If three planes contain the same line ell_ij, the same quotient F/(P_i P_j) still vanishes on every target line, now including ell_ij by its third plane. Again contradiction. Thus no three planes contain a line, and L is exactly the pseudostar consisting of all distinct pair intersections.

The source's Proposition 2.6 proves such pseudostars are ACM. One can additionally check this algebraically: J=(F/P_1,...,F/P_d) is the maximal-minor ideal of the d by (d-1) matrix whose jth column is P_j e_j - P_d e_d. Its height is two; Hilbert–Burch gives a perfect ideal and Cohen–Macaulay quotient. At a minimal prime (P_i,P_j), every other P_k is a unit since there is no triple line, and J localizes to (P_i,P_j). Thus it is generically reduced. A Cohen–Macaulay ring has no embedded associated primes, so J is reduced; it equals the intersection of the line primes. This also verifies the ACM assertion without a hypothesis of proper fourfold-plane intersections.

## Required disposition

The complex/characteristic-zero mathematical chain is sound. Do not erase the coplanar case, claim singular isolated points are covered by the adjoint lemma, assert equality q_*omega_X=omega_Y, or assume all hyperplanes are in full general position. Most importantly, do not turn this into an arbitrary-characteristic theorem without a valid replacement for the vanishing argument. No novelty, human peer-review, publication, or full source-literal resolution is certified by this audit.

## Binding to submitted TURN_1.md

Read the entire submitted TURN_1.md at 2026-10-02 04:10 UTC. It matches the mathematical chain audited above, and its current opening/closing scope qualifications correctly retain original-source unresolved status. Verdict: PASS_SCOPED_CHARACTERISTIC_ZERO_THEOREM, ORIGINAL_UNRESOLVED_ARBITRARY_CHARACTERISTIC. This is an independent AI audit, not a human referee report.

Minor exposition hardening (not a mathematical repair): specify that the chosen resolution is an isomorphism over Y_reg. Replace the compressed Bertini-integrality justification with the explicit connectedness argument above using H^1(O_X(-H))=0; this avoids relying on an unstated irreducible-Bertini formulation for the pulled-back subsystem. The existing conclusion is valid. Normalization need not embed into P^3, but H is still globally generated and nef/big via its map to S; no embedding assumption on Y or X was used.

Exact original source convention is https://arxiv.org/pdf/1306.4387, section 1 opening (PDF p1), and the target is Question3.1 (PDF p8). This source is primary and was opened in full text. OWR printed514 repeats the target without replacing the field convention with a characteristic-zero restriction. Thus a narrowly worded negative answer over C is justified, but a global source-literal `claimed_solved` disposition is not justified at this checkpoint.
