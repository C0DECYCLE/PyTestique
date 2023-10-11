import sys
from dist.PyTestique import PyTestique


def setup_foo() -> None:
    print("setup foo!")


def test_foo() -> None:
    print("test foo!")


def teardown_foo() -> None:
    print("teardown foo!")


def setup_bar() -> None:
    print("setup bar!")


def test_bar() -> None:
    print("test bar!")


def teardown_bar() -> None:
    print("teardown bar!")


PyTestique(sys.argv, globals())
