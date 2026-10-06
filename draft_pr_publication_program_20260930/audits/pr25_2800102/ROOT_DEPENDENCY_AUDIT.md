# Root audit of the square Gaussian target and external dependencies

Checkpoint: 2026-10-01 UTC. This is validation of existing literature, not
a new problem-solving attempt. The original sixteen-file source audit,
its real-proof hold, its historical receipts, and the early root seal are
preserved. A new independent real falsifier and a fresh complete gate are
still required before changing the current disposition. Workflow estimate
at this checkpoint: 65%; original proof-search budget remains 0/5.

## Exact claim and proof standard

For every integer N>=1, with independent real variance-one entries or
standard circular complex entries (each component has variance 1/2), set
alpha_K(N)=N^(-3/2) E Tr sqrt(XX*). The original Bandeira2013/MIT2015
target asks for real increase and complex decrease in the square case.
Both strict directions cover the weak formulation. A rectangular theorem,
bounded prefix, asymptotic inequality, or unnormalized nuclear norm does
not discharge this target.

The root read the actual original author post and full MIT handout,
Hutnik real2608.12151v2 square proof through Proposition2.2, Abel
Theorem2.5, Section3.1--3.3 and AppendixA.1, the whole three-page
Baslingker--Dan2608.27532v1 proof, and Abreu--Patil2609.07802v1's complete
square decrement dependency (density/recurrence/generating function,
continuation and Delta-domain transfer, leading asymptotics, Lemmas5--6
and the complete Section4 upper bound). Hutnik unitary2608.12147v2's
model, attribution and square sign statements were checked; its wider
shape-transition claims are not certified here. Fresh root download
hashes and the failed versioned Livan--Vivo request are recorded in
ROOT_SOURCE_RETRIEVAL.json. The direct real derivation below does not
assume the inaccessible download's density identity.

This is ordinary analytic verification using established Gamma/Beta,
Laguerre, finite Pfaffian, hypergeometric continuation and coefficient
transfer results within their hypotheses. It is not a formal machine
proof. Early family messages preceded the root reconstruction seal;
therefore the root is not an additional blind independent family.

## Complex square: direct reconstruction removes continuation ambiguity

The joint law gives counting density exp(-x) sum_(j<N) L_j(x)^2,
of mass N. With sigma_m=(-1/2)_m/m! and h_j=Gamma(j+3/2)/j!,
the finite connection formula and orthogonality give

    Y_N=sum_(k<N) sum_(j<=k) sigma_(k-j)^2 h_j,
    sum_(N>=1) Y_N z^(N-1)
       =Gamma(3/2)(1-z)^(-5/2) 2F1(-1/2,-1/2;1;z).

Each coefficient is a finite sum. Conjugating the hypergeometric ODE
and extracting coefficients proves, for every N>=1,

    Y_(N+1)=(2+3/(4N^2))Y_N-Y_(N-1),
    Y_0=0, Y_1=sqrt(pi)/2, Y_2=11sqrt(pi)/8.

Thus neither Carlson continuation nor an imported integer-moment
polynomial identification is needed for this square half moment.
For alpha_N=Y_N/N^(3/2), the increment recurrence has positive previous-
increment coefficient and negative source coefficient because

    (1+x)^(3/2)+(1-x)^(3/2)>2+3x^2/4, 0<x<=1.

The second derivative is strictly above3/2 on(0,1); integrate twice
and use the endpoint value. Base strictness is121<128. Induction proves
strict complex decrease for every N. The printed Baslingker--Dan scalar
domain x>=0 is wider than its real domain; every use x=1/N is valid.

## Real square: density, both parities and analytic interchange

The root challenged real_family/DERIVATION.md equation by equation.
Let w=x^((lambda-1)/2)e^(-x/2), P_j=L_j^lambda, and
D=x d/dx+(lambda+1-x)/2. Then (xwP_j)'=wDP_j and
DP_j=((j+1)P_(j+1)-(j+lambda)P_(j-1))/2. Endpoint
terms vanish for lambda>=0. With psi_j=integral sign(y-x)w(y)P_j(y)dy,
B_ij=integral wP_i psi_j, H_j=Gamma(j+lambda+1)/j!, integration
by parts gives B D=-2H, with this sign convention.

The skew recurrence determines the upper even/odd block explicitly;
even size gives B_N^(-1)=-D_N H_N^(-1)/2. For odd size the integral
border b has b_(2m)=2^omega Gamma(omega)(omega)_m/m!, b_odd=0,
omega=(lambda+1)/2. The augmented inverse is

    [ Q, -e_last/b_last ; e_last^T/b_last, 0 ],
    Q=-D_N H_N^(-1)/2.

Multiplication verifies the last-column rank-one correction cancels,
not just the even block. Logarithmic finite-Pfaffian differentiation
then gives -phi^T Q psi for even size and the additional
phi_last/b_last for odd size. At N1 the kernel correction cancels
and the remaining term is the elementary chi-square density. This
explicit odd border is essential, not a limiting convention.

The exact psi recurrence and Gamma duplication match the printed
Phi1/Phi2 formula, including the real exp(-x/2) versus complex exp(-x)
scale. The x=2y density Jacobian is1/2. The independent monomial
joint-law controls reproduce printed half moments for both parities.

