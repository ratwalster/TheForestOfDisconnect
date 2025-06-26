{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    # ... other packages
    (python312.withPackages (ps: [
      ps.pyngrok
      # ... other Python 3.12 packages
    ]))
  ];
}

