"""Read-only closed-member seal, source-identity, dedup and bookkeeping checks."""
from pathlib import Path
import json,gzip,hashlib,subprocess,sys,copy
P=Path(__file__).resolve().parent
class Failure(RuntimeError):pass
def need(ok,label):
 if not ok:raise Failure(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def obj(n):return json.loads((P/n).read_bytes())
def raw(k):return gzip.decompress((P/'private/sources'/(k+'.gz')).read_bytes())
def frozen():
 m=obj('MANIFEST.json');want=m['files'];actual={str(x.relative_to(P)) for x in P.rglob('*') if x.is_file() and x.name!='MANIFEST.json'}
 need(actual==set(want),'closed member set')
 for name,z in want.items():
  b=(P/name).read_bytes();need(len(b)==z['bytes'] and sha(b)==z['sha256'],'sealed bytes '+name)
 need(sum(x.stat().st_size for x in P.rglob('*') if x.is_file())<=8*1024*1024,'8MiB cap')
def rowcheck(r):
 need(r['result_family_count']==1,'one family')
 need(r['service_write_calls']==0 and r['new_publication_eligible']is False,'source only')
 need(r['full_solution_doi_authenticated']is None and r['alternative_whole_proof_adopted']is False,'limits')
 v=r['values'];need(type(v)is list and len(v)==4 and all(type(x)is str for x in v),'four typed values')
 need(v[1]==v[2]=='','B/C blank')
 need('https://multiscalar.ai/results/erdos-1038/paper.pdf' in v[3] and 'https://github.com/AlecKriebel/Math/pull/1310' in v[3],'authentic main source and PR')
 need('Runzhou Tao' in v[3] and 'Terence Tao' in v[3] and 'not independently certified' in v[3],'author and alternative limits')
 need(r['result_family_key']=='EP1038_r1_finite_monic_strict_unit_sublevel_infimum_exact_L','family key')
def sources():
 for fn in ['SOURCE_INDEX.json','ADDITIONAL_SOURCE_INDEX.json','VERSION_COMPLETION_INDEX.json']:
  for r in obj(fn):
   if 'error' in r:continue
   b=gzip.decompress((P/r['capture']).read_bytes());need(len(b)==r['bytes'] and sha(b)==r['sha256'],'source '+r['key'])
 expected={'dpt_paper':'c6baa6e345568142c00724079dcc5f4b1713ca191fad06fe82cba07842c667fa','wang_paper':'3a7e857b12e59f24af17f36a30030b0ad6368c2d59955ef58e643400917565ad','osf_v2':'aa6984d799948601a1059e03ded9210dfe21c281f991b07832ceb33aab25599b'}
 for k,h in expected.items():need(sha(raw(k))==h,'exact pinned paper '+k)
 tree=json.loads(raw('dpt_tree'));source=raw('dpt_paper');blob=hashlib.sha1(('blob '+str(len(source))+'\0').encode()+source).hexdigest()
 need(next(x for x in tree['tree'] if x['path']=='papers/erdos1038/Erdos_1038.pdf')['sha']==blob,'DPT immutable Git blob')
 native=json.loads(raw('osf_files_public'));v2=next(x for x in native['data'] if x['attributes']['guid']=='ynb6j')['attributes']
 need(v2['extra']['hashes']['sha256']==sha(raw('osf_v2')) and v2['size']==len(raw('osf_v2')),'OSF native file hash')
 need(json.loads(raw('osf_node_public'))['data']['attributes']['public']is True,'OSF currently public')
 need(json.loads(raw('osf_identifiers'))['data']==[],'OSF no authenticated identifier')
 wrong=json.loads(raw('wrong_zenodo_record'));need(wrong['id']==19549033 and 'Finite Execution' in wrong['metadata']['title'],'reject unrelated DOI')
 upper=json.loads(raw('zenodo_upper_record'));need(upper['id']==19503638 and 'upper bound' in upper['metadata']['title'],'weaker DOI identity')
 need('1.837' in upper['metadata']['description'] and '11/6' in upper['metadata']['description'],'weaker bound not exact theorem')
 found=[]
 for k in ['datacite_title_1038']+['datacite_title_1038_page'+str(i) for i in range(2,7)]:
  x=json.loads(raw(k));need(x['meta']['total']==512,'DataCite query count');found+=x['data']
 need(len(found)==len({x['id'] for x in found})==512,'complete bounded query pagination')
def ledger():
 for phase in ['initial','final']:
  r=obj(phase.upper()+'_LEDGER_CHECK.json')
  need(r['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and r['numeric_gid']==1254632077,'ledger identity')
  need(r['column_count']==43 and r['row_counts']=={'UNFORMATTED_VALUE':191,'FORMULA':191},'ledger extent')
  need(r['metadata_stable'] and r['typed_views_equal'] and r['service_write_calls']==0,'ledger consistency')
  for receipt in r['captures']:
   b=gzip.decompress((P/'private'/('ledger_'+phase)/(receipt['name']+'.json.gz')).read_bytes())
   need(len(b)==receipt['raw_bytes'] and sha(b)==receipt['raw_sha256'],'ledger raw capture')
  need(not any(x['exact_alias_hits'] for x in r['leads']),'no exact existing ledger row')
 f=obj('FINAL_DEDUP_SUMMARY.json');need(f['semantic_equivalent_rows']==[] and f['result_family_count']==1 and f['source_only_proposal'],'semantic conclusion')
def main():
 frozen();sources();ledger();row=obj('ROW_PROPOSAL.json');rowcheck(row)
 identity=[]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,*flags,str(P/'check_identity.py')],capture_output=True)
  need(r.returncode==0,'independent exact identities '+str(flags));identity.append(r.stdout)
 need(identity[0]==identity[1]==identity[2],'optimized identity agreement')
 need(identity[0]==(P/'identity_result.json').read_bytes()==(P/'identity_result_O.json').read_bytes()==(P/'identity_result_OO.json').read_bytes(),'sealed exact result')
 controls=[]
 for label,mut in [('DOI in C',lambda x:x['values'].__setitem__(2,'https://doi.org/10.5281/zenodo.19503638')),('duplicate families',lambda x:x.update(result_family_count=2)),('unreviewed proof adopted',lambda x:x.update(alternative_whole_proof_adopted=True)),('new publication',lambda x:x.update(new_publication_eligible=True)),('missing main source',lambda x:x['values'].__setitem__(3,'PR1310 only')),('external write claim',lambda x:x.update(service_write_calls=1))]:
  z=copy.deepcopy(row);mut(z)
  try:rowcheck(z)
  except Failure:controls.append(label)
  else:raise Failure('bad row accepted '+label)
 print(json.dumps({'status':'PASS','scope':'bounded priority/source identity and one-source-only-family recommendation; no publication readiness','exact_identities':len(json.loads(identity[0])['exact_identities']),'incorrect_row_variants_rejected':controls,'source_author_code_executed':False,'service_write_calls':0},sort_keys=True,indent=2))
if __name__=='__main__':main()