Abel completion is analytic, not an interchange of merely formal tails.
For fixed polynomial p and real |a|<1, integrate its monomials against
x^lambda exp(-x)L^lambda(a,x). Their absolute majorants are constants
times Gamma(lambda+j+3/2)(1-a)^(j+1/2). For the parity Beta integral
the remaining weight (1-z^2)^(omega-1) is integrable since omega>=1/2.
For an interior Abel parameter, a Cauchy coefficient bound on a larger
circle supplies a geometric ratio and an integrable exponential tail.
These justify Fubini and dominated convergence for the integrated
half moment. The final diagonal summand is O(m^(-omega-3/2)), at
least O(m^-2), so its ordinary tail is absolutely convergent.

Finite Laguerre connection products give Q=kappa+E, with
kappa_d=1/[pi(d^2-1/4)], E>=0 and E decreasing in its first index.
The parity-completed second index is N-1+2u in both cases. The printed
adjacent A-coefficient comparison at square shape for N>=3 is justified
by its exact gamma-ratio derivative and the telescoping shape-one
upper bound; auxiliary real shape interpolation is a density/gamma
inequality, not a matrix of noninteger dimension. No bounded sample
of u was substituted for this all-u proof.

## Quantitative complex input: no circular use of the real result

Abreu--Patil's positive generating function is the one derived above.
Its logarithmic hypergeometric continuation is on the principal cut
branch, with a convergent local expansion for |1-z|<1 and
|arg(1-z)|<pi. The manuscript explicitly verifies an analytic
Delta-domain before coefficient transfer. Its arbitrary-order remainder
justifies the recurrence comparison eliminating all odd inverse powers:
the leading coefficient at index j is j(j-2), which is nonzero for
odd j. This is not coefficient extraction from a real-axis bound.

The first singular coefficients are c0=2/pi, c1=-5/(2pi),
c2=(log2/4+11/32)/pi, d2=-1/(16pi). Gamma-ratio expansion gives

    alpha_C(n)=8/(3pi)+(ell_n-17/6)/(16pi n^2)
                    +O(log n/n^4),
    Delta_n=(ell_n-10/3)/(8pi n^3)+O(log n/n^4),
    ell_n=log n+gamma+6log2.

The arithmetic constants were checked independently. Define
E_n=8pi[n(n+1)]^(3/2)Delta_n-log n. The above proves
E_n tends to gamma+6log2-10/3. Positive connection coefficients,
Gauss's sum and Gamma log-convexity give the independent auxiliary
upper bound alpha_C(n)<8(n+1/2)/(3pi n).

The exact E recurrence and the scalar coefficient comparison in
BOUND_AUDIT.md imply E_n strictly decreases. The printed Lemma6 starts
at an index that omits q1, but its actual convergent-series proof holds
for all0<t<1; applying it at t=1/2 closes that boundary. The compared
odd coefficients are nonnegative and the even coefficient ratio has
positive residue24j^2+77j+50. There is no unsupported endpoint inference.
The E limit now gives Delta_n>0 and alpha_C(n)>8/(3pi). Only then does
the positive leading q coefficient give 8pi q_(n-1)Y_n>1/n.
Strict infinite telescoping proves for every n>=1

    0<Delta_n<[H_n+6log2-10/3]/[8pi(n(n+1))^(3/2)].

No real theorem or withdrawn2016 estimate enters this derivation.

## Real reserve and finite exceptions

For N>=3 the real diagonal variation exceeds1/[8pi N(N+1)].
The root checked the Gamma/digamma lower bound and the first-diagonal
ratio: after N=t+3 its deciding polynomial is
4t^3+32t^2+71t+37>0. Subtracting the independently certified complex
decrement gives the real reserve. The harmonic estimate starts at N4
and propagates by induction; the rational constants give a bound
strictly above1/(160N^2). Direct joint-law exact means and Machin-
formula rational pi/radical enclosures close N1,2,3 without relying
on decimal numerical evidence or assuming the asserted Appendix values.

The first raw means are sqrt(2/pi), sqrt(pi)(2-sqrt2/2), and
3sqrt(pi)/2+2sqrt(2/pi); division by N^(3/2) is retained. Root isolated
reproduction verifies these computations and all three family controls.

## Current disposition and explicit limits

At ordinary analytic-proof standard, the root identifies no remaining
central mathematical gap in the original square external theorem chain.
The separate new real falsifier and a fresh review of any new current
candidate remain outstanding process gates. Do not transfer an original
source-only PASS to a stronger edited candidate. Do not rewrite original
hold metadata, seals, receipts or the 0/5 budget.

If accepted after those gates, credit the2026 external papers as resolving
the exact source problem. This is not a new campaign solution and requires
no new paper, DOI, release or tracker row. Broader rectangular transitions,
human peer review, formal verification, worldwide priority, and historical
absence of every remote duplicate are not certified. The old imported
withdrawn claim remains rejected; the separate August2026 published
recurrence letter does not reinstate it. Actual original negative-search
receipts are absent, so those historical statements remain attributed
reports rather than independently reproduced historical evidence.
