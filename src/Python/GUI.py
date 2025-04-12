# pylint: disable=no-name-in-module

import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTabWidget,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QDoubleSpinBox,
    QDateEdit,
    QStackedWidget,
    QDialog,
    QTableView,
    QHeaderView,
    QMessageBox,
    QCompleter,
)
from PyQt6.QtCore import QDate, pyqtSignal, Qt, QSortFilterProxyModel
from Account import Account, AccountType, AccountStatus
from AccountList import AccountsTableModel
from Transaction import TransactionType
from COBOLInterface import COBOL_list_accounts


class AccountDetailsWidget(QWidget):
    """Widget to display detailed account information"""

    def __init__(self, accounts_model):
        super().__init__()
        self.current_account = None
        self.accounts_model = accounts_model
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Account information section
        info_group = QGroupBox("Account Information")
        info_layout = QFormLayout()

        self.account_number = QLabel("Loading...")
        self.account_holder = QLabel("Loading...")
        self.account_type = QLabel("Loading...")
        self.creation_date = QLabel("Loading...")
        self.current_balance = QLabel("Loading...")
        self.status = QLabel("Loading...")

        info_layout.addRow("Account Number:", self.account_number)
        info_layout.addRow("Account Holder:", self.account_holder)
        info_layout.addRow("Account Type:", self.account_type)
        info_layout.addRow("Created On:", self.creation_date)
        info_layout.addRow("Current Balance:", self.current_balance)
        info_layout.addRow("Status:", self.status)

        info_group.setLayout(info_layout)

        # Action buttons
        action_layout = QHBoxLayout()

        self.btn_edit = QPushButton("Edit Details")
        self.btn_edit.clicked.connect(self.edit_account_details)

        self.btn_freeze = QPushButton("Freeze Account")
        self.btn_freeze.clicked.connect(self.toggle_freeze)

        self.btn_close = QPushButton("Close Account")
        self.btn_close.clicked.connect(self.close_account)

        action_layout.addWidget(self.btn_edit)
        action_layout.addWidget(self.btn_freeze)
        action_layout.addWidget(self.btn_close)

        # Transaction history
        history_group = QGroupBox("Transaction History")
        history_layout = QVBoxLayout()

        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(5)
        self.transaction_table.setHorizontalHeaderLabels(
            ["Date", "Type", "Amount", "Balance", "Description"]
        )
        self.transaction_table.horizontalHeader().setStretchLastSection(True)

        # Filter controls
        filter_layout = QHBoxLayout()
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.filter_type = QComboBox()
        self.filter_type.addItem("All", None)
        self.filter_type.addItems([t.value.title() for t in TransactionType])
        self.btn_filter = QPushButton("Apply Filter")

        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.date_to)
        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self.filter_type)
        filter_layout.addWidget(self.btn_filter)

        history_layout.addLayout(filter_layout)
        history_layout.addWidget(self.transaction_table)
        history_group.setLayout(history_layout)

        # Add all sections to main layout
        layout.addWidget(info_group)
        layout.addLayout(action_layout)
        layout.addWidget(history_group)

        self.setLayout(layout)

    def edit_account_details(self):
        """
        Open a dialog to edit account details.
        The dialog contains fields for account holder name and type.
        The changes are applied to the current account.
        """
        if not self.current_account:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Account Details")
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Editable fields
        name_edit = QLineEdit(self.current_account.account_holder)
        type_combo = QComboBox()
        for acc_type in AccountType:
            type_combo.addItem(acc_type.value, acc_type)
        type_combo.setCurrentIndex(
            list(AccountType).index(self.current_account.account_type)
        )

        form_layout.addRow("Account Holder:", name_edit)
        form_layout.addRow("Account Type:", type_combo)
        layout.addLayout(form_layout)

        # Buttons
        btn_save = QPushButton("Save")
        btn_cancel = QPushButton("Cancel")
        btn_save.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)
        layout.addWidget(btn_save)
        layout.addWidget(btn_cancel)

        dialog.setLayout(layout)

        if dialog.exec():
            self.accounts_model.update_account(
                self.current_account,
                {
                    "account_holder": name_edit.text().strip(),
                    "account_type": type_combo.currentData(),
                },
            )
            self.load_account_data(self.current_account)

    def toggle_freeze(self):
        """
        Toggle the freeze status of the current account.
        If the account is active, it will be frozen, and vice versa.
        If the account is closed, no action will be taken.
        """
        if not self.current_account:
            return

        if self.current_account.status == AccountStatus.FROZEN:
            self.accounts_model.update_account(
                self.current_account, {"status": AccountStatus.ACTIVE}
            )
        elif self.current_account.status == AccountStatus.ACTIVE:
            self.accounts_model.update_account(
                self.current_account, {"status": AccountStatus.FROZEN}
            )

        self.status.setText(self.current_account.status.value)
        self.load_account_data(self.current_account)  # Refresh button states

    def close_account(self):
        """
        Confirm and close the selected account.
        """
        if not self.current_account:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Close",
            f"Are you sure you want to close account #{self.current_account.account_number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.accounts_model.close_account(self.current_account)
            self.load_account_data(self.current_account)  # Refresh

    def load_account_data(self, account):
        self.current_account = account

        if account is None:
            self.account_number.setText("Loading...")
            self.account_holder.setText("Loading...")
            self.account_type.setText("Loading...")
            self.creation_date.setText("Loading...")
            self.current_balance.setText("Loading...")
            self.status.setText("Loading...")
            return

        self.account_number.setText(str(account.account_number))
        self.account_holder.setText(account.account_holder)
        self.account_type.setText(account.account_type.value)
        self.creation_date.setText(account.creation_date.strftime("%Y-%m-%d"))
        self.current_balance.setText(f"${account.balance:.2f}")
        self.status.setText(account.status.value)

        # Update button states based on status
        if account.status == AccountStatus.ACTIVE:
            self.btn_freeze.setEnabled(True)
            self.btn_close.setEnabled(True)
            self.btn_edit.setEnabled(True)
            self.btn_freeze.setText("Freeze Account")
        elif account.status == AccountStatus.FROZEN:
            self.btn_freeze.setEnabled(True)
            self.btn_close.setEnabled(True)
            self.btn_edit.setEnabled(False)
            self.btn_freeze.setText("Unfreeze Account")
        elif account.status == AccountStatus.CLOSED:
            self.btn_freeze.setEnabled(False)
            self.btn_close.setEnabled(False)
            self.btn_edit.setEnabled(False)

    def load_transaction_history(
        self, account_id, date_from=None, date_to=None, trans_type=None
    ):
        """Load transaction history from backend with optional filters"""
        # This will be implemented to interact with COBOL
        pass


