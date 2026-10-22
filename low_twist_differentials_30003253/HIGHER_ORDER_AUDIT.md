# Independent audit: higher-order branch-integral forms on the projective plane

Date: 2026-10-20. Scope: the stated symmetric-differential construction and finite minimum-twist algorithm, not the broader Garcia-Fritz question.

**Verdict.** All five mathematical claims are correct with the conventions below. The implementation is currently exact over rational coefficients, not general algebraic coefficients. For singular branches, integrality must mean generic tangential vanishing, equivalently vanishing after pullback to the normalization; it must not silently mean vanishing in a possibly torsion-bearing sheaf of Kahler differentials.

Throughout, the base field has characteristic zero, symmetric order is a positive integer, and the branch collection is nonempty. Write $E=\Omega^1_{\mathbf P^2}$ and let $B_i=(F_i=0)$ be distinct reduced irreducible homogeneous plane curves, with total degree $b$. Statements concerning the smooth-branch kernel additionally assume one smooth irreducible curve $B$ of degree $b\ge2$.

## 1. Universal lower bound

If $\omega\in H^0(\mathbf P^2,\operatorname{Sym}^r E(k))$ and $k<2r$, its **tangential pullback** to every line $L$ lies in

$$H^0(L,\operatorname{Sym}^r\Omega_L^1(k))=H^0(L,\mathcal O_L(k-2r))=0.$$

At any point of $\mathbf P^2$, every nonzero tangent direction is tangent to a unique line through that point. Thus the homogeneous degree-$r$ polynomial determined by the tensor $\omega$ vanishes on every tangent vector. In characteristic zero this forces the tensor to vanish. Hence

$$H^0(\mathbf P^2,\operatorname{Sym}^r E(k))=0\qquad(k<2r).$$

The adjective “tangential” matters: the whole restricted bundle $\operatorname{Sym}^r(E|_L)(k)$ is not just $\mathcal O_L(k-2r)$.

## 2. Incidence-polynomial presentation

Put $d=k-2r\ge0$, $x=(x_0,x_1,x_2)$, and $a=x\times dx$. The three entries of $a$ generate $E(2)$, with their unique bundle relation $x\cdot a=0$. Equivalently, the Euler sequence and $E\simeq T_{\mathbf P^2}(-3)$ give

$$0\longrightarrow\mathcal O(-1)\longrightarrow\mathcal O^3\longrightarrow E(2)\longrightarrow0.$$

Taking symmetric powers of this quotient by a line subbundle, then twisting by $d$, gives

$$0\longrightarrow\mathcal O(d-1)\otimes\operatorname{Sym}^{r-1}\mathbf C^3
\longrightarrow\mathcal O(d)\otimes\operatorname{Sym}^{r}\mathbf C^3
\longrightarrow\operatorname{Sym}^rE(k)\longrightarrow0.$$

Since $H^1(\mathbf P^2,\mathcal O(d-1))=0$, global sections are exactly polynomials $P(x,a)$ of bidegree $(d,r)$ modulo $(x\cdot a)Q$, where $Q$ has bidegree $(d-1,r-1)$. Substitution $a=x\times dx$ is the corresponding differential form. Consequently the dimension is

$$\binom{d+2}{2}\binom{r+2}{2}-\binom{d+1}{2}\binom{r+1}{2}
=\frac{(r+1)(d+1)(r+d+2)}2.$$

For $d=0$, the relation space is zero. For $d<0$, the same sequence also directly proves the vanishing in Section 1.

## 3. Exact branch test

At a smooth point $x$ of $F_i=0$, a nonzero projective tangent vector represented by $v$ satisfies $x\cdot\nabla F_i=v\cdot\nabla F_i=0$. Therefore $x\times v$ is a nonzero scalar multiple of $\nabla F_i$. The tensor vanishes on the branch tangent exactly when $P(x,\nabla F_i)$ vanishes generically on that branch. Irreducibility and reducedness then give the equivalent polynomial condition

$$F_i\mid P(x,\nabla F_i).$$

This is independent of the incidence representative, since $x\cdot a$ specializes to $\deg(F_i)F_i$ by Euler's identity. Singular points cause no additional condition for normalized/generic branch-integrality: a regular pulled-back tensor vanishing on a dense open subset of the normalization vanishes identically.

## 4. Finite exact search

Let $F=\prod_iF_i$. The first-order form

$$\ell\,dF-bF\,d\ell\in H^0(\mathbf P^2,E(b+1))$$

is integral along every branch. Choose $\ell$ so the form is nonzero; for a single line, exclude $\ell$ proportional to its equation. Indeed, identically zero would imply $F$ is a constant multiple of $\ell^b$, which is incompatible with reducedness except for that line case.

Thus the absolute minimum over **positive** symmetric orders occurs in the finite range

$$2\le k\le b+1,\qquad1\le r\le\lfloor k/2\rfloor.$$

For each pair, select a basis of the incidence quotient and impose the branch divisibilities by polynomial remainder. This is a finite homogeneous linear system. The first nonzero kernel in increasing $k$ is the exact global minimum, and a kernel vector provides a verifiable witness. Exact arithmetic is effective over a number field containing all algebraic input coefficients, hence over effectively specified $\overline{\mathbf Q}$ input. No corresponding computability claim is warranted for arbitrary unspecified complex coefficients.

## 5. Stronger bound for one smooth irreducible branch

Let $i:B\hookrightarrow\mathbf P^2$ be smooth irreducible of degree $b\ge2$, and define

$$K_r=\ker\bigl(\operatorname{Sym}^rE\longrightarrow i_*\operatorname{Sym}^r\Omega_B^1\bigr).$$

