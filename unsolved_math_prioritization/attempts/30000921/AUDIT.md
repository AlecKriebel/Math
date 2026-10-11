# Independent audit of polynomial multiplication and differentiation hypercyclicity

This is an AI-assisted, unrefereed mathematical review edition. Acceptance is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or novelty clearance.

The full authored mathematical proof and independent audit are retained, including every written argument, formula, and counterexample. This is not a computational reproduction package: executable code, raw computational datasets, copied source PDFs/text/images, search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Source retrieval, inspection, and mathematical executions described below are historical acts of the original investigation or audit. Publication preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution. The original proof and audit remain unchanged.

## Decision and scope

**ACCEPT as a complete negative answer to target 30000921, OWR-1787-006.**
The candidate proves that multiplication by z does not preserve every
differentiation-hypercyclic entire function. Its stronger fixed-polynomial,
density, monomial, and multiplier-classification statements are also correct.
No mathematical correction is required. This decision certifies the mathematical
argument, not novelty, historical priority, journal acceptance, or publication.
The exact immutable candidate identity is recorded in ACCEPTANCE.json.

The audit independently reconstructed every infinite-dimensional argument below.
It read the candidate as mathematical text, checked the original source statement
and nearby theorems, and used separately written finite exact-arithmetic checks
only to corroborate coefficient identities. No candidate-authored or
source-authored program was imported or executed.

## Source statement and operation

The original target is Question 5 on printed page 330, PDF page 34, in George
Costakis's contribution to the 2008 Oberwolfach report. The universal assertion
is

\[
\forall f\in HC(D)\ \forall p\in\mathbb C[z]\text{ nonconstant},
\qquad pf\in HC(D),
\]

