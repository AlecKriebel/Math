# Independent adversarial audit of restricted deductions

Audit checkpoint (clock verified): **2026-10-17T20:57:14Z**. Assigned review completion estimate: **100%** for the frozen claims below, including the later exact-homomorphic-slice lemma and nonlinear-embedding counterexample. Estimated discovery progress toward each original arbitrary quasi-isometry question: **5%**; this is an exploratory planning estimate, not a probability for either answer. No arbitrary quasi-isometry construction or separating invariant is established.

This reviewer examined the two named notebooks, `PROBLEM.md`, and the later `constructive_affine_obstruction.md`, did not read another reviewer's verdict, and did not contact an external individual, use Git, publish, or change the source notebooks. Reading publicly available primary papers was the only external research activity.

## Frozen scope and verdict

The initial snapshot was frozen at **2026-10-17T20:52:47.965469+00:00** in `partial_adversary01_sources/`. Its manifest records:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `approach_coset_geometry.md` | 5903 | `5f76266447cb4192056382954bab3c073ad375c50869ccc849bcc90abef09ef0` |
| `approach_constructive.md` | 6775 | `6b84b1312216524c7f59764527bbeb3943ef6351a2230f17a9e0eeb2a373f32b` |
| `PROBLEM.md` | 1132 | `a99810a547e08c162a3ee635887d7778b4b76e192e254dc417215e8e0dddf5c2` |

At 20:54:01 UTC these source hashes were unchanged. Later edits are outside that frozen audit. A later parent message requested an additional audit of an explicitly stated homomorphic-slice lemma; its full statement and independent proof appear below. The intervening constructive notebook version, SHA-256 `f4d7df428902e44777b29f4667bb1ba5cb9efb8ba03c90e69b578ac1bb1fe657`, had no such lemma when inspected. This audit makes no claim to review its added families C and D.

The subsequently written `constructive_affine_obstruction.md` was frozen and fully inspected at **2026-10-17T20:56:21.503664+00:00**, with 7589 bytes and SHA-256 `0f36a91f0fe8aac710f91ea5b1a877e67796af4ea099a4c4824540a61d8f0643`. Its exact statement, biorder argument, bounded-homomorphism lemma, and five-step proof agree with the independent proof in Section 6; no additional defect was found. `additional_manifest.json` records that snapshot. Section 7 audits the parent's later explicitly stated counterexample; it does not depend on a later source-file version.

**Verdict:** all six restricted deductions survive. There is no counterexample to a claim as actually stated with the conventions below. Two plausible strengthenings are false: denominator depth is not globally Lipschitz on the usual Cayley metric, and affine normalization of an entire local subgroup cannot be justified merely from arbitrary dyadic endpoints. Neither false strengthening is needed in the notebooks. The stronger exact-homomorphic-slice obstruction also survives independent proof.

## Assumptions and conventions that must remain explicit

The group is the usual **finite** dyadic PL group $F$ on $[0,1]$, with slopes powers of two. Multiplication means $fg=f\circ g$. Let $S=\{x_0^{\pm1},x_1^{\pm1}\}$, with the functions in the constructive notebook, and use the **left-invariant** word metric $d_F(g,h)=|g^{-1}h|_S$. Exact numerical lengths below concern this generating set. Their unboundedness consequences hold for every finite generating set.

Write $H=\operatorname{Stab}_F(1/2)$. Its two restrictions, rescaled by factors two, identify it with $F\times F$. For product spaces, use the sum metric. The coset arguments also work with the usual max or finite-$p$ product metrics, since restricting to either coordinate recovers that coordinate's metric. They do not claim anything about deliberately warped metrics depending on both coordinates. All distances in a metric space $P$ or $Y$ are finite.

