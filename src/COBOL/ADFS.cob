      * ACCOUNT DATA FILE STRUCTURE
       FD ACCOUNT-FILE
           LABEL RECORDS ARE STANDARD.
           01 ACCOUNT-RECORD.
               05 AR-ACCOUNT-NUMBER        PIC 9(6).
               05 AR-ACCOUNT-HOLDER        PIC X(100).
               05 AR-ACCOUNT-TYPE          PIC X(10).
               05 AR-ACCOUNT-BALANCE       PIC 9(9)V99.
               05 AR-STATUS                PIC X(10).
               05 AR-OPEN-DATE             PIC X(10).
               05 AR-LAST-UPDATE           PIC X(10).

       FD TRANSACTION-FILE
           LABEL RECORDS ARE STANDARD.
           01 TRANSACTION-RECORD.
                05 TR-TRANSACTION-ID           PIC 9(10).
                05 TR-ACCOUNT-NUMBER           PIC 9(6).
                05 TR-DATE                     PIC X(10).
                05 TR-TYPE                     PIC X(10).
                05 TR-AMOUNT                   PIC 9(9)V99.
                05 TR-BALANCE-AFTER            PIC 9(9)V99.
                05 TR-NOTES                    PIC X(100).