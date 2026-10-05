# Five substantive approaches and their stopping points

All five concern the original unrestricted orbit-equivalence question, rather than strengthened hypotheses silently replacing it.

## 1. Periodic-orbit and invariant-measure rigidity

**Attempt.** Recover a Markov presentation or a mixing conclusion from orbit cardinalities, periodic growth, dense orbit structure, and the induced map on invariant probabilities.

**Established.** A homeomorphic orbit equivalence preserves every least orbit period, each fixed-point count, the zeta function, dense periodic points, and dense full orbits. In this setting the target is forward topologically transitive. Its entropy is at least the source entropy. Invariant probabilities correspond affinely by pushforward. Most usefully, if the target is SFT, it is automatically mixing. Proofs: Lemmas 1–4 in `proofs.md`.

**Exact obstruction.** None of these conclusions supplies a finite bound on forbidden-word lengths. Periodic growth does not identify word growth in an arbitrary subshift, and the pushforward of the Parry measure has not been proved maximal-entropy for that target. A proof needs an implication from these necessary invariants to finite type that is not present here. The finite-type assumption in the graph argument is indispensable to that argument, not a conclusion of it.

## 2. Upgrade the orbit cocycle, then use rigidity

**Attempt.** Pull the target map back to the source space, write it as a pointwise integer power of the source, and try to apply continuous-cocycle rigidity using compactness or expansivity.

**Established.** A continuous integer jump function gives flip conjugacy by Boyle–Tomiyama Theorem 3.2, so the desired conclusion holds under that additional condition. Bounded jumps alone give their Theorem 2.3/Corollary 2.7, with an exceptional periodic set, rather than the same unrestricted global conclusion. Baire category gives a dense open set where a jump can be chosen locally constant. An explicit self-orbit-equivalence of the binary full shift nevertheless has unique jumps `2n+1` on explicit aperiodic points. Its homeomorphism and inverse are continuous. Proof and exact controls: Lemmas 5–6.

**Exact obstruction.** Expansivity and compactness of both subshifts do not bound the jump function of an arbitrary orbit equivalence. One would have to construct a better orbit equivalence or control the unbounded/discontinuous part without assuming it away. The example is a counterexample to that proposed upgrade, not to Boyle's question.

## 3. Transfer shadowing / stabilize finite-language approximations

**Attempt.** Transport finite-type local gluing to the target through the orbit map, using the equivalence between shadowing and finite type for finite-alphabet subshifts.

**Established.** A complete proof shows that a subshift is SFT if and only if it has two-sided shadowing. Equivalently its canonical finite-word SFT approximations stabilize. Thus target shadowing is an exact sufficient and necessary closing goal. For every window size, an explicit forbidden periodic configuration of the even shift passes every test at that window size, ruling out finite-test or compactness-only stabilization arguments. Proof: Lemmas 7–8.

**Exact obstruction.** An orbit homeomorphism preserves orbit sets but not their integer clocks. A target pseudo-orbit pulls back to approximate variable-length source moves; signs, overlap, and unbounded lengths prevent the asserted ordinary-source pseudo-orbit argument. No uniform shadowing modulus for the pulled-back target map is proved. The even-shift example tests this inference only; no TOE to a mixing SFT is asserted for it.

## 4. Construct a counterexample by positive variable speed

**Attempt.** On the mixing SFT space, replace the source by a positive pointwise speedup, retain the same complete orbits, and try to obtain an expansive non-SFT target.

**Established.** On any infinite orbit, a strictly positive successor permutation with one full orbit must be the ordinary successor. Consequently a continuous orbit-preserving map with the same full orbits and everywhere-positive jumps on the dense aperiodic set equals the original shift. Everywhere-negative jumps analogously give its inverse. The proof requires no regularity of the jump function. Squaring a shift fails the same-orbits requirement; finite cycles allow different positive generators, but density of aperiodic points prevents extending that exception here. Proof: Lemma 9.

**Exact obstruction.** A genuine counterexample cannot come from this monotone-speed construction. It must reorder infinite orbits nonmonotonically (or use a different mechanism), while still proving continuity, inverse continuity, expansivity, and non-finite-type language. No such counterexample is constructed.

## 5. Promote orbit equivalence to suspension-flow equivalence

**Attempt.** Use ordered cohomology or return sections to reconstruct an SFT from its orbit relation.

**Established.** Clopen global return maps and finite continuous integer-roof suspensions of SFTs are SFTs, by explicit finite graph constructions. With the Parry–Sullivan common-section theorem, a homeomorphism flow equivalent to an SFT is an SFT. Under the standing TOE hypotheses, therefore, target finite type and source–target flow equivalence are equivalent (the reverse direction uses Boyle–Handelman Theorem 1.12 after finite type has already been obtained). A symbol expansion gives an exact negative control: it preserves flow equivalence but changes fixed-point counts, so flow equivalence is not the original orbit relation. Proof: Lemmas 10–11.

**Exact obstruction.** Boyle–Handelman Theorem 1.12 assumes both systems are irreducible SFTs. Applying it before establishing finite type of the target is circular. General TOE does not identify the suspension topology and time orientation. Ordered invariants alone have not supplied the missing global cross section or an applicable one-SFT extension of that theorem.

## Final status

Five approaches completed with their stated partial results and obstructions. Original target unresolved. The results are reductions and failed-method controls, with no claimed new resolution or established novelty.
