# Turn 1: a quantitative product-class theorem and persistent-rank obstruction

The arbitrary higher-dimensional question remains unresolved. This turn reconstructs the credited one-dimensional mechanism, sharpens its coefficient bookkeeping, and proves the source implication for Cartesian products of aperiodic one-dimensional subshifts, with a sharp quantitative total-rank bound. It also isolates why counting raw approximant cells is insufficient in general.

## 1. One-dimensional cohomology from finite words

Let X be a minimal subshift over a finite alphabet, with word complexity p(n). Its suspension Omega_X is the quotient of X times R by(x,t+1)~(shift(x),t). For each n, the Rauzy graph R_n has p(n) vertices (length-n words) and p(n+1) oriented edges (length-(n+1) words), joining the prefix to the suffix. Minimality makes the graph strongly connected: any two words occur, in that order, in a sufficiently long word of the recurrent language.

Choose nested centered intervals of n coordinates. Forgetting the new outer coordinate gives continuous graph maps R_(n+1)→R_n, mapping each edge with its unit interval parameter unchanged. The inverse limit is the suspension. Indeed, a suspension point supplies all centered words and its position in the current unit tile. Conversely compatible interior-edge points have a common interval parameter and compatible words determining a point of X; compatible vertices determine the same information at a tile boundary. Increasing centered windows separate suspension points. The resulting continuous bijection from the compact suspension to the Hausdorff inverse limit is a homeomorphism. This is the Rauzy construction of Julien, arXivv1 Theorem5.10.

By continuity of Čech cohomology under inverse limits of compact polyhedra,

    H^1(Omega_X;Q)=direct_limit H^1(R_n;Q).

For a connected finite graph,

    dim H^1(R_n;Q)=p(n+1)−p(n)+1.                         (1.1)

Also H^0(Omega_X;Q)=Q and all higher groups vanish. No injectivity of the bonding maps on cohomology is assumed.

## 2. The direct-limit rank lemma in both useful directions

For any sequential direct system of vector spaces V_n with finite dimensions:

- If dim V_n<=M at infinitely many indices, the direct limit has dimension at most M. Any M+1 putative independent limit vectors lift to a common later stage with dimension at most M, giving a relation which persists to the limit.
- If the direct limit contains r independent vectors, then dim V_n>=r at every sufficiently late stage. Lift the vectors to a common stage. A relation between their images at any later stage would give the same relation in the limit, contradicting independence.

Applied to(1.1), if C=liminf p(n)/n<infinity, then infinitely many n satisfy p(n+1)−p(n)<=floor(C). Otherwise the eventual integer increments would be at least floor(C)+1, forcing the liminf ratio to be at least that larger integer. Hence

    r_X:=dim H^1(Omega_X;Q)<=floor(C)+1.                  (2.1)

In particular the usual O(n) hypothesis suffices, as in the credited Julien result. Conversely, when r_X is finite, the second part of the lemma gives

    p(n+1)−p(n)>=r_X−1 eventually,
    p(n)>=(r_X−1)n−B                                    (2.2)

for some constant B. The statement also holds with any finite r represented by independent classes when the limit rank is infinite.

The argument uses cofinal small ranks and persistent classes, rather than assuming that every graph cycle survives. A direct system Q^n with every bonding map zero has limit rank0 despite unbounded stage dimensions. An abstract growing approximant rank alone therefore cannot certify infinite tiling cohomology.

## 3. Cartesian products of aperiodic words

Let X_1,...,X_d be minimal aperiodic one-dimensional subshifts. Color the unit cube at z=(z_1,...,z_d) by

    (x_1(z_1),...,x_d(z_d)),  x_i in X_i.

The resulting Z^d subshift is the product system, and its translational tiling hull is homeomorphic to

    Omega=Omega_(X_1) times ... times Omega_(X_d).

The independent coordinate shifts make the orbit closure the full product. Repetitivity follows by taking a common return bound for the finitely many coordinate words in a desired box. A translational period must preserve the unit grid and hence have integer coordinates; each nonzero coordinate would be a period of its aperiodic one-dimensional factor. Thus these are fully aperiodic source-admissible tilings.

For n-cube words, complexity is exactly

    P(n)=product_(i=1)^d p_i(n).                           (3.1)

Morse–Hedlund gives p_i(n)>=n+1. A short reason is that if p_i(n)<=n for some n, monotonicity from p_i(0)=1 forces an earlier zero increment. Every word at that length then has a unique successor; recurrence puts the sequence on a finite directed cycle, giving periodicity. Thus if

    C=liminf P(n)/n^d<infinity,

then along the same cofinal subsequence p_i(n)/n is bounded for every i, and(2.1) makes all r_i:=dim H^1(Omega_(X_i);Q) finite.

The field Künneth formula gives the full graded rank polynomial

    sum_k dim H^k(Omega;Q) t^k =product_i (1+r_i t).       (3.2)

One can see this without imposing an unwarranted local-contractibility assumption on the hull: apply ordinary rational Künneth to finite products of the graph approximants, then use Čech continuity and the fact that filtered direct limits of vector spaces commute with finite tensor products. This supplies every degree, not only H^1.

## 4. A sharp coefficient bound for the product class

Set a_i=max(1,r_i−1). Combining Morse–Hedlund with(2.2) yields p_i(n)>=a_i n−B_i for all sufficiently large n. Divide(3.1) by n^d and take the liminf:

    product_i a_i<=C.

For every nonnegative integer r, 1+r<=3 max(1,r−1). Therefore(3.2) at t=1 gives

    dim H^*(Omega;Q)=product_i(1+r_i)<=3^d C.              (4.1)

This is a theorem for the Cartesian-product subclass, and the coefficient C refers exactly to n-cube word complexity. The source's radius convention gives the same polynomial growth condition after fixed rescaling, but not necessarily the same numerical C.

The constant3^d is sharp in this subclass. For a Sturmian subshift, p(n)=n+1, so(2.1) gives r<=2. There are also two independent rational cohomology classes: the constant unit-edge cochain and the cochain indicating symbol1. Integration against the invariant measure coming from irrational circle rotation sends them to1 and to the irrational symbol frequency alpha. Integration annihilates coboundaries: at each Rauzy stage, incoming and outgoing edge frequencies at a vertex agree by shift invariance, so the weighted sum of a vertex coboundary is zero. It is compatible with the bonding maps. A rational relation between these classes would therefore give q+r alpha=0, forcing both coefficients to vanish. Thus r=2.

For a d-fold product of Sturmian systems, C=1 and(3.2) is(1+2t)^d; total rank is exactly3^d. These are genuine fully aperiodic examples, not products with periodic directions.

## 5. Controls and the remaining gap

verify_turn1.py generates the full finite Sturmian languages from exact irrational-rotation interval partitions, computes the connected graph ranks, and checks product-complexity and tensor-rank formulas. It also verifies the direct-limit bookkeeping with finite linear maps. These finite tests support the algebraic constructions; they do not establish the arbitrary tiling implication.

A general low-complexity tiling need not be a Cartesian product. Its higher-dimensional approximants can have cancellations between cohomological degrees and bonding maps can kill classes. No decomposition or persistent-rank estimate reducing the source's full class to(4.1) has been proved in this turn.
