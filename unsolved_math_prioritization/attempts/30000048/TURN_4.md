# Turn 4: two unrestricted SU(3) obstructions

2026-10-02. Fourth substantive author turn for problem 30000048. The original classification remains unresolved. The results below have no highest-weight cutoff within their stated hypotheses, but neither theorem covers an arbitrary S-character. Independent review is pending; historical novelty is not asserted.

## 1. Results and their role

Let chi_(a,b) denote the irreducible SU(3) character with highest weight (a,b), a,b>=0, and set S_(a,b)=|chi_(a,b)|^2. All Haar measures below have mass one.

**Theorem A: the single-irrep affine family.** Let chi be a nontrivial irreducible SU(3) character and c an integer. If 1+c chi is real and nonnegative everywhere, then either c=0, or c=1 and chi=chi_(1,1). The latter function is |chi_(1,0)|^2. All these functions have Haar mean one. Thus the SU(3) instance of the source's subquestion about functions 1+chi has only the standard adjoint example.

**Theorem B: integral convex-square rigidity.** Suppose finitely many real numbers t_i>=0 sum to one. If

    f=sum_i t_i S_(a_i,b_i)

is an integral virtual character of SU(3), then all terms with t_i>0 are the same square function. In particular f is one irreducible square. The t_i need not be rational and the weights (a_i,b_i) are unbounded.

Theorem B rules out constructing a counterexample by a fractional positive average of irreducible squares, even when integer coefficients might appear after tensor-product cancellations. An exploratory search for pairwise norm congruences modulo two up to a+b=50 found no collisions apart from conjugation; Theorem B now excludes this entire mechanism at every weight, without relying on that search.

Theorem A handles an unbounded sparse family. Theorem B handles an unbounded construction family. A general nonnegative virtual character need not have either displayed form. Neither positivity nor Haar mean one has been shown to imply a convex-square decomposition, so this turn does not settle the original source problem even for SU(3).

## 2. Explicit negative witnesses for every higher self-dual character

Complex conjugation interchanges chi_(a,b) and chi_(b,a). If c is nonzero and 1+c chi is real, irreducible-character independence implies chi is self-dual, hence chi=chi_(a,a) for a>=1. Its dimension is (a+1)^3.

If c<0, evaluation at the identity gives 1+c(a+1)^3<0. It remains to consider positive integral c.

Write n=a+1. For

    g_theta=diag(1,e^(i theta),e^(-i theta)),  0<theta<pi,

the Weyl character formula, using (a,a)=a rho, gives

    chi_(a,a)(g_theta)
       = [sin(n theta/2)/sin(theta/2)]^2
           * sin(n theta)/sin(theta).                    (2.1)

Indeed, the three positive-root angles are theta, theta, 2theta, and the numerator Weyl alternant is the denominator alternant with each exponent multiplied by n. Formula (2.1) is valid at the displayed regular elements; no limit at a singular torus point is needed below. Its exact Laurent form is

    chi_(a,a)(1+s^2+s^(-2),1+s^2+s^(-2))
       * (s-s^(-1))^2(s^2-s^(-2))
      = (s^n-s^(-n))^2(s^(2n)-s^(-2n)),                  (2.2)

where the notation on the left means the character's integral polynomial in the fundamental characters u and v. This identity is checked independently for representative n in the executable, while Weyl's formula proves it for every n.

For a>=3, take

    theta=3pi/(2n),  n>=4.

Then sin(n theta/2)^2=1/2 and sin(n theta)=-1, so

    chi_(a,a)(g_theta)
      = -1/[2 sin^2(3pi/(4n)) sin(3pi/(2n))].            (2.3)

Here 0<3pi/(4n)<pi/4 and 0<3pi/(2n)<pi/2. Therefore both sine factors are positive and

    0<2 sin^2(3pi/(4n)) sin(3pi/(2n))<1.

The value in (2.3) is strictly less than -1. This is an exact analytic witness for every a>=3, not a grid or floating-point minimum.

