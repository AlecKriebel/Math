# Turn 3: the full SU(3) height-four span, without a center assumption

2026-10-02, 04:05 UTC. Third substantive author turn for problem 30000048. This is a scoped partial theorem. The source question for arbitrary connected simply connected compact Lie groups remains unresolved. Separate independent review is pending; no historical novelty claim is made.

## 1. Result and exact scope

Write chi_(a,b) for the SU(3) irreducible character of highest weight (a,b), where a,b are nonnegative integers. Define the finite integral span

    V_4 = sum_(a+b<=4) Z chi_(a,b).

There are fifteen irreducibles in this span. No restriction on their integer coefficients, apart from the hypotheses below, is imposed.

**Theorem.** If f belongs to V_4, is real and nonnegative at every element of SU(3), and has normalized Haar mean one, then f is exactly one of

    1,
    |chi_(1,0)|^2,
    |chi_(2,0)|^2,
    |chi_(1,1)|^2.                                      (1)

The respective square-root dimensions are 1, 3, 6, and 8. The conjugate roots chi_(0,1) and chi_(0,2) give the same functions. In particular, center invariance is a conclusion in this entire span, not a hypothesis.

Turn 2 handled only the five center-neutral irreducibles in V_4. The new part proves that none of the ten other irreducibles can occur in a nonnegative mean-one function in V_4. After imposing reality, these are five extra unrestricted integer parameters, which are eliminated analytically rather than by an experimental coefficient cutoff.

This does not prove any support bound for arbitrary S-characters. In particular it leaves SU(3) weights with a+b>=5, other higher-rank simple factors, and mixtures of higher-rank factors outside the proved scope.

## 2. Polynomial coordinates and two interior trace values

For g in SU(3), put u=tr(g) and v=conjugate(u). All characters in V_4 are polynomials in u,v with integer coefficients and total degree at most four. More precisely,

    chi_(a,b) = u^a v^b + terms of strictly smaller total degree
    whenever a+b<=4.                                    (2)

For completeness the distinct formulas up to exchanging a,b and u,v are

    chi_(0,0) = 1
    chi_(1,0) = u
    chi_(2,0) = u^2-v
    chi_(1,1) = uv-1
    chi_(3,0) = u^3-2uv+1
    chi_(2,1) = u^2v-v^2-u
    chi_(4,0) = u^4-3u^2v+v^2+2u
    chi_(3,1) = u^3v-2uv^2-u^2+2v
    chi_(2,2) = u^2v^2-u^3-v^3.                          (3)

These identities follow by multiplying by the Weyl denominator. The executable checks each of all fifteen formulas against the SU(3) Weyl alternant formula, rather than assuming the polynomial labels. Their triangular form proves that V_4 is precisely the integer polynomials in u,v of total degree at most four. Conversely, elimination of the leading monomials using (2) proves the integral spanning assertion, not just rational spanning.

Let D denote the set of possible traces. We need only the following elementary facts; we do not assume a plotted or numerical description of the full deltoid D.

**Trace fact A: the unit circle is in D.** If |s|=1, then

    diag(-s^2, s^(-1), -s^(-1)) in SU(3)

has trace -s^2. Its determinant is one, and -s^2 runs through the entire unit circle.

**Trace fact B: both 0 and 1 are interior points of D.** Parametrize diagonal matrices by

    U(theta,phi)=e^(i theta)+e^(i phi)+e^(-i(theta+phi)).

The derivative columns, viewed as vectors in the real plane, are i(z_1-z_3) and i(z_2-z_3). At (z_1,z_2,z_3)=(1,omega,omega^2), where omega=e^(2 pi i/3), the trace is zero and the real Jacobian is

    [ -sqrt(3)/2   -sqrt(3) ]
    [  3/2             0   ],

whose determinant is 3sqrt(3)/2. At (1,i,-i), the trace is one and the Jacobian is

    [ -1  -2 ]
    [  1   0 ],

whose determinant is 2. The inverse function theorem therefore gives open neighborhoods of 0 and 1 contained in D. This also justifies testing arbitrarily small real and imaginary perturbations of the trace zero, and perturbations to both sides of the unit circle near trace one.

The existence of an open trace set proves polynomial uniqueness in u,v: substituting u=X+iY and v=X-iY is an invertible complex-linear change of polynomial variables. Consequently, if an integral polynomial P(u,v) is real on D, then P(u,v)=P(v,u), as an identity. This is the reality condition used below.

## 3. Central averaging and the four possible averages

Write x=uv and y=u^3+v^3. Average f over the three central elements:

    H(g) = (f(g)+f(omega g)+f(omega^2 g))/3.               (4)

