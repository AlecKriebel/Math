"""Parent-requested outer-document repair; verification ZIP bytes stay fixed."""
from pathlib import Path
import datetime,hashlib,json
H=Path(__file__).absolute().parent;A=H.parent;C=A/'candidate';T=H/'private_tmp'
def require(ok,msg):
    if not ok:raise ValueError(msg)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
tool=(A/'publication_tools_01/portable.py').read_bytes();require(pin(tool)['sha256']=='bcaac73bf1620098e0d24f2a2cb9399613567be6018b99329c0a58b6e0101910','frozen tool')
m={'__name__':'frozen_portable_API','__file__':str(A/'publication_tools_01/portable.py')};exec(compile(tool,m['__file__'],'exec',optimize=0),m)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
old={n:(C/n).read_bytes() for n in ('PUBLICATION.md','LITERATURE_AND_SCOPE.md','CURRENT_PUBLICATION_MANIFEST.json')}
oldcore=(H/'CANDIDATE_CORE_PINS.json').read_bytes();oldseal=(H/'SEALED_CANDIDATE_RECEIPT.json').read_bytes()
for n,b in old.items():(T/('before_outer_guides_'+n)).write_bytes(b)
(T/'before_outer_guides_CANDIDATE_CORE_PINS.json').write_bytes(oldcore)
(T/'before_outer_guides_SEALED_CANDIDATE_RECEIPT.json').write_bytes(oldseal)
publication='''# Current publication and verification guide

Version1.0.0,16October2026. The current paper is [the PDF](rank-two-fano-note.pdf),
with actual [TeX source](note.tex). See [README.md](README.md) for scope,
dependency trust, priority and AI-review disclosures, and executable commands.

The current outer authority is [CURRENT_PUBLICATION_MANIFEST.json](CURRENT_PUBLICATION_MANIFEST.json),
authenticated by its separately supplied SHA256. The portable ZIP is
[rank-two-fano-verification.zip](rank-two-fano-verification.zip); its
[package index](verification/package_index.json) also requires an independent
SHA256. Current checks use portable.py with the README's current/verify commands.
Only the PDF and verification ZIP are declared deposit assets.

All21original files are unchanged in [verification/source/](verification/source/).
The legacy PUBLICATION_MANIFEST.json and verify_publication.py describe and
check that original-only21file format; they are preserved historical evidence,
not the current expanded outer-packet authority or top-level checking command.
The current wrapper replays the original launcher/checkers in a private isolated
copy while authenticating the full current evidence inventory separately.

The current bounded priority disposition is in
[FINAL_PRIORITY_DISPOSITION.md](verification/root_evidence/FINAL_PRIORITY_DISPOSITION.md).
Historical reports and earlier fixture receipts are dated snapshots. They do
not establish final whole-package clearance, novelty, human peer review, formal
verification or publication approval. Original claimed research effort1/5 is
unchanged. This guide was updated during final assembly at '''+now+'''.
'''
(C/'PUBLICATION.md').write_text(publication)
header=('> Current-context header added '+now+'. The body below is the unchanged\n> historical7October2026 literature/scope snapshot. For the current paper,\n> see [note.tex](note.tex) and [the PDF](rank-two-fano-note.pdf); for current\n> Li–Li and Miao–Wang January2024 chronology and remaining priority limits,\n> see [FINAL_PRIORITY_DISPOSITION.md](verification/root_evidence/FINAL_PRIORITY_DISPOSITION.md).\n> The original unprefixed file is preserved in verification/source/.\n\n').encode()
(C/'LITERATURE_AND_SCOPE.md').write_bytes(header+old['LITERATURE_AND_SCOPE.md'])
for n in ('PUBLICATION.md','LITERATURE_AND_SCOPE.md'):require((C/'verification/source'/n).read_bytes()==(A/'source'/n).read_bytes(),'source copy changed')
blobs={p.relative_to(C).as_posix():m['read_regular'](p) for p in C.rglob('*') if p.is_file() and p.name!='CURRENT_PUBLICATION_MANIFEST.json'}
require(len(blobs)==178,'unexpected current payload size')
index={'schema':m['CURRENT_SCHEMA'],'problem_id':'30005079','files':[{'path':n,**pin(b)} for n,b in sorted(blobs.items())]}
raw=(json.dumps(index,indent=2,sort_keys=True)+'\n').encode();(C/'CURRENT_PUBLICATION_MANIFEST.json').write_bytes(raw);blobs['CURRENT_PUBLICATION_MANIFEST.json']=raw
m['current_inputs'](C,pin(raw)['sha256']);m['closed_tree'](C,set(blobs))
core={'schema':'rank-two-fano-30005079-final-candidate-core-v1','problem_id':'30005079','head':'a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7','files':[{'path':n,**pin(b)} for n,b in sorted(blobs.items())]}
coreraw=(json.dumps(core,indent=2,sort_keys=True)+'\n').encode();(H/'CANDIDATE_CORE_PINS.json').write_bytes(coreraw)
receipt={'timestamp_utc':now,'completion_estimate_percent':75,'scope':'Parent-requested current outer documentation repair; no portable ZIP/index, source21, tool, preprint or frozen audit changes.','changed_outer_documents':['PUBLICATION.md','LITERATURE_AND_SCOPE.md'],'previous_document_pins':{n:pin(old[n]) for n in ('PUBLICATION.md','LITERATURE_AND_SCOPE.md')},'current_document_pins':{n:pin(blobs[n]) for n in ('PUBLICATION.md','LITERATURE_AND_SCOPE.md')},'unchanged_ZIP':pin(blobs['rank-two-fano-verification.zip']),'unchanged_portable_index':pin(blobs['verification/package_index.json']),'previous_outer_manifest':pin(old['CURRENT_PUBLICATION_MANIFEST.json']),'current_outer_manifest':pin(raw),'previous_core_pin_list':pin(oldcore),'current_core_pin_list':pin(coreraw),'outer_original_changes_only':['README.md','RESEARCH_LOG.md','PUBLICATION.md','LITERATURE_AND_SCOPE.md'],'actual_final_current_replays_required':True,'pre_repair_seal_raws_preserved_privately':True}
(H/'OUTER_CURRENT_GUIDE_REPAIR_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
seal=json.loads(oldseal);seal.update(timestamp_utc=now,core_pin_list=pin(coreraw),current_manifest=pin(raw),outer_original_changes_only=receipt['outer_original_changes_only'],scope='Closed final candidate byte sealing after parent-requested outer guide repairs; current actual normal/O replay and independent ZIP reconstruction remain to run.')
(H/'SEALED_CANDIDATE_RECEIPT.json').write_text(json.dumps(seal,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'RESEALED_AFTER_OUTER_GUIDE_REPAIR','current_manifest':pin(raw),'core':pin(coreraw),'ZIP':pin(blobs['rank-two-fano-verification.zip'])},indent=2))
