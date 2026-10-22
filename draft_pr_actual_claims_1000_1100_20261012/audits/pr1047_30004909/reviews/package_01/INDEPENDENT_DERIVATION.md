# Independent derivation, frozen before historical comparisons

The claims below were derived after reading the full current TeX and before reading prior audit verdicts or source-comparison reports. They are mathematical deductions, not deductions from a receipt or a PASS label.

## Exact target and quantifiers

Let F(V) consist of nonnegative, monotone, submodular f with f(empty)=0 and all singleton values one. The claimed refutation concerns a single dimension-independent alpha>0 and, for every such f on each finite V, an ordinary **unscaled** matroid rank on exactly V with r(S)/alpha <= f(S) <= alpha r(S) for every S. The original source's separate all-V quantifier must be checked, and the note explicitly treats it as an interpretation. No weighted, scaled, copied-domain, or sum-of-ranks approximant belongs to this target class.

Every nonempty S satisfies 1<=f(S)<=|S|. The upper bound follows by adding elements, using diminishing returns and singleton value one. Hence the free matroid with alpha=n works in fixed nonzero dimension n. Empty V has only the zero functions and causes no obstruction. A universal constant is therefore materially different from a constant for a fixed V.

## Square-root family and exact optimum

For h(k)=sqrt(k), h(0)=0, all increments d_k=1/(sqrt(k+1)+sqrt(k)) decrease. For two sets with intersection size t and difference sizes a,c, the submodularity difference is sum_{j=0}^{a-1}(d_{t+j}-d_{t+c+j})>=0, including a=0, t=0 and containments. The function is normalized and monotone.

The upper singleton comparison 1<=alpha*r({i}) forces every element to be a nonloop and alpha>=1. The total rank R is an integer in [1,n], so a basis B has size and rank R>0. At B, R/alpha<=sqrt(R), so alpha>=sqrt(R) and R<=alpha^2. At V, sqrt(n)<=alpha*R<=alpha^3, so alpha>=n^(1/6). A proposed fixed alpha fails for any integer n>max(1,alpha^6). The universal all-subset quantifier permits the adversarial basis to depend on the proposed matroid. No probabilistic, oracle or computational claim enters this proof.

For U_{R,n}, rank at size k is min(k,R). For 1<=k<=R, r/f=sqrt(k) and f/r=1/sqrt(k); for R<=k<=n, they are R/sqrt(k) and sqrt(k)/R. Thus the largest ratio is max(sqrt(R),sqrt(n)/R). The basis and whole-set necessary inequalities give this same lower bound for every matroid of total rank R. Minimizing over **integer** R=1,...,n proves the exact optimum. At n=m^3, R=m makes both terms sqrt(m); n=1 gives one; n=2 gives sqrt(2), not 2^(1/6). Empty-set ratios are not divided: comparisons are zero on both sides.

## Rational family

For |V|=m^2 and integer m>=1, g(empty)=0 and g(k)=1+(k-1)/m for k>=1. The increments are 1,1/m,1/m,...; hence normalized monotone submodular. Values are rational, and m>=2 includes noninteger values. Equivalently g=(1-1/m)U_1+(1/m)U_{m^2}, with nonnegative coefficients even at m=1.

Again alpha>=1 and R>=1. The basis inequality R/alpha<=(m+R-1)/m gives m<=alpha+alpha(m-1)/R. The whole-set inequality m+1-1/m<=alpha*R implies R>=m/alpha, since m+1-1/m>=m. Therefore alpha(m-1)/R<=alpha^2(m-1)/m<=alpha^2, proving m<=alpha+alpha^2. The positive root bound follows because alpha>0 and x^2+x increases for x>=0. Since alpha>=1, alpha+alpha^2<=2alpha^2, hence alpha>=sqrt(m/2)=n^(1/4)/sqrt(2). No division by m-alpha occurs. At m=1 all deductions remain valid, although the exact optimum is one and the displayed bounds are weaker. Loops, total rank zero and division by empty-set values are excluded by the singleton step.

## Classical decomposition and copied-element check

For h(0)=0 with nonnegative decreasing increments d_i=h(i)-h(i-1), let c_i=d_i-d_{i+1} for i<n and c_n=d_n. The kth increment of sum_i c_i min(k,i) is sum_{i>=k}c_i=d_k. The zero values agree, proving h(k)=sum_i c_i min(k,i), c_i>=0. For h(1)=1, sum_i c_i=1. For n>=2, c_1=2h(1)-h(2). This is a telescoping identity and does not rely on correctness of a printed prior formula.

For g_m, make m copies of each original element, partitioned into m-1 rank-one uniform layers on V and one free layer on V. Their direct sum has, on the union of all copy blocks of S, rank (m-1)min(|S|,1)+|S|=m*g_m(S), also for empty S and m=1. This is a scaled rank on an expanded domain; it is not a rank on V. Proper historical credit requires primary-source checking.

## Conditional broader envelope, not a paper novelty claim

For any normalized monotone concave cardinal h on n>=1, h(k)/k decreases for k>=1. A loopless rank-R matroid forces alpha>=R/h(R) at a basis and alpha>=h(n)/R at V. Uniform rank R attains max(R/h(R),h(n)/R): k/h(k) grows on k<=R, R/h(k) decreases on k>=R, and h(k)/k<=1<=R/h(R) on k<=R. Thus the same integer-rank envelope holds. This independent derivation does not establish historical novelty or priority. The current paper explicitly leaves the history of this generic envelope unresolved and does not claim it as a new theorem.

## Falsifiable remaining checks

Compare source display and admissible-input language in the entire Vegh contribution. Check primary bodies for the cardinality decomposition, structural root-linear output and oracle-hard rank inputs, and copied-domain construction. Inspect every PDF page and all metadata claims. Execute extraction, verifier, builder and mathematics checker, exercise fault controls, and independently check archive bytes/custody. Historical unread-source limits remain limits even if the elementary proof checks out.
