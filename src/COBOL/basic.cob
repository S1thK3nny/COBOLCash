       IDENTIFICATION DIVISION.
       PROGRAM-ID. BANK-SERVER.
       
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT ACCOUNT-FILE ASSIGN TO "account.dat"
               ORGANIZATION IS INDEXED
               ACCESS MODE IS DYNAMIC
               RECORD KEY IS AR-ACCOUNT-NUMBER
               FILE STATUS IS WS-FILE-STATUS.
           SELECT TRANSACTION-FILE ASSIGN TO "transaction.dat"
               ORGANIZATION IS INDEXED
                ACCESS MODE IS DYNAMIC
                RECORD KEY IS TR-TRANSACTION-ID
                FILE STATUS IS WS-FILE-STATUS.
       
       DATA DIVISION.
       FILE SECTION.
      * ACCOUNT DATA FILE STRUCTURE
       FD ACCOUNT-FILE
           LABEL RECORDS ARE STANDARD.
       01  ACCOUNT-RECORD.
           05 AR-ACCOUNT-NUMBER        PIC 9(6).
           05 AR-ACCOUNT-HOLDER        PIC X(100).
           05 AR-ACCOUNT-TYPE          PIC X(10).
           05 AR-ACCOUNT-BALANCE       PIC 9(9)V99.
           05 AR-STATUS                PIC X(10).
           05 AR-OPEN-DATE             PIC X(10).
           05 AR-LAST-UPDATE           PIC X(10).

       FD TRANSACTION-FILE
           LABEL RECORDS ARE STANDARD.
       01  TRANSACTION-RECORD.
           05 TR-TRANSACTION-ID           PIC 9(10).
           05 TR-ACCOUNT-NUMBER           PIC 9(6).
           05 TR-DATE                     PIC X(10).
           05 TR-TYPE                     PIC X(10).
           05 TR-AMOUNT                   PIC 9(9)V99.
           05 TR-BALANCE-AFTER            PIC 9(9)V99.
           05 TR-NOTES                    PIC X(100).


       WORKING-STORAGE SECTION.
       01 WS-FILE-STATUS       PIC X(2).
           88 SUCCESS          VALUE "00".
           88 END-OF-FILE      VALUE "10".
           88 INVALID-RECORD   VALUE "22".

       01 STDIN-LINE         PIC X(200).
       01 COMMAND            PIC X(50).

       01 CURRENT-DATE-DATA.
           05 CD-YEAR          PIC 9(4).
           05 CD-MONTH         PIC 9(2).
           05 CD-DAY           PIC 9(2).

       01  PARAM-ACCOUNT-NUMBER    PIC 9(6).
       01  PARAM-ACCOUNT-HOLDER    PIC X(100).
       01  PARAM-ACCOUNT-TYPE      PIC X(10).
       01  PARAM-ACCOUNT-BALANCE   PIC 9(9)V99.
       01  PARAM-STATUS            PIC X(10).
       01  PARAM-OPEN-DATE         PIC X(10).
       01  PARAM-LAST-UPDATE       PIC X(10).
       
       01 WS-EOF             PIC X VALUE 'N'.
       
       PROCEDURE DIVISION.
           PERFORM INITIALIZE-FILES

           PERFORM UNTIL WS-EOF = 'Y'
               ACCEPT STDIN-LINE FROM SYSIN
               IF STDIN-LINE = SPACES
                   MOVE 'Y' TO WS-EOF
               ELSE
                   PERFORM PROCESS-COMMAND
               END-IF
           END-PERFORM
           CLOSE ACCOUNT-FILE TRANSACTION-FILE
           GOBACK.

       INITIALIZE-FILES.
           OPEN I-O ACCOUNT-FILE
               IF NOT SUCCESS
                   OPEN OUTPUT ACCOUNT-FILE
                   CLOSE ACCOUNT-FILE
                   OPEN I-O ACCOUNT-FILE
               END-IF

           OPEN I-O TRANSACTION-FILE
               IF NOT SUCCESS
                   OPEN OUTPUT TRANSACTION-FILE
                   CLOSE TRANSACTION-FILE
                   OPEN I-O TRANSACTION-FILE
               END-IF.
       
       PROCESS-COMMAND.
           UNSTRING STDIN-LINE DELIMITED BY "|"
               INTO COMMAND
       
           EVALUATE COMMAND
               WHEN "CREATE"
                   PERFORM CREATE-ACCOUNT
               WHEN OTHER
                   DISPLAY "ERROR|Unknown command"
           END-EVALUATE.

       CURRENT-DATE-INTO-CDD.
           MOVE FUNCTION CURRENT-DATE TO CURRENT-DATE-DATA
           STRING CD-YEAR DELIMITED BY SIZE
                    "-" DELIMITED BY SIZE
                    CD-MONTH DELIMITED BY SIZE
                    "-" DELIMITED BY SIZE
                    CD-DAY DELIMITED BY SIZE
           INTO PARAM-LAST-UPDATE.

       CREATE-ACCOUNT.
           UNSTRING STDIN-LINE DELIMITED BY "|"
                INTO COMMAND, PARAM-ACCOUNT-HOLDER,
                PARAM-ACCOUNT-TYPE, PARAM-ACCOUNT-BALANCE
               
           PERFORM CURRENT-DATE-INTO-CDD
           
           MOVE 1 TO PARAM-ACCOUNT-NUMBER
           MOVE PARAM-ACCOUNT-NUMBER TO AR-ACCOUNT-NUMBER
           MOVE PARAM-ACCOUNT-HOLDER TO AR-ACCOUNT-HOLDER
           MOVE PARAM-ACCOUNT-TYPE TO AR-ACCOUNT-TYPE
           MOVE PARAM-ACCOUNT-BALANCE TO AR-ACCOUNT-BALANCE
           MOVE "ACTIVE" TO AR-STATUS
           MOVE PARAM-LAST-UPDATE TO AR-OPEN-DATE
           MOVE PARAM-LAST-UPDATE TO AR-LAST-UPDATE
           DISPLAY     "INFO|Creating account"
           DISPLAY     "INFO|Account Number: " AR-ACCOUNT-NUMBER
           DISPLAY     "INFO|Account Holder: " AR-ACCOUNT-HOLDER
           DISPLAY     "INFO|Account Type: " AR-ACCOUNT-TYPE
           DISPLAY     "INFO|Account Balance: " AR-ACCOUNT-BALANCE
           DISPLAY     "INFO|Account Status: " AR-STATUS
           DISPLAY     "INFO|Account Open Date: " AR-OPEN-DATE
           DISPLAY     "INFO|Account Last Update: " AR-LAST-UPDATE.