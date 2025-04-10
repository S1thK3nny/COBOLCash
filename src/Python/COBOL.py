import subprocess
import os.path

COBOL_DIRECTORY = "src/COBOL/"
BINARY_PATH = os.path.join(COBOL_DIRECTORY, "basic")


def call_cobol(command_string):
    proc = subprocess.Popen(
        [BINARY_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = proc.communicate(command_string + "\n")

    if stderr:
        print("COBOL Error:", stderr)
    return stdout.strip()


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


# Example usage
if os.path.isfile(BINARY_PATH):
    print("COBOL program exists.")
else:
    print("COBOL program does not exist. Compiling...")
    if compile_cobol():
        print("Compilation successful.")
    else:
        print("Compilation failed.")
        raise Exception("Compilation failed.")

response = call_cobol("DEPOSIT|123456|100.00|ATM deposit")
print("Response from COBOL:", response)
