#!/usr/bin/env python3
"""Source-only expectation closure. No writer/site paths, network, writes or science."""
from pathlib import Path
import hashlib
import json
import sys

A=Path(__file__).resolve().parent
checks=0
def need(c,m):
    global checks
    checks+=1
    if not c:raise ValueError(m)
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def check(e):
    p=Path(e['path']);b=p.read_bytes()
    need(not p.is_symlink(),'input symlink '+str(p))
    need(len(b)==e['bytes'] and sha(b)==e.get('SHA256',e.get('sha256')),'input bytes '+str(p))
    return b
def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return list(a)==list(b) and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def main():
    pre=sys.argv[1:]==['--preseal']
    need(pre or not sys.argv[1:],'only --preseal accepted')
    need(pre or (A/'INITIAL_EXPECTATIONS_SEAL.json').is_file(),'default requires initial seal')
    if not pre:
        se=load(A/'INITIAL_EXPECTATIONS_SEAL.json')
        need(se['status']=='SOURCE_ONLY_INDEPENDENT_EXPECTATIONS_SEALED_AWAITING_TWO_GATES','literal initial status')
        for e in se['bindings'].values():check(e)
    man=load(A/'INITIAL_MANIFEST.json')
    for e in man['files']:check(e)
    need(not any(p.is_symlink() for p in A.rglob('*')),'no audit symlinks')
    inputs=load(A/'INPUT_MANIFEST.json')
    need(inputs['website_or_writer_namespace_paths']==[],'source-only input interface')
    for e in inputs['files']:check(e)
    protected=load(A/'PROTECTED_NAMESPACE_MANIFEST.json')
    need([x['complete_file_count'] for x in protected['namespaces']]==[121,69,81,59],'four complete namespace extents')
    for ns in protected['namespaces']:
        root=Path(ns['path'])
        need(not any(p.is_symlink() for p in root.rglob('*')),'protected namespace symlinks')
        need({str(p) for p in root.rglob('*') if p.is_file()}=={e['path'] for e in ns['files']},'protected complete namespace membership')
        for e in ns['files']:check(e)
    expect=load(A/'INDEPENDENT_EXPECTATIONS.json')
    need(expect['held_gates']=={'actual_new_website_GO_received':False,'writer_immutable_FINAL_received':False,'website_baseline_inspected_listed_or_frozen':False,'writer_stage_code_copy_or_opinions_read':False,'production_authority':False},'historical initial gates retained')
    paths=load(A/'EXPECTED_OUTPUT_PATHS.json')
    need(len(paths['paths'])==11 and len({e['website_relative_path'] for e in paths['paths']})==11,'exact eleven proposed outputs')
    need(sum(e['kind']=='unchanged_native_asset' for e in paths['paths'])==5,'five unchanged native originals')
    need(sum(e['kind']=='unchanged_adopted_Bib' for e in paths['paths'])==2,'two unchanged adopted Bibs')
    for t in expect['targets']:
        rid=t['record_id'];base=A/'inputs'/rid;c=load(base/'publication.json');ad=load(base/'ROOT_EDITORIAL_ADOPTION.json');src=load(base/'SOURCE_READY.json')
        main=(base/'PUBLIC_MAIN.html').read_text();tr=ad['future_exact_reader_only_transform_authorized']
        need(main.startswith('<main>') and main.count(tr['from'])==1,'literal two-edit transformation preconditions')
        expected=main.replace(tr['from'],tr['to'],1).replace('<main>','<main id="main">',1)
        need(check(t['expected_complete_transformed_main'])==expected.encode(),'whole independently expected main bytes')
        need(c['abstract']==t['full_unchanged_abstract']==ad['original_full_abstract'],'whole abstract')
        need(c['follow_up'] is None and c['code_license'] is None,'literal followup/code instrument nulls')
        need(c['canonical_url'] is None and c['AA'] is None and c['proposed_canonical_url'] is None,'historical private canonical nulls')
        need(src['version_field_present'] is (rid=='23440943'),'native version presence')
        need(src['version']==('1.0.0' if rid=='23440943' else None),'literal native version')
        need(c['publication_date']==('2026-10-17' if rid=='23440943' else '2026-10-15'),'original publication date')
        need(same(c['source_binding']['whole_original_source_ready'],src),'entire typed ordered SOURCE_READY retained')
        need([e['filename'] for e in t['native_assets_and_media_expectations_in_original_order']]==ad['actual_native_order'],'native encoding order')
        for e in t['native_assets_and_media_expectations_in_original_order']:
            b=check(e['whole_original_source_asset'])
            need(hashlib.md5(b).hexdigest()==e['whole_original_source_asset']['original_api_file_object']['checksum'].split(':')[1],'native checksum')
            need(e['contentUrl']==ad['future_proposed_canonical_url']+e['filename'],'article-root future asset URL')
        need(c['prepared_bibtex']==(base/'citation.bib').read_text(),'whole Bib exact')
    ledger=load(A/'WHOLE_LITERAL_OBJECT_LEDGER.json')
    need(len(ledger['whole_literal_wrappers'])==67,'complete wrapper occurrence ledger')
    for e in ledger['whole_literal_wrappers']:
        value=load(Path(e['container_file']))
        for part in e['pointer'].split('/')[1:]:
            key=part.replace('~1','/').replace('~0','~');value=value[int(key)] if isinstance(value,list) else value[key]
        need(same(value['whole_literal_object'],json.loads(check(e['whole_original_binding']))),'entire original typed/key/list/null literal wrapper')
    plan=expect['planning_only']
    need(plan['current_root_report']['independently_measured_here'] is False,'current count attribution')
    need(plan['required_future_baseline_after_separate127128_publication_and_root_GO']['independently_measured_here'] is False,'future baseline not measured')
    need(plan['proposed_after_this_two_article_stage']['independently_measured_here'] is False,'candidate counts are planned')
    print(json.dumps({'status':'PASS_SOURCE_ONLY_INITIAL_EXPECTATIONS','checks':checks,'protected_complete_files':330,'whole_literal_wrapper_occurrences':67,'proposed_outputs':11,'website_or_writer_namespace_reads':0,'network':0,'writes':0,'subprocesses':0,'project_imports':0,'scientific_execution':0,'full_audit_complete':False},indent=2))
if __name__=='__main__':main()
