# Design decisions

| Question | Decision |
|---|---|
| Where are tickets stored? | A `list` of `dict`s, passed as the first argument to every function. |
| How is invalid input signalled? | Exceptions deriving from `CampusFlowError` (`ValidationError`, `TicketNotFoundError`, `WorkflowError`, `StorageError`). The CLI catches them and prints `Error: <message>`. |
| What do functions return? | `create_ticket`, `assign_ticket`, `change_status`, `reopen_ticket` return the updated ticket. |
| Who owns JSON? | `storage.py` (`load_tickets`, `save_tickets`); only `cli.py` calls it. |
| How do we test without input()? | Business logic never prompts. `cli.run` takes `input_func` / `output_func` so tests script it. |
| Corruption safety | Validate first, mutate last; saves are atomic (temp file + `os.replace`). |
| Queue meaning | "Open, unresolved" = status `open` (work waiting to be picked up). |
| ID generation | Highest existing number + 1, so IDs stay unique after reload. |

## Ownership
- **Engineer A:** `tickets.py` (creation, validation, priority) + `tests/test_tickets.py`
- **Engineer B:** `workflow.py`, `reports.py` + `tests/test_workflow.py`
- **Both:** `storage.py`, `cli.py`, `tests/test_storage.py`, docs
