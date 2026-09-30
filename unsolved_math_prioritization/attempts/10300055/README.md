# Calegari Question 13.2: tightness of contact connection forms

[The proof candidate](CANDIDATE.md) gives an affirmative answer to the conditional tightness question using the Eliashberg–Thurston theorem and Gray stability. The proof includes a regularization argument for $C^1$ forms and retains the source's $C^2$ foliation hypothesis. Separate adversarial review is pending; neither historical priority nor human peer review is claimed.

This does not answer the preceding existence question, problem 10300054. The argument is conditional on the connection form already being contact.

- [Source audit](SOURCE_AUDIT.md)
- [Readiness and prior-attempt gate](readiness.json)
- [Research log](RESEARCH_LOG.md)
- [Frozen artifact hashes](frozen_artifacts.json)
- [Exact finite controls](verify.py) and [receipt](verification.json)

Reproduce the controls with Python 3 and SymPy 1.14.0:

    python3 verify.py

The script writes deterministic JSON to standard output. The controls check exterior-algebra identities, both orientations, the constant-versus-variable gauge distinction, and local smoothing corrections. They do not replace the topological proof or certify the imported classical theorems.

The dataset record and prior triage report are reproduced with attribution to [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), pinned revision 37e53eabe540fb458758e198be61634bd02ee008, CC BY 4.0. The earlier triage assertion of open status was not treated as verified mathematical evidence.
