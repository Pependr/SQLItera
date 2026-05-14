---
id: "scheme-classes-2026-05-14"
status: "todo"
priority: "medium"
assignee: null
epic: "CoreFunctionality"
dueDate: null
created: "2026-05-14T15:45:21.508Z"
modified: "2026-05-14T15:51:09.089Z"
completedAt: null
labels: []
order: "a1"
---
Scheme classes

Schemes represent the objects and data structures of SQLite. They are responsible for storing certain properties that you can specify (like a default value for a column) and constructing queries for interacting with those objects, but not executing them. Schemes are immutable, but they have methods for coping and creating new schemes based off themselves. Schemes are composable. For example, a table consists of a set of columns, and the table must not know anything about the certain type of a column it gets, so any possible set of columns works.