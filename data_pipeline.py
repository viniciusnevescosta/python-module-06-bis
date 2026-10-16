from typing import Any, Protocol

from data_processor import (
    LogProcessor,
    NumericProcessor,
    TextProcessor,
)
from data_stream import DataStream as BaseDataStream


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        fields = []
        for _, value in data:
            if any(character in value for character in (',', '"', '\n', '\r')):
                value = '"' + value.replace('"', '""') + '"'
            fields.append(value)
        print(",".join(fields))


class JSONExportPlugin:
    @staticmethod
    def _escape(value: str) -> str:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        for code in range(32):
            escaped = escaped.replace(chr(code), f"\\u{code:04x}")
        return escaped

    def process_output(self, data: list[tuple[int, str]]) -> None:
        fields = [f'"item_{rank}": "{self._escape(value)}"'
                  for rank, value in data]
        print("JSON Output:")
        print("{" + ", ".join(fields) + "}")


class DataStream(BaseDataStream):
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for processor in self._processors:
            output: list[tuple[int, str]] = []
            for _ in range(nb):
                try:
                    output.append(processor.output())
                except IndexError:
                    break
            plugin.process_output(output)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("\nInitialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()
    numeric = NumericProcessor()
    text = TextProcessor()
    logs = LogProcessor()
    for processor in (numeric, text, logs):
        stream.register_processor(processor)

    first_batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING", "log_message": "Use ssh instead"},
            {"log_level": "INFO", "log_message": "User connected"},
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"\nSend first batch of data on stream: {first_batch}\n")
    stream.process_stream(first_batch)
    stream.print_processors_stats()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    print()
    stream.print_processors_stats()

    second_batch: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE", "log_message": "Certificate expiring"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {second_batch}\n")
    stream.process_stream(second_batch)
    stream.print_processors_stats()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
