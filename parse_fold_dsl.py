from src.utils.dsl_parser import DSLParser

def load_fold_dsl(path: str):
    parser = DSLParser()
    return parser.parse(path)

def print_section_tree(section, level: int = 0):
    indent = "  " * level
    print(f"{indent}- {section.name} (ID: {section.id}, tension: {section.tension})")
    for child in getattr(section, 'children', []):
        print_section_tree(child, level + 1)

if __name__ == "__main__":
    dsl = load_fold_dsl("docs/fold_dsl-sample.yaml")

    print(f"title: {dsl.title}")
    print(f"tags: {dsl.tags}")

    print("=== Fold構造 ===")
    print_section_tree(dsl.sections[0])

    print("\n=== Bridgeリンク ===")
    for link in dsl.links:
        print(f"{link.source} -> {link.target} (type: {link.type}, weight: {link.weight})")

    print("\n=== Semantic ===")
    print(dsl.semantic.model_dump())
