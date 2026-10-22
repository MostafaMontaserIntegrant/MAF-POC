"""Fibonacci utilities designed to be easily unit tested."""


def fibonacci(n):
    """Return the nth Fibonacci number (0-indexed: fib(0) = 0, fib(1) = 1).

    Raises:
        ValueError: if n is negative.
        TypeError: if n is not an integer.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_sequence(count):
    """Return a list containing the first `count` Fibonacci numbers.

    Raises:
        ValueError: if count is negative.
        TypeError: if count is not an integer.
    """
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("count must be an integer")
    if count < 0:
        raise ValueError("count must be a non-negative integer")

    return [fibonacci(i) for i in range(count)]


if __name__ == "__main__":
    for i in range(10):
        print(f"fibonacci({i}) = {fibonacci(i)}")
