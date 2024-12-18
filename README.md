# Gerrymandering

Trevor Nichols, Aiden Bugayong

This project aims to determine if gerrymandering has occurred, or is possible with the current voting distribution of various US states.

We attempt to simulate this via pseudo random groupings of polling neighborhoods into larger groupings which we may approximate as counties. Then, we simulate what a vote would result in given these county lines in order to determine the winner of each election. After running this simulation several times, we used a normal distribution to approximate the distribution of county affiliation per state. With this normal distribution, we can compare the real-world distribution to our expected ranges with a z-test in order to determine how likely a state has been affected by gerrymandering.

## Setup

### Required Software

- Docker
- docker-compose
- nix (optional)
- python 3, jupyter

### Dependencies

If using nix, simply activate the development shell provided with the `nix develop` command, this will download pinned versions of all required software, including python dependencies.

Python dependencies may be found within the dependencies section in the `flake.nix` file if manual installation is required.

Without nix, GDAL, QGIS, and DBeaver will be helpful for looking at data as simulations are performed or just to interact with data more directly.

With nix, GDAL and QGIS are provided automatically with the development shell, and DBeaver is provided with the command `nix run .#db`

### Running the backend

#### .env file

A sample `.env` file is provided below:

```.env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_ENDPOINT=localhost
POSTGRES_DB=Jerry
DB_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_ENDPOINT}:5432/${POSTGRES_DB}
```

Be sure to configure the username and password for your database

#### docker-compose

In a terminal environment in this directory, run `docker-compose up`

This command should download the necessary containers to run the database backend, and initialize it with functions, plugins, and datastructures necessary for our analysis.

### Running the application

After ensuring the backend has been initialized, the jupyter notebook titled `import_data.ipynb` will assist you in importing the input GeoJSON file into the database.

Ensure that your `.env` file is accessible as the script requires it to execute.

Certain cells marked "only run once" exist for the purpose of importing the input GeoJSON file, and setting up primary tables with the input data. The simulation cell marked "may take a long time" will take a long time to complete, on the order of hours, and is the only other cell that will write to the database.

All other cells should be run in the order that they appear in the notebook, without risk of writing or tampering with the database.

The final two cells allow you to generate a visualization of the clustering process by exporting html files to an ignored `viz` directory. If interested in creating these visualizations, ensure that the proper directories exist.

These visualizations would be nice to share, but many of them are on the orders of 100mb, making it hard to host on GitHub.

Full database backups may be shared at request, as the backup is ~60GB compressed.

## Structure

Most necessary files are in the root of the repository.

The `db` directory contains files that will be shared with the database backend. This includes the initialization script

The database storage volume by default is stored in your default volume storage directory configured in docker. If you would like to change the default to a different location, edit the `compose.yml` file. The database is compatible with bind mounts for the volume.

Both `.nix` files are necessary for dependency pinning for long term reproducibility of this project.

`notes.sql` contains initialization instructions for the database if not using the provided jupyter notebook
