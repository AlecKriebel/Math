# Independent audit of the controlled affine obstruction

Problem 4600045 / AMR-045-0045. Audit date: 2026-10-10 UTC.

## Verdict and exact binding

**ACCEPT AS A CORRECT PARTIAL EXCLUSION THEOREM. DO NOT ACCEPT AS A SOLUTION OF THE ORIGINAL EXISTENCE PROBLEM.**

This proof-only edition retains the acceptance of the mathematical text distributed in `PROOF.md`, 11,894 bytes, SHA-256 `d760fc625e018bbce09151d2bcc8cf187686e59c9decd5dfb931113367cc1870`. All theorem statements and proof passages are unchanged from the audited text; the editorial boundary is recorded in `PROVENANCE.md`. The theorem, its exact finite-period count, its multiplicity bound, and both sharper special cases withstand independent reconstruction. The proof is self-contained.

Two small corrections were made during review: one missing TeX backslash and a clarification of the literal scope of the Boyle–Lee citation. Neither changed the theorem or its proof. The complete repair history is recorded separately in `SCOPE_REPAIR_LEDGER.md`.

The accepted result rules out every map in the stated controlled-affine family as a strict-growth example. It supplies no surjective cellular automaton with growth less than its alphabet size, no upper bound establishing such an example, and no resolution for arbitrary nonlinear cellular automata. Novelty of the general formula is not certified.

## Original target and source check

The original sources use all positive spatial periods, including divisors of the named period, and the upper exponential limit of the number of jointly periodic points. The target is an example on a full alphabet of size N with strict upper growth below N. These conventions were verified directly in Boyle–Lee, printed pp. 2–3, and Boyle, printed p. 26. The corresponding original PDF pages were visually inspected, not inferred from a database summary.

- Mike Boyle and Bryant Lee, *Jointly Periodic Points in Cellular Automata: Computer Explorations and Conjectures*, author manuscript, https://math.umd.edu/~mboyle/papers/18nov2006.pdf.
- Mike Boyle, *Open Problems in Symbolic Dynamics*, author manuscript, https://www.math.umd.edu/~mboyle/papers/openfinalsub3nov2007.pdf.

For any finite alphabet, J_k is at most N^k. The condition limsup J_k^(1/k) < N is equivalent to the existence of a fixed rho < N with J_k <= rho^k for every sufficiently large k. A strict inequality only along an infinite selected sequence is not enough. Conversely, a selected sequence whose roots approach N proves the full limsup is N. The candidate uses precisely the latter valid implication.

## Independent reconstruction of the proof

### The local map and surjectivity

Let B be a nonempty finite alphabet of size s and K a finite field with q elements and characteristic p. The coefficient functions c and d can inspect any fixed finite set of control coordinates, including negative offsets; they need not be single-site or linear. The local rule

F(a,b)_i = (a_(i+1), b_i + c(sigma^i a)b_(i+1) + d(sigma^i a))

therefore defines a continuous, shift-commuting map on the full (sq)-symbol shift. The case s=1 is included, while q is at least 2, so the alphabet remains nontrivial.

For a prescribed output (u,v), the only possible control preimage is a_i=u_(i-1). Its values fix the entire sequences c_i and d_i. The remaining equations are b_i+c_i b_(i+1)=v_i-d_i. Every finite subsystem is solvable by enclosing its indices in [L,R], choosing b_(R+1), and recursively solving backward through the interval. No division by c_i occurs. Each equation is a cylinder-closed constraint in compact K^Z. The finite-intersection property provides a common solution to the entire system. This proves genuine bi-infinite surjectivity, including zero coefficients and coefficient sequences with arbitrary zero patterns.

This argument does not imply that the restriction to any fixed spatial-period ring is surjective. Indeed, the binary derivative on a power-of-two ring is a counterexample to that stronger statement. The candidate explicitly keeps these notions separate.

### The shift adjustment and possible cocycle error

