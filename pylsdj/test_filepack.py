import os
import sys
import json
from nose.tools import raises, assert_equal, assert_list_equal
from .vendor.six.moves import range

SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))

sys.path.append(os.path.join(SCRIPT_DIR, os.path.pardir))


def assert_bytearray_equal(x, y):
    assert_list_equal(list(map(hex, x)), list(map(hex, y)))

from . import filepack as filepack
from . import blockutils as bl
from . import bread_spec as bread_spec
import bread as b


def test_basic_compress_decompress():
    data = [i % 10 for i in range(5000)]

    compressed = filepack.compress(data)

    decompressed = filepack.decompress(compressed)

    assert_list_equal(data, decompressed)


def test_rle_compress():
    data = [0xde for i in range(350)]
    data.extend([0xfe for i in range(220)])
    data.append(42)
    data.append(17)

    compressed = filepack.compress(data)

    reference = [filepack.RLE_BYTE, 0xde, 255,
                 filepack.RLE_BYTE, 0xde, 95,
                 filepack.RLE_BYTE, 0xfe, 220,
                 42, 17]

    assert_list_equal(compressed, reference)

    decompressed = filepack.decompress(compressed)

    assert_list_equal(decompressed, data)


def test_short_rle_compress():
    data = [0xde, 0xde, 42, 17, 12]

    compressed = filepack.compress(data)

    assert_list_equal(compressed, data)


def test_rle_special_byte():
    data = [filepack.RLE_BYTE, filepack.RLE_BYTE,
            filepack.SPECIAL_BYTE, filepack.SPECIAL_BYTE,
            filepack.RLE_BYTE, filepack.SPECIAL_BYTE]

    reference = [filepack.RLE_BYTE,
                 filepack.RLE_BYTE,
                 filepack.RLE_BYTE,
                 filepack.RLE_BYTE,
                 filepack.SPECIAL_BYTE,
                 filepack.SPECIAL_BYTE,
                 filepack.SPECIAL_BYTE,
                 filepack.SPECIAL_BYTE,
                 filepack.RLE_BYTE,
                 filepack.RLE_BYTE,
                 filepack.SPECIAL_BYTE,
                 filepack.SPECIAL_BYTE]

    compressed = filepack.compress(data)

    assert_list_equal(compressed, reference)

    decompressed = filepack.decompress(compressed)

    assert_list_equal(decompressed, data)


def test_default_instr_compress():
    data = []

    for i in range(42):
        data.extend(filepack.DEFAULT_INSTRUMENT)

    reference = []

    reference.extend([0, filepack.SPECIAL_BYTE,
                      filepack.DEFAULT_INSTR_BYTE, 41])
    reference.extend(filepack.DEFAULT_INSTRUMENT_FILEPACK)

    reference = bytearray(reference)

    decompressed_reference = filepack.decompress(reference)
    assert_list_equal(decompressed_reference, data + [0])

    data = bytearray(data)

    compressed = filepack.compress(data)

    assert_bytearray_equal(bytearray(compressed + [0]), reference)

    decompressed = filepack.decompress(compressed)

    assert_bytearray_equal(data, bytearray(decompressed))


def test_instrument_sizes():
    instr_bytes = list(filepack.DEFAULT_INSTRUMENT)

    parsed = b.parse(instr_bytes, bread_spec.instrument)
    assert_equal(len(parsed), 16 * 8)

    raw_data = b.write(parsed, bread_spec.instrument)
    assert_bytearray_equal(raw_data, bytearray(filepack.DEFAULT_INSTRUMENT))

    instr_bytes[0] = 1

    parsed = b.parse(instr_bytes, bread_spec.instrument)
    assert_equal(len(parsed), 16 * 8)

    instr_bytes[0] = 2

    parsed = b.parse(instr_bytes, bread_spec.instrument)
    assert_equal(len(parsed), 16 * 8)

    instr_bytes[0] = 3

    parsed = b.parse(instr_bytes, bread_spec.instrument)
    assert_equal(len(parsed), 16 * 8)


