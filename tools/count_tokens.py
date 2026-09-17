import tiktoken
import argparse

def count_tokens(text: str, model_name: str = "gpt-4o") -> int:
    """Возвращает количество токенов в строке текста для указанной модели."""
    try:
        # Автоматически подбирает кодировку (tokenizer) для конкретной модели
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Если модель новая или не найдена, используем стандартную кодировку o200k (для GPT-4o)
        print(f"Модель '{model_name}' не найдена. Используется стандартная кодировка o200k.")
        encoding = tiktoken.get_encoding("o200k")

    # Кодируем текст в токены и считаем их количество
    token_list = encoding.encode(text)
    return len(token_list)

# --- Пример использования ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Text token counter")
    parser.add_argument("-f", type=str, help="File name")
    parser.add_argument("-m", type=str, default="gpt-4o", help="Model")
    args = parser.parse_args()


    with open(args.f, 'r', encoding='utf-8') as f:
        text = f.read()
    sample_text = text
    model = args.m

    num_tokens = count_tokens(sample_text, model_name=model)

    # print(f"Текст: '{sample_text}'")
    print(f"Модель: {model}")
    print(f"Количество токенов: {num_tokens}")
