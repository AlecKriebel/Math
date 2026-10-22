# Turn 3: a broad Hahn family is too strong, while a finite-support variant fails IOpen

Status: two explicit construction barriers. No model separating finite TEIP fragments is obtained. Standard real-closed Hahn-field facts are credited dependencies, not new results.

## 1. Full negative truncation rings

Let F be an archimedean real-closed ordered field and G a divisible ordered abelian group. Let K=F((t^G)) be the Hahn field: supports are well ordered in the additive exponent order, and the least exponent determines the leading term and sign. We use the standard theorem that K is real closed under these hypotheses; see Aschenbrenner–van den Dries–van der Hoeven, *Asymptotic Differential Algebra and Model Theory of Transseries*, Corollary3.5.19 and the following Hahn-field example on printed p151.

Put I=Z+F((t^(G<0))), meaning all Hahn series supported in nonpositive exponents whose constant coefficient is an integer. Negative support may be infinite. Sums and products stay in I, since sums of negative exponents are negative and the constant coefficient of a product is the product of its constants. A positive element with a negative leading exponent exceeds every standard integer; otherwise it is a positive integer. Thus I is discretely ordered.

It is an integer part of K. For z∈K, keep its entire negative-exponent part and take an integer floor of its constant coefficient in F. The remainder is theta+epsilon with 0≤theta<1 in F and epsilon infinitesimal of positive valuation. If theta=0 and epsilon<0, subtract1 from the proposed integer part. In every other case no adjustment is needed. The resulting p∈I satisfies p≤z<p+1. The negative-infinitesimal case is included explicitly; truncation alone need not equal the floor. Shepherdson's theorem now gives I_(≥0) models IOpen.

Define

P={2^k t^g:g<0,k∈Z} ∪ {2^k:k∈N}.

Every positive nonstandard element is within a multiplicative factor2 of a member of P, by dyadically bracketing its leading coefficient, with the same equality/tail-sign adjustment as Turn2. The archimedean hypothesis on F is essential for this standard-integer dyadic bracket. Ordered division of two P elements stays in P. Hence P2-IP and P2-Div hold, so I_(≥0) models TEIP.

This is a predicate-theory expansion, not a claim that K itself has an exponential making this I an exponential integer part. The first-order characterization may require an elementary extension.

For nontrivial G, the constant-coefficient divisor proof from Turn2 again shows that the internally oddless elements are exactly standard powers of2 and are not cofinal. Thus varying the rank, size or order type of G within this full-truncation construction cannot create a model of a finite game fragment which fails TEIP: every such model already satisfies the entire theory. For G={0}, the model is the standard nonnegative integers and the noncofinality conclusion is not asserted.

## 2. A tempting finite-support repair breaks the base theory

Take G=Q² with lexicographic order, e1=(1,0), e2=(0,1), so e1 exceeds every standard multiple of e2. Let J be the subring of I containing only finite supports, with the same integer-constant condition. The finite-support version is a natural attempt to retain a simpler ambient ring. It still has the same monomial power predicate, but it already fails a quantifier-free induction consequence.

Consider the positive element

a=t^(-2e1)+t^(-2e1+e2) in J.

In K its positive square root is

h=t^(-e1)(1+t^e2)^(1/2)=Σ_(n≥0) b_n t^(-e1+n e2),

where b_n=binomial(1/2,n). The support is well ordered, every exponent (-1,n) is negative, and every b_n is nonzero. The formal binomial identity proves h²=a. No p∈J is within distance1 of h: p has finite support, so h-p retains a nonzero negative-exponent term. Its leading exponent is therefore negative and |h-p| exceeds every standard integer.

Consequently there is no z∈J_(≥0) satisfying z²≤a<(z+1)². But IOpen proves such an integer-square-root property: if no such z existed, the open formula z²≤a would hold at0 and be preserved by successor, so open induction would imply it for all z, contradicting z=a+1. Therefore J_(≥0) is not a model of IOpen. The monomial predicate still satisfies the interval and ordered-division axioms in J, so even all power-of-two game sentences over a discretely ordered ring do not by themselves recover the omitted open-induction base.

The failure is specific to this nonarchimedean exponent group and finite-support restriction. It does not contradict the credited rational-exponent Puiseux polynomial model in Turn2, where the relevant positive exponent steps are archimedean and a root's negative principal part is finite.

## 3. Outcome of the attempted construction route

The full negative Hahn truncation supplies too much structure: a P2 expansion and all game axioms. The naive higher-rank finite truncation removes too much: it loses open induction itself. These are concrete obstructions to the attempted valuation-based model construction, not an argument that no other construction can separate the fragments.

`verify_turn3.py` checks the exact binomial coefficients and square identities of finite prefixes, lexicographic sign controls, and floor-boundary bookkeeping. It does not prove real closedness or decide any first-order theory.
