# Independent analytic freeze, before historical reports

2026-10-16 05:22:00 UTC. Completion estimate: 70%. This freeze precedes inspection of source/audits, previous verdicts, and other audit-family findings.

## Result reached independently

The arithmetic/rank portion of PROOF.md is valid. There is no arithmetic counterexample to its claim that the explicitly defined a,b have irrational ratio and yield a nondivisorial valuation on C(V×F1). This is an acceptance of this family’s obligations, conditional on the separately audited geometric and global-minimizer identification. No independent check in this family promotes a merely chosen valuation to the canonical minimizer.

## Exact moments and normalization

I independently integrated the polynomial-times-exponential pieces by the finite derivative antiderivative recurrence, rather than reusing the candidate’s symbolic integration. exact_rank_checks.py and EXACT_RANK_RESULTS.json verify the two elementary identities exactly, total masses 5 and 4, zero-parameter moments 5/12 and 2/3, and rational root brackets stated in the candidate. The Taylor sum order is 24, with exact absolute-first-moment remainder constants rather than the candidate’s looser constants. All 21 immutable source-file byte/SHA pins match the parent receipt.

Each moment F(t)=∫xρ(x)e^(−tx)dx has derivative −∫x²ρ(x)e^(−tx)dx<0. The positive values at zero and eventual dominance of a fixed negative subinterval over the positive part give existence of a positive zero. Hence each positive root is unique. Exponential-polynomial rewritings have artificial zeros at t=0 and may not substitute for the original root definitions.

The F1 polygon has width y+2 and horizontal average y/2. Thus the x-moment is one-half the y-moment when ξ=(0,b), and both vanish at B’s root. The covariance Hessian is positive definite because P has interior. Its fan determinant checks and area/centroid checks pass. This identifies the full toric critical point, not only a critical point on one chosen line.

Actual primary MW v2 §3.1 pp.11–12 was read and p.12 rendered/visually inspected: its divisor-order coordinate is shifted by discrepancy 1, so the canonical coordinate is s=k/m−1; its density and exponential sign are exactly those in (A). Actual WZ Theorem1.1 and Lemma2.2 were read; the latter uses e^(+c·y) for the analytic holomorphic vector c, whereas the candidate consistently uses the algebraic/filtration convention e^(−ξ·y). The conversion is c=−ξ. No factor-two conversion is needed because ord_D(w)=1 in the chosen character lattice. For a degree-m toric section, raw order is j+m. Subtracting m(a+b) from ak+b(j+m) gives a(k−m)+bj, in agreement with both canonical coordinates. Discrepancy a+b follows from the two transverse smooth divisors.

## Irrationality proof, all denominators

B’s positive zero b cannot have b²=2, since its remaining coefficient would then be 8+4b≠0. If b were algebraic and nonzero, its equation would force exp(2b) algebraic, contradicting Hermite–Lindemann. The classical theorem’s exact nonzero-algebraic hypothesis was independently checked against Theorem A on the first page of É.Delaygue, A Lindemann–Weierstrass theorem for E-functions, arXiv:2210.12046v2. This is a primary research paper stating the classical theorem; the 1882 original digitization was inaccessible (403), so I do not claim to have inspected the original proof. Neither Schanuel’s conjecture nor transcendence of a/b is assumed.

Assume a/b=p/q>0, p,q integers, and put r=p/q, z=exp(b/q). The candidate correctly obtains A_r(b,z)=B_q(b,z)=0, with
A_r(T,Z)=[r³T³+r²T²−2rT−6] Z^(3p)+16rT Z^(2p)+4rT+6,
B_q(T,Z)=(T²−2) Z^(2q)+3T²+4T+2.
Since b is transcendental and B makes z algebraic over Q(b), the field transport to a finite extension of Q(T) is legitimate. For an infinity valuation ν(T)=−e, R(T)=−(3T²+4T+2)/(T²−2) is a unit and Z^(2q)=R(T) forces ν(Z)=0. The three A summands have values −3e,−e,−e, impossible for a vanishing sum. No cancellation can hide in the cubic coefficient, whose top term is nonzero r³T³. Existence of the infinity extension follows by applying Stacks tag09E8 to the DVR Q[1/T]_(1/T) in characteristic0; its finite extension is separable.

An independent certificate avoids the valuation-extension step entirely. The Sylvester resultant Res_Z(A_r,B_q) has degree at most 3(2q)+2(3p)=6(p+q) in T by separate homogeneity. Its leading coefficient is Res_Z(r³Z^(3p),Z^(2q)+3)=r^(6q)3^(3p)≠0. Therefore it is a nonzero Q[T] polynomial. A common root z at transcendental b would make that polynomial vanish at b, a contradiction. This proves every rational ratio is excluded, independently of any finite tests. Actual exact Fraction/Sylvester determinant controls at five small p,q reproduce the stated degree and leading coefficient; they are controls on this proof, not a universal inference.

## Function-field rational rank and residue

At η(E×D), the local ring is regular of dimension2. Choose h∈C(V) with ord_E(h)=1, and torus characters z,w on F1 with ord_D(z)=0, ord_D(w)=1. The Gauss formula on C(V)(z,w) is well-defined: minimal terms for different pairs (ord_E coefficient,j) have distinct values because a/b is irrational; for a fixed pair, nonzero Laurent polynomials in z cannot cancel in the residue field C(E)(z). Multiplicativity follows from multiplication of those nonzero leading polynomials, so the valuation extends to the fraction field.

Both a=v(h) and b=v(w) survive on the function field. Every value is in aZ+bZ, giving equality. Its rational rank is2. Its ordered (Krull) rank is1, since it is an ordered subgroup of R; these notions must not be confused. Every c ord_F has value group cZ and rational rank1, regardless of whether c is irrational. Thus v is nondivisorial exactly in the candidate’s stated convention.

The residue field is C(E)(z): value-zero fractions have equal leading pairs (k,j), which cancel, leaving a ratio of residues in C(E)(z), and every such rational residue occurs. Its transcendence degree is2+1=3. Hence rat.rank(v)+trdeg_C κ(v)=2+3=5=dimX, the Abhyankar equality, with no lost section-degree direction. This is a quasi-monomial Abhyankar valuation centered at the codimension2 stratum. The direct value-group proof is sufficient for nondivisoriality and needs no converse divisorial criterion.

## Remaining scope

The irreducibility and exact Segre graded-ring identification, finite generation, singular central fiber, weak product-soliton argument, and global H-minimizer theorem application require the separate geometry/global families. The official OWR question has no dimension ceiling or product exclusion. Under those identifications, this arithmetic result supplies the genuinely nondivisorial minimizing valuation sought by the exact target. No full historical priority search was undertaken. No candidate/original source was changed.
