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


def fetch_apt_dependencies(package_name: str, version: str, repo_url: str) -> list:
  mock_dependencies = {
      "requests": ["libc6 (>= 2.17)", "python3-urllib3", "python3-charset-normalizer"],
      "default": ["libc6", "base-files"],
  }
  return mock_dependencies.get(package_name, ["libc6", "base-files"])


def main():
  if len(sys.argv) < 2:
    print(
        "Использование: python src/main.py <path_to_config.yaml>",
        file=sys.stderr,
    )
    sys.exit(1)

  config_path = sys.argv[1]
  config = load_config(config_path)

  print("=== Параметры конфигурации (Этап 1) ===")
  for key, value in config.items():
    print(f"{key}: {value}")

  pkg_name = config.get("package_name")
  pkg_version = config.get("package_version")
  repo_url = config.get("repository_url")

  direct_dependencies = fetch_apt_dependencies(pkg_name, pkg_version, repo_url)

  print(
      f"\n=== Прямые зависимости пакета {pkg_name} (версия {pkg_version}) [Этап"
      " 2] ==="
  )
  for dep in direct_dependencies:
    print(f" - {dep}")


if __name__ == "__main__":
  main()