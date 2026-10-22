#!/usr/bin/env python3
"""Relocated finite replays and optional input identity checks; no global proof."""
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

def need(x,m):
    if not x: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def run(script,args=(),optimized=False,cwd=None):
    cp=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[str(script)]+list(map(str,args)),cwd=cwd,capture_output=True,text=True,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    need(cp.returncode==0 and not cp.stderr,'bounded replay failed: '+cp.stderr)
    return json.loads(cp.stdout)
def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    for n in ['catalog','problems','reports','dmms-pdf','dg-pdf','lms-pdf','published-pdf']:p.add_argument('--'+n,type=Path)
    a=p.parse_args();root=a.root.resolve();audit=root/'independent_audit';pins={
    'MANIFEST.json':(3374,'205501b7ebfe2f7449fb18d5832e330c122f567a936142affcdb81a93b738855'),
    'verify_audit.py':(5703,'ddaab01950c77a158f9dbf7885b6bc87de6e1651a1686e28c632bb113794c53a'),
    'mutation_checks.py':(5583,'f4b68ab01ce495e59690ca54c25ed9119c981ce8b68e38d5f872e88101644fb4')}
    for name,pin in pins.items():
        b=(audit/name).read_bytes();need((len(b),sha(b))==pin,'replay entry pin')
    result={'schema':'ep642-publication-replay-v1','finite_checks_prove_infinite_target':False,'original_optimized_checks_active':False,'corpus':'NOT_RUN','public_pdf_identity':'NOT_RUN','runs':{}}
    corpus=[a.catalog,a.problems,a.reports];need(all(corpus) or not any(corpus),'supply all three corpus files')
    if all(corpus):
        meta=json.loads((audit/'source_verification.json').read_bytes())['input_verification'];data=[];identities={}
        for path,key in zip(corpus,['catalog','problems','research_results']):
            b=path.read_bytes();v=meta[key];need((len(b),sha(b))==(v['bytes'],v['sha256']),'complete input mismatch: '+key);identities[key]={'bytes':len(b),'sha256':sha(b),'match':True};data.append(json.loads(b))
        c,pr,rr=data;cs=[x for x in c if str(x['id'])=='2228'];ps=[x for x in pr if str(x['id'])=='2228'];need(len(cs)==len(ps)==1,'unique exact ID');record=ps[0];report=rr.get(record['problem_number'],{});need(record['problem_number']=='EP-642' and cs[0]['rank']==900 and report=={},'target or report changed');pair=sha(json.dumps([record,report],sort_keys=True).encode());statement=sha(record['statement'].encode());need(pair==meta['pair_sha256'] and statement==meta['statement_sha256'],'complete target/report pair mismatch');result['corpus']={'status':'PASS','files':identities,'pair_sha256':pair,'statement_sha256':statement,'complete_target_and_report_checked':True,'unique_numeric_problem_id':True,'catalog_id_normalized_to_string':True,'rank':900,'report_empty':True}
    pdfs=[a.dmms_pdf,a.dg_pdf,a.lms_pdf,a.published_pdf];need(all(pdfs) or not any(pdfs),'supply all four PDF files')
    if all(pdfs):
        meta=json.loads((audit/'source_verification.json').read_bytes())['public_pdf_rehashes'];out=[]
        for path,v in zip(pdfs,meta):
            b=path.read_bytes();need(b.startswith(b'%PDF-') and (len(b),sha(b))==(v['bytes'],v['sha256']),'public PDF pin mismatch');out.append({'url':v['url'],'bytes':len(b),'sha256':sha(b),'match':True})
        result['public_pdf_identity']={'status':'PASS','files':out,'downloaded_during_this_run':False,'complete_paper_proofs_certified':False}
    with tempfile.TemporaryDirectory(prefix='ep642-publication-replay-') as tmp:
        tmp=Path(tmp);moved=tmp/'accepted';shutil.copytree(audit,moved)
        for optimized in [False,True]:
            mode='optimized' if optimized else 'normal'
            result['runs']['accepted_relocated_'+mode]=run(moved/'verify_audit.py',['--root',moved,'--expected-manifest-sha256',pins['MANIFEST.json'][1]],optimized,tmp)
            result['runs']['mutations_relocated_'+mode]=run(moved/'mutation_checks.py',[],optimized,tmp)
            result['runs']['independent_relocated_'+mode]=run(moved/'independent_checks.py',[moved/'corrected/validation.py'],optimized,tmp)
        for label in ['accepted_relocated','mutations_relocated','independent_relocated']:
            need(result['runs'][label+'_normal']==result['runs'][label+'_optimized'],'normal/optimized replay mismatch')
    m=result['runs']['mutations_relocated_normal'];need(len(m['semantic_mutations'])==10 and all(x['rejected'] for x in m['semantic_mutations']),'semantic rejection count');need(len(m['integrity_mutations'])==16 and all(x['rejected'] for x in m['integrity_mutations']),'integrity rejection count')
    result.update(normal_optimized_equal=True,semantic_mutation_rejections=10,integrity_mutation_rejections=16,scope='Finite corroboration, byte identity, and validation hardening only. No full solution, asymptotic improvement or novelty certification.')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
