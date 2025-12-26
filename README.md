## Deployment

This service is deployed on Render using Docker.

- Web service listens on `$PORT`
- PostgreSQL is provided via Render managed database
- Secrets are stored in Render Environment Variables
- ETL runs at startup

Endpoints:
- `/health`
- `/data`
- `/stats`
- `/metrics`
