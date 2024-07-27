#!/bin/bash

# Usage:
# ./formatting.sh              # Run on all Python files in backend_dtx
# ./formatting.sh path/to/file # Run on specific file or directory in backend_dtx

# Set the base directory to backend_dtx
TARGET="../$1"

# Function to check if a Python module is installed, and install it if not
function ensure_module_installed {
  local module_name=$1
  local install_name=${2:-$1}  # If install name is different, it can be passed as a second argument
  if ! python -c "import $module_name" &> /dev/null; then
    echo "$module_name is not installed. Installing it now..."
    pip3 install "$install_name"
  else
    echo "$module_name is already installed."
  fi
}

# Ensure required modules are installed
ensure_module_installed black
ensure_module_installed docformatter
ensure_module_installed isort
ensure_module_installed flake8

# Run Black, docformatter, and isort on the target
black "$TARGET" --line-length 79
docformatter -i -r "$TARGET"
isort "$TARGET"
flake8 "$TARGET"
pylint $(find "$TARGET" -type f -name "*.py" | grep -v "__init__.py")


# Print completion message
echo ""
echo "Formatting completed for target: $TARGET"
