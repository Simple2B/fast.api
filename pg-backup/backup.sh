#! /bin/sh

set -e
set -o pipefail

if [ "${POSTGRES_DATABASE}" = "**None**" ]; then
  echo "You need to set the POSTGRES_DATABASE environment variable."
  exit 1
fi

if [ "${POSTGRES_HOST}" = "**None**" ]; then
  if [ -n "${POSTGRES_PORT_5432_TCP_ADDR}" ]; then
    POSTGRES_HOST=$POSTGRES_PORT_5432_TCP_ADDR
    POSTGRES_PORT=$POSTGRES_PORT_5432_TCP_PORT
  else
    echo "You need to set the POSTGRES_HOST environment variable."
    exit 1
  fi
fi

if [ "${POSTGRES_USER}" = "**None**" ]; then
  echo "You need to set the POSTGRES_USER environment variable."
  exit 1
fi

if [ "${POSTGRES_PASSWORD}" = "**None**" ]; then
  echo "You need to set the POSTGRES_PASSWORD environment variable or link to a container named POSTGRES."
  exit 1
fi

export PGPASSWORD=$POSTGRES_PASSWORD
POSTGRES_HOST_OPTS="-h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER $POSTGRES_EXTRA_OPTS"

echo "Creating dump of ${POSTGRES_DATABASE} database from ${POSTGRES_HOST}..."
pg_dump $POSTGRES_HOST_OPTS $POSTGRES_DATABASE > dump.sql

echo "Compressing data..."
if [ "${DATA_FOLDERS_TO_BACKUP}" = "**None**" ]; then
  tar cvzf backup.tgz dump.sql
else
  tar cvzf backup.tgz dump.sql ${DATA_FOLDERS_TO_BACKUP}
fi

echo "Copy achive to /backup"
cp backup.tgz /backup/${POSTGRES_DATABASE}_$(date +"%Y-%m-%dT%H:%M:%SZ").tgz
echo "Remove oldest backups"
ls -tp /backup/*.tgz | grep -v '/$' | tail -n +${DAYS_HISTORY}
ls -tp /backup/*.tgz | grep -v '/$' | tail -n +${DAYS_HISTORY} | xargs -I {} rm -- {}

echo "DB backuped successfully"