class TransactionWidget(QWidget):
    """Widget for performing various transactions"""

    transaction_completed = pyqtSignal(
        TransactionType, int
    )  # Signal to update UI after transaction

    def __init__(self, accounts_model):
        super().__init__()
        self.accounts_model = accounts_model
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Transaction type selector
        self.transaction_type = QComboBox()
        self.transaction_type.addItems(
            ["Deposit", "Withdrawal", "Transfer", "Apply Interest", "Charge Fee"]
        )
        self.transaction_type.currentIndexChanged.connect(self.change_transaction_form)

        main_layout.addWidget(QLabel("Select Transaction Type:"))
        main_layout.addWidget(self.transaction_type)

        # Stacked widget to hold different transaction forms
        self.transaction_stack = QStackedWidget()

        # Create the different transaction forms
        self.deposit_form = self.create_deposit_form()
        self.withdrawal_form = self.create_withdrawal_form()
        self.transfer_form = self.create_transfer_form()
        self.interest_form = self.create_interest_form()
        self.fee_form = self.create_fee_form()

        self.transaction_stack.addWidget(self.deposit_form)
        self.transaction_stack.addWidget(self.withdrawal_form)
        self.transaction_stack.addWidget(self.transfer_form)
        self.transaction_stack.addWidget(self.interest_form)
        self.transaction_stack.addWidget(self.fee_form)

        main_layout.addWidget(self.transaction_stack)
        self.setLayout(main_layout)

    def create_searchable_account_combo(self):
        """Create a searchable account combo box that displays account number and holder"""
        combo = QComboBox()
        combo.setEditable(True)

        # Create a custom model that formats the display text
        class AccountComboModel(QSortFilterProxyModel):
            def __init__(self, source_model):
                super().__init__()
                self.setSourceModel(source_model)

            def data(self, index, role=Qt.ItemDataRole.DisplayRole):
                if (
                    role == Qt.ItemDataRole.DisplayRole
                    or role == Qt.ItemDataRole.EditRole
                ):
                    account_index = self.mapToSource(index)
                    account = self.sourceModel().get_account(account_index.row())
                    if account:
                        return f"#{account.account_number} - {account.account_holder}"
                return super().data(index, role)

        # Set up the proxy model
        proxy_model = AccountComboModel(self.accounts_model)
        combo.setModel(proxy_model)

        # Set up the completer
        completer = QCompleter(proxy_model)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        combo.setCompleter(completer)

        return combo

    def create_transaction_form(self, transaction_type: TransactionType):
        """Create a transaction form for either deposit or withdrawal"""
        widget = QWidget()
        layout = QFormLayout()

        # Create account selection combo box
        account_select = self.create_searchable_account_combo()

        # Create amount field
        amount_field = QDoubleSpinBox()
        amount_field.setRange(0.01, 1000000.00)
        amount_field.setPrefix("$")
        amount_field.setDecimals(2)

        # Create description field
        description_field = QLineEdit()

        # Create button
        button = QPushButton(f"Process {transaction_type.value.capitalize()}")

        # Store fields as instance variables based on transaction type
        if transaction_type == TransactionType.DEPOSIT:
            self.deposit_account = account_select
            self.deposit_amount = amount_field
            self.deposit_description = description_field
            self.btn_process_deposit = button
        else:  # WITHDRAWAL
            self.withdrawal_account = account_select
            self.withdrawal_amount = amount_field
            self.withdrawal_description = description_field
            self.btn_process_withdrawal = button
        button.clicked.connect(lambda: self.process_transaction(transaction_type))

        # Add all fields to layout
        layout.addRow("Account:", account_select)
        layout.addRow("Amount:", amount_field)
        layout.addRow("Description:", description_field)
        layout.addRow("", button)

        widget.setLayout(layout)
        return widget

    def create_deposit_form(self):
        """Create deposit transaction form"""
        return self.create_transaction_form(TransactionType.DEPOSIT)

    def create_withdrawal_form(self):
        """Create withdrawal transaction form"""
        return self.create_transaction_form(TransactionType.WITHDRAWAL)

    def create_transfer_form(self):
        """Create transfer transaction form"""
        widget = QWidget()
        layout = QFormLayout()

        # Use searchable account combo boxes instead of QLineEdit
        self.transfer_from = self.create_searchable_account_combo()
        self.transfer_to = self.create_searchable_account_combo()

        self.transfer_amount = QDoubleSpinBox()
        self.transfer_amount.setRange(0.01, 1000000.00)
        self.transfer_amount.setPrefix("$")
        self.transfer_amount.setDecimals(2)
        self.transfer_description = QLineEdit()
        self.btn_process_transfer = QPushButton("Process Transfer")
        self.btn_process_transfer.clicked.connect(
            lambda: self.process_transaction(TransactionType.TRANSFER)
        )

        layout.addRow("From Account:", self.transfer_from)
        layout.addRow("To Account:", self.transfer_to)
        layout.addRow("Amount:", self.transfer_amount)
        layout.addRow("Description:", self.transfer_description)
        layout.addRow("", self.btn_process_transfer)

        widget.setLayout(layout)
        return widget

    def create_interest_form(self):
        """Create interest application form"""
        widget = QWidget()
        layout = QFormLayout()

        self.interest_account = self.create_searchable_account_combo()
        self.interest_rate = QDoubleSpinBox()
        self.interest_rate.setRange(0.01, 100.00)
        self.interest_rate.setSuffix("%")
        self.interest_rate.setDecimals(2)
        self.interest_description = QLineEdit()
        self.btn_apply_interest = QPushButton("Apply Interest")
        self.btn_apply_interest.clicked.connect(
            lambda: self.process_transaction(TransactionType.INTEREST)
        )

        layout.addRow("Account Number:", self.interest_account)
        layout.addRow("Interest Rate:", self.interest_rate)
        layout.addRow("Description:", self.interest_description)
        layout.addRow("", self.btn_apply_interest)

        widget.setLayout(layout)
        return widget

    def create_fee_form(self):
        """Create fee charging form"""
        widget = QWidget()
        layout = QFormLayout()

        self.fee_account = self.create_searchable_account_combo()
        self.fee_amount = QDoubleSpinBox()
        self.fee_amount.setRange(0.01, 1000.00)
        self.fee_amount.setPrefix("$")
        self.fee_amount.setDecimals(2)
        self.fee_type = QComboBox()
        self.fee_type.addItems(
            [
                "Maintenance",
                "Overdraft",
                "Service",
                "Late Payment",
                "Wire Transfer",
                "Other",
            ]
        )
        self.fee_description = QLineEdit()
        self.btn_charge_fee = QPushButton("Charge Fee")
        self.btn_charge_fee.clicked.connect(
            lambda: self.process_transaction(TransactionType.FEE)
        )

        layout.addRow("Account Number:", self.fee_account)
        layout.addRow("Fee Amount:", self.fee_amount)
        layout.addRow("Fee Type:", self.fee_type)
        layout.addRow("Description:", self.fee_description)
        layout.addRow("", self.btn_charge_fee)

        widget.setLayout(layout)
        return widget

    def change_transaction_form(self, index):
        """Change the displayed transaction form based on selection"""
        self.transaction_stack.setCurrentIndex(index)

    def process_transaction(self, transaction_type: TransactionType):
        """Process deposit/withdrawal transaction"""

        target_account = None

        if transaction_type == TransactionType.DEPOSIT:
            account_combo = self.deposit_account
            amount = self.deposit_amount.value()
            description = self.deposit_description.text()
        elif transaction_type == TransactionType.WITHDRAWAL:
            account_combo = self.withdrawal_account
            amount = self.withdrawal_amount.value()
            description = self.withdrawal_description.text()
        elif transaction_type == TransactionType.TRANSFER:
            account_combo = self.transfer_from
            target_account = self.transfer_to
            amount = self.transfer_amount.value()
            description = self.transfer_description.text()
        elif transaction_type == TransactionType.INTEREST:
            account_combo = self.interest_account
            amount = self.interest_rate.value()
            description = self.interest_description.text()
        elif transaction_type == TransactionType.FEE:
            account_combo = self.fee_account
            amount = self.fee_amount.value()
            description = (
                f"{self.fee_type.currentText()}: {self.fee_description.text()}"
            )
        else:
            return

        # Get the selected account from the combo box
        account_index = account_combo.currentIndex()
        selected_account = self.accounts_model.get_account(account_index)

        if target_account:
            target_account = target_account.currentIndex()
            target_account = self.accounts_model.get_account(target_account)

        if selected_account:
            success = self.accounts_model.process_transaction(
                transaction_type,
                selected_account.account_number,
                amount,
                description,
                target_account.account_number if target_account else None,
            )

            if success:
                self.transaction_completed.emit(
                    transaction_type, selected_account.account_number
                )
                self._reset_transaction_form(transaction_type)
            else:
                QMessageBox.warning(
                    self, "Transaction Error", "Transaction could not be processed."
                )
        else:
            # Handle case where no account is selected
            QMessageBox.warning(self, "Transaction Error", "Please select an account.")

    def _reset_transaction_form(self, transaction_type: TransactionType):
        """Reset form fields after successful transaction"""
        if transaction_type == TransactionType.DEPOSIT:
            self.deposit_amount.setValue(0.01)
            self.deposit_description.clear()
        elif transaction_type == TransactionType.WITHDRAWAL:
            self.withdrawal_amount.setValue(0.01)
            self.withdrawal_description.clear()
        elif transaction_type == TransactionType.TRANSFER:
            self.transfer_amount.setValue(0.01)
            self.transfer_description.clear()
        elif transaction_type == TransactionType.INTEREST:
            self.interest_rate.setValue(0.01)
            self.interest_description.clear()
        elif transaction_type == TransactionType.FEE:
            self.fee_amount.setValue(0.01)
            self.fee_description.clear()


