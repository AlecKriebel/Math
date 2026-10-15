# An argument derivative is not a tangent-argument derivative

This is an audit-only nonimplication certificate, not a new support-point theorem and not a scope clearance of an unread paper. Zemyan's 2003 primary publisher abstract positively reports a support omitted arc with a tangent waver; the complete formula/proof remains unread. It may carry additional relevant conclusions. The following certificate only explains why that abstract alone cannot be treated as a negative answer to either question in Problem6.72.

Let r≥1, p=6/5, b(r)=(3/4)r^(−p), and define

    θ(r)=−∫_r^∞ tan(b(s))/s ds,
    w(r)=r exp(iθ(r)).

The integral converges: b decays as r^(−p) and tan b is bounded by a constant times b on [0,3/4]. The curve is real analytic, injective and radially ordered because its modulus is r. It has a finite tip at r=1 and an asymptotic ray with θ→0. It satisfies the necessary strict radial-angle bound |β|<π/4, since π>3 and 0<b≤3/4.

We have θ′=tan(b)/r>0 and

    arg(w′/w)=arg(1/r+iθ′)=b(r).

Thus the continuous radius argument θ is strictly increasing and the signed outward radial angle β=b is strictly decreasing; its ordinary magnitude is also strictly decreasing. Yet the tangent direction φ=arg w′=θ+b has

    φ′(r)=[tan b−p b]/r.

At r=1, b=3/4. The alternating trigonometric series gives sin b≥b−b³/6 and cos b≤1−b²/2+b⁴/24, with cos b>0. Exact arithmetic proves the first bound is larger than (p b) times the second, so tan b>p b and φ′>0. At r=(3/2)^(5/6)>1, b=1/2; sin b≤b and cos b≥1−b²/2 give tan b≤4/7<3/5=p b, so φ′<0. Continuity supplies a tangent waver. Complex conjugation reverses these signs and gives specifically clockwise-to-counterclockwise turning while preserving monotonicity of θ and the signed/unsigned radial angles.

This curve is NOT asserted to be the omitted slit of a support point in S. Increasing modulus, asymptotic direction and the π/4 property are necessary conditions, not a sufficient characterization. The certificate proves that these geometric constraints plus a tangent waver alone do not logically settle the target. Only reading the actual earlier construction can decide whether it additionally supplies nonmonotone θ or β. No historical-firstness or absence of prior resolution follows from this certificate.
