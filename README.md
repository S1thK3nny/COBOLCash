# COBOLCash

COBOLCash is a hobby project that I developed in order to learn COBOL. It's a small banking administration tool with a PyQt6 desktop GUI on top and a GnuCOBOL program underneath that performs banking tasks and stores accounts and transactions in indexed COBOL files.  
Most people know the "Learn COBOL and earn $200k a year" memes, so of course I had to at least look at what it's all about.

For now, some parts of the GUI are just for show, as the features in the COBOL backend have not yet been fully implemented.

## Features

- **Accounts:** Create checking, savings, credit and loan accounts with an optional initial deposit. Edit account holders and types, and freeze, unfreeze, close or remove accounts.
- **Search and filter:** Search by account number or holder name, filter by status and type and sort by any column. Double-click an account to open its details.
- **Transactions:** Deposits, withdrawals and transfers between accounts. If you withdraw or transfer more than the balance, whatever is left is used instead of going into negative figures. Transactions are refused for frozen and closed accounts.
- **Transaction history:** Each account displays its transactions, which can be filtered by date range and type.
- **Self-compiling backend:** The COBOL program is compiled with `cobc` the first time you start the GUI.

## Requirements

- Linux or WSL. Native Windows won't work.
- Python 3.12
- [GnuCOBOL](https://gnucobol.sourceforge.io/)
- [PyQt6](https://pypi.org/project/PyQt6/)

```sh
sudo apt install gnucobol
python3 -m venv .venv
source .venv/bin/activate
pip install PyQt6
```

## Usage

Run it from the repository root. The paths to the COBOL program and the data files are relative to the working directory:

```sh
python src/Python/main.py
```

`main.py` only compiles `src/COBOL/basic.cob` if `src/COBOL/basic` doesn't exist yet. If you change the COBOL source, delete the binary and it gets rebuilt on the next start.  
Accounts and transactions are saved to `account.dat` and `transaction.dat` in the working directory; delete them to start over. Be careful not to collapse the economy!

| Tab | Description |
| --- | --- |
| Accounts Manager | List of all accounts with search, filters, sorting, and buttons to create and remove accounts |
| Account Details | Info about the selected account, edit/freeze/close buttons and the transaction history |
| Transactions | Deposit, withdrawal and transfer forms with searchable account pickers |
| Reports | UI only |
| Settings | UI only |

## How it works

Python and COBOL talk through pipes. For every action, `COBOLInterface.py` starts the COBOL binary, writes a single `|`-separated command to its stdin and parses whatever comes back on stdout, either `OK|...` or `ERROR|...`.

You can skip the GUI and talk to the backend directly:

```sh
# create an account with $100 initial deposit
echo "CREATE-ACCOUNT|John Doe|Checking|100" | ./src/COBOL/basic

# list every account
echo "LIST-ACCOUNTS" | ./src/COBOL/basic
```

| Command | Arguments | Description |
| --- | --- | --- |
| `CREATE-ACCOUNT` | `<holder>\|<type>\|<initial balance>` | Creates an account and books the initial deposit as its first transaction |
| `GET-ACCOUNT` | `<account>` | Returns a single account |
| `LIST-ACCOUNTS` | - | Returns every account, each followed by `ACC-DONE` |
| `UPDATE-ACCOUNT` | `<account>\|<field>\|<value>` | Field is `ACCOUNT_HOLDER`, `ACCOUNT_TYPE` or `STATUS` |
| `DELETE-ACCOUNT` | `<account>` | Deletes the account record |
| `TRANSACTION` | `<DEPOSIT\|WITHDRAWAL>\|<account>\|<amount>\|<description>` | Books a deposit or withdrawal |
| `TRANSFER` | `<from>\|<amount>\|<description>\|<to>` | Moves money between two accounts |
| `LIST-TRANSACTIONS` | `<account>\|<from date>\|<to date>` | Dates are `YYYY-MM-DD`, or a space for no limit. |
| `SECRET` | `<transaction id>\|<date>` | Changes the date of an existing transaction. Made for testing only. Very evil. |

## License

Released under the [MIT License](LICENSE), © 2025 S1thK3nny.
