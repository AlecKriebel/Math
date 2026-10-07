# Exact target and present status

Status: UNRESOLVED; no unconditional theorem or publication claim.

Let L_eta be the single-mode pure-loss bosonic channel with independent vacuum environment, eta in [1/2,1]. Codes may use arbitrary entanglement across n channel inputs. Mean input constraint is Tr[(sum_i a_i^dagger a_i) rho_average] <= nN for finite N>=0. Use the exact net resource generation/consumption conventions of Wilde–Hayden–Guha and its coding theorem dependencies. Logarithms in capacity formulas are base2: rates in bits, qubits, ebits per use.

Core hypothesis to prove: the C/Q/E region is the closure of the union lambda in [0,1] of
C+2Q <= g(lambda N)+g(eta N)-g((1-eta)lambda N),
Q+E <= g(eta lambda N)-g((1-eta)lambda N),
C+Q+E <= g(eta N)-g((1-eta)lambda N).

Primary-source public/private/key Eq.(2) target: closure of union lambda in [0,1] of
R+P <= g(eta N),
P+S <= g(eta lambda N)-g((1-eta)lambda N),
R+P+S <= g(eta N)-g((1-eta)lambda N).
Rates may be negative for consumed resources; exact permitted operations require audit. This is not a two-way-assisted statement.

Pivotal entropy premise: for all finite n>=1 and arbitrary finite-energy rho, S(L_t^tensor n(rho)) >= n g(t g^(-1)(S(rho)/n)), t in [0,1]. Upstream family273 asserts this via EPnI but validity/semantics/build are under independent audit.

Success requires complete rigor for both regions, ensembles/energy/truncation/closures and boundaries N=0,lambda=0,1,eta=1/2,1. A dependency gap precludes unconditional success.

## Operational correction checkpoint

The literal predecoding private secrecy condition in WH 1005.3818v3 Sec5 is inconsistent with its own unit-resource protocol. At N=0 it excludes every positive generated private/key dimension, whereas the displayed region includes OTP(-1,1,-1). The original literal private target is therefore false. Independent proof: notes/upstream_proof/new_operational_check.md.

A candidate repaired model protects generated W=(M,T_A) by trace decoupling from Eve and all public X=(K,L). Consumed V=(J,S_B) may become correlated with W and transcript; only generated secrets are retained as secure resources. All original signed forward resource accounting, finite gross resource rates, no feedback, and average photon constraints remain. A corrected converse is derived; conventional achievability is under independent construction audit. No silent replacement of the literal source model.
