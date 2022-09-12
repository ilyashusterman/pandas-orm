FROM python:3.9.13-slim-buster

RUN apt update

WORKDIR /src

ADD /requirements.txt /django_backend
ADD /Makefile /django_backend
RUN make pip_install_wheel || true && make pip_install
RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get auto-remove -y \
    && rm -rf /var/lib/apt/lists/*

COPY /django_backend /src/django_backend
COPY /django_backend /src/tools


ENV PYTHONPATH ${PYTHONPATH}:/src/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
