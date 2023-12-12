
# Testing Sortedness

We define an array of length $n$ to be $\epsilon$-sorted if modifying $\epsilon n$ entries would make it sorted. For example, the following array 

<table> 
	<tr> 
		<td> 1 </td> <td> 2 </td> <td> <b> 6 </b> </td> <td> 3 </td> <td> 4 </td> <td> 5 </td> <td> 7 </td> <td> 8 </td>
	</tr>
</table>

is $\frac{1}{8}$-sorted, since we just need to change $\frac{1}{8} \cdot 8 = \epsilon n = 1$ element. Insertion sort will perform a linear number of operations to arrange this array correctly, whereas quicksort would still take $O(n \log n)$ expected time. On the other hand, if an array is far from being sorted, insertion sort would take $O(n^2)$. Without being able to assess which of the two cases we are facing, we cannot pick the most efficient algorithm. 

Unfortunately, finding exactly how sorted an array is requires computing the size of the longest increasing subsequence, which takes $O(n \log n)$ time. That would counteract any benefit from choosing the appropriate sorting algorithm.

Instead, we can use a probabilistic (coRP-type) sublinear algorithm to check if the array is close to sorted. Our algorithm should succeed with at least **constant probability**. This approach requires a property that sorted arrays always have and unsorted arrays only sometimes have. Additionally, that property must be verifiable in sublinear time, for example $O(\log n)$. 

**Property:** Binary search for an existing element in a sorted array always succeeds.

In contrast, arrays that are not sorted will have at most $(1 - \epsilon) n$ elements with this property. Therefore, if $S$ is the event that the array is sorted and $b$ is the event that performing binary search on a single element of the array is successful, then $Pr[b | S] = 1$ and $Pr[b | \neg S] = (1 - \epsilon)$. Repeating the check $T$ times successfully happens with probability

$$Pr[b_1, b_2, \ldots b_t | \neg S] \leq \prod_{i = 1}^T Pr[b_i | \neg S] = (1-  \epsilon)^T$$

A very useful inequality in these situations is $1 + x \leq e^x$. Substituting $x = - \epsilon$ we get

$$(1 - \epsilon)^{T} \leq e^{-\epsilon \cdot T}$$

Setting $T = \lceil\frac{\ln 3}{\epsilon}\rceil$ it transforms to

$$(1 - \epsilon)^{\lceil\frac{\ln 3}{\epsilon}\rceil} \leq e^{\left(-\epsilon \frac{\ln 3}{\epsilon}\right)} = 1/3$$

Thus the tester rejects an array that is $\epsilon$-far from sorted with probability at least $2/3$.

Despite the elaborate analysis above, the algorithm is quite easy to describe.

```
Function isEpsilonSorted(a, epsilon):
	T = ceil(ln(3) / epsilon)
	for t in T:
		select random element X of the array
		if not binarySearch(a, X):
			return False
	return True
```

## Assignment

Given an array $a$ and a target $\epsilon$, your code should detect if the array is not $\epsilon$-sorted with at least constant probability by selecting $\lceil\frac{\ln 3}{\epsilon}\rceil$ random elements and searching for them using binary search. If all elements are successfully found, then it should return True, False otherwise.

## Testing

A number of test cases have been provided and you can test your implemenation by using the `pytest` library.

Install the required libraries by running the following command:

```
python3 -m pip install -r requirements.txt
```

Then you can run all the tests at once with the following command:

```
python3 -m pytest test_sortedness.py
```

Note that you do not need to do any parsing of these files yourself; that task is handled for you by our tests.

You can invoke `pytest` in a number of ways. Optionally, you can read up on it [here](https://docs.pytest.org/en/6.2.x/usage.html). Most notably, you can run a single test on its own with the `-k` flag. For instance:

```
python3 -m pytest -k 5
```

This command runs the fifth test.

It is useful to see only first test that fails, which can be done with the `-x` flag. Finally, the `-v` flag will make test output more verbose, which can help you diagnose if tests are failing.

## Submission

Submit your code by committing and pushing it to your github repository. This assignment is due at the same time as the Homework 2 theory problems, and the same late penalty applies. We will grade the code based on the last commit before the deadline.

Note that the tests are mainly to help you confirm that your code is working. Your grade **is not** simply your score on the tests. We will read your code as well. *If the deadline is close and you are still not passing tests, you should push your code anyway; you may get partial credit.*

