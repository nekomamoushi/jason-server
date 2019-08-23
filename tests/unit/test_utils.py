
from jason_server.utils import chunk_list, str_to_int


def test_chunk_list():

    d = [{'a': 1}, {'b': 2}, {'c': 3}, {'d': 4}, {'e': 5}, {'f': 6}, {'g': 7}]
    chunk_d = chunk_list(d)
    chunk_l = list(chunk_d)
    assert len(d) == len(chunk_l)

    chunk_d = chunk_list(d, chunk_size=2)
    chunk_l = list(chunk_d)
    assert 4 == len(chunk_l)

    chunk_d = chunk_list(d, chunk_size=3)
    chunk_l = list(chunk_d)
    assert 3 == len(chunk_l)
    assert 1 == len(chunk_l[2])


def test_str_to_int():
    string_no_digit = "jesuisunefougere"
    string_all_digit = "1234"
    string_some_digit = "ehy45"

    assert string_no_digit == str_to_int(string_no_digit)
    assert 1234 == str_to_int(string_all_digit)
    assert string_some_digit == str_to_int(string_some_digit)
