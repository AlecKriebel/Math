# A limited kernel bridge, derived independently during priority verification

This is an audit deduction, not a statement that an earlier paper explicitly
printed the entire candidate theorem. It removes one artificial kernel
distinction on a specified intersection of driver classes; it does not remove
the arbitrary-compensator or BGindex2 questions.

Let `g(x)=x_+^alpha f(x)` be a candidate kernel, and put
`g_star(x)=f(0)x_+^alpha exp(-x)`, `r=g-g_star`. At zero,
`f(x)-f(0)exp(-x)=O(x)`, while its derivative is bounded. Thus
`r'(x)=O(x^alpha)` near zero. At infinity, both r and its derivative
decay exponentially up to a polynomial factor. In particular,
`r in L1(R) intersection L2(R)`, `r' in L1(R) intersection L2(R)`,
and `r(0)=0`. Extend r by zero on the negative half-line.

For any driver with the candidate's deterministic quadratic-rate bound K,
the entire two-sided martingale convolution with r has a derivative D in
`L2(P times [0,T])`: isometry gives
`E int_0^T |D_u|^2 du <= KT ||r'||_2^2`.
The kernel identity and stochastic Fubini identify its increments with
integrals of D. There is no endpoint term because `r(0)=0`. Bounded
drift gives a derivative bounded by `B||r'||_1`. Hence this perturbation
has an absolutely continuous version with square-integrable derivative
and its normalized quadratic energy tends to zero with factor
`Delta^(1-2alpha)`. The Euclidean reverse triangle inequality transfers
any existing stable limit of the `g_star` statistic to g, once that
existing statistic is tight.

Apply this to the bounded-adapted-volatility, finite-quadratic-rate
intersection in INITIAL_PRIORITY_RECONSTRUCTION.md. The2016v2/2018
prior theorem covers `g_star` at mesh1/n; the displayed independent
perturbation deduction gives the same fixed-time limit for every candidate
kernel g on this intersection. Thus lack of eventual monotonicity of
`|g'|` is not by itself evidence of a still-unsolved source question.
This argument does not assert all prior heavy-tailed or unbounded-volatility
drivers have these L2 bounds, does not assert an arbitrary-mesh corollary
of the old theorem, and does not establish prior coverage of a general
predictable compensator or BGindex2. Those remain separate questions.

The argument uses only the already independently validated smooth-energy
bound, martingale isometry and stochastic Fubini. It does not invoke the
candidate's complete target convergence to prove a prior implication.
No new proof-attempt turn, candidate edit or provider mutation is made.
