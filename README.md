# Nauclerus Logbook

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Daniel-Fernandez-951/GA-Pilot-Logbook">
    <img src="images/logo_nauclerusV0.png" alt="Logo" width="746" height="261">
  </a>

  <h3 align="center">General Aviation Pilot Logbook API </h3>


**API endpoint for general aviation pilots and student pilots to store their logbook data**. Nauclerus runs in a Docker container,
allowing secure **local** access and redundant storage using NAS device that supports running Docker containers. Nauclerus can
also send your logbook data to a cloud service, ensuring there's always a backup of your logbook.  




### Known Issues
- When connecting to *Heroku PostgresQL Datastore*:
    - `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`
    
_Solution_: Navigate to `.env` file and change your database URI from `postgres://` --> `postgresql://`