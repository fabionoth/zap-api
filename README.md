# Zap-api

How to Install
```bash
$ export ZAP_APIKEY=SupriseMotherFucker;
$ docker-compose up -d
```

How to use
```bash
$ curl http://localhost:5000/
$ curl http://localhost:5000/api?host=https://example-host.com
$ curl http://localhost:5000/reports
$ curl http://localhost:5000/reports?report=report_example-host.com.timestamp.html
```
