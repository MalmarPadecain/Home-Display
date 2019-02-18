from unittest import mock

import pytest
from pytest import fixture

from core.data.phone_call import PhoneCall, CallPaginator, Type


class TestType:
    @pytest.mark.parametrize("test_input,expected", [
        ("call_out", Type.OUTGOING),
        ("call_in", Type.INCOMING),
        ("call_in_fail", Type.MISSED),
        ("call_rejected", Type.REJECTED)
    ])
    def test_from_str(self, test_input, expected):
        assert Type.from_str(test_input) == expected


class TestCallPaginator:
    values = [
        PhoneCall.create("call_out", "13.02.19 00:19", "0"),
        PhoneCall.create("call_out", "13.02.19 00:19", "1"),
        PhoneCall.create("call_out", "13.02.19 00:19", "2"),
        PhoneCall.create("call_out", "13.02.19 00:19", "3"),
        PhoneCall.create("call_out", "13.02.19 00:19", "4"),

        PhoneCall.create("call_out", "13.02.19 00:19", "5"),
        PhoneCall.create("call_out", "13.02.19 00:19", "6"),
        PhoneCall.create("call_out", "13.02.19 00:19", "7"),
        PhoneCall.create("call_out", "13.02.19 00:19", "8"),
        PhoneCall.create("call_out", "13.02.19 00:19", "9"),

        PhoneCall.create("call_out", "13.02.19 00:19", "10"),
        PhoneCall.create("call_out", "13.02.19 00:19", "11"),
        PhoneCall.create("call_out", "13.02.19 00:19", "12"),
        PhoneCall.create("call_out", "13.02.19 00:19", "13")
    ]

    @fixture
    def fresh_paginator(self):
        paginator = CallPaginator()
        m = mock.Mock(side_effect=lambda n, s: self.values[paginator.offset: paginator.offset + n])
        paginator._query = m
        return paginator

    @fixture
    def end_paginator(self):
        paginator = CallPaginator()
        m = mock.Mock(side_effect=lambda n, s: self.values[paginator.offset: paginator.offset + n])
        paginator._query = m
        paginator.get_next_n_calls(5)
        paginator.get_next_n_calls(5)
        paginator.get_next_n_calls(5)
        return paginator

    def test_get_next_n_calls_fresh(self, fresh_paginator):
        assert fresh_paginator.get_next_n_calls(5) == self.values[0:5]

    def test_get_next_n_calls_fresh_backwards(self, fresh_paginator):
        assert fresh_paginator.get_next_n_calls(-5) == self.values[0:5]

    def test_get_next_n_calls_fresh_last_slice(self, fresh_paginator):
        fresh_paginator.get_next_n_calls(5)
        fresh_paginator.get_next_n_calls(5)
        assert fresh_paginator.get_next_n_calls(5) == self.values[10:14]
        print(fresh_paginator.offset)

    def test_get_next_n_calls_past_end(self, end_paginator):
        assert end_paginator.get_next_n_calls(5) == []

    def test_get_next_n_calls_end_backwards(self, end_paginator):
        assert end_paginator.get_next_n_calls(-5) == self.values[4:9]

    def test_get_next_n_calls_past_end_backwards(self, end_paginator):
        end_paginator.get_next_n_calls(5)
        assert end_paginator.get_next_n_calls(-5) == self.values[9:14]

    def test_get_next_n_calls_two_past_backwards(self, end_paginator):
        end_paginator.get_next_n_calls(5)
        end_paginator.get_next_n_calls(5)
        assert end_paginator.get_next_n_calls(-5) == self.values[9:14]
