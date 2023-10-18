import sys
from dist.PyTestique import PyTestique, PyTestiqueAsserts


def test_foo() -> None:
    print("test foo!")
    PyTestiqueAsserts.assertAlmostEqual(6.666666677, 6.666666666699)


def setup_bar() -> None:
    print("setup bar!")
    raise Exception("Oh fuck! Setup bar exception.")


def test_bar() -> None:
    print("test bar!")


def teardown_bar() -> None:
    print("teardown bar!")


def test_foobar() -> None:
    print("test foobar!")
    assert False


def test_foobarfoo() -> None:
    print("test foobarfoo!")
    raise NameError("FooBarFoo weird name.")


def teardown_foobarfoo() -> None:
    print("teardown foobarfoo!")
    raise Exception("Teardown foobarfoo exception.")


PyTestique(sys.argv, globals())
