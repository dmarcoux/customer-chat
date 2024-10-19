{
  description = "Python development environment";

  inputs = {
    # Use https://www.nixhub.io/ to easily find the exact commit to use in order to pin an input (and its packages) to a specific version
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { nixpkgs, ... } @ inputs:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { system = "${system}"; config.allowUnfree = true; };

    # Locales
    glibcLocales = pkgs.glibcLocales;

    # Bundle of SSL certificates
    cacert = pkgs.cacert;
  in
  {
    # Create development shell
    devShells.${system}.default = pkgs.mkShell {
      name = "devShell-Python";

      # Packages installed in the development shell
       packages = with pkgs; [
        python312
        # Package installer for Python
        python312Packages.pip
        # Timezones
        tzdata
        # Locales
        glibcLocales
        # Bundle of SSL certificates
        cacert
      ];

      # Commands to be executed in the development shell
      shellHook = ''
        # Set LANG for locales
        export LANG="C.UTF-8"

        # Remove duplicate commands from Bash shell command history
        export HISTCONTROL=ignoreboth:erasedups

        # Without this, there are warnings about LANG, LC_ALL and locales.
        # Many tests fail due those warnings showing up in test outputs too...
        # This solution is from: https://gist.github.com/aabs/fba5cd1a8038fb84a46909250d34a5c1
        export LOCALE_ARCHIVE="${glibcLocales}/lib/locale/locale-archive"

        # For the bundle of SSL certificates to be used in applications (like curl and others...)
        export SSL_CERT_FILE=${cacert}/etc/ssl/certs/ca-bundle.crt
      '';
    };
  };
}
