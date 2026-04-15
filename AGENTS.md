# Codex Context

## Do

- Name classes, functions, properties in english
- Keep the existing layering: controller -> service -> repository.
- Prefer explicit FastAPI dependencies with `Annotated[..., Depends(...)]` at the usage site.
- Keep controllers thin: validate/serialize and delegate business rules to services.
- Add or update tests when behavior changes.
- Use `uv run pytest` for tests and `uv run ruff check .` for lint.
- Organize imports using Python good practices: standard library first, third-party packages second, local application imports last, with a blank line between groups.
- Keep imports sorted within each group and split long import lists across multiple lines when needed.

## Don't

- Do not move business rules into controllers.
- Do not access SQLAlchemy models directly from controllers when a service exists.
- Do not introduce dependency type aliases like `UserServiceDependency` or `SessionDependency`.
- Do not make broad structural changes unless the task requires them.