class AccountsManagerWidget(QWidget):
    """Widget for managing accounts"""

    account_selected = pyqtSignal(Account)
    account_selected_double_clicked = pyqtSignal(Account)

    def __init__(self, accounts_model):
        super().__init__()
        self.accounts_model = accounts_model
        self.initUI()

    def initUI(self):
        """
        Initialize the UI components for the Accounts Manager.
        """
        # Create a QTableView and set the model
        self.table_view = QTableView()
        self.table_view.setModel(self.accounts_model)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view.setSortingEnabled(True)
        self.table_view.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.table_view.selectionModel().selectionChanged.connect(
            self.on_account_selected
        )
        self.table_view.doubleClicked.connect(self.switch)

        # Optionally, add search and filter tools:
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by account number or name...")
        self.search_input.textChanged.connect(lambda text: self.apply_filters())
        self.search_input.setClearButtonEnabled(True)

        self.filter_status = QComboBox()
        self.filter_status.addItem("All Accounts", None)
        for status in AccountStatus:
            self.filter_status.addItem(status.value, status)
        self.filter_status.currentIndexChanged.connect(lambda: self.apply_filters())

        self.filter_type = QComboBox()
        self.filter_type.addItem("All Types", None)
        for acc_type in AccountType:
            self.filter_type.addItem(acc_type.value, acc_type)
        self.filter_type.currentIndexChanged.connect(lambda: self.apply_filters())

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.filter_status)
        search_layout.addWidget(self.filter_type)

        # Action buttons at the bottom
        button_layout = QHBoxLayout()
        self.btn_new_account = QPushButton("New Account")
        self.btn_new_account.clicked.connect(self.create_new_account)

        self.btn_view_details = QPushButton("Remove Account")
        self.btn_view_details.clicked.connect(self.remove_account)

        self.btn_batch_interest = QPushButton("Batch Interest")
        self.btn_export = QPushButton("Export Data")

        button_layout.addWidget(self.btn_new_account)
        button_layout.addWidget(self.btn_view_details)
        button_layout.addWidget(self.btn_batch_interest)
        button_layout.addWidget(self.btn_export)

        # Set up the main layout
        layout = QVBoxLayout()
        layout.addLayout(search_layout)
        layout.addWidget(self.table_view)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_account_selected(self):
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if selected_indexes:
            row = selected_indexes[0].row()
            account = self.accounts_model.get_account(row)
            if account:
                self.account_selected.emit(account)

    def switch(self, index):
        """Switch to the account details tab"""
        self.account_selected_double_clicked.emit(
            self.accounts_model.get_account(index.row())
        )

    def apply_filters(self):
        text = self.search_input.text()
        status = self.filter_status.currentData()
        acc_type = self.filter_type.currentData()
        print("Applying filters:", text, status, acc_type)
        self.accounts_model.set_filters(text, status, acc_type)

    def create_new_account(self):
        """Open dialog to create new account"""
        dlg = QDialog(self)
        dlg.setWindowTitle("Create New Account")
        dlg.setMinimumSize(400, 300)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        # Account Holder field
        self.input_account_holder = QLineEdit()
        form_layout.addRow(
            "Account Holder:", self.input_account_holder
        )  # TODO: Fix empty field

        # Account Type field using a QComboBox with enum values
        self.combo_account_type = QComboBox()
        for acc_type in AccountType:
            self.combo_account_type.addItem(acc_type.value, acc_type)
        form_layout.addRow("Account Type:", self.combo_account_type)

        # Initial Balance field using QDoubleSpinBox
        self.input_balance = QDoubleSpinBox()
        self.input_balance.setRange(0, 1e9)
        self.input_balance.setPrefix("$")
        self.input_balance.setDecimals(2)
        form_layout.addRow("Initial Balance:", self.input_balance)

        layout.addLayout(form_layout)

        # Add form fields and buttons here
        self.btn_create = QPushButton("Create Account")
        self.btn_cancel = QPushButton("Cancel")
        layout.addWidget(self.btn_create)
        layout.addWidget(self.btn_cancel)

        dlg.setLayout(layout)
        self.btn_create.clicked.connect(dlg.accept)
        self.btn_cancel.clicked.connect(dlg.reject)

        if dlg.exec() == QDialog.DialogCode.Accepted:
            account_holder = self.input_account_holder.text().strip()

            account_type = (
                self.combo_account_type.currentData()
            )  # Returns AccountType enum
            balance = self.input_balance.value()

            self.accounts_model.add_account(account_holder, account_type, balance)
        else:
            print("Account creation canceled.")

    def remove_account(self):
        """
        Remove selected account from the list and update the model.
        This method will be called when the "Remove Account" button is clicked.
        """
        selected_indexes = self.table_view.selectionModel().selectedRows()
        if not selected_indexes:
            print("Tried to remove account, but none selected.")
            QMessageBox.warning(self, "Warning", "No account selected.")
            return

        selected_row = selected_indexes[0].row()
        account = self.accounts_model.get_account(selected_row)

        confirm = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Are you sure you want to remove account #{account.account_number}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm == QMessageBox.StandardButton.Yes:
            print(f"Removing Account #{account.account_number}")
            self.accounts_model.remove_account(account)

    def apply_batch_interest(self):
        """Apply interest to multiple accounts"""
        # Will be implemented
        pass

    def export_accounts_data(self):
        """Export accounts data to file"""
        # Will be implemented
        pass


