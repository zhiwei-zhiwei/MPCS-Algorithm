import os
import pytest

from noahs_ark import largest_island


INPUT_PREFIX = "input"
OUTPUT_PREFIX = "output"
TESTCASE_DIR = "testcases"
TIMEOUT = 20

dir_path = os.path.dirname(os.path.realpath(__file__))
test_path = os.path.join(dir_path, TESTCASE_DIR)
input_files = sorted([f for f in os.listdir(test_path) if f.startswith(INPUT_PREFIX)])
files = []
for i in input_files:
    o = OUTPUT_PREFIX + i[len(INPUT_PREFIX):]
    full_input_path = os.path.join(test_path, i)
    full_output_path = os.path.join(test_path, o)
    if os.path.isfile(full_output_path):
        files.append((full_input_path, full_output_path))

input_files = list(map(lambda x: x[0], files))  # Used as ids for the tests.


def read_input(file):
    with open(file) as f:
        n, m = [int(i) for i in f.readline().split()]
        heights = [[int(i) for i in line.split()] for line in f]
        return n, m, heights


def read_output(file):
    with open(file) as f:
        return [line.strip() for line in f]


# Defines the setup of the test below. Since `params` is set to a list, this will
# execute any related tests once per item in that list (a pair of files).
# Note: The time it takes to run the fixture does not count towards the execution
# timeout. (I've checked.)
@pytest.fixture(params=files, ids=input_files)
def file_io(request):
    (input_file, output_file) = request.param
    n, m, heights = read_input(input_file)
    mask = read_output(output_file)
    mask = [[l == '1' for l in m_line] for m_line in mask]

    return n, m, heights, mask,


@pytest.mark.execution_timeout(TIMEOUT)
def test_solve(file_io):
    n, m, heights, expected_mask = file_io
    mask = largest_island(heights)

    assert mask == expected_mask
