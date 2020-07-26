# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import itertools
from datetime import datetime
import sys

from anonymizer.utils.dateutil.parser import parse

import pytest

# Platform info
IS_WIN = sys.platform.startswith("win")

try:
    datetime.now().strftime("%-d")
    PLATFORM_HAS_DASH_D = True
except ValueError:
    PLATFORM_HAS_DASH_D = False


@pytest.fixture(params=[True, False])
def fuzzy(request):
    """Fixture to pass fuzzy=True or fuzzy=False to parse"""
    return request.param


# Parser test cases using no keyword arguments.
# Format: (parsable_text, expected_datetime, assertion_message)
PARSER_TEST_CASES = [
    ("Thu Sep 25 10:36:28 2003", datetime(2003, 9, 25, 10, 36, 28), "date command format strip"),
    ("Thu Sep 25 2003", datetime(2003, 9, 25), "date command format strip"),
    ("2003-09-25T10:49:41", datetime(2003, 9, 25, 10, 49, 41), "iso format strip"),
    ("2003-09-25T10:49", datetime(2003, 9, 25, 10, 49), "iso format strip"),
    ("2003-09-25T10", datetime(2003, 9, 25, 10), "iso format strip"),
    ("2003-09-25", datetime(2003, 9, 25), "iso format strip"),
    ("20030925T104941", datetime(2003, 9, 25, 10, 49, 41), "iso stripped format strip"),
    ("20030925T1049", datetime(2003, 9, 25, 10, 49, 0), "iso stripped format strip"),
    ("20030925T10", datetime(2003, 9, 25, 10), "iso stripped format strip"),
    ("20030925", datetime(2003, 9, 25), "iso stripped format strip"),
    ("2003-09-25 10:49:41.502000", datetime(2003, 9, 25, 10, 49, 41, 502000), "python logger format"),
    ("199709020908", datetime(1997, 9, 2, 9, 8), "no separator"),
    ("19970902090807", datetime(1997, 9, 2, 9, 8, 7), "no separator"),
    ("09-25-2003", datetime(2003, 9, 25), "date with dash"),
    ("25-09-2003", datetime(2003, 9, 25), "date with dash"),
    ("10-09-2003", datetime(2003, 10, 9), "date with dash"),
    ("10-09-03", datetime(2003, 10, 9), "date with dash"),
    ("2003.09.25", datetime(2003, 9, 25), "date with dot"),
    ("09.25.2003", datetime(2003, 9, 25), "date with dot"),
    ("25.09.2003", datetime(2003, 9, 25), "date with dot"),
    ("10.09.2003", datetime(2003, 10, 9), "date with dot"),
    ("10.09.03", datetime(2003, 10, 9), "date with dot"),
    ("2003/09/25", datetime(2003, 9, 25), "date with slash"),
    ("09/25/2003", datetime(2003, 9, 25), "date with slash"),
    ("25/09/2003", datetime(2003, 9, 25), "date with slash"),
    ("10/09/2003", datetime(2003, 10, 9), "date with slash"),
    ("10/09/03", datetime(2003, 10, 9), "date with slash"),
    ("2003 09 25", datetime(2003, 9, 25), "date with space"),
    ("09 25 2003", datetime(2003, 9, 25), "date with space"),
    ("25 09 2003", datetime(2003, 9, 25), "date with space"),
    ("10 09 2003", datetime(2003, 10, 9), "date with space"),
    ("10 09 03", datetime(2003, 10, 9), "date with space"),
    ("25 09 03", datetime(2003, 9, 25), "date with space"),
    ("03 25 Sep", datetime(2003, 9, 25), "strangely ordered date"),
    ("25 03 Sep", datetime(2025, 9, 3), "strangely ordered date"),
    ("  July   04 ,  1976   12:01:02   AM  ", datetime(1976, 7, 4, 0, 1, 2), "extra space"),
    ("Wed, July 10, '96", datetime(1996, 7, 10, 0, 0), "random format"),
    ("1996.July.10 AD 12:08 PM", datetime(1996, 7, 10, 12, 8), "random format"),
    ("July 04, 1976", datetime(1976, 7, 4), "random format"),
    ("07 04 1976", datetime(1976, 7, 4), "random format"),
    ("04 Jul 1976", datetime(1976, 7, 4), "'%-d %b %Y' format"),
    ("07-04-76", datetime(1976, 7, 4), "random format"),
    ("19760704", datetime(1976, 7, 4), "random format"),
]
# Check that we don't have any duplicates
assert len(set([x[0] for x in PARSER_TEST_CASES])) == len(PARSER_TEST_CASES)


