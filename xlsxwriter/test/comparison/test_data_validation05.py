###############################################################################
#
# Tests for XlsxWriter.
#
# Copyright (c), 2013-2014, John McNamara, jmcnamara@cpan.org
#

import unittest
import os
from ...workbook import Workbook
from ..helperfunctions import _compare_xlsx_files


class TestCompareXLSXFiles(unittest.TestCase):
    """
    Test file created by XlsxWriter against a file created by Excel.

    """

    def setUp(self):
        self.maxDiff = None

        filename = 'data_validation02.xlsx'

        test_dir = 'xlsxwriter/test/comparison/'
        self.got_filename = test_dir + '_test_5' + filename
        self.exp_filename = test_dir + 'xlsx_files/' + filename

        self.ignore_files = []
        self.ignore_elements = {}

    def test_create_file(self):
        """Test the creation of an  XlsxWriter file data validation."""
        filename = self.got_filename

        ####################################################

        workbook = Workbook(filename)

        worksheet = workbook.add_worksheet()

        worksheet.data_validation(
            'C2', {'validate': 'list',
                   'value': ['Foo', 'Bar', 'Baz'],
                   'input_title': 'This is the input title',
                   'input_message': 'This is the input message',
                   }
        )

        # The following should be rejected because the input message is too long.
        input_title = 'This is the longest input title1'
        input_message = 'This is the longest input message ' + ('a' * 222)
        values = [
            "Foobar", "Foobas", "Foobat", "Foobau", "Foobav", "Foobaw",
            "Foobax", "Foobay", "Foobaz", "Foobba", "Foobbb", "Foobbc",
            "Foobbd", "Foobbe", "Foobbf", "Foobbg", "Foobbh", "Foobbi",
            "Foobbj", "Foobbk", "Foobbl", "Foobbm", "Foobbn", "Foobbo",
            "Foobbp", "Foobbq", "Foobbr", "Foobbs", "Foobbt", "Foobbu",
            "Foobbv", "Foobbw", "Foobbx", "Foobby", "Foobbz", "Foobca",
            "End"
        ]

        # Ignore the warnings raised by data_validation().
        import warnings
        warnings.filterwarnings('ignore')

        worksheet.data_validation(
            'D6', {'validate': 'list',
                   'value': values,
                   'input_title': input_title,
                   'input_message': input_message,
                   }
        )

        workbook.close()

        ####################################################

        got, exp = _compare_xlsx_files(self.got_filename,
                                       self.exp_filename,
                                       self.ignore_files,
                                       self.ignore_elements)

        self.assertEqual(got, exp)

    def tearDown(self):
        # Cleanup.
        if os.path.exists(self.got_filename):
            os.remove(self.got_filename)


if __name__ == '__main__':
    unittest.main()
