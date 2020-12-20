{
  pkgs ? import (builtins.fetchGit {
    url = "https://github.com/NixOS/nixpkgs/";
    ref = "nixos-20.09";
  }) {}
}:

pkgs.mkShell {
  name = "AoC20";
  buildInputs = with pkgs; [
    gitAndTools.gitFull
    pypy3
    python39
    python39Packages.venvShellHook
  ];
  venvDir = "./.venv";
  postShellHook = ''
    unset SOURCE_DATE_EPOCH
    pip install -r requirements.txt
  '';
}