def test_default_wave_compress():
    data = []

    for i in range(33):
        data.extend(filepack.DEFAULT_WAVE)

    compressed = filepack.compress(data)

    reference = [filepack.SPECIAL_BYTE, filepack.DEFAULT_WAVE_BYTE, 33]

    decompressed_reference = filepack.decompress(reference)
    assert_list_equal(decompressed_reference, data)

    decompressed = filepack.decompress(compressed)

    assert_list_equal(data, decompressed)
    assert_list_equal(compressed, reference)


def test_large_rle_compress():
    data = []

    for i in range(275):
        data.append(42)

    compressed = filepack.compress(data)

    reference = [filepack.RLE_BYTE, 42, 255, filepack.RLE_BYTE, 42, 20]

    assert_list_equal(compressed, reference)

    decompressed = filepack.decompress(compressed)

    assert_list_equal(data, decompressed)


@raises(AssertionError)
def test_bad_rle_split():
    data = [filepack.RLE_BYTE]

    factory = bl.BlockFactory()

    filepack.split(data, bl.BLOCK_SIZE, factory)


@raises(AssertionError)
def test_bad_special_byte_split():
    data = [filepack.SPECIAL_BYTE]

    factory = bl.BlockFactory()

    filepack.split(data, bl.BLOCK_SIZE, factory)


@raises(AssertionError)
def test_block_jump_during_split_asserts():
    data = [filepack.SPECIAL_BYTE, 47]

    factory = bl.BlockFactory()

    filepack.split(data, bl.BLOCK_SIZE, factory)


def test_special_byte_on_block_boundary():
    data = [42, 17, filepack.SPECIAL_BYTE, filepack.SPECIAL_BYTE,
            100, 36]

    factory = bl.BlockFactory()

    filepack.split(data, 5, factory)

    block_0_expected = [42, 17, filepack.SPECIAL_BYTE, 1, 0]
    block_1_expected = [filepack.SPECIAL_BYTE, filepack.SPECIAL_BYTE, 100,
                        filepack.SPECIAL_BYTE, 2]
    block_2_expected = [36, filepack.SPECIAL_BYTE, filepack.EOF_BYTE, 0, 0]

    assert_equal(len(factory.blocks), 3)
    assert_list_equal(factory.blocks[0].data, block_0_expected)
    assert_list_equal(factory.blocks[1].data, block_1_expected)
    assert_list_equal(factory.blocks[2].data, block_2_expected)


def test_rle_byte_on_block_boundary():
    data = [42, 17, filepack.RLE_BYTE, filepack.RLE_BYTE,
            100, 36]

    factory = bl.BlockFactory()

    filepack.split(data, 5, factory)

    block_0_expected = [42, 17, filepack.SPECIAL_BYTE, 1, 0]
    block_1_expected = [filepack.RLE_BYTE, filepack.RLE_BYTE, 100,
                        filepack.SPECIAL_BYTE, 2]
    block_2_expected = [36, filepack.SPECIAL_BYTE, filepack.EOF_BYTE, 0, 0]

    assert_equal(len(factory.blocks), 3)
    assert_list_equal(factory.blocks[0].data, block_0_expected)
    assert_list_equal(factory.blocks[1].data, block_1_expected)
    assert_list_equal(factory.blocks[2].data, block_2_expected)


def test_full_rle_on_block_boundary():
    data = [42, filepack.RLE_BYTE, 55, 4, 22, 3]

    factory = bl.BlockFactory()

    filepack.split(data, 5, factory)

    block_0_expected = [42, filepack.SPECIAL_BYTE, 1, 0, 0]
    block_1_expected = [filepack.RLE_BYTE, 55, 4, filepack.SPECIAL_BYTE, 2]
    block_2_expected = [22, 3, filepack.SPECIAL_BYTE, filepack.EOF_BYTE, 0]

    assert_equal(len(factory.blocks), 3)
    assert_list_equal(factory.blocks[0].data, block_0_expected)
    assert_list_equal(factory.blocks[1].data, block_1_expected)
    assert_list_equal(factory.blocks[2].data, block_2_expected)


