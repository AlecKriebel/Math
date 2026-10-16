# A descent interpretation for signed adjacent-sum polytopes

**Problem:** UnsolvedMath 30003813 / OWR-16164-005.  
**Date:** 2026-10-03.  
**Status:** Claimed solved (1/5); independent mathematical audit PASS.  
**Attribution:** An explicit application of classical order-polytope and
P-partition theory; no novelty claim.

## 1. Target and scope

For an integer $n\geq 1$ and signs

$$
\varepsilon=(\varepsilon_1,\ldots,\varepsilon_{n-1})\in\{-,+\}^{n-1},
$$

let

$$
Q_\varepsilon=\{x\in[0,1]^n:
 x_i+x_{i+1}\leq1\text{ if }\varepsilon_i=-,
 \quad x_i+x_{i+1}\geq1\text{ if }\varepsilon_i=+\}.
$$

We give a finite permutation-statistic interpretation of every coefficient of

$$
h^*_{Q_\varepsilon}(z)
 =(1-z)^{n+1}\sum_{m\geq0}|mQ_\varepsilon\cap\mathbb Z^n|z^m.
\tag{1}
$$

The exact original question appears at the end of Matthieu Josuat-Vergès's
joint-work abstract with Arvind Ayyer and Sanjay Ramassamy, printed page 1410
of the 2018 Oberwolfach report (PDF page 30). Its final sentence is:

> The problem is to understand what is the combinatorics of the
> h*-polynomial of these polytopes.

The preceding definition is precisely the adjacent-sum family above. The
source does not specify which sign denotes which inequality, so the convention
here is stated explicitly. The certificate addresses the literal request for
a combinatorial interpretation. It does not supply a statistic on the original
cyclic-order objects, a new swap statistic, or a claim that the authors' broader
research program is completed. It does not assert that a new theorem has been
discovered or that a published paper explicitly closed this OWR question.

## 2. Explicit answer using only permutations

For a permutation $\sigma\in S_n$, write

$$
\operatorname{Des}(\sigma)
 =\{i\in\{1,\ldots,n-1\}:\sigma(i)>\sigma(i+1)\},
 \qquad \operatorname{des}(\sigma)=|\operatorname{Des}(\sigma)|.
$$

From the sign sequence form the subset

$$
D_\varepsilon
 =\{i:\ i\text{ is odd and }\varepsilon_i=+\}
 \cup
 \{i:\ i\text{ is even and }\varepsilon_i=-\}.
\tag{2}
$$

Choose any one permutation $\alpha\in S_n$ with

$$
\operatorname{Des}(\alpha)=D_\varepsilon.
\tag{3}
$$

An explicit construction of such an $\alpha$ is given below, so this choice
does not require solving any other problem.

**Theorem.** For every $n\geq1$, every sign sequence $\varepsilon$, and
every choice in (3),

$$
\boxed{
h^*_{Q_\varepsilon}(z)
 =\sum_{\substack{\sigma\in S_n\\
              \operatorname{Des}(\sigma)=D_\varepsilon}}
   z^{\operatorname{des}(\alpha\circ\sigma^{-1})}.
}
\tag{4}
$$

Composition in (4) means that the one-line word being measured is

$$
\alpha(\sigma^{-1}(1)),\ldots,\alpha(\sigma^{-1}(n)).
$$

In particular the coefficient of $z^k$ counts the permutations with descent
set exactly $D_\varepsilon$ for which that word has exactly $k$ descents.
The polynomial in (4) is independent of the chosen $\alpha$.

## 3. The oriented path and its natural labels

On the vertices $1,\ldots,n$, orient every path edge by the rules

$$
\begin{array}{c|cc}
 &\varepsilon_i=-&\varepsilon_i=+\\ \hline
i\text{ odd}&i\prec i+1&i+1\prec i\\
i\text{ even}&i+1\prec i&i\prec i+1.
\end{array}
\tag{5}
$$

Let $P_\varepsilon$ be the partial order obtained by taking the transitive
closure. An oriented path has no directed cycle: a directed cycle would give
an undirected cycle in the path. Thus this is a partial order.

A **linear-extension word** $w=(w_1,\ldots,w_n)$ lists all vertices, with
each smaller element before every larger comparable element. A **natural
labeling** $\omega:P_\varepsilon\to\{1,\ldots,n\}$ is an order-preserving
bijection. Equivalently, $\omega$, viewed as the one-line permutation

$$
\omega(1),\ldots,\omega(n),
$$

has descent set exactly $D_\varepsilon$. The equivalence holds because
(5) gives all generating comparisons; satisfying them implies satisfying
their transitive closure.

For a deterministic natural labeling, repeatedly remove the minimal vertex
with the smallest original index and assign it the next available label.
A nonempty finite acyclic graph always has a vertex with no predecessor, so
this algorithm terminates and gives the required $\alpha$ in (3).

Define

$$
d_\omega(w)=\#\{j\in\{1,\ldots,n-1\}:\omega(w_j)>\omega(w_{j+1})\}.
\tag{6}
$$

We will prove the equivalent identity

