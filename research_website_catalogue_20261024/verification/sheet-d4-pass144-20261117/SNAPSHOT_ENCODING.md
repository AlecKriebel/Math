The native CellData and eight-tab metadata snapshots are stored losslessly as
`recursive-json-intern-v1` to avoid repeating identical formatting objects.
The top-level `root` is a reference into `nodes`. A primitive is unchanged.
For `{"$ref": n}`, read nodes[n]: an array node decodes its `items` in order;
an object node decodes its ordered `[key, value]` pairs from `entries`.
Apply the same rule recursively. Equal structured objects share a node.
The before snapshots were encoded and decoded in memory and compared to the
complete native structured response before the two-cell mutation. Readback
comparisons used complete uncompressed native CellData and metadata objects.
