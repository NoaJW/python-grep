import re
import requests
import os


def find_word_in_content(source, content, word, case_insensitive=False, reverse_search=False):
    lines = content.split('\n')

    flags = re.IGNORECASE if case_insensitive else 0

    # Find the word in each line
    matches = [(i + 1, line) for i, line in enumerate(lines) if re.search(fr'\b{word}\b', line, flags=flags)]

    if reverse_search:
        matches = [(i + 1, line) for i, line in enumerate(lines) if (i + 1, line) not in matches]

    # Return the results in the specified format        
    return [f"{source} | line {line_number} = {line_content}" for line_number, line_content in matches]


def search_word_in_file(file_path, word, case_insensitive=False, reverse_search=False):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Find and print occurrences of the word
        results = find_word_in_content(file_path, content, word, case_insensitive, reverse_search)
        for result in results:
            print(result)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")


def search_word_in_folder(folder_path, word, case_insensitive=False, reverse_search=False):
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()

                # Find and print occurrences of the word
                results = find_word_in_content(file_path, content, word, case_insensitive, reverse_search)
                for result in results:
                    print(result)
    except FileNotFoundError:
        print(f"Error: Folder not found at {folder_path}")


def grep(input_str, word, case_insensitive=False, reverse_search=False):
    try:
        # Check if the input string contains a URL
        url_match = re.search(r'url:(\S+)', input_str)
        url = url_match.group(1) if url_match else None

        # Check if the input string contains a file path
        file_match = re.search(r'file:(\S+)', input_str)
        file_path = file_match.group(1) if file_match else None

        # Check if the input string contains a folder path
        folder_match = re.search(r'folder:(\S+)', input_str)
        folder_path = folder_match.group(1) if folder_match else None

        if url:
            # Get content of the URL
            response = requests.get(url)
            content = response.text

            # Find and print occurrences of the word
            results = find_word_in_content(url, content, word, case_insensitive, reverse_search)
            for result in results:
                print(result)
        if file_path:
            search_word_in_file(file_path, word, case_insensitive, reverse_search)
        if folder_path:
            search_word_in_folder(folder_path, word, case_insensitive, reverse_search)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")


if __name__ == "__main__":
    user_input = input("Enter grep command (e.g., grep -v -i hello url:http://www.lipsum.com/): ")

    # Regex pattern to match
    pattern = r'grep(?: (-v))?(?: (-i))?(?: (\S+))? (?:file:(\S+))?(?:,?url:(\S+))?(?:,?folder:(\S+))?'

    match = re.match(pattern, user_input)

    # TODO: url, file and folder are not in sequence and may have multiples
    if match:
        reverse_search = bool(match.group(1))
        case_insensitive = bool(match.group(2))
        word = match.group(3)
        url = match.group(4)
        file_path = match.group(5)
        folder_path = match.group(6)
  
        grep(user_input, word, case_insensitive, reverse_search)
    else:
        print("Invalid input. Please follow the format: grep [-v] [-i] <word> url:<URL>")