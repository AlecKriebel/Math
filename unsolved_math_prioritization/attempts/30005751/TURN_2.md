# Turn 2: the oddless finite upper bound is genuinely stronger

Status: an explicit reduct-language separation eliminates a natural finite candidate. It does not rule out other finite axiomatizations of TEIP. The underlying model is credited prior work; no novelty claim.

## 1. A credited nonstandard model and its power predicate

Let F be the real algebraic numbers and X a positive infinite indeterminate. Let I be the ring of finite Puiseux polynomials

p=Σ_(q∈S) a_q X^q, S⊆Q_(≥0) finite, a_q∈F, with a_0∈Z,

ordered by the sign of the coefficient at its largest exponent. Put M=I_(≥0). Jeřábek's Example3.10 recalls Shepherdson's result that M models IOpen and gives an expansion to TEIP_P2. This IOpen fact is an external dependency, not proved by the finite polynomial checker below.

For clarity, the power predicate can be checked directly:

P={2^k X^q:q>0 rational, k∈Z} ∪ {2^k:k∈N}.

For a positive nonstandard p, let aX^q be its leading term. Choose an integer k that brackets the positive real-algebraic coefficient a between consecutive powers of2. If a is exactly a power of2 and the lower tail is negative, shift k down by1; otherwise use the ordinary lower bracket. Leading-term comparison gives a unique element w∈P with w≤p<2w. For standard positive p use the usual power-of-two bracket.

If u,v∈P and u≤v, the quotient v/u is again in P: its exponent is positive unless the exponents of u,v coincide, in which case the quotient is a nonnegative integer power of2. Thus the two credited axioms P2-IP and P2-Div hold, and M models the reduct theory TEIP.

## 2. Standard divisibility is controlled by the constant coefficient

For a standard positive integer n and p∈I,

n divides p in I iff n divides the integer constant coefficient a_0.

Indeed, the quotient p/n has allowed real-algebraic coefficients at every positive exponent; its only possible obstruction to membership in I is the constant coefficient a_0/n. The same equivalence holds in M for positive p, since the quotient then remains positive.

Let Pow2(u) be the paper's oddless formula: every divisor d of u is either1 or even. We claim

Pow2(M)={2^k:k∈N},

where the set on the right consists only of standard elements.

For a positive nonstandard p, if a_0=0, then3 divides p, so p is not oddless. If a_0≠0, write a_0=2^e b with b an odd nonzero integer and e standard. Then d=p/2^e belongs to M, is nonstandard and hence greater than1, and has odd constant coefficient b. Therefore d is an odd divisor of p, again refuting oddlessness. This argument also covers negative constant coefficients: the positive leading term makes p and d positive, and parity of b is unaffected by its sign.

Zero is not oddless because3 divides0. For a positive standard integer u, every positive divisor in M is at most u and therefore standard; the finite elements of M are exactly the standard nonnegative integers. Hence its oddlessness is exactly its ordinary number-theoretic oddlessness, which means it is a power of2. This proves the claim.

## 3. Consequences for the proposed finite replacement

Taking x=X, there is no oddless u with u≤X<2u, nor any oddless u>X. Thus

M models TEIP + not(Pow2-IP) + not(Pow2-Cof).

It does satisfy Pow2-Div, because its oddless elements are the standard powers of2 and their divisibility is linearly ordered. In particular, TEIP does not imply cofinality or interval density of the internally defined oddless elements.

The credited Theorem6.2/Corollary6.3 of the current paper give the finite relative upper bound

TEIP_Pow2 = IOpen + Pow2-IP + Pow2-Div,

which contains TEIP. The present model shows the inclusion is strict. This is a separation in the original language, not merely the known nonuniqueness of a predicate expansion. It blocks the candidate answer “replace the extra predicate by the oddless formula and use its two axioms.”

## 4. Exact limit of the deduction

A strict finite upper bound does not imply that the smaller theory lacks some different finite axiomatization. The model above satisfies every finite-round TEIP game axiom, so it cannot witness a strict hierarchy of those closed axioms. The next construction route must leave this class of models or find a different obstruction.

`verify_turn2.py` checks exact divisor certificates for rational-coefficient sample polynomials and the standard cases. These samples lie inside the credited model; their finite verification neither establishes IOpen nor exhausts its nonstandard universe.
