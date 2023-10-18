import time
from typing import Optional, Callable, Type, Union, Pattern


class PyTestiqueAsserts:
    @staticmethod
    def assertEqual(a: any, b: any) -> None:
        assert a == b

    @staticmethod
    def assertNotEqual(a: any, b: any) -> None:
        assert a != b

    @staticmethod
    def assertTrue(x: Union[bool, any]) -> None:
        assert bool(x) is True

    @staticmethod
    def assertFalse(x: Union[bool, any]) -> None:
        assert bool(x) is False

    @staticmethod
    def assertIs(a: any, b: any) -> None:
        assert a is b

    @staticmethod
    def assertIsNot(a: any, b: any) -> None:
        assert a is not b

    @staticmethod
    def assertIsNone(x: any) -> None:
        assert x is None

    @staticmethod
    def assertIsNotNone(x: any) -> None:
        assert x is not None

    @staticmethod
    def assertIn(a: any, b: any) -> None:
        assert a in b

    @staticmethod
    def assertNotIn(a: any, b: any) -> None:
        assert a not in b

    @staticmethod
    def assertIsInstance(a: any, b: Type) -> None:
        assert isinstance(a, b)

    @staticmethod
    def assertNotIsInstance(a: any, b: Type) -> None:
        assert not isinstance(a, b)

    @staticmethod
    def assertRaises(
        exc: Type[Exception], fun: Callable, args: tuple[any], *kwds: any
    ) -> None:
        try:
            fun(*args, **kwds)
        except exc:
            assert True
        else:
            raise AssertionError

    @staticmethod
    def assertAlmostEqual(a: float, b: float, afterComma: int = 7) -> None:
        assert round(a - b, afterComma) == 0

    @staticmethod
    def assertNotAlmostEqual(a: float, b: float, afterComma: int = 7) -> None:
        assert round(a - b, afterComma) != 0

    @staticmethod
    def assertGreater(a: any, b: any) -> None:
        assert a > b

    @staticmethod
    def assertGreaterEqual(a: any, b: any) -> None:
        assert a >= b

    @staticmethod
    def assertLess(a: any, b: any) -> None:
        assert a < b

    @staticmethod
    def assertLessEqual(a: any, b: any) -> None:
        assert a <= b

    @staticmethod
    def assertRegexpMatches(s: str, r: Pattern) -> None:
        assert r.search(s)

    @staticmethod
    def assertNotRegexpMatches(s: str, r: Pattern) -> None:
        assert not r.search(s)

    @staticmethod
    def assertItemsEqual(a: list[any], b: list[any]) -> None:
        assert sorted(a) == sorted(b)


class PyTestiqueUtils:
    green: str = "\033[92m"
    yellow: str = "\033[93m"
    red: str = "\033[91m"
    resetColor: str = "\033[0m"

    @staticmethod
    def timeFormat(nanoSeconds: Optional[int]) -> str:
        return f"{((nanoSeconds or 0) / 1_000_000):.3f} ms"

    @staticmethod
    def countPercent(value: Optional[int], total: Optional[int]) -> str:
        return f"{(((value or 0) / (total or 1)) * 100):.0f}%"

    @staticmethod
    def stateColor(state: Optional[str]) -> str:
        if state == "pass":
            return PyTestiqueUtils.green
        if state == "fail":
            return PyTestiqueUtils.yellow
        if "error" in state:
            return PyTestiqueUtils.red
        return PyTestiqueUtils.resetColor

    @staticmethod
    def stateSymbol(state: Optional[str]) -> str:
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
        self.__times: dict[str, int] = {}

    def timeStart(self, name: str) -> None:
        self.__times[name] = time.time_ns()

    def timeStop(self, name: str) -> Optional[int]:
        if name in self.__times:
            previous: int = self.__times[name]
            self.timeDelete(name)
            return time.time_ns() - previous
        return None

    def timeDelete(self, name: str) -> None:
        del self.__times[name]


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

    @property
    def errors(self) -> list[BaseException]:
        return self.__errors

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
        # "pass" | "fail" | "setup-error" | "test-error" | "teardown-error" | "test-teardown-error"
        self.__state: Optional[str] = None
        self.__durationSetup: Optional[int] = None
        self.__durationTest: Optional[int] = None
        self.__durationTeardown: Optional[int] = None
        self.__errors: list[BaseException] = []

    def execute(self) -> None:
        if self.state is not None:
            return
        if self.__executeSetup():
            self.__executeTest()
            self.__executeTeardown()

    def __executeSetup(self) -> bool:
        timeName: str = f"{self.name}-setup"
        try:
            if self.__setup:
                self.__analytics.timeStart(timeName)
                self.__setup()
                self.__durationSetup = self.__analytics.timeStop(timeName)
            return True
        except BaseException as error:
            self.__durationSetup = self.__analytics.timeStop(timeName)
            self.__registerError(error)
            self.__updateState("setup-error")
            return False

    def __executeTest(self) -> None:
        timeName: str = f"{self.name}-test"
        try:
            self.__analytics.timeStart(timeName)
            self.__test()
            self.__durationTest = self.__analytics.timeStop(timeName)
            self.__updateState("pass")
        except AssertionError:
            self.__durationTest = self.__analytics.timeStop(timeName)
            self.__updateState("fail")
        except BaseException as error:
            self.__durationTest = self.__analytics.timeStop(timeName)
            self.__registerError(error)
            self.__updateState("test-error")

    def __executeTeardown(self) -> None:
        timeName: str = f"{self.name}-teardown"
        try:
            if self.__teardown:
                self.__analytics.timeStart(timeName)
                self.__teardown()
                self.__durationTeardown = self.__analytics.timeStop(timeName)
        except BaseException as error:
            self.__durationTeardown = self.__analytics.timeStop(timeName)
            self.__registerError(error)
            if self.state == "test-error":
                self.__updateState("test-teardown-error")
            else:
                self.__updateState("teardown-error")

    def __updateState(self, state: str) -> None:
        self.__state = state

    def __registerError(self, error: BaseException) -> None:
        self.__errors.append(error)