The classical structural inputs are: $F'$ is simple, $F/F'\cong\mathbb Z^2$, and $F'$ comprises elements identity near the interval endpoints. These are Theorems 4.1 and 4.5 of [Cannon–Floyd–Parry, *Introductory notes on Richard Thompson's groups*](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf), printed pp. 228 and 230. The nontrivial bumps below have infinite order, proving infinitude where it is needed. [Burillo–Cleary–Röver, *Commensurations and subgroups of finite index of Thompson's group F*](https://msp.org/gt/2008/12-3/gt-v12-n3-p10-p.pdf), Proposition 2.1, independently confirms that finite-index subgroups of $F$ contain $F'$ and have derived subgroup $F'$. The product extension is proved here rather than assumed.

## 1. The virtual centralizer: verified by two proofs

Define the virtual centralizer here as

\[
\operatorname{VC}_F(H)=\{a\in F:[H:C_H(a)]<\infty\}.
\]

For dyadic $c<d$, put $\ell=d-c$ and rescale the displayed $x_0$ into $[c,d]$, extending it by identity. On its three interior pieces the resulting bump $b$ is

\[
b(t)=t/2+c/2,\qquad b(t)=t-\ell/4,\qquad b(t)=2t-d.
\]

Its interior breakpoints are $c+\ell/2$ and $c+3\ell/4$, both dyadic. Its slopes are $1/2,1,2$. On every interior point it satisfies $b(t)<t$. Thus it is an element of the actual dyadic group $F$, and every positive power moves every interior point while fixing the complement of $(c,d)$. No breakpoint involving division by three occurs.

Suppose $a\ne1$. There is a moved point $x$ in one of the two open half intervals: fixing both open halves would force $a=1$ by continuity. Choose dyadic $c,d$ inside that half with $x\in(c,d)$ and $a(x)\notin[c,d]$. For the bump $b$ above and every positive integer $m$,

\[
ab^m(x)\ne a(x)=b^m a(x).
\]

So $a$ commutes with no positive power of $b$. But every finite-index subgroup of $H$ contains a positive power of each $b\in H$, by the finite action of its cyclic subgroup on the coset set. Hence $C_H(a)$ cannot have finite index. This proves $\operatorname{VC}_F(H)=\{1\}$ **without using simplicity**. Equivalently the conjugates by powers of this particular bump are already pairwise distinct. Properness of any finite-generator word metric makes the orbit unbounded.

The source's proof is also correct: $b$ lies in the relevant factor of $H'=F'_L\times F'_R$, since it is identity near that half's endpoints. Thus $C_F(H')=1$ by the same pointwise argument. A finite coset action of $H$ kills each infinite simple factor of $H'$, so finite index of $C_H(a)$ implies $H'\le C_H(a)$, and therefore $a=1$. No normality of $C_H(a)$ is assumed; it is the kernel of the coset action that is normal.

**Dyadic scope trap checked.** Arbitrary dyadic $c,d$ suffice for the *single forward-rescaled bump* just constructed. They do not automatically make affine normalization of the *entire* local subgroup an isomorphism onto the standard $F$: for example normalizing $[1/8,1/2]$ takes its interior dyadic point $1/4$ to $1/3$. A small dyadic bump with a genuine breakpoint at $1/4$ witnesses the problem. The source does not require this false generalization. Taking $d-c$ a power of two would also avoid it.

## 2. Both untwisted coset-product orders: verified

Let $s:P\to F$ be any map, with no homomorphism or section assumption, and suppose a proposed map on $H\times P$ has a global upper bound $d(\Psi(u),\Psi(v))\le Ld(u,v)+C$.

For $\Psi(h,p)=s(p)h$, fix $p,q$. Comparing $(h,p)$ and $(h,q)$ gives

\[
|h^{-1}s(p)^{-1}s(q)h|_F\le Ld_P(p,q)+C \quad\text{for every }h\in H.
\]

The entire conjugacy orbit of $s(p)^{-1}s(q)$ lies in one finite ball. Section 1 forces that element to be the identity, so $s(p)=s(q)$. Since $p,q$ were arbitrary, $s$ is constant.

For $\Psi(h,p)=h s(p)$, let $b_1,\ldots,b_k$ generate $H$. Comparing $(1,p)$ and $(b_j,p)$ uniformly bounds every $s(p)^{-1}b_js(p)$. There are only finitely many possible tuples, as the target balls are finite. Equal tuples for $s_1,s_2$ imply $s_2s_1^{-1}\in C_F(H)=1$. Thus $s(P)$ is finite.

Every inverse and multiplication order above was checked with the declared metric. The first convention parametrizes left cosets $s(p)H$, the second right cosets $Hs(p)$. An injective section of an infinite coset set violates the respective conclusion. The coset index is infinite: the points $x_0^{-n}(1/2)=1-2^{-(n+1)}$ are distinct, so their left cosets modulo $H$ are distinct. These arguments use the upper bound alone; an arbitrary coordinate change depending on both $h$ and $p$ is outside their scope.

## 3. Noncommensurability and homomorphic quasi-isometries: verified

