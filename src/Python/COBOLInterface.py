import subprocess
import os.path
from Account import Account

COBOL_DIRECTORY = "src/COBOL/"
BINARY_PATH = os.path.join(COBOL_DIRECTORY, "basic")


def call_cobol(command_string, verbose=False):
    if "|" not in command_string:
        raise ValueError("Invalid COBOL command format.")

    proc = subprocess.Popen(
        [BINARY_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate(command_string + "\n")

    if verbose:
        print("[COBOL OUT]:", stdout)
        print("[COBOL ERR]:", stderr)

    result = stdout.strip()
    if result.startswith("ERROR"):
        return f"COBOL responded with error: {result}"
    return result


def compile_cobol():
    # Compile the COBOL program
    compile_command = [
        "cobc",
        "-x",
        "-o",
        BINARY_PATH,
        BINARY_PATH + ".cob",
    ]
    proc = subprocess.run(compile_command, capture_output=True, text=True)

    if proc.returncode != 0:
        print("Compilation Error:", proc.stderr)
        return False
    return True


def get_account(account_number: int) -> Account:
    response = call_cobol(f"GET-ACCOUNT|{account_number}")
    if response.startswith("ERROR"):
        print("Error fetching account:", response)
        return None

    account_data = [item.strip() for item in response.split("|")]

    # Pop and discard the status field (e.g., 'OK')
    account_data.pop(0)

    # Create a new Account and populate it
    acc = Account()
    acc.from_list(account_data)

    return acc


if __name__ == "__main__":
    if not os.path.exists(COBOL_DIRECTORY):
        os.makedirs(COBOL_DIRECTORY)

    # Check if the COBOL binary exists
    if os.path.isfile(BINARY_PATH):
        print("COBOL program exists.")
    else:
        print("COBOL program does not exist. Compiling...")
        if compile_cobol():
            print("Compilation successful.")
        else:
            print("Compilation failed.")
            raise Exception("Compilation failed.")

    response = call_cobol("CREATE-ACCOUNT|John Doe|Checking|100")
    print("Response from COBOL:", response)

    response = call_cobol("GET-ACCOUNT|1")
    print("Response from COBOL:", [item.strip() for item in response.split("|")])
