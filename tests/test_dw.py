import sys, tempfile, sqlite3, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.load_dw import load
class TestDW(unittest.TestCase):
    def test_load_has_star_schema(self):
        with tempfile.TemporaryDirectory() as d:
            db=Path(d)/"dw.db"; n=load(db)
            with sqlite3.connect(db) as conn:
                tables={r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                self.assertIn("fact_sales",tables); self.assertGreater(n,100)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0],n)
if __name__=="__main__": unittest.main()
