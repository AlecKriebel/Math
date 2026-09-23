# Independent geometric audit: local positive polarization cone

Checkpoint: 2026-09-23 04:07 UTC. Best-guess completion: **100% for an independent proof of the stated basis-existence conjecture**, subject to integration by the main audit. Novelty and literature priority are not assessed here.

This investigation began from the exact conjecture supplied by the parent and did not read any other audit files or the supplied Taylor proof. It uses positivity of conditioned bilinear forms and a finite discrete maximum argument, rather than expansion of the desired mixed inequality.

## Exact claim and verdict

Let m >= 1, let d >= 2 be even, and let p be a real homogeneous polynomial of degree d with p(v) > 0 for every nonzero v in R^m. Write A for its symmetric d-linear polarization, normalized by A(v,...,v) = p(v).

**Verdict: the conjecture is true.** There is a basis x_1,...,x_m satisfying

\[
0<A(x_{j_1},\ldots,x_{j_d})\leq\prod_{r=1}^{d}p(x_{j_r})^{1/d}
\]

for every index tuple. Equality in the upper bound occurs exactly for tuples with all indices identical. Thus every genuinely mixed basis entry is both positive and strictly below the proposed bound.

In fact, a stronger uniform statement holds: there is a nonempty open cone C of nonzero vectors such that the displayed inequality holds for **all** d-tuples in C, with upper equality exactly when all vectors are positively proportional.

## 1. A direction with a positive definite polarization slice

Choose a unit vector e minimizing p on the Euclidean unit sphere, and put P = p(e) > 0. Homogeneity gives

\[
p(v)\geq P\|v\|^d\qquad(v\in\mathbb R^m),
\]

with equality at v=e. Consequently g(v)=p(v)-P||v||^d has a global minimum of zero at e, and D^2 g(e) is positive semidefinite. Since

\[
D^2p(e)[v,v]=d(d-1)A(e^{d-2},v,v)
\]

and

\[
D^2(\|\cdot\|^d)(e)[v,v]
 =d\|v\|^2+d(d-2)\langle e,v\rangle^2,
\]

we obtain the explicit lower bound

\[
\boxed{\quad
A(e^{d-2},v,v)\geq
\frac{P}{d-1}\left(\|v\|^2+(d-2)\langle e,v\rangle^2\right).
\quad}
\]

In particular, B_0(u,v)=A(e^{d-2},u,v) is positive definite, with smallest Euclidean eigenvalue at least P/(d-1). This step does not assume convexity of p or of p^(1/d).

Geometrically, the radial sublevel body of p is enclosed by a Euclidean ball tangent in direction e; the lower comparison polynomial gives a strictly positive quadratic slice there.

## 2. An open cone with all conditioned slices positive definite

Positive definiteness is open in the space of symmetric bilinear forms. The mapping

\[
(z_1,\ldots,z_{d-2})\longmapsto
\big[(u,v)\longmapsto A(z_1,\ldots,z_{d-2},u,v)\big]
\]

is continuous. Therefore some epsilon > 0 has the following property: whenever all unit vectors z_i satisfy ||z_i-e|| < epsilon, the displayed bilinear form is positive definite. Shrink epsilon, if necessary, so that A(z_1,...,z_d)>0 for every d-tuple of unit vectors in the cap; this is possible because A(e,...,e)=P>0. We may also impose epsilon < 1, so the cap lies in the hemisphere <e,z> > 0.

Define

\[
C=\{t z:t>0,\ \|z\|=1,\ \|z-e\|<\varepsilon\}.
\]

Positive scaling of the conditioning vectors multiplies a bilinear form by a positive scalar. It follows that, for **every** z_1,...,z_{d-2} in C,

\[
B_{z_1,\ldots,z_{d-2}}(u,v)
 =A(z_1,\ldots,z_{d-2},u,v)
\]

is a positive definite bilinear form on all of R^m. Also A is positive on C^d.

For d=2 the conditioning list is empty and B=A is already positive definite; the cap can still be chosen to make A positive on C^2.

## 3. Exact Cauchy–Schwarz propagation gives generalized Holder

Take any finite collection u_1,...,u_n in C normalized by p(u_i)=1. This normalization preserves C. For each multi-index alpha in N^n with |alpha|=d, set

\[
c_\alpha=A(u_1^{\alpha_1},\ldots,u_n^{\alpha_n})>0.
\]

If alpha_i,alpha_j > 0 and i != j, freeze the d-2 other arguments. Cauchy–Schwarz in the resulting positive definite bilinear form gives

\[
c_\alpha^2\leq
 c_{\alpha+e_i-e_j}\,c_{\alpha-e_i+e_j}.
\tag{CS}
\]

Here e_i denotes a multi-index coordinate vector, not the minimizing direction e.

