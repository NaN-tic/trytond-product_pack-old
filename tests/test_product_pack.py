#!/usr/bin/env python
# This file is part of the product_pack module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.tests.test_tryton import test_view, test_depends
import trytond.tests.test_tryton
import unittest


class ProductPackTestCase(unittest.TestCase):
    '''
    Test Product Pack module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('product_pack')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('product_pack')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPackTestCase))
    return suite
