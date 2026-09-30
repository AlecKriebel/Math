# 30000177 / OWR-785-003: four-qubit W-state LOCC dense coding

**Full candidate, awaiting independent review.** In the source's asymptotic
model, an explicit Bell-measurement preprocessing step gives a cq multiple-access
channel with achievable sum rates approaching 3/2 + h₂(1/4) ≈ 2.311278 bits per
pair of transmitted qubits. In particular, independent rates 9/8 each exceed
the two-bit benchmark. Winter's established coding theorem supplies the block
code; all quantum block decoding occurs locally at the second receiver.

- [Complete proof and exact protocol](CANDIDATE.md)
- [Source and prior-work audit](SOURCES.md)
- [Exact checker](verify_channel.py) and [receipt](verification.json)
- [Research log](RESEARCH_LOG.md), [status](status.json), [readiness](readiness.json)

Run `python3 verify_channel.py` from this directory. Standard library only.
The 903 exact assertions check the finite channel and entropy calculation;
they do not simulate an asymptotic coding theorem. Bell-measurement and cq-coding
foundations are credited. Optimal capacity, one-copy zero-error performance,
experimental realization and priority are not claimed.
