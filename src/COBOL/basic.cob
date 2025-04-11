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
       01  PARAM-ACCOUNT-HOLDER    PIC X(50).
       01  PARAM-ACCOUNT-TYPE      PIC X(10).
       01  PARAM-ACCOUNT-BALANCE   PIC 9(9)V99.
       01  PARAM-STATUS            PIC X(10).
       01  PARAM-OPEN-DATE         PIC X(10).
       01  PARAM-LAST-UPDATE       PIC X(10).

       01  PARAM-FIELD             PIC X(20).
       01  PARAM-VALUE             PIC X(50).
       01  PARAM-DESCRIPTION       PIC X(100).
       
       01  WS-EOF             PIC X VALUE 'N'.
       
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
               WHEN "CREATE-ACCOUNT"
                   PERFORM CREATE-ACCOUNT
               WHEN "GET-ACCOUNT"
                   PERFORM GET-ACCOUNT
               WHEN "LIST-ACCOUNTS"
                   PERFORM LIST-ACCOUNTS
               WHEN "DELETE-ACCOUNT"
                   PERFORM DELETE-ACCOUNT
               WHEN "UPDATE-ACCOUNT"
                   PERFORM UPDATE-ACCOUNT
               WHEN "TRANSACTION"
                   CONTINUE
               WHEN "TRANSFER"
                   CONTINUE
               WHEN "APPLY-INTEREST"
                   CONTINUE
               WHEN "CHARGE-FEE"
                   CONTINUE
               WHEN OTHER
                   DISPLAY "ERROR|Unknown command"
           END-EVALUATE.

       CURRENT-DATE-INTO-PLU.
           MOVE FUNCTION CURRENT-DATE TO CURRENT-DATE-DATA
           STRING CD-YEAR DELIMITED BY SIZE
                    "-" DELIMITED BY SIZE
                    CD-MONTH DELIMITED BY SIZE
                    "-" DELIMITED BY SIZE
                    CD-DAY DELIMITED BY SIZE
           INTO PARAM-LAST-UPDATE.

       GET-AVAILABLE-ACCOUNT-NUMBER.
      * Find and increment the last account number
      * Need to use AR-ACCOUNT-NUMBER here instead of directly
      * PARAM-ACCOUNT-NUMBER because it is the record key
           MOVE HIGH-VALUES TO AR-ACCOUNT-NUMBER
           START ACCOUNT-FILE KEY IS <= AR-ACCOUNT-NUMBER
           IF SUCCESS
               READ ACCOUNT-FILE PREVIOUS RECORD
               IF SUCCESS
                   ADD 1 TO AR-ACCOUNT-NUMBER
                   MOVE AR-ACCOUNT-NUMBER TO PARAM-ACCOUNT-NUMBER
               END-IF
           END-IF.

       MOVE-PARAM-TO-AR-ACCOUNT-AND-READ-FILE.
           MOVE PARAM-ACCOUNT-NUMBER TO AR-ACCOUNT-NUMBER
           READ ACCOUNT-FILE
           IF NOT SUCCESS
               DISPLAY "ERROR|Account not found"
               EXIT PARAGRAPH
           END-IF

       CREATE-ACCOUNT.
           UNSTRING STDIN-LINE DELIMITED BY "|"
                INTO COMMAND, PARAM-ACCOUNT-HOLDER,
                PARAM-ACCOUNT-TYPE, PARAM-ACCOUNT-BALANCE
               
           PERFORM CURRENT-DATE-INTO-PLU
           PERFORM GET-AVAILABLE-ACCOUNT-NUMBER
           
           MOVE PARAM-ACCOUNT-NUMBER TO AR-ACCOUNT-NUMBER
           MOVE PARAM-ACCOUNT-HOLDER TO AR-ACCOUNT-HOLDER
           MOVE PARAM-ACCOUNT-TYPE TO AR-ACCOUNT-TYPE
           MOVE PARAM-ACCOUNT-BALANCE TO AR-ACCOUNT-BALANCE
           MOVE "ACTIVE" TO AR-STATUS
           MOVE PARAM-LAST-UPDATE TO AR-OPEN-DATE
           MOVE PARAM-LAST-UPDATE TO AR-LAST-UPDATE

           WRITE ACCOUNT-RECORD
               INVALID KEY
                   DISPLAY "ERROR|Account creation failed"
               NOT INVALID KEY
                   DISPLAY "OK|" AR-ACCOUNT-NUMBER 
                   "|Account created successfully"
           END-WRITE.

      *     IF SUCCESS
      * Create transaction if the balance is above 0, need to implement
      * the transaction stuff before that though
      *     END-IF.

       GET-ACCOUNT.
              UNSTRING STDIN-LINE DELIMITED BY "|"
                 INTO COMMAND, PARAM-ACCOUNT-NUMBER
                
              MOVE PARAM-ACCOUNT-NUMBER TO AR-ACCOUNT-NUMBER
              READ ACCOUNT-FILE
                INVALID KEY
                     DISPLAY "ERROR|Account not found"
                NOT INVALID KEY
                     DISPLAY "OK|" AR-ACCOUNT-NUMBER 
                     "|" AR-ACCOUNT-HOLDER 
                     "|" AR-ACCOUNT-TYPE 
                     "|" AR-ACCOUNT-BALANCE 
                     "|" AR-STATUS 
                     "|" AR-OPEN-DATE 
                     "|" AR-LAST-UPDATE
              END-READ.

       LIST-ACCOUNTS.
           MOVE LOW-VALUES TO AR-ACCOUNT-NUMBER
           START ACCOUNT-FILE KEY IS >= AR-ACCOUNT-NUMBER
           IF NOT SUCCESS
               DISPLAY "ERROR|No accounts found"
               EXIT PARAGRAPH
           END-IF

           PERFORM UNTIL 1 = 2
                READ ACCOUNT-FILE NEXT RECORD
                     AT END
                          EXIT PERFORM
                     NOT AT END
                          DISPLAY AR-ACCOUNT-NUMBER 
                          "|" AR-ACCOUNT-HOLDER 
                          "|" AR-ACCOUNT-TYPE 
                          "|" AR-ACCOUNT-BALANCE 
                          "|" AR-STATUS 
                          "|" AR-OPEN-DATE 
                          "|" AR-LAST-UPDATE
                          DISPLAY "ACC-DONE"
                END-READ
           END-PERFORM.
       
       DELETE-ACCOUNT.
           UNSTRING STDIN-LINE DELIMITED BY "|"
               INTO COMMAND, PARAM-ACCOUNT-NUMBER

           PERFORM MOVE-PARAM-TO-AR-ACCOUNT-AND-READ-FILE

           DELETE ACCOUNT-FILE
           IF SUCCESS
               DISPLAY "OK|Account deleted successfully"
           ELSE
               DISPLAY "ERROR|Failed to deleted account"
           END-IF.

       UPDATE-ACCOUNT.
           UNSTRING STDIN-LINE DELIMITED BY "|"
           INTO COMMAND, PARAM-ACCOUNT-NUMBER, PARAM-FIELD, PARAM-VALUE

           PERFORM MOVE-PARAM-TO-AR-ACCOUNT-AND-READ-FILE

           EVALUATE PARAM-FIELD
               WHEN "ACCOUNT_HOLDER"
                   MOVE PARAM-VALUE TO AR-ACCOUNT-HOLDER
               WHEN "ACCOUNT_TYPE"
                   MOVE PARAM-VALUE TO AR-ACCOUNT-TYPE
               WHEN "STATUS"
                   MOVE PARAM-VALUE TO AR-STATUS
               WHEN OTHER
                   DISPLAY "ERROR|Unknown PARAM-FIELD"
           END-EVALUATE.

           PERFORM CURRENT-DATE-INTO-PLU
           MOVE PARAM-LAST-UPDATE TO AR-LAST-UPDATE

           REWRITE ACCOUNT-RECORD
           IF SUCCESS
               DISPLAY "OK|Account updated successfully|" PARAM-FIELD
      -        "|" PARAM-VALUE
           ELSE
               DISPLAY "ERROR|Failed to update account"
           END-IF.

       TRANSACTION.
           UNSTRING STDIN-LINE DELIMITED BY "|"
               INTO COMMAND, PARAM-FIELD,
               PARAM-ACCOUNT-NUMBER, PARAM-VALUE, PARAM-DESCRIPTION

      * Start using TR Records

           PERFORM MOVE-PARAM-TO-AR-ACCOUNT-AND-READ-FILE

           EVALUATE PARAM-FIELD
               WHEN "DEPOSIT"
                   CONTINUE
               WHEN "WITHDRAWAL"
                   CONTINUE
               WHEN OTHER
                  DISPLAY "ERROR|Unknown transaction type"
           END-EVALUATE.
           