For $G=F^r\times\mathbb Z^s$, set $D=(F')^r\times\{0\}$. Every homomorphism $D\to K$ to a finite group kills each simple factor, hence is trivial. Consequently every finite-index subgroup $U\le G$ contains $D$, by its finite coset action. The group $D$ is perfect: each infinite simple factor is nonabelian, so its derived subgroup is the whole factor. Therefore

\[
D=[D,D]\le[U,U]\le [G,G]=D.
\]

It follows that $U_{\rm ab}=U/D$, a finite-index subgroup of $G/D\cong\mathbb Z^{2r+s}$. In particular every finite-index subgroup of $F,F\times\mathbb Z,F\times F$ has abelianization rank $2,3,4$, respectively. This verifies the needed finite-index assertion, including subgroups of products that need not themselves be product subgroups. The three groups are pairwise noncommensurable.

If a group homomorphism is a quasi-isometry between finitely generated groups, its lower bound confines its kernel to a finite ball. Coarse density makes its image finite index: every target element is in the image times one of finitely many bounded-length words. Here every source is torsion-free, since a nonidentity increasing interval homeomorphism moves a point strictly along all positive iterates; products with $\mathbb Z$ remain torsion-free. Thus the finite kernel is trivial, and such a homomorphism would give an isomorphism with a finite-index subgroup of the target, contradicting the ranks. The argument also excludes maps a uniformly bounded distance from a homomorphism, because that homomorphism would itself be a quasi-isometry.

This is **not** an obstruction to general quasi-isometries. Neither abelianization rank nor commensurability is being asserted to be a quasi-isometry invariant.

## 4. Exact distance from the fixed stabilizer: verified

For $q=m/2^k\in(0,1)$ reduced, write $\delta(q)=k$. The formulas for $x_0,x_0^{-1},x_1,x_1^{-1}$ have slopes in $\{1/2,1,2\}$ and intercept denominators dividing $8$. Thus for $k\ge3$, every piece sends $q$ to depth at most $k+1$. The cases of smaller depth are completely exhausted by $q=1/2,1/4,3/4$:

| $q$ | $x_0(q)$ | $x_0^{-1}(q)$ | $x_1(q)$ | $x_1^{-1}(q)$ |
| --- | --- | --- | --- | --- |
| $1/2$ | $1/4$ | $3/4$ | $1/2$ | $1/2$ |
| $1/4$ | $1/8$ | $1/2$ | $1/4$ | $1/4$ |
| $3/4$ | $1/2$ | $7/8$ | $5/8$ | $7/8$ |

Hence $\delta(s(q))\le\delta(q)+1$ for every generator or inverse. Apply this to the successive letters of any word, starting with its rightmost letter, to obtain $\delta(u(1/2))\le |u|+1$.

For $n\ge0$ and $h\in H$,

\[
(x_0^{-n})^{-1}h(1/2)=x_0^n(1/2)=2^{-(n+1)}.
\]

The depth bound gives $|(x_0^{-n})^{-1}h|\ge n$. The choice $h=1$ gives an upper bound $n$, proving $d_F(x_0^{-n},H)=n$. Thus every map whose image is contained in this fixed $H$ fails coarse surjectivity, including both displayed product embeddings.

**A false strengthening has an exact counterexample.** The function $g\mapsto\delta(g(1/2))$ is not globally Lipschitz for the standard left-invariant metric. Let $a_n=L(x_0^n)$. Then $d_F(a_n,a_nx_0)=1$, while $a_n(1/2)=1/2$ and $(a_nx_0)(1/2)=2^{-(n+2)}$, a depth jump $n+1$. The source uses only the proved lower bound on word length from the identity, so this counterexample does not invalidate it.

## 5. The specified Cantor–Bernstein bijections: verified and falsified

For either $i$, $J_iI_i=L$. With $A_0=F\setminus J_i(Y_i)$ and $A=\bigcup_{k\ge0}L^k(A_0)$, one has $A=A_0\sqcup L(A)$. The piecewise map $B_i$ in the source is a bijection: its two branch images are disjoint, because $I_i(a)=J_i^{-1}(b)$ would imply $b=L(a)\in A$. To check surjectivity, given $y\in Y_i$, if $J_i(y)\notin A$, use the second branch. Otherwise $J_i(y)\in A\setminus A_0=L(A)$, and injectivity of $J_i$ gives $y=I_i(a)$ for some $a\in A$. Injection within each branch is immediate.

For $n\ge1$, let $h_n=x_1^n=R(x_0^n)$ and $f_n=h_nx_0$. Their domain distance is exactly one. Each $h_n\in J_i(Y_i)$ has nontrivial support in the open right half, whereas every $L^k(A_0)$ for $k\ge1$ is supported in $[0,2^{-k}]$. Thus $h_n\notin A$. Meanwhile $f_n(1/2)=h_n(1/4)=1/4$, so $f_n\notin H\supseteq J_i(Y_i)$, giving $f_n\in A_0$. This checks both membership decisions and both branch formulas.

The right endpoint character $\chi(g)=\log_2g'(1^-)$ is a homomorphism with $\chi(x_0)=\chi(x_1)=1$. Therefore $|x_0^n|=n$ and $|f_n|=n+1$, by matching the character lower bounds with the written words. The product differences of the images are $(f_n,x_0^{-n})$ for $Y_2$ and $(f_n,-n)$ for $Y_1$. Their sum-metric lengths are exactly $2n+1$. Consequently each specified bijection sends pairs at distance one to pairs at unbounded distance and fails even bornology. The exact number changes under a max product metric, but still diverges.

This rejects those precise canonical bijections. It does not reject every possible Cantor–Bernstein-inspired smoothing, much less every quasi-isometry.

## 6. Additional audit: exact homomorphic horizontal slices

Additional statement received from the parent during this review and independently checked on **2026-10-17 at approximately 20:55 UTC**:

> Let $Y$ be an unbounded metric space. There is no coarsely onto quasi-isometry $\Phi:F\times Y\to F$, for the sum product metric, having exact horizontal slices $\Phi(f,y)=s_y\alpha_y(f)$, where every $\alpha_y:F\to F$ is a group homomorphism and $s_y\in F$.

This statement is correct. Here is a complete proof, including the equalizer and root steps that could otherwise hide an assumption.

**Unique roots.** The group $F$ is bi-orderable directly from its PL geometry. Declare a nonidentity $u$ positive if its slope immediately to the right of its leftmost departure from the identity is greater than one. A finite PL map always has such a first nonidentity affine piece. Products of positive maps are positive: the earliest departure decides, or at a common departure the two slopes multiply. Increasing PL conjugacy preserves the sign and the one-sided slope at this departure. Thus the positive cone is closed under products and conjugacy, and exactly one of $u,u^{-1}$ is positive. It defines a bi-invariant total order. If $a<b$, bi-invariance gives the strict chain

\[
a^n<b a^{n-1}<b^2a^{n-2}<\cdots<b^n \quad(n\ge1).
\]

Therefore $a^n=b^n$ forces $a=b$: $F$ has unique positive roots. This root assertion is not being assumed for arbitrary orientation-preserving homeomorphism groups.

Fix $y_0\in Y$, write $s_0=s_{y_0}$, and set $t_y=s_y^{-1}s_0$. The upper bound on vertical pairs says

\[
|\alpha_y(f)^{-1}t_y\alpha_0(f)|\le Ld_Y(y,y_0)+C \quad\text{for every }f\in F.
\]

Let $\beta_y=\operatorname{Ad}_{t_y}\alpha_0$. The discrepancy $\Delta_y(f)=\alpha_y(f)^{-1}\beta_y(f)$ has finite image: multiplying the bounded expression above by $t_y^{-1}$ increases length by at most $|t_y|$, independently of $f$. Let $E_y=\{f:\alpha_y(f)=\beta_y(f)\}$. It is a subgroup, and

\[
\Delta_y(f)=\Delta_y(g)\quad\Longleftrightarrow\quad gf^{-1}\in E_y.
\]

Thus the fibers of the discrepancy are exactly the right cosets $E_yf$, and $E_y$ has finite index. Each $f\in F$ has a positive power in $E_y$. Applying the homomorphisms and unique roots gives $\alpha_y(f)=\beta_y(f)$ for all $f$. In particular,

\[
\Phi(f,y)=p_f s_y,\qquad p_f=s_0\alpha_0(f)s_0^{-1}.
\]

Put $P=\{p_f:f\in F\}$ and $C_0=C_F(P)$. The horizontal lower quasi-isometry bound confines $\ker\alpha_0$ to a finite ball. Since $F$ is torsion-free, $\alpha_0$ is injective; consequently $P'\ne1$.

Choose the two generators $b=x_0,x_1$. The upper bound on $(1,y),(b,y)$ confines every $s_y^{-1}p_b s_y$ to a fixed finite ball. There are only finitely many resulting tuples. Equal tuples for $s_y,s_z$ are equivalent to $s_zs_y^{-1}\in C_0$, so

\[
\{s_y:y\in Y\}\subseteq\bigcup_{j=1}^k C_0t_j
\]

for finitely many $t_j\in F$. Since $C_0$ centralizes $P$, $Q=PC_0$ is a subgroup, $P\triangleleft Q$, and the image of $\Phi$ lies in $\bigcup_jQt_j$. Coarse density with radius $R$ gives

\[
F=\bigcup_j Qt_j B_R(1),
\]

a finite union of right cosets of $Q$. Hence $Q$ has finite index and contains $F'$. Now $1\ne P'\triangleleft Q$ and $P'\le F'$. It follows that $P'$ is a nontrivial normal subgroup of $F'$, and simplicity gives $P'=F'$. In particular $P\supseteq F'$.

The local bump argument of Section 1, applied throughout $(0,1)$, proves $C_F(F')=1$. Therefore $C_0=1$, and the set of all $s_y$ is finite. Its diameter $D$ is finite, whereas the vertical lower bound at $f=1$ yields

\[
L^{-1}d_Y(y,z)-C\le d_F(s_y,s_z)\le D.
\]

This bounds the diameter of $Y$, a contradiction.

**Boundary checks.** The familiar block embedding $F\times F\hookrightarrow F$ has exact homomorphic slices and is a quasi-isometric embedding, so coarse density is essential in this proof: its $Q$ is contained in the infinite-index midpoint stabilizer. If $Y$ is bounded, projection $F\times Y\to F$ supplies examples, so unboundedness is essential. Without the horizontal lower bound, constant homomorphisms would invalidate the step $P'\ne1$. No unjustified assumption that a finite-index subgroup of a product is itself a product is used. Uniformly bounded perturbations of these exact-slice maps are excluded as a formal consequence, but arbitrary nonalgebraic horizontal maps remain untouched.

## 7. A nonlinear embedding refutes an excessive rigidity premise

At the parent's additional request, independently check the following counterexample to the assertion that every quasi-isometric embedding $F\to F$ is a bounded distance from an affine homomorphism. Let

\[
j:F\times\mathbb Z\longrightarrow F,\qquad j(g,n)=L(g)R(x_0^n),
\qquad \psi(g)=j(g,|g|_F).
\]

Use the classical fact, already cited in the constructive notebook, that the standard block map $j$ is a quasi-isometric embedding; the relevant reference is [Cleary–Taback, *Geometric quasi-isometric embeddings into Thompson's group F*](https://nyjm.albany.edu/j/2003/9-11p.pdf), Theorem 3.4 and the product embedding discussion. The graph map itself satisfies the elementary inequalities

\[
d_F(g,h)\le d_F(g,h)+\big||g|_F-|h|_F\big|\le 2d_F(g,h),
\]

so $\psi$ is a quasi-isometric embedding by composition. Its right endpoint character is exactly

\[
\chi_1(\psi(g))=|g|_F.
\]

Let $w\in F'\setminus\{1\}$, and let $g\mapsto s\alpha(g)$ be any affine homomorphism, with $s\in F$ and $\alpha:F\to F$ a homomorphism. Since $\chi_1\circ\alpha$ is a homomorphism to an abelian group, it kills $F'$. Thus $\chi_1(s\alpha(w^n))=\chi_1(s)$ for every $n$. Torsion-freeness makes the powers of $w$ distinct; properness makes $|w^n|\to\infty$. The 1-Lipschitz endpoint character gives

\[
d_F\big(\psi(w^n),s\alpha(w^n)\big)
\ge \big||w^n|_F-\chi_1(s)\big|\longrightarrow\infty.
\]

For an explicit choice, $w=[x_0,x_1]\ne1$, since $x_0x_1(3/4)=3/8\ne1/2=x_1x_0(3/4)$. This independently verifies that $\psi$ is not a bounded distance from **any** affine homomorphism.

The entire image of $\psi$ lies in $H$, so Section 4 proves it is not coarsely dense. It is therefore a counterexample to the proposed rigidity assertion about *embeddings*, and supplies no counterexample or answer to the two original quasi-isometry questions. It does not by itself settle a more restrictive assertion about coarsely dense maps, though the general exact-slice obstruction cannot simply be promoted by asserting embedding rigidity.

## Reproducibility and precise remaining gap

`partial_adversary01_sources/check_exact_dyadics.py` uses exact rational arithmetic. Its recorded output is `check_exact_dyadics_output.json`. The independent computation passed 32,764 generator depth checks on all reduced dyadics of depth at most 13 and 32,764 inverse identity checks. A radius-10 orbit search found the exact lengths $0,1,\ldots,10$ for $2^{-(n+1)}$. It also checked the explicit sequences and the false-global-Lipschitz counterexample for $1\le n\le128$. These are supplementary finite checks; the general arguments above supply the proofs.

The strongest verified outcome is the collection of restricted exclusions, including the exact homomorphic-slice obstruction. An arbitrary quasi-isometry need not be a homomorphism, lie near one, preserve any coset decomposition, or have homomorphic slices. None of the verified arguments supplies a rigidity theorem forcing such behavior. Therefore **both original questions, $F\simeq_{QI}F\times\mathbb Z$ and $F\simeq_{QI}F\times F$, remain unresolved by this work**. No novelty, priority, or publication claim has been validated by this audit.
