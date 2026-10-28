import unittest
from analysis_agent import analyze_opportunity
class TestAnalysis(unittest.TestCase):
 def test_scam_flags(self):
  x=analyze_opportunity({'title':'Guaranteed profit send crypto','description':'investment required','url':'https://example.com','source':'test','reward_text':''})
  self.assertEqual(x['risk'],'high');self.assertFalse(x['recommended'])
 def test_score_range(self):
  x=analyze_opportunity({'title':'paid remote Python task bounty $500','description':'A detailed task','url':'https://example.com','source':'test','reward_text':''})
  self.assertGreaterEqual(x['score'],0);self.assertLessEqual(x['score'],100)
if __name__=='__main__':unittest.main()
