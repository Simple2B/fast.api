# docker-backup-s3

Backup Postgres db and data files to mounted volume /backup

## Usage

Docker Compose:

```yaml
database:
  image: postgres:12
  environment:
    POSTGRES_DB: dbname
    POSTGRES_USER: user
    POSTGRES_PASSWORD: password

backup:
  build: pg-backup/
  image: slitidd/chairlift-pg-backup
  links:
    - database
  environment:
    SCHEDULE: "@daily"
    POSTGRES_DATABASE: dbname
    POSTGRES_USER: user
    POSTGRES_PASSWORD: password
    POSTGRES_EXTRA_OPTS: "--schema=public --blobs"
    DAYS_HISTORY: 30
```

### Automatic Periodic Backups

You can additionally set the `SCHEDULE` environment variable like `-e SCHEDULE="@daily"` to run the backup automatically.

`DAYS_HISTORY` - variable defines period in days, after that backup files will be removed

### Predefined schedules

| Entry                  | Description                                | Equivalent To   |
| ---------------------- | ------------------------------------------ | --------------- |
| @yearly (or @annually) | Run once a year, midnight, Jan. 1st        | 0 0 0 1 1 \*    |
| @monthly               | Run once a month, midnight, first of month | 0 0 0 1 \* \*   |
| @weekly                | Run once a week, midnight between Sat/Sun  | 0 0 0 \* \* 0   |
| @daily (or @midnight)  | Run once a day, midnight                   | 0 0 0 \* \* \*  |
| @hourly                | Run once an hour, beginning of hour        | 0 0 \* \* \* \* |

More details - (Go-lang cron)[https://pkg.go.dev/github.com/robfig/cron#hdr-Predefined_schedules]

### Manually create backup

For manually run database backup you need goto project folder and execute the following line.

```bash
docker-compose exec backup sh backup.sh
```

### Manually restore latest stored backup

For restore the latest backup you need goto project folder and execute the following line.

```bash
docker-compose exec backup sh restore.sh
```

**Warning!**
This will potentially put your database in a very bad state or complete destroy your data, be very careful.
