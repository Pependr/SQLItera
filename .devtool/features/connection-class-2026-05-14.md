---
id: "connection-class-2026-05-14"
status: "in-progress"
priority: "medium"
assignee: null
epic: "CoreFunctionality"
dueDate: null
created: "2026-05-14T15:44:04.093Z"
modified: "2026-05-14T15:49:35.706Z"
completedAt: null
labels: []
order: "a0"
---
# Connection class

Connection class encapsulates all direct interactions with the connected database. It basically abstracts away direct calls on sqlite3.Connection and sqlite3.Cursor's methods, making things safer by managing those objects for you and less verbose by providing a toolkit for basic interactions.