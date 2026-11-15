#!/usr/bin/env python3
"""Read-only, offline closure; optional bounded own replay; no source programme rerun."""
from pathlib import Path, PurePosixPath
import json,hashlib,argparse,subprocess,sys

ROOT=Path(__file__).resolve().parent
SOURCE=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/22983513/sources')
EARLY='e4ea462ab222efa5a602d428f6d49ec58e96a357010b6e35404913a2e0ab1590'
READY='9ab3aa2364dbc078c0cae228e9a627b75586a6da5f9a1a4c2111391c5bd5ca20'
LITERAL='The full stated strict Yang and finite Dirichlet-gap nonattainment claims are supported; no substantive gap found.'


def need(x,m):
    if not x:raise RuntimeError(m)


def sha(b):return hashlib.sha256(b).hexdigest()


def safe(s):
    need(type(s) is str and s and '\\' not in s and ':' not in s and '\x00' not in s,'Invalid relative path')
    q=PurePosixPath(s);need(not q.is_absolute() and '..' not in q.parts and q.as_posix()==s,'Unsafe relative path');return Path(s)


def blob(b,r):
    need(type(r['bytes']) is int and r['bytes']>=0 and len(b)==r['bytes'] and sha(b)==r['SHA256'],'Whole-byte mismatch')


def record(base,r):
    q=base/safe(r['path']);need(q.is_file() and not q.is_symlink() and q.resolve().is_relative_to(base),'Missing, linked or escaped payload');blob(q.read_bytes(),r)


