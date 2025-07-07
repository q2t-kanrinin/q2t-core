import yaml

def load_fold_dsl(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

def print_section_tree(section: dict, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {section['name']} (ID: {section['id']}, tension: {section.get('tension',0)})")
    # 子要素がある場合は再帰
    for child in section.get("children", []):
        print_section_tree(child, level + 1)

if __name__ == "__main__":
    dsl = load_fold_dsl("docs/fold_dsl-sample.yaml")
    
    section = dsl.get("section")
    print("=== Fold構造 ===")
    print_section_tree(section)

    print("\n=== Bridgeリンク ===")
    links = dsl.get("links", [])
    for link in links:
        print(f"{link['source']} -> {link['target']} (type: {link['type']}, weight: {link['weight']})")

    print("\n=== Semantic ===")
    semantic = dsl.get("semantic", {})
    print(semantic)
