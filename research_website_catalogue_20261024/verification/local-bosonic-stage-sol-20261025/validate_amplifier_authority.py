"""Falsify the exact proposed amplifier authority expressions in memory."""
from pathlib import Path
import ast, copy, hashlib, json, re, datetime
O=Path(__file__).resolve().parent;R=O.parents[1];p=R/'papers/22089807'
c=json.loads((p/'publication.json').read_text());gate=json.loads((p/'promotion.json').read_text());binding=c['source_binding']
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
clearance_path=R/gate['root_clearance_file'];clearance=json.loads(clearance_path.read_text())
source=(O/'final-content-check.proposed.py').read_text();tree=ast.parse(source)
tests={}
for n in ast.walk(tree):
    if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='test' and n.args and isinstance(n.args[0],ast.Constant):
        name=n.args[0].value
        if name in ['root_authority_and_scope','original_custom_review_bindings','historical_scope_hold_preserved','standard_original_receipt_metadata_assets','tex_and_abstract_hashes','standalone_reader_never_substituted']:
            tests[name]=compile(ast.Expression(n.args[1]),'<exact proposed checker expression>','eval')
textpath=p/binding['source_tex_path'];a=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',textpath.read_text(),re.S).group(1)
raw_receipt=json.loads((p/'sources/receipt.json').read_text());receipt=copy.deepcopy(raw_receipt)
f=O/'public/research'/c['slug']/'index.html';h=f.read_text()
env=dict(p=p,R=R,c=c,gate=gate,binding=binding,sha=sha,clearance=clearance,clearance_path=clearance_path,raw_receipt=raw_receipt,receipt=receipt,receipt_file=p/'sources/receipt.json',record_file=p/'sources/record.json',asset_root=p/'sources',rid='22089807',asset_name=lambda x:x.get('name',x.get('filename')),hashlib=hashlib,json=json,textpath=textpath,a=a,f=f,frames=[1],texts=[1]*21,TEX_PATHS={'22089807':binding['source_tex_path'].removeprefix('sources/')})
for name,expr in tests.items():assert eval(expr,env),name
cases=[]
def reject(name,test,edit):
    altered={k:copy.deepcopy(v) if isinstance(v,(dict,list)) else v for k,v in env.items()};edit(altered)
    try:value=eval(tests[test],altered)
    except (KeyError,TypeError,ValueError):value=False
    assert not value,name
    cases.append({'case':name,'exact_proposed_check':test,'rejected':True,'original_inputs_mutated':False})
reject('root-object-rewrite','root_authority_and_scope',lambda e:e['clearance'].update(approved_scope='unsupported'))
reject('root-hash-rewrite','root_authority_and_scope',lambda e:e['gate'].update(root_clearance_sha256='0'*64))
reject('historical-scope-pass-rewrite','historical_scope_hold_preserved',lambda e:e['gate']['reviews']['scope']['verdict'].update(promotion_authorized=True))
reject('original-analytic-verdict-rewrite','original_custom_review_bindings',lambda e:e['gate']['reviews']['analytic']['verdict'].update(verdict='rewritten'))
reject('original-adversarial-verdict-rewrite','original_custom_review_bindings',lambda e:e['gate']['reviews']['adversarial']['verdict'].update(verdict='rewritten'))
reject('raw-receipt-schema-rewrite','standard_original_receipt_metadata_assets',lambda e:e.update(raw_receipt=[]))
def tamper_hash(relative):
    return lambda e:e.update(sha=lambda path:'0'*64 if path==p/relative else sha(path))
reject('source-receipt-tamper','standard_original_receipt_metadata_assets',tamper_hash('sources/receipt.json'))
reject('source-metadata-tamper','standard_original_receipt_metadata_assets',tamper_hash('sources/record.json'))
reject('original-source-tex-tamper','tex_and_abstract_hashes',tamper_hash(binding['source_tex_path']))
reject('original-report-tamper','original_custom_review_bindings',tamper_hash(gate['reviews']['analytic']['report']))
reject('original-verdict-bytes-tamper','original_custom_review_bindings',tamper_hash(gate['reviews']['adversarial']['verdict_file']))
reject('embedded-reader-substitution','standalone_reader_never_substituted',lambda e:e.update(sha=lambda path:binding['embedded_pdf_sha256'] if path==f.parent/c['pdf_filename'] else sha(path)))
target=O/'amplifier-authority-negative-controls.json';assert not target.exists();target.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','controls_rejected':len(cases),'method':'Exact expressions extracted from the final proposed checker, with copied in-memory objects and intercepted read-only hashes. No original files changed.','cases':cases},indent=2)+'\n')
print('PASS',len(cases),'amplifier authority mutation controls')