class PyTestiqueOutput:
    @staticmethod
    def intro(
        totalCount: int,
        ranCount: int,
        pattern: str,
        durationRegister: int,
        durationExecutioner: int,
    ) -> str:
        withoutPattern: str = "with no pattern"
        withPattern: str = f"with pattern '{pattern}'"
        return (
            f"\n"
            f"--------------------------------------\n"
            f"Registered {totalCount} tests in {PyTestiqueUtils.timeFormat(durationRegister)}\n"
            f"Matched {ranCount} tests {withoutPattern if pattern is None else withPattern}\n"
            f"Ran {ranCount} tests in {PyTestiqueUtils.timeFormat(durationExecutioner)}\n"
            f"--------------------------------------"
        )

    @staticmethod
    def test(name: str, test: PyTestiqueTest) -> str:
        seperator: str = ", "
        times: list[Optional[str]] = [
            PyTestiqueOutput.__testTime("setup", test.durationSetup),
            PyTestiqueOutput.__testTime("test", test.durationTest),
            PyTestiqueOutput.__testTime("teardown", test.durationTeardown),
        ]
        return (
            f"{PyTestiqueUtils.stateColor(test.state)}"
            f"{PyTestiqueUtils.stateSymbol(test.state)} {test.state} '{name}' ("
            f"{seperator.join([time for time in times if time is not None])})"
            f"{PyTestiqueUtils.resetColor}"
        )

    @staticmethod
    def outro(
        ranCount: int,
        passCount: int,
        failCount: int,
        errorCount: int,
        errors: dict[BaseException, str],
    ) -> str:
        def countPercent(count: int) -> str:
            return PyTestiqueUtils.countPercent(count, ranCount)

        return (
            f"--------------------------------------\n"
            f"{passCount} pass ({countPercent(passCount)}), "
            f"{failCount} fail ({countPercent(failCount)}), "
            f"{errorCount} error ({countPercent(errorCount)})\n"
            f"{PyTestiqueOutput.__errors(errors) if len(errors) > 0 else ''}"
            f"======================================\n"
        )

    @staticmethod
    def __testTime(description: str, duration: Optional[int]) -> Optional[str]:
        return (
            f"{description} {PyTestiqueUtils.timeFormat(duration)}"
            if duration is not None
            else None
        )

    @staticmethod
    def __errors(errors: dict[BaseException, str]) -> str:
        linebreak: str = "\n"
        return (
            f"--------------------------------------\n"
            f"{linebreak.join([PyTestiqueOutput.__error(errors[e], e) for e in errors])}\n"
        )

    @staticmethod
    def __error(name: str, error: BaseException) -> str:
        return f"'{type(error).__name__}' in test '{name}': '{error}'"


class PyTestique:
    def __init__(self, cliArgs: list[str], globalContext: dict[str, any]) -> None:
        self.__analytics: PyTestiqueAnalytics = PyTestiqueAnalytics()
        self.__pattern: Optional[str] = self.__processPattern(cliArgs)
        self.__tests: dict[str, PyTestiqueTest] = {}
        self.__durationRegister: Optional[int] = None
        self.__durationExecutioner: Optional[int] = None
        self.__errors: dict[BaseException, str] = {}
        self.__register(globalContext)
        self.__executioner()
        self.__outputer()

    def __processPattern(self, cliArgs: list[str]) -> Optional[str]:
        if "--select" not in cliArgs:
            return None
        selectIndex: int = cliArgs.index("--select")
        if selectIndex is len(cliArgs) - 1:
            return None
        return cliArgs[selectIndex + 1]

    def __register(self, globalContext: dict[str, any]) -> None:
        self.__analytics.timeStart("register")
        for name in globalContext:
            if not name.startswith("test_"):
                continue
            self.__registerTest(name[5:], globalContext)
        self.__durationRegister = self.__analytics.timeStop("register")

    def __registerTest(self, name: str, globalContext: dict[str, any]) -> None:
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
            for error in self.__tests[name].errors:
                self.__errors[error] = name
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
        setupCount: int = self.__count("setup-error")
        testCount: int = self.__count("test-error")
        teardownCount: int = self.__count("teardown-error")
        testTeardownCount: int = self.__count("test-teardown-error")
        errorCount: int = sum((setupCount, testCount, teardownCount, testTeardownCount))
        ranCount: int = sum((passCount, failCount, errorCount))
        self.__outputerIntro(ranCount)
        for name in self.__tests:
            if self.__tests[name].state is None:
                continue
            self.__outputerTest(name)
        self.__outputerOutro(
            ranCount,
            passCount,
            failCount,
            errorCount,
            self.__errors,
        )

    def __outputerIntro(self, ranCount: int) -> None:
        PyTestiqueUtils.print(
            PyTestiqueOutput.intro(
                len(self.__tests),
                ranCount,
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
        errorCount: int,
        errors: dict[BaseException, str],
    ) -> None:
        PyTestiqueUtils.print(
            PyTestiqueOutput.outro(
                ranCount,
                passCount,
                failCount,
                errorCount,
                errors,
            )
        )
