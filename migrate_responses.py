#!/usr/bin/env python3
"""
Скрипт для миграции responses из плоской структуры в иерархическую по темам
"""
from pathlib import Path
import shutil
import re

def parse_filename(filename: str) -> tuple[str, int]:
    """
    Парсит имя файла и возвращает (topic_name, number)
    Примеры:
        'airq.md' -> ('airq', 1)
        'airq(1).md' -> ('airq', 2)
        'airq(5).md' -> ('airq', 6)
    """
    stem = Path(filename).stem
    
    # Проверяем наличие номера в скобках
    match = re.match(r'^(.+?)\((\d+)\)$', stem)
    if match:
        topic = match.group(1)
        number = int(match.group(2)) + 1  # +1 потому что первый файл без номера
        return topic, number
    else:
        # Файл без номера - это первый файл темы
        return stem, 1


def migrate_responses(old_dir: Path, new_dir: Path, dry_run: bool = False):
    """
    Мигрирует файлы из плоской структуры в папки по темам
    """
    if not old_dir.exists():
        print(f"Папка {old_dir} не найдена")
        return
    
    # Получаем все .md файлы
    md_files = sorted(old_dir.glob("*.md"))
    
    print(f"Найдено {len(md_files)} файлов для миграции")
    
    if dry_run:
        print("\n=== DRY RUN MODE ===\n")
    
    # Группируем файлы по темам
    topics = {}
    for md_file in md_files:
        topic, number = parse_filename(md_file.name)
        if topic not in topics:
            topics[topic] = []
        topics[topic].append((number, md_file))
    
    # Создаем новую структуру
    for topic, files in topics.items():
        # Сортируем файлы по номерам
        files.sort(key=lambda x: x[0])
        
        # Создаем директорию для темы
        topic_dir = new_dir / topic
        
        if not dry_run:
            topic_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nТема: {topic} ({len(files)} файлов)")
        
        # Копируем файлы с новыми именами
        for idx, (old_num, old_file) in enumerate(files, start=1):
            new_filename = f"{idx:03d}.md"
            new_path = topic_dir / new_filename
            
            print(f"  {old_file.name} -> {topic}/{new_filename}")
            
            if not dry_run:
                shutil.copy2(old_file, new_path)
    
    if not dry_run:
        print(f"\n✓ Миграция завершена!")
        print(f"  Обработано тем: {len(topics)}")
        print(f"  Всего файлов: {len(md_files)}")
        print(f"\nСтарые файлы остались в {old_dir}")
        print(f"Новые файлы находятся в {new_dir}")
        print(f"\nПосле проверки можете удалить старые файлы:")
        print(f"  rm {old_dir}/*.md")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Миграция responses в новую структуру")
    parser.add_argument("--old-dir", type=Path, default="responses",
                        help="Путь к старой папке responses (по умолчанию: responses)")
    parser.add_argument("--new-dir", type=Path, default="responses_new",
                        help="Путь к новой папке responses (по умолчанию: responses_new)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать что будет сделано, без реальных изменений")
    parser.add_argument("--in-place", action="store_true",
                        help="Мигрировать прямо в responses (создаст backup)")
    
    args = parser.parse_args()
    
    old_dir = Path(args.old_dir)
    
    if args.in_place:
        # Создаем backup старых файлов
        backup_dir = Path("responses_backup")
        if not args.dry_run:
            print(f"Создание backup в {backup_dir}...")
            backup_dir.mkdir(exist_ok=True)
            for f in old_dir.glob("*.md"):
                shutil.copy2(f, backup_dir / f.name)
            print(f"✓ Backup создан")
        new_dir = old_dir
    else:
        new_dir = Path(args.new_dir)
    
    migrate_responses(old_dir, new_dir, args.dry_run)
