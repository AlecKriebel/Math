# Independent analytic attack record

Derived after the source-first plan and primary problem assessment, without treating favorable gates or reviewer conclusions as authority. Locations refer to current centered_pedal_dn.tex sections and labels.

## Geometry and complete scope

Stachel's journal Theorem 4.3 supplies P(w)=(-a sn w,b cn w), delta=4K tau/N and v=delta/2 in (0,K). cn(v)=beta/b is uniquely solvable on that interval. Confocality gives dn²(v)=a² beta²/(b² alpha²), hence the stated a=alpha dn(v)/cn(v). P parametrizes once modulo4K; gcd(N,tau)=1 is precisely least physical period. Primitive stars are the larger coprime tau cases. Reversal reverses both the ordered vertices and the induced ordered edge feet and negates both signed areas.

Substituting P(u±v) into n(u)·X leaves numerator sn²(u)dn²(v)+cn²(u)=1-k²sn²(u)sn²(v), the addition denominator. The contact is on the inner ellipse. For real u, n·n=dn²(u)/beta²>0, so Q=n/(n·n) is the actual complete-line Euclidean foot. Its components have length units. Bilinear complex continuation is appropriate. The shoelace factor1/2 and double endpoint occurrence give A=C_A S with the stated positive C_A, without requiring simple polygons.

## Two-pole divisor

The order of delta/(2K)=2tau/N modulo1 is m=N for odd N and N/2 for even N. The generator delta/ell is2tau or tau, coprime to m; each residue occurs N/m times. This follows from gcd, independently of finite checks. S is even by j→N-j, ell-periodic by residue reindexing and2p-antiperiodic by dn.

DLMF22.4 confirms the Jacobi poles2rK+(2s+1)p and dn periods2K,4p. At p, dn(p+z)=-i cn(z)/sn(z)=-i/z+O(z), so Res S=-i N/m; equal real-period translates cannot cancel. Thus S is nonconstant with exactly two simple poles on X=C/(ell Z+4p Z). At p+ell/2 and3p+ell/2 evenness and antiperiodicity force zeros. A principal divisor on a compact torus has total degree zero, making these simple and exhaustive. Shifting by ell/2 exchanges zeros and poles; S(w)S(w+ell/2) is holomorphic on X and constant. Real positivity makes the constant positive. No unsupported assertion about a smaller imaginary period is required.

## Pedal cancellation and multiplicities

At common Jacobi poles Q is holomorphic and zero, since its numerator has a simple pole and dn² a double pole. Its only remaining possible poles are dn zeros at r=K+p and translates, of order at most2. DLMF22.4.3 gives Q(r+x)=(alpha/k) cn(x)/sn²(x) (dn(x),i), even in x, so there is no simple Laurent coefficient. The DLMF sign dn(r+x)=+i k' sc(x) does not change Q because dn is squared.

A singular vertex's incident area terms combine into det(Q(r+eps),Q(r+delta+eps)-Q(r-delta+eps))/2. Neighbors are regular because0<delta<2K is not a real pole-to-pole displacement. Reflection makes the difference2eps Q'(r+delta)+O(eps³), reducing the double pole to a simple pole. For even N the two singular indices differ by m=N/2>=2. Their incident edge sets are disjoint, including N4; the regular N4 neighbors vanish. N3 has one singular index. Real2K translation negates all Q values, preserving determinants, so antipodal residues add.

T is2K-periodic,2p-antiperiodic and delta-periodic, hence ell-periodic. On X its only possible simple poles match S(u+K). Matching one residue and using antiperiodicity removes both poles. The difference is constant on X and its antiperiod forces zero. This neither assumes the target invariant nor divides by polygon area.

U=(alpha/k)(1,i) and Res S(u+K)=-i N/m give C_T=i det(U,Q'(r+delta)). Let q=Qx+iQy. Rationalization gives q(r+x)=-alpha k cn(x)/(1+dn(x)). The Jacobi ODE yields q'=alpha k sn(x)(dn(x)+k'²)/(1+dn(x))² and hence exactly the displayed C_T. Its factors are positive for0<delta<2K. Sign, factor, length² units and N4 are consistent.

## Parity, boundaries and counterexample

(K+v)/ell=N/2+tau for odd N, and(m+tau)/2 for even N. For4|N, m is even and tau odd, giving a half-period. For primitive N=2 mod4, m and tau are odd, giving a full period and A B=C_A C_T S². Genuine poles and positive coefficients prove nonconstancy; an identity on a real interval would extend meromorphically and contradict those poles.

As k→0, S→N and the coefficients recover ordinary circle polygon/pedal areas. At exact circularity the excluded-period nonconstancy need not persist; a>b excludes it. lambda→0 or b² removes the proper nested elliptic geometry. No uniform boundary extension is asserted. Hyperbolic/nonconfocal caustics, arbitrary moving point, clipped feet, and unweighted star-face areas are excluded. Real trace positivity proves both areas positive in the chosen orientation, so absolute values of those shoelace areas correctly preserve the product.

Own exact code verifies H/J membership, tangent discriminants, interior caustic contacts, forward unit reflection, distinct vertices, complete-line feet and shoelace sums. Products14000/729 and14336/729 multiply by4 under double traversal, giving twelve-entry gap448/243. This falsifies a list-length reading while leaving least physical period six.

Own finite diagnostics check38,057 coprime cases through N500 and24 modulus/period/star configurations, including k=1e-6,0.9999, complex phases and near-pole residues. They support, but do not replace, the analytic argument.

## Attribution, antecedents and reading limits

Ferudun's centered primary PDF was freshly read completely in memory; SHA2568ba41a5466bc289a9f714b57527f596fbe39b3422bc6bcf0a95d39bbde50c40c. It states the same theorem, stars and repeated-six/twelve obstruction, and derives B as a coefficient times sum dn/W. The current addition identity converts this to S(w+K+v)/(ab). Thus the normalization/coefficient follows from that preprint and standard identities, as the note explicitly acknowledges. No theorem/formula/method novelty is claimed.

The later arbitrary-point primary PDF was read for introduction and Lemma4.3 with adjacent context, plus attribution/disclosure contexts. Its adjacent-foot cancellation supports the precise citation. I did not audit the complete17-page theorem or its supplement.

AST arXiv2001.02934v2 Section4 was checked from primary arXiv HTML/PDF text: adjacent-neighbor cancellation, bilinear complex coordinates, boundedness and Liouville are antecedents. Chavez-Caliz journal Section5 Theorem6 uses meromorphic area products and zero/pole removal for original/outer tangent polygons. Neither citation is misrepresented as itself proving this centered odd-period theorem.

No exhaustive literature or worldwide-priority search, independence certification or formal proof-assistant verification was attempted. Those claims are absent from the current note.

Conclusion: no mathematical gap or substantive scope/attribution defect found. This independent audit judgment is not publication authorization.