The conormal sequence on $B$, followed by symmetric powers, gives the exact sequence

$$0\longrightarrow\operatorname{Sym}^rE(k-b)\longrightarrow K_r(k)
\longrightarrow i_*\bigl(\mathcal O_B(k-b)\otimes\operatorname{Sym}^{r-1}(E|_B)\bigr)\longrightarrow0.$$

Here the kernel of $\operatorname{Sym}^r(E|_B)\to\operatorname{Sym}^r\Omega_B^1$ is precisely the conormal line $\mathcal O_B(-b)$ multiplied by $\operatorname{Sym}^{r-1}(E|_B)$.

For $r\ge2$, set $q=r-1$. Restricting Euler gives $E|_B\hookrightarrow\mathcal O_B(-1)^3$, hence

$$\mathcal O_B(k-b)\otimes\operatorname{Sym}^q(E|_B)
\hookrightarrow\mathcal O_B(k-b-q)^{\binom{q+2}{2}}.$$

If $k<b+r-1$, the line bundles on the right have negative degree, so the quotient term has no global section. At the endpoint $k=b+r-1$, any quotient-term section is a constant tensor $T\in\operatorname{Sym}^q\mathbf C^3$ belonging to $\operatorname{Sym}^q(\ker x)$ for every $x\in B$. Equivalently, contraction $x\lrcorner T=0$. This condition is linear in $x$, and a plane irreducible curve of degree at least two spans $\mathbf P^2$. Therefore every contraction of $T$ vanishes, forcing $T=0$. This endpoint argument requires $q\ge1$.

For all $k\le b+r-1$, the left term also has no global sections because $k-b\le r-1<2r$. Thus

$$H^0(K_r(k))=0\quad\text{for }r\ge2\text{ and }k<b+r.$$

Combining this with the universal lower bound gives $k\ge\max(2r,b+r)$ for any nonzero such section. In order one, the residue sequence separately excludes $k=b$ and the displayed first-order form realizes $k=b+1$. Therefore the all-orders global minimum for a smooth irreducible plane curve is exactly $b+1$. A line also has minimum $2$, by the universal lower bound and its first-order examples.

## 6. Implementation audit

Reinspection of the corrected `checks/branch_integrality.py` confirms that:

- Excluding monomials divisible by $x_0a_0$ is a valid standard-monomial basis for the single incidence relation, with the stated dimension.
- Both the coefficient-matrix construction and witness checks now use the normal form returned by `groebner([F], ..., domain=QQ).reduce(...)`. A fixed Groebner normal form is rational-linear and has kernel $(F)$, so stacking its coefficient equations correctly implements simultaneous branch-integrality.
- Exact `DomainMatrix` rank/nullspace calculations over `QQ`, followed by an independent witness check, implement the linear-algebra step. The increasing-$k$, bounded-$r$ search implements the finite minimum theorem.
- Explicit exceptions reject empty input, zero or constant equations, nonhomogeneous equations, repeated factors, and shared components between supplied equations. The kernel entrypoint requires a positive integer order and an integer twist.
- The witness verifier independently checks order/twist, nonzero polynomial, correct bidegree, nonzero incidence-quotient class, and divisibility for every branch.
- Squarefree reducible equations may group several components. This is valid: modulo an irreducible factor $F_j$ of $G$, one has $\nabla G=(G/F_j)\nabla F_j$; homogeneity of degree $r$ in the second variable multiplies the evaluated polynomial by $(G/F_j)^r$, which is nonzero in the domain modulo $F_j$. Thus grouped and split component tests are equivalent.
- All integrity checks use explicit exceptions or `require`, not optimization-removable `assert` statements. The implementation remains exact for rational coefficients only; the general algebraic-coefficient theorem requires an algebraic-number-field backend not present here.

**Regression repaired.** The earlier use of `Poly.rem` was not a valid linear multivariate normal-form map for matrix construction. For the coordinate-transformed smooth conic

$$F=xz-y^2-yz-z^2,$$

the old column matrix at $(r,k)=(1,3)$ has kernel dimension $2$, incorrectly losing one section. The corrected Groebner-normal-form matrix has rank $5$ in ambient dimension $8$, giving the required kernel dimension $3$. Each of the three explicit sections $\ell\,dF-2F\,d\ell$, with $\ell=x,y,z$, independently passes the current verifier. This supersedes the original implementation audit's endorsement of the `Poly.rem` matrix construction; none of the mathematical proofs requires alteration.

Independent guard tests were rerun both normally and with `python -O`. All seventeen negative controls were rejected in both modes: empty, zero, constant, nonhomogeneous, nonreduced, duplicate, and shared-component input; zero, negative, and nonintegral order; nonintegral twist; zero, wrong-bidegree, zero-incidence-class, wrong-branch, and invalid-order witnesses; and a deliberately false `require` condition. A valid line witness was accepted, the transformed conic retained dimension $3$, and the grouped product $xyz$ agreed with the split branches $x,y,z$ at $(r,k)=(2,4)$ in both modes.

Independent exact spot checks returned: for the smooth conic $xz-y^2$, dimensions $0,3,1,3$ at $(r,k)=(1,2),(1,3),(2,4),(3,6)$, respectively; the quadratic-order conic witness was $ac-b^2/4$. The Fermat cubic had zero kernel at the delicate $(r,k)=(2,4)$ endpoint. These checks supplement, rather than replace, the proofs above.

**Scope limit:** this establishes the specified plane branch-integrality optimization and its finite exact search. It does not assert a solution of the broader original Garcia-Fritz problem.
