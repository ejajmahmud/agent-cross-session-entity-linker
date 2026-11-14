"""CLI for agent-cross-session-entity-linker."""
import argparse
import sys
from .core import CrossSessionEntityLinker

def main():
    parser = argparse.ArgumentParser(description="Agent Cross-Session Entity Linker CLI")
    parser.add_argument("--demo", action="store_true", help="Run cross-session entity linking demo")
    args = parser.parse_args()

    if args.demo:
        linker = CrossSessionEntityLinker()
        linker.register_canonical_entity("USER_01", "Ejaj Mahmud")
        linker.add_alias("USER_01", "ejajjoy3")
        linker.add_alias("USER_01", "ejaj")

        queries = ["ejaj", "Ejaj Mahmud", "ejajjoy3", "Unknown User"]
        for q in queries:
            cid = linker.resolve(q)
            print(f"[+] Surface: '{q}' -> Canonical ID: {cid or 'UNRESOLVED'}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
