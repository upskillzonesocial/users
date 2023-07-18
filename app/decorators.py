# Decorators
"""
Decorator is  a function it takes another fun as argument and
returns the modified function without changing the
original function



"""
import time


def execution_time_calculator(another_function):
    def wrapper():
        st = time.time()
        another_function()
        et = time.time()
        print(f"Function {another_function.__name__} took {et - st} seconds")

    return wrapper


@execution_time_calculator
def fun1():
    time.sleep(5)


@execution_time_calculator
def fun2():
    time.sleep(3)


fun1()
fun2()

# In the above example fun1 & fun2 don't have time logic to find
# the total time of function execution. But Decorator function has
# time logic written which would cal total time took in seconds.

# Now that we are decorating fun1 & fun2 with time logic
import datetime

print(str(datetime.datetime.now()))
