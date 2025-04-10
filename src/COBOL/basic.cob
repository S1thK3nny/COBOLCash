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
       WORKING-STORAGE SECTION.
       
       01 WS-FILE-STATUS       PIC X(2).
           88 SUCCESS          VALUE "00".
           88 END-OF-FILE      VALUE "10".
           88 INVALID-RECORD   VALUE "22".

       01 STDIN-LINE         PIC X(200).
       01 COMMAND            PIC X(10).
       01 ACCOUNT-NUMBER     PIC 9(6).
       01 AMOUNT             PIC 9(5)V99.
       01 DESCRIPTION        PIC X(50).
       
       01 WS-EOF             PIC X VALUE 'N'.
       
       PROCEDURE DIVISION.
           PERFORM UNTIL WS-EOF = 'Y'
               ACCEPT STDIN-LINE FROM SYSIN
               IF STDIN-LINE = SPACES
                   MOVE 'Y' TO WS-EOF
               ELSE
                   PERFORM PROCESS-COMMAND
               END-IF
           END-PERFORM
       
           GOBACK.
       
       PROCESS-COMMAND.
           UNSTRING STDIN-LINE DELIMITED BY "|"
               INTO COMMAND, ACCOUNT-NUMBER, AMOUNT, DESCRIPTION
       
           EVALUATE COMMAND
               WHEN "DEPOSIT"
                   DISPLAY "OK|Deposited $" AMOUNT " into account " 
      -                    ACCOUNT-NUMBER
               WHEN OTHER
                   DISPLAY "ERROR|Unknown command"
           END-EVALUATE.
