with import <nixpkgs> {}; {
  env = stdenv.mkDerivation {
    name = "firerule-env";
    buildInputs = [ 
      gnumake
      python3
      python3Packages.pyqt5 python3Packages.scipy python3Packages.numpy
    ];
  };
}