Let M be the largest c_alpha. Among the multi-indices attaining M, choose alpha maximizing S(alpha)=sum_i alpha_i^2. Suppose alpha has two positive components alpha_i,alpha_j. Both neighboring entries in (CS) are at most M, so (CS) forces **both** to equal M. But

\[
S(\alpha+e_i-e_j)-S(\alpha)=2(\alpha_i-\alpha_j)+2,
\]

\[
S(\alpha-e_i+e_j)-S(\alpha)=2(\alpha_j-\alpha_i)+2.
\]

At least one of these increments is positive, contradicting maximality of S. Therefore the chosen alpha is pure: alpha=d e_i. Hence M=c_{d e_i}=p(u_i)=1. We have proved every normalized mixed entry is at most 1.

Given arbitrary y_1,...,y_d in C, apply this finite argument to u_r=y_r/p(y_r)^(1/d), and use multilinearity. This proves

\[
0<A(y_1,\ldots,y_d)\leq\prod_{r=1}^d p(y_r)^{1/d}
\quad\text{for all }(y_1,\ldots,y_d)\in C^d.
\]

There is no appeal to a pre-existing generalized Holder theorem and no uncontrolled error term: the finite maximum argument is the complete reduction to pure diagonal entries.

## 4. Equality and a basis

If a normalized tuple contains a nonproportional pair u,v, freeze its other arguments and apply the **strict** Cauchy–Schwarz inequality in the positive definite conditioned bilinear form:

\[
A(\ldots,u,v)^2
 < A(\ldots,u,u)A(\ldots,v,v)\leq1.
\]

Thus its mixed entry is strictly less than 1. Conversely, if all arguments are positively proportional, homogeneity gives equality. Since C lies in a hemisphere, its nonzero collinear vectors are positively proportional.

An open cone contains a basis. Explicitly, complete e to an orthonormal basis e,v_2,...,v_m and choose delta > 0 sufficiently small. The vectors

\[
x_1=e,\qquad x_i=e+\delta v_i\quad(2\leq i\leq m)
\]

all lie in C, and their determinant in this orthonormal coordinate system is delta^(m-1), so they are independent. Optionally normalize them to p(x_i)=1; independence and membership in C remain intact.

Any tuple involving at least two distinct basis indices contains a nonproportional pair. Therefore it has strict upper inequality, while all-pure tuples have equality by the definition of polarization. The absolute-value version in the original conjecture follows immediately from positivity.

## Boundary cases, limitations, and falsification checks

- **m=1:** choose the positive ray through e. The basis exists; strictness for genuinely mixed basis tuples is vacuous.
- **d=2:** the method reduces to ordinary Cauchy–Schwarz for the positive definite quadratic form. The empty conditioned list causes no difficulty.
- **Zero inputs:** excluded from C. If the cone is enlarged to include zero, the inequality still holds but upper equality also holds whenever some input is zero; the stated equality characterization must then be amended.
- **Signs:** independent sign changes of the chosen basis preserve the absolute-value conclusion. Positivity of mixed entries requires the common cone choice.
- **Uniformity:** C is chosen once and works for every finite input set and all tuples from C. The combinatorial maximum is taken separately for each finite collection; that does not weaken the uniform cone claim.
- **Conditioning:** the displayed explicit basis becomes close to linearly dependent as delta tends to zero. The argument provides no quantitative lower bound on its determinant or condition number in terms of degree and dimension alone.
- **No assumption of global convexity:** p can be nonconvex away from the cap. The proof uses a strictly positive slice at one direction and continuity of fully polarized conditioned slices.
- **Local convexity shortcut:** merely saying that p^(1/d) is locally convex would leave an unproved step for general d-linear entries. The actual sufficient property established here is positive definiteness of A(z_1,...,z_{d-2},.,.) for independent conditioning arguments in a common cone; (CS) and the finite maximum proof close that gap. No claim is made here about whether convexity alone implies a corresponding global inequality.
- **Degree and positivity:** the proof requires d>=2 and P>0. It does not establish an extension to arbitrary merely nonnegative forms.
- **No novelty assertion:** this is an independently reconstructed proof of the exact stated claim, not a verified claim that the argument or result is new.

## Independent adversarial check and final status

A separate adversarial subagent was asked to verify only the argument stated above, with no file access or edits. It confirmed the Hessian bound, joint-continuity cone step, finite maximum proof, and strictness argument. It highlighted the zero-input equality exception, which is explicitly excluded above. No mathematical gap was found.

**Strongest verified result:** the open-cone generalized Holder theorem with positivity and strictness stated above, implying the original basis-existence conjecture.

**Exact remaining gap for this approach:** none identified for the existence claim under the stated hypotheses. Literature priority, integration with the supplied material, and any quantitative basis-conditioning objective remain outside this independent audit.

Checkpoint: 2026-09-23 04:10 UTC. Best-guess completion: **100% for this independent proof route**.