Write S for simultaneous shift of both tracks and H=S^(-1)F. Since F commutes with S, so does H. On P_k=Fix(S^k), S has finite order dividing k. If F^t x=x, then H^(tk)x=S^(-tk)F^(tk)x=x. If H^t x=x, the same calculation using F=SH gives F^(tk)x=x. Thus the two maps have exactly the same periodic-point set inside P_k.

The direct coordinate calculation gives

H(a,b)_i=(a_i, b_(i-1)+c(sigma^(i-1)a)b_i+d(sigma^(i-1)a)).

This is the crucial indexing point. The coefficient at site i in H is c_(i-1), not c_i. The control word is fixed, so there is no omitted time-dependent coefficient cocycle. Arbitrary finite control memory remains harmless because the entire periodic control configuration is unchanged by H.

For a fixed k-word a, the fibre action is the affine self-map T_a b+e_a of K^k with (T_a b)_i=b_(i-1)+c_(i-1)b_i. Fibres are indexed by words with a fixed origin. Each spatial point is counted once, including words with a smaller least period; dividing by k would be incorrect.

### Periodic points of an affine map

For an arbitrary linear T on K^k, choose m large enough for kernels and images to stabilize. Then K^k=ker(T^m) direct sum im(T^m). The intersection is zero: if x=T^m y and T^m x=0, then y belongs to ker(T^(2m))=ker(T^m), so x=0. Rank-nullity gives the direct sum. Both summands are T-invariant. The first restriction is nilpotent, and the second is an automorphism.

If r is the algebraic multiplicity of zero in the characteristic polynomial, the nilpotent summand has dimension r. Decomposing e accordingly, the nilpotent affine component has one fixed point because I-T is invertible on that summand. Translating by it reduces the map to a nilpotent linear operator, whose only periodic point is zero. On the invertible summand, any affine translate is a permutation of a finite set, so every point is periodic. The product has exactly q^(k-r) periodic points.

This argument works in every characteristic. It neither divides by a period nor assumes the whole affine map has a fixed point. For example, a nonzero translation on an invertible summand can have temporal period p and no fixed point while every point is periodic. Thus the affine term really does disappear from the count, even though it can change orbit lengths and positions.

### Characteristic polynomial and small rings

For k>=2, tI-T_a has diagonal entries t-c_(i-1) and a single cyclic off-diagonal entry -1 in each row. A nonzero determinant term must use either all diagonal entries or the entire cyclic permutation: using one off-diagonal column forces the next row away from its diagonal, and this continues around the cycle. The cyclic term has sign (-1)^(k-1) times product (-1)^k, hence contribution -1. Therefore

Q_a(t)=det(tI-T_a)=product_i(t-c_i)-1.

For k=2 the two matrix entries in each row are distinct, and the formula reads (t-c_1)(t-c_0)-1. For k=1 they overlap: T_a is multiplication by 1+c_0, giving t-(1+c_0)=(t-c_0)-1. These checks also hold in characteristic 2, where minus and plus coincide. Q_a is monic of degree k, so it is never the zero polynomial and its zero multiplicity is always defined.

Applying the affine count to each control word and then the shift equivalence yields exactly J_k(F)=sum_(a in B^k) q^(k-r(a)). No unproved asymptotic or probabilistic step enters this formula.

### Multiplicity estimate over arbitrary finite fields

If one coefficient is zero, Q_a(0)=-1, so r(a)=0. Otherwise a positive multiplicity requires product_i(-c_i)=1. Let U be the distinct nonzero coefficients and n_u their positive integer multiplicities. Put e=min_u v_p(n_u), n_u=p^e m_u, and R(t)=product_u(t-u)^(m_u). Then

Q_a(t)=(R(t)-1)^(p^e).

Since Q_a(0)=0, injectivity of Frobenius in a field implies R(0)=1. If h is the multiplicity of zero in R-1, then r=p^e h.

The rational logarithmic derivative is R'/R=sum_u m_u/(t-u)=A/D, where D=product_u(t-u). At least one m_u is nonzero in characteristic p. Its distinct simple pole has nonzero residue, so the rational function and A are nonzero. The numerator has degree at most |U|-1. At zero, R and D are both units. Consequently ord_0(R')=ord_0(A)<=|U|-1.

