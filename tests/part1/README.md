Part 1 test datasets for `q2` through `q6`.

Each `.sql` file is a small, self-contained dataset meant to exercise one
query's edge cases from the handout. Load them after `schema.ddl`, then load
the matching query file.

Example:

```powershell
psql -d csc343 -v ON_ERROR_STOP=1 `
  -f schema.ddl `
  -f tests/part1/q2_helpfulness_core.sql `
  -f part1/q2.sql `
  -c "TABLE Recommender.q2;"
```

You can also use `tests/part1/run-part1-test.ps1`.
