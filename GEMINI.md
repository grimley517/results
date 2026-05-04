# Project Context: Results Reorganized

This repository manages sailing race results, handicaps (PY), and entry codes (QE). It has been reorganized for better maintainability.

## Directory Structure

- `src/`: Contains all Python source code. Priority was given to 2026 versions, followed by 2025.
- `Archive/`: Historical race data and published results.
  - Structure: `Archive/{Year}/{Series}/{File}.race`
  - Also contains historical HTML results and audit logs.
- `PY/`: Portishead Yardstick (PY) handicap data files (.txt and .csv).
- `QE archive/`: Quarterly Entry (QE) code files (.txt).
- `docs/`: Documentation, entry forms, and reference materials.
- `upload/`: Landing zone for new `.race` files before they are archived and processed.

## Configuration

- `config.json`: Standard configuration used by the GUI and core scripts. Format: `["PY_PATH", "QE_PATH", "BROWSER"]`.
- `configMod.json`: Extended configuration for specific processing scripts.

## Key Workflows

1. **Race Entry:** New `.race` files are typically uploaded to `upload/`.
2. **Archiving:** Races should be moved to `Archive/{Year}/{Series}/` based on their filename.
3. **Source Updates:** All code changes must be made within the `src/` directory.

## Development Notes

- The system uses a mix of JSON and text-based data files for handicaps and entry validation.
- Always check `config.json` paths when moving data files.
