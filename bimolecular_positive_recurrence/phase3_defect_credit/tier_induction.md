# Tier induction and global assembly

## 1. Finite tier extraction

Let \(x_n\in\Gamma\) be any divergent sequence. For each coordinate, pass to
a subsequence on which it is either constant or tends to infinity. For every
pair from the finite monomial set

\[
\mathcal M_2=
\{1,x_i,x_i(x_i-1),x_ix_j:i\ne j\},
\]

pass again so that the ratio tends to zero, infinity, or a finite positive
limit. Diagonal extraction terminates because \(\mathcal M_2\) is finite.
This gives a finite ordered source-tier partition and an active capped face.

When the generator is applied to a certificate of degree \(P\), only a finite
larger monomial set is produced. The same extraction is made for that set.
Thus no compactness argument ranges over an infinite family of monomials.

## 2. Top support dichotomy

Let \(I\) be the species in the highest population tier.

### Safe case

If \(I\) is quadratically safe, the one-linkage safe-support theorem gives
\(q_I(y)\in\{0,1\}\). The defect-credit theorem applies.

If its zero-cycle branch occurs, there is

\[
M_I+b\cdot X_J=\text{constant}.
\]

But \(X_J=o(M_I)\) and \(M_I\to\infty\), a contradiction. Hence the finite
Bellman hierarchy has a strictly negative layer.

### Dissipative case

If \(I\) is not quadratically safe, begin with a binary source supported in
\(I\). Its quadratic closure either reaches a lower-molecularity target or
adds a species outside the current top support. In a one-linkage mixed
network it cannot remain forever inside a purely binary supported component:
otherwise strong connectivity would force every complex into that pure
binary component.

Use the same expanded automaton, now with the lexicographic reward

\[
(\Delta N,\Delta M_I,\Delta M_{I_2},\ldots).
\]

A closure edge that lowers molecularity is strictly draining in the first
coordinate. An edge that only enlarges support moves to a regime of strictly
larger closure rank. The closure rank is the pair

\[
\bigl(|\operatorname{Cl}_2(I)|,
      \text{distance to a molecularity descent}\bigr),
\]

ordered by larger closure and then shorter distance. It is well founded and
has at most \(d+|\mathcal C|\) strict changes. The cycle-pivot/Bellman proof
therefore gives either negative drift before exit or a strict rank advance.
A cycle of rank advances is impossible. After finitely many advances a
molecularity descent supplies the negative layer.

## 3. Why nested scales are finite

A regime exit can do only one of three things:

1. a top species loses a fixed fraction of its population;
2. a lower species joins the current top tier; or
3. two previously tied source monomials separate into distinct tiers.

The first is already a radial decrease. The second strictly enlarges top
support. The third strictly refines a weak order on a finite monomial set.
Consequently a path of unresolved exits has bounded length. No argument of
the form "continue similarly through the remaining tiers" is used; the rank
is explicit and finite.

## 4. Global Bellman patching

Form the finite regime graph whose vertices are:

- capped active faces;
- weak orders of the finite monomial set needed by the certificate;
- quadratic-closure ranks;
- expanded target/source phases; and
- zero-reward SCCs already contracted.

Include every exact one-reaction seam crossing and every designated episode
exit as an edge. On each edge record the lexicographic leading reward. The
cycle-pivot theorem applies to this union graph. Therefore the global system
of Bellman difference inequalities is feasible. Add a common sufficiently
large positive leading coefficient to make every piece coercive, and clear
all positive monomial denominators. This gives one piecewise
generalized-polynomial function \(V_\Gamma\).

At a seam the value used after the jump is the piece assigned to the target
regime. Seam inequalities were included in the same Bellman system, so there
is no unverified max/min boundary.

## 5. Uniformity by contradiction

Suppose the exact generator estimate failed outside every finite set. Choose
\(x_n\in\Gamma\) with \(|x_n|\to\infty\) and

\[
\mathcal L V_\Gamma(x_n)>-1.
\]

Extract the stabilized face and monomial tiers described above. The sequence
lies eventually in one closed regime or on one seam cell. Divide the exact
generator expression by its largest positive monomial. Every lower term
vanishes or converges to its finite tied-tier coefficient. The Bellman
certificate leaves a strictly negative leading limit. This contradicts the
chosen inequality.

Hence there are a finite \(K\subset\Gamma\) and \(\epsilon>0\) with

\[
\mathcal L V_\Gamma(x)\le-\epsilon
\qquad(x\notin K).
\]

Rescale \(V_\Gamma\) by \(1/\epsilon\) to obtain drift at most \(-1\).

## 6. Boundary classes

If a species is permanently zero on \(\Gamma\), delete its coordinate and
all reactions never enabled on \(\Gamma\). The capped-face automaton performs
this restriction automatically. If a reaction can create the species from a
state in \(\Gamma\), the face is not closed and the corresponding seam edge
is retained. Thus the argument neither assumes positivity nor enlarges the
communicating class.
