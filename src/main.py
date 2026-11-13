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


def load_test_graph(file_path: str) -> dict:
    graph = {}
    try:
        with open(f"tests/{file_path}", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                pkg = parts[0].strip()
                deps = []
                if len(parts) > 1 and parts[1].strip():
                    deps = [d.strip() for d in parts[1].split()]
                graph[pkg] = deps
        return graph
    except FileNotFoundError:
        print(f"Ошибка: Тестовый файл графа '{file_path}' не найден.", file=sys.stderr)
        sys.exit(1)


def fetch_dependencies(pkg: str, repo_url: str, test_mode: bool) -> list:
    if test_mode:
        graph = load_test_graph(repo_url)
        return graph.get(pkg, [])
    else:
        mock_dependencies = {
            "requests": ["libc6", "python3-urllib3"],
            "libc6": [],
            "python3-urllib3": [],
        }
        return mock_dependencies.get(pkg, [])


def build_graph_bfs_recursive(
        current_level_nodes: list,
        repo_url: str,
        test_mode: bool,
        max_depth: int,
        current_depth: int,
        visited: set,
        full_graph: dict,
) -> dict:
    if current_depth > max_depth or not current_level_nodes:
        return full_graph

    next_level_nodes = []
    for pkg in current_level_nodes:
        if pkg not in visited:
            visited.add(pkg)
            deps = fetch_dependencies(pkg, repo_url, test_mode)
            full_graph[pkg] = deps
            for dep in deps:
                if dep not in visited and dep not in next_level_nodes:
                    next_level_nodes.append(dep)

    if next_level_nodes:
        build_graph_bfs_recursive(
            next_level_nodes,
            repo_url,
            test_mode,
            max_depth,
            current_depth + 1,
            visited,
            full_graph,
        )

    return full_graph


def compute_reverse_dependencies(graph: dict) -> dict:
    reverse_graph = {}
    for pkg, deps in graph.items():
        if pkg not in reverse_graph:
            reverse_graph[pkg] = []
        for dep in deps:
            if dep not in reverse_graph:
                reverse_graph[dep] = []
            if pkg not in reverse_graph[dep]:
                reverse_graph[dep].append(pkg)
    return reverse_graph


def print_ascii_tree(pkg: str, graph: dict, prefix: str = "", visited: set = None):
    if visited is None:
        visited = set()
    print(f"{prefix}{pkg}")
    if pkg in visited:
        return
    visited.add(pkg)
    deps = graph.get(pkg, [])
    for i, dep in enumerate(deps):
        connector = "└── " if i == len(deps) - 1 else "├── "
        extension = "    " if i == len(deps) - 1 else "│   "
        print_ascii_tree(dep, graph, prefix + connector, visited.copy())


def main():
    if len(sys.argv) < 2:
        print(
            "Использование: python src/main.py <path_to_config.yaml>",
            file=sys.stderr,
        )
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)

    print("=== Параметры конфигурации ===")
    for key, value in config.items():
        print(f"{key}: {value}")

    pkg_name = config.get("package_name")
    repo_url = config.get("repository_url")
    test_mode = config.get("test_mode", False)
    max_depth = config.get("max_depth", 5)
    ascii_tree_enabled = config.get("ascii_tree", False)
    output_image = config.get("output_image", "graph.png")

    print(
        f"\n[Stage 3] Построение графа зависимостей для '{pkg_name}' (макс. глубина:"
        f" {max_depth})..."
    )

    dependency_graph = build_graph_bfs_recursive(
        [pkg_name], repo_url, test_mode, max_depth, 1, set(), {}
    )

    print(f"\n=== Граф прямых зависимостей [Этап 3] ===")
    for node, deps in dependency_graph.items():
        print(f"{node} -> {deps}")

    reverse_graph = compute_reverse_dependencies(dependency_graph)

    print(f"\n=== Граф обратных зависимостей [Этап 4] ===")
    for node, rev_deps in reverse_graph.items():
        print(f"{node} <- {rev_deps}")

    if ascii_tree_enabled:
        print(f"\n=== ASCII-дерево зависимостей [Этап 5] ===")
        print_ascii_tree(pkg_name, dependency_graph)
    else:
        print(f"\n[Этап 5] Визуализация: параметр ascii_tree выключен в config.yaml. Файл экспорта: {output_image}")


if __name__ == "__main__":
    main()