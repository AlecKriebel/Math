# Turn1: zero-face reduction and exhaustive proof through five coordinates

AI-assisted mathematical proof candidate, independent review pending. Original question unresolved1/5. The classical greedy and face facts are credited in SOURCE_GATE.md. The finite theorem here is computer-assisted, with complete search space justified below; it is not an all-dimension claim.

## 1. Canonical data

Write B=B(b)={x:x(S)<=b(S) for all S subset V, x(V)=b(V)}, with finite normalized submodular b, b(empty)=0. Since0 belongs to B, b(V)=0 and b(S)>=0. The base is bounded. Greedy optimization shows b(S)=max_{x in B}x(S), by taking all elements of S first in the permutation. Consequently the assumed integral vertices imply every b(S) is an integer, whether or not integrality was initially required of the given representation. For every S,

0<=b(S)<=min(|S|,|V−S|),

because each coordinate of every point of B lies in[-1,1] and the total sum is0.

For a permutation pi with prefixes S_j, its greedy vector has coordinates x_{pi(j)}=b(S_j)−b(S_{j−1}). These vectors are precisely the vertices, with possible repetition. A strict order of objective coefficients makes its greedy vector the unique optimizer, so none of the generated vectors is merely a nonvertex integer point.

## 2. Reduce to positive proper-subset functions

Choose a chain of zero sets

empty=S0 strictly contained in S1 strictly contained in ... strictly contained in Sk=V,

with b(S_i)=0, maximal under insertion of further zero sets. Let A_i=S_i−S_{i−1}, and on A_i define

b_i(T)=b(S_{i−1} union T)−b(S_{i−1})=b(S_{i−1} union T).

Each b_i is normalized submodular, has b_i(A_i)=0, and is strictly positive on every nonempty proper subset of A_i; otherwise another zero set could be inserted in the chain.

The face of B defined by x(S_i)=0 for all i is the Cartesian product of the B(b_i). Here is a direct verification. A point of that face restricts to a base of each b_i by applying the original inequality to S_{i−1} union T. Conversely suppose every block restriction is in B(b_i). For any S, put T_i=S intersect A_i. The sum of its block bounds is at most b(S): diminishing returns compares the increment of adding T_i to S_{i−1} with the increment of adding it to the smaller S intersect S_{i−1}; summing telescopes. The totals on the blocks are zero, so this point lies in B and in the stated face.

Each factor's vertices are coordinates of vertices of this face, hence of vertices of B, so their coordinates still lie in{−1,0,1}. Each factor contains0. If every factor has an opposite pair of vertices, concatenating these pairs gives opposite vertices of the face and therefore of B. A singleton block contributes the zero vertex. It therefore suffices in any dimension to prove the conjecture for functions with b(empty)=b(V)=0 and b(S)>0 for every nonempty proper S.

For these reduced instances the canonical integer bounds become

1<=b(S)<=min(|S|,n−|S|).

In particular singleton and cosingleton values equal1. No positivity of the original b on all proper sets was assumed; it has been obtained on the factors by a genuine face reduction.

## 3. Complete finite search for n<=5

For n=1 there is the singleton zero base. For n=2 or3 every nonempty proper value is forced to1. For n=4 only the six two-element subsets vary, each independently in{1,2}:64 candidate tables. For n=5 the ten two-element and ten three-element subsets vary in{1,2}:2^20=1,048,576 candidate tables. Thus the search space is complete after Section2's reduction, not a sample of generated matroids or cut functions.

A set function is submodular if and only if all elementary square inequalities hold:

b(S+i)+b(S+j)>=b(S)+b(S+i+j), for distinct i,j outside S.

Necessity is immediate. Sufficiency follows by telescoping these inequalities to obtain diminishing returns for adding one element to nested sets, and then telescoping over the elements of arbitrary differences. The enumerator tests exactly these inequalities; only accepted tables are processed.

For each accepted table it runs all n! greedy permutations, checks every coordinate is in{−1,0,1}, deduplicates the resulting vertices and tests for a pair of negative vectors. Coordinates are encoded as ternary digits v_i+1; negation sends code c to3^n−1−c. Integer arithmetic is exact and no tolerance or LP solver is used.

The complete output is:
- n1:1 candidate,1 accepted,1 vertex
- n2:1 candidate,1 accepted,at most2 vertices
- n3:1 candidate,1 accepted,at most6 vertices
- n4:64 candidates,all64 accepted,at most14 vertices
- n5:1,048,576 candidates,4,209 accepted,at most31 vertices
Every accepted table has an opposite greedy-vertex pair. Consequently, together with the factor reduction, the original opposite-vertex assertion holds for every ground set of size at most5. It also holds in arbitrary ambient dimension whenever all blocks in a maximal zero-set-chain reduction have size at most5.

The largest accepted case is not asserted extremal beyond the enumerated range. The arbitrary-dimensional conjecture is untouched outside the stated block class.

## 4. Reproduction and finite-proof boundaries

Compile and run:

g++ -std=c++17 -O2 turn1/enumerate_small.cpp -o /tmp/opposite-small
/tmp/opposite-small

Compare stdout byte-for-byte with turn1/verification.json. The source contains no network operations or external dependencies. It checks21,704,870 elementary inequalities during rejection/acceptance and2,531,567 greedy coordinates, and separately verifies one opposite witness per accepted table. These counts do not include any arbitrary-dimensional inference.

The output includes per-size counts and an FNV64 rolling checksum of (table mask, selected witness) rows. These witness rows are deterministically regenerable, but the full streams are not retained; the checksum is not a stored certificate or cryptographic proof. The proof of complete coverage is Sections1–3 plus the auditable enumeration code. An independent implementation is appropriate for final review. All classical structure results and source-known special cases retain their credit; no novelty claim is made.
