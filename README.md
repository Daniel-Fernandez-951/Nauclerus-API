<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Daniel-Fernandez-951/GA-Pilot-Logbook">
    <img src="images/logo_nauclerusV0.png" alt="Logo" width="746" height="261">
  </a>

  <h3 align="center">General Aviation Pilot Logbook API </h3>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-nauclerus-logbook-api">About Nauclerus Logbook API</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



## About Nauclerus Logbook API

**API endpoint for general aviation pilots and student pilots to store their logbook data**. Nauclerus runs in a Docker container,
allowing secure **local** access and redundant storage using NAS device that supports running Docker containers. Nauclerus can
also send your logbook data to a cloud service, ensuring there's always a backup of your logbook.  


### Built With
<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
  <img alt="Logo" width="180" height="180">
</p>


### Known Issues
- When connecting to *Heroku PostgresQL Datastore*:
    - `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`
    
_Solution_: Navigate to `.env` file and change your database URI from `postgres://` --> `postgresql://`