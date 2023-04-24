FROM alpine:3.15

ADD install.sh install.sh
RUN sh install.sh && rm install.sh

ENV POSTGRES_DATABASE **None**
ENV POSTGRES_HOST **None**
ENV POSTGRES_PORT 5432
ENV POSTGRES_USER **None**
ENV POSTGRES_PASSWORD **None**
ENV POSTGRES_EXTRA_OPTS ''
ENV SCHEDULE **None**
ENV DROP_PUBLIC 'yes'
ENV DATA_FOLDERS_TO_BACKUP **None**
ENV DAYS_HISTORY 30

ADD run.sh run.sh
ADD backup.sh backup.sh
ADD restore.sh restore.sh


CMD ["sh", "run.sh"]
