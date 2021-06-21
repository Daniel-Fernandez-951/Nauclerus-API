<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Daniel-Fernandez-951/GA-Pilot-Logbook">
    <img src="images/logo_nauclerusV0.png" alt="Logo" width="746" height="261">
  </a>

  <h3 align="center">General Aviation Pilot Logbook API </h3>

-----------------------

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
          <ul>
            <li><a href="#datastorageoptions">Data Storage Options</a></li>
          </ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
    <li><a href="#knownissues">Known Issues</a></li>
  </ol>
</details>

------------------------------

<!-- ABOUT THE PROJECT -->
## About Nauclerus Logbook API

**API endpoint for general aviation pilots and student pilots to store their logbook data**. Nauclerus runs in a Docker container,
allowing secure **local** access and redundant storage using NAS device that supports running Docker containers. Nauclerus can
also send your logbook data to a cloud service, ensuring there's always a backup of your logbook.


### Built With
For more details, checkout [requirements.txt](https://github.com/Daniel-Fernandez-951/GA-Pilot-Logbook/blob/master/requirements.txt) file.

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [SQLAlchemy](https://docs.sqlalchemy.org/)
* [Numpy](https://numpy.org/doc/)
* [Pandas](https://pandas.pydata.org/)


<!-- GETTING STARTED -->
## Getting Started

Instructions for running the Dockerfile locally. Running this on a NAS device (Synology or QNAP), please refer
to NAS distributor documentation for running Nauclerus API on your device.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

#### Data Storage Options
* **Local Storage**: 
  - Change `/app/sqlUtils/database.py`
    ```python
    from os import getenv
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    
    load_dotenv()
    
    SQLALCHEMY_DATABASE_URL = getenv('HEROKU_SQL_DB')
    
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    
    Base = declarative_base()
    ```

* **Cloud Database Storage**:
  - Create `/.env` file
    - ```dotenv
      HEROKU_SQL_DB=sqlite:///./sql_app.db
      ```
      Change `sql_app.db` to any file name you'd like!

### Installation


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements



<!-- KNOWN ISSUES -->
## Known Issues
- When connecting to *Heroku PostgresQL Datastore*:
    - `sqlalchemy.exc.NoSuchModuleError: Can't load plugin: sqlalchemy.dialects:postgres`
    
_Solution_: Navigate to `.env` file and change your database URI from `postgres://` --> `postgresql://`