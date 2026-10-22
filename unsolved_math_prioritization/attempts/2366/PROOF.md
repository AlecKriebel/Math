# EP887 / 2366: Czech's five-divisor construction, reconstructed with corrections

This AI-assisted authored reconstruction is unrefereed. Acceptance means an independent internal AI audit of the pinned prior construction. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, priority, or exhaustive current-literature status is claimed. The general EP887 target remains unresolved by this work.

This edition retains the complete self-contained analytical proof, including the finite inequalities needed at small parameters. It is not a computational reproduction package: executable programs, raw census certificates, copied source documents, and images are not distributed. Historical aggregate checks are supporting metadata; the proof does not depend on access to omitted code or census outputs. Edition preparation performed no new proof search, scholarly-source retrieval, or visual source inspection, and did not execute or import the original mathematical checker.

## Verdict and scope

**Accept the core of Theorem 1 in the pinned July 2026 manuscript by M. Czech, with the ancillary corrections below.** An independent exact reconstruction proves that every positive integral solution of

\[
z^2-56x^2=65,\qquad x\ge37,
\]

produces five distinct positive divisors of

\[
n=(x^2-1)(x^2-4)(x^2-16)(x^2-49)
\]

in the strictly open right interval \((\sqrt n,\sqrt n+31n^{1/4})\). Their five positive cofactors lie strictly below \(\sqrt n\), in the corresponding symmetric window. The displayed Pell recurrence supplies infinitely many distinct such integers \(n\). This establishes the restricted lower obstruction **\(K\ge5\)** for the one-sided formulation. It does not establish an upper bound independent of the window constant, nor refute the existence of such an upper bound.

This is an audit of an existing construction, not a novelty claim, formal proof-assistant verification, or assessment of the current global status of EP887. Acceptance does not extend to all historical, bibliographic, speculative, or optimality sentences in the manuscript.

The exact target retains the quantifiers

\[
\exists K\;\forall C>0\;\exists n_0(C)\;\forall n>n_0(C):
\#\{d\mid n:\sqrt n<d<\sqrt n+Cn^{1/4}\}\le K.
\]

The present lower construction only restricts the possible value of \(K\).

## Historically inspected source

