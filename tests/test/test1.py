import unittest
import sys
sys.path.append('../')
from test_code import test_submit_code1 as tc

class Test1(unittest.TestCase):
  def setUp(self):
    print("setup...")

  def tearDown(self):
    print("teardown!")

  # 故障状態のサーバが存在するケース
  def test_exist(self):
    case_path = "../test_case/case1/exist.txt"
    ans_path = "../test_case/ans1/exist.txt"
    self.assertEqual(True, tc.test_submit_code1(case_path, ans_path))
  
  # 故障状態のサーバが存在しないケース
  def test_not_exist(self):
    case_path = "../test_case/case1/not_exist.txt"
    ans_path = "../test_case/ans1/not_exist.txt"
    self.assertEqual(True, tc.test_submit_code1(case_path, ans_path))
  
  # 何度も連続でタイムアウトした故障状態のサーバが存在するケース
  def test_continue_timeout(self):
    case_path = "../test_case/case1/continue_timeout.txt"
    ans_path = "../test_case/ans1/continue_timeout.txt"
    self.assertEqual(True, tc.test_submit_code1(case_path, ans_path))
  
  # 同じサーバが故障と復活を繰り返すケース
  def test_status_repetition(self):
    case_path = "../test_case/case1/status_repetition.txt"
    ans_path = "../test_case/ans1/status_repetition.txt"
    self.assertEqual(True, tc.test_submit_code1(case_path, ans_path))


if __name__ == "__main__":
  unittest.main()