def test_default_on_block_boundary():
    data = [42, filepack.SPECIAL_BYTE, filepack.DEFAULT_INSTR_BYTE, 3, 2, 5]

    factory = bl.BlockFactory()

    filepack.split(data, 5, factory)

    block_0_expected = [42, filepack.SPECIAL_BYTE, 1, 0, 0]
    block_1_expected = [filepack.SPECIAL_BYTE, filepack.DEFAULT_INSTR_BYTE, 3,
                        filepack.SPECIAL_BYTE, 2]
    block_2_expected = [2, 5, filepack.SPECIAL_BYTE, filepack.EOF_BYTE, 0]

    assert_equal(len(factory.blocks), 3)
    assert_list_equal(factory.blocks[0].data, block_0_expected)
    assert_list_equal(factory.blocks[1].data, block_1_expected)
    assert_list_equal(factory.blocks[2].data, block_2_expected)


def test_merge_with_rle_byte():
    factory = bl.BlockFactory()

    block1 = factory.new_block()
    block1.data = [filepack.RLE_BYTE, filepack.RLE_BYTE, 2, 1, 3,
                   filepack.SPECIAL_BYTE, 1, 0, 0]
    block2 = factory.new_block()
    block2.data = [4, 3, 6, filepack.SPECIAL_BYTE, filepack.EOF_BYTE]

    data = filepack.merge(factory.blocks)
    expected_data = [filepack.RLE_BYTE, filepack.RLE_BYTE, 2, 1, 3, 4, 3, 6]

    assert_list_equal(data, expected_data)


def test_merge_with_full_rle():
    factory = bl.BlockFactory()
    block1 = factory.new_block()
    block1.data = [filepack.RLE_BYTE, 42, 17, 1, 1, 4,
                   filepack.SPECIAL_BYTE, 1, 0, 0]
    block2 = factory.new_block()
    block2.data = [4, 4, 42, filepack.SPECIAL_BYTE, filepack.EOF_BYTE]

    data = filepack.merge(factory.blocks)

    assert_list_equal(data, [filepack.RLE_BYTE, 42, 17, 1, 1, 4, 4, 4, 42])


def test_merge_with_special_byte():
    factory = bl.BlockFactory()

    block1 = factory.new_block()
    block1.data = [filepack.SPECIAL_BYTE, filepack.SPECIAL_BYTE, 2, 1, 3,
                   filepack.SPECIAL_BYTE, 1, 0, 0]
    block2 = factory.new_block()
    block2.data = [4, 3, 6, filepack.SPECIAL_BYTE, filepack.EOF_BYTE]

    data = filepack.merge(factory.blocks)
    expected_data = [filepack.SPECIAL_BYTE, filepack.SPECIAL_BYTE, 2, 1, 3, 4,
                     3, 6]

    assert_list_equal(data, expected_data)


def test_merge_with_special_command():
    factory = bl.BlockFactory()

    block1 = factory.new_block()
    block1.data = [filepack.SPECIAL_BYTE, filepack.DEFAULT_INSTR_BYTE, 4, 6,
                   1, 93, filepack.SPECIAL_BYTE, 1, 0, 0]
    block2 = factory.new_block()
    block2.data = [3, 3, 33, filepack.SPECIAL_BYTE, filepack.EOF_BYTE]

    data = filepack.merge(factory.blocks)
    expected_data = [filepack.SPECIAL_BYTE, filepack.DEFAULT_INSTR_BYTE, 4, 6,
                     1, 93, 3, 3, 33]

    assert_list_equal(data, expected_data)


@raises(AssertionError)
def test_decompress_bogus_special_byte_asserts():
    data = [filepack.SPECIAL_BYTE, filepack.EOF_BYTE]

    filepack.decompress(data)