The center acts on chi_(a,b) by omega^(a-b). Thus (4) deletes irreducibles with a-b not divisible by three. It preserves integrality of the irreducible coefficients, nonnegativity, and Haar mean one. It also preserves the support condition a+b<=4.

The surviving irreducibles are exactly (0,0),(1,1),(3,0),(0,3),(2,2). Reality pairs (3,0) and (0,3), so

    H=1+A chi_(1,1)+B(chi_(3,0)+chi_(0,3))+C chi_(2,2),
    A,B,C in Z.

The exact theorem of turn 2 therefore applies. Its entire finite exclusion certificate was rerun in this turn: Schur coefficient bounds reduce to 19,635 triples, 19,631 have exact negative witnesses at actual SU(3) traces, and the four remaining triples have global square identities. No grid-only positivity assertion is an input. The four possibilities are

    H_0=1,
    H_3=x,
    H_6=x^2-y+x,
    H_8=(x-1)^2.                                        (5)

Their labels refer to the square-root dimensions. The use of turn 2 is an explicit dependency, not an independent reproof of its finite enumeration. Its executable, bounds, and proof remain preserved unchanged.

All real noncentral monomials of total degree at most four come in the five conjugate pairs below. Hence there exist integers a,b,c,d,e, with no a priori bounds needed, such that

    f=H+a(u+v)+b(u^2+v^2)+c x(u+v)
        +d(u^4+v^4)+e x(u^2+v^2).                       (6)

## 4. Integral Laurent extremality

We use the following elementary lemma, the constant-one and constant-two cases of Serre's one-variable argument (2025, Proposition 5.2 and Corollary 5.4).

**Lemma.** Let p(z)=sum_(j=-M)^M q_j z^j have integer coefficients, with q_(-j)=q_j, and be nonnegative on |z|=1.

1. If q_0=1, then p=1.
2. If q_0=2, then either p=2 or p=2+epsilon(z^m+z^(-m)) for some positive integer m and epsilon in {1,-1}.

**Proof.** If p is nonconstant, choose M>0 with q_M nonzero. Summing its values over the M-th roots of 1 and over the roots of z^M=-1 gives M(q_0+2q_M) and M(q_0-2q_M). All summands are nonnegative, so |q_M|<=q_0/2. This contradicts nonzero integral q_M when q_0=1. When q_0=2, one has q_M=epsilon=1 or -1. One of the two sums vanishes, so p vanishes at all M of the corresponding points. Nonnegativity implies at least double zeros in the circle parameter, and the parameter z is locally analytic with nonzero derivative, so these are double zeros of z^M p(z). Its degree is 2M, and its leading coefficient is epsilon. These zeros and the coefficient force p=2+epsilon(z^M+z^(-M)). The constant case is immediate. QED.

We also use the constant-one statement for an integral Laurent polynomial on a higher-dimensional torus. To prove it, choose an integer one-parameter substitution that is injective on its finite exponent support, including zero. Such a substitution exists by avoiding finitely many integral hyperplanes. The resulting one-variable polynomial remains nonnegative, has integer coefficients, and has constant coefficient one. The lemma makes it identically one; injectivity gives the same conclusion for the original polynomial.

The restriction used below is p(z)=f(z,z^(-1)). This is legitimate by trace fact A, even though choosing a matrix with trace z does not need to define a group homomorphism. It is a nonnegative integral Laurent polynomial. Formula (6) gives

    p(z)=H(z,z^(-1))+(a+c)(z+z^(-1))
             +(b+e)(z^2+z^(-2))+d(z^4+z^(-4)).           (7)

## 5. Elimination of every noncentral coefficient

### Case H=1

Restrict f to the maximal torus, using its genuine torus weight expansion. It is a nonnegative integral Laurent polynomial in two variables. Its constant Laurent coefficient is unchanged by central averaging, because the zero weight is fixed by every central translation. Since H=1, this constant coefficient is one. The multivariable form of the lemma proves f=1 on the torus, hence on SU(3) by conjugacy into a maximal torus. This argument does not require a degree cutoff.

### Case H=x

On the trace unit circle H=1. By (7), p has constant Laurent coefficient one, so the lemma gives p=1. Independence of the frequencies 1,2,4 yields

    a+c=0, b+e=0, d=0.                                  (8)

At u=0, f=0, and trace fact B gives nonnegativity on a full real neighborhood of zero. The linear term is a(u+v). On small positive and negative real u this forces a=0. The quadratic term is then

    uv+b(u^2+v^2).

Taking u real and u purely imaginary, and dividing by |u|^2 before taking the limit to zero, gives respectively 1+2b>=0 and 1-2b>=0. Thus -1/2<=b<=1/2. Since b is an integer, b=0. Equation (8) now gives c=e=0. Therefore f=H.

### Case H=x^2-y+x

