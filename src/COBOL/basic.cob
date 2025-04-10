       IDENTIFICATION DIVISION.
       PROGRAM-ID. BANK-SERVER.
       
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       
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
