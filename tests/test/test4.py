import unittest
import sys
sys.path.append('../')
from test_code import test_submit_code4 as tc

class Test4(unittest.TestCase):
  def setUp(self):
    print("setup...")

  def tearDown(self):
    print("teardown!")

  # 故障状態のサブネットが存在するケース
  def test_exist(self):
    N = 2
    case_path = "../test_case/case4/exist.txt"
    ans_path = "../test_case/ans4/exist.txt"
    self.assertEqual(True, tc.test_submit_code4(N, case_path, ans_path))
  
  # 故障状態のサブネットが存在しないケース
  def test_not_exist(self):
    N = 2
    case_path = "../test_case/case4/not_exist.txt"
    ans_path = "../test_case/ans4/not_exist.txt"
    self.assertEqual(True, tc.test_submit_code4(N, case_path, ans_path))


if __name__ == "__main__":
  unittest.main()