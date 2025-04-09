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
)
from PyQt6.QtCore import QDate, pyqtSignal
from Account import Account, AccountType, AccountStatus
from AccountList import AccountsTableModel


class AccountDetailsWidget(QWidget):
    """Widget to display detailed account information"""

    def __init__(self):
        super().__init__()
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
        self.btn_freeze = QPushButton("Freeze Account")
        self.btn_close = QPushButton("Close Account")

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
        self.filter_type.addItems(
            ["All", "Deposit", "Withdrawal", "Transfer", "Interest", "Fee"]
        )
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

    def load_account_data(self, account_id):
        """Load account details from backend"""
        # This will be implemented to interact with COBOL
        pass

    def load_transaction_history(
        self, account_id, date_from=None, date_to=None, trans_type=None
    ):
        """Load transaction history from backend with optional filters"""
        # This will be implemented to interact with COBOL
        pass


class TransactionWidget(QWidget):
    """Widget for performing various transactions"""

    transaction_completed = pyqtSignal(
        str, str
    )  # Signal to update UI after transaction

    def __init__(self):
        super().__init__()
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

    def create_deposit_form(self):
        """Create deposit transaction form"""
        widget = QWidget()
        layout = QFormLayout()

        self.deposit_account = QLineEdit()
        self.deposit_amount = QDoubleSpinBox()
        self.deposit_amount.setRange(0.01, 1000000.00)
        self.deposit_amount.setPrefix("$")
        self.deposit_amount.setDecimals(2)
        self.deposit_description = QLineEdit()
        self.btn_process_deposit = QPushButton("Process Deposit")

        layout.addRow("Account Number:", self.deposit_account)
        layout.addRow("Amount:", self.deposit_amount)
        layout.addRow("Description:", self.deposit_description)
        layout.addRow("", self.btn_process_deposit)

        widget.setLayout(layout)
        return widget

    def create_withdrawal_form(self):
        """Create withdrawal transaction form"""
        widget = QWidget()
        layout = QFormLayout()

        self.withdrawal_account = QLineEdit()
        self.withdrawal_amount = QDoubleSpinBox()
        self.withdrawal_amount.setRange(0.01, 1000000.00)
        self.withdrawal_amount.setPrefix("$")
        self.withdrawal_amount.setDecimals(2)
        self.withdrawal_description = QLineEdit()
        self.btn_process_withdrawal = QPushButton("Process Withdrawal")

        layout.addRow("Account Number:", self.withdrawal_account)
        layout.addRow("Amount:", self.withdrawal_amount)
        layout.addRow("Description:", self.withdrawal_description)
        layout.addRow("", self.btn_process_withdrawal)

        widget.setLayout(layout)
        return widget

    def create_transfer_form(self):
        """Create transfer transaction form"""
        widget = QWidget()
        layout = QFormLayout()

        self.transfer_from = QLineEdit()
        self.transfer_to = QLineEdit()
        self.transfer_amount = QDoubleSpinBox()
        self.transfer_amount.setRange(0.01, 1000000.00)
        self.transfer_amount.setPrefix("$")
        self.transfer_amount.setDecimals(2)
        self.transfer_description = QLineEdit()
        self.btn_process_transfer = QPushButton("Process Transfer")

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

        self.interest_account = QLineEdit()
        self.interest_rate = QDoubleSpinBox()
        self.interest_rate.setRange(0.01, 100.00)
        self.interest_rate.setSuffix("%")
        self.interest_rate.setDecimals(2)
        self.interest_description = QLineEdit()
        self.btn_apply_interest = QPushButton("Apply Interest")

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

        self.fee_account = QLineEdit()
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

    def process_deposit(self):
        """Process deposit transaction"""
        # Will be implemented to interact with COBOL
        pass

    def process_withdrawal(self):
        """Process withdrawal transaction"""
        # Will be implemented to interact with COBOL
        pass

    def process_transfer(self):
        """Process transfer transaction"""
        # Will be implemented to interact with COBOL
        pass

    def apply_interest(self):
        """Apply interest to an account"""
        # Will be implemented to interact with COBOL
        pass

    def charge_fee(self):
        """Charge fee to an account"""
        # Will be implemented to interact with COBOL
        pass


class AccountsManagerWidget(QWidget):
    """Widget for managing accounts"""

    account_selected = pyqtSignal(str)

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
        """Handle account selection from the table"""
        # Will emit signal with account ID
        selected_row = self.table_view.currentRow()
        if selected_row >= 0:
            account_id = self.table_view.item(selected_row, 0).text()
            print("Selected account ID:", account_id)
            self.account_selected.emit(account_id)

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

            new_account = Account(
                account_number=0,  # TODO: This should be auto-generated or fetched from the database
                account_holder=account_holder,
                account_type=account_type,
                balance=balance,
                status=AccountStatus.ACTIVE,
            )

            # Here you might add the new account to your account list or database
            print("New account created:", new_account)
            # For example, you might call:
            self.accounts_model.add_account(new_account)
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
        print(f"Removing Account #{selected_row}")
        self.accounts_model.remove_account(
            self.accounts_model.get_account(selected_row)
        )

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
        self.accounts_model = AccountsTableModel([])
        self.initUI()

    def initUI(self):
        # Create main tab widget
        self.tabs = QTabWidget()

        # Create the various tabs
        self.accounts_manager = AccountsManagerWidget(self.accounts_model)
        self.account_details = AccountDetailsWidget()
        self.transaction_widget = TransactionWidget()
        self.reports_widget = ReportsWidget()
        self.settings_widget = SettingsWidget()

        # Add tabs to the widget
        self.tabs.addTab(self.accounts_manager, "Accounts Manager")
        self.tabs.addTab(self.account_details, "Account Details")
        self.tabs.addTab(self.transaction_widget, "Transactions")
        self.tabs.addTab(self.reports_widget, "Reports")
        self.tabs.addTab(self.settings_widget, "Settings")

        # Connect signals
        self.accounts_manager.account_selected.connect(self.show_account_details)

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
        compile_cobol_action = tools_menu.addAction("Compile COBOL Programs")
        tools_menu.addSeparator()
        consistency_check_action = tools_menu.addAction("Database Consistency Check")
        optimize_action = tools_menu.addAction("Optimize Database")

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = help_menu.addAction("About")
        help_action = help_menu.addAction("User Guide")

    def show_account_details(self, account_id):
        """Show account details in the account details tab"""
        self.account_details.load_account_data(account_id)
        self.tabs.setCurrentIndex(1)  # Switch to account details tab

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

    def compile_cobol_programs(self):
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
