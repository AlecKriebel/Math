# Restricted obstruction: affine homomorphisms on product fibers

2026-10-17 20:55 UTC. Discovery completion estimate for the original Kourovka questions: **8%** each. Status of this lemma: deduction complete; frozen for independent adversarial verification. No novelty claim is made, and this is **not** a solution of either quasi-isometry question.

## Exact statement

Let $F$ have any finite word metric, let $Y$ be any nonempty unbounded metric space, and give $F\times Y$ the sum metric. There is no quasi-isometry

$$\Psi:F\times Y\longrightarrow F$$

such that, for every $y\in Y$, there are an element $s_y\in F$ and a homomorphism $\alpha_y:F\to F$ satisfying

$$\Psi(f,y)=s_y\alpha_y(f)\qquad\text{for all }f\in F.$$

In particular, this restriction rules out such constructions for $Y=\mathbb Z$ and $Y=F$. The maps $\alpha_y$ may vary with $y$, and are not initially assumed injective. No continuity, geodesicity, bounded geometry, or group structure is assumed for $Y$.

This also rules out a quasi-isometry lying at a uniformly bounded distance from a map of this form: a uniformly bounded perturbation of a quasi-isometry remains a quasi-isometry.

## Elementary inputs

### 1. Unique roots in $F$

The group $F$ is bi-orderable. Here is a direct positive-cone construction, included to expose the premise rather than hide it behind a citation. If $f\ne1$, let $a$ be the left endpoint of its support. Since $f$ has finitely many linear pieces, immediately to the right of $a$ it has slope $2^k\ne1$. Declare $f$ positive when $k>0$.

If two positive elements have different left support endpoints, their product has the sign of the one with the earlier endpoint. If their left endpoints agree, their initial slopes multiply and are both greater than one. The positive cone is therefore closed under multiplication. Inversion reverses the sign. Conjugation by an increasing PL map moves the left support endpoint but preserves this initial slope, since the one-sided slopes of the conjugator and its inverse cancel. Thus this positive cone defines a bi-order.

In any bi-ordered group, $a<b$ implies $a^m<b^m$ for every positive integer $m$ (insert successive factors and use invariance on both sides). Consequently

$$a^m=b^m\quad\Longrightarrow\quad a=b.$$

In particular $F$ is torsion-free.

### 2. Finite-index subgroups and the centralizer of $F'$

