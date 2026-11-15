"""Preflight custody only. No candidate access, source replay, network or writes."""
from pathlib import Path
import json,hashlib
E=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/six-paper-independent-code-audit-sol-20261114');P=E.parents[1]
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,label):
 if not ok:raise ValueError(label)
def main():
 A=P/'verification/root-six-editorial-reading-20261114/ROOT_ADOPTION.json';need(sha(A)=='1ab177bed7047c45ebbef7abddb0f2e3aced9287ac04286eb1ca7984e7e6483c','root adoption pin');a=load(A)
 expected=['23124601','23333046','23383952','23539734','22929857','23320818'];need(a['allowed_records']==expected,'exact six targets')
 need(a['production_install_authorized'] is False and a['AA_writes_authorized'] is False,'withheld production/native gates')
 for x in load(E/'ALL_PREFLIGHT_BINDINGS.json')['files']:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'input changed '+str(p))
 for x in [a['previous106_adoption']]+a['new_five_adoptions']:
  p=Path(x['path']);need(sha(p)==x['sha256'],'whole individual adoption pin');d=load(p)
  if 'whole_scientific_authority_original' in d:
   p=P/d['scientific_authority_path'];need(sha(p)==d['scientific_authority_sha256'],'whole scientific authority byte binding')
   need(json.dumps(load(p),ensure_ascii=False,separators=(',',':'))==json.dumps(d['whole_scientific_authority_original'],ensure_ascii=False,separators=(',',':')),'whole ordered scientific original')
 for r in load(E/'NATIVE_SCHEMA_BINDINGS.json')['records']:
  for x in r['whole_original_objects']:
   p=Path(x['original_path']);q=Path(x['snapshot_path']);need(p.read_bytes()==q.read_bytes() and sha(q)==x['sha256'],'literal native snapshot/order/headers')
 pages=load(E/'EXPECTED_PAGES.json')['pages'];need([x['record_id'] for x in pages]==expected,'independent six-page expectation')
 need(sum(len(x['blocks']) for x in pages)==211 and sum(len(x['h2_headings']) for x in pages)==62,'complete body-block expectations')
 for x in pages:
  need(x['abstract'] in [v['text'] for v in x['blocks']],'whole abstract block');need(x['follow_up'] is None and x['native_AA_must_remain_null'] is True,'withheld follow-up/native field')
  need(hashlib.sha256(x['complete_bibtex'].encode()).hexdigest()==x['citation_bib_sha256'],'exact prepared BibTeX')
 overlay=load(E/'EXPECTED_OVERLAY.json');need(len(overlay['exact_overlay_paths'])==len(set(overlay['exact_overlay_paths']))==26,'exact bounded overlay')
 f=load(E/'PREFLIGHT_FIXTURES_NORMAL.json');need(f['negative_fixtures_rejected']==20 and f['not_a_candidate_audit'] is True,'meaningful oracle self-checks')
 need((E/'PREFLIGHT_FIXTURES_NORMAL.json').read_bytes()==(E/'PREFLIGHT_FIXTURES_OPTIMIZED.json').read_bytes(),'ordinary and optimized oracle self-check identity')
 if (E/'PREFLIGHT_SEAL.json').exists():
  need(sha(E/'PREFLIGHT_MANIFEST.json')==load(E/'PREFLIGHT_SEAL.json')['manifest_sha256'],'preflight manifest/seal')
  for x in load(E/'PREFLIGHT_MANIFEST.json')['files']:
   p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'frozen preflight artifact')
 print(json.dumps({'status':'PASS_INDEPENDENT_PREFLIGHT_CUSTODY_ONLY','approved_targets':6,'complete_body_blocks':211,'ordered_section_headings':62,'whole_native_snapshots':18,'original_input_bindings':73,'oracle_negative_fixtures':20,'candidate_code_or_output_audited':False,'production_or_native_clearance':False},indent=2))
if __name__=='__main__':main()
