#!/usr/bin/env python3
"""Offline provenance adapter for the unchanged meromorphic checker.

Only digest(PDFS/known-primary-name) is supplied from the frozen source manifest.
No PDF contents are mathematical inputs. All other digests and main() execute
unchanged. This mode does NOT re-read/re-verify external primary PDFs.
The harness's --primary-dir mode instead runs the original script directly.
"""
from pathlib import Path
import json,sys

def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    script=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve()
    ns={'__name__':'portable_meromorphic_archived','__file__':str(script)}
    exec(compile(script.read_bytes(),str(script),'exec'),ns)
    source=json.loads((ns['SOURCE']/'source_manifest.json').read_text())
    supplied={ns['PDFS']/r['file']:r['sha256'] for r in source['sources']}
    known={'invariants_v11.pdf':'c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da','invariants_final.pdf':'c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42','stachel_published.pdf':'9121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8'}
    if {p.name:h for p,h in supplied.items()}!=known or len(supplied)!=3:
        raise ValueError('Expected exactly three known attested primary hashes')
    original_digest=ns['digest'];seen=[]
    def attested_digest(path):
        path=Path(path)
        if path in supplied:
            seen.append(path.name);return supplied[path]
        return original_digest(path)
    ns['digest']=attested_digest
    sys.argv=[str(script),'--output',str(output)]
    ns['main']()
    if sorted(seen)!=sorted(p.name for p in supplied):raise ValueError('Unexpected preflight use')
if __name__=='__main__':main()
