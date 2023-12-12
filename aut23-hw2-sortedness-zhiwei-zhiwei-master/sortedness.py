import math
import random
from math import ceil
from typing import *


def isEpsilonSorted(array: List[int], eps: float):
    """
    Given an array of integers in [n], return True if the array is epsilon sorted.

    The function should return True with a constant probability if the array is epsilon sorted
    and False with a constant probability if it is not.

    This function should run in sublinear time to the size of the array.

    Parameters
    ----------
    array : List[int]
        The array that is being checked
    eps : float
        How sorted we check the array to be

    Returns
    -------
    boolean
        Whether the array is epsilon sorted
    """

    # TODO: Your code here

    def binarySearch(a, X):
        low, high = 0, len(a) - 1
        while low <= high:
            mid = (low + high) // 2
            if a[mid] == X:
                return True
            elif a[mid] < X:
                low = mid + 1
            else:
                high = mid - 1
        return False

    T = ceil(math.log(3) / eps)
    for t in range(T):
        if eps >= 1: return True
        rand_choose = array[random.randint(0, len(array) - 1)]
        if not binarySearch(array, rand_choose):
            return False
    return True

# if __name__ == '__main__':
#     isEpsilonSorted([1,2,3,4,2,6,7,8], 0.2)
