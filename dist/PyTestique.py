import time
from typing import List, Dict, Optional, Callable


class PyTestiqueAnalytics:
    __times: Dict[str, int]

    def __init__(self) -> None:
        self.__times = {}

    def timeStart(self, name: str) -> None:
        self.__times[name] = time.time_ns()

    def timeStop(self, name: str) -> Optional[int]:
        if name in self.__times:
            return time.time_ns() - self.__times[name]
        return None

    @staticmethod
    def timeFormat(duration: int):
        return f"{duration * 0.000001} ms"


class PyTestiqueTest:
    __analytics: PyTestiqueAnalytics
    __name: str
    __setup: Callable[[], None]
    __test: Callable[[], None]
    __teardown: Callable[[], None]
    # "pass" | "fail" | "setup-error" | "test-error" | "teardown-error"
    __state: Optional[str]
    __durationSetup: Optional[int]
    __durationTest: Optional[int]
    __durationTeardown: Optional[int]

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
        self.__analytics = analytics
        self.__name = name
        self.__test = test
        self.__setup = setup
        self.__teardown = teardown
        self.__state = None
        self.__durationSetup = None
        self.__durationTest = None
        self.__durationTeardown = None

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


class PyTestique:
    __analytics: PyTestiqueAnalytics
    __pattern: Optional[str]
    __tests: Dict[str, PyTestiqueTest]
    __durationRegister: Optional[int]
    __durationExecutioner: Optional[int]

    def __init__(self, cliArgs: List[str], globalContext: Dict[str, any]) -> None:
        self.__analytics = PyTestiqueAnalytics()
        self.__pattern = self.__processPattern(cliArgs)
        self.__tests = {}
        self.__durationRegister = None
        self.__durationExecutioner = None
        self.__register(globalContext)
        self.__executioner()

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

    def __executioner(self):
        self.__analytics.timeStart("executioner")
        for name in self.__tests:
            if self.__pattern is not None and self.__pattern not in name:
                continue
            self.__tests[name].execute()
        self.__durationExecutioner = self.__analytics.timeStop("executioner")
