#!/usr/bin/env python3
"""Allowlist publication-safe evidence from private read-only sheet responses."""
import hashlib,re,json
PUBLICATION_PRS=(618,623,662,681)
PRIVATE_KEYS=('tracker_all_A_D','tracker_metadata',*(f'pr{n}_tracker_exact' for n in PUBLICATION_PRS))
HEADER=['Original Problem','Solution Chat URL','DOI','Notes']
def normalize_doi(value):
 return re.sub(r'^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)','',value.strip(),count=1,flags=re.I).removesuffix('/').lower()
def pad(row):return (row+['']*4)[:4]
def digest(value):return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def scoped_evidence(key,raw,raw_bytes,entries):
 if key not in PRIVATE_KEYS:raise ValueError('Not a private spreadsheet readback')
 result={'schema':'completed-eight-scoped-sheet-evidence-v1','checked_utc':raw.get('checked_utc'),'command':raw.get('command'),'returncode':raw.get('returncode'),
 'raw_readback':{'private_path':f'tmp/{key}.json','bytes':len(raw_bytes),'sha256':hashlib.sha256(raw_bytes).hexdigest(),'excluded_from_publication':True},
 'only_own_row_contents_retained':True}
 if raw.get('returncode')!=0 or 'response' not in raw:
  result['status']='RAW_READBACK_FAILED_DETAILS_PRIVATE';return result
 response=raw['response']
 if key=='tracker_metadata':
  selected=[x for x in response.get('sheets',[]) if x.get('properties',{}).get('sheetId')==1254632077]
  matches=len(selected)==1 and selected[0]['properties'].get('title')=='Math Puzzles'
  result['response']={'spreadsheetId':response.get('spreadsheetId'),'selected_gid_match_count':len(selected),'selected_title_matches_expected':matches,'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}] if matches else []}
 elif key.endswith('_tracker_exact'):
  number=int(re.fullmatch(r'pr(\d+)_tracker_exact',key).group(1))
  entry=next(x for x in entries if x['pr']==number and 'doi' in x)
  values=response.get('values',[]);matches=len(values)==1 and pad(values[0])==entry['tracker_row'] and response.get('range')==entry['tracker_range']
  result['response']={'range':entry['tracker_range'],'matches_saved_exact_row_and_range':matches,'observed_values_sha256':digest(values),'values':[entry['tracker_row']] if matches else []}
 else:
  rows=response.get('values',[]);own=[];doi_checks=[]
  for entry in entries:
   if 'doi' not in entry:continue
   target=int(re.search(r'!A(\d+):D',entry['tracker_range']).group(1))
   actual=pad(rows[target-1]) if target<=len(rows) else None;exact=actual==entry['tracker_row']
   selected={'pr':entry['pr'],'row_number':target,'range':entry['tracker_range'],'matches_saved_exact_row':exact}
   if exact:selected['values']=entry['tracker_row']
   own.append(selected)
   hits=[i+1 for i,row in enumerate(rows) if len(row)>2 and normalize_doi(row[2])==entry['doi'].lower()]
   exact_hits=[i+1 for i,row in enumerate(rows) if pad(row)==entry['tracker_row']]
   doi_checks.append({'pr':entry['pr'],'doi':entry['doi'],'normalized_column_C_match_rows':hits,'normalized_column_C_match_count':len(hits),'exact_A_D_match_rows':exact_hits,'exact_A_D_match_count':len(exact_hits)})
  header=rows[0] if rows else []
  result['response']={'range':"'Math Puzzles'!A:D",'majorDimension':response.get('majorDimension'),'header':HEADER if header==HEADER else [],'header_matches_expected':header==HEADER,'observed_header_sha256':digest(header),'total_returned_rows':len(rows),'selected_own_rows':own,'global_DOI_uniqueness_checks':doi_checks}
 result['status']='SCOPED_EVIDENCE_ONLY';return result
