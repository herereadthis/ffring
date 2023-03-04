# ffring

## ChatGPT prompt

create a  pep8 valid and pyling-valid flask restAPI that returns user profiles. Make all dependencies in requirements.txt installed in a venv. The files should be in a typical directory structure for a python package. Everything should be in a docker container then have a script that automatically launches the container and restAPI when the computer turns on. The end result is that when I open a web browser and go to localhost:8082/users/john, I should get a JSON of john's user profile

## Cron steps

* Make the shell script executable by running the following command:
  ```shell
  chmod +x build_and_run.sh
  ```
* Open the crontab file by running the following command:
  ```shell
  crontab -e
  ```
* Add the following line at the end of the file to run the shell script at system startup:
  ```shell
  @reboot /path/to/your/project/directory/build_and_run.sh
  ```
  Replace /path/to/your/project/directory with the actual path to your project directory.
* Save and exit the crontab file.

## Local dev

```shell
# Create local environment directory
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required packages
pip3 install -r requirements.txt

# start the application
python3 app.py
```

    