On the trace unit circle H=2-z^3-z^(-3). Equation (7) has constant coefficient two and coefficient -1 at both frequencies 3 and -3. The lemma forces

    p(z)=2-z^3-z^(-3):

indeed the constant possibility cannot have these coefficients, and the only two-term possibility with a nonzero frequency 3 has m=3 and epsilon=-1. Again (8) follows. Near zero, H has leading quadratic term uv and no linear or constant term. Exactly the same local argument as in the preceding case forces a=b=0, and then c=d=e=0. Hence f=H.

### Case H=(x-1)^2

For every trace z with |z|=1, all three summands in (4) are nonnegative and their average H(z)=0. Therefore each is zero; in particular p(z)=0. Equation (7) again gives (8). Substituting these relations into (6) gives the exact factorization

    f=(x-1)[(x-1)-a(u+v)-b(u^2+v^2)].                    (9)

Take z in a sufficiently short open arc of the unit circle near 1. By trace fact B an open neighborhood of z is in D. As u moves radially through z, x-1 changes sign. Nonnegativity of (9) on both sides forces its second factor at u=z to vanish. Consequently

    a(z+z^(-1))+b(z^2+z^(-2))=0

on an open arc. A Laurent polynomial that vanishes on an open arc is identically zero, so the distinct Fourier coefficients give a=b=0. Equation (8) gives c=d=e=0. Thus f=H in the last case as well.

This proves necessity in (1). Sufficiency follows from the exact square formulas (3),(5) and Schur orthogonality: the square roots are irreducible, so each square is everywhere nonnegative and has Haar mean exactly one. The theorem is proved.

## 6. Reproducible controls and limitations

Run, from the original repository target directory:

    python3 verify_turn3.py

In the recovered layout used for this turn, run:

    python3 turn3/verify_turn3.py --prior-dir prior

The standard-library executable checks all fifteen Weyl identities and triangular leading terms; all 225 Haar orthogonality pairs; center weights and the five noncentral polynomial pairs; the circle restrictions and four square identities; the explicit unit-circle group realization; the two exact local Jacobians; and the factorization (9). It then reruns the complete turn-2 certificate. The receipt records 364 new exact assertions, plus the 19,889 prior turn-2 assertions rerun, with the unchanged exclusion-witness digest. These algebra checks complement the proof; the inverse function theorem, the nonnegative-zero multiplicity argument, and the analytic classification are justified above, not inferred from a test grid or advertised as formally proof-assistant-verified.

The broader mechanism is central averaging followed by integer Fourier rigidity on a trace circle and local positivity at its zeros. At higher degree, the difference f-H can contain extra multiples of uv-1 and higher-order terms at u=0. The present relations no longer eliminate all those terms. Nor has it been proved that an arbitrary central average belongs to the four functions in (5). Reusing the current argument without such new input would merely conceal the higher-degree problem.

**Exact remaining gap:** either classify arbitrary nonnegative integral SU(3) character polynomials of Haar mean one without a support bound, or exhibit a globally certified counterexample; then still address every other simply connected compact Lie group for an affirmative resolution. There is currently neither a full candidate proof nor a counterexample. Original status: unresolved after 3/5 substantive author turns; two remain.

## 7. Source and recovery record

The source target is Serre's 2004 question in *On the values of the characters of compact Lie groups*, section 2, printed pp. 666-667. The author-hosted two-page source was reopened on 2026-10-02:

https://www.college-de-france.fr/media/jean-pierre-serre/UPL8835246706135048784_On_the_values_of_the_characters_of_compact_Lie_groups.pdf

The later primary source is Serre, *Zeros de caracteres*, L'Enseignement Mathematique 71 (2025), 433-457, DOI 10.4171/LEM/1095; the exact question is Problem 4.6 and the credited Laurent lemma appears in section 5:

https://ems.press/content/serial-article-files/50890

The original target webpage was unavailable through the web tool in this turn. The pinned source fallback in SOURCE_GATE.md was respected. The 2025 primary source explicitly retains the general statement as a problem. A bounded current search found finite-group S-character papers but no source settling this connected simply connected classification; this is not a comprehensive worldwide novelty certification.

Branch math/30000048-positive-characters-wip was verified at 637057d98f94496fbc3b33d3ab36d8e161b5bcaf before the turn. All nineteen target files were recovered, and all eighteen entries in TURN_2_MANIFEST.json were matched byte-for-byte by size and SHA-256. The branch's canonical queue row still says queued, 0/5, while its explicit turn artifacts prove two completed author turns before this one. That stale queue row must be reconciled by the single coordinating writer; it must not reset or override the substantive-turn ledger. No GitHub write or publication was performed in this turn.

Repository-required completion estimate: 30%, subjective and uncalibrated, not a correctness probability or a claim that 30% of the unrestricted cases have been covered.
