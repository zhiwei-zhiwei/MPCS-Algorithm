from collections import Counter

from bitstring import Bits
import pytest

import huffman

TEXTS = [
    "David Huffman invented Huffman coding at MIT in 1952.",

    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut "
    "labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco "
    "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in "
    "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
    "cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",

    "To be, or not to be, that is the question:"
    "Whether 'tis nobler in the mind to suffer"
    "The slings and arrows of outrageous fortune,"
    "Or to take arms against a sea of troubles"
    "And by opposing end them. To dieto sleep,"
    "No more; and by a sleep to say we end"
    "The heart-ache and the thousand natural shocks"
    "That flesh is heir to: 'tis a consummation"
    "Devoutly to be wish'd. To die, to sleep;"
    "To sleep, perchance to dreamay, there's the rub:"
    "For in that sleep of death what dreams may come,"
    "When we have shuffled off this mortal coil,"
    "Must give us pausethere's the respect"
    "That makes calamity of so long life."
    "For who would bear the whips and scorns of time,"
    "Th'oppressor's wrong, the proud man's contumely,"
    "The pangs of dispriz'd love, the law's delay,"
    "The insolence of office, and the spurns"
    "That patient merit of th'unworthy takes,"
    "When he himself might his quietus make"
    "With a bare bodkin? Who would fardels bear,"
    "To grunt and sweat under a weary life,"
    "But that the dread of something after death,"
    "The undiscovere'd country, from whose bourn"
    "No traveller returns, puzzles the will,"
    "And makes us rather bear those ills we have"
    "Than fly to others that we know not of?"
    "Thus conscience doth make cowards of us all,"
    "And thus the native hue of resolution"
    "Is sicklied o'er with the pale cast of thought,"
    "And enterprises of great pith and moment"
    "With this regard their currents turn awry"
    "And lose the name of action.",

    "Beautiful is better than ugly."
    "Explicit is better than implicit."
    "Simple is better than complex."
    "Complex is better than complicated."
    "Flat is better than nested."
    "Sparse is better than dense."
    "Readability counts."
    "Special cases aren't special enough to break the rules."
    "Although practicality beats purity."
    "Errors should never pass silently."
    "Unless explicitly silenced."
    "In the face of ambiguity, refuse the temptation to guess."
    "There should be one-- and preferably only one --obvious way to do it."
    "Although that way may not be obvious at first unless you're Dutch."
    "Now is better than never."
    "Although never is often better than *right* now."
    "If the implementation is hard to explain, it's a bad idea."
    "If the implementation is easy to explain, it may be a good idea."
    "Namespaces are one honking great idea -- let's do more of those!",
]

EXPECTED_LENGTHS = [
    226,
    1847,
    6022,
    3567,
]


@pytest.mark.parametrize("text,expected_length", zip(TEXTS, EXPECTED_LENGTHS))
def test_texts(text, expected_length):
    frequency_map = Counter(text)
    codec = huffman.HuffmanCodec(frequency_map)
    huffman_encoding = codec.encode(text)
    assert len(huffman_encoding) <= expected_length
    assert codec.decode(huffman_encoding) == text


def test_doctest():
    import doctest
    assert doctest.testmod(huffman).failed == 0


@pytest.mark.parametrize("text", TEXTS)
def test_encoding_error(text):
    frequency_map = Counter(text)
    codec = huffman.HuffmanCodec(frequency_map)
    text = text[:len(text)//2] + "&" + text[len(text)//2:]
    with pytest.raises(ValueError, match="Unsupported symbol: '&'"):
        codec.encode(text)


def test_decoding_error():
    text = "aaaaaabbbbbccccddd"
    frequency_map = Counter(text)
    codec = huffman.HuffmanCodec(frequency_map)
    huffman_encoding = codec.encode(text)

    bad_encoding0 = huffman_encoding + Bits(bin="0b0")
    with pytest.raises(ValueError, match="Could not decode."):
        codec.decode(bad_encoding0)

    bad_encoding1 = Bits(bin="0b0") + huffman_encoding
    with pytest.raises(ValueError, match="Could not decode."):
        codec.decode(bad_encoding1)
