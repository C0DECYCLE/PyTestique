import time
from typing import List, Dict, Optional, Callable, Any, Type, Union, Pattern


class PyTestiqueAsserts:
    @staticmethod
    def assertEqual(a: Any, b: Any):
        assert a == b

    @staticmethod
    def assertNotEqual(a: Any, b: Any):
        assert a != b

    @staticmethod
    def assertTrue(x: Union[bool, Any]):
        assert bool(x) is True

    @staticmethod
    def assertFalse(x: Union[bool, Any]):
        assert bool(x) is False

    @staticmethod
    def assertIs(a: Any, b: Any):
        assert a is b

    @staticmethod
    def assertIsNot(a: Any, b: Any):
        assert a is not b

    @staticmethod
    def assertIsNone(x: Any):
        assert x is None

    @staticmethod
    def assertIsNotNone(x: Any):
        assert x is not None

    @staticmethod
    def assertIn(a: Any, b: Any):
        assert a in b

    @staticmethod
    def assertNotIn(a: Any, b: Any):
        assert a not in b

    @staticmethod
    def assertIsInstance(a: Any, b: Type):
        assert isinstance(a, b)

    @staticmethod
    def assertNotIsInstance(a: Any, b: Type):
        assert not isinstance(a, b)

    @staticmethod
    def assertRaises(exc: Type[Exception], fun: Callable, args: tuple, *kwds: Any):
        try:
            fun(*args, **kwds)
        except exc:
            assert True
        else:
            raise AssertionError

    @staticmethod
    def assertAlmostEqual(a: float, b: float, afterComma: int = 7):
        assert round(a - b, afterComma) == 0

    @staticmethod
    def assertNotAlmostEqual(a: float, b: float, afterComma: int = 7):
        assert round(a - b, afterComma) != 0

    @staticmethod
    def assertGreater(a: Any, b: Any):
        assert a > b

    @staticmethod
    def assertGreaterEqual(a: Any, b: Any):
        assert a >= b

    @staticmethod
    def assertLess(a: Any, b: Any):
        assert a < b

    @staticmethod
    def assertLessEqual(a: Any, b: Any):
        assert a <= b

    @staticmethod
    def assertRegexpMatches(s: str, r: Pattern):
        assert r.search(s)

    @staticmethod
    def assertNotRegexpMatches(s: str, r: Pattern):
        assert not r.search(s)

    @staticmethod
    def assertItemsEqual(a: list, b: list):
        assert sorted(a) == sorted(b)


class PyTestiqueUtils:
    green: str = "\033[92m"
    yellow: str = "\033[93m"
    red: str = "\033[91m"
    resetColor: str = "\033[0m"

    @staticmethod
    def timeFormat(duration: int) -> str:
        return f"{(duration * 0.000001):.3f} ms"

    @staticmethod
    def countPercent(value: int, total: int) -> str:
        return f"{((value / total) * 100):.0f}%"

    @staticmethod
    def stateColor(state: str) -> str:
        if state == "pass":
            return PyTestiqueUtils.green
        if state == "fail":
            return PyTestiqueUtils.yellow
        if "error" in state:
            return PyTestiqueUtils.red
        return PyTestiqueUtils.resetColor

    @staticmethod
    def stateSymbol(state: str) -> str:
        if state == "pass":
            return "|"
        if state == "fail":
            return "-"
        if "error" in state:
            return "x"
        return "?"

    @staticmethod
    def print(content: str) -> None:
        print(content)


class PyTestiqueAnalytics:
    def __init__(self) -> None:
        self.__times: Dict[str, int] = {}

    def timeStart(self, name: str) -> None:
        self.__times[name] = time.time_ns()

    def timeStop(self, name: str) -> Optional[int]:
        if name in self.__times:
            return time.time_ns() - self.__times[name]
        return None


