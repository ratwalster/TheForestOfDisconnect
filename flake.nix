# flake.nix
{
  description = "A development shell for forestofdisconnect";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: {
    devShells.x86_64-linux.default = let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in pkgs.mkShell {
      buildInputs = with pkgs; [
        python311
        # Add ngrok here
        ngrok
        # If you still need pyngrok for your Python application, keep it:
        python311Packages.pyngrok
        python311Packages.pyyaml
        # Add other Python packages from requirements.txt if needed
        # pkgs.python311Packages.pip
      ];

      # Set up your Python virtual environment if you still want to use it
      # postShellHook = ''
      #   if [ ! -d .venv ]; then
      #     echo "Creating virtual environment..."
      #     python3 -m venv .venv
      #   fi
      #   source .venv/bin/activate
      # '';

      # Or, if you want to rely purely on Nix for dependencies, you might not need the venv
      # For example, to install requirements:
      # shellHook = ''
      #   pip install -r requirements.txt
      # '';

    };
  };
}
