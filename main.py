from resume_parser import parse_resume, parse_information

PATH = "PATH TO RESUME"

def main():
    path = PATH
    text = parse_resume(path)

    print("========== EXTRACTED TEXT ==========")
    print(text)

    parsed = parse_information(text)

    print("\n===== STRUCTURED RESUME INFO =====")
    for key, value in parsed.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
