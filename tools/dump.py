from pathlib import Path
import json
import os

class Dumper:
    def __init__(self, topics_dir: Path = "topics", resp_dir: Path = "responses"):
        self.topics_dir = Path(topics_dir)
        self.resp_dir = Path(resp_dir)


    def _get_next_response_number(self, topic_dir: Path) -> int:
        # Получаем все файлы в директории топика
        if not topic_dir.exists():
            return 1
        
        # Ищем все .md файлы с числовыми именами
        existing_files = list(topic_dir.glob("*.md"))
        if not existing_files:
            return 1
        
        # Извлекаем номера из имен файлов
        numbers = []
        for f in existing_files:
            try:
                # Убираем расширение и пробуем преобразовать в число
                num = int(f.stem)
                numbers.append(num)
            except ValueError:
                # Если имя файла не число, пропускаем
                continue
        
        # Возвращаем следующий номер после максимального
        return max(numbers) + 1 if numbers else 1

    def dump_json(self, topic_name: str, msg: str):
        if topic_name != "":
            filename = self.topics_dir / f"{topic_name}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(msg, f, ensure_ascii=False, indent=2)

    def dump_md(self, topic_name: str, content: str) -> Path:
        if topic_name != "":
            # Создаем папку для топика
            topic_dir = self.resp_dir / topic_name
            topic_dir.mkdir(parents=True, exist_ok=True)
            
            # Получаем следующий номер для файла
            next_num = self._get_next_response_number(topic_dir)
            filename = topic_dir / f"{next_num:03d}.md"
        else:
            # Для сообщений без топика создаем папку "general"
            general_dir = self.resp_dir / "general"
            general_dir.mkdir(parents=True, exist_ok=True)
            
            next_num = self._get_next_response_number(general_dir)
            filename = general_dir / f"{next_num:03d}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content.strip())
        return filename


if __name__ == "__main__":
    dumper_agent = Dumper()

    dumper_agent.dump_md("test", "dummy text")
    dumper_agent.dump_md("test", "dummy text1")
    dumper_agent.dump_md("test", "dummy text2")

    dumper_agent.dump_json("test", "dummy text")