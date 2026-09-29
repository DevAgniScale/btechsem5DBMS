# UNIT IV — Transaction Processing Concept

---

## Topic: Transaction System (ACID Properties, Transaction States, Reasons for Failure)
- **[2025]** Section A (1.f): Explain properties of Transaction.
- **[2021]** Section A (1.g): What are ACID properties of Transaction?
- **[2021]** Section A (1.h): What are various reasons for transaction failure?
- **[2022]** Section A (i): When is a transaction Rolled Back?
- **[2022]** Section B (d): List ACID properties of transaction. Explain the usefulness of each. What is the importance of log?
- **[2023]** Section A (g): Discuss Consistency and Isolation property of a transaction.
- **[2023]** Section A (h): Draw a state diagram and discuss the typical states that a transaction goes through during execution.
- **[2024-I]** Section A (g): Define a transaction in the context of database management.
- **[2024-II]** Section A (g): Name one property of ACID.
- **[2024-II]** Section C (7.b): Explain how transaction scheduling affects the execution of transactions in a database system.

## Topic: Testing of Serializability
- **[2021]** Section B (2.d): Explain the method of testing the serializability. Consider schedules S1 and S2 — check whether they are conflict equivalent or not.
- **[2022]** Section C (7.a): Identify whether given schedule S: R1(X) R2(X) R2(Y) W2(Y) R1(Y) W1(X) is equivalent to a serial schedule or not.
- **[2024-I]** Section C (7.a): What is serializability of transaction scheduling, and how can you determine if a schedule is serializable?

## Topic: Serializability of Schedules (Conflict & View Serializable Schedule)
- **[2025]** Section C (6.a): Illustrate Conflict Serializable Schedule. Check the given Schedule S1 (R1(X), R2(X), R2(Y), W2(Y), R1(Y), W1(X)) is Conflict Serializable and View Serializable or not.
- **[2021]** Section C (6.a): What is Conflict Serializable Schedule? Check the given Schedule S1 is Conflict Serializable or not?
- **[2022]** Section C (6.a): Describe serializable schedule. Discuss conflict serializability with suitable example.
- **[2023]** Section A (j): Describe how view serializability is related to conflict serializability.
- **[2023]** Section C (6.b): State whether given schedules S1 and S2 for transactions T1, T2, and T3 are serializable or not, and write equivalent serial schedules.
- **[2024-I]** Section C (7.b): Provide examples of transaction schedules and analyze whether they are conflict serializable and/or view serializable.
- **[2024-II]** Section C (7.a): Define Conflict Serializability and View Serializability and explain their differences.

## Topic: Recoverability (Recoverable, Cascadeless, Strict Schedules)
- **[2025]** Section C (6.b): Explain schedule and transaction. Define the concepts of recoverable, cascade less, and strict schedules, and compare them in terms of recoverability.
- **[2023]** Section B (d): Define recoverable, cascade less, and strict schedules, and compare them in terms of their recoverability.
- **[2023]** Section C (6.a): Determine the strictest recoverability condition that schedules S1, S2, and S3 satisfy.

## Topic: Recovery from Transaction Failures / Log Based Recovery
- **[2025]** Section B (2.d): Determine different types of failures in case of transactions and how it can be recovered based on log file. Explain with suitable example.
- **[2023]** Section B (e): Discuss the immediate update recovery technique in both single-user and multiuser environments.

## Topic: Checkpoints
- No PYQs for this topic.

## Topic: Deadlock Handling
- **[2025]** Section C (7.b): Explain deadlock. What are the necessary conditions for it? How it can be detected and recovered?
- **[2021]** Section C (6.b): Explain Deadlock Handling with Suitable Example.
- **[2022]** Section C (6.b): Discuss the procedure of deadlock detection and recovery in transaction.

## Topic: Distributed Database (Distributed Data Storage, Concurrency Control, Directory System)
- No PYQs for this topic.
