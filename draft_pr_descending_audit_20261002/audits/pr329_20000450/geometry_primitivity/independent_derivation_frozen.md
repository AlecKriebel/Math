# Independent primitivity derivation freeze

Native UTC 2026-10-04T10:28:55.383005+00:00. No root new exploratory calculation/addendum read. Existing completed geometry namespace is held unchanged. Reading exposure consists of the original side-product A/B/C already independently reconstructed in the earlier audit and this new narrow task.

Write r=sqrt(5), phi=(1+r)/2, H=5phi+lambda. The reconstructed affine coefficients are A=10X+H, B=-20X^3+2H X^2-5phi^3-2lambda, C=2X^5+H X^4-(5phi^3+2lambda)X^2+phi^5+lambda. A has one simple root X0=-H/10 in characteristic zero. A vertical component can exist only if B(X0)=C(X0)=0, because any common content factor must divide linear A.

At that root,

B(X0)=H^3/25-5phi^3-2lambda=lambda(lambda+5r)(lambda+5(phi+1))/25.

For lambda outside {0,-5r}, the sole possible zero is lambda=-5(phi+1). At this value H=-5 and X0=1/2; B(X0)=0 implies 5phi^3+2lambda=-40X0^3, and hence C(X0)=32X0^5+phi^5+lambda=1+(5phi+3)-5(phi+1)=-1. Thus A,B,C have no common root and gcd=1 for every lambda outside {0,-5r}. This includes lambda=-phi^5 and the allowed cusp -(25+10r)/4. The latter values need no special generic inference: they lie in the proven uniform parameter set.

Gauss's lemma then promotes irreducibility of G in algebraic-closure(F)(X)[Y] to irreducibility in algebraic-closure(F)[X,Y] because G is primitive in Y. For lambda=-phi^5, the existing double-cover proof still gives degree four over the X-line: the conic discriminant is nonzero, and the square-root branch polynomial has exactly one double root plus two distinct odd branch points. Thus its quartic irreducibility also holds there although its normalization has genus zero. For ordinary elliptic parameters, four odd branch points give the same degree-four conclusion.

The degree-five homogeneous pencil has nonzero T=0 term 2X(X^4-10X^2Y^2+5Y^4), so it has no T factor. Any hypothetical nontrivial homogeneous factorization would dehomogenize to a factorization of G. Since G is irreducible, one factor would dehomogenize to a nonzero constant and must be a scalar multiple of a power of T; that is impossible. Hence the entire projective polynomial is absolutely irreducible for every finite characteristic-zero lambda outside {0,-5r}.

Prospective exact checks: rebuild A/B/C from the homogeneous side product, prove B(X0) factorization, verify C=-1 at its only allowed B-zero, compute resultant/shared-root elimination, verify two genuinely bad vertical-content fibres, and inject a factor X-X0 at an allowed parameter to ensure a content detector rejects it. Also use the true allowed parameter -5(phi+1) as a false-content control: A=B=0 at X0 but C=-1, so checking only A and B would give a false conclusion.

Completion estimate 60%; exact remaining gap is independent symbolic verification and portable receipts/inventory, not a new conceptual gap.
