import os
import tempfile
from .vendor.six.moves import range

def printable_decimal_and_hex(num):
    return "{0:d} (0x{0:x})".format(num)

def assert_index_sane(index, upper_bound_exclusive):
    assert type(index) == int, "Indices should be integers; '%s' is not" % (
        index)
    assert 0 <= index < upper_bound_exclusive, (
        "Index %d out of range [%d, %d)" % (index, 0, upper_bound_exclusive))


class ObjectLookupDict(object):

    def __init__(self, id_list, object_list):
        self.id_list = id_list
        self.object_list = object_list

    def __getitem__(self, index):
        assert_index_sane(index, len(self.id_list))

        return self.object_list[self.id_list[index]]

    def __setitem__(self, index, value):
        assert_index_sane(index, len(self.id_list))

        self.id_list[index] = value.index


def name_without_zeroes(name):
    """
    Return a human-readable name without LSDJ's trailing zeroes.

    :param name: the name from which to strip zeroes
    :rtype: the name, without trailing zeroes
    """
    first_zero = name.find(b'\0')

    if first_zero == -1:
        return name
    else:
        return str(name[:first_zero])


class temporary_file:

    def __enter__(self):
        (tmp_handle, tmp_abspath) = tempfile.mkstemp()
        os.close(tmp_handle)
        self.abspath = tmp_abspath
        return self.abspath

    def __exit__(self, t, value, traceback):
        if hasattr(self, 'abspath') and self.abspath is not None:
            os.unlink(self.abspath)