For the remaining a=2, use trace u=v=3/2. It occurs at an actual group element g_theta with cos(theta)=1/4. The exact formula

    chi_(2,2)=u^2v^2-u^3-v^3

gives

    chi_(2,2)(g_theta)=(3/2)^4-2(3/2)^3=-27/16<-1.

Thus for every a>=2 and every positive integer c, 1+c chi_(a,a) takes a negative value.

Finally, chi_(1,1)=|u|^2-1. It has minimum -1, attained at the trace-zero matrix diag(1,omega,omega^2). Hence 1+c chi_(1,1) can be nonnegative for positive integral c only when c=1, and then it equals |u|^2. This proves Theorem A, including all signs of c and all nontrivial irreducibles.

## 3. An exact diagonal tensor-product multiplicity

For n=a+b and 0<=k<=n, let m_k(a,b) be the multiplicity of chi_(k,k) in S_(a,b). We prove

    m_k(a,b)=min(a,b,k,n-k)+1.                            (3.1)

There is no such constituent for k>n. In particular m_n=1 and m_0=1.

We use the classical Littlewood–Richardson rule with the top-to-bottom, right-to-left ballot-word convention. This is a credited tensor-product rule, not a new general theorem. The specific tableau count is supplied completely here.

The SU(3) characters chi_(a,b) and chi_(b,a) are restrictions of the GL(3) Schur characters for

    lambda=(n,b,0),  mu=(n,a,0).

Their product has total polynomial degree 3n. The only GL(3) highest weight that restricts to chi_(k,k) and has this degree is

    nu=(n+k,n,n-k),                                     (3.2)

obtained from (2k,k,0) by a determinant twist n-k. If k>n its last part is negative, so it cannot occur in a polynomial representation. This proves the zero assertion. For 0<=k<=n, the desired multiplicity is the LR coefficient c^nu_(lambda,mu).

The skew diagram nu/lambda has these row intervals:

    row 1: columns n+1,...,n+k                 (k boxes)
    row 2: columns b+1,...,n                   (a boxes)
    row 3: columns 1,...,n-k                   (n-k boxes).

Content mu requires n entries equal to 1 and a entries equal to 2, with no other symbols. The first row must consist entirely of 1s: otherwise its rightmost non-1 would violate the ballot condition before any 1 was read. Let t be the number of 2s in row 2. Weak row increase fixes row 2 as a-t 1s followed by t 2s, and the content then fixes row 3 as

    b-k+t 1s followed by a-t 2s.

All these quantities are nonnegative precisely when

    0<=t<=a,  t>=k-b.

Reading row 2's 2s first requires t<=k. Reading row 3's 2s first imposes the same inequality: the total number of 2s is then a, while the number of 1s read earlier is k+a-t. All subsequent prefixes only add 1s.

There are no overlapping columns between row 1 and row 2 or 3. The only column constraints are between rows 2 and 3, in columns b+1,...,n-k when this interval is nonempty. Under t<=k, row 2's 2s begin strictly after that interval and row 3's 1s end before it. Thus each overlapping column has 1 above 2. Conversely, no further column restriction remains.

Consequently the allowable tableaux are in bijection with the integers

    max(0,k-b)<=t<=min(a,k).

Their number is

    min(a,k)-max(0,k-b)+1
      =min(a,b,k,a+b-k)+1,

which proves (3.1). The formula includes zero-length skew rows, k=0, k=n, and a=0 or b=0.

## 4. Proof of integral convex-square rigidity

Delete zero-weight terms from the asserted finite convex combination. Let

    N=max_i(a_i+b_i).

By (3.1) and its zero extension, the coefficient of chi_(N,N) in f is exactly

    sum_(a_i+b_i=N) t_i.

It is positive and at most one. Since f is an integral virtual character, this coefficient is an integer, hence equals one. Therefore every positive-weight term has a_i+b_i=N. This step rules out mixing different heights, even when all other coefficients are allowed to vary.

Set r_i=min(a_i,b_i), so 0<=r_i<=floor(N/2). For 0<=j<=floor(N/2), (3.1) becomes

    m_j(a_i,b_i)=min(r_i,j)+1.

