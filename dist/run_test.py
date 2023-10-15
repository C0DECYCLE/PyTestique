import sys
from dist.PyTestique import PyTestique, PyTestiqueAsserts


def setup_foo() -> None:
    print("setup foo!")


def test_foo() -> None:
    PyTestiqueAsserts.assertAlmostEqual(6.666666677, 6.666666666699)


def teardown_foo() -> None:
    print("teardown foo!")


def setup_bar() -> None:
    print("setup bar!")


def test_bar() -> None:
    print("test bar!")
    raise Exception()


def teardown_bar() -> None:
    print("teardown bar!")


def setup_foobar() -> None:
    print("setup foobar!")


def test_foobar() -> None:
    print("test foobar!")
    assert False


def teardown_foobar() -> None:
    print("teardown foobar!")


PyTestique(sys.argv, globals())