def negatives():
    n=0
    for s in ['', '../x', '/x', 'a/../x', 'a\\x', 'a:x', 'a//x']:
        try:safe(s)
        except RuntimeError:n+=1
        else:raise RuntimeError('Path rejection escaped')
    for b,r in [(b'a',{'bytes':2,'SHA256':sha(b'a')}),(b'b',{'bytes':1,'SHA256':sha(b'a')}),(b'a',{'bytes':True,'SHA256':sha(b'a')})]:
        try:blob(b,r)
        except RuntimeError:n+=1
        else:raise RuntimeError('Binding rejection escaped')
    return n


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preseal',action='store_true');ap.add_argument('--replay-own',action='store_true');args=ap.parse_args()
    mb=(ROOT/'OWNED_MANIFEST.json').read_bytes();m=json.loads(mb);need(m['record_id']==22983513 and m['owned_root']==str(ROOT),'Wrong packet identity')
    actual=set()
    for q in ROOT.rglob('*'):
        need(not q.is_symlink(),'Unexpected symlink')
        if q.is_file():actual.add(q.relative_to(ROOT).as_posix())
    names=[r['path'] for r in m['files']];need(len(names)==len(set(names)),'Duplicate owned paths');need(set(names)==actual-{'OWNED_MANIFEST.json','FINAL_SEAL.json'},'Owned inventory mismatch')
    for r in m['files']:record(ROOT,r)
    if not args.preseal:
        seal=json.loads((ROOT/'FINAL_SEAL.json').read_bytes());need(seal['record_id']==22983513 and seal['owned_manifest_SHA256']==sha(mb),'Final seal mismatch');need(seal['source_bindings_SHA256']==sha((ROOT/'SOURCE_BINDINGS.json').read_bytes()),'Source-binding seal mismatch');need(seal['early_seal_SHA256']==EARLY,'Wrong early pin');need(seal['scientific_findings_withheld_pending_root119_gate'] is True,'Historical gate flag changed')
    eb=(ROOT/'EARLY_INDEPENDENCE_SEAL.json').read_bytes();need(sha(eb)==EARLY,'Early seal changed');e=json.loads(eb);em=(ROOT/e['manifest']).read_bytes();need(sha(em)==e['manifest_SHA256'],'Early manifest changed')
    early=json.loads(em)['files']
    for r in early:record(ROOT/'early',r)
    need(e['actual_complete_PDF_pages_read']==3 and e['actual_complete_TeX_lines_read']==173 and e['fresh_individual_rasters_read']==3 and e['distinct_families']==8,'Early reading contract mismatch')
    need(e['foreign_science_code_results_triage_old_current_peer_opinions_before_seal'] is False and e['prior_acquisition_exposure']=='metadata/custody only; no scientific reading','Independence disclosure/history changed')
    sb=json.loads((ROOT/'SOURCE_BINDINGS.json').read_bytes());need(sb['source_root']==str(SOURCE),'Wrong source root');seen=set()
    for r in sb['bindings']:
        q=Path(r['path']);need(q.is_absolute() and not q.is_symlink() and q.is_file() and q.resolve().is_relative_to(SOURCE),'Source binding escaped');need(str(q) not in seen,'Duplicate source binding');seen.add(str(q));blob(q.read_bytes(),r)
    need(sha((SOURCE/'SOURCE_READY.json').read_bytes())==READY,'Original source readiness changed')
    v=json.loads((ROOT/'CUSTOM_VERDICT.json').read_bytes());need(v['literal_custom_verdict']==LITERAL and v['full_original_quantified_claim_checked'] is True and v['new_narrowing_or_extended_repair'] is False,'Literal verdict mismatch');need(v['source_site_core_Sheet_Git_docs_old_packet_mutations'] is False and v['root_only_adoption_authority'] is True,'Authority fence changed')
    own=(ROOT/'computations/own-normal.stdout').read_bytes();need(own==(ROOT/'computations/own-optimized.stdout').read_bytes(),'Own complete normal/optimized outputs differ');o=json.loads(own);need(o['status']=='PASS' and len(o['wrong_variant_or_model_falsifiers'])==8 and all(o['wrong_variant_or_model_falsifiers'].values()),'Own diagnostic outcome mismatch')
    for k,value in {'all_J_interval_formula_checks':300,'certified_box_gap_cases':5120,'validated_Fourier_tail_enclosures':12,'exact_Fourier_tail_summands':7012}.items():need(o['counts'][k]==value,'Own diagnostic coverage changed')
    for mode in ['normal','optimized']:
        rec=json.loads((ROOT/('computations/own-'+mode+'.receipt.json')).read_bytes());need(rec['exit_code']==0 and (ROOT/('computations/own-'+mode+'.stderr')).read_bytes()==b'','Own actual execution failed')
    native_dir=SOURCE/'attempts/20261115T032014Z/published-source/owr_3389_016_strict_gap/verification';native_result=(native_dir/'results.json').read_bytes();code=(native_dir/'verify.py').read_bytes();need((ROOT/'reproduction/supplied-verify.unchanged.py').read_bytes()==code,'Supplied code copy changed')
    for mode in ['normal','optimized']:
        rec=json.loads((ROOT/('reproduction/supplied-'+mode+'.receipt.json')).read_bytes());need(rec['exit_code']==0 and rec['original_code_unchanged'] is True and rec['actual_code_SHA256']==sha(code),'Supplied actual code/run mismatch');need(rec['complete_JSON_equal_to_original_results'] is True and rec['complete_output_bytes_equal_to_original_results'] is True,'Supplied reproduction mismatch');need((ROOT/('reproduction/supplied-'+mode+'.results.json')).read_bytes()==native_result,'Supplied complete output bytes differ');need((ROOT/('reproduction/supplied-'+mode+'.stderr')).read_bytes()==b'','Supplied stderr')
    r=json.loads(native_result);need(r['status']=='pass' and r['check_count']==7016 and r['boxes']['J_cases']==1312 and r['negative_controls']['expected_failures_detected']==3,'Original native result semantics changed')
    replay=False
    if args.replay_own:
        cmd=[sys.executable,'-E','-B']+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'own_controls.py')];z=subprocess.run(cmd,cwd=ROOT,capture_output=True,timeout=180);need(z.returncode==0 and z.stderr==b'' and z.stdout==own,'Read-only own full-output replay mismatch');replay=True
    print(json.dumps({'status':'PASS','record_id':22983513,'owned_payloads':len(names),'whole_source_bindings':len(seen),'early_payloads':len(early),'custody_negative_controls':negatives(),'own_bounded_replay':replay,'supplied_campaign_repeated':False,'source_or_site_or_owned_writes':0,'network':0,'preseal':args.preseal},sort_keys=True))


if __name__=='__main__':main()