For j>=1, the difference of the coefficients of chi_(j,j) and chi_(j-1,j-1) in f is therefore

    sum_i t_i [min(r_i,j)-min(r_i,j-1)]
      =sum_(r_i>=j) t_i.                               (4.1)

The left side is an integer. The right side is in [0,1], so it is zero or one. If two positive-weight terms had different r_i, choose j just above the smaller value and no larger than the larger value. The right side would then be strictly between zero and one, a contradiction.

All r_i are equal. Their sums a_i+b_i are already equal to N, so all unordered pairs {a_i,b_i} are equal. The only two possible ordered pairs are conjugate, and their square characters are identical. Thus every positive-weight summand is one fixed S_(a,b), and f equals it. When N=0 or N=1 there is only one unordered pair already, and the conclusion holds without (4.1). This proves Theorem B.

## 5. What this closes, and the exact remaining gap

The arithmetic averaging route is now blocked as a counterexample construction for SU(3). For example, if two different square functions were congruent coefficientwise modulo two, their half-sum would be an integral virtual character, contradicting Theorem B. The same obstruction applies to arbitrary finite averages with real weights, not just pairs or rational weights.

The larger classification does not follow. Pointwise positivity of a virtual character supplies no proven diagonal convex-square decomposition. General real polynomials on the compact trace region may also have mixed terms in a character-square representation, or have no such representation. Neither Theorem A nor B handles those cases. Treating the existence of the required convex-square decomposition as an assumption would simply transfer the unresolved classification to an equivalent unsupported assertion; it is not a completed proof route.

Even the simply connected simple group SU(3) remains unclassified at unrestricted support. No nonnegative mean-one virtual character outside the square family has been found or globally certified. For an affirmative answer to the original target, all other simply connected compact groups and products must also be handled. The SU(2)^r result from turn 1 and the complete SU(3) height-four result from turn 3 remain separate scoped partials.

The final remaining substantive turn should test a materially different mechanism, such as genuinely non-diagonal positive polynomial constructions or another simple rank-two root system. Merely increasing the averaging search bound cannot help after Theorem B.

Original status: **unresolved after 4/5 substantive author turns; one remains**. There is no full candidate proof or counterexample. Repository-required completion estimate remains 30%, subjective and uncalibrated, not a correctness probability.

## 6. Exact controls and sources

Run `python3 verify_turn4.py`. The standard-library program verifies 66 character formulas by independent Weyl alternants, decomposes 66 exact tensor products through a+b<=10, checks every diagonal multiplicity against (3.1), verifies the threshold moments (4.1), checks 11 exact principal Laurent identities, and checks the exceptional a=2 witness -27/16. All 2,265 assertions pass. The arbitrary-weight statements are proved above; their validity is not inferred from the finite bound in these controls.

The earlier modular exploration and its receipt are retained as exploratory history only. No part of either theorem depends on a modular search, numerical sine evaluation, or a finite positivity grid.

Primary background:

- Serre, *Zeros de caracteres*, section 4, Problem 4.6 and its first remark, and section 2 for the Weyl formula: https://ems.press/content/serial-article-files/50890. The exact source problem and the distinction between pointwise nonnegativity and ordinary-character coefficients remain as recorded in SOURCE_GATE.md.
- The Littlewood–Richardson theorem is classical. A primary proof reference is Stembridge, *A Concise Proof of the Littlewood-Richardson Rule*, Electronic Journal of Combinatorics 9 (2002), N5, DOI 10.37236/1666: https://www.combinatorics.org/ojs/index.php/eljc/article/view/v9i1n5.
- A directly accessible primary exposition of the LR rule is Prasad, *An Introduction to Schur Polynomials*, Theorems 19.2 and 19.5, https://arxiv.org/pdf/1802.06073. Its bottom-up reading-word convention with suffix conditions is equivalent to the reversed ballot-word convention used above.

The multiplicity formula and representation-theoretic ingredients may have prior appearances; no claim of historical novelty is made. Separate independent review of these scoped conclusions remains necessary before promoting them as reviewed results.
