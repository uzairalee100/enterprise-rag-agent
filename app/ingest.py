from app.vectorstore import build_index


def main():
    store = build_index(force=True)
    count = len(store.get()["ids"])
    print(f"Indexed {count} chunks into Chroma collection.")


if __name__ == "__main__":
    main()
