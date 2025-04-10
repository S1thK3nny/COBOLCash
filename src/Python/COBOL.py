import subprocess
import os.path

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
        raise Exception(f"COBOL responded with error: {result}")
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


if os.path.isfile(BINARY_PATH):
    print("COBOL program exists.")
else:
    print("COBOL program does not exist. Compiling...")
    if compile_cobol():
        print("Compilation successful.")
    else:
        print("Compilation failed.")
        raise Exception("Compilation failed.")

response = call_cobol("CREATE|John Doe|Checking|100")
print("Response from COBOL:", response)
