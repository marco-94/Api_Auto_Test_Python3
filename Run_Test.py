
import unittest
from BeautifulReport import BeautifulReport
import time

if __name__ == '__main__':
    suite_tests = unittest.defaultTestLoader.discover("./test_case",
                                                      pattern="test_case_*.py",
                                                      top_level_dir=None)

    BeautifulReport(suite_tests).report(filename='新增房源-' + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()),
                                        description='新增房源',
                                        report_dir='./test_report')
