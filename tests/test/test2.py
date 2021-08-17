import unittest
import sys
sys.path.append('../')
from test_code import test_submit_code2 as tc

class Test2(unittest.TestCase):
  def setUp(self):
    print("setup...")

  def tearDown(self):
    print("teardown!")

  # 故障状態のサーバが存在するケース
  def test_exist(self):
    N = 2
    case_path = "../test_case/case2/exist.txt"
    ans_path = "../test_case/ans2/exist.txt"
    self.assertEqual(True, tc.test_submit_code2(N, case_path, ans_path))
  
  # タイムアウトは発生するが故障状態のサーバが存在しないケース
  def test_not_exist(self):
    N = 2
    case_path = "../test_case/case2/not_exist.txt"
    ans_path = "../test_case/ans2/not_exist.txt"
    self.assertEqual(True, tc.test_submit_code2(N, case_path, ans_path))


if __name__ == "__main__":
  unittest.main()