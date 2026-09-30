# 10600042: an even-strand Markov formulation

**Complete candidate for the literal source question; independent review pending.**

The package gives four explicit classical and eight explicit virtual algebraic move schemes whose states always have even strand count. Ordinary oriented braid closure is retained. A positive one-strand padding in the proof converts every edge of a usual Markov certificate to a named even move, including both virtual exchange directions. No unspecified odd-intermediate path is an allowed move.

- [Complete move list and two-direction proof](CANDIDATE.md)
- [Source and prior-art audit](SOURCES.md), [primary PDF hashes](source_manifest.json)
- [Word-level checker](verify_even_moves.py), [exact receipt](even_move_verification.json)
- [Pinned source record](source_record.json), [readiness](readiness.json), [status](status.json)
- [Research log](RESEARCH_LOG.md), [turn ledger](turns.jsonl)

Run `python3 verify_even_moves.py` with the Python standard library. It passes3219 exact assertions on280 Markov-edge cases and224 braid-relation cases. It checks syntactic lifting, supports, endpoint parity, reversibility, height rounding and permutation-cycle counts. It is not a knot-equivalence oracle or formal proof of the underlying Markov theorems.

The argument is an elementary reformulation of established results. Historical novelty is unestablished. No minimality, plat-closure substitution, framed/transverse version, or stronger bounded-support locality property is claimed.
