from pathlib import Path
import json
import os

class Dumper:
    def __init__(self, topics_dir: Path = "topics", resp_dir: Path = "responses"):
        self.topics_dir = Path(topics_dir)
        self.resp_dir = Path(resp_dir)


    def _get_unique_filename(self, filepath: Path) -> Path:
        # Если файла нет, возвращаем путь как есть
        if not os.path.exists(filepath):
            return filepath

        # Разделяем путь на директорию/имя и расширение
        # Пример: 'C:/docs/report.txt' -> ('C:/docs/report', '.txt')
        base, extension = os.path.splitext(filepath)

        counter = 1
        # Цикл работает, пока файл с таким именем существует
        while os.path.exists(f"{base}({counter}){extension}"):
            counter += 1

        # Возвращаем уникальный путь с номером
        return f"{base}({counter}){extension}"

    def dump_json(self, topic_name: str, msg: str):
        if topic_name != "":
            filename = self.topics_dir / f"{topic_name}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(msg, f, ensure_ascii=False, indent=2)

    def dump_md(self, topic_name: str, content: str) -> Path:
        if topic_name != "":
            original_filename = f"{topic_name}.md"
        else:
            original_filename = "ans.md"
        unique_name = self._get_unique_filename(self.resp_dir / original_filename)

        ufilename = unique_name
        with open(ufilename, "w", encoding="utf-8") as f:
            f.write(content.strip())
        return ufilename


if __name__ == "__main__":
    dumper_agent = Dumper()

    dumper_agent.dump_md("test", "dummy text")
    dumper_agent.dump_md("test", "dummy text1")
    dumper_agent.dump_md("test", "dummy text2")

    dumper_agent.dump_json("test", "dummy text")