"""Search several public feeds. No feed can cover literally every global opportunity."""
import hashlib,json,time,urllib.parse,urllib.request
from config import USER_AGENT,TIMEOUT,MAX_ITEMS,GITHUB_TOKEN,ENABLE_JOBS,ENABLE_GITHUB,SEARCH_TERMS
SOURCES={'jobbi':'https://jobbi.org/gigs.json','himalayas':'https://himalayas.app/jobs/api','remoteok':'https://remoteok.com/api'}
def get_json(url,headers=None):
 h={'User-Agent':USER_AGENT,'Accept':'application/json'}; h.update(headers or {})
 req=urllib.request.Request(url,headers=h)
 with urllib.request.urlopen(req,timeout=TIMEOUT) as r:return json.loads(r.read().decode('utf-8',errors='replace'))
def norm(source,title,url,description='',category='other',reward='',raw=None):
 title=str(title or 'Opportunity without title').strip(); url=str(url or '').strip(); ident=hashlib.sha256((source+'|'+(url or title)).encode()).hexdigest()[:24]
 return {'id':ident,'source':source,'title':title,'url':url,'description':str(description or '')[:10000],'category':category,'reward_text':str(reward or ''),'score':0,'risk':'unassessed','status':'discovered','discovered_at':int(time.time()),'raw':raw or {}}
def fetch_jobbi():
 out=[]
 try:
  d=get_json(SOURCES['jobbi']); d=d.get('gigs',d.get('data',d.get('results',[]))) if isinstance(d,dict) else d
  for x in (d if isinstance(d,list) else [])[:MAX_ITEMS]:
   if isinstance(x,dict):out.append(norm('jobbi',x.get('title') or x.get('name'),x.get('url') or x.get('link'),x.get('description') or x.get('summary'),'gig',x.get('reward') or x.get('pay'),x))
 except Exception as e:print('[WARN] Jobbi:',e)
 return out
def fetch_himalayas():
 out=[]
 try:
  d=get_json(SOURCES['himalayas']); jobs=d.get('jobs',[]) if isinstance(d,dict) else d
  for x in (jobs if isinstance(jobs,list) else [])[:MAX_ITEMS]:
   if isinstance(x,dict):out.append(norm('himalayas',x.get('title'),x.get('applicationLink') or x.get('url') or x.get('jobUrl'),x.get('description') or x.get('excerpt'),'remote_job',x.get('salary') or x.get('salaryRange'),x))
 except Exception as e:print('[WARN] Himalayas:',e)
 return out
def fetch_remoteok():
 out=[]
 try:
  d=get_json(SOURCES['remoteok']);
  for x in (d if isinstance(d,list) else [])[1:MAX_ITEMS+1]:
   if isinstance(x,dict):out.append(norm('remoteok',x.get('position') or x.get('title'),x.get('url'),x.get('description'),'remote_job',x.get('salary'),x))
 except Exception as e:print('[WARN] RemoteOK:',e)
 return out
def fetch_github():
 out=[]; headers={'Authorization':'Bearer '+GITHUB_TOKEN} if GITHUB_TOKEN else {}
 for term in SEARCH_TERMS:
  q=urllib.parse.urlencode({'q':f'"{term}" (bounty OR reward OR paid OR "$" OR microtask) is:issue is:open','sort':'updated','order':'desc','per_page':'30'})
  try:
   d=get_json('https://api.github.com/search/issues?'+q,headers)
   for x in d.get('items',[]):out.append(norm('github',x.get('title'),x.get('html_url'),x.get('body'),'open_source_task','',x))
  except Exception as e:print('[WARN] GitHub search',term,':',e)
  time.sleep(.12)
 return out
def discover_opportunities():
 items=[]
 if ENABLE_JOBS:items+=fetch_jobbi()+fetch_himalayas()+fetch_remoteok()
 if ENABLE_GITHUB:items+=fetch_github()
 unique={}
 for x in items:unique.setdefault(x['url'] or x['id'],x)
 return list(unique.values())
