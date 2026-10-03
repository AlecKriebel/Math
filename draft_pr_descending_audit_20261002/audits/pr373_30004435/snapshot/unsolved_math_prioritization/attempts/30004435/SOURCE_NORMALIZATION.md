# Exact source and proof-method boundary

Problem30004435 / OWR-17474-009 is Jeffrey Steif's Question C in “Some results and open questions concerning Gibbs states, quasilocality and bilateral determinism,” printed pp.632–633 of OWR11/2020. The complete contribution was read and Question C was visually checked. [Primary report](https://ems.press/content/serial-article-files/46847).

The process is strictly stationary, indexed by all integers, with a finite alphabet. No Markov, finite-memory, mixing, reversibility or ergodicity assumption is present. The remote-left and remote-right tail fields must coincide modulo null sets. All fields here are understood as completed measure algebras.

The equality itself is known. The source explicitly requests a proof using probability theory without entropy theory. A proof via the Pinsker algebra, a Shannon/relative-entropy calculation, or an information-rate argument with terminology changed would not satisfy this request. Our partial arguments use conditional expectation, Markov coupling and finite-dimensional probability only; a full result is not asserted for a subclass.

The bilateral tail is a different field. The source explicitly notes finite-state bilaterally deterministic examples with trivial one-sided tails and maximal bilateral tail. Thus equality of all three tails cannot be assumed for general stationary processes. An invariant sigma algebra also differs from a sigma algebra whose individual events are invariant; periodic phase information is an elementary warning.

Primary literature consulted:
- Al-Najjar–Shmaya, *Learning the ergodic decomposition*, arXiv1406.6670, Theorem5.2, pp.13–14. Their proof explicitly invokes the entropy-based equality, citing Weiss, *Single Orbit Dynamics*, §7. Example6.1 gives the infinite-alphabet asymmetric-tail example used as a control here
- M. D. Lemańczyk, *Recurrence of stochastic processes in some concentration of measure and entropy problems*, University of Warsaw dissertation, December2020, AppendixB.1 andB.3.2. The general equality is obtained through entropy/Pinsker theory. The finite-Markov classification is recorded separately in(B.3.3), with credit to Blackwell–Freedman(1964)

No method-compliant proof for the unrestricted original was identified in these sources. The literature search is not a worldwide novelty or open-status certification. Adjacent30004434 is the different Gibbs-coupling Question A.
