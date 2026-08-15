import unittest
from github_profile_dashboard import dashboard,probe
class T(unittest.TestCase):
 def test_metrics(self):self.assertEqual(dashboard({"repositories":[{"name":"x","visibility":"public","stars":2}]})["stars"],2)
 def test_private(self):self.assertFalse(dashboard({"repositories":[{"name":"x","visibility":"private"}]})["ok"])
 def test_negative(self):self.assertFalse(dashboard({"repositories":[{"name":"x","visibility":"public","stars":-1}]})["ok"])
 def test_probe(self):self.assertTrue(probe()["ok"])
if __name__=="__main__":unittest.main()