We use the classical theorem that $F'$ is infinite and simple; see [Cannon–Floyd–Parry, *Introductory notes on Richard Thompson's groups*, Theorem 4.5](https://www.imo.universite-paris-saclay.fr/~emmanuel.breuillard/Cannon.pdf).

Every finite-index subgroup $Q\le F$ contains $F'$. Indeed, the finite permutation action on its cosets restricts to a homomorphism from infinite simple $F'$ to a finite symmetric group. That homomorphism is trivial, so $F'$ lies in the core of $Q$. This fact is also [Burillo–Cleary–Röver, Proposition 2.1](https://maths.nuigalway.ie/research/Preprints/2007/IRL-GLWY-2007-002.pdf).

Also

$$C_F(F')=1.$$

To see this directly, if $w\ne1$, choose a small standard dyadic interval $I\subset(0,1)$ with $w(I)\cap I=\varnothing$. Such an interval exists near any point moved by $w$. A nontrivial commutator from a clone of $F$ supported inside $I$ belongs to $F'$. Its support and the support of its conjugate by $w$ are disjoint, so the two elements cannot be equal. Thus $w$ does not centralize $F'$.

## Lemma: bounded-distance homomorphisms into $F$ agree

Let $G$ be any group and $a,b:G\to F$ homomorphisms. If

$$\sup_{g\in G}|a(g)^{-1}b(g)|<\infty,$$

then $a=b$.

**Proof.** Properness of a finite word metric makes the set of differences finite. Put

$$E=\{g\in G:a(g)=b(g)\}.$$

This is a subgroup. The fibers of $\delta(g)=a(g)^{-1}b(g)$ are precisely its cosets $Eg$: equality $\delta(g)=\delta(h)$ is equivalent to $a(gh^{-1})=b(gh^{-1})$. Hence $E$ has finite index in $G$. For every $g$, some positive power $g^m$ belongs to $E$, giving $a(g)^m=b(g)^m$. Unique roots in $F$ imply $a(g)=b(g)$. $\square$

## Proof of the restricted obstruction

Suppose that $\Psi$ is an $(A,B)$ quasi-isometric embedding whose image is $R$-dense, with the displayed affine-homomorphism form. Fix $y_0\in Y$, and abbreviate $s_0=s_{y_0}$ and $\alpha_0=\alpha_{y_0}$.

### Step 1: vertical control identifies all homomorphisms up to conjugation

For each fixed $y$, vertical pairs with the same $f$ satisfy

$$|\alpha_0(f)^{-1}s_0^{-1}s_y\alpha_y(f)|
\le A\,d_Y(y_0,y)+B=:C_y\qquad\text{for all }f.$$

Write $t_y=s_0^{-1}s_y$. The homomorphism $\beta_y(f)=t_y\alpha_y(f)t_y^{-1}$ then satisfies

$$|\alpha_0(f)^{-1}\beta_y(f)|\le C_y+|t_y|.$$

The preceding lemma implies $\beta_y=\alpha_0$, so

$$\alpha_y(f)=s_y^{-1}s_0\alpha_0(f)s_0^{-1}s_y,$$

and therefore

$$\Psi(f,y)=s_0\alpha_0(f)s_0^{-1}s_y.\tag{1}$$

Define $P=s_0\alpha_0(F)s_0^{-1}$ and $C=C_F(P)$.

### Step 2: horizontal control gives finitely many centralizer cosets

Take a finite generating set $a_1,\dots,a_k$ of $F$, and write $b_i=s_0\alpha_0(a_i)s_0^{-1}$. From (1),

$$|s_y^{-1}b_i s_y|
=d_F(\Psi(1,y),\Psi(a_i,y))
\le A+B$$

for every $i$ and $y$. There are only finitely many possible $k$-tuples of these conjugates. If $s_y$ and $s_z$ give the same tuple, $s_y s_z^{-1}$ centralizes every $b_i$, hence belongs to $C$. Choose representatives $r_1,\dots,r_M$ for the tuples that occur. Then

$$s_y\in\bigcup_{j=1}^M C r_j,$$

and (1) gives

$$\Psi(F\times Y)\subseteq\bigcup_{j=1}^M PCr_j.$$

Since $C$ centralizes $P$, the set $Q=PC$ is a subgroup and $P\trianglelefteq Q$.

### Step 3: coarse density forces this subgroup to have finite index

The $R$-density assumption implies

$$F=\Psi(F\times Y)\,B_F(R)
\subseteq\bigcup_{j=1}^M\bigcup_{b\in B_F(R)}Q r_j b.$$

The ball is finite, so this is a finite union of right cosets of $Q$. Thus $[F:Q]<\infty$, and the elementary input gives $F'\le Q$.

### Step 4: simplicity eliminates the centralizer

The restriction $f\mapsto\Psi(f,y_0)$ is a quasi-isometric embedding. Its homomorphism part $\alpha_0$ has trivial kernel: a nontrivial kernel element would, by torsion-freeness, have distinct powers of unbounded word length, contradicting the lower quasi-isometry bound. Therefore $P\cong F$ and $P'\ne1$.

Since $P\trianglelefteq Q$, its characteristic subgroup $P'$ is normal in $Q$. Also $P'\le F'$ because its elements are commutators in $F$. As $F'\le Q$, it follows that $P'$ is a nontrivial normal subgroup of simple $F'$. Hence

$$P'=F'.$$

Consequently $C\le C_F(P')=C_F(F')=1$. The finitely many centralizer cosets from Step 2 are now singletons, so the set $\{s_y:y\in Y\}$ is finite.

### Step 5: the lower bound contradicts unboundedness of $Y$

Because $\Psi(1,y)=s_y$, the lower quasi-isometry bound yields

$$A^{-1}d_Y(y,z)-B\le|s_y^{-1}s_z|.$$

The right side is uniformly bounded, since the set of $s_y$ is finite. Thus $Y$ is bounded, contradicting the hypothesis. $\square$

## Exact scope and remaining gap

This proves a restriction on one broad construction family. It supplies no quasi-isometry invariant separating $F$ from either product. A hypothetical quasi-isometry can have highly nonhomomorphic horizontal slices, and nothing here proves that such slices must be uniformly close to affine homomorphisms. Establishing that latter assertion would be a major additional rigidity theorem; it is not assumed or suggested as a routine remaining step.

No part of the original claim is marked solved. The fiberwise-affine route is marked **blocked** unless a materially different, nonhomomorphic compensation mechanism is introduced.
