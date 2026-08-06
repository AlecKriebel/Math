# Theorem statement

## Unrestricted binary single-linkage positive-recurrence theorem

Let \(G=(\mathcal S,\mathcal C,\mathcal R)\) be a finite stochastic
mass-action reaction network. Assume:

1. every complex has molecularity at most two;
2. the reaction graph has one linkage class; and
3. that linkage class is strongly connected.

Assign an arbitrary positive rate constant to every reaction. Then every
closed communicating class \(\Gamma\) of the associated nonexplosive
continuous-time Markov chain is positive recurrent.

Equivalently, for every closed communicating class there is a unique
stationary probability distribution on that class.

No assumption is made that a species occurs as a unary complex \(S_i\), as a
pure binary complex \(2S_i\), or in a positive state. The theorem includes
classes on coordinate faces and classes cut out by signed conservation laws,
parity restrictions, or proper sublattices.

## Quantitative form proved

For every infinite closed class \(\Gamma\), the proof constructs a proper
piecewise generalized-polynomial function

\[
V_\Gamma:\Gamma\longrightarrow[0,\infty)
\]

and a finite set \(K\subset\Gamma\) such that

\[
\mathcal L V_\Gamma(x)\le -1,
\qquad x\in\Gamma\setminus K.
\]

The pieces and their coefficients are obtained from finite exact data:
active coordinate faces, weak orders of finitely many source monomials,
expanded target/source automata, cycle-reward certificates, and rational
Bellman inequalities. The construction is class-specific only through the
active face and the linear/lattice invariants of the class.

The generator inequality is used only to prove finite mean return. No claim
of geometric or exponential ergodicity is made.
