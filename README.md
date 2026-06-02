# Calculator-mokka

A sleek, modern, neon dark-mode calculator application built with Python and PySide6. It features keyboard support, a minimalist graphical interface, and a seamless Linux desktop integration.

## Features
- **Neon Dark-Mode UI**: Vibrant purple and orange highlights on a dark background.
- **Linux Desktop Integration**: Automatically show up in your application menu with a custom icon.

## Installation

### Quick Install (via curl)
If you want a quick installation directly from the repository, execute the following command in your terminal:

```bash
curl -sSL https://raw.githubusercontent.com/MonuGurjar/Calculator-Mokka/main/install.sh | bash
```

### Manual Install
If you have downloaded the folder locally, simply navigate to the directory and run the installation script:

```bash
cd Calculator-Mokka
chmod +x install.sh
./install.sh
```

This will automatically create a Python virtual environment, install the necessary dependencies (`PySide6`), and add **Calculator-mokka** to your system's Start Menu.

## Uninstallation
To remove the application from your Start Menu, simply delete the desktop entry:
```bash
rm ~/.local/share/applications/garuda-mokka-calc.desktop
```