A polynomial starting in degree h has a derivative starting in degree at least h-1 whenever that derivative is nonzero. In positive characteristic the leading derivative may vanish, which increases this order rather than reversing the inequality. Thus h-1<=ord_0(R')<=|U|-1, giving h<=|U|<=q-1. Also p^e divides sum_u n_u=k, hence e<=v_p(k). It follows that r<=(q-1)p^(v_p(k)).

This uses characteristic p rather than cardinality q in the valuations. It remains valid over extension fields: residues m_u are taken in the prime subfield, while the coefficient values u range over all q-1 nonzero elements. No identification of F_(p^d) with the residue ring modulo p^d is made.

The q-1 constant cannot be uniformly reduced. An independent check gives a sharp family: in characteristic 2 take each nonzero coefficient once; in odd characteristic take each twice. Since product_(u nonzero)(t-u)=t^(q-1)-1, the resulting Q has zero multiplicity q-1 and k is prime to p. This sharpness observation is supplementary and is not needed for the accepted claim.

### The all-period limsup

For every k prime to p, each fibre contributes at least q^(k-(q-1)), so

J_k(F) >= s^k q^(k-(q-1)).

Taking kth roots along arbitrarily large such k gives a limiting lower bound sq. The universal upper bound (sq)^k then forces the full limsup to equal sq. The lower estimate can have a negative exponent for small k, which merely makes it weaker; it does not invalidate the inequality. The exact formula remains integral.

The multiplicity bound may be of order k along characteristic-power subsequences. The proof does not ignore those periods or claim ordinary convergence in the general case. Full limsup growth only needs the proved complementary sequence of arbitrarily large good periods.

### The two sharper cases

For a nonconstant single-site control coefficient c_0:B->K, M=max_z |c_0^(-1)(z)| is strictly smaller than s. After k-1 symbols are chosen, a zero partial product makes every last symbol yield an invertible fibre. Otherwise exactly one possible field value for the last coefficient is forbidden, with at most M control symbols mapping to that value. At least (s-M)s^(k-1) fibres are therefore wholly periodic. This remains valid at k=1, with the empty partial product equal to 1. It proves the asserted all-k lower bound and ordinary limit sq; d may still have larger range.

If the coefficient is identically zero, T_a is a cyclic permutation, hence every affine fibre is a permutation and J_k=(sq)^k. For a nonzero constant c, let D be the multiplicative order of -c. D divides q-1 and is prime to p. Writing k=p^v m with p not dividing m gives Q=((t-c)^m-1)^(p^v). The inner polynomial vanishes at zero precisely when D divides m, and then its derivative m(-c)^(m-1) is nonzero. Thus r=p^v in those cases and r=0 otherwise.

When r>0, r/k=1/m<=1/D, with equality along k=D p^v. Hence the liminf is s q^(1-1/D), while the full limsup remains sq. The binary derivative example, including k=1 and every power-of-two k, agrees with these formulas. Its sparse subsequence is not a target solution.

## Literature and claim-scope safeguards

Boyle–Lee Proposition 3.4 uses cyclic-alphabet addition. The final candidate correctly limits its literal invocation to the one-track prime-field, zero-affine-term case. Printed pp. 7–8 also discuss the equicontinuity mechanism. The citation is used only for its qualitative full-growth conclusion in that stated class; all exact finite-period estimates accepted here are established by the candidate’s self-contained proof.

No identified Boyle–Fiebig theorem is accepted as a proof dependency. The author’s literature search is bounded; neither this audit nor the candidate establishes the absence of a later result or the publication priority of this obstruction.

## Remaining gap and stopping condition

This attempt has established a correct obstruction and has reached its stated partial outcome. Any further construction must leave, or genuinely extend beyond, the analyzed family and still prove surjectivity and one strict exponential bound for every sufficiently large spatial period. Nonlinear fibre dynamics, other control evolutions, and more general fibre operators are not settled by this proof. Merely applying the same multiplicity argument to those maps without a valid fixed-fibre reduction would be an unsupported transfer.

No mathematical repair remains for the accepted bytes. The original existence problem is not solved by this work.
