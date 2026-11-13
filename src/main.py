import sys
import yaml


def load_config(path: str) -> dict:
  try:
    with open(path, "r", encoding="utf-8") as f:
      config = yaml.safe_load(f)
      if not isinstance(config, dict):
        raise ValueError("Конфигурационный файл должен содержать словарь.")
      return config
  except FileNotFoundError:
    print(f"Ошибка: Файл конфигурации '{path}' не найден.", file=sys.stderr)
    sys.exit(1)
  except yaml.YAMLError as e:
    print(
        f"Ошибка: Невалидный формат YAML в файле '{path}': {e}", file=sys.stderr
    )
    sys.exit(1)
  except Exception as e:
    print(f"Непредвиденная ошибка при чтении конфига: {e}", file=sys.stderr)
    sys.exit(1)


def validate_parameters(config: dict) -> None:
  required_keys = [
      "package_name",
      "repository_url",
      "test_mode",
      "package_version",
      "output_image",
      "ascii_tree",
      "max_depth",
  ]

  for key in required_keys:
    if key not in config:
      raise ValueError(f"Отсутствует обязательный параметр: '{key}'")


def main():
  if len(sys.argv) < 2:
    print(
        "Использование: python src/main.py <path_to_config.yaml>",
        file=sys.stderr,
    )
    sys.exit(1)

  config_path = sys.argv[1]
  config = load_config(config_path)

  try:
    validate_parameters(config)
  except ValueError as e:
    print(f"Ошибка конфигурации: {e}", file=sys.stderr)
    sys.exit(1)

  print("=== Параметры конфигурации (Этап 1) ===")
  for key, value in config.items():
    print(f"{key}: {value}")


if __name__ == "__main__":
  main()