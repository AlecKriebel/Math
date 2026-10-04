# Independent source-first formulation and controls

Author: independent adversarial audit agent. Frozen target: `c683fc4b84266a6a153c087e182cf427ed502d6c`. Written before opening any candidate or prior reviewer result. All raw documents, extraction, and renderings remain in ignored `tmp/`.

## Primary statement, normalization, and scope

Fresh primary reads: [OWR 22/2022](https://ems.press/content/serial-article-files/46961), printed pp. 1227–1228; [Liu–Mubayi–Reiher](https://homepages.math.uic.edu/~mubayi/papers/XizhiReiherInduced.pdf), definitions p. 1, Construction 1.9 pp. 5–6, Theorem 1.16 / Conjecture 1.17 / Theorem 1.18 p. 10; [Pikhurko–Razborov](https://pikhurko.github.io/E/PikhurkoRazborov17cpc.pdf), construction pp. 139–140 and Theorem 1.1 p. 140. Exact hashes and extraction diagnostics are in `source_metadata.json`. Rendered originals were inspected to resolve extraction artifacts.

For a finite simple graph, `p=e(G)/binom(n,2)` and `c=N_ind(C4,G)/binom(n,4)`, counting four-vertex subsets. In a graphon this is the probability that four independent sampled vertices induce a graph isomorphic to C4; the probability of one specified labeled cycle with two specified diagonals absent is `c/3`. Thus `N_ind(C4,G)=c*n^4/24+o(n^4)`. The unrestricted hypothesis is `I(C4,p)=F(p)` for every `p>1/2`, with limiting endpoint versions at `p=1/2,1`. It is an existence/value hypothesis, not uniqueness or a claim that all triangle minimizers are themselves C4 maximizers.

OWR Conjecture 11 gives the same high-density hypothesis; its Theorem 12 cites an earlier-version theorem number and contains the textual mislabel “Theorem 11.” The freshly retrieved LMR version instead numbers the conjecture 1.17 and the critical-density upper theorem 1.18. This discrepancy is bibliographic, not mathematical.

LMR proves `I(C4,p)=3p^2/2` for `0<=p<=1/2`, and proves `I(C4,p)<=3p(1-p)^2` for `1/2<=p<=1`, tight at `p=1-1/k`. These are external premises; this audit has not reconstructed their general flag-algebra/symmetrization proofs. PR Theorem 1.1 is another external premise: for every epsilon there are delta and n0, uniformly over the actual edge density a, such that every graph with triangle density at most `g3(a)+delta` is within `epsilon*binom(n,2)` adjacency changes of its described family H(a,n). The family has `t-1` independent classes of asymptotic mass c joined completely to one triangle-free block of mass `s=1-(t-1)c`, whose internal edge density tends to `2c(1-tc)/s^2<=1/2`. The clique density theorem identifies `g3` with the construction's triangle density. I rely on these credited theorems, not a purported independent full proof.

## Independently reconstructed all-part-count optimization

For complete multipartite part masses `a_i>=0`, `sum a_i=1`, put `q=1-p=sum a_i^2`. A C4 has two vertices in each of two distinct classes, so

`c=6*sum_{i<j} a_i^2 a_j^2=3(q^2-sum a_i^4)`.

Maximizing c is minimizing the fourth moment with fixed first and second moments. This includes all finite part counts, with zero classes deleted.

Here is a proof that also covers diverging numbers of classes. Sort parts decreasingly. The compact closure of all finite vectors consists of decreasing nonnegative sequences with sum at most one. There is uniform second-moment tail bound `sum_{i>N}a_i^2<=a_(N+1)<=1/(N+1)`; fourth moments have uniform tails too. Consequently an attained minimum exists in that closure at fixed q>0. If it has dust `d=1-sum a_i>0`, choose any positive entry a, decrease it to a-epsilon, and add `b=sqrt(2a*epsilon-epsilon^2)`. The second moment is unchanged and the total mass increase `b-epsilon` is below d for small positive epsilon. The fourth moment changes by `-4a^3*epsilon+O(epsilon^2)<0`. Hence no minimizer has dust.

If all its positive entries are equal, there are finitely many. Otherwise choose two unequal entries to provide rank two for the constraints. Finite-coordinate variations and the implicit-function theorem give common Lagrange multipliers with

`4a_i^3-2lambda*a_i-mu=0`.

The cubic has no quadratic term and therefore at most two positive roots (three positive roots would have positive sum). Thus infinitely many positive entries are impossible, since every entry belongs to a finite set bounded away from zero. The minimizer has finite support.

If the two roots are `x>y>0`, subtracting their equations gives `lambda=2(x^2+xy+y^2)`. The constrained Hessian diagonal at y is

`12y^2-2lambda=4(y-x)(x+2y)<0`.

If y were repeated, a vector supported on two y coordinates with entries +1,-1 is tangent to both constraints and gives a negative second variation; a smooth exactly feasible curve exists because of the two unequal entries. This contradicts a minimum. Therefore there are m-1 copies of x and exactly one y. Solving

`(m-1)x+y=1`, `(m-1)x^2+y^2=q`

gives `x=(1+sqrt((m*q-1)/(m-1)))/m`, `y=1-(m-1)x`. Feasibility gives `1/m<=q<=1/(m-1)`. For nonreciprocal q, m is uniquely `ceil(1/q)`. At q=1/r the only supported optimum is r equal classes: the adjacent expression with m=r+1 has its small class zero and is the same graphon. Equal-root cases and zero-root faces are therefore covered, not assumed away. The endpoints p=1/2 and p=1 have respective values 3/8 and 0; p=1 follows also by bounding the probability of two missing diagonals.

Define for `p in [1-1/(m-1),1-1/m]`:

`F(p)=3[(1-p)^2-(m-1)x^4-y^4]`.

At every branch junction the vectors coincide after deleting a zero class. This proves continuity. The critical value is `F(1-1/r)=3(r-1)/r^3`. This entire optimization is reconstructed here; no finite search is its proof.

## Independently reconstructed join replacement and its exact gap

Let independent outside classes have masses a_i, and let an arbitrary graphon H have mass s, joined fully to every outside class. Write its internal densities h and c_H. Exact sampling gives

`p=1-sum a_i^2-s^2(1-h)`

`c=6*sum_{i<j}a_i^2*a_j^2+6*s^2*(1-h)*sum a_i^2+s^4*c_H`.

The only possible class patterns are 2+2 in outside classes, 2+2 between H and one outside class, and four inside H. A 3+1 pattern has a universal vertex of degree three. Fixing h fixes p and every term except c_H. If `h<=1/2`, the externally proved low-density bound `c_H<=3h^2/2` allows replacement by a complete bipartite H with the same h and no smaller c. This turns the whole graphon into a complete multipartite graphon. Therefore `c<=F(p)` universally throughout this one-low-density-block join class, including h=0 or 1/2 and zero outside classes.

Using PR Theorem 1.1, every sequence `G_n` with `p_n->p>=1/2` and triangle density `g3(p_n)+o(1)` is edit-close to this class. Diagonal selection of epsilon yields o(n^2) edits. An adjacency change influences at most `binom(n-2,2)` four-subsets; hence any induced four-vertex density changes by at most `6 E/binom(n,2)`. Applying the join replacement and continuity proves `limsup c(G_n)<=F(p)`. This quantifies over ALL asymptotically triangle-minimizing sequences, not just the canonical construction. Near p=1 the conclusion follows from the missing-edge bound, and branch junctions follow by continuity. The proof depends on the external PR theorem and LMR low-density bound, and is otherwise reconstructed.

The missing step for the unrestricted conjecture is a justification that arbitrary C4 maximizing sequences can be reduced to this join class, or some other universal bound. Neither multipartite optimization nor triangle stability supplies that implication. A route that assumes every C4 maximizer minimizes triangle density transfers the central difficulty and is blocked without new evidence.

## Falsifiers and nonmultipartite ties

For an interior branch, let `r=m-2`, take r outside independent parts each of mass x, and set `s=x+y`. Inside H put a complete bipartite graph on positive masses b,c, plus isolated mass d, with `bc=xy`, `b+c+d=s`. Choices with d>0 exist whenever x>y>0 (for example b=c=sqrt(xy)). The block has h=`2bc/s^2<=1/2`, and `c_H=6b^2c^2/s^4=3h^2/2`. It has precisely the same global edge, triangle, and C4 densities as the canonical construction, yet is not complete multipartite. A paw induced by one outside vertex and vertices from b,c,d has density `24*r*x*b*c*d>0`; every complete multipartite graph has zero induced paw density. The four-vertex edit bound implies edit-distance fraction at least `4*r*x*b*c*d` when normalized by binom(n,2). Thus the tie remains a positive distance from every multipartite sequence. It refutes a uniqueness/edit-stability inference; it does not refute the source's value conjecture. At branch endpoints d vanishes in the above family; a positive separation claim there would be false.

An explicit rational control is m=3, x=2/5, y=1/5, outside mass 2/5, residual masses b=3/10, c=4/15, d=1/30. It has `p=16/25`, `c=144/625`, triangle density `24/125`, paw density `16/625`, and edit-distance fraction at least `8/1875`. Ordered-assignment enumeration, separate from the moment formulas, checks these values.

Control targets: wrong cycle normalization; repeated-small-root false optimum; part counts beyond the selected branch; junction zero classes; a dense internal block improperly subjected to the low-density bound; omission of the s^4 c_H term; uniqueness of replacement; and treating a triangle theorem as an unrestricted C4 theorem. No claim of current open status is made beyond these three freshly retrieved primary documents; current priority would require a broader independent literature check.
