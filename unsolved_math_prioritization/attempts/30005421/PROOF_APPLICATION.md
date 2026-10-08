# Prior-result application: uniform expansion for wild quivers

Target identifier: **30005421 / OWR-12697690-001**. Verification date: **8 October 2026**.

**Disposition: affirmative, already proved by Markus Reineke. No novel theorem is claimed.**

The relevant result is the forward implication of Theorem 2.4 in Markus Reineke, *Expander representations of quivers*, **Forum of Mathematics, Sigma 14 (2026), e132, 1–10**, [doi:10.1017/fms.2026.10284](https://doi.org/10.1017/fms.2026.10284), published online 29 September 2026. A public author version is [arXiv:2411.15609v2](https://arxiv.org/abs/2411.15609v2), dated 6 July 2026. Reineke credits Urban Jezernik for the argument simplifying Lemma 5.3. The construction below is a verification of that published argument, with its uniform choices and elementary incidence calculation spelled out.

## 1. Exact question and scope

The originating contribution is Reineke's *Expander representations*, in [Oberwolfach Report 7/2023](https://doi.org/10.4171/owr/2023/7), printed pp.405–406; the [official report PDF](https://ems.press/content/serial-article-files/47001) was inspected, including a rendering of p.405.

Its setting is a **finite acyclic quiver** $Q$, representations over an **algebraically closed field** $F$, and a slope $\mu=\Theta/\kappa$, rational-valued on nonzero integral dimension vectors, with $\kappa$ positive. The requested conclusion is

$$
\exists\mu\;\forall\delta\in(0,1)\;\exists\epsilon>0\;\exists\text{an unbounded family }(V_j)_j
\quad
\mu(U)\leq\mu(V_j)-\epsilon
$$

for every nonzero subrepresentation $U\subseteq V_j$ satisfying

$$
\kappa(U)\leq\delta\kappa(V_j).
$$

The field has no characteristic restriction. Wildness is that of the finite acyclic path algebra; for a connected quiver it means the underlying graph is neither Dynkin nor extended Dynkin. Disconnected quivers are included by selecting a wild connected component.

The published paper allows real-valued slopes and uses a strict gap inequality. Its proof actually supplies an integral-coefficient slope and one family working simultaneously for all $\delta$. These strengthen, rather than alter, the original question. Neither arbitrary non-algebraically-closed fields, oriented cycles, prescribed slopes, nor explicit matrices are part of this conclusion.

## 2. Forms and a fixed rational slope

Write the Euler form as

$$
E(a,b)=\sum_i a_i b_i-\sum_{i\to j}a_i b_j,
\qquad S(a,b)=E(a,b)+E(b,a),
\qquad A(a,b)=E(a,b)-E(b,a).
$$

Thus $S(a,b)=a^TCb$, where $C$ is the symmetric Cartan matrix. First assume $Q$ connected and wild. By the standard Dynkin/extended-Dynkin classification and Perron–Frobenius applied to the nonnegative irreducible matrix $2I-C$, the least eigenvalue $\lambda_1$ of $C$ is negative and simple. It has a vector $v>0$; the next eigenvalue satisfies $\lambda_2>\lambda_1$. This is precisely the input recorded in Reineke's Lemma 5.1.

For a positive real vector $d$ close in direction to $v$, put

$$
w=-Cd>0,\qquad B=-S(d,d)=w\cdot d>0,\qquad
M(d)=\max_i\frac{d_i}{w_i},
$$

and define the restricted Rayleigh minimum

$$
b(d)=\min_{\substack{\|x\|=1\\S(d,x)=0}}S(x,x).
$$

The minimum exists. It is continuous as the nonzero normal $Cd$ varies: the unit spheres in the corresponding hyperplanes vary continuously, and the quadratic form is continuous on the compact unit sphere. Equivalently, a sequence of minimizing unit vectors has a convergent subsequence for the lower bound, while orthogonal projection of a minimizing vector onto nearby hyperplanes gives the upper bound.

At $d=v$,

$$
M(v)=-1/\lambda_1,\qquad b(v)=\lambda_2.
$$

Consequently the scale-invariant continuous quantity

$$
c(d)=1+\min\{b(d),0\}M(d)
$$

is positive near the ray through $v$. Indeed its value on that ray is (1) if $\lambda_2\geq0$, and $1-\lambda_2/\lambda_1>0$ otherwise. Choose a **positive rational** $d$ in this neighborhood and clear denominators. Positive rescaling preserves $w>0$, $M$, the orthogonality hyperplane, and $c$. We therefore fix $d\in\mathbb Z_{>0}^{Q_0}$ and $c=c(d)>0$ for the remainder of the proof.

Set

$$
\Theta(a)=A(d,a),\qquad \kappa(a)=-S(d,a)=w\cdot a,
\qquad\mu(a)=\frac{\Theta(a)}{\kappa(a)}.
$$

These two linear forms have integral coefficients, $\kappa$ is strictly positive on the nonzero nonnegative cone, and $\mu(d)=0$. The slope is fixed once and for all; it does not depend on the family index, $\delta$, or a subrepresentation.

## 3. Uniform numerical inequality

Take any real vector $0\leq f\leq d$ satisfying $E(f,d-f)\geq0$, and suppose $0<\eta<1$, where

$$
\eta=\frac{\kappa(f)}{\kappa(d)}.
$$

Write $f=\eta d+x$. Then $S(d,x)=0$, and the coordinate bounds give

$$
-\eta d_i\leq x_i\leq(1-\eta)d_i,
\qquad
x_i^2\leq\eta(1-\eta)d_i^2+(1-2\eta)d_ix_i.
$$

Multiplying by $w_i/d_i>0$ and summing cancels the linear term because $w\cdot x=0$. It follows that

$$
\sum_i\frac{w_i}{d_i}x_i^2\leq\eta(1-\eta)B,
\qquad
\|x\|^2\leq M(d)\eta(1-\eta)B. \tag{1}
$$

If $b(d)\geq0$, then $S(x,x)\geq0$. If $b(d)<0$, the definition of $b(d)$ and (1) give

$$
S(x,x)\geq b(d)\|x\|^2
\geq b(d)M(d)\eta(1-\eta)B.
$$

Both cases are expressed by

$$
S(x,x)\geq\min\{b(d),0\}M(d)\eta(1-\eta)B. \tag{2}
$$

The Euler inequality implies

$$
A(d,f)\leq S(d,f)-S(f,f)
=-\eta(1-\eta)B-S(x,x)
\leq-c\eta(1-\eta)B. \tag{3}
$$

Since $\kappa(f)=\eta B>0$, (3) yields the dimension-independent slope bound

$$
\mu(d)-\mu(f)=-\mu(f)\geq c(1-\eta). \tag{4}
$$

This is Reineke's Lemma 5.3 and Corollary 5.4 in a form with a single constant chosen before $f$. In particular, it does not assert that every individual restricted Rayleigh quotient approaches $\lambda_2$; only their minimum has that limit.

## 4. One family of representations, independent of the cutoff

For each integer $n\geq1$, let $D=nd$. The representation space $R_D(Q)$ is an affine space over $F$. For each integral vector $0\leq e\leq D$, let $Z_e\subseteq R_D(Q)$ consist of the representations admitting an $e$-dimensional subrepresentation.

Here is the elementary incidence calculation underlying the needed direction of the general-subrepresentation criterion. Over

$$
G_e=\prod_i\operatorname{Gr}(e_i,D_i),
$$

consider the incidence space of pairs $(V,(U_i)_i)$ with each arrow of $V$ mapping $U_i$ into $U_j$. For fixed $(U_i)$, the condition on arrow $i\to j$ imposes exactly $e_i(D_j-e_j)$ independent linear conditions. This incidence space is a vector bundle over $G_e$, and its dimension is

$$
\dim R_D(Q)+\sum_i e_i(D_i-e_i)
-\sum_{i\to j}e_i(D_j-e_j)
=\dim R_D(Q)+E(e,D-e).
$$

Its projection to $R_D(Q)$ has closed image $Z_e$, because the Grassmannian factor is projective. Therefore, if $E(e,D-e)<0$, the image is a proper closed subset. There are only finitely many possible integral $e$. Since affine space over an algebraically closed field is irreducible, their finite union cannot fill $R_D(Q)$.

Choose $V_n\in R_D(Q)$ outside **all** these negative-Euler loci. Every subrepresentation of $V_n$ consequently has dimension vector $e$ with

$$
E(e,D-e)\geq0. \tag{5}
$$

This choice depends on $n$ but not on $\delta$. It is the same generic-avoidance argument used in Reineke's numerical criterion, with the finite set chosen once for the whole dimension vector. No uncountable intersection of open sets, and no uncountability assumption on $F$, is needed.

For a nonzero proper subrepresentation $U\subset V_n$, put $e=\dim U$ and $f=e/n$. Then $0\leq f\leq d$, and (5) implies $E(f,d-f)\geq0$. Also

$$
\eta=\frac{\kappa(e)}{\kappa(nd)}
=\frac{\kappa(f)}{\kappa(d)}\in(0,1).
$$

Slope homogeneity and (4) now show

$$
\mu(V_n)-\mu(U)\geq c(1-\eta). \tag{6}
$$

Given any $\delta\in(0,1)$, choose

$$
\epsilon(\delta)=\frac c2(1-\delta)>0.
$$

Whenever $\kappa(U)\leq\delta\kappa(V_n)$, equation (6) gives

$$
\mu(U)\leq\mu(V_n)-c(1-\delta)
<\mu(V_n)-\epsilon(\delta).
$$

This verifies both the original weak inequality and the paper's strict convention. The constant is independent of $n$. Moreover,

$$
\dim_F V_n=n\sum_i d_i\longrightarrow\infty.
$$

Thus $(V_n)_{n\geq1}$ is one unbounded uniform expander family. Taking $\delta=\kappa(U)/\kappa(V_n)$ in (6) also proves every $V_n$ is stable.

## 5. Disconnected quivers and conclusion

A finite acyclic wild quiver has a wild connected component $Q'$. Apply the preceding construction there. Extend its representations by zero at other vertices; extend $\Theta$ by zero and choose any positive integer coefficients for $\kappa$ at the other vertices. Every subrepresentation is still supported on $Q'$, so its dimensions, slopes and cutoff inequalities are unchanged. The extended slope remains rational and has positive denominator on the full nonnegative cone.

This proves the complete affirmative answer to the original OWR question in its actual source setting. The already-known result is due to Reineke. The proof here is an attributed verification/application, with no additional mathematical scope or novelty claim.

## 6. Audit boundaries

- The required direction is **wildness implies existence**. The published converse is not needed to resolve this target; this packet does not claim a new or independently reconstructed proof of the converse.
- Algebraic closure is preserved. No descent to a fixed nonclosed field is asserted.
- Only existence is established. No efficient algorithm or explicit arrow matrices are asserted.
- The positive gap need not remain bounded below as $\delta\to1$; the target fixes each $\delta<1$.
- The source's strict-versus-weak gap convention, its compressed spectral-minimum argument, and the family/cutoff quantifier order are handled explicitly above. They leave no missing bridge for the target.
- The accompanying exact tests check algebra and finite examples. They supplement the general proof and do not prove a universal statement by finite sampling.