def test_weird_rle_compress():
    data = [0x1b, 0xc0, 0x00, 0x0f, 0x1d, 0xc0, 0x00, 0x0f, 0x1e, 0xc0,
            0x00, 0x0f, 0x20, 0xc0, 0x00, 0x1f, 0x22, 0x00, 0x00, 0x00,
            0x1e, 0x00, 0x1b, 0x00, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00,
            0x1d, 0x00, 0x00, 0x00, 0x19, 0x00, 0x00, 0x00, 0x20, 0x00,
            0x00, 0x00, 0x20, 0x00, 0x1e, 0x00, 0x1d, 0x00, 0x1b, 0x00,
            0x00, 0x00, 0x17, 0x00, 0x19, 0x00, 0x00, 0x00, 0x1b, 0x00,
            0x00, 0x00, 0x1e, 0x00, 0x1d, 0x00, 0x00, 0x00, 0x19, 0x00,
            0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x1d, 0x00, 0x00, 0x00,
            0x1e, 0x00, 0x00, 0x00, 0x1b, 0x00, 0x1e, 0x00, 0x00, 0x00,
            0x22, 0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x1d, 0x00,
            0x00, 0x00, 0x25, 0x00, 0x00, 0x00, 0x20, 0xc0, 0x00, 0x05,
            0x23, 0x00, 0x00, 0x00, 0x25, 0x00, 0x23, 0x00, 0x00, 0x00,
            0x1e, 0xc0, 0x00, 0x05, 0x20, 0x00, 0x00, 0x00, 0x1d, 0x00,
            0x19, 0x00, 0x00, 0x00, 0x1d, 0xc0, 0x00, 0x05, 0x20, 0x00,
            0x00, 0x00, 0x1d, 0x00, 0x19, 0x00, 0x00, 0x00, 0x1d, 0x00,
            0x00, 0x00, 0x1b, 0x00, 0x1b, 0x00, 0x00, 0x00, 0x16, 0x00,
            0x00, 0x00, 0x1b, 0x00, 0x00, 0x00, 0x1e, 0x00, 0x00, 0x00,
            0x1d, 0x00, 0x00, 0x00, 0x19, 0x00, 0x20, 0x00, 0x00, 0x00,
            0x1d, 0xc0, 0x00, 0x05, 0x1b, 0x00, 0x00, 0x00, 0x03, 0x00,
            0x03, 0x00, 0x00, 0x00, 0x03, 0x00, 0x03, 0x00, 0x1b, 0x19,
            0x03, 0xc0, 0x00, 0x0d, 0x03, 0x01, 0x0f, 0xc0, 0x00, 0x0f,
            0x19, 0xc0, 0x00, 0x1f, 0x1e, 0x00, 0x00, 0x00, 0x23, 0x00,
            0x1e, 0x00, 0x00, 0x00, 0x1b, 0xc0, 0x00, 0x05, 0x1d, 0x00,
            0x00, 0x00, 0x20, 0x00, 0x1d, 0x00, 0x00, 0x00, 0x19, 0xc0,
            0x00, 0x05, 0x1b, 0xc0, 0x00, 0x8f, 0x31, 0x00, 0x1b, 0x00,
            0x31, 0x00, 0x1b, 0x00, 0x31, 0x00, 0x1b, 0x00, 0x31, 0x00,
            0x1b, 0x00, 0x31, 0x00, 0x19, 0x00, 0x31, 0x00, 0x19, 0x00,
            0x31, 0x00, 0x19, 0x00, 0x31, 0x00, 0x19, 0x00, 0x31, 0x00,
            0x17, 0x00, 0x31, 0x00, 0x17, 0x00, 0x31, 0x00, 0x17, 0x00,
            0x31, 0x00, 0x17, 0x00, 0x31, 0xc0, 0x00, 0x09, 0x31, 0xc0,
            0x00, 0x05, 0x31, 0x00, 0x31, 0xc0, 0x00, 0x07, 0x31, 0xc0,
            0x00, 0x05, 0x31, 0x00, 0x0f, 0x00, 0x31, 0x00, 0x0f, 0x00,
            0x31, 0x00, 0x0f, 0x00, 0x31, 0x00, 0x0f, 0x00, 0x31, 0xc0,
            0x00, 0x9f, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
            0x01, 0x01, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00,
            0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x01, 0x00,
            0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00,
            0x01, 0x00, 0xc0, 0x01, 0x08, 0x00, 0x00, 0xc0, 0x01, 0x0e,
            0xc0, 0x00, 0x10, 0x01, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff,
            0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0,
            0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00,
            0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff,
            0xc0, 0x00, 0xab, 0xc0, 0xff, 0x40, 0xc0, 0x00, 0x60, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06,
            0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x06, 0x06, 0xc0, 0x00, 0x0e, 0x06, 0x06, 0xc0, 0x00,
            0x0e, 0x7f, 0x7f, 0x20, 0x31, 0x7f, 0x7f, 0x20, 0x30, 0x7f,
            0x7f, 0x20, 0x30, 0x7f, 0x7f, 0x20, 0x30, 0x7f, 0x10, 0x21,
            0x30, 0x7f, 0x10, 0x21, 0x30, 0x7f, 0x7f, 0x20, 0x30, 0x7f,
            0x7f, 0x20, 0x30, 0x7f, 0x10, 0x21, 0x30, 0x7f, 0x10, 0x21,
            0x30, 0x7f, 0x7f, 0x20, 0x30, 0x7f, 0x7f, 0x20, 0x30, 0x7f,
            0x11, 0x22, 0x31, 0x7f, 0x12, 0x22, 0x30, 0x7f, 0x13, 0x22,
            0x30, 0x7f, 0x12, 0x22, 0x30, 0x7f, 0x7f, 0x20, 0x30, 0x7f,
            0x7f, 0x20, 0x30, 0x7f, 0x7f, 0x20, 0x30, 0x7f, 0x7f, 0x20,
            0x30, 0x7e, 0x7e, 0x23, 0x32, 0xc0, 0xff, 0xff, 0xc0, 0xff,
            0xff, 0xc0, 0xff, 0xff, 0xc0, 0xff, 0xaf, 0xc0, 0x00, 0xff,
            0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0,
            0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00,
            0x47, 0x43, 0x20, 0x33, 0x20, 0x43, 0x23, 0x33, 0x20, 0x44,
            0x20, 0x33, 0x20, 0x44, 0x23, 0x33, 0x20, 0x45, 0x20, 0x33,
            0x20, 0x46, 0x20, 0x33, 0x20, 0x46, 0x23, 0x33, 0x20, 0x47,
            0x20, 0x33, 0x20, 0x47, 0x23, 0x33, 0x20, 0x41, 0x20, 0x33,
            0x20, 0x41, 0x23, 0x33, 0x20, 0x42, 0x20, 0x33, 0x20, 0x43,
            0x20, 0x34, 0x20, 0x43, 0x23, 0x34, 0x20, 0x44, 0x20, 0x34,
            0x20, 0x44, 0x23, 0x34, 0x20, 0x45, 0x20, 0x34, 0x20, 0x46,
            0x20, 0x34, 0x20, 0x46, 0x23, 0x34, 0x20, 0x47, 0x20, 0x34,
            0x20, 0x47, 0x23, 0x34, 0x20, 0x41, 0x20, 0x34, 0x20, 0x41,
            0x23, 0x34, 0x20, 0x42, 0x20, 0x34, 0x20, 0x43, 0x20, 0x35,
            0x20, 0x43, 0x23, 0x35, 0x20, 0x44, 0x20, 0x35, 0x20, 0x44,
            0x23, 0x35, 0x20, 0x45, 0x20, 0x35, 0x20, 0x46, 0x20, 0x35,
            0x20, 0x46, 0x23, 0x35, 0x20, 0x47, 0x20, 0x35, 0x20, 0x47,
            0x23, 0x35, 0x20, 0x41, 0x20, 0x35, 0x20, 0x41, 0x23, 0x35,
            0x20, 0x42, 0x20, 0x35, 0x20, 0x43, 0x20, 0x36, 0x20, 0x43,
            0x23, 0x36, 0x20, 0x44, 0x20, 0x36, 0x20, 0x44, 0x23, 0x36,
            0x20, 0x45, 0x20, 0x36, 0x20, 0x46, 0x20, 0x36, 0x20, 0x72,
            0x62, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xa7, 0xc0, 0x01, 0x09,
            0xc0, 0x00, 0x17, 0x01, 0x01, 0x01, 0xc0, 0x00, 0x0d, 0x01,
            0x01, 0x01, 0xc0, 0x00, 0x0d, 0x01, 0x01, 0xc0, 0x00, 0x0e,
            0xc0, 0x01, 0x05, 0xc0, 0x00, 0x0c, 0x01, 0x02, 0x02, 0xc0,
            0xff, 0x0c, 0x05, 0x06, 0x07, 0x08, 0xc0, 0xff, 0x0c, 0x09,
            0x0a, 0x0b, 0x0c, 0xc0, 0xff, 0x0c, 0x02, 0x03, 0x00, 0x00,
            0xc0, 0xff, 0x0c, 0x09, 0x0a, 0x0b, 0x0d, 0xc0, 0xff, 0x0c,
            0x0e, 0x0f, 0x15, 0x16, 0xc0, 0xff, 0x0c, 0x17, 0xc0, 0xfe,
            0x0f, 0xc0, 0xff, 0x90, 0xc0, 0x11, 0x04, 0xc0, 0xff, 0x0c,
            0x12, 0x12, 0x13, 0x13, 0xc0, 0xff, 0x0c, 0xc0, 0x13, 0x04,
            0xc0, 0xff, 0x0c, 0x12, 0x12, 0x13, 0x13, 0xc0, 0xff, 0xcc,
            0x20, 0x21, 0x22, 0x21, 0xc0, 0xff, 0x0c, 0x23, 0x24, 0x23,
            0x24, 0xc0, 0xff, 0x0c, 0xc0, 0x25, 0x04, 0xc0, 0xff, 0x0c,
            0x26, 0xc0, 0xfe, 0x0f, 0xc0, 0xff, 0xc0, 0x30, 0x31, 0x31,
            0x32, 0x00, 0xc0, 0xff, 0x0c, 0xfe, 0xfe, 0xfe,
            0x33, 0xc0, 0xff, 0x0c, 0x35, 0xc0, 0xfe, 0x0f, 0xc0, 0xff,
            0xff, 0xc0, 0xff, 0xff, 0xc0, 0xff, 0xff, 0xc0, 0xff, 0xff,
            0xc0, 0xff, 0xb4, 0xc0, 0xfe, 0x0b, 0xee, 0xee, 0xc0, 0xfe,
            0x07, 0xc0, 0xff, 0x0c, 0x00, 0x00, 0x00, 0x02, 0xc0, 0x00,
            0x2c, 0x04, 0x00, 0x08, 0x0a, 0xc0, 0x00, 0xec, 0xfe, 0xfe,
            0xc0, 0x00, 0x0e, 0x0c, 0x0c, 0xc0, 0x00, 0xff, 0xc0, 0x00,
            0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff, 0xc0, 0x00, 0xff,
            0xc0, 0x00, 0xff, 0xc0, 0x00, 0xd5, 0x88, 0x00, 0x3f, 0xff,
            0x00, 0x22, 0x83, 0x00, 0x00, 0xd0, 0x00, 0x00, 0x00, 0xf3]

    decompressed = filepack.decompress(data)

    recompressed = filepack.compress(decompressed)
    assert_list_equal(data, recompressed)


def test_sample_song():
    sample_song_compressed = os.path.join(
        SCRIPT_DIR, "test_data", "sample_song_compressed.json")

    with open(sample_song_compressed, "r") as fp:
        compressed = json.load(fp)

    decompressed = filepack.decompress(compressed)

    recompressed = filepack.compress(decompressed)

    assert_equal(len(decompressed), 0x8000)

    assert_equal(len(recompressed), len(compressed))
    assert_list_equal(recompressed, compressed)