class ReportsWidget(QWidget):
    """Widget for generating reports"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Report type selection
        report_group = QGroupBox("Generate Reports")
        report_layout = QVBoxLayout()

        report_type_layout = QHBoxLayout()
        report_type_layout.addWidget(QLabel("Report Type:"))
        self.report_type = QComboBox()
        self.report_type.addItems(
            [
                "Daily Transaction Summary",
                "Account Balance Report",
                "Interest Earned Report",
                "Fees Collected Report",
                "Account Activity Report",
                "Dormant Accounts Report",
            ]
        )
        report_type_layout.addWidget(self.report_type)

        # Report parameters
        param_layout = QFormLayout()
        self.date_range_from = QDateEdit()
        self.date_range_from.setDate(QDate.currentDate().addDays(-30))
        self.date_range_to = QDateEdit()
        self.date_range_to.setDate(QDate.currentDate())

        self.account_filter = QLineEdit()
        self.account_filter.setPlaceholderText("Leave blank for all accounts")

        self.min_amount = QDoubleSpinBox()
        self.min_amount.setRange(0, 1000000.00)
        self.min_amount.setPrefix("$")
        self.min_amount.setDecimals(2)

        param_layout.addRow("From Date:", self.date_range_from)
        param_layout.addRow("To Date:", self.date_range_to)
        param_layout.addRow("Account Filter:", self.account_filter)
        param_layout.addRow("Minimum Amount:", self.min_amount)

        # Generate button
        self.btn_generate = QPushButton("Generate Report")

        # Add all to report layout
        report_layout.addLayout(report_type_layout)
        report_layout.addLayout(param_layout)
        report_layout.addWidget(self.btn_generate)
        report_group.setLayout(report_layout)

        # Report output
        output_group = QGroupBox("Report Output")
        output_layout = QVBoxLayout()

        self.report_table = QTableWidget()

        output_buttons = QHBoxLayout()
        self.btn_print = QPushButton("Print")
        self.btn_export_csv = QPushButton("Export to CSV")
        self.btn_export_pdf = QPushButton("Export to PDF")

        output_buttons.addWidget(self.btn_print)
        output_buttons.addWidget(self.btn_export_csv)
        output_buttons.addWidget(self.btn_export_pdf)

        output_layout.addWidget(self.report_table)
        output_layout.addLayout(output_buttons)
        output_group.setLayout(output_layout)

        # Add to main layout
        layout.addWidget(report_group)
        layout.addWidget(output_group)

        self.setLayout(layout)

    def generate_report(self):
        """Generate the selected report"""
        # Will be implemented to interact with COBOL
        pass

    def print_report(self):
        """Print the current report"""
        # Will be implemented
        pass

    def export_to_csv(self):
        """Export the current report to CSV"""
        # Will be implemented
        pass

    def export_to_pdf(self):
        """Export the current report to PDF"""
        # Will be implemented
        pass


class SettingsWidget(QWidget):
    """Widget for application settings"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # COBOL configuration
        cobol_group = QGroupBox("COBOL Configuration")
        cobol_layout = QFormLayout()

        self.cobol_path = QLineEdit()
        self.btn_browse_cobol = QPushButton("Browse")

        cobol_path_layout = QHBoxLayout()
        cobol_path_layout.addWidget(self.cobol_path)
        cobol_path_layout.addWidget(self.btn_browse_cobol)

        self.compile_on_start = QComboBox()
        self.compile_on_start.addItems(["Yes", "No"])

        cobol_layout.addRow("GNU COBOL Path:", cobol_path_layout)
        cobol_layout.addRow("Compile on Start:", self.compile_on_start)
        cobol_group.setLayout(cobol_layout)

        # Database settings
        db_group = QGroupBox("Database Settings")
        db_layout = QFormLayout()

        self.db_path = QLineEdit()
        self.btn_browse_db = QPushButton("Browse")

        db_path_layout = QHBoxLayout()
        db_path_layout.addWidget(self.db_path)
        db_path_layout.addWidget(self.btn_browse_db)

        self.backup_location = QLineEdit()
        self.btn_browse_backup = QPushButton("Browse")

        backup_path_layout = QHBoxLayout()
        backup_path_layout.addWidget(self.backup_location)
        backup_path_layout.addWidget(self.btn_browse_backup)

        self.auto_backup = QComboBox()
        self.auto_backup.addItems(["Daily", "Weekly", "Monthly", "Never"])

        db_layout.addRow("Database Path:", db_path_layout)
        db_layout.addRow("Backup Location:", backup_path_layout)
        db_layout.addRow("Auto Backup:", self.auto_backup)
        db_group.setLayout(db_layout)

        # Application settings
        app_group = QGroupBox("Application Settings")
        app_layout = QFormLayout()

        self.default_interest_rate = QDoubleSpinBox()
        self.default_interest_rate.setRange(0.01, 20.00)
        self.default_interest_rate.setValue(1.50)
        self.default_interest_rate.setSuffix("%")
        self.default_interest_rate.setDecimals(2)

        self.default_fee = QDoubleSpinBox()
        self.default_fee.setRange(0.01, 100.00)
        self.default_fee.setValue(5.00)
        self.default_fee.setPrefix("$")
        self.default_fee.setDecimals(2)

        self.log_level = QComboBox()
        self.log_level.addItems(["Debug", "Info", "Warning", "Error", "Critical"])

        app_layout.addRow("Default Interest Rate:", self.default_interest_rate)
        app_layout.addRow("Default Fee:", self.default_fee)
        app_layout.addRow("Log Level:", self.log_level)
        app_group.setLayout(app_layout)

        # Save and reset buttons
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save Settings")
        self.btn_reset = QPushButton("Reset to Defaults")

        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_reset)

        # Add all to main layout
        layout.addWidget(cobol_group)
        layout.addWidget(db_group)
        layout.addWidget(app_group)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_settings(self):
        """Save current settings"""
        # Will be implemented
        pass

    def reset_settings(self):
        """Reset settings to defaults"""
        # Will be implemented
        pass

    def browse_cobol_path(self):
        """Browse for COBOL executable"""
        # Will be implemented
        pass

    def browse_db_path(self):
        """Browse for database file"""
        # Will be implemented
        pass

    def browse_backup_path(self):
        """Browse for backup location"""
        # Will be implemented
        pass


