# Independent source derivation (before earlier reviews)

Recorded after reading all 16 PDF pages of Duren–Leung–Schiffer (DLS), including the publisher wrapper, and all four PDF pages of Zhang–Ma (ZM). All article pages were rendered and visually inspected in full, including equations and references. No earlier review was read before this record.

## Exact scope and mechanism

DLS define the **radial angle** as the outward-oriented signed angle beta = arg(dw/w). It is not the polar argument theta = arg(w), nor the tangent direction phi = arg(dw). Their trajectory equation is Phi(w)(dw/w)^2 > 0, Phi(w)=L(f^2/(f-w)). Thus beta=-arg(Phi)/2 with the branch |beta|<pi/4 in the interior.

The special hypothesis |beta(w0)|=pi/4 is equivalent to Re Phi(w0)=0 and Phi(w0) is nonzero. The normalized Möbius transform ftilde=w0 f/(w0-f) is then a second maximizer for the **same** functional, because f-ftilde=f^2/(f-w0). Its second trajectory equation pulls back to

    [Phi(w)-Phi(w0)](1-w/w0)^(-2)(dw/w)^2 > 0.

Both equations are therefore conditional on exact tip-angle attainment. Rationality of Phi by itself does not supply the second equation. This is the crucial scope boundary.

DLS Theorem 1 (pp.265–267): the two equations and their quotient under exact tip-angle attainment; rational Phi makes the curve algebraic.
DLS Theorem 2 (pp.267–268): point evaluation f(xi), xi nonzero, cannot attain |beta(w0)|=pi/4. Under contrary hypothesis the quotient gives a half-line and the original equation forces a radial ray, contradicting the hypothesis.
DLS Theorem 3 (pp.268–271): every finite coefficient functional sum(lambda_n a_n), with the highest coefficient nonzero, has strict |beta(w0)|<pi/4. Assuming equality yields two equations, an algebraic continuation whose sheets all vanish at z=0, and a unique germ there; the resulting rational coefficient support point is a Koebe rotation, a contradiction.
DLS Theorem 4 (pp.271–272): rational **functions** f in S omitting one arc to infinity omit a half-line (Srebro result quoted, not reproved). This is distinct from rational **type** of L, which only says Phi is rational for each f.
DLS Theorem 5 (pp.272–274): rational-type L plus no double zeros of Phi, plus exact tip-angle attainment, forces a half-line. Proof centers continuation at the finite tip z0; the only unexcluded alternative sheet is a double zero of Phi away from w0. Remark that this zero restriction is probably unnecessary is a conjectural extension.
DLS §7 (pp.274–275): derivative evaluation e^(-i alpha) f'(xi) has Phi=e^(-i alpha) BC(B-2w)/(w-B)^2 and no double zeros. Equality can occur only for the previously identified half-line derivative-angle extremum. No bent equality example is constructed.
DLS Theorem 6 (pp.275–277): for arbitrary L, exact tip-angle attainment confines the slit to the quarter-plane from w0 between directions w0 and ±i w0. Its bisector is the tip tangent and is parallel to the asymptotic ray. The concluding suggestion that all equality slits are half-lines is not a theorem in this source.

ZM (pp.598–601) prove DLS Theorem 5 without the double-zero restriction, retaining rational-type L and exact tip-angle attainment. They instead center continuation at the preimage z1 of infinity and put u=1/w, P(u)=Phi(1/u). The pulled-back equations yield

    P(u)(u'/u)^2=z^(-2)Q(z),
    [P(u)-P(u0)](1-u0/u)^(-2)(u'/u)^2=z^(-2)R(z),
    [P(u)-P(u0)]u^2 / ((u-u0)^2 P(u))=R(z)/Q(z).

Q is nonzero at z1 and R has a double zero there. All continuation sheets must have u(z1)=0: a pole forces P(infinity)=0 but makes the second equation have order -2 instead of +2; at a finite nonzero value unequal u0, zero/nonzero and pole cases give inconsistent orders; at u0 the nonvanishing derivative P'(u0) gives incompatible orders. Since P has a simple zero at u=0 and P(u0)≠0, the quotient has a nonzero linear term at 0 and hence a unique local germ u=c(z-z1)^2+... . A monodromy argument produces a rational function, and DLS Theorem 4 yields a half-line. ZM has no additional construction, numerical example, general monotonicity theorem, or nonmonotonicity counterexample. Its references are just Duren's book and DLS.

## Independent implications for the two monotonicity questions

Let w(r)=r exp(i theta(r)) on an actual omitted slit oriented toward infinity, r increasing. Then w_r/w=1/r+i theta_r and

    beta=arctan(r theta_r),    theta_r=tan(beta)/r.

Polar monotonicity is a sign question for beta. Radial-angle monotonicity is a question about beta_r. An upper bound |beta|≤pi/4 supplies neither. The trajectory equation additionally gives

    beta_r=-(1/2) Im[(Phi'(w)/Phi(w))w_r],

which contains no automatic one-sided derivative inequality.

For every half-line w(t)=a+bt, t≥0, rotate b to be positive real and write a/b=x+iy. With increasing modulus and support-point bound the tip has x>0 and |y|≤x. Then

    theta_t= -y / ((x+t)^2+y^2),
    beta=-arg(x+t+iy),
    beta_t= y / ((x+t)^2+y^2).

Thus theta and beta are monotone, beta tends to zero, and |beta| decreases. At the equality tip |y|=x the same conclusions hold. A half-line is therefore not a counterexample to either monotonicity question. This calculation includes both signs and limiting radial case y=0.

The DLS/ZM equality mechanism is a second-maximizer Möbius symmetry, followed by paired differential equations and algebraic continuation. No source proof uses a small perturbation of a coefficient extremum to create an interior sign reversal or a radial-angle turning point. Nothing yet supports a universal priority clearance; the full 2014 commentary has not been read and cannot be assumed to repeat DLS.


## Adversarial correction to the ZM proof summary

The preceding paragraph describes the source's stated elimination argument; inspection of its orders reveals an omitted case. In its (9) with P(omega) nonzero (the authors' m=0 case), the second equation does **not** necessarily have order 2(alpha-1): P(omega) may equal P(u0). If P(u)-P(u0) vanishes to order n at omega, the second order is n alpha+2(alpha-1), while the first forces alpha=1. The second equation then permits n=2, exactly its required order 2 at z1. The displayed argument has not eliminated this branch. This is a gap in this printed proof, not a counterexample to the theorem. Q/R positivity and global rational-type/support conditions might rule it out, but the source does not supply that additional argument and the local-order proof alone does not do so. No universal theorem invalidity is claimed.
