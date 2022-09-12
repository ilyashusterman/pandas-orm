FROM postgres:11.5-alpine

# An additional setting that is recommended for all users regardless of this
# value is the runtime "--stop-timeout" (or your orchestrator/runtime's
# equivalent) for controlling how long to wait between sending the defined
# STOPSIGNAL and sending SIGKILL (which is likely to cause data corruption).
#
# The default in most runtimes (such as Docker) is 10 seconds, and the
# documentation at https://www.postgresql.org/docs/12/server-start.html notes
# that even 90 seconds may not be long enough in many instances.

RUN apk add bash
ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl

RUN apk add --no-cache \
    $MUSL_LOCALE_DEPS

RUN apk add --no-cache \
    $MUSL_LOCALE_DEPS \
    && wget https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip \
    && unzip musl-locales-master.zip \
      && cd musl-locales-master \
      && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
      && cd .. && rm -r musl-locales-master

COPY /docker_services/postgres/scripts/ /docker-entrypoint-initdb.d/
COPY /docker_services/postgres/postgresql.conf /etc/postgresql/postgresql.conf
COPY /docker_services/postgres/main/pg_hba.conf /etc/postgresql/main/pg_hba.conf
COPY /docker_services/postgres/mock_db/ /mock_db/
ENV POSTGRES_PASSWORD 'password'
CMD ["postgres","-c","config_file=/etc/postgresql/postgresql.conf" ]