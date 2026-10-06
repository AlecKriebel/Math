# Attempt 3: a Hasse–Minkowski obstruction to all quadratic-image definitions

## Strategy

The diagonal-fiber normal form from Attempt 2 suggests trying an arbitrary number of square variables but at most one independent linear equation in all the remaining variables after additive elimination. No additional witness-only constraints are allowed in this restricted fragment. A branch with a nonzero coefficient of the free parameter is the value set

S_{c,q}={c+q(z):z in Q^r},

where q is a rational diagonal quadratic form. Its positive-existential formula says x=c+sum a_j s_j with all P₂(s_j). This attempt proves that no finite union of such branches defines the nonsquares. In fact the result holds for the images of arbitrary rational polynomials of total degree at most two.

## The local representation input

We use the classical Hasse–Minkowski representation theorem: for nonzero a in Q and a rational quadratic form h, h represents a over Q if and only if it represents a over every completion Q_v, including R. Zero coefficients can be removed without changing the represented set, so degeneracy causes no difficulty. The representation variant is stated explicitly as Theorem 26.3 in Bjorn Poonen's MIT 'Introduction to arithmetic geometry' notes, https://math.mit.edu/~poonen/782/782notes.pdf. It also follows from the standard homogeneous theorem by adjoining the term -a t²; if the resulting rational isotropic vector has t=0, isotropy of the nondegenerate h itself makes h universal, supplying a representation of a.

For completeness, the last assertion is elementary. If h(v)=0 with v≠0 in a nondegenerate space, choose w with the polar bilinear form B(v,w)≠0. Then h(sv+w)=2s B(v,w)+h(w) takes every rational value as s varies. We only use the representation theorem with a nonzero target.

## Each square-free quadratic image has one fixed local obstruction

**Lemma.** Suppose S_{c,q} contains no rational square, including zero. Then there is a place v such that S_{c,q} contains no element that is a square in Q_v.

**Proof.** Evaluating z=0 shows that c is a rational nonsquare, so in particular c≠0. A rational square in S_{c,q} is exactly a solution to

q(z)-w²=-c.

By hypothesis the rational quadratic form h(z,w)=q(z)-w² does not represent the nonzero number -c over Q. The representation theorem supplies a place v where it does not represent -c over Q_v. Now suppose x=c+q(z) with z rational and x=w_v² with w_v in Q_v. Then the pair (z,w_v) represents -c under h over Q_v, a contradiction. Thus every element of S_{c,q} is a nonsquare in this one fixed completion. □

This is stronger than attaching a potentially varying local obstruction to each x. The obstruction is uniform over the whole branch because the equation testing intersection with rational squares is one fixed quadratic equation.

## Finite-union impossibility

**Theorem.** The nonsquare set N=Q\P₂ is not a finite union of sets S_{c,q}.

**Proof.** If N were such a union, each constituent would be disjoint from rational squares. Apply the lemma to obtain one place v_i for each constituent. Let S be the finite set of finite primes among those places. By Attempt 1, the positive nonsquare

x=1+(4 product_{p in S} p)²

is a square in every Q_p for p in S and is also a square in R. It is consequently a square in every Q_{v_i}. The lemma excludes it from every constituent, contradicting that their union equals N. □

Branches independent of x after linear elimination give Q or the empty set; a nonempty all-Q branch is incompatible with N. A constant image is the r=0 case and is covered by the same proof. Thus the theorem handles every finite disjunction of the diagonal normal-form branches having at most one independent equation total, with no additional witness-only constraints and without bounding the number of square atoms.

## Extension to arbitrary degree-two polynomial images

**Corollary.** No finite collection of rational polynomials f_i, of total degree at most two and with any finite number of variables, satisfies N=union_i f_i(Q^{r_i}).

**Proof.** Write f(z)=z^T A z+l^T z+c with A symmetric. If l is nonzero on ker A, take v in ker A with l^T v≠0. Along each line z+t v, f changes by the nonconstant affine function t l^T v; hence its image is all Q and cannot be a constituent of N. Otherwise l lies in im A. Choose h with 2Ah=l. Completing the square gives f(z)=(z+h)^T A(z+h)+c-h^T A h. Translating the input does not change the set of values, and rational diagonalization puts this in S_{c',q}. Apply the theorem. Constant and linear polynomials are covered by the same dichotomy. □

## Boundary of the argument

This does not rule out intersections of several diagonal equations. For such an intersection, adjoining x=w² gives a simultaneous system of quadrics, and failure of a rational point need not be explained by one completion. Applying Hasse–Minkowski separately to each equation would ignore the common witnesses and would be invalid. The local-global failure of varieties cut out by multiple equations is exactly the escape hatch left to a possible positive definition.

Likewise, a projection from a constrained higher-dimensional variety is not the same as the image of a polynomial map on unrestricted Q^r. Poonen's nonsquare theorem in the ring language is therefore not contradicted by this corollary.

## Attempt outcome

The single-diagonal-equation route fails at all dimensions, for a proved reason. A successful definition must use genuinely simultaneous square constraints (after additive elimination), or another equivalent mechanism beyond a finite union of quadratic polynomial images. This is useful restricted negative progress; it does not decide the full AIM question. No originality claim is made for these elementary consequences of Hasse–Minkowski.

Fresh substantive attempt count: 3/5.
