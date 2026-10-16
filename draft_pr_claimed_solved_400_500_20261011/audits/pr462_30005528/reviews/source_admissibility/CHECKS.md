# Checkable independent verification

Reviewer: /root/pr462_source_admissibility
Frozen head: 3d5701d67e18745715d384c3db3fbee588b42a98
Purpose: adversarial verification of the supplied construction, with zero original proof-search attempts.

## Admissibility and closedness

Use alpha=sqrt(2), Sigma=S^1 x [0,1], s(z,t)=1+t, and F(z,t)=(exp(2 pi i(alpha+t))z,t). The displayed formula maps Sigma to itself because multiplying by a unit complex number preserves |z|=1 and the second coordinate stays in [0,1]. The cylinder is compact, connected, metric, and infinite. The size is continuous, finite, and at least 1, including both boundary circles. The inverse obtained by replacing the exponential's exponent with its negative is defined on the entire cylinder and is continuous.

The tile set T={(x,F(x)):x in Sigma} is compact as the image of compact Sigma under a continuous map into Sigma x Sigma. This product is Hausdorff, so T is closed. Equivalently, if x_j->x and F(x_j)->y, continuity gives y=F(x); no additional limiting edge is missing. In particular, closing the relation cannot create extra bottom-circle cycles.

## Exhaustiveness of legal sequences and the source average

Given any legal tile sequence with a_1=x, every legal edge has the unique form [a_i,F(a_i)]. Thus b_i=F(a_i), and matching forces a_(i+1)=F(a_i). Induction gives a_i=F^(i-1)(x), b_i=F^i(x). This covers every legal infinite sequence; there is no switching between heights, hidden extra edge, or sequence without an orbit starting point. Conversely, any starting point has an infinite forward orbit and therefore supplies a legal sequence.

If x=(z,t), the height of every symbol in this orbit is t. Exactly N+1 terms of value 1+t occur in the source numerator, so the normalized quantity is ((N+1)/N)(1+t). Its ordinary limit equals 1+t. The lower bound 1 is attained precisely at t=0, and all points of that circle have legal orbits. This establishes an attained infimum without relying on a compactness/existence theorem.

## Exact periodicity

The only number-theoretic assumption is sqrt(2) being irrational. If sqrt(2)=a/b with positive coprime integers a,b, then a^2=2b^2 makes a even; writing a=2c makes b^2=2c^2 and b even, a contradiction. Thus the exact exclusion of every positive integer period uses a proved elementary fact.

For any positive integer q, direct induction gives F^q(z,t)=(exp(2 pi i q(alpha+t))z,t). A legal tile sequence is period-q exactly when F^q(x)=x: necessity follows by comparing the first coordinate of its first and (q+1)st tiles; sufficiency follows by iterating the equality. Because every z on S^1 is nonzero, equality is equivalent to exp(2 pi i q(alpha+t))=1, hence q(alpha+t) is an integer. This is equivalent to alpha+t being rational.

At t=0 and t=1 the angle is irrational, because adding an integer preserves irrationality. No special phase z, including z=1 or z=-1, can evade the nonzero cancellation. Any periodic height is strictly between 0 and 1 and has size 1+t>1. The cylinder does not include z=0; that fixed-point failure mode is excluded by the definition of S^1. A repetition of sizes alone is not a repetition of the tiles; the source defines the sequence of ordered tiles.

For an eventually periodic orbit, F^(m+q)(x)=F^m(x) for some m>=0,q>=1. Applying F^(-m), justified by the displayed global inverse, yields F^q(x)=x. Thus the minimizing bottom-circle orbits are not eventually periodic either.

## Density, nonvacuity, and limits

Rational angles are dense in [alpha,alpha+1]. Subtracting alpha gives a dense set of permitted periodic heights in [0,1]; each such height carries a whole periodic circle. Any nonempty product-open neighborhood meets one of these circles, including neighborhoods of either boundary circle. This proves density in the product topology.

For alpha=sqrt(2), let m_n=floor(n sqrt(2))+1. Irrationality gives 0<m_n-n sqrt(2)<1. Therefore t_n=m_n/n-sqrt(2) is in (0,1/n), lies in the alphabet, and tends to 0. At this height the rotation is rational m_n/n, whose least positive return is q_n=n/gcd(m_n,n). At n=1 the height 2-sqrt(2) gives genuine period-one tiles, so exclusion of periodic minimizers is nonvacuous. A fixed z at heights t_n converges to (z,0); its successive tiles converge to the bottom irrational orbit. Each individual bounded-period set is closed, but their infinite union need not be closed. Compactness alone consequently does not supply a periodic limit.

## Bounded-period gap

For a periodic orbit with least period q<=Q, write alpha+t=p/q in lowest terms. With alpha=sqrt(2), r=p/q lies in (sqrt(2),sqrt(2)+1), so p,q are positive integers and p^2-2q^2 is a positive integer. Algebra gives

    t = (p^2-2q^2) / [q^2(r+sqrt(2))]
      >= 1 / [(2sqrt(2)+1)Q^2].

The inequality uses both q<=Q and r<=sqrt(2)+1; all denominators are positive. It holds for Q>=1, including the period-one competitor. Periodic averages approaching 1 therefore require least periods exceeding every fixed bound. No empirical approximation or unproved Diophantine estimate is used.

## Planar coordinates

H(z,t)=(1+t)z maps the cylinder bijectively to {u:1<=|u|<=2}. Its inverse H^(-1)(u)=(u/|u|,|u|-1) is continuous because |u|>=1. In these coordinates the size is |u| and the conjugated successor is exp(2 pi i(sqrt(2)+|u|-1))u, exactly as stated in the frozen proof. Positivity and all symbolic claims persist. This realizes an alphabet as a planar annulus, not a one-dimensional packing.

## Finite exact sanity check

Run `python3 verify_exact_competitors.py`. The saved result reports 4,096 competitors with integer-certified floor bounds and least returns, plus 1,260 independently enumerated reduced rational angles for denominators at most 64. The script uses no floating point. These finite checks corroborate formulas only; the preceding deductions establish the universal claims.
