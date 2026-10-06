from abc import ABC, abstractmethod
from typing import Any, Union


Number = Union[int, float]
NumericData = Union[Number, list[Number]]
TextData = Union[str, list[str]]
LogEntry = dict[str, str]
LogData = Union[LogEntry, list[LogEntry]]


class DataProcessor(ABC):
    def __init__(self, name: str) -> None:
        self.name = name
        self._data: list[tuple[int, str]] = []
        self._total_processed = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def _store(self, value: str) -> None:
        rank = self._total_processed
        self._data.append((rank, value))
        self._total_processed += 1

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError(f"No data available in {self.name}")
        return self._data.pop(0)

    def total_processed(self) -> int:
        return self._total_processed

    def remaining(self) -> int:
        return len(self._data)


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if type(data) in (int, float):
            return True
        if type(data) is list:
            return bool(data) and all(
                type(item) in (int, float) for item in data
            )
        return False

    def ingest(self, data: NumericData) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self._store(str(value))


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if type(data) is list:
            return bool(data) and all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: TextData) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self._store(value)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")

    def _valid_entry(self, data: Any) -> bool:
        return (
            type(data) is dict
            and isinstance(data.get("log_level"), str)
            and isinstance(data.get("log_message"), str)
        )

    def validate(self, data: Any) -> bool:
        if self._valid_entry(data):
            return True
        if type(data) is list:
            return bool(data) and all(self._valid_entry(item) for item in data)
        return False

    def ingest(self, data: LogData) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self._store(f"{value['log_level']}: {value['log_message']}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===")
    numeric = NumericProcessor()
    print("\nTesting Numeric Processor...")
    print(f" Trying to validate input '42': {numeric.validate(42)}")
    print(f" Trying to validate input 'Hello': {numeric.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except TypeError as error:
        print(f" Got exception: {error}")
    numbers: list[Number] = [1, 2, 3, 4, 5]
    print(f" Processing data: {numbers}")
    numeric.ingest(numbers)
    print(" Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f" Numeric value {rank}: {value}")

    text = TextProcessor()
    print("\nTesting Text Processor...")
    print(f" Trying to validate input '42': {text.validate(42)}")
    words = ["Hello", "Nexus", "World"]
    print(f" Processing data: {words}")
    text.ingest(words)
    print(" Extracting 1 value...")
    rank, value = text.output()
    print(f" Text value {rank}: {value}")

    logs = LogProcessor()
    entries = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print("\nTesting Log Processor...")
    print(f" Trying to validate input 'Hello': {logs.validate('Hello')}")
    print(f" Processing data: {entries}")
    logs.ingest(entries)
    print(" Extracting 2 values...")
    for _ in range(2):
        rank, value = logs.output()
        print(f" Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
