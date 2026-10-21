# Independent full-level, specialization and arithmetic audit

This report closes C005-C010 and C044-C061 for the immutable qualification_v03 candidate. It also supplies the arithmetic part of C004 together with the separate complete geometry and kernel reports. No conclusion below is inferred from a prior PASS label. The exact equation identities were checked in the first independent assessment before supplement exposure, and the decisive classical input was subsequently obtained from independently retrieved primary sources. This is a mathematical review within the declared assumptions, not external human peer review or publication approval.

## Fixed assumptions and source applicability

Write r=sqrt(5), K=Q(r), phi=(1+r)/2, c=phi^5=(11+5r)/2, d=5+2r and delta^2=d. Fix the manuscript's side-product scale, affine unit circle and origin O=[0:1:0]. The arithmetic statements concern finite lambda in K with lambda not 0,-5r,-c. Geometric identities and normalization assertions apply after any characteristic-zero base extension. They do not imply the same extension degrees over a larger arbitrary coefficient field. The generic arithmetic base is K(lambda). The pencil's nonreduced member at infinity is excluded from the elliptic family. No claim over Q, characteristic two/five, nonregular pentagons, alternative star expressions, local solubility or Sha is being proved.

The exact transport to the nonsingular Tate curve is

    D_beta: y^2+(1-beta)xy-beta y=x^3-beta x^2,
    beta=-lambda/[c(lambda+5r)],
    k=4(lambda+5r)/r, q=dk^2,
    xi=q(x-beta), eta=(k delta)^3[y+((1-beta)x-beta)/2].

The fresh geometry certificates prove the whole equation identity, projective origin preservation and nonzero scales on every allowed fiber. This is an actual origin-preserving isomorphism over M=K(delta); a j-invariant comparison is not its justification. The pullback identity

    Delta_beta=125 lambda^5(lambda+c)/[c^6(lambda+5r)^7]

proves that no allowed plane parameter gives a singular Tate curve. In particular the five-cusp plane member remains a smooth elliptic normalization.

Independently retrieved sources, actual native retrieval clocks, complete streams, byte pins, extractions and selected original renders are retained in this phase3 directory. Fisher's published primary has 33 physical pages; the operative readings here are Lemma1.1 at printed172, the discriminant at173, the full-level definition/action at179, and Lemma3.4 at194, with original pixels at physical4,11,26,27. Other initial contextual text scopes were read, but a whole33-page reading is not asserted by this reviewer. Morton v1 has10 pages and v4 has19; operative text v1 pp3-7 and v4 pp5-9,18, and original pixels v1 pp3-5/v4 pp5-7,18 were inspected. This is not a claim to have reread every Morton page. Verdure is an18-page scan: all18 original pages were visually read, including the complete operative proof on printed84-88. Nearly empty pdftotext output was never treated as a reading. Sutherland's actual lecture5 degree/division statements and lecture23 section23.5/Theorem23.29 were read; the original latter theorem page13 was visually inspected. Referenced textbook proofs were not separately reread.

## Fine marking, signs, and every specialization

Fisher's [published primary](https://ems.press/content/serial-article-files/31488) Lemma1.1 gives the unique Tate normal form of a curve with a marked point of order at least four and states that this marked pair has no automorphisms. Its n=5 equation is exactly the manuscript's D_beta. At printed179 he defines Y(n) by triples (E,P,Q) with e_n(P,Q)=zeta and gives the action Q -> Q+P, with quotient X1(n). Thus, once the nonzero point P0=(0,0) and zeta are fixed, there are exactly five complementary choices Q with pairing zeta, rather than ten unmarked abscissas or twenty unsigned coordinates. They form a degree-five torsor under the constant cyclic group/identified mu5. Simultaneous sign change of an abstract basis does not create an extra degree-two cover: the fixed pointed object has no automorphisms, and an isomorphism between differently represented pointed objects transports the entire basis. Forgetting the marking or pairing would change this count and is not being done.

This fine interpretation remains valid at j=0 and1728. Nontrivial origin-fixing automorphisms there have orders dividing6 or4; none fixes a nonzero fifth-torsion marking. Fisher's marked-pair uniqueness therefore applies there as well. In characteristic zero E[5] is finite etale, and the subset e5(P0,Q)=zeta is finite etale of degree five over the nonsingular pointed Tate base. Neither a generic irreducibility hypothesis on every fiber nor a generic-only j statement is needed.

Fisher's Lemma3.4 and its marked-subgroup proof give the full-level map beta=tau f(tau)/g(tau), with exactly

    f=tau^4+3tau^3+4tau^2+2tau+1,
    g=tau^4-2tau^3+4tau^2-3tau+1.

Set epsilon(tau)=(phi tau+1)/(tau-phi), iota(v)=(cv+1)/(v-c). Direct matrix multiplication makes both involutions: their squared fractional-linear matrices are scalar matrices. The exact rational identities, independently checked before the package was read, are

    tau f/g=iota(epsilon(tau)^5), iota(beta)=-1/(lambda+c).