where multiplication is pointwise and H(C) carries the compact-open topology.
The adjacent Theorem 6 gives a residual class of functions for which every
nonzero polynomial multiplier works. These are different quantifiers. The
original page was visually inspected, including Definition 4, Theorem 6, and
Question 5. [Original report](https://ems.press/content/serial-article-files/46147).

One counterexample with the admissible nonconstant polynomial p(z)=z disproves
the full universal assertion. There is no obligation to disprove it separately
for every p; the candidate nevertheless establishes that stronger fixed-p result.
The target is neither p(D)f nor p composed with f, and it is not a question about
translation or composition-operator hypercyclicity.

## Existence and density of starting functions

The candidate supplies a complete Baire argument, so existence of a starting
hypercyclic function is not an unproved premise. The standard analytic inputs
are the Weierstrass locally uniform limit theorem, Taylor approximation, Cauchy
estimates, and the Baire category theorem.

Write ||u||_r=max over |z|<=r of |u(z)|. Completeness of H(C) for its standard
countable family of disk seminorms follows by taking compatible uniform limits
on each disk and applying the Weierstrass theorem. Differentiation is continuous
by a Cauchy estimate on a slightly larger disk. Polynomials with coefficients in
Q+iQ form a countable dense set; enumerate them as P_j.

For positive integers j,r,s, consider the open set

\[
U_{j,r,s}=\bigcup_{n\ge0}\{u:\|D^n u-P_j\|_r<1/s\}.
\]

To check density, let V be any nonempty open subset of H(C), and choose a
polynomial Q in V. If P_j(z)=sum from k=0 to d of b_k z^k, set

\[
I_nP_j(z)=\sum_{k=0}^d b_k\frac{k!}{(n+k)!}z^{n+k}.
\]

Termwise differentiation gives D^n(I_nP_j)=P_j. For every fixed R each term has
disk norm at most |b_k| k! R^(n+k)/(n+k)!, which tends to zero. There are only
finitely many terms, hence I_nP_j tends to zero in H(C). Choose n larger than
the degree of Q and sufficiently large that Q+I_nP_j is in V. Its n-th
derivative is P_j, proving V meets U_{j,r,s}.

Baire's theorem makes the intersection of all these countably many open dense
sets dense and nonempty. Membership makes the derivative orbit dense: first
approximate a target entire function by a P_j on a sufficiently large integer
disk, then choose s to make 1/s smaller than the remaining error allowance.
Every compact set is contained in such a disk. Thus HC(D) is dense and nonempty.

This is an existence proof, not a printed numerical Taylor-coefficient list or
a computation of a particular MacLane function. The counterexample construction
is explicit relative to any starting f in HC(D); Baire provides such an f.
No stronger form of constructivity is necessary for the existential negation of
the target.

## Dense tails and null perturbations

A potential error in this kind of argument is to use a merely dense sequence
as if all of its tails were dense. The candidate proves the needed fact here.

Fix N. The set E={D^n f:0<=n<N} is finite and closed. Every nonempty open subset
V of H(C) contains infinitely many elements: sufficiently small distinct
constant perturbations of any element of V remain in V. Therefore V minus E
is nonempty and open. A full dense derivative orbit meets V minus E, and every
index realizing such a point is at least N. The derivative tail is dense.

For an arbitrary target g, choose n_j strictly increasing so that D^(n_j)f
approximates g on the disk of radius j to within 1/j. This is possible by tail
density, and it gives locally uniform convergence D^(n_j)f -> g.

If D^n h -> 0 locally uniformly, then along those same indices
D^(n_j)(f+h) -> g. Since g was arbitrary, f+h remains hypercyclic. This is an
additive null-orbit perturbation lemma; it does not claim that arbitrary small
perturbations preserve hypercyclicity.

## Entire corrections with vanishing derivative orbit

Let alpha be any complex number and let c_k tend to zero. Such a sequence is
bounded, say by C. The series

\[
h(z)=\sum_{k\ge0}c_k\frac{(z-\alpha)^k}{k!}
\]

converges absolutely and uniformly on each disk about alpha, dominated by C e^R.
It defines an entire function, and its Taylor series can be differentiated
termwise. For every derivative order n,

\[
\sup_{|z-\alpha|\le R}|h^{(n)}(z)|
\le\sum_{k\ge0}|c_{n+k}|\frac{R^k}{k!}
\le e^R\sup_{j\ge n}|c_j|\longrightarrow0.
\]

All these estimates refer to derivative-normalized coefficients c_k, not
ordinary Taylor coefficients. This normalization is respected throughout the
candidate. Disks centered at alpha exhaust C, so the estimate is exactly the
compact-open convergence required by the perturbation lemma.

## The counterexample for p equal to z

Start with any f in HC(D), writing a_k=f^(k)(0). Set t_k=1/(k+1). Keep
b_k=a_k when |a_k|>=t_k; otherwise replace it by the positive real number t_k.
Then |b_k|>=t_k and, for c_k=b_k-a_k,

\[
|c_k|\le2t_k=\frac{2}{k+1}.
\]

The bound includes complex a_k: in the replacement branch it is just
|t_k-a_k|<=t_k+|a_k|<2t_k. At equality |a_k|=t_k the coefficient is kept.
There is no claim that the perturbation is bounded by t_k; the actual sealed
candidate correctly uses the factor 2.

The function h with normalized coefficients c_k is entire and satisfies
||D^n h||_R<=2e^R/(n+1). Put F=f+h. The previous lemmas prove F is
hypercyclic and F^(k)(0)=b_k. For every n>=1, Leibniz's rule gives

\[
(zF)^{(n)}(z)=zF^{(n)}(z)+nF^{(n-1)}(z),\qquad
|(zF)^{(n)}(0)|=n|b_{n-1}|\ge1.
\]

At n=0 the value is zero. Every derivative-orbit evaluation at 0 therefore
lies in {0} union {w:|w|>=1}. Its distance from 1/2 is at least 1/2, including
the zeroth derivative. The nonempty open set

\[
\{u\in H(\mathbb C):|u(0)-1/2|<1/4\}
\]

is disjoint from the whole orbit of zF. It is open by continuity of evaluation
at 0, and contains the constant function 1/2. Thus zF is not hypercyclic.
The n=0 case and all n>=1 are covered; the proof does not rely on eventual
orbit exclusion alone or on finitely many observed coefficients.

## Each fixed polynomial and the triangular recursion

Fix an arbitrary nonconstant p. The fundamental theorem of algebra supplies a
root alpha, of some multiplicity m>=1. Write

\[
p(\alpha+w)=\sum_{j=m}^d q_jw^j,\qquad q_m\ne0,
\quad a_k=f^{(k)}(\alpha).
\]

For an arbitrary eta>0, recursively construct c_k. At stage k put n=k+m and
A_k=q_m (k+m)!/k!. The contribution to (pF)^(n)(alpha) excluding A_k c_k is

\[
S_k=A_ka_k+
\sum_{j=m+1}^{\min(d,k+m)}
q_j\frac{(k+m)!}{(k+m-j)!}(a_{k+m-j}+c_{k+m-j}).
\]

Every correction index in this sum satisfies 0<=k+m-j<k. No unchosen future
coefficient is used. At k=0 the sum is empty. Since A_k is nonzero, take c_k=0
when |S_k|>=eta, and otherwise take c_k=(eta-S_k)/A_k. This ensures

\[
|S_k+A_kc_k|\ge\eta,\qquad
|c_k|\le\frac{2\eta\,k!}{|q_m|(k+m)!}.
\]

The estimate is uniform in the sizes of the previously constructed terms and
in all other polynomial coefficients. Large S_k needs no correction; small S_k
can be sent exactly to eta with the stated small correction. The dependence of
S_k on earlier corrections thus causes no accumulation in the bound for c_k.
Because m>=1, the bound tends to zero. It is at most 2eta/(|q_m|m!), so the
correction series is entire. In fact the sharper bound

\[
\sup_{|z-\alpha|\le R}|h^{(n)}(z)|
\le\frac{2\eta e^R}{|q_m|}\frac{n!}{(n+m)!}
\]

holds: the factorial ratio decreases as its index increases. In particular
D^n h -> 0, and F=f+h is hypercyclic.

The exact Taylor-product formula is

\[
(pF)^{(n)}(\alpha)=
\sum_{j=m}^{\min(d,n)}q_j\frac{n!}{(n-j)!}
(a_{n-j}+c_{n-j}).
\]

It is a finite coefficient identity between convergent entire power series.
For n=k+m the expression is S_k+A_kc_k. Later corrections cannot change it,
since their normalized Taylor indices are greater than k. Hence every order
n>=m has evaluation modulus at least eta. Orders n<m vanish because pF has
a zero of order at least m at alpha. The open evaluation disk centered at
eta/2 of radius eta/4 is missed by the whole derivative orbit. Thus pF is not
hypercyclic.

The eta parameter also proves the asserted density. On a disk centered at
alpha,

\[
\|h\|_{R,\alpha}\le\frac{2\eta e^R}{|q_m|m!}.
\]

Given any neighborhood W of f, finitely many compact-open constraints suffice
inside W; all the relevant compact sets fit inside one disk centered at alpha.
Choose eta small enough for that bound to satisfy the constraints, then run the
recursion with this eta. The bound is uniform over its coefficient choices, so
there is no continuity or circular-dependence assumption in choosing eta.
Counterexamples are dense near every starting f in HC(D), and HC(D) is dense
in H(C); consequently the fixed-p counterexample set is dense in H(C).

## Additional conclusions and excluded quantifiers

The single F constructed for p=z and eta=1 also defeats every multiplier z^m
with m>=1. For n<m the evaluation at 0 vanishes. Writing n=k+m for n>=m,

\[
|(z^mF)^{(n)}(0)|\ge\frac{(k+m)!}{k!(k+1)}
=\prod_{j=2}^m(k+j)\ge1,
\]

with the product equal to 1 when m=1. The same open evaluation disk works for
every m. This verifies precisely the simultaneous monomial claim.

For a nonzero constant c, multiplication by c is a homeomorphism of H(C) and
D^n(cf)=cD^nf, so it preserves every hypercyclic vector. The zero multiplier
fails, and every nonconstant polynomial fails by the preceding construction.
Thus the classification of universal polynomial multipliers is exact.

The fixed-p theorem has the order of quantifiers

\[
\forall p\text{ nonconstant}\ \forall f\in HC(D)\ \forall W\ni f\text{ open}
\ \exists F\in W\cap HC(D):pF\notin HC(D).
\]

It does not yield one F that fails for all nonconstant p. Its proof may choose
a different root, correction, and F for different p. It also does not state
that every f fails for any prescribed p. The residual positive class in the
original report is compatible with dense negative examples: dense sets may be
meagre. No topology or category contradiction is present.

## Later literature and historical boundaries

The inspected 2018 paper treats selected multiplicative structures, polynomial
composition, and convolution or composition operators. Its introduction on
PDF pages 1–3 supplies no universal pointwise-product conclusion for all
f in HC(D). This was a statement-context inspection, not a full audit of its
proofs. [2018 paper](https://jot.theta.ro/jot/archive/2018-080-001/2018-080-001-011.pdf).

Costakis's 2010 Theorem 1.7 states a residual common-hypercyclicity result for
the sequences n^b D^n over real b. Theorem 1.7 was visually checked on PDF page
5; the related Section 6 text on pages 21–22 was inspected. That generic
statement does not imply that every D-hypercyclic function is common for those
sequences. [2010 publisher reference](https://doi.org/10.4064/sm201-3-1).

Bounded independent searches for the exact title and polynomial-multiplier
formulation did not establish an earlier settlement or historical priority.
They are not an exhaustive bibliography and do not prove that the question
remained open in 2026. The 2010 direct PDF and DOI requests failed in the web
reader during this audit; its already retrieved whole PDF was independently
hashed and its relevant local pages inspected. Retrieval success is not being
claimed for those failed web requests. Public source identities and exact
inspection bounds appear in SOURCES.json.

## Finite corroboration and integrity controls

The auditor's independent program uses exact Gaussian-rational arithmetic. In
each of Python normal, -O, and -OO modes it checked 4,961 z-replacement cases,
246 monomial indices, 450 recursive fixed-p coefficients, 30 low derivatives,
6,525 preservation checks for previously fixed derivative values, and 10,168
factorial-tail inequalities. The positive receipts are identical. Complex
coefficients, several root multiplicities, nontrivial cross terms, and multiple
eta values are included. These finite checks corroborate algebra only; they do
not establish hypercyclicity, infinitude, asymptotic decay, density, or novelty.

Four deliberate algebra mutations were rejected in each interpreter mode:
omitting the replacement, shifting a factorial index, dropping cross terms, and
reversing the tail inequality. The checker uses explicit exceptions rather
than assertions, so optimization cannot silently disable its checks.

The original audit packet was authenticated by a closed-set manifest and an
outside seal. Separately authored integrity checks verified byte counts,
hashes, exact membership, safe paths, and absence of symbolic links. Its
mutation-control and normal/-O/-OO verification receipts were retained with
that original packet; public receipt identities and historical scope appear in
VERIFICATION.json. Integrity is evidence that reviewed bytes did not change,
not a replacement for the written mathematical proof.

Ten integrity mutations were rejected in each interpreter mode, for 30
negative cases: byte replacement, deletion, an extra file, an extra directory,
a file symlink, a parent-directory symlink, a duplicate member, path traversal,
a wrong outside digest, and absent declared packet status. All mutations used
synthetic disposable fixtures; the candidate and source packets were unchanged.

This edition distributes the complete authored audit, an authored acceptance
record, and public source-verification metadata. Copied source text or images,
raw search results, private coordination material, and checker artifacts are
not distributed. The accepted mathematical arguments and original audit remain
unchanged; editorial changes concern review status and distribution references.
