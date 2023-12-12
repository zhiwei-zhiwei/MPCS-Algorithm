# Noah's Ark

It has been raining for 40 days and 40 nights and the whole world has gone underwater! But finally the clouds are parting and the sun shines once more. You need to decide where you will dock your ark and rebuild civilization. It has been decided that you should find the largest landmass. You are lucky to have an exceptional topographical map that has the exact heights of the entire terrain. Unfortunately, you can't just find the largest landmass over sea level, as water can be trapped in valleys, forming lakes that should not be counted toward the size of the landmass. In order for a point of the terrain to be part of the landmass, water must be able to drain to sea level (height $\leq 0$). Water can flow to any of the eight surrounding points whose height is strictly less. For example, if a point has height $2$, then water can drain to all adjacent (including diagonally) points with height up to $1$. 


## Assignment

Given the topological map as a square $n \times m$ array, you need to return a mask of the largest island. In the first line there are two integers, $n$ and $m$, the dimensions of the grid. Each of the next $n$ lines has $m$ integers, the heights of the grid. In your function `largest_island`, you are given `heights` as a list of integer lists. For example, consider the following input

```
5 5
0 1 3 2 3
2 2 2 2 1
3 3 1 2 2
2 1 1 3 3
3 2 5 1 -2
```

Below is shown the topological map of heights in grayscale. After the water drains, land is shown with black. Finally, in the third image, the largest island is shown.

&emsp;&emsp; <img src="https://lh3.googleusercontent.com/pw/AIL4fc8zMGEnx1O8xqJneGVmeSO3z_lGtrgGp5AT59XFbw0liJOUN1mFMIuZwZuOX_EJNpW8aeCJYGkA77Pf2GCoLdnq-kCdxlLKr0A68r7I2WZB1HowAZsDXInDF_GlMjqLAWST5RE5IQy0CNgf_FzhT6Ma=w1007-h1007-s-no?authuser=0" width="200"> &emsp;&emsp;&emsp;&emsp; <img src="https://lh3.googleusercontent.com/pw/AIL4fc8RhGpsgi9xihInZfkSjVpRsa_1QqK5dQM0PsdBJ9520hiz7KToTcpVq8k0yRnsOKAtbXTCLPUx3Cj_0CIdeotrHQRMzud5DYPWVkGDNadd1Z_aT6z-fmI6d3yuaezJYMWcnNm8zs_xMjuHonL5nzCA=w1068-h1068-s-no?authuser=0" width=200> &emsp;&emsp;&emsp;&emsp; <img src="https://lh3.googleusercontent.com/pw/AIL4fc8rvz-iaRqdmwgcXR2zCVF8vpO-YX285XyH5PfV_5OXJjyp9DS_kY2j2vuZKjYOTKXgb45UsNCGT2nWSgizJl68XwYUE5bXRfSAKIR3esCREcs5qd2d9OSI6PmiFdVhiSqScGYZEjn4u-KfI4Iqp_Q8=w1068-h1068-s-no?authuser=0" width=200>
 
Translating `True` to `1` and `False` to `0`, the correct output will be
```
01100
11100
11000
00000
00000
``` 

## A Note on Recursion

If you choose to write a recursive algorithm, then there is a chance you will run into `RecursionError: maximum recursion depth exceeded`. This occurs when python makes too many recursive calls, by default the limit is a depth of 1000 'nested' calls. 

You can override the recursion depth if you want, by calling `sys.setrecursionlimit(n)` once at the start of your code. However, python is still limited by the size of the stack (i.e. the memory region where data associated with each function is stored). If you exceed this limit, you will likely see a `segfault`. There isn't an easy fix in this case.

So be aware of how deep your recursive calls can get. If you can bound the depth to a reasonable level, you should be safe. If you do find your code `segfualt`-ing, then you may want to redesign a piece of your algorithm. You might be able to maintain the core of the recursive algorithm if you store function information (i.e. arguments) in a seperate data structure. This takes pressure off of the stack memory region, putting the same data on the heap.


## Testing

A number of test cases have been provided and you can test your implementation by using the `pytest` library.

Install the required libraries by running the following command:

```
python3 -m pip install -r requirements.txt
```

Then you can run all the tests at once with the following command:

```
python3 -m pytest test_noahs_ark.py
```

Note that you do not need to do any parsing of these files yourself; that task is handled
for you by our tests.

You can invoke `pytest` in a number of ways. Optionally, you can read up on it
[here](https://docs.pytest.org/en/6.2.x/usage.html). Most notably, you can run a single
test on its own with the `-k` flag. For instance:

```
python3 -m pytest -k input05.txt
```

This command runs the fifth test.

It is useful to see only first test that fails, which can be done with the `-x` flag.
Finally, the `-v` flag will make test output more verbose, which can help you diagnose if tests are failing.

## Submission

Submit your code by committing and pushing it to your github repository. This assignment is due at the same time as the Homework 5 theory problems, and the same late penalty applies. We will grade the code based on the last commit before the deadline.

Note that the tests are mainly to help you confirm that your code is working. Your grade **is not** simply your score on the tests. We will read your code as
well. *If the deadline is close and you are still not passing tests, you should
push your code anyway; you may get partial credit.*