Consequently the geometric marked cover has generic function field u^5=-1/(lambda+c), u=epsilon(tau), over K(zeta). This correspondence includes the marked Z/5 subgroup in Fisher's proof; it is not inferred merely from two matching rational fractions on an unrelated family.

Take the base B=P1_lambda minus {0,-5r,-c,infinity}. Its coordinate ring is normal. The pointed torsion cover is finite etale over B. The Kummer cover is also finite etale there: a=lambda+c is a nonzero unit, u is nonzero, and the derivative 5u^4 is invertible. The two connected generic covers have isomorphic function fields by the actual Fisher map. Each finite normal cover is the integral closure of the same base in that function field. They therefore agree over the whole B, not just its generic point. Their fibers are precisely the complementary marked vectors, including a split five-point fiber. Extra automorphisms of an unmarked CM curve do not interfere. This proves C044-C047 without extending a generic irreducibility statement to each specialization.

The field equality under u=-1/theta, theta^5=a, is literal in both directions. For a fixed identified Kummer group, [-1/a]=[a]^{-1}; -1 is a fifth power. The manuscript explicitly makes this inversion distinction, so no fixed-class sign error remains (C048).

## Independent older specialization route

The [original Verdure scan](https://math.uit.no/ansatte/hugues/papers/IJPAM.pdf), printed80-81, Proposition3 and Corollary1, proves that after a field contains zeta and a rational nonzero fifth-torsion point, the full coordinate extension is cyclic of degree one or five; the relevant complementary abscissa also generates it. The elementary representation reason is useful to check applicability: in a basis beginning with the marked P, every Galois matrix has first column (1,0). Fixing the pairing value forces its determinant to be one, leaving only the five unipotent matrices [[1,t],[0,1]]. This is an upper bound on the coordinate field, not a proof that the degree is always five.

Verdure's Tate equation at83 has parameter t=beta with the same signs as D_beta. Theorem5 at84 states the nonsingular full-torsion iff criterion over a field containing zeta and of characteristic different from5. For zeta+zeta^-1=(r-1)/2, its two discriminant roots are alpha5=c and beta5=-c^-1. The criterion is that (beta-c)/(beta+c^-1) be a fifth power. The proof on84-88 works over Z[1/5][T] using projective polynomial addition and Lagrange resolvents. At88 it explicitly justifies specialization for every P5(T) nonzero: the discriminant and the necessary parameter differences remain nonzero, so the displayed nonzero resolvent does not disappear. It is genuinely an all-nonsingular-specialization input. No generic-to-special leap or unproved assertion that all radical degrees stay five is required.

In the current parameter the checked exact ratio is

    (beta-c)/(beta+c^-1)=-c(lambda+c)=(-phi theta)^5.

Let F=K(zeta), H=F(D_beta[5]). Adjoining theta makes the criterion a fifth power, so H is contained in F(theta). If theta is already in F, this is H=F. Otherwise F(theta)/F has degree five: over a field containing mu5, the orbit of a fifth root is a subgroup of the five roots and has size one or five. The criterion forbids H=F; the preceding degree bound forces H=F(theta). This proves equality, not just an upper inclusion, in both cases. The Weil pairing supplies F inside K(D_beta[5]), hence K(D_beta[5])=F(theta). The same argument works with base L=K(delta,zeta) and after every allowed specialization. It independently closes C050-C052 even without relying exclusively on the normalization-of-cover argument.

Morton's actual [v1](https://arxiv.org/pdf/1612.06268v1) pp3-5 and [v4](https://arxiv.org/pdf/1612.06268v4) pp5-7 give the prior universal residual table and product coordinates. His curve E5(b) is D_beta under b=-beta, epsilon=phi^-1, epsilon_bar=-phi. All eleven D5 coefficients agree, row by row, with R_beta under that substitution. His radical becomes

    u_M^5=(2b+11+5r)/(-2b-11+5r)=c(lambda+c), u_M=phi theta.

Both branches of his product coordinates are old mathematics. V4p18 recovers the generic field; that generic recovery alone was not used as a universal-specialization proof here. These older inputs are expressly credited in the note. The exact radical comparison closes C049, and the actual v1 witnesses that it is already present in2016, independently of later PDF rebuild dates. This does not certify the ultimate earliest discovery of the general machinery.

## Lower inclusions for the twist field

The genuine Tate isomorphism gives L(E_lambda[5])=L(theta). To descend from that equality to the exact field over K, let H_E=K(E_lambda[5]). The point P0 has image

    xi=-q beta, eta=-k^3 d delta beta/2.

The eta coefficient excluding delta is a nonzero element of K: k,d,beta all are nonzero on the allowed range. Thus delta lies in H_E, not merely in a convenient field over which one could write a map. The coordinate field here is intrinsic to the smooth elliptic curve: its K-defined isomorphism to W transports its torsion coordinate field, and the W point genuinely has the displayed coordinate.

The [actual Sutherland lecture23](https://math.mit.edu/classes/18.783/2023/LectureNotes23.pdf) Theorem23.29 and Corollary23.30 state nondegeneracy, Galois equivariance and the cyclotomic inclusion. The geometric kernel is a full rank-two fifth-torsion group by the independently checked direct kernel proof. A basis has primitive fifth-root pairing value; since all points and the curve coefficients are fixed over H_E, its pairing value is fixed there. Hence zeta lies in H_E. This supplies L inside H_E. Therefore H_E=L(E[5])=L(theta), proving C005,C052-C054. No lower inclusion is inferred from a polynomial splitting upper bound or from delta merely appearing in a chosen formula.

## Exact degree, group and rational subgroups

Norm_K/Q(d)=(5+2r)(5-2r)=5. If d were a square in K, its norm would be a rational square. Thus M=K(delta) is quadratic. Under the fixed real embedding, d is positive and M is real. F=K(zeta) is imaginary quadratic over the real field K because K is precisely the real quadratic subfield of Q(zeta5). Hence M and F are distinct quadratic extensions, their intersection is K, and [L:K]=4 (C055).

For a in K*, if v in L has v^5=a, then N_L/K(v)^5=a^4. Thus (a/N(v))^5=a. This proves that a becomes a fifth power in L exactly when already one in K. It covers every nonzero a, including negative a, and does not confuse the degree-four norm with a degree-two one. If a is not a fifth power in K, the cyclic Kummer extension L(theta)/L has degree five; if it is, the extension is trivial. Together with the compulsory degree-four L this proves degrees20 and4, respectively, with no smaller exceptional arithmetic field (C006,C056).

Choose the real fifth root theta of real a; there is one even when a<0. In the nonsplit case N=F(theta) is the splitting field of X^5-a over K. Its subgroup over F is cyclic order five; complex conjugation fixes theta and inverts zeta, hence conjugates rotation to its inverse. Therefore Gal(N/K)=D10, of order ten. D10 has a unique index-two subgroup, its order-five rotation subgroup, so its unique quadratic subfield is F. Since M is quadratic and different from F, M intersects N in K. Adjoining delta gives the direct product D10 x C2. In the split case N=F and adjoining M gives C2 x C2 (C007,C057). This argument does not assume positive a or confuse a group over K with one over Q.

For the generic base, the valuation of lambda+c at lambda=-c is one. A fifth power has valuations divisible by five, so a is not a fifth power in K(lambda). The same norm argument applies after adjoining the independent constant quadratics. Thus the generic field has degree20 and the same stated group (C010,C058). The finite specialization may reduce to degree4 exactly as specified; generic irreducibility is not imposed on it.

The independent involution changing delta while fixing N is available in both cases by the proven disjointness. In the actual equation map xi stays fixed and eta changes sign, which is the W group negation. Hence it acts on E[5] by -I. Its only fixed fifth-torsion vector is zero, so E(K)[5]=0 (C008,C059).

Over M the five smooth infinity points exist and are exactly the transported cyclic marked group by the direct map-limit calculation. The group of real elliptic points has one or two circle components; odd-order torsion is in the identity component and its fifth kernel has exactly five elements. Since M is a real subfield, E(M)[5] cannot exceed five, and the infinity subgroup supplies five. Hence it is the entire M-rational kernel (C009,C060). Equivalently the matrices below give that fixed space in both split and nonsplit cases; that argument also applies directly to the generic representation.

Start with the infinity generator P. Complex conjugation fixes it and has determinant -1 from the Weil pairing. For a complementary Q it has C(Q)=-Q+tP. Replacing Q by Q-tP/2 makes Q anti-invariant; division by two is legitimate modulo five and adding a multiple of P preserves the pairing. The Kummer subgroup fixes P and acts nontrivially on Q as Q -> Q+vP. Exact coordinate-field equality implies v is nonzero, and choosing its generator normalizes v to1. Delta's independent involution acts as -I. The matrices are therefore exactly -I, diag(1,-1), [[1,1],[0,1]], with the last absent in the split case. They satisfy the dihedral conjugation relation, have the correct cyclotomic determinants and generate the faithful order20 or4 image. This closes C061 without assuming a basis sign convention that the manuscript did not state.

## Strongest result and exact limits

The full coordinate field, every allowed specialization, all degrees/groups and rational subgroups are proved within the exact stated arithmetic base and origin. No central arithmetic or modular premise remains unsupported. The old universal source machinery is a credited theorem input; this is not a proof-assistant formalization or a rederivation of all Weil-pairing theory. Ultimate priority, oral workshop knowledge, current openness and first-public timestamps remain historical limitations, distinct from these deductions. Publication and final external namespace closure remain root obligations. No candidate/global file was changed by this reviewer.
