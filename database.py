import json, sqlite3, time
from config import DB_PATH

def connect():
 c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; return c

def init_db():
 with connect() as c:
  c.executescript('''CREATE TABLE IF NOT EXISTS opportunities(id TEXT PRIMARY KEY,source TEXT,title TEXT,url TEXT,description TEXT,category TEXT,reward_text TEXT,score REAL,risk TEXT,status TEXT,discovered_at INTEGER,raw_json TEXT); CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY,path TEXT,title TEXT,kind TEXT,created_at INTEGER,status TEXT); CREATE TABLE IF NOT EXISTS portfolio(id INTEGER PRIMARY KEY,asset TEXT,quantity REAL,entry_price REAL,current_price REAL,note TEXT,created_at INTEGER); CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY,version TEXT,started_at INTEGER,ended_at INTEGER,summary_json TEXT); CREATE TABLE IF NOT EXISTS improvements(id INTEGER PRIMARY KEY,version_from TEXT,version_to TEXT,proposal TEXT,evidence_json TEXT,status TEXT,created_at INTEGER);''')
def save_opportunity(x):
 with connect() as c:c.execute('INSERT OR REPLACE INTO opportunities VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(x['id'],x['source'],x['title'],x['url'],x['description'],x['category'],x['reward_text'],x['score'],x['risk'],x['status'],x['discovered_at'],json.dumps(x.get('raw',{}),ensure_ascii=False)))
def save_product(path,title,kind):
 with connect() as c:c.execute('INSERT INTO products(path,title,kind,created_at,status) VALUES(?,?,?,?,?)',(str(path),title,kind,int(time.time()),'draft'))
def record_run(version,start,end,summary):
 with connect() as c:c.execute('INSERT INTO runs(version,started_at,ended_at,summary_json) VALUES(?,?,?,?)',(version,start,end,json.dumps(summary,ensure_ascii=False)))
def add_improvement(proposal,evidence):
 with connect() as c:c.execute('INSERT INTO improvements(version_from,version_to,proposal,evidence_json,status,created_at) VALUES(?,?,?,?,?,?)',('1.0.0','1.0.1',proposal,json.dumps(evidence),'proposed_review_required',int(time.time())))
