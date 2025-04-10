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
       01 COMMAND            PIC X(10).
       01 ACCOUNT-NUMBER     PIC 9(6).
       01 AMOUNT             PIC 9(5)V99.
       01 DESCRIPTION        PIC X(50).
       
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
               INTO COMMAND, ACCOUNT-NUMBER, AMOUNT, DESCRIPTION
       
           EVALUATE COMMAND
               WHEN "DEPOSIT"
                   DISPLAY "OK|Deposited $" AMOUNT " into account " 
      -                    ACCOUNT-NUMBER
               WHEN OTHER
                   DISPLAY "ERROR|Unknown command"
           END-EVALUATE.
