"""Prepare PR190-specific gated disposition scripts; does not run them."""
from pathlib import Path
A=Path(__file__).resolve().parent;OLD=A.parent/'pr184_10300044'
if any((A/n).exists() for n in ['prepare_final_scoped_merge.py', 'prepare_factual_completion.py']):raise RuntimeError('Historical generator retired: canonical outputs already exist; preserve independently repaired current scripts.')
def unique(s,a,b):
 if s.count(a)!=1:raise ValueError('Nonunique adaptation '+a[:70])
 return s.replace(a,b)
s=(OLD/'prepare_final_scoped_merge.py').read_text().replace('PR184','PR190').replace('pr184_10300044','pr190_5000007').replace('pulls/184','pulls/190').replace('10300044','5000007').replace('fbd6561971368a0867df83453454427863d7f910','0c3346c8ebcb3b967a1d8bf9a283f027b44b738c')
s=s.replace("cells[9]=' 2/5 '","cells[9]=' unknown/5 (interrupted) '")
start=s.index("cells[11]=' Verified negative answer")
end=s.index(";cells[12]",start)
s=s[:start]+"cells[11]=' Verified two-part answer: imported bare-angle distance-two exclusion FALSE by exactly two direct proper face diagonals; explicitly adopted parity-selected endpoint exclusion PROVED without length bound. Supported source disambiguation, not authenticated author erratum or uniquely forced printed intent. Classical AAH/Troubetzkoy midpoint mechanism and Ferudun contemporaneous exact overlap credited; current DOI-version files authenticated, historical firstness/awareness/independence uncertified; older body/version gaps disclosed. Exact optimization-safe reproduction separates valid16faceword from terminal-type and displayed-coordinate errors. Successive fresh whole-package reviews clean. Extensive AI; unrefereed. '"+s[end:]
s=s.replace("j['fully_completed_count']==37 and j['published_count']==21 and j['last_completed_PR']==179 and 184 not in", "j['fully_completed_count']==38 and j['published_count']==22 and j['last_completed_PR']==184 and 190 not in")
s=s.replace("j['current_PR']==184","j['current_PR']==190")
s=s.replace('intake185','intake191').replace('next_numeric_intake_cursor=185','next_numeric_intake_cursor=191')
s=s.replace('Fixed hyperbolic-M/Na/commontransversal mathematics cleared','Qualified bare-angle counterexamples and adopted parity-selected theorem cleared').replace('no firstness/minimality claim','no firstness/author-intent/independence claim').replace('37completed/21published','38completed/22published')
s=unique(s,"'Merge PR190: unbounded taut Godbillon-Vey numbers on fixed hyperbolic manifold\\n\\nCredited classical consequence answering literal Calegari2002v1 Q10.6. Historicalpriority unresolved, bounded body/version access gaps disclosed; nofirstness or minimality claim. Exactreviewed preprint '","'Merge PR190: two formulations of the dodecahedral endpoint question\\n\\nBare-angle exclusion false by two face diagonals; adopted parity-selected unbounded endpoint theorem proved. Classical inputs and exact contemporary overlap credited; current DOI files authenticated, historicalfirstness/sourceintent/independence not certified. Exactreviewed preprint '")
s=s.replace("NATIVE+'CANDIDATE.md',NATIVE+'verify.py',NATIVE+'review/independent_checks.py'","NATIVE+'PROOF_V2.md',NATIVE+'check_certificate.py',NATIVE+'independent_review/reviewer_exact_check.py'")
s=s.replace("'/taut_godbillon_vey.tex'","'/dodecahedron_endpoint.tex'")
# Fields stating the case number as a numeric value need explicit adaptation.
s=s.replace("'PR':184","'PR':190")
(A/'prepare_final_scoped_merge.py').write_text(s)
s=(OLD/'prepare_factual_completion.py').read_text().replace('PR184','PR190').replace('merge184','merge190').replace('pr184_10300044','pr190_5000007').replace('pulls/184','pulls/190').replace('10300044','5000007')
s=s.replace("j['fully_completed_count']==37 and j['published_count']==21 and j['last_completed_PR']==179 and 184 not in", "j['fully_completed_count']==38 and j['published_count']==22 and j['last_completed_PR']==184 and 190 not in")
s=s.replace("'PR':184","'PR':190").replace("'original_budget':'2/5'","'original_budget':'unknown/5 (interrupted)'")
s=s.replace("'result':'One fixed closed hyperbolic M, smooth cooriented taut F_N, ordinary GV=Na with a>0 and the same all-leaf embedded positive circle; negative answer to literal Calegari math/0209081v1 Q10.6. Classical ingredients credited; no minimality/firstness/guaranteed novelty claim.'","'result':'Imported bare-angle exclusion false by exactly two proper face diagonals per initial face/vertex; adopted parity-selected endpoint theorem proved without length bound. Classical midpoint mechanisms and exact Ferudun current overlap credited, current DOI-version identity authenticated; no author-authenticated erratum, unique intended reading, firstness or independence certification.'")
s=s.replace('fully_completed_count_postimage\':38','fully_completed_count_postimage\':39').replace('published_count_postimage\':22','published_count_postimage\':23')
s=s.replace("next_original_status_intake':185","next_original_status_intake':191").replace('intake185','intake191').replace('postimage38completed/22published','postimage39completed/23published')
s=s.replace('completed=38,published=22,fully_completed_count=38,published_count=22','completed=39,published=23,fully_completed_count=39,published_count=23').replace("{'completed':37,'published':21}","{'completed':38,'published':22}")
s=s.replace('bibliographic repair globally propagated','current DOI-file identity repair globally propagated').replace('no firstness/minimality claim','no firstness/author-intent/independence claim')
s=s.replace("append(184)","append(190)").replace("require(184 not in","require(190 not in")
s=s.replace("j['fully_completed_count']==38 and len(set(j['fully_completed_eligible_PRs']))==38","j['fully_completed_count']==39 and len(set(j['fully_completed_eligible_PRs']))==39").replace("j['published_count']==22,'Published count'","j['published_count']==23,'Published count'")
s=s.replace('last_completed_PR=184','last_completed_PR=190').replace("last_completed_original_budget='2/5'","last_completed_original_budget='unknown/5 (interrupted)'").replace("published_qualified_credited_classical_taut_GV_unboundedness_note","published_qualified_two_formulations_dodecahedral_endpoint_note").replace('last_published_PR=184','last_published_PR=190').replace('current_PR=184','current_PR=190').replace("current_original_budget='2/5'","current_original_budget='unknown/5 (interrupted)'")
s=s.replace('next_numeric_intake_cursor=185','next_numeric_intake_cursor=191').replace('100*38/99','100*39/99').replace('38/dated99','39/dated99').replace('22published','23published').replace("fully_completed_count':38","fully_completed_count':39").replace("published_count':22","published_count':23").replace('fixed-hyperbolic-M/Na/commontransversal theorem','two-part dodecahedral endpoint result')
# Active aliases are updated together; no historical case ledger is rewritten.
s=unique(s,"save(out/'CURRENT_PROGRESS.json',j)","j.update(current_source_author_authenticated_erratum=False,current_source_unique_intent_certified=False,current_current_primary_overlap_verified=True,current_DOI_file_identity_verified=True)\n save(out/'CURRENT_PROGRESS.json',j)")
(A/'prepare_factual_completion.py').write_text(s)
print('Prepared gated PR190 final merge and factual completion scripts; no external actions.')