M. Czech, *Five divisors near sqrt(n), infinitely often: a Pell-tuned refinement of the Erdős–Rosenfeld construction (Erdős problem #887)*, July 2026.

- Public source: https://czechu.blog/erdos/problems/887/note887.pdf
- PDF: 337,341 bytes; SHA256 `0a20ebeffa5e48201875cbdc62526224a17a54e55ae10e3755364bb334fcf77a`
- All five pages were text-read and visually inspected in the prior audit; they were not reinspected during edition preparation.
- The source identifies its discovery as AI-assisted and offers verification scripts on request. No scripts were requested, and neither supplied author code nor the embedded verifier was executed.
- The original retained download succeeded on 2026-10-10. A fresh web-reader attempt on 2026-10-11 was inaccessible; this audit is tied to the retained, hash-verified bytes, not a claim that the live file was unchanged at that later attempt.

## Independent proof

Put \(w=x^2\), \(r=\sqrt n\), and define the five pairs as follows:

\[
\begin{aligned}
d_1&=x^4-5x^2+4,&e_1&=x^4-65x^2+784,\\
d_2&=x^4-17x^2+16,&e_2&=x^4-53x^2+196,\\
d_3&=x^4-20x^2+64,&e_3&=x^4-50x^2+49,\\
d_4&=x^4-35x^2+90x-56,&e_4&=x^4-35x^2-90x-56,\\
d_5&=x^4-35x^2+56+2xz,&e_5&=x^4-35x^2+56-2xz.
\end{aligned}
\]

### 1. Factorizations and positivity

Multiplying the four quadratic factors gives

\[
n=x^8-70x^6+1113x^4-4180x^2+3136.
\]

The first three factorizations just distribute the four factors into two pairs. For the fourth,

\[
d_4=(x+7)(x-4)(x-2)(x-1),\qquad
 e_4=(x-7)(x+4)(x+2)(x+1).
\]

Every linear factor here is positive when \(x\ge37\). The fifth factorization follows from

\[
(x^4-35x^2+56)^2-n=4x^2(56x^2+65)=4x^2z^2.
\]

Thus all five products are \(d_i e_i=n\). For the fifth pair set \(A=w^2-35w+56\) and \(B=2xz\). We have \(A>0\), \(B>0\), and \(A^2-B^2=n>0\). Hence \(A>B\), which proves \(e_5>0\) as well as \(d_5>0\). Integrality is immediate from the hypotheses.

The differences are

\[
(y_1,y_2,y_3,y_4,y_5)=
(60w-780,36w-180,30w+15,180x,4xz).
\]

They are all positive. Positive factors with \(d_i e_i=n\) and \(d_i>e_i\) satisfy \(d_i>r>e_i\). This proves strict one-sidedness without any floating-point comparisons.

### 2. Distinctness

The pair sums have the form

\[
u_i=d_i+e_i=2x^4-70x^2+\kappa_i,
\qquad (\kappa_1,\ldots,\kappa_5)=(788,212,113,-112,112).
\]

For fixed \(n>0\), a positive pair with a prescribed sum is determined as the two roots of \(T^2-u_iT+n\). The five different sum offsets therefore give five different pairs. Since the chosen \(d_i\) are the larger members, they are pairwise distinct; likewise the five \(e_i\) are distinct. No \(d_i\) can equal an \(e_j\), as they are on opposite sides of \(r\).

The larger root \((u+\sqrt{u^2-4n})/2\) is increasing for \(u>2r\). Since \(\kappa_1\) is largest, \(d_1\) is the largest of the five displayed divisors.

### 3. Exact window certificates

For any positive pair \(d>e\), put \(u=d+e\), \(y=d-e\). Then

\[
u-2r=\frac{y^2}{u+2r}<\frac{y^2}{4r},\qquad
 d-r=\frac{y+u-2r}{2}<\frac y2+\frac{y^2}{8r}.
\]

Since \(w>49\) and not all the factors of \(n\) equal \(w-49\),

\[
r>(w-49)^2,\qquad n^{1/4}>w-49.
\]

Consequently it is sufficient to show

\[
\frac y2+\frac{y^2}{8(w-49)^2}<31(w-49). \tag{A}
\]

For the first pair, clearing the positive denominator in (A) gives

\[
P_1(w)=8w^3-13416w^2+997944w-22294232>0.
\]

Writing \(t=w-1681\), this is

\[
P_1(w)=8t^3+26928t^2+23711616t+1745673984.
\]

Every coefficient is positive, so it holds for every integer \(x\ge41\).

For the other four pairs, \(0<y_i\le36w\) for \(x\ge37\). In particular, \(z^2=56x^2+65<64x^2\), so \(y_5<32w\); also \(180x\le36x^2\), and the two remaining comparisons are immediate. The expression on the left of (A) increases with positive \(y\). Thus it suffices to use \(y=36w\), giving

\[
P_*(w)=104w^3-23640w^2+1440600w-29176952>0.
\]

Writing \(t=w-1369\),

\[
P_*(w)=104t^3+403488t^2+521452512t+224473384944,
\]

which is positive for all \(x\ge37\).

The Pell equation has no solutions with \(38\le x\le40\), as the following exact inequalities show:

\[
284^2<80929<285^2,\quad
291^2<85241<292^2,\quad
299^2<89665<300^2.
\]

The middle entries are respectively \(56x^2+65\) for \(x=38,39,40\). At \(x=37,z=277\),

\[
n=3334958827200,\qquad 1826186^2<n<1826187^2,
\]

so \(\lfloor r\rfloor=1826186\). The already proved ordering gives the maximum \(D=d_1=1867320\). Exact integers give

\[
31^4n-(D-1826186)^4=217020355915097264>0.
\]

Therefore \(D-r<31n^{1/4}\), and the same holds for the other four. This finishes the universal right-window proof. It uses explicit integer certificates rather than rounded numerical roots.

### 4. Cofactors and infinitude

For each pair,

\[
r-e_i=\frac{r(d_i-r)}{d_i}<d_i-r<31n^{1/4}.
\]

All ten displayed divisors are therefore in the symmetric open window.

The map

\[
(x,z)\longmapsto(15x+2z,112x+15z)
\]

preserves \(z^2-56x^2\), since \(15^2-56\cdot2^2=1\) and \(112=56\cdot2\). Starting from \((37,277)\), it preserves positivity and strictly increases \(x\). Every factor \(x^2-a^2\), \(a\in\{1,2,4,7\}\), is positive and strictly increases with \(x\ge37\); their product consequently increases. This yields infinitely many distinct \(n\), not just infinitely many presentations of one integer.

Exhaustion of all Pell orbits is unnecessary. One positive seed and the strictly increasing recurrence already establish the required infinitude.

## Corrections and limits on ancillary claims

### A. The claimed minimality of 31 needs qualification

The identity

\[
n=(x^4-35x^2-56)^2-8100x^2
\]

and positivity of \(x^4-35x^2-56\) show

\[
u_1-2r>900.
\]

Using \((d_1-r)^2=d_1(u_1-2r)\) and \(d_1>r\), this implies

\[
d_1-r>30n^{1/4}.
\]

Thus \(C\le30\) fails for the five displayed divisors, and 31 is the least **integer** constant that works for all five displayed divisors at every admissible parameter. This least-integer claim concerns the five displayed divisors; no complete count of all divisors at a sample parameter is used here.

It is not the least real constant. For example, **\(C=61/2=30.5\) works for every admissible parameter**. Repeating (A) with \(61/2\), the first-pair polynomial, shifted by \(w=4096+t\), is

\[
4t^3+36324t^2+97208748t+63607521132>0.
\]

For the other pairs, using \(y\le36w\) and shifting by \(w=1369+t\), the polynomial is

\[
100t^3+387648t^2+500543712t+215273512944>0.
\]

For completeness, the only admissible parameter below 64 is 37. The necessary finite exclusions can be checked directly, without an omitted scan: for each row below, the stated integer \(k\) satisfies \(k^2<56x^2+65<(k+1)^2\).

| x | k | x | k |
|---:|---:|---:|---:|
| 38 | 284 | 51 | 381 |
| 39 | 291 | 52 | 389 |
| 40 | 299 | 53 | 396 |
| 41 | 306 | 54 | 404 |
| 42 | 314 | 55 | 411 |
| 43 | 321 | 56 | 419 |
| 44 | 329 | 57 | 426 |
| 45 | 336 | 58 | 434 |
| 46 | 344 | 59 | 441 |
| 47 | 351 | 60 | 449 |
| 48 | 359 | 61 | 456 |
| 49 | 366 | 62 | 464 |
| 50 | 374 | 63 | 471 |

These finite inequalities merely expand the accepted small-parameter check into a directly reviewable part of the proof. At \(x=37\), the same maximal divisor satisfies the strict certificate

\[
61^4n-16(D-1826186)^4=369163180726092224>0.
\]

This proves the claimed counterexample to real minimality over the entire admissible family, not only at a few orbit points.

For an eventual rather than all-parameter window statement, the distinction is even sharper: \(n^{1/4}/x^2\to1\) and \((d_1-r)/x^2\to30\), while \(d_1\) is the largest displayed divisor. Hence every fixed \(C>30\) works for all sufficiently large admissible parameters, whereas \(C\le30\) never contains all five. The infimum in that eventual interpretation is 30 and is not attained. This is a clarification of the existing family's constant, not a solution of the unrestricted problem.

### B. Pell necessity is specific to the displayed ansatz

For the fifth pair with prescribed midpoint \(A=x^4-35x^2+56\), integrality requires \(2x\sqrt{56x^2+65}\) to be integral. Since \(x\ne0\), the square root is then rational, and a rational square root of an integer is integral. This proves the exact Pell condition for that ansatz. Irrationality of \(\sqrt{56}\) is not needed for this argument.

It does not show that all other near-square factorizations are impossible off the Pell conic. For example, at \(x=38\), set \(n=4139341315200\) and \(d=2041200\). Direct integer equalities and inequalities give

\[
n=d\cdot2027896,\qquad d^2>n,\qquad
(d^2+n)^2<(2d+31^2)^2n.
\]

The last inequality is exactly the strict \(C=31\) right-window test derived in the verification discussion below. Substitution shows that \(d\) is not one of the first four polynomial divisors, while \(284^2<56\cdot38^2+65<285^2\). Thus an additional divisor can occur away from the Pell condition for the prescribed fifth-pair midpoint. The stronger complete-census count is not asserted in this edition. The manuscript's “only there” sentence must be restricted to its particular fifth-pair formula.

### C. The original question is one-sided

Erdős–Rosenfeld's original Question 1, printed page 358, uses the interval above \(\sqrt n\). Czech's page-2 symmetric restatement is not a literal transcription of that question with the same normalization of \(K\).

Existence of some uniform bound is equivalent between appropriate one-sided and symmetric versions, but the numerical constants need not be the same. Right-side pairing immediately places each cofactor closer to the center; the reverse direction can require increasing the window constant. The present theorem implies at least ten symmetric-window divisors from five right-window divisors. “Equivalently” should not be read as a general same-window counting equivalence. The one-sided obstruction is \(K\ge5\); a symmetric counting convention would produce an obstruction of ten for this construction.

### D. Balanced splits are checked directly; historical sameness is overstated

The first four displayed polynomial factorizations are balanced splits of the linear factors with weights \(\{-7,-4,-2,-1,1,2,4,7\}\); their correctness was proved directly above. This edition does not claim exhaustive balanced-split maximality from an omitted enumeration. No maximality assertion, and no general Fano-plane argument from Erdős–Rosenfeld Proposition 4.3, is needed for acceptance of the five-divisor theorem.

The manuscript's claim that these weights are “exactly” the original consecutive-factor construction in symmetric form should be read as sharing the method, not literal equality or an affine recentering of \(\{0,\ldots,7\}\). The consecutive gaps of the present ordered set are not constant. No fifth balanced split is asserted or needed.

### E. Nonsquareness; complete sample counts are not needed

This edition does not reproduce or assert complete sample divisor counts. Such counts require the omitted enumeration evidence and are unnecessary for the lower bound. The construction proves at least five right-window divisors; no eventual exact-five assertion is made.

The assertion that the admissible family is nonsquare can also be proved. Put \(Q=x^4-35x^2-56\). For \(x\ge64\),

\[
2Q-1-8100x^2=2w^2-8170w-113.
\]

At \(w=4096+t\), this is \(2t^2+8214t+89999>0\). Thus \((Q-1)^2<n<Q^2\). The only smaller admissible parameter is 37, where its exact floor square root verifies nonsquareness. This confirms the specific nonsquare observation without treating Chan's square theorem as a general result.

### F. Statements outside this acceptance

The secondary family in Remark 4 is not specified with a complete proof or seed in the pinned manuscript and is not accepted by this audit. The speculative sixth-pair discussion, generic genus reasoning, suggested implications of Siegel/Bombieri–Lang, and historical priority or record claims are not dependencies of the accepted theorem and are not certified here. In particular, a generic geometric assertion cannot by itself exclude all exceptional or degenerate families.

No cited formal-conjectures pull request was inspected or accepted as formal evidence. No assertion about the literal \(C=1\) transcription is being credited to the \(C=31\) construction.

## Comparison with the earlier sources

- **Erdős–Rosenfeld (1997), Proposition 4.2:** four small factor differences for the product of eight consecutive integers, with a fixed bound involving \(16N_a^{1/4}\). This is not four divisors in the literal open \(C=1\) right window. Converting their difference bound gives an upper-divisor offset of at most \((8+o(1))N_a^{1/4}\). Printed Proposition 4.1 has an ill-formed interval inequality, so it is not silently substituted as a valid literal interval definition.
- **Chan, arXiv:1303.2069v1 (2013):** a sufficiently-large-square theorem with at most five divisors in a symmetric window. The discussion of three one-sided divisors counts the central square root; the displayed Pell construction explicitly lists it. It is not a claim of three divisors strictly above the square root, nor a general-integer upper bound.
- **Chan, arXiv:1406.2230v1 (2014), Theorem 2:** an almost-square result with the hypothesis \(n=(N-a)(N+b)\), \(0\le a\le b\le\exp((\log n)^{2/7})\), and symmetric width \(n^{1/4}(\log n)^{1/14}\), giving at most 18 divisors for sufficiently large \(n\). The plus sign and the almost-square hypothesis are essential. This audit checked the statement and its role; it does not independently accept the entire chain of Turk-dependent upper-bound arguments.

The accepted construction is elementary after its formulas are given. It requires no cited upper-bound theorem, no general Pell existence theorem, no general maximal-split theorem, and no author-supplied computational output.

## Historical verification and exact finite-test logic

The historical independently authored standard-library checker used integer arithmetic and polynomial coefficient convolution. Its recorded coverage included exact identities, universal positive-coefficient window bounds, positive-factor and distinctness checks, the Pell map, small parameters, finite orbit samples, and two different exact census methods at small instances. Code and detailed census records are omitted. The original audit recorded 228 checks and 14 negative controls in each mode; VERIFICATION.json records their byte identities and the reproduction boundary, without asserting unprovided sample counts.

For a rational constant \(C=a/b>0\), exact right-window membership for positive \(d>\sqrt n\) is equivalent to

\[
b^4(d^2+n)^2<(2db^2+a^2)^2 n.
\]

Indeed, both sides of \(b(d-\sqrt n)<a n^{1/4}\) are positive. Squaring and rearranging gives \(b^2(d^2+n)<(2db^2+a^2)\sqrt n\), whose two sides are also positive; a second squaring gives the displayed inequality, and both steps reverse. The strict inequality and the separately checked side condition protect both endpoints. A complete census can enumerate pair sums because every eligible divisor gives

\[
0<d+n/d-2\sqrt n=(d-\sqrt n)^2/d<C^2.
\]

Historical negative controls rejected altered identities, a wrong seed, a non-Pell parameter, a perturbed fifth divisor, duplicate divisors and offsets, the \(C=30\) window, reversed side placement, and both open-window endpoints. They used explicit runtime checks rather than removable Python assertions.

The recorded normal, `-O`, and `-OO` executions passed and produced byte-identical result JSON. These original mathematical executions were not repeated during edition preparation. The finite controls supplement the universal proof above; they are not a replacement for it and are not a formal proof-assistant certificate. All finite facts actually needed by the analytical argument have been retained as explicit inequalities or identities above.

## Public references

1. M. Czech, July 2026 manuscript: https://czechu.blog/erdos/problems/887/note887.pdf
2. P. Erdős and M. Rosenfeld, *The factor-difference set of integers*, Acta Arith. 79 (1997), 353–359: https://matwbn.icm.edu.pl/ksiazki/aa/aa79/aa7944.pdf
3. T. H. Chan, arXiv:1303.2069v1: https://arxiv.org/abs/1303.2069v1
4. T. H. Chan, arXiv:1406.2230v1: https://arxiv.org/abs/1406.2230v1
