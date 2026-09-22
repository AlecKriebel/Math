"""Prepare/read short source packets; this script does NOT author desk reviews."""
import json,sqlite3,pathlib,sys,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
HERE=ROOT/'review_v2'
def rows():
 c=sqlite3.connect(ROOT/'cache/catalog.sqlite')
 return [(k,json.loads(p),json.loads(r)) for k,p,r in c.execute('select key,payload,report from records order by cast(key as integer)')]
def prepare():
 data=rows();groups=[[] for _ in range(6)]
 # Keep nearby domain records together but balance the number of records.
 data.sort(key=lambda x:((x[1].get('category') or {}).get('display_name',''),int(x[0])))
 for n,x in enumerate(data):groups[min(5,n*6//len(data))].append(x[0])
 manifest={'source_revision':json.loads((ROOT/'manifest.json').read_text())['revision'],'shards':groups,'records':len(data)}
 (HERE/'assignments.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print([(i,len(g)) for i,g in enumerate(groups)])
def packet(shard,start,count):
 ids=json.loads((HERE/'assignments.json').read_text())['shards'][shard][start:start+count]
 data={k:(p,r) for k,p,r in rows()}
 for k in ids:
  p,r=data[k]
  gap=r.get('what_remains','')
  print(json.dumps({'id':k,'code':p['problem_number'],'title':p['title'],'statement':p['statement'],
   'difficulty':p.get('difficulty_level_id'),'year':p.get('proposed_year'),'status':p.get('status'),
   'classification':p.get('research_classification'),'statement_status':p.get('statement_status'),
   'summary':p.get('research_summary'),'literature':p.get('literature_assessment'),
   'prior_note':r.get('verification_note'),'gap_excerpt':gap[:900], 'gap_truncated':len(gap)>900,
   'source':p.get('source_url')},ensure_ascii=False))
if __name__=='__main__':
 if sys.argv[1]=='prepare':prepare()
 else:packet(*map(int,sys.argv[1:]))
