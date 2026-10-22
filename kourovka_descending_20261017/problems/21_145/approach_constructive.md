# Constructive quasi-isometry search for Kourovka 21.145

Author of this research notebook: independent work in Alec Kriebel's project (ORCID https://orcid.org/0009-0001-9320-500X).

## Scope and success criteria

The two targets are (a) a quasi-isometry between the finitely generated group $F$ and $F\times\mathbb Z$, and (b) a quasi-isometry between $F$ and $F\times F$. The product metric here is the sum of standard word metrics. A successful construction must give a well-defined map, uniform two-sided distance bounds, and a uniform coarse-surjectivity radius. A product subgroup embedding alone cannot settle either question.

This notebook deliberately develops explicit constructions before consulting any other approach team's verdicts. It records only this route. No external communication, branch changes, commits, or pushes were made by its author.

## 2026-10-17 20:49 UTC checkpoint

Discovery completion estimate: **5%** for each target. Status: no quasi-isometry construction established.

Primary references checked:

* [Cleary–Taback, *Geometric quasi-isometric embeddings into Thompson's group F*, NYJM 9 (2003), 141–148](https://nyjm.albany.edu/j/2003/9-11p.pdf): Theorem 2.1 gives $N(w)-2\le |w|\le4N(w)-4$ for reduced tree pairs, and Theorem 3.4 gives product subgroup embeddings. Their introduction explicitly discusses Bridson's $F\times\mathbb Z$ question. These are embeddings, not a coarse-surjectivity assertion.
* [Belk–Brown, *Forest diagrams for elements of Thompson's group F*](https://pi.math.cornell.edu/~kbrown/papers/Forest.pdf): Theorem 4.2.2 expresses word length as caret count plus weights on spaces. This makes pointer normalization plausible, but it supplies no product metric estimate for such a normalization.
* [Burillo–Cleary–Stein, *Metrics and embeddings of generalizations of Thompson's group F*](https://arxiv.org/abs/math/9809185): reduced tree size is comparable to word length. No additional metric equivalence is assumed below.

## Conventions for checkable constructions

Multiplication is composition, $fg=f\circ g$. Set

$$x_0(t)=\begin{cases}t/2&0\le t\le1/2,\\t-1/4&1/2\le t\le3/4,\\2t-1&3/4\le t\le1,\end{cases}$$

and let $x_1$ be the right-half clone of $x_0$: identity on $[0,1/2]$, and $x_1(t)=1/2+x_0(2t-1)/2$ on $[1/2,1]$. These are the usual two generators up to the standard composition convention.

Write $L(f)=f\oplus1$ and $R(f)=1\oplus f$ for left/right affine clones. The map

$$J_2:F\times F\longrightarrow F,\qquad J_2(a,b)=a\oplus b$$

has image $H=\operatorname{Stab}_F(1/2)$. The map

$$J_1:F\times\mathbb Z\longrightarrow F,\qquad J_1(a,n)=a\oplus x_0^n$$

is likewise an injection; its image is a subgroup of $H$. Both are the familiar product embedding mechanism, not a new result.

## Construction family A: fixed root splitting

**Mechanism.** Split a reduced tree pair at the root; read its two subpairs as coordinates in $F\times F$. Equivalently, use $J_2^{-1}$.

**Exact gap.** This is defined directly only on $H$. In a general tree pair, source and target left subtrees need not have the same number of leaves. Refinement cannot repair the underlying obstruction $f(1/2)\ne1/2$. Treating every pair as two independent subpairs is therefore not a map on all of $F$.

**Quantitative failure of coarse surjectivity.** For an interior dyadic rational $q$, write $\delta(q)$ for its reduced denominator exponent: $q=m/2^{\delta(q)}$, $m$ odd. Directly from the displayed generators and their inverses,

$$\delta(s(q))\le\delta(q)+1\quad(s\in\{x_0^{\pm1},x_1^{\pm1}\}).$$

For depths at least three this follows immediately from slope/intercept formulas; the finitely many dyadics of depths one and two are checked separately. Consequently a word of length $r$ sends $1/2$ to a dyadic of depth at most $r+1$.

For $g_n=x_0^{-n}$ and every $h\in H$, the element $u=g_n^{-1}h=x_0^n h$ satisfies

$$u(1/2)=2^{-(n+1)},\qquad |u|\ge n.$$

Taking $h=1$ gives the reverse inequality, so

$$\boxed{d_F(x_0^{-n},H)=n.}$$

Thus neither fixed-block product embedding is coarsely onto. The same ray also rules out any proposed image contained in this fixed point stabilizer. This is an elementary rejection certificate, not an obstruction to arbitrary nonhomomorphic quasi-isometries.

## Construction family B: Cantor–Bernstein / Hilbert-hotel absorption

**Mechanism.** There are injections both ways: $I_2(f)=(f,1)$ and $J_2$ for the square, or $I_1(f)=(f,0)$ and $J_1$ for the cyclic product. Since $J_iI_i=L$, apply the ordinary set-theoretic Cantor–Bernstein construction and hope it respects distance.

For either target $Y_i$, define

$$A_0=F\setminus J_i(Y_i),\qquad A_{k+1}=L(A_k),\qquad A=\bigcup_{k\ge0}A_k,$$

and the actual bijection

$$B_i(f)=\begin{cases}I_i(f)&f\in A,\\J_i^{-1}(f)&f\notin A.\end{cases}$$

The second branch is defined because $f\notin A_0$ implies $f\in J_i(Y_i)$. The standard disjoint-chain argument establishes bijectivity. This is a concrete globally onto candidate, unlike a bare product embedding.

**Falsification, with exact distances.** Let $h_n=x_1^n=R(x_0^n)$, $n\ge1$, and $f_n=h_nx_0$. Then $d_F(h_n,f_n)=1$. The element $h_n$ lies in $J_i(Y_i)$, while every $A_k$ with $k\ge1$ is supported in $[0,2^{-k}]$. Since $h_n$ has nontrivial support in the right half, $h_n\notin A$. Meanwhile

$$f_n(1/2)=h_n(1/4)=1/4,$$

so $f_n\notin H$, hence $f_n\in A_0$. Therefore

$$B_2(h_n)=(1,x_0^n),\quad B_2(f_n)=(x_1^nx_0,1),$$

and

$$B_1(h_n)=(1,n),\quad B_1(f_n)=(x_1^nx_0,0).$$

The right endpoint slope character $\chi(f)=\log_2 f'(1^-)$ takes both generators to $1$, so it is $1$-Lipschitz for word length. It proves $|x_0^n|=n$ and $|x_1^nx_0|=n+1$, matching the displayed words. Thus for **both** candidates,

$$\boxed{d_{Y_i}(B_i(h_n),B_i(f_n))=2n+1\quad\text{while}\quad d_F(h_n,f_n)=1.}$$

**Status: blocked.** The canonical Cantor–Bernstein bijection is not even bornologous. Mutual undistorted embeddings do not license this gluing. Reopening requires a materially new construction that smooths these partition boundaries uniformly; relabeling the existing copies gives no progress.

## 2026-10-17 20:54 UTC checkpoint

Discovery completion estimate: **8%** for each original target; no positive construction or full negative obstruction established. Several natural construction mechanisms now have exact rejection certificates. These percentages describe exploratory progress, not confidence that either target answer is negative.

### Construction family C: endpoint-height / forest-pointer normalization

**Mechanism.** Let $\eta(f)=-\log_2 f'(0^+)$ and $K=\ker\eta$. Since $\eta(x_0)=1$ and $\eta(x_1)=0$, both orders of factorization give set-theoretic bijections between $K\times\mathbb Z$ and $F$:

$$\Psi_R(k,n)=kx_0^n,\qquad \Psi_L(k,n)=x_0^n k.$$

Give $K$ its metric inherited from $F$. Identifying $K$ with $F$ is an additional unsupported step; it is not assumed. Even before that step, the displayed product metric straightening fails.

**Left placement: exact vertical distortion.** Put $k_m=x_1^m$. The two inputs $(k_m,0)$ and $(k_m,1)$ have product distance $1$, but their images have distance

$$|k_m^{-1}x_0 k_m|=2m+1.$$

For a direct proof of equality, the displayed word gives the upper bound. Each standard generator and inverse has every slope between $1/2$ and $2$, so a word of length $r$ has every slope between $2^{-r}$ and $2^r$. Put $q_m=1-2^{-(m+2)}$. Immediately to the right of $q_m$, the three factors in $k_m^{-1}x_0 k_m$ have slopes $2^m$, $2$, and $2^m$, respectively: $k_m(q_m)=3/4$, $x_0(3/4)=1/2$, and $k_m^{-1}$ has right slope $2^m$ at $1/2$. Thus the conjugate has a slope $2^{2m+1}$, proving the matching lower bound.

**Right placement: unbounded horizontal distortion.** Inputs $(1,n)$ and $(x_1,n)$ have distance $1$. Their image distance is

$$|x_0^{-n}x_1x_0^n|.$$

This conjugate is supported on $[1-2^{-(n+1)},1]$ and has a genuine breakpoint at $1-2^{-(n+3)}$. Its reduced denominator depth is $n+3$. A word of length $r\ge1$ has all breakpoint depths at most $r+2$: the generators have depths at most $3$, and on right multiplication every old breakpoint is pulled back through one generator, increasing depth by at most one. Hence the image distance is at least $n+1$; the displayed word gives an upper bound $2n+1$. Unboundedness alone rejects the candidate.

The inverse right normalization also fails the upper bound: the adjacent inputs $x_0^{-n}$ and $x_0^{-n}x_1$ have the same height $-n$, while their normalized $K$ coordinates are $1$ and $x_0^{-n}x_1x_0^n$.

**Status: blocked.** These are set bijections with a warped metric, not product quasi-isometries. Reopening requires a normalization that controls the conjugation uniformly. Moving the height coordinate to the other end does not do so.

### Construction family D: variable-depth cloning plus compensation

**Mechanism tested.** Let $\phi$ be the right shift $\phi(x_i)=x_{i+1}$. One may try $\phi^n(f)x_0^{-n}$, hoping the added $x_0^{-n}$ cancels the depth cost. For $n\ge1$,

$$x_0^n\phi^n(x_0)x_0^{-n}=x_0x_1x_0^{-1},\qquad
x_0^n\phi^n(x_1)x_0^{-n}=x_1.$$

Thus the endomorphism $\theta(f)=x_0^n\phi^n(f)x_0^{-n}$ is independent of $n\ge1$, and

$$\phi^n(f)x_0^{-n}=x_0^{-n}\theta(f).$$

The apparent depth compensation reduces exactly to a fixed clone followed by an endpoint-height factor. At the same depth, the horizontal metric is controlled, but changing depth reintroduces vertical conjugation. Explicitly, take $f=x_1^m$ and depths $1,2$. Since $\theta(x_1)=x_1$, these adjacent product inputs have images $x_0^{-1}x_1^m$ and $x_0^{-2}x_1^m$, whose distance is

$$|x_1^{-m}x_0^{-1}x_1^m|=|x_1^{-m}x_0x_1^m|=2m+1.$$

The first equality here is equality of word lengths, because the two displayed elements are inverses. Conjugating on both sides instead erases the $n$ coordinate entirely. Failure already on the positive-depth subset rules out extending this formula to a quasi-isometry on a product with $\mathbb Z$.

**Status: blocked in this form.** A valid recursive redistribution must depend on both coordinates in a substantially more flexible way, and must pass uniform adjacent-point tests, including the family $x_1^m,x_1^mx_0$.

### Exact computation supplement

The self-contained `constructive_checks.py` implements composition and inversion of finite PL maps over rational numbers, with no floating-point arithmetic. Running it checks the generator dyadic-depth inequality on all reduced dyadics of depths $1$ through $11$ (8,188 generator applications), and the conjugation, endpoint slopes, and breakpoint formulas for $1\le n\le40$. All assertions passed at this checkpoint. `constructive_checks_output.json` records sample values. These finite checks supplement the general arguments above and establish no claim about the original quasi-isometry questions.

### Moving-cut route and coordination

Before reading any other route's notes, this author independently found the same elementary obstruction to untwisted coset-section coordinates as the root researcher: finite conjugated-generator tuples control one multiplication order, while local supports give unbounded conjugacy in the other. On receiving the root's message at approximately 20:52 UTC, this author redirected away from duplicating that proof. The more flexible possibility of genuinely coordinate-dependent, nonhomomorphic compensation remains open.

## 2026-10-17 20:55 UTC checkpoint: a broader restricted obstruction

Discovery completion estimate remains **8%** for both original questions. The complete deduction in `constructive_affine_obstruction.md` rules out every coarsely onto quasi-isometric map $F\times Y\to F$ whose horizontal slices have the form $s_y\alpha_y(f)$, where each $\alpha_y:F\to F$ is a homomorphism and $Y$ is any unbounded metric space. The homomorphisms may vary with $y$. The argument also rules out uniform bounded perturbations of this family. The file was frozen at 20:55 UTC for fresh adversarial verification.

This does not classify general quasi-isometric embeddings of $F$ into itself. Indeed, the root researcher supplied a counterexample to any naive affine classification: composing the bilipschitz graph embedding $g\mapsto(g,|g|)$ with the block embedding $F\times\mathbb Z\hookrightarrow F$ yields a quasi-isometric embedding whose right endpoint slope is $|g|$. Along powers of a nontrivial commutator, this is unbounded, whereas the endpoint character of an affine homomorphism is constant. Thus no automatic passage from arbitrary quasi-isometry fibers to affine fibers is justified.

At 20:56 UTC, this author also independently opened the primary [Gili Golan preprint, *Every copy of Thompson's group F in F is undistorted*, arXiv:2608.17193v1, submitted 17 August 2026](https://arxiv.org/abs/2608.17193). Its announced result concerns injective copies of $F$, and supplies no coarse-surjectivity assertion for either product. The fresh theorem does not repair any of the rejected constructions here; the obstruction above does not depend on it.
