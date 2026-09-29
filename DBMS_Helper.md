# 🗄️ DBMS Master Exam Helper & Quick Revision Guide

A comprehensive, high-yield reference guide for **Database Management Systems (DBMS)** tailored for B.Tech / University exams, recurring PYQs, and rapid revision.

---

## 📌 Quick Navigation
1. [Unit-by-Unit High-Yield Topics & Core Concepts](#-unit-by-unit-high-yield-topics)
2. [Most Repeated PYQ Patterns (Must-Prepare)](#-most-repeated-pyq-patterns)
3. [Key Formulas, Rules & Thumb Rules](#-key-formulas-rules--cheat-sheet)
4. [High-Probability Differences (Comparison Tables)](#-high-probability-differences-tables)
5. [Exam Strategy & Scoring Tips](#-exam-day-strategy)

---

## 🎯 Unit-by-Unit High-Yield Topics

### 🔹 Unit 1: Introduction, Architecture & ER Modeling
- **3-Schema Architecture**:
  - *Internal / Physical Level*: How data is physically stored (indices, B-Trees, hashing).
  - *Conceptual / Logical Level*: What data is stored and entity relationships (tables, constraints).
  - *External / View Level*: User-specific tailored views.
- **Data Independence**:
  - *Physical Data Independence*: Changing physical storage (e.g., adding indexes) without altering logical schema.
  - *Logical Data Independence*: Changing conceptual schema (e.g., adding columns) without breaking existing external views.
- **ER Model Elements**:
  - *Entities* (Rectangles), *Attributes* (Ovals; Key = Underlined, Multivalued = Double Oval, Derived = Dashed Oval), *Relationships* (Diamonds), *Weak Entity* (Double Rectangle + Dashed Underline for Partial Key/Discriminator).
- **Extended ER Concepts**:
  - *Generalization* (Bottom-up: Car, Truck $\rightarrow$ Vehicle)
  - *Specialization* (Top-down: Employee $\rightarrow$ Developer, Manager)
  - *Aggregation* (Treating a relationship set as an abstract entity).
- **ER to Relational Table Reduction**:
  - Strong Entity $\rightarrow$ Separate table with Primary Key.
  - Weak Entity $\rightarrow$ Table with Owner Primary Key + Partial Key.
  - 1:N Relationship $\rightarrow$ Foreign Key on the "Many" side.
  - M:N Relationship $\rightarrow$ New junction/bridge table with PKs of both participating entities.

---

### 🔹 Unit 2: Relational Model, Algebra & SQL
- **Integrity Constraints**:
  - *Entity Integrity*: Primary key attribute cannot contain `NULL`.
  - *Referential Integrity*: Foreign key value must either exist as a primary key in referenced relation or be `NULL`.
  - *Domain Constraint*: Attribute value must belong to valid predefined domain.
- **Relational Algebra (Fundamental Operations)**:
  - Selection: $\sigma_{\text{condition}}(R)$ (Filters rows)
  - Projection: $\pi_{\text{attributes}}(R)$ (Selects columns, removes duplicates)
  - Cartesian Product: $R \times S$
  - Union ($\cup$), Set Difference ($-$), Intersection ($\cap$) — *Require Union Compatibility (same degree and corresponding domains)*
  - Natural Join ($R \bowtie S$) — Combines matching tuples on common attribute names.
- **SQL Clauses & Execution Order**:
  - Writing order: `SELECT` $\rightarrow$ `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `ORDER BY`
  - Execution order: `FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY`
- **Joins in SQL**:
  - `INNER JOIN`: Only matching records from both tables.
  - `LEFT / RIGHT OUTER JOIN`: All records from left/right + matching from other (unmatched filled with NULL).
  - `FULL OUTER JOIN`: All records from both tables with NULLs where matches don't exist.

---

### 🔹 Unit 3: Database Design, Normalization & Functional Dependencies
- **Functional Dependency (FD)**: $X \rightarrow Y$ means if two tuples agree on $X$, they must agree on $Y$.
- **Armstrong’s Axioms**:
  1. *Reflexivity*: If $Y \subseteq X$, then $X \rightarrow Y$.
  2. *Augmentation*: If $X \rightarrow Y$, then $XZ \rightarrow YZ$.
  3. *Transitivity*: If $X \rightarrow Y$ and $Y \rightarrow Z$, then $X \rightarrow Z$.
  4. *Decomposition*: If $X \rightarrow YZ$, then $X \rightarrow Y$ and $X \rightarrow Z$.
  5. *Union*: If $X \rightarrow Y$ and $X \rightarrow Z$, then $X \rightarrow YZ$.
- **Normal Forms Hierarchy**:
  - **1NF**: Atomic values only (no multi-valued/composite attributes).
  - **2NF**: In 1NF + **No Partial Dependency** (No Non-Prime attribute depends on a proper subset of any Candidate Key).
  - **3NF**: In 2NF + **No Transitive Dependency** (For every non-trivial FD $X \rightarrow Y$, either $X$ is a Super Key or $Y$ is a Prime Attribute).
  - **BCNF (Boyce-Codd NF)**: For every non-trivial FD $X \rightarrow Y$, $X$ **must** be a Super Key.
  - **4NF**: Addresses Multi-Valued Dependencies ($X \twoheadrightarrow Y$).
  - **5NF / PJNF**: Addresses Join Dependencies (Lossless decomposition into 3 or more tables).
- **Decomposition Properties**:
  - *Lossless Join*: Natural join of decomposed tables must produce original relation without spurious tuples ($R_1 \cap R_2 \rightarrow R_1$ OR $R_1 \cap R_2 \rightarrow R_2$).
  - *Dependency Preservation*: $(F_1 \cup F_2)^+ = F^+$.

---

### 🔹 Unit 4: Transaction Processing & Recovery
- **ACID Properties**:
  - **Atomicity**: "All or Nothing" (Managed by Recovery Manager / Log).
  - **Consistency**: Database transitions from one valid state to another.
  - **Isolation**: Concurrent transactions execute without interference (Managed by Concurrency Controller).
  - **Durability**: Committed updates persist even during crashes (Managed by Log/Recovery Manager).
- **Transaction States**:
  - `Active` $\rightarrow$ `Partially Committed` $\rightarrow$ `Committed`
  - `Active / Partially Committed` $\rightarrow$ `Failed` $\rightarrow$ `Aborted` (Rollback) $\rightarrow$ `Terminated`.
- **Serializability**:
  - *Conflict Serializable*: Schedule can be transformed into a serial schedule by swapping non-conflicting operations. Tested using a **Precedence Graph (Serialization Graph)**: If cycle exists $\rightarrow$ **Not Conflict Serializable**.
  - *View Serializable*: Weaker condition; tested through initial read, write-read, and final write conditions.
- **Recoverability Classification**:
  - *Recoverable*: If $T_j$ reads data written by $T_i$, then $T_i$ must commit before $T_j$ commits.
  - *Cascadeless*: $T_j$ reads data written by $T_i$ only **after** $T_i$ has committed (avoids cascading rollbacks).
  - *Strict*: $T_j$ can neither read nor write data modified by $T_i$ until $T_i$ commits/aborts.
- **Log-Based Recovery**:
  - *Deferred Update*: Changes written to DB only after commit. Redo only needed.
  - *Immediate Update*: Changes written to DB while active. Requires Undo & Redo.
  - *Checkpoints*: Periodic sync point that avoids scanning the entire log history during recovery.

---

### 🔹 Unit 5: Concurrency Control Techniques
- **Locking Protocols**:
  - *Shared Lock (S)*: Read-only access; multiple transactions can hold S-locks concurrently.
  - *Exclusive Lock (X)*: Read and Write access; only one transaction can hold X-lock.
  - **Two-Phase Locking (2PL)**:
    - *Growing Phase*: Locks acquired, none released.
    - *Shrinking Phase*: Locks released, none acquired.
    - Ensures conflict serializability, but can cause **deadlocks**.
  - **Strict 2PL**: Releases all exclusive (X) locks only at transaction commit/abort (Guarantees strict schedule & no cascading aborts).
  - **Rigorous 2PL**: Releases ALL locks (S and X) only at commit/abort.
- **Timestamp-Based Ordering Protocol**:
  - Assigns unique timestamp $TS(T_i)$ upon arrival.
  - For $T_i$ issuing $Read(Q)$: If $TS(T_i) < W\text{-timestamp}(Q)$, roll back $T_i$.
  - For $T_i$ issuing $Write(Q)$: If $TS(T_i) < R\text{-timestamp}(Q)$ or $TS(T_i) < W\text{-timestamp}(Q)$, roll back $T_i$.
  - Guarantees conflict serializability without deadlocks.
- **Validation-Based (Optimistic) Protocol**:
  - 3 Phases: Read $\rightarrow$ Validation $\rightarrow$ Write.
  - Best suited when conflict probability is low.

---

## 📊 High-Probability Differences Tables

### 1. DDL vs DML vs DCL vs TCL
| Feature | DDL (Definition) | DML (Manipulation) | DCL (Control) | TCL (Transaction) |
|---|---|---|---|---|
| **Purpose** | Defines database schema/structure | Manipulates table data | Manages permissions/access | Manages transaction states |
| **Commands** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME` | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | `GRANT`, `REVOKE` | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |
| **Auto-Commit** | Yes (Permanent immediately) | No (Can be rolled back) | Yes | N/A |

---

### 2. DELETE vs TRUNCATE vs DROP
| Feature | `DELETE` | `TRUNCATE` | `DROP` |
|---|---|---|---|
| **Type** | DML | DDL | DDL |
| **Operation** | Deletes specific rows (`WHERE`) | Deletes all rows at once | Removes entire table schema + data |
| **Rollback** | Possible (logged row by row) | Not rollbackable (in standard mode) | Cannot be rolled back |
| **Speed** | Slower for large datasets | Very fast (resets high-water mark) | Instantaneous table removal |

---

### 3. 3NF vs BCNF
| Criteria | 3NF | BCNF |
|---|---|---|
| **Condition for $X \rightarrow Y$** | $X$ is Super Key **OR** $Y$ is Prime Attribute | $X$ **MUST** be Super Key |
| **Strictness** | Relaxed (Allows prime on RHS) | Strict (No non-trivial FD unless LHS is SK) |
| **Dependency Preservation** | **Always guaranteed** | May or may not preserve all dependencies |
| **Lossless Join** | Always achievable | Always achievable |

---

### 4. Conflict Serializability vs View Serializability
| Aspect | Conflict Serializability | View Serializability |
|---|---|---|
| **Checking Mechanism** | Precedence Graph (Cycle detection in polynomial time $O(V+E)$) | NP-Complete problem (Harder to check for large schedules) |
| **Scope** | Strict subset of view serializability | Broader (Includes all conflict serializable schedules + some blind write schedules) |
| **Constraint** | Swapping non-conflicting adjacent operations | Preserving view equivalence (read-from & final writes) |

---

## ⚡ Key Formulas, Rules & Cheat Sheet

1. **Closure of Attribute Set $(X^+)$**:
   - Start with $X^+ = X$.
   - For every FD $A \rightarrow B$, if $A \subseteq X^+$, then $X^+ = X^+ \cup B$.
   - If $X^+$ includes all attributes of relation $R$, then $X$ is a **Super Key**.
   - If no proper subset of $X$ is a Super Key, then $X$ is a **Candidate Key**.

2. **Prime vs Non-Prime Attributes**:
   - **Prime Attribute**: Part of *at least one* Candidate Key.
   - **Non-Prime Attribute**: Not part of *any* Candidate Key.

3. **Lossless Join Condition for Decomposition $R \rightarrow (R_1, R_2)$**:
   $$R_1 \cap R_2 \rightarrow R_1 \quad \text{OR} \quad R_1 \cap R_2 \rightarrow R_2$$
   *(Common attributes must form a Super Key in either $R_1$ or $R_2$)*.

4. **Number of Super Keys Calculation**:
   - For a relation with $n$ attributes and a Candidate Key of size $k$:
     $$\text{Total Super Keys} = 2^{n - k}$$

---

## 🏆 Exam Day Strategy
- **For 2-Mark Questions**:
  - State the definition in 1 line.
  - Give the exact mathematical condition or syntax.
  - Give a 1-line mini example.
- **For 10-Mark Questions**:
  - Always draw a neat, labeled block diagram (DBMS Architecture, 3-Schema, ER diagram, Transaction State Diagram, Precedence Graph).
  - Structure answers into: **Definition $\rightarrow$ Properties/Rules $\rightarrow$ Working Example $\rightarrow$ Advantages/Disadvantages**.
  - For normalization questions, write down all Candidate Keys, Prime/Non-Prime sets, and test FDs one by one explicitly.
