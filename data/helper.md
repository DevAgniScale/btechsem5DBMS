## Topic: Important Topics & Unit-Wise Weightage
- **[CORE_TOPICS]**:
  - **Unit 1 (Architecture & ER)**: 3-Schema Architecture, Physical vs Logical Data Independence, ER Diagram construction, ER to Relational Table reduction rules.
  - **Unit 2 (Relational Model & SQL)**: Relational Algebra operators (Select, Project, Joins), SQL Joins & Subqueries, Integrity Constraints (Entity, Referential), differences (DELETE vs TRUNCATE vs DROP, DDL vs DML).
  - **Unit 3 (Design & Normalization - Highest Priority)**: Finding Candidate Keys using Attribute Closure, Minimal/Canonical Cover, Normal Forms (1NF, 2NF, 3NF, BCNF, 4NF/MVD), Lossless Join & Dependency Preservation test.
  - **Unit 4 (Transactions & Recovery)**: ACID properties, Precedence Graph cycle test for Conflict Serializability, Recoverable vs Cascadeless vs Strict schedules, Log-Based Recovery (Deferred vs Immediate Update).
  - **Unit 5 (Concurrency Control)**: Two-Phase Locking (Basic 2PL, Strict 2PL, Rigorous 2PL), Timestamp Ordering Protocol, Validation-based protocol, Deadlock detection and recovery.

## Topic: High-Yield Numericals & 10-Mark Questions
- **[KEY_PATTERNS]**:
  - **Normalization Problem**: Given relation $R$ and set of FDs $F$, find all Candidate Keys, Prime/Non-Prime attributes, determine highest normal form, and decompose into 3NF / BCNF.
  - **Serializability Schedule Problem**: Given concurrent schedule $S$, draw the Precedence Graph to test Conflict Serializability, find equivalent serial schedule, and test recoverability.
  - **ER Design Problem**: Draw a complete ER diagram for a given system (e.g. University, Hospital, Company) and convert entities/relationships into relational schemas.
  - **Relational Algebra & SQL**: Write RA expressions and SQL queries for a given multi-table schema.
  - **Concurrency Comparison**: Explain 2PL vs Timestamp Ordering protocols with working diagrams and deadlock behavior.

## Topic: 2-Mark Short Answer Definitions & Key Differences
- **[KEY_DEFINITIONS]**:
  - **DDL vs DML**: DDL defines schema (`CREATE`, `ALTER`, `DROP`, `TRUNCATE` - auto-committed); DML manages data (`SELECT`, `INSERT`, `UPDATE`, `DELETE` - rollbackable).
  - **DELETE vs TRUNCATE vs DROP**: `DELETE` removes selected rows (DML, slow, logged); `TRUNCATE` deletes all rows (DDL, fast); `DROP` deletes entire table structure.
  - **Super Key vs Candidate Key**: Super Key is any attribute set uniquely identifying a tuple; Candidate Key is a minimal Super Key (no redundant attributes).
  - **3NF vs BCNF**: 3NF allows prime attribute on RHS ($X \rightarrow Y$ requires $X$ is Super Key OR $Y$ is Prime); BCNF strictly requires $X$ is Super Key.
  - **Lossless Join Rule**: $(R_1 \cap R_2) \rightarrow R_1$ OR $(R_1 \cap R_2) \rightarrow R_2$.
  - **Conflict vs View Serializability**: Conflict serializable is tested via cycle-free Precedence Graph; View serializable includes blind-write schedules.

## Topic: Exam Strategy, Time Management & Revision Guide
- **[GUIDELINES]**:
  - **Priority 1 (Must-Pass Core)**: Normalization (Candidate Keys, 2NF/3NF/BCNF), Conflict Serializability Precedence Graph, ACID properties, ER reduction rules.
  - **Priority 2 (High Scoring)**: Relational Algebra queries, SQL Joins & Aggregate functions, 2PL locking protocols, 3-Schema Architecture & Data Independence.
  - **Priority 3 (Theory & Buffer)**: Recovery techniques (Log-based, Checkpoints), Deadlock handling, MVD & 4NF, Timestamp Ordering.
  - **Answer Presentation**: In 10-markers, always include a neat labeled diagram (Architecture, State transitions, Precedence Graph) and highlight key terms.
