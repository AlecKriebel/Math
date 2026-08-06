# Failure of a naive fixed quadratic correction

For the face-stress cycle `0 -> A+B -> B -> 0`, a tempting correction is

    V_c(A,B)=(A+B)^2-cAB.

At `(n,0)`, the birth increment has leading coefficient `(4-c)n`, so
negative leading drift requires `c>4`.  But global coercivity on the positive
quadrant requires `c<4`, because `AB <= (A+B)^2/4`.  Thus this particular
quadratic family cannot simultaneously be coercive and repair the boundary
drift.