$$
h^*_{Q_\varepsilon}(z)=
\sum_{w\text{ a linear-extension word of }P_\varepsilon}z^{d_\omega(w)}.
\tag{7}
$$

Indeed, the order-preserving bijection $\sigma$ associated to $w$ is
defined by $\sigma(w_j)=j$. Thus $w_j=\sigma^{-1}(j)$, and setting
$\omega=\alpha$ turns (7) into (4).

## 4. Reflection identifies an order polytope

Consider the affine map $T:\mathbb R^n\to\mathbb R^n$ given by

$$
y_i=T(x)_i=\begin{cases}
x_i,&i\text{ odd},\\
1-x_i,&i\text{ even}.
\end{cases}
\tag{8}
$$

Its linear part is diagonal with entries $1,-1,1,-1,\ldots$, and its
translation vector is integral. It is its own inverse and is a lattice
automorphism. Direct substitution gives

$$
x_i+x_{i+1}-1
 =\begin{cases}
y_i-y_{i+1},&i\text{ odd},\\
y_{i+1}-y_i,&i\text{ even}.
\end{cases}
\tag{9}
$$

Consequently, the four cases in (5) are exactly the transformed inequalities,
and

$$
T(Q_\varepsilon)=O(P_\varepsilon)
 =\{y\in[0,1]^n:y_a\leq y_b\text{ whenever }a\prec b\}.
\tag{10}
$$

For completeness, this polytope is full-dimensional and integral. For each
linear-extension word $w$, the region

$$
0\leq y_{w_1}\leq\cdots\leq y_{w_n}\leq1
\tag{11}
$$

is a full-dimensional simplex with integral vertices: the zero vector and
the indicator vectors of the suffixes of $w$. Its interior is nonempty,
for example at $y_{w_j}=j/(n+1)$. Every point of the order polytope lies in
one of these simplices: sort its coordinates increasingly and break ties
using any natural labeling. A comparable pair is then ordered correctly.
This is a finite union of integral simplices and is convex, so it equals
the convex hull of their integral vertices. Reflection proves the same
properties for $Q_\varepsilon$.

One must use the appropriate translated map on dilates. For every integer
$m\geq0$, define

$$
T_m(x)_i=\begin{cases}
x_i,&i\text{ odd},\\
m-x_i,&i\text{ even}.
\end{cases}
\tag{12}
$$

Equation (9), with the constant 1 replaced by $m$, shows that $T_m$ is a bijection

$$
mQ_\varepsilon\cap\mathbb Z^n
\longleftrightarrow
\{y\in\{0,\ldots,m\}^n:y_a\leq y_b\text{ for }a\prec b\}.
\tag{13}
$$

This also holds for $m=0$, where both sets contain only the zero vector.

## 5. A disjoint lattice-point partition and the descent weight

Fix a natural labeling $\omega$. For an integer point $y$ in the
right-hand set of (13), order the vertices by the lexicographic keys

$$
(y_v,\omega(v)).
$$

This gives one unique linear-extension word $w$. If $a\prec b$, either
$y_a<y_b$, or $y_a=y_b$ and $\omega(a)<\omega(b)$, so $a$ occurs
before $b$.

The integer points assigned to a particular $w$ are exactly the sequences

$$
0\leq a_1\leq\cdots\leq a_n\leq m,
\qquad a_j<a_{j+1}\text{ whenever }\omega(w_j)>\omega(w_{j+1}),
\tag{14}
$$

where $a_j=y_{w_j}$. Necessity follows from the tie-breaking rule.
Conversely, every sequence in (14) is order-preserving on $P_\varepsilon$,
since $w$ is a linear extension. Within each block of equal $a_j$'s,
the labels must be increasing: otherwise some adjacent label pair in the
block would be a descent, contradicting its required strict inequality.
Thus sorting reconstructs exactly $w$. This proves both exhaustion and
disjointness, including every boundary point.

Let $d=d_\omega(w)$. Subtract from $a_j$ the number of required strict
steps before position $j$. This gives a bijection from (14) to weakly
increasing sequences of $n$ integers in $\{0,\ldots,m-d\}$. Their number
is

$$
\binom{m+n-d}{n}\quad(m\geq d),
$$

and it is zero if $m<d$. Equivalently, the $n+1$ endpoint and successive
gaps become nonnegative integers summing to $m-d$. Hence

$$
|mQ_\varepsilon\cap\mathbb Z^n|
 =\sum_w\binom{m+n-d_\omega(w)}{n},
\tag{15}
$$

where summands with $m<d_\omega(w)$ are zero. The ordinary generating
function for the summand indexed by $w$ is

$$
\sum_{m\geq d}\binom{m+n-d}{n}z^m
 =\frac{z^d}{(1-z)^{n+1}}.
\tag{16}
$$

Summing (16) and using (1) proves (7) and (4).

This argument works for **every** natural labeling. The left side of (7)
does not depend on a labeling, so the descent enumerator is independent of
the choice. Individual words need not retain their descent counts when
labels change; the assertion is equality of the distributions. This proves
the labeling-invariance part of the theorem. □

## 6. Boundary cases and examples

- If $n=1$, the sign word and descent set are empty. There is one permutation,
  and $h^*_{[0,1]}(z)=1$.
