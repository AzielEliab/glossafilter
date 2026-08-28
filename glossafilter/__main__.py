"""Allow ``python -m glossafilter`` to invoke the CLI."""

from glossafilter.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
