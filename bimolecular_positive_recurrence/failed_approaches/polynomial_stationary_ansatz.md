# Failure of the simplest factorial-polynomial stationary ansatz

Writing a candidate stationary measure as

    pi(x)=h(x)/prod_i x_i!

turns stationarity into

    sum_{y->y'} kappa (x)_{y'} h(x+y-y')
      = h(x) sum_{y->y'} kappa (x)_y.

A constant `h` is exactly the product-Poisson/complex-balance case and fails
for arbitrary weakly reversible rate vectors.  Even the calibration network
`0 <-> A` generally needs an exponential factor `h(x)=c^x`, not a fixed
polynomial.  Consequently, a universal finite-degree polynomial numerator
cannot be assumed.
