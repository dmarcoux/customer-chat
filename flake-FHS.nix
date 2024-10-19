{
  description = "Python development environment based on the Filesystem Hierarchy Standard (FHS)";
  # https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard

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
    # Create development shell based on the Filesystem Hierarchy Standard (FHS) with a set of
    # standard packages based on the list maintained by the appimagetools package
    #
    # buildFHSEnv -> https://nixos.org/manual/nixpkgs/stable/#sec-fhs-environments
    #
    # The packages included in appimagetools.defaultFhsEnvArgs are:
    # https://github.com/NixOS/nixpkgs/blob/fd6a510ec7e84ccd7f38c2ad9a55a18bf076f738/pkgs/build-support/appimage/default.nix#L72-L208
    devShells.${system}.default = (pkgs.buildFHSEnv (pkgs.appimageTools.defaultFhsEnvArgs // {
          name = "python-development-environment";
          # Packages installed in the development shell
          targetPkgs = pkgs: with pkgs; [
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
          profile = ''
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
        })).env;
  };
}