class PyTestiqueTest:
    @property
    def name(self) -> str:
        return self.__name

    @property
    def state(self) -> Optional[str]:
        return self.__state

    @property
    def durationSetup(self) -> Optional[int]:
        return self.__durationSetup

    @property
    def durationTest(self) -> Optional[int]:
        return self.__durationTest

    @property
    def durationTeardown(self) -> Optional[int]:
        return self.__durationTeardown

    def __init__(
        self,
        analytics: PyTestiqueAnalytics,
        name: str,
        test: Callable[[], None],
        setup: Callable[[], None] = None,
        teardown: Callable[[], None] = None,
    ) -> None:
        self.__analytics: PyTestiqueAnalytics = analytics
        self.__name: str = name
        self.__test: Callable[[], None] = test
        self.__setup: Optional[Callable[[], None]] = setup
        self.__teardown: Optional[Callable[[], None]] = teardown
        # "pass" | "fail" | "setup-error" | "test-error" | "teardown-error"
        self.__state: Optional[str] = None
        self.__durationSetup: Optional[int] = None
        self.__durationTest: Optional[int] = None
        self.__durationTeardown: Optional[int] = None

    def execute(self) -> None:
        if self.state is not None:
            return
        self.__analytics.timeStart(f"{self.name}-setup")
        succesfullSetup: bool = self.__executeSetup()
        self.__durationSetup = self.__analytics.timeStop(f"{self.name}-setup")
        if succesfullSetup:
            self.__analytics.timeStart(f"{self.name}-test")
            self.__executeTest()
            self.__durationTest = self.__analytics.timeStop(f"{self.name}-test")
            self.__analytics.timeStart(f"{self.name}-teardown")
            self.__executeTeardown()
            self.__durationTeardown = self.__analytics.timeStop(f"{self.name}-teardown")

    def __executeSetup(self) -> bool:
        try:
            if self.__setup:
                self.__setup()
            return True
        except:
            self.__updateState("setup-error")
            return False

    def __executeTest(self) -> None:
        try:
            self.__test()
            self.__updateState("pass")
        except AssertionError:
            self.__updateState("fail")
        except:
            self.__updateState("test-error")

    def __executeTeardown(self) -> None:
        try:
            if self.__teardown:
                self.__teardown()
        except:
            self.__updateState("teardown-error")

    def __updateState(self, state: str) -> None:
        self.__state = state


class PyTestiqueOutput:
    @staticmethod
    def intro(
        ranCount: int,
        totalCount: int,
        pattern: str,
        durationRegister: int,
        durationExecutioner: int,
    ) -> str:
        return (
            f"\n"
            f"Registered {totalCount} tests in {PyTestiqueUtils.timeFormat(durationRegister)}\n"
            f"Matched {ranCount} with pattern '{pattern}'\n"
            f"Ran {ranCount} tests in {PyTestiqueUtils.timeFormat(durationExecutioner)}\n"
            f"--------------------------------------"
        )

    @staticmethod
    def test(name: str, test: PyTestiqueTest) -> str:
        return (
            f"{PyTestiqueUtils.stateColor(test.state)}"
            f"{PyTestiqueUtils.stateSymbol(test.state)} {test.state} '{name}' ("
            f"setup {PyTestiqueUtils.timeFormat(test.durationSetup)}, "
            f"test {PyTestiqueUtils.timeFormat(test.durationTest)}, "
            f"teardown {PyTestiqueUtils.timeFormat(test.durationTeardown)})"
            f"{PyTestiqueUtils.resetColor}"
        )

    @staticmethod
    def outro(
        ranCount: int,
        passCount: int,
        failCount: int,
        setupErrorCount: int,
        testErrorCount: int,
        teardownErrorCount: int,
    ) -> str:
        return (
            f"--------------------------------------\n"
            f"{passCount} pass ({PyTestiqueUtils.countPercent(passCount, ranCount)}), "
            f"{failCount} fail ({PyTestiqueUtils.countPercent(failCount, ranCount)}), "
            f"{setupErrorCount} setup error ({PyTestiqueUtils.countPercent(setupErrorCount, ranCount)}), "
            f"{testErrorCount} test error ({PyTestiqueUtils.countPercent(testErrorCount, ranCount)}), "
            f"{teardownErrorCount} teardown error ({PyTestiqueUtils.countPercent(teardownErrorCount, ranCount)})\n"
            f"======================================\n"
        )


