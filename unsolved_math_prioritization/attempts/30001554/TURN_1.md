# Turn 1: exact signed-period model and orbit reduction

Status: original conjecture unresolved. All words below are nonempty, indices start at0, borders are nonempty and proper. Write t=tau_theta(w), n=|w|, and p=pi_theta^alt(w).

## 1. The involution really is a letter permutation

A morphic involution cannot erase a letter a, since theta(a)=epsilon would give theta²(a)=epsilon rather than a. If theta(a) has k letters, applying the nonerasing morphism again gives a word of length at least k. Since theta²(a)=a, k=1. Thus theta restricts to a permutation of letters, consisting of fixed points and two-cycles, and acts componentwise on words. This justifies, rather than assumes, the literal model used by the checkers.

For 1<=p<=n, the alternating block definition is equivalent to

    w[i+p] = theta(w[i]) for 0<=i<n−p.                 (1)

The forward implication follows by crossing a block boundary in (u theta(u))^omega. For the reverse implication, take u=w[0:p]. Applying(1) repeatedly along each residue class modulo p reproduces the alternating blocks, including a truncated last block. The case p=n is vacuous and always works.

A border of length k is equivalent to the negative shift p=n−k in(1). In particular, w is theta-unbordered exactly when its least negative period is n. Every factor of length greater than a negative period p has a theta-border of length its own length minus p. Consequently

    1 <= tau_theta(w) <= pi_theta^alt(w) <= n.        (2)

This remains true with fixed letters and overlapping borders.

## 2. Shortest-border warning and a valid replacement

A shortest theta-border is **ordinary unbordered**. Indeed, let b be the shortest nonempty theta-border of w. If c were a nonempty proper ordinary border of b, then c is a prefix of w, and theta(c) is a suffix of theta(b), hence of w. This makes c a shorter theta-border of w, a contradiction.

It need not be theta-unbordered. For theta(0)=1 and theta(1)=0, w=0110 has only the theta-border01, of length2; this border itself has a theta-border of length1. Thus the classical shortest-border-is-unbordered argument cannot be transferred by replacing every ordinary border with a theta-border. This is a method obstruction, not a counterexample to the original conjecture.

## 3. Orbit projection and a parameter-bounded alphabet

Let O be the alphabet of theta-orbits and let rho map each letter to its orbit. Put v=rho(w). If a factor x of w has a theta-border b, its projected prefix rho(b) equals its projected suffix rho(theta(b)); hence rho(x) is ordinarily bordered. Contrapositively, every ordinarily unbordered factor of v lifts to a theta-unbordered factor of w. Therefore

    tau(v) <= tau_theta(w)=t.                        (3)

Use the credited Holub–Nowotka ordinary-word theorem: a nonempty word x with |x|>7(tau(x)−1)/3 has least ordinary period tau(x). The author manuscript states this precise strict inequality on pp.1–2; the present packet uses that prior theorem as a dependency and does not reprove its full argument. Under the original hypothesis n>=3t, we have

    n >= 3t > 7(t−1)/3 >= 7(tau(v)−1)/3.

Thus v has least ordinary period q=tau(v)<=t. In particular, every orbit appearing in v already appears in its first q letters. There are at most q distinct orbits, and the theta-closed support of w has at most2q<=2t letters.

**Scoped reduction.** For a fixed value t, any counterexample can be relabeled equivariantly to an alphabet of at most2t letters, with its orbit sequence ordinary periodic of period at most t. Equivariant injective relabeling preserves each letter equality and each equality x=theta(y), so it preserves all borders, t, and p exactly. This reduction does not bound the word length, nor does orbit periodicity imply alternating letter periodicity: the choices within two-letter orbits are still uncontrolled. The original all-t question remains.

## 4. Two complete special cases

If t=1, every adjacent two-letter factor is theta-bordered. Its only possible border has length1, so w[i+1]=theta(w[i]) throughout. Therefore p=1=t, without needing n>=3.

If every occurring letter is fixed by theta, ordinary and theta-borders coincide, as do ordinary and alternating periods. The Holub–Nowotka theorem above settles the original implication for this subcase. This is credited prior ordinary-word mathematics, not a new resolution of the mixed/two-cycle problem.

## 5. Exact finite controls and source extremal family

verify_turn1.py uses direct prefix/suffix comparisons and a separate block-language check. It exhausts all binary-swap words through length13, swap-plus-fixed-letter ternary words through length9, two-swap four-letter words through length7, and binary identity words through length10:69,795 words total. It checks(2), the border/shift equivalence, the shortest-border lemma, the t=1 case, and the target implication whenever its hypothesis holds. All283 tested antecedent instances satisfy the conclusion. These are finite controls only, not a proof for arbitrary words.

The original report gives, for i>=2 and the binary swap,

    w_i=(01)^i 011 (01)^i 001 (01)^i 0,
    n=6i+7, tau_theta=2i+4, pi_theta^alt=4i+5.

The checker independently computes these parameters for2<=i<=30. Here n−3tau_theta=−5, and n/tau_theta tends to3 from below. The all-i extremal formula is credited to the report; this turn verifies the stated finite range but does not supply a new all-i proof. The family demonstrates why a coefficient less than3 cannot suffice asymptotically if the cited general formula is used. It never meets the conjecture's n>=3t hypothesis.

The exact receipt contains243,434 assertions. No assertion count or finite scan certifies the unrestricted theorem. The next gap is controlling the signs within the periodic orbit projection, or producing a genuine threshold counterexample.
