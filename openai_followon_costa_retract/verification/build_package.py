#!/usr/bin/env python3
"""Assemble the explicitly curated publication files, excluding reading copies/caches."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]

def main():
    entries={
      'main.tex':'manuscript/main.tex',
      'README.md':'publication/PACKAGE_README.md',
      'LICENSES.md':'publication/LICENSES.md',
      'THIRD_PARTY_NOTICES.md':'publication/THIRD_PARTY_NOTICES.md',
      'LICENSE.upstream-APACHE-2.0.txt':'publication/LICENSE.upstream-APACHE-2.0.txt',
      'requirements.txt':'verification/stabilization/requirements.txt',
      'check_stabilization.py':'verification/stabilization/check_stabilization.py',
      'check_nonpolynomiality_certificates.py':'notes/nonpolynomiality/check_certificates.py',
      'checks/stabilization_result.json':'verification/stabilization/result.json',
      'checks/nonpolynomiality_identities.txt':'notes/nonpolynomiality/symbolic_audit.txt',
      'audits/stabilization.md':'notes/stabilization/AUDIT.md',
      'audits/nonpolynomiality.md':'notes/nonpolynomiality/audit.md',
      'audits/bundle_lift.md':'notes/nonpolynomiality/bundle_skeptic/audit.md',
      'audits/formal_scope.md':'notes/formal_scope/README.md',
      'audits/formal_declarations.json':'notes/formal_scope/declaration_map.json',
      'audits/formal_mechanical_receipt.json':'notes/formal_scope/mechanical_receipt.json',
      'audits/priority.md':'notes/priority/PRIORITY_AUDIT.md',
      'audits/priority_search_log.md':'notes/priority/SEARCH_LOG.md',
      'audits/verified_citations.bib':'notes/priority/VERIFIED_CITATIONS.bib',
      'provenance/manuscript_source_hashes.json':'sources/PINNED_SOURCE_MANIFEST.json',
      'provenance/lean_source_hashes.json':'notes/formal_scope/source_manifest.json',
      'provenance/literature_source_hashes.json':'sources/priority/SOURCE_MANIFEST.json',
      'DEPENDENCY_LEDGER.md':'DEPENDENCY_LEDGER.md',
      'THEOREM_LEDGER.md':'THEOREM_LEDGER.md',
    }
    output=ROOT/'publication/upload-kit';output.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'manuscript/main.pdf',output/'paper.pdf')
    payload={name:(ROOT/path).read_bytes() for name,path in entries.items()}
    # Apache-licensed pinned source closure, with our minimal build configuration.
    lean=ROOT/'verification/lean_copy'
    for path in sorted(lean.rglob('*')):
        if path.is_file() and (path.suffix=='.lean' or path.name=='lean-toolchain'):
            if '.lake' not in path.parts:
                payload['lean/'+str(path.relative_to(lean))]=path.read_bytes()
    payload['lean/README.md']=b'Pinned OpenAI family 047 sources, Apache 2.0; unchanged OAI modules.\nThe minimal Lake configuration is an audit adaptation excluding unrelated dependencies.\nRun lake update; lake exe cache get; lake build OAI.Algebra.AffineCancellation.Main; lake env lean PrintAxioms.lean.\nThese commands require sufficient disk and network. Full proof compilation was NOT reproduced in this package audit.\nSee ../audits/formal_scope.md and ../provenance/lean_source_hashes.json.\n'
    for name in ['lake_update.log','model_lean_attempt.log','targeted_lean_attempt.log']:
        payload['audits/formal_scope_logs/'+name]=(ROOT/'notes/formal_scope'/name).read_bytes()
    inner={'source_commit':'adc7f1241b42e322a6451854ab7e4b4c146bf78a','files':{n:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())}}
    payload['CONTENTS.json']=(json.dumps(inner,indent=2)+'\n').encode()
    with zipfile.ZipFile(output/'source-and-verification.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(payload.items()):
            info=zipfile.ZipInfo(name,date_time=(2026,10,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16;z.writestr(info,data)
    receipt={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(output.iterdir()) if p.is_file()}
    receipt['zenodo-deposit.json']={'sha256':hashlib.sha256((ROOT/'zenodo-deposit.json').read_bytes()).hexdigest()}
    (ROOT/'publication/PACKAGE_HASHES.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
