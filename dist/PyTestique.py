import time
from typing import List, Dict, Optional, Callable


class PyTestiqueAnalytics:
    __times: Dict[str, float]

    def __init__(self) -> None:
        self.__times = {}

    def timeStart(self, name: str) -> None:
        self.__times[name] = time.time()

    def timeStop(self, name: str) -> Optional[float]:
        if name in self.__times:
            return time.time() - self.__times[name]
        return None


class PyTestiqueTest:
    __name: str
    __setup: Callable[[], None]
    __test: Callable[[], None]
    __teardown: Callable[[], None]
    __state: Optional[
        str
    ]  # "pass" | "fail" | "setup-error" | "test-error" | "teardown-error"
    __duration: float

    def __init__(
        self,
        name: str,
        test: Callable[[], None],
        setup: Callable[[], None] = None,
        teardown: Callable[[], None] = None,
    ) -> None:
        self.__name = name
        self.__test = test
        self.__setup = setup
        self.__teardown = teardown
        self.__state = None
        self.__duration = 0.0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def state(
        self,
    ) -> Optional[
        str
    ]:  # "pass" | "fail" | "setup-error" | "test-error" | "teardown-error"
        return self.__state

    def execute(self) -> None:
        if self.__state != None:
            return
        if self.__executeSetup():
            self.__executeTest()
            self.__executeTeardown()

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
    analytics: PyTestiqueAnalytics

    def __init__(self, cliArgs: List[str], globalContext: Dict[str, any]) -> None:
        self.analytics = PyTestiqueAnalytics()