class PyTestique:
    def __init__(self, cliArgs: List[str], globalContext: Dict[str, any]) -> None:
        self.__analytics: PyTestiqueAnalytics = PyTestiqueAnalytics()
        self.__pattern: Optional[str] = self.__processPattern(cliArgs)
        self.__tests: Dict[str, PyTestiqueTest] = {}
        self.__durationRegister: Optional[int] = None
        self.__durationExecutioner: Optional[int] = None
        self.__register(globalContext)
        self.__executioner()
        self.__outputer()

    def __processPattern(self, cliArgs: List[str]) -> Optional[str]:
        if not "--select" in cliArgs:
            return None
        selectIndex: int = cliArgs.index("--select")
        if selectIndex is len(cliArgs) - 1:
            return None
        return cliArgs[selectIndex + 1]

    def __register(self, globalContext: Dict[str, any]) -> None:
        self.__analytics.timeStart("register")
        for name in globalContext:
            if not name.startswith("test_"):
                continue
            self.__registerTest(name[5:], globalContext)
        self.__durationRegister = self.__analytics.timeStop("register")

    def __registerTest(self, name: str, globalContext: Dict[str, any]) -> None:
        self.__tests[name] = PyTestiqueTest(
            self.__analytics,
            name,
            globalContext.get(f"test_{name}"),
            globalContext.get(f"setup_{name}"),
            globalContext.get(f"teardown_{name}"),
        )

    def __executioner(self) -> None:
        self.__analytics.timeStart("executioner")
        for name in self.__tests:
            if self.__pattern is not None and self.__pattern not in name:
                continue
            self.__tests[name].execute()
        self.__durationExecutioner = self.__analytics.timeStop("executioner")

    def __count(self, state: Optional[str]) -> int:
        count: int = 0
        for name in self.__tests:
            if self.__tests[name].state is not state:
                continue
            count += 1
        return count

    def __outputer(self) -> None:
        passCount: int = self.__count("pass")
        failCount: int = self.__count("fail")
        setupErrorCount: int = self.__count("setup-error")
        testErrorCount: int = self.__count("test-error")
        teardownErrorCount: int = self.__count("teardown-error")
        ranCount: int = sum(
            (passCount, failCount, setupErrorCount, testErrorCount, teardownErrorCount)
        )
        self.__outputerIntro(ranCount)
        for name in self.__tests:
            if self.__tests[name].state is None:
                continue
            self.__outputerTest(name)
        self.__outputerOutro(
            ranCount,
            passCount,
            failCount,
            setupErrorCount,
            testErrorCount,
            teardownErrorCount,
        )

    def __outputerIntro(self, ranCount: int) -> None:
        PyTestiqueUtils.print(
            PyTestiqueOutput.intro(
                ranCount,
                len(self.__tests),
                self.__pattern,
                self.__durationRegister,
                self.__durationExecutioner,
            )
        )

    def __outputerTest(self, name: str) -> None:
        PyTestiqueUtils.print(PyTestiqueOutput.test(name, self.__tests[name]))

    def __outputerOutro(
        self,
        ranCount: int,
        passCount: int,
        failCount: int,
        setupErrorCount: int,
        testErrorCount: int,
        teardownErrorCount: int,
    ) -> None:
        PyTestiqueUtils.print(
            PyTestiqueOutput.outro(
                ranCount,
                passCount,
                failCount,
                setupErrorCount,
                testErrorCount,
                teardownErrorCount,
            )
        )