@pytest.mark.parametrize("parsable_text,expected_datetime,assertion_message", PARSER_TEST_CASES)
def test_parser(parsable_text, expected_datetime, assertion_message):
    resulting_datetime, resulting_format = parse(parsable_text, return_format=True)
    assert resulting_datetime == expected_datetime, assertion_message
    assert resulting_datetime.strftime(resulting_format) == parsable_text, assertion_message + " format"


class TestFormat(object):
    def test_ybd(self):
        # If we have a 4-digit year, a non-numeric month (abbreviated or not),
        # and a day (1 or 2 digits), then there is no ambiguity as to which
        # token is a year/month/day.  This holds regardless of what order the
        # terms are in and for each of the separators below.

        seps = ["-", " ", "/", "."]

        year_tokens = ["%Y"]
        month_tokens = ["%b", "%B"]
        day_tokens = ["%d"]
        if PLATFORM_HAS_DASH_D:
            day_tokens.append("%d")

        prods = itertools.product(year_tokens, month_tokens, day_tokens)
        perms = [y for x in prods for y in itertools.permutations(x)]
        unambig_fmts = [sep.join(perm) for sep in seps for perm in perms]

        actual = datetime(2003, 9, 25)

        for fmt in unambig_fmts:
            dstr = actual.strftime(fmt)
            res, res_fmt = parse(dstr, return_format=True)
            assert res == actual
            assert res_fmt == fmt

    # TODO: some redundancy with PARSER_TEST_CASES cases
    @pytest.mark.parametrize(
        "fmt,dstr",
        [
            ("%a %b %d %Y", "Thu Sep 25 2003"),
            ("%b %d %Y", "Sep 25 2003"),
            ("%Y-%m-%d", "2003-09-25"),
            ("%Y%m%d", "20030925"),
            ("%Y-%b-%d", "2003-Sep-25"),
            ("%d-%b-%Y", "25-Sep-2003"),
            ("%b-%d-%Y", "Sep-25-2003"),
            ("%m-%d-%Y", "09-25-2003"),
            ("%d-%m-%Y", "25-09-2003"),
            ("%Y.%m.%d", "2003.09.25"),
            ("%Y.%b.%d", "2003.Sep.25"),
            ("%d.%b.%Y", "25.Sep.2003"),
            ("%b.%d.%Y", "Sep.25.2003"),
            ("%m.%d.%Y", "09.25.2003"),
            ("%d.%m.%Y", "25.09.2003"),
            ("%Y/%m/%d", "2003/09/25"),
            ("%Y/%b/%d", "2003/Sep/25"),
            ("%d/%b/%Y", "25/Sep/2003"),
            ("%b/%d/%Y", "Sep/25/2003"),
            ("%m/%d/%Y", "09/25/2003"),
            ("%d/%m/%Y", "25/09/2003"),
            ("%Y %m %d", "2003 09 25"),
            ("%Y %b %d", "2003 Sep 25"),
            ("%d %b %Y", "25 Sep 2003"),
            ("%m %d %Y", "09 25 2003"),
            ("%d %m %Y", "25 09 2003"),
            ("%y %d %b", "03 25 Sep",),
        ],
    )
    def test_strftime_formats_2003Sep25(self, fmt, dstr):
        expected = datetime(2003, 9, 25)

        # First check that the format strings behave as expected
        #  (not strictly necessary, but nice to have)
        assert expected.strftime(fmt) == dstr

        res, res_fmt = parse(dstr, return_format=True)
        assert res == expected
        assert res_fmt == fmt
