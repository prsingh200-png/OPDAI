# Security

- Never commit `.env`.
- Never commit uploaded patient documents.
- Use HTTPS in production.
- Rotate the JWT secret.
- Replace demo doctor credentials before deployment.
- Add proper RBAC and audit logging before handling real patient data.
- Treat AI output as assistive only; physician review is mandatory.
