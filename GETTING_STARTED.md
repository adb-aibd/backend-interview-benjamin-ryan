# Money Changer Web API Usage Guide

## Overview

This document describes how this project can be run during development/testing.

## Setting up

1. Open this project folder with VS Code. Code will prompt to ask if it should
   reopen the project inside a dev container.
2. After the dev container is built, use alembic to update the database to
   ensure that the app works.

   ```bash
   $ alembic check # Check the current db migration version.
   INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
   INFO  [alembic.runtime.migration] Will assume transactional DDL.
   ERROR [alembic.util.messaging] Target database is not up to date.
   FAILED: Target database is not up to date.

   $ alembic upgrade head # Run the migrations
   INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
   INFO  [alembic.runtime.migration] Will assume transactional DDL.
   INFO  [alembic.runtime.migration] Running upgrade  -> 0743dfaa431d, initial schema
   ```

## Running the API server

1. In VS Code, press F5 to launch a debug session of the API server.
   Alternatively, press Ctrl+Shift+P and look for the "Debug: Start Debugging"
   command.

2. The launch configuration in `launch.json` should automatically open to the
   OpenAPI spec UI page. If not, open the "Ports" view on VS Code and open the
   link under "Forwarded Address" corresponding to port 8080, then append "/ui"
   to the URL in your browser's address bar.
