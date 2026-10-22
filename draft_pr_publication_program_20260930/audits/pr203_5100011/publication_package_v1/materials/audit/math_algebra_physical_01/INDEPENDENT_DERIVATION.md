# Direct definitions and exact four-period result

Prepared independently before original proof/code review. Numerical diagnostic uses no elliptic-function orbit construction.

For cyclic vertices P_i and nonzero side vector v_i=P_{i+1}-P_i, the perpendicular foot is F_i=P_i+((M-P_i)·v_i)/(v_i·v_i) v_i. This formula projects to the complete original side line and remains valid outside its segment. Signed area is one half the cyclic cross-product sum. If the side line has unit normal n_i and equation n_i·X=h_i, then F_i=M+(h_i-n_i·M)n_i. Translating all feet by -M gives

B(M)=1/2 sum_i (h_i-n_i·M)(h_{i+1}-n_{i+1}·M) det(n_i,n_{i+1}).

Thus B is a real quadratic polynomial of M, with no division by B. Negative and zero values require no exceptional convention. Reversing the vertex list reverses both signed areas and preserves their product. Repeating a list r times multiplies each area by r and their product by r²; this alone establishes no phase invariance for an excluded primitive orbit.

## Physical generator

The caustic has axes c_a=sqrt(a²-lambda), c_b=sqrt(b²-lambda), 0<lambda<b². For a boundary point P, put w=(P_x/c_a,P_y/c_b), r²=w·w>1. Its positive tangent contact is

T=diag(c_a,c_b)[w+sqrt(r²-1) Jw]/r²,

where J rotates counterclockwise by pi/2. Then T lies on the caustic, and (T-P) is perpendicular to its normal. Put v=T-P. The second intersection with the outer ellipse is Q=P+tau v, where

tau=-2(P_x v_x/a²+P_y v_y/b²)/(v_x²/a²+v_y²/b²).

The code checks tau>1, forward orientation, both conics, caustic tangency and the usual unit-velocity reflection formula at every vertex. A closure caustic is obtained by monotone bisection on accumulated boundary angle for fixed N and coprime winding w. This last monotonicity is used as a numerical root finder, not asserted here as a new theorem. Closure, least-period separation, and winding are separately checked.

## Exact N=4 reconstruction

Let x²+y²=1, a>b>0, D=sqrt(b⁴x²+a⁴y²)>0 and

P=(ax,by), Q=(-a³y/D,b³x/D).

The ordered quadrilateral is P,Q,-P,-Q. The caustic parameter is lambda_4=a²b²/(a²+b²), strictly between 0 and b². The independent exact reduction verifies Q lies on the outer ellipse and both distinct side lines are tangent to that caustic. Since the caustic lies strictly inside the outer ellipse, each contact is strictly inside the chord. The quadrilateral is nondegenerate because det(P,Q)=ab(b²x²+a²y²)/D>0.

At P, a positive boundary tangent is t=(-ay,bx). Direct calculation gives t·(Q-P)=D+(a²-b²)xy and t·(P+Q)=D-(a²-b²)xy. Both are positive because

D²-(a²-b²)²x²y²=(b²x²+a²y²)²>0.

The exact polynomial check verifies

[t·(Q-P)]² |P+Q|² = [t·(P+Q)]² |Q-P|².

The positive signs remove the square ambiguity, proving equality of the unit-velocity tangential components. Convexity gives opposite normal components, hence reflection. The same formula maps Q to -P: the new D equals a²b²/D, so the argument applies at each vertex. The four vertices are distinct and no period smaller than four occurs.

For any parallelogram with four side lines (n_0,h_0),(n_1,h_1),(-n_0,h_0),(-n_1,h_1), the foot-area identity reduces exactly to

B(M)=2 h_0 h_1 det(n_0,n_1)/(|n_0|² |n_1|²),

independent of every finite real M, including feet outside segments. With d=det(P,Q), L_-²=|P-Q|², L_+²=|P+Q|², this gives A=2d and B=4d³/(L_-² L_+²). The exact reduction verifies

d⁴(a²+b²)² = a⁴b⁴ L_-² L_+²,

and therefore

A B(M)=8 a⁴ b⁴/(a²+b²)².

This is an independently checked exact N=4 result for the displayed family. It does not prove the universal target for every multiple of four. Formula signs above are positive in the chosen orientation; reversal makes A and B negative and leaves the product unchanged. In particular B does not vanish in this N=4 family for any M. Zero/negative pedals at other eligible periods must be checked separately.
