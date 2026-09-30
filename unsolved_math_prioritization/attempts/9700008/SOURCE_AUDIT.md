# Source and convention audit

Checked 2026-09-30.

The complete original [Aldous problem page](https://www.stat.berkeley.edu/~aldous/Research/OP/cayley.html)
was read, along with its [maintained index](https://www.stat.berkeley.edu/~aldous/Research/OP/index.html).
The source dates its first web posting to March 2009. It describes the
geometric-stopping stationary law, explicitly defines a uniform endpoint at
zero, and lists three questions. Two comparison expressions use infinity,
although its parameter was defined only between zero and one. The page
provides no definition of that infinity endpoint or change of variable.

The pinned dataset paraphrases this as an “endpoint value.” That paraphrase
does not identify an endpoint. The partial result preserves the original
ambiguity and keeps the whole bundled record unresolved. Its negative
comparison with the uniform endpoint is expressly conditional on that
interpretation. It does not refute an expression with no specified meaning.

The standard conventions were checked against the same author's book with
James Fill:

- [Chapter 11, Section 2.1](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch11.S2.html)
  gives symmetric-proposal acceptance as the minimum of one and the target
  weight ratio, with rejection producing a self-loop.
- [Chapter 4, Section 4](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch4.S4.html)
  defines discrete-time relaxation through the second largest eigenvalue
  in algebraic order. It explicitly includes the complete graph as an example.
- [Chapter 3, Section 6.3, Theorem 3.25](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S6.html)
  states the variance/Dirichlet-form characterization used for the flow bound.

The counterexample is an undirected complete Cayley graph, so neither
nonreversibility nor a nonuniform proposal is introduced. A four-vertex
instance also defeats the absolute-gap interpretation; fixed laziness is
handled explicitly. The growing family uses unbounded degree, and therefore
does not purport to refute a separately restricted bounded-degree comparison.

Searches for the exact problem title, geometric-stopping Metropolis chains,
and Aldous's Cayley relaxation questions found no primary source clarifying
the infinity notation. They did not establish historical priority for these
elementary calculations. General MCMC comparison results and results about
unweighted random walks on regular graphs are not substituted for the
specific source model.

The complete pinned record and its earlier triage report are preserved in
[source_record.json](source_record.json), with attribution to
[ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath),
revision `37e53eabe540fb458758e198be61634bd02ee008`, CC-BY-4.0. The upstream
report asserts no verified solution and is treated as search guidance only.
Hashes of the retrieved primary pages are in
[source_manifest.json](source_manifest.json); third-party HTML is not
redistributed in this package. No outside contact was made.