- If $n=2$, either sign gives an integral triangle, and (4) gives $h^*=1$.
- Alternating signs give a consistently oriented path, hence a total order.
  There is one linear extension, so $h^*=1$. This includes both starting signs.
- For $n=3$ and signs $--$, the order is $1\prec2\succ3$.
  A natural labeling is $(1,3,2)$. Its extension words are $132$ and $312$,
  with label words $123$ and $213$; therefore $h^*=1+z$.
- The original vertex indices are generally **not** natural labels. Counting
  their raw descents in those same words would incorrectly give $2z$.
- For $n=4$ and signs $--+$, the relations are $1\prec2\succ3\succ4$.
  The extension words $1432,4132,4312$, under natural labeling $(1,4,3,2)$,
  give label words $1234,2134,2314$. Thus $h^*=1+2z$. In particular,
  arbitrary signed cases need not have palindromic $h^*$.

Complementing all coordinates sends $Q_\varepsilon$ to $Q_{-\varepsilon}$;
reversing their order sends it to $Q_{\operatorname{rev}(\varepsilon)}$.
Both are affine lattice bijections on every dilation, so their $h^*$
polynomials agree. Nonnegativity of every coefficient follows directly from
(4); its constant coefficient is one because the only increasing label word
is $1,\ldots,n$, which corresponds to the chosen natural labeling itself.

## 7. Attribution and literature boundary

The method uses Stanley's established theory. The order-polytope definition,
integrality, canonical simplices, and order-polynomial connection appear in
**Stanley, Two poset polytopes** (1986), Definition 1.1, Corollary 1.3,
Theorem 4.1, and Section 5. The natural-label descent generating function is
Stanley's P-partition formula, cited as **Enumerative Combinatorics**, volume 1,
second edition, Theorem 3.15.8. A directly checked primary-paper restatement
is **Coons and Sullivant** (2023), Theorem 16, PDF page 8. Sections 4 and 5
above give a self-contained specialization with all sign and labeling
conventions explicit.

**Ayyer, Josuat-Vergès and Ramassamy** (2020) treat these signed polytopes
under the notation $\widetilde B_s$, with their sign convention reversed from ours and
their sign-word length one smaller than the dimension. Their Theorem 2.5
gives integrality and normalized volume in terms of cyclic orders. Their
Theorem 2.9 supplies a descent interpretation for the separate family
$B_{I,n}$ defined with upper bounds on consecutive sums. It is not cited
here as a signed-family $h^*$ theorem. Their Remark 2.6 does not preclude
an affine equivalence to an order polytope.

The literature check did not locate a paper explicitly identifying (4) as
the resolution of the OWR signed question. The certificate is therefore
presented as a classical-corollary answer to its literal target, not as a
historically established closure or a novel contribution.

### Sources

1. M. Josuat-Vergès, joint with A. Ayyer and S. Ramassamy, *Enumeration of cyclic
   orders and consecutive coordinates polytopes*, in *Enumerative Combinatorics*,
   Oberwolfach Reports **15** (2018), printed pp. 1408-1410; question on p. 1410.
   [Official report](https://publications.mfo.de/bitstream/handle/mfo/3645/OWR_2018_23.pdf?isAllowed=y&sequence=1).
   [Publisher record](https://ems.press/journals/owr/articles/16164).
2. R. P. Stanley, *Two poset polytopes*, Discrete & Computational Geometry
   **1** (1986), 9-23, DOI 10.1007/BF02187680.
   [Author-hosted paper](https://math.mit.edu/~rstan/pubs/pubfiles/66.pdf).
3. J. I. Coons and S. Sullivant, *The h-star polynomial of the order polytope of the
   zig-zag poset*, Electronic Journal of Combinatorics **30**(2) (2023), P2.44,
   DOI 10.37236/11526. Theorem 16 restates Stanley's general formula.
   [Published paper](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p44/pdf/).
4. A. Ayyer, M. Josuat-Vergès and S. Ramassamy, *Extensions of partial cyclic
   orders and consecutive coordinate polytopes*, Annales Henri Lebesgue **3**
   (2020), 275-297, DOI 10.5802/ahl.33, Theorems 2.5 and 2.9 and Remark 2.6.
   [Published paper](https://ahl.centre-mersenne.org/item/10.5802/ahl.33.pdf).

## 8. Reproducible finite checks

Run `python3 verify.py --max-n 8 --output verification.json` using Python 3.
No third-party dependencies or network access are needed.

The test enumerates every sign pattern in dimensions 1 through 8, compares
two natural-label descent distributions with integer counts in the original
adjacent-sum coordinates, and checks the binomial identity (15). It also
checks the pointwise reflection and tie-breaking rule on every grid point
for dimensions at most 5 and dilations 0 through 4. A negative control
demonstrates why the unrelabeled original vertex labels are invalid.

The recorded run passed 255 sign patterns, 46,233 permutation words,
2,558 Ehrhart evaluations, 79,657 pointwise reflection checks, and 12,195
tie-sorting checks. These are modest finite checks; the proof in Sections
3-5, rather than the computations, establishes the formula for all $n$.
