{
  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = {...}@inputs:
  inputs.flake-utils.lib.eachDefaultSystem (system: let
    pkgs = (import inputs.nixpkgs) {
      inherit system;
      config = {
        allowUnfree = true;
      };
    };
    in
    {
      devShells = rec {
        docker-python = pkgs.mkShell {
          packages = with pkgs; [
            docker-compose
            docker
            podman-compose
            podman
            jupyter
            gdal
            qgis
            postgresql16Packages.postgis
            (python3.withPackages (pythonPackages: with pythonPackages; [
              ipykernel
              pandas
              geopandas
              scikit-learn
              pip
              numpy
              scipy
              matplotlib
              notebook
              requests
              python-dotenv
              psycopg2
              psycopg
              folium
              mapclassify
            ]))
          ];
        };
        default = docker-python;
      };
      apps = rec {
          db = {
            type = "app";
            program = "${pkgs.writeShellScriptBin "start-compose.sh" ''GDK_BACKEND=x11 ${pkgs.dbeaver-bin}/bin/dbeaver''}/bin/start-compose.sh";
          };
          default = db;
        # pgadmin = {
        #   type = "app";
        #   program = "${pkgs.pgadmin4-desktopmode}/bin/pgadmin4";
        # };
        # default = pgadmin;
      };
    }
  );
}