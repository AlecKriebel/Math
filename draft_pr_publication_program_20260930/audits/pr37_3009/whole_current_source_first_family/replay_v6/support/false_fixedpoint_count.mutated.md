# Doubly small homeomorphisms in dimensions one and two

**Status: scoped known-theorem consequence; the full higher-dimensional problem remains unresolved in this attempt.** The planar conclusion follows from established surface dynamics. No novelty is claimed for the reduction below, and no conclusion for arbitrary dimension is asserted.

Problem 3009 / KP-5.2. Original substantive budget: 1/5; new substantive attempts: 0; audit attempts: 0. The original checked-date/model/reasoning/deadline fields are archival only, retained byte-exact in original_archive/. Current runtime model and reasoning are not independently exposed; no current deadline is inferred. A NEW whole-current-packet source-first adversarial gate remains pending.

## 1. Exact target and recurrence topology

[K3, Problem 5.2](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed pp. 302–303, asks whether a homeomorphism $h:\mathbb R^n\to\mathbb R^n$ must be the identity when

1. there is one finite constant $D$ such that every full orbit has diameter at most $D$; and
2. $h^{n_j}\to\mathrm{id}$ in the compact-open topology for a sequence $n_j\to+\infty$.

It also asks the boundary-fixed closed-ball special case. The source separately mentions diffeomorphisms and stronger $C^\infty$ recurrence. These variants must not be conflated. The proof here works in the homeomorphism category for $n\le2$, so it also covers diffeomorphisms in those dimensions without any derivative estimates.

The first hypothesis is equivalent to

$$|h^k(x)-x|\le D\qquad (x\in\mathbb R^n,\ k\in\mathbb Z).\tag{1}$$

One implication uses $k=0$ as the other orbit point. For the converse, apply (1) at $h^\ell(x)$ with exponent $k-\ell$. Compact-open convergence in the second hypothesis means uniform convergence on **each compact set**, not uniform Euclidean convergence on all of $\mathbb R^n$.

## 2. Two imported planar theorems

The argument uses exactly these established results.

- **Cartwright–Littlewood.** An orientation-preserving plane homeomorphism preserving a nonempty compact connected set whose complement is connected has a fixed point in that set. The precise statement is Theorem A in [Boroński, *On a generalization of the Cartwright–Littlewood fixed point theorem for planar homeomorphisms*](https://arxiv.org/pdf/1510.06663), p. 1; its Section 3 describes the classical Brown covering-space proof. The original Cartwright–Littlewood theorem is from 1951; Brown's one-page proof is *Proc. AMS* 65 (1977), 372, as cited by K3. The direct AMS PDF was inaccessible during this check, so it is not represented as having been read.
- **Kolev–Pérouème.** A nonidentity recurrent orientation-preserving homeomorphism of $S^2$ has exactly three fixed points. See [*Recurrent surface homeomorphisms*](https://arxiv.org/pdf/math/0303258), Theorem 1.1, p. 2, and [the 1998 publication](https://doi.org/10.1017/S0305004197002272). Here recurrence means that one sequence of iterates converges uniformly to the identity in a metric on the compact sphere. The current arXiv text is v3, revised 2 March 2009. The boundary-fixed disk consequence is explicitly stated immediately after its theorem in the directly read accessible arXiv v3 (2 March 2009) of the 1998-published paper. The printed 1998 disk passage has not been directly verified. It is not a new result of this attempt.

## 3. Orientation and recurrence at infinity

A plane homeomorphism satisfying $|h(x)-x|\le D$ preserves orientation. Indeed,

$$H_t(x)=(1-t)x+t h(x),\qquad 0\le t\le1,$$

is a proper homotopy from the identity to $h$: $|H_t(x)|\ge|x|-D$ uniformly in $t$. It extends continuously over the one-point compactification, fixing infinity, so $h$ has degree $1$. No claim that the intermediate maps are homeomorphisms is needed.

Let $\widehat h:S^2\to S^2$ be the one-point extension. Under (1), compact-open recurrence of $h$ implies uniform recurrence of $\widehat h$. To see this explicitly, use the chordal metric from stereographic projection:

$$q(x,y)=\frac{2|x-y|}{\sqrt{1+|x|^2}\sqrt{1+|y|^2}}.$$

For $|x|\ge R>D$ and every integer $k$, (1) gives $|h^k(x)|\ge R-D$ and therefore

$$q(h^k(x),x)\le\frac{2D}{\sqrt{1+R^2}\sqrt{1+(R-D)^2}}.\tag{2}$$

The right side tends to zero with $R$, independently of $k$. On the compact disk $|x|\le R$, the chosen iterates converge uniformly in Euclidean distance, hence in $q$. Infinity is fixed. Splitting the sphere into these two regions proves uniform convergence of $\widehat h^{n_j}$ to the identity.

This step uses the global orbit bound. It does not claim that compact-open recurrence by itself is uniform Euclidean recurrence.

## 4. Fixed points occur arbitrarily far out

Assume $D>0$; if $D=0$, (1) already says $h=\mathrm{id}$. Fix $a\in\mathbb R^2$ and put

$$U_a=\bigcup_{k\in\mathbb Z}h^k(B(a,2D)).$$

Each set in the union is connected and intersects the original ball: it contains $h^k(a)$, which lies in $B(a,2D)$ by (1). Consequently $U_a$ is connected. It is open and invariant, and

$$B(a,2D)\subset U_a\subset B(a,3D).$$

The last inclusion follows by applying (1) to every point of the original ball. Its closure $C_a$ is a nonempty compact connected invariant set. Fill all bounded complementary components of $C_a$, obtaining $K_a$. Then $K_a$ is a compact connected set with connected complement and is still contained in $\overline{B(a,3D)}$. For the containment, every point outside that disk connects to infinity without meeting $C_a$ and thus belongs to its unbounded complementary component.

The unbounded complementary component is preserved by $h$, because a plane homeomorphism extends to the one-point compactification and fixes infinity. Hence $h(K_a)=K_a$. Cartwright–Littlewood now gives

$$\operatorname{Fix}(h)\cap\overline{B(a,3D)}\ne\varnothing\qquad\text{for every }a\in\mathbb R^2.\tag{3}$$

Taking two centers more than $6D$ apart gives two distinct finite fixed points. Together with infinity, $\widehat h$ has at least three fixed points. Section 3 makes it an orientation-preserving recurrent sphere homeomorphism. Kolev–Pérouème therefore forces $\widehat h=\mathrm{id}$ and hence $h=\mathrm{id}$.

**Planar conclusion.** Part (a) of KP-5.2 has an affirmative answer in dimension $2$. The argument is an explicit consequence of the imported classical theorems, with no assumption of equicontinuity or compact closure of the cyclic subgroup.

## 5. Closed balls and dimension one

For a boundary-fixed homeomorphism $h$ of the closed disk $\overline{B^2}$, extend $h$ by the identity outside the disk. This is a plane homeomorphism. Its full orbits have diameter at most $2$ and its compact-open recurrence follows from uniform convergence on the compact closed disk. The planar conclusion applies. Equivalently, this is the disk corollary directly read in Kolev–Pérouème's accessible arXiv v3 (2009) of the 1998-published paper; the printed 1998 disk passage remains unverified.

This extension is used only in the homeomorphism category. A diffeomorphism of a closed ball that is the identity on the boundary need not glue smoothly to the exterior identity without extra matching conditions. No such smooth gluing is asserted or needed here.

On $\mathbb R$, a homeomorphism satisfying the global displacement bound cannot reverse orientation, since a decreasing surjection has $h(x)\to-\infty$ as $x\to+\infty$. It is therefore increasing. If $h(x)>x$ for some $x$, every positive iterate satisfies $h^m(x)\ge h(x)>x$, contradicting recurrence at $x$; the case $h(x)<x$ is analogous. Thus $h=\mathrm{id}$. An interval homeomorphism fixing both endpoints is also increasing, so the same argument proves the one-dimensional boundary-fixed case.

## 6. Why this does not settle the higher-dimensional question

The exact planar mechanism is the nonseparating-continuum fixed-point theorem together with the two-fixed-point restriction on recurrent sphere homeomorphisms. Neither is supplied in the required form for higher dimensions. The higher-dimensional sphere can have nontrivial recurrent rotations with many fixed points, so merely repeating the last fixed-point count is invalid.

Recurrence is weaker than equicontinuity of all iterates. The introduction of Kolev–Pérouème explicitly discusses nonregular recurrent surface homeomorphisms and cites Fokkink–Oversteegen's construction. A sequence returning to the identity supplies no uniform modulus of continuity for all intervening powers. Thus neither Arzelà–Ascoli nor averaging over a compact group is available from the stated assumptions alone.

The source's comparison with Hilbert–Smith explicitly adds compact closure of the cyclic subgroup. That extra hypothesis cannot be silently inserted. In particular, [Pardon's established three-dimensional Hilbert–Smith theorem](https://arxiv.org/abs/1112.2324) assumes a locally compact acting group; it does not supply the missing compactness or local compactness of this cyclic closure. Likewise, the known periodic case attributed by K3 to Newman's theorem does not turn a recurrent map into a periodic one. No proof of such a reduction was obtained here, including in the stronger smooth-recurrence category in dimensions at least $3$.

A related citation requires special care: Oversteegen–Tymchatyn's 1990 theorem titled *Recurrent homeomorphisms on $\mathbb R^2$ are periodic* uses uniform recurrence for the Euclidean metric on the entire plane. It is not a direct theorem about arbitrary compact-open recurrence on a noncompact domain. The present proof avoids that substitution by proving (2) and then using the compact-sphere theorem.

**Disposition:** the complete target remains unresolved in this attempt. The saved result is an explicit, credited low-dimensional consequence and a precise account of the missing higher-dimensional mechanism. Finite algebraic checks of (2) cannot certify any of the global topological theorems. No new discovery, exhaustive novelty audit, or full solution is claimed.
