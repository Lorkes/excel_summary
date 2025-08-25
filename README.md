# Setup guide
## System requirements
- Docker compose
- git

## Quick setup
1. install git from https://git-scm.com/downloads (if not installed)
2. Install docker compose following instructions at https://docs.docker.com/compose/install/ (select appropriate option for your operating system and depending on your preferences - command-line (CLI) or graphical (GUI) application)
3. Clone the project repository via `git clone git@github.com:Lorkes/excel_summary.git`
4. Navigate to the project directory
5. Copy `example.env` file into new `.env` file
6. It is recommended to update the values with some meaningful/custom ones, but default will work as well
7. Execute
    ```shell
    docker compose up --build
    ```
8. You should be able to access http://127.0.0.1:8000/
9. Congratulations! Your app is working now. You should be able to upload the file at http://127.0.0.1:8000/summary/ (or send it via Postman, note trailing `/`)

# Troubleshooting
## Error: That port is already in use/Bind for 0.0.0.0:8000 failed: port is already allocated
- ### Reason: default port used to start django app is 8000, looks like there is something else already running on such port on your system
- ### Solution: either turn off the service/app which occupies port 8000 or start this app with different port - customize value HOST_PORT=XXXX in your .env file

# Swagger
Available under
- http://127.0.0.1:8000/api/schema/
- http://127.0.0.1:8000/api/schema/redoc/
- http://127.0.0.1:8000/api/schema/swagger-ui/
