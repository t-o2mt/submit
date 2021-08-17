import unittest
import sys
sys.path.append('../')
from test_code import test_submit_code3 as tc

class Test3(unittest.TestCase):
  def setUp(self):
    print("setup...")

  def tearDown(self):
    print("teardown!")

  # 過負荷状態のサーバが存在するケース
  def test_exist(self):
    N, m, t = 2, 2, 14
    case_path = "../test_case/case3/exist.txt"
    ans_path = "../test_case/ans3/exist.txt"
    self.assertEqual(True, tc.test_submit_code3(N, m, t, case_path, ans_path))
  
  # 過負荷状態のサーバが存在しないケース
  def test_not_exist(self):
    N, m, t = 2, 2, 14
    case_path = "../test_case/case3/not_exist.txt"
    ans_path = "../test_case/ans3/not_exist.txt"
    self.assertEqual(True, tc.test_submit_code3(N, m, t, case_path, ans_path))


if __name__ == "__main__":
  unittest.main()