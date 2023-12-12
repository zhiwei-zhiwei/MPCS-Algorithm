import random
import pytest

from sortedness import isEpsilonSorted


SEED = 17
REPEATS = 20
INPUT_PREFIX = "input"
TESTCASE_DIR = "testcases"
TIMEOUT = 20

random.seed(SEED)
with open('testcases_descriptions.txt') as f:
    params = []
    ids = []
    for i, line in enumerate(f, 1):
        tokens = line.split()
        n = int(tokens[0])
        eps = float(tokens[1])
        params.append((n, eps))
        ids.append(f'{i}')

# input_files = files     # Used as ids for the tests.


def generate_array(n, epsilon):
    array = list(range(n))
    for i in range(n - 1):
        if random.random() < epsilon / 2:
            j = random.randint(i+1, n-1)
            array[i], array[j] = array[j], array[i]
    return array


def least_above(ans, elem):
    low, high = 0, len(ans) - 1
    while low < high - 1:
        mid = (low + high) // 2
        if ans[mid] < elem:
            low = mid
        else:
            high = mid
    if ans[low] > elem:
        return low
    else:
        return high


def how_sorted(array):
    ans = [array[0]]
    for a in array[1:]:
        if a > ans[-1]:
            ans.append(a)
        else:
            j = least_above(ans, a)
            ans[j] = a
    return 1 - len(ans) / len(array)


# Defines the setup of the test below. Since `params` is set to a list, this will
# execute any related tests once per item in that list (a pair of files).
# Note: The time it takes to run the fixture does not count towards the execution
# timeout. (I've checked.)
@pytest.fixture(params=params, ids=ids)
def file_io(request):
    n, epsilon = request.param
    arrays = [generate_array(n, epsilon) for _ in range(REPEATS)]
    epsilons = [how_sorted(array) for array in arrays]
    return [(arr, eps) for (arr, eps) in zip(arrays, epsilons) if eps > 0]


@pytest.mark.execution_timeout(TIMEOUT)
def test_solve(file_io):
    inputs = file_io

    # This test should pass, since the chance `isEpsilonSorted` returns false
    # is at least 2/3.
    results = [isEpsilonSorted(array, epsilon) for (array, epsilon) in inputs]
    assert not all(results), 'All the tests returned True'

    # Note: We don't have a reliable lower bound for how often the algorithm rejects
    # an array that is X times more sorted than the supplied epsilon. Actually, 
    # it depends a lot on the structure of the underlying array. (Can you see why?)
    # For this reason, we generate many seperate arrays instead of testing 1 array many times.
    # Even so, we don't know the actual rejection rate, so we can only say ~empirically~
    # that this part of the test should pass.
    results = [isEpsilonSorted(array, 10 * epsilon) for (array, epsilon) in inputs]
    assert any(results), 'None of the tests returned True'
