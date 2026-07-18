import initialize


def main():
    print("=== Which llm to use ===")
    print("g: Gemini, o: ollama")
    model_type = input(":")
    if model_type == "g":
        from agent import gemini

        gemini.main_loop()
    elif model_type == "o":
        from agent.loop import main_loop

        main_loop()
    elif model_type == "q":
        return
    else:
        print("Enter valid input.")
        main()


if __name__ == "__main__":
    main()
