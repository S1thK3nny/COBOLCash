import subprocess
import os.path
from Account import Account

COBOL_DIRECTORY = "src/COBOL/"
BINARY_PATH = os.path.join(COBOL_DIRECTORY, "basic")


def COBOL_call(command_string, verbose=False):
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


def COBOL_compile():
    # Compile the COBOL program
    if not os.path.exists(COBOL_DIRECTORY):
        os.makedirs(COBOL_DIRECTORY)

    # Check if the COBOL binary exists
    if os.path.isfile(BINARY_PATH):
        print("COBOL program exists, return early boys.")
        return True
    else:
        print("COBOL program does not exist. Compiling...")

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


def COBOL_get_account(account_number: int) -> Account:
    response = COBOL_call(f"GET-ACCOUNT|{account_number}")
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


def COBOL_list_accounts():
    response = COBOL_call("LIST-ACCOUNTS")
    if response.startswith("ERROR"):
        print("Error fetching accounts:", response)
        return []

    lines = response.split("ACC-DONE")
    accounts = []

    for raw_account in lines:
        raw_account = raw_account.strip()
        if not raw_account:
            continue

        fields = [item.strip() for item in raw_account.split("|")]
        if len(fields) < 7:
            print("Skipping incomplete record:", fields)
            continue

        acc = Account()
        acc.from_list(fields)
        accounts.append(acc)

    return accounts


if __name__ == "__main__":
    response = COBOL_call("CREATE-ACCOUNT|John Doe|Checking|100")
    print("Response from COBOL:", response)

    response = COBOL_call("GET-ACCOUNT|1")
    print("Response from COBOL:", [item.strip() for item in response.split("|")])
