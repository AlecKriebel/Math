# Uniform primitivity and projective irreducibility addendum

Prepared for root external reading/replay. This narrow addendum supplies the content step missing from the transition between function-field and whole-plane irreducibility. It does not reopen the held geometry audit or grant publication clearance. No root new exploratory calculation or addendum was read before the independent derivation freeze at 2026-10-04T10:28:55.383005+00:00, and none has since been read.

Let F be any characteristic-zero field containing a chosen r with r^2=5, let phi=(1+r)/2, and let lambda be any finite element of F. All irreducibility assertions below are over the algebraic closure of F, so they survive arbitrary characteristic-zero base change. Put H=5phi+lambda. The independently reconstructed affine side-product pencil is

G=A(X)Y^4+B(X)Y^2+C(X),

A=10X+H,

B=-20X^3+2H X^2-5phi^3-2lambda,

C=2X^5+H X^4-(5phi^3+2lambda)X^2+phi^5+lambda.

**Uniform content proof.** Any common nonconstant factor of A,B,C over the algebraic closure must vanish at A's unique root X0=-H/10. Using phi^2=phi+1 and r=2phi-1 gives the exact identity

B(X0)=lambda(lambda+5r)(lambda+5(phi+1))/25.

Suppose lambda is outside {0,-5r}. The only remaining possibility for B(X0)=0 is lambda=-5(phi+1). Then H=-5, X0=1/2, and

C(X0)=1+phi^5-5(phi+1)=-1,

because phi^5=5phi+3. Thus A,B,C have no common root. Their gcd is 1 over the algebraic closure: G is primitive as a polynomial in Y over the polynomial ring in X. The argument is uniform, including lambda=-phi^5 and the allowed cusp lambda=-(25+10r)/4. An independent elimination check gives monic gcd in lambda of resultant_X(A,B) and resultant_X(A,C) exactly lambda(lambda+5r), corroborating the complete parameter set.

**From the quartic field to the whole affine plane.** In the independently verified conic reduction, lambda outside {0,-5r} makes the quadratic equation for Y^2 a genuine degree-two extension of the X-line: its discriminant differs by a square factor from a quadratic with discriminant 64lambda(lambda+5r). The conic is rational. Over its function field, the equation for the remaining Y square root differs by nonzero squares from F(s-alpha*lambda)/s. Its numerator has three distinct roots and its value at s=0 is nonzero outside {0,-5r,-phi^5}; hence it is nonsquare and the full field has degree four over the X-line. At lambda=-phi^5 the numerator instead has exactly one double root and one further simple root, while s=0 remains distinct. Those two odd-valuation points again make it nonsquare, so the same degree-four irreducibility holds there. Therefore G is irreducible in the polynomial ring over the rational-function field in X for every lambda outside {0,-5r}. The cusp value needs no separate exclusion. Gauss's lemma, together with the just-proved primitivity, now makes G irreducible in the whole two-variable affine polynomial ring over the algebraic closure. In particular, no vertical component was silently lost by passage to the X function field.

**Projective completion.** The homogeneous pencil is exactly its degree-five homogenization

Ph=T^5 G(X/T,Y/T)=P+lambda*T*(X^2+Y^2-T^2)^2.

Its infinity restriction is

Ph(X,Y,0)=2X(X^4-10X^2Y^2+5Y^4),

which is not the zero polynomial; therefore T does not divide Ph. If Ph had a nontrivial homogeneous factorization, dehomogenization at T=1 would factor the irreducible G. One factor would therefore dehomogenize to a nonzero constant. A homogeneous polynomial with constant dehomogenization is a scalar times a power of T, contradicting the absence of a T factor. Thus the full projective plane polynomial is absolutely irreducible at every finite characteristic-zero lambda outside {0,-5r}, including the genus-zero center specialization and elliptic cusp specialization.

## Exact checker and controls

The portable, main-guarded `verify_primitivity.py` requires only SymPy 1.14.0 and uses exact arithmetic over Q(sqrt(5)). It reconstructs A/B/C from the side product, checks the root factor and C=-1, independently checks the resultant gcd, verifies the actual bad vertical factors, checks the center/cusp specializations, and checks exact degree-five homogenization with nonzero infinity restriction. `run_receipt.py` retains native UTC, exit code, exact script hash and full stdout/stderr. It invokes Python with `-B` to avoid cache writes in the held runtime.

The successful computation ran natively from 2026-10-04T10:31:19.926336+00:00 to 2026-10-04T10:31:20.567053+00:00, exit 0 and empty stderr. Eighteen exact identity assertions passed, along with content-degree and infinity controls. Meaningful negative controls rejected (a) falsely inferring common content from A and B alone at the allowed parameter -5(phi+1), (b) declaring an artificially injected vertical factor primitive, and (c) declaring an artificially T-multiplied homogeneous polynomial free of a T factor. These controls do not modify the candidate or held geometry files.

Two earlier attempts failed at a local check-counter scope bug introduced by wrapping the script in its main guard. Their complete exact script versions, full outputs and receipts are retained as v1/v2; neither is evidence for the result. The corrected final run completed. No installation, Git/API write, source namespace mutation, outreach or publication action occurred.

Strongest verified result: the affine polynomial is primitive uniformly outside the two line-union parameters, and the irreducible quartic function field promotes to absolute irreducibility of the entire projective plane polynomial. Exact remaining mathematical gap in this narrow addendum: none identified. Completion estimate 98%, with root external reading/replay and closure pending. The namespace is held stable after its inventory; it is not self-sealed or a full-preprint clearance.
