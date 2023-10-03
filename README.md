# TuringFit

TuringFit ([turingfit.com](https://turingfit.com)) is a Strava weekly ranking app for sport challenges.

![Screenshot](screenshot.png)

Then the following variables that are given to you when you create an application on **strava.com**.

* `STRAVA_SECRET`
* `STRAVA_KEY`
* `SECRET_KEY`

## 1. Environment Setup

- Python 3.8 or higher with Pip

```
pip install -r requirements.txt
```

## 2. Run Developement Server


```
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
