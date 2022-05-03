import functools
import time


def retry(max_attempts=1, backoff=1, exceptions=None):
    exceptions = tuple(exceptions) or (Exception,)
    """Simple retry decorator to allow counter for attempts,
    backoff setting and an exception list"""

    def retry_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(backoff)
        return wrapper
    return retry_decorator


if __name__ == "__main__":
    from random import randint

    class LowerException(Exception):
        pass

    class LargerException(Exception):
        pass

    def tryordie(number):
        my_favourite_number = 7
        if number == my_favourite_number:
            return my_favourite_number
        elif number < my_favourite_number:
            raise LowerException("small number")
        else:
            raise LargerException("large number")

    @retry(3, 1, (LowerException, LargerException, TypeError))
    def guesser():
        """try to guess number"""
        mynum = randint(0, 10)  # nosec
        if mynum == 0:
            mynum = "Zero"
        print("trying ", mynum)
        print(tryordie(mynum))

    guesser()
