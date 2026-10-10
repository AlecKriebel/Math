# Turn 5: exact finite search, qualitative stability and the compactness boundary

Fifth and final substantive author turn. The full arbitrary-support conjecture remains unresolved. This turn tests whether finite algebraic search or limits of nearly admissible products can settle it, and records the exact obstruction to that inference.

## 1. Each degree is a finite algebraic problem

Fix a Boolean polynomial C of degree D with C(0)=1. Write its distinct complex roots as rho_1,…,rho_s, of multiplicities e_1,…,e_s. Every monic divisor A is specified by choosing, for each root, a multiplicity f_j∈{0,…,e_j}; its cofactor B is then determined. There are

product_j (e_j+1) ≤ product_j 2^(e_j) = 2^D

such ordered divisor/cofactor pairs. Repeated roots do not create a continuous family. For prescribed degrees, the count is at most the corresponding root-submultiset count, and the same bound still applies.

All these coefficients are algebraic. In principle one can compute the algebraic roots, enumerate the submultisets, form the factors and decide exactly whether coefficients are real and nonnegative. A real factor corresponds to a submultiset closed under complex conjugation, not necessarily to a union of rational irreducible factors. Enumerating only rational factors would miss precisely the irrational possibilities left by Turn 1.

For D≥1 there are 2^(D−1) Boolean polynomials with both endpoints 1, so at most 2^(2D−1) monic ordered divisor/cofactor candidates at that degree before sign and constant-term restrictions. This proves finite decidability at each degree and a semidecision procedure for a counterexample by scanning degrees. No algorithm implementation, practical complexity bound or stopping degree for a proof of the universal conjecture is asserted.

Finite checking therefore has the correct logical shape: it can certify a bounded-degree theorem or find an exact finite counterexample. Without a uniform mathematical argument, exhausting more degrees never proves that every degree is fair.

## 2. A rigorous fixed-degree compactness statement

Fix degrees m,n and the compact cube K of coefficient pairs A,B whose constant and leading coefficients are 1 and whose remaining coefficients are in [0,1]. This is a prescribed normalized coefficient domain; it is not asserted to describe every approximate probability factorization automatically.

For a fixed target C define E_C(A,B)=max_k |[x^k](AB−C)|. It is continuous on K. Its exact zero set Z_C is finite by Section 1, possibly empty. For any eta>0, there is delta>0 such that

E_C(A,B)<delta implies that (A,B) is within eta of Z_C in coefficient sup norm.

If Z_C is empty, the assertion means that sufficiently small residual is impossible. Proof: on the compact set of points at distance at least eta from Z_C, the continuous positive residual attains a strictly positive minimum. If this compact set is empty the assertion is immediate. This gives no explicit value or degree-uniform bound for delta.

When C is a fixed palindromic Boolean polynomial, Turn 3's credited coefficient proof makes every point of Z_C a Boolean factorization. Thus near factorizations in the stated compact cube are qualitatively close to exact fair factors. The same conclusion holds for any fixed C already known to be fair. For an arbitrary C, replacing Z_C by the set of fair factors would assume the conjecture for that C.

Conversely, at fixed m,n, a sequence in K with residual tending to zero and distance at least a fixed eta>0 from every Boolean factor pair would have a convergent subsequence giving an exact unfair factorization. Both the degree bound and the non-Boolean separation are essential. A few small numerical residuals without a certified limit or exact algebraic sign test do not supply this argument.

## 3. Why unbounded-degree limits do not finish the proof

Compactness at one degree does not furnish compactness in a fixed finite-dimensional space when degrees grow. A coordinatewise limit may be an infinite formal power series and need not correspond to a finite probability distribution or preserve a leading coefficient.

The already-known formal-power-series example, credited to Will Sawin in the primary discussion and recorded by Ghidelli, shows the danger sharply. Put

H(x)=(1−x)^(-1/2)=sum_(k≥0) binom(2k,k) x^k / 4^k.

Every coefficient is positive, and coefficients after the constant term lie strictly between 0 and 1, yet H(x)^2=1/(1−x), whose coefficients are all 1. This is an identity of formal power series; it is not a finite counterexample or a probability law uniform on the infinite integers. The coefficients are rational, illustrating exactly why the monic finite-polynomial hypothesis in Turn 1 cannot be dropped.

For the finite truncation H_N, its square agrees with 1/(1−x) through degree N, but its coefficient at degree 2N is (binom(2N,N)/4^N)^2∈(0,1) for N≥1. Hence arbitrarily long admissible prefixes do not extend automatically to a finite Boolean product.

The September 2026 epsilon-unfair result must likewise be kept separate: it explicitly allows a negative quotient coefficient −t_n. The theorem is useful information about approximate signed factors, but those factors violate the exact nonnegativity required here. No limit argument in this packet repairs that violation while preserving every finite hypothesis.

## 4. Final sharp gap

Five approaches have produced arithmetic restrictions, support certificates, an outer-reflection criterion, an explicit residual-system identity and exact finite-search/stability statements. They provide neither a universal proof nor an admissible counterexample.

A decisive next result must either exclude all remaining asymmetric irrational algebraic factorizations in arbitrary degree, or exhibit a finite exact monic factorization with every coefficient nonnegative and at least one non-Boolean coefficient. Proving an a priori degree bound or a uniform obstruction theorem would also close the logical gap, but neither has been established. Bounded scans, conjugate positivity assumptions, signed near-counterexamples and infinite series do not substitute for that missing step.

Author search stops here at five turns. Independent review is required for every scoped claim and the final unsolved disposition. No novelty certification is asserted.