class BankingAdminGUI(QMainWindow):
    """Main window for the banking admin application"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banking Admin System")
        self.setMinimumSize(1000, 700)
        self.accounts_model = AccountsTableModel(COBOL_list_accounts())
        self.selected_account = None
        self.initUI()

    def initUI(self):
        # Create main tab widget
        self.tabs = QTabWidget()

        # Create the various tabs
        self.accounts_manager = AccountsManagerWidget(self.accounts_model)
        self.account_details = AccountDetailsWidget(self.accounts_model)
        self.transaction_widget = TransactionWidget(self.accounts_model)
        self.reports_widget = ReportsWidget()
        self.settings_widget = SettingsWidget()

        # Add tabs to the widget
        self.tabs.addTab(self.accounts_manager, "Accounts Manager")
        self.tabs.addTab(self.account_details, "Account Details")
        self.tabs.addTab(self.transaction_widget, "Transactions")
        self.tabs.addTab(self.reports_widget, "Reports")
        self.tabs.addTab(self.settings_widget, "Settings")

        self.tabs.currentChanged.connect(self.on_tab_changed)

        # Connect signals
        self.accounts_manager.account_selected.connect(self.show_account_details)
        self.accounts_manager.account_selected_double_clicked.connect(
            self.switchToDetails
        )

        # Set the central widget
        self.setCentralWidget(self.tabs)

        # Create status bar
        self.statusBar().showMessage("Ready")

        # Create menu bar
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        backup_action = file_menu.addAction("Backup Database")
        restore_action = file_menu.addAction("Restore Database")
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)

        # Account menu
        account_menu = menubar.addMenu("Account")

        new_account_action = account_menu.addAction("New Account")
        new_account_action.triggered.connect(self.accounts_manager.create_new_account)
        account_menu.addSeparator()

        new_account_action = account_menu.addAction("Remove Account")
        new_account_action.triggered.connect(self.accounts_manager.remove_account)
        account_menu.addSeparator()

        batch_interest_action = account_menu.addAction("Apply Batch Interest")
        batch_interest_action.triggered.connect(
            self.accounts_manager.apply_batch_interest
        )
        account_menu.addSeparator()
        export_action = account_menu.addAction("Export Accounts Data")
        export_action.triggered.connect(self.accounts_manager.export_accounts_data)

        # Reports menu
        reports_menu = menubar.addMenu("Reports")

        daily_summary_action = reports_menu.addAction("Daily Transaction Summary")
        balance_report_action = reports_menu.addAction("Account Balance Report")
        interest_report_action = reports_menu.addAction("Interest Earned Report")
        fees_report_action = reports_menu.addAction("Fees Collected Report")
        activity_report_action = reports_menu.addAction("Account Activity Report")
        dormant_report_action = reports_menu.addAction("Dormant Accounts Report")

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        check_cobol_action = tools_menu.addAction("Check COBOL Installation")
        COBOL_compile_action = tools_menu.addAction("Compile COBOL Programs")
        tools_menu.addSeparator()
        consistency_check_action = tools_menu.addAction("Database Consistency Check")
        optimize_action = tools_menu.addAction("Optimize Database")

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        help_action = help_menu.addAction("User Guide")

    def show_account_details(self, account):
        self.selected_account = account  # store it for later

    def on_tab_changed(self, index):
        if self.tabs.widget(index) is self.account_details and self.selected_account:
            # TODO: On account removal, selected_account should be None
            self.account_details.load_account_data(self.selected_account)

    def switchToDetails(self):
        """Switch to the account details tab"""
        self.tabs.setCurrentIndex(1)

    def backup_database(self):
        """Backup the database"""
        # Will be implemented
        pass

    def restore_database(self):
        """Restore the database from backup"""
        # Will be implemented
        pass

    def check_cobol_installation(self):
        """Check if GNU COBOL is installed"""
        # Will be implemented
        pass

    def COBOL_compile_programs(self):
        """Compile COBOL programs"""
        # Will be implemented
        pass

    def show_about_dialog(self):
        """Show about dialog"""
        # Will be implemented
        pass

    def show_user_guide(self):
        """Show user guide"""
        # Will be implemented
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BankingAdminGUI()
    window.show()
    sys.exit(app.exec())
