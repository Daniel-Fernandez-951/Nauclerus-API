# GA-Pilot-Logbook
API endpoint for general aviation pilots and student-pilots to store their logbook data.



### Known Errors
- When connecting to *Heroku PostgresQL Datastore*:
    - `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`
    
_Solution_: Navigate to `.env` file and change your database URI from `postgres://` --> `postgresql://`