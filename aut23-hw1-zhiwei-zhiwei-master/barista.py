from typing import List, Tuple


def solve(N: int, K: int, times: List[int]) -> Tuple[int, int]:
    """
    Given the number of baristas, your position in the queue and the time it
    takes each barista to prepare a drink, returns which barista will make your
    drink and when it will be ready.

    Parameters
    ----------
    N : int
        The number of baristas.
    K : int
        Your position in the queue.
    times : List[int]
        A list of the time it takes each barista to prepare a drink.

    Returns
    -------
    Tuple[int, int]
        Two integers, the number of the barista who will prepare your drink and
        the time that it will be ready
    """

    # TODO: Your code here.
    # https://chat.openai.com/share/b78f13b3-e1e8-4bbe-a5e4-89fcb6b0b91f
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b
        return a

    def lcm(a: int, b: int) -> int:
        return abs(a * b) // gcd(a, b)

    def lcm_list(numbers: List[int]) -> int:
        result = 1
        for num in numbers:
            result = lcm(result, num)
        return result

    def total_drinks_served(t: int, times: List[int]) -> int:
        a = sum((t // time) for time in times)
        return a

    max_num = lcm_list(times)  # find the lcm
    sum_customer = total_drinks_served(max_num, times)  # base on the lcm number, find sum of customer it can serve
    # print(max_num)
    # print(sum_customer)
    iteration_times = K // sum_customer  # time of iteration
    rest_customer = K - iteration_times * sum_customer  # the rest of customer

    if rest_customer == 0:
        if len(set(times)) == 1:
            return len(times), iteration_times * max_num
        return 1, iteration_times * max_num
    # print(iteration_times)
    # print(rest_customer)
    # Brute force approach - timeout
    barista_list = [0] * N  # Each barista's next available time
    # print("next_available", next_available)
    time = 0
    for _ in range(rest_customer):
        # print(baristaList)
        barista = min(range(N), key=lambda i: barista_list[i])
        # print("---------------", barista)

        time += barista_list[barista]
        barista_list[barista] += times[barista]
    print(barista_list)
    return barista + 1, barista_list[barista] + iteration_times * max_num


def read_input():
    N, K = [int(i) for i in input().split()]
    times = [int(i) for i in input().split()]
    return N, K, times


def main():
    N, K, times = read_input()
    barista, T = solve(N, K, times)
    print(barista, T)


if __name__ == '__main__':
    main()
