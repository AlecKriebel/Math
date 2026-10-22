#!/usr/bin/env python3
import os,sys
sys.dont_write_bytecode=True
from pathlib import Path
R=Path(__file__).resolve().parent;A=R.parents[1]
os.environ['TMPDIR']=str(R/'ignored_scratch/tmp');os.environ['PYTHONDONTWRITEBYTECODE']='1'
import copy,datetime,hashlib,json,re
from html.parser import HTMLParser

def need(v,m):
 if not v:raise RuntimeError(m)
def load(p):return json.loads((A/p).read_text())
def strip(v):
 if isinstance(v,dict):return {k:strip(x)for k,x in v.items()if k!='title'}
 if isinstance(v,list):return [strip(x)for x in v]
 return v
raw=load('priority/graph_literature/QUERY_LEDGER.json');pub=load('priority/graph_literature_public/QUERY_LEDGER.json')
need((A/'priority/graph_literature_public/INITIAL_SEAL_RECEIPT.json').read_bytes()==(A/'priority/graph_literature/MANIFEST.json').read_bytes(),'initial B seal receipt');rawrows=raw['queries'];pubrows=pub['queries'];need(strip(rawrows)==pubrows,'projection preserved nontitle fields')
titles=sum('title'in e for q in rawrows for e in q['returned_entries']);urls=sum(len(q['returned_entries'])for q in pubrows);need(titles==893 and urls==893,'projection counts')
queries=[q['literal_query']for q in load('priority/primary_lineage/QUERY_LEDGER.json')['queries']]+[q['literal_query']for q in pubrows]+[q['query']for q in load('priority/root_extension/QUERY_LEDGER.json')['entries']];need(len(queries)==111 and len(set(queries))==107,'query count')
html=(A/'priority/graph_literature/ignored_local/capuano2026.html').read_text();rawhits=len(re.findall('clique',html,re.I));singular=len(re.findall(r'\bclique\b',html,re.I))
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
p=Text();p.feed(html);visible=' '.join(p.parts);visiblehits=len(re.findall('clique',visible,re.I));need((rawhits,visiblehits,singular)==(4,1,0),'clique count semantics')
context=load('CURRENT_PR1268_CONTEXT.json');regs=context['authored_freezes'];need(len(regs)==13,'registry13')
# Explicit current normalized manifest: only declared family-relative paths, detached seal historical.
reg=next(r for r in regs if r['base']=='reviews/note_author');need(reg['path'].endswith('NORMALIZED_MANIFEST.json'),'normalized note authority');norm=load(reg['path']);note=[]
for e in norm['authored_files']:
 b=(A/'reviews/note_author'/e['path']).read_bytes();need(len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256'],'note binding');need(not e['path'].startswith('publication/'),'external manuscript member');note.append(e['path'])
# Original editorial output slices, all protected/unchanged boundaries and exact replacements;
# unavailable removed bodies are deliberately never synthesized from hashes.
ed=load('submitted/EDITORIAL_MAP.json');edrows=[]
for art in ed['artifacts']:
 b=(A/'submitted'/art['artifact']).read_bytes();ranges=[]
 for e in art['operations']:
  piece=b[e['output_start']:e['output_end']];need(piece==e['replacement_utf8'].encode()and hashlib.sha256(piece).hexdigest()==e['replacement_sha256'],'replacement bytes');ranges.append((e['output_start'],e['output_end']))
 for e in art['unchanged_ranges']:
  piece=b[e['output_start']:e['output_end']];need(hashlib.sha256(piece).hexdigest()==e['sha256'],'unchanged output slice');ranges.append((e['output_start'],e['output_end']))
 for e in art['protected_mathematical_regions']:
  piece=b[e['output_start']:e['output_end']];need(len(piece)==e['bytes']and hashlib.sha256(piece).hexdigest()==e['sha256'],'protected output slice')
 pos=0
 for start,end in sorted(ranges):need(start==pos,'output partition');pos=end
 need(pos==len(b),'complete output partition');edrows.append(art['artifact'])
report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'projection':{'queries':59,'returned_URLs':urls,'removed_title_fields':titles,'all_other_query_fields_equal_local_original':True,'original_ledger_not_portably_authenticated':True,'initial_seal_receipt_equals_local_original_manifest':True},'search_counts':{'entries':len(queries),'exact_distinct_strings':len(set(queries)),'no_priority_inference':True},'capuano_scope':{'raw_substrings':rawhits,'visible_substrings':visiblehits,'whole_word_singular':singular,'no_full_article_absence_claim':True},'registry':regs,'note_normalized_members_authenticated':note,'editorial_output_slices_verified':edrows,'unavailable_historical_edited_bodies_not_replay_certified':3,'limits':'Source receipts authenticate local exact bytes. Only paper-cited pages personally reread for mathematical citation checks; report/ledger scope records reviewed, not independently repeated full-source readings or provider executions. Every PASS/RESOLVED was treated as hypothesis.'}
(R/'PROVENANCE_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in{'registry','note_normalized_members_authenticated','editorial_output_slices_verified'}},indent=2))
