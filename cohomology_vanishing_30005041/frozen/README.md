# Cohomology-vanishing exponents: five-attempt checkpoint

**Original problem: UNSOLVED in this work.** No full proof, counterexample, novelty claim, paper, or new DOI is proposed. These are AI-assisted, unrefereed research notes with elementary scoped propositions and a small exact regression checker.

- Catalogue: 30005041 / OWR-9790362-012; queue rank 482.
- Source: Mikael de la Salle, joint work with Amine Marrakchi, “Group actions on Lp-spaces: dependance on p,” in *Geometric Structures in Group Theory*, Oberwolfach Reports 19 (2022), report 11, pp. 567–569; **Question 1 on p. 568**. Workshop February 27–March 5, 2022; report published March 2023.
- Exact mathematical target: for a fixed continuous homomorphism `sigma: G -> Aut(X,[mu]) ⋉ L^0(X,mu;{-1,1})`, with its induced Lamperti representations `pi_p`, is `{p>0 : H^1(G,pi_p)=0}` an interval?
- `H^1` here is ordinary continuous first cohomology, not reduced cohomology. The same nonsingular action and sign cocycle are held fixed, including at p=2. Real functions and standard sigma-finite measure spaces are used.
- Scope of elementary propositions below: countable discrete groups unless explicitly stated otherwise. They do not prove the assertion for arbitrary topological groups or diffuse nonsingular actions.

## Results and limits

1. The Mazur map is not a map on arbitrary 1-cocycles. A short all-p formal-coboundary implication holds when there are no nonzero invariant measurable vectors; it does not handle genuine measurable cohomology.
2. For an equivalent **finite invariant measure**, the interval conclusion on `[1,infinity)` follows from the known formal-coboundary theorem. A bounded strictly positive multiplication intertwiner `L^q(mu)->L^p(mu)`, p<q, exists exactly when such an invariant measure exists. This sharply delimits this particular interpolation route.
3. For a signed permutation representation of Z on a countable atomic space, the vanishing set is either all `(0,infinity)` or empty. It is all precisely when every orbit is a finite negative-sign cycle and the cycle lengths are uniformly bounded. This is a self-contained special-case calculation, not a claimed new theorem.
4. For finitely generated groups, countable direct sums of individually cohomologically trivial Banach representations are trivial precisely when their primitive estimates are uniform. Negative cycles give an explicit warning: every component can have zero cohomology while the sum has nonzero cohomology for every p.
5. Any interval hole at `1<=a<b<c`, if it exists, must have nonzero **nonformal** cohomology at b. The elementary exact sequence isolates that obstruction; finite-atomic experiments and formal-coboundary manipulations cannot eliminate it.

See [the five substantive attempts](ATTEMPTS.md) and the [source and status ledger](SOURCES.md). Run `python3 checks/exact_controls.py` for small, exact, standard-library regression checks. The symbolic arguments establish the stated infinite-family special cases; the finite checks do not establish the general problem.

## Next meaningful research step

Investigate a genuinely diffuse nonsingular action without an equivalent finite invariant measure, and compute the image of `H^1(G,L^b)` in `H^1(G,L^0)` while controlling two endpoint cohomology groups. Alternatively prove a cocycle transport theorem that preserves the fixed Lamperti family. No such construction or theorem was obtained here.
