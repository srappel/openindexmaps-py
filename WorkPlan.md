# Work Plan for CLI Implementation

## 1. Set up a Development Branch
- **Objective**: Create a separate branch for this new functionality.
- **Task**: 
  - Create a new branch, e.g., `feature/cli-enhancements`, to work on the new features.
  - Commit regularly to track progress.

  ```bash
  git checkout -b feature/cli-enhancements
  ```

## 2. Implement OpenIndexMap Creation with Defaults
- **Objective**: Implement the functionality to create an `OpenIndexMap` and set defaults.
- **Tasks**:
  - Implement the `oim` command in `oimpycli.py`.
  - Update the `OpenIndexMap` class to handle defaults properly.
  - Ensure defaults are stored and can be accessed later.
- **Testing**:
  - Write tests for creating an OpenIndexMap with defaults.
  - Manually test via CLI to ensure creation works correctly.
  
  ```bash
  oimpy oim --name "Map Collection X" --scale "1:25000" --edition-no "1975" --date 1975 --publisher "Defense Mapping Agency"
  ```

  - **Goal**: OpenIndexMap is created, defaults are stored.

## 3. Implement Active OpenIndexMap Handling
- **Objective**: Implement functionality to make an OpenIndexMap "active" after creation.
- **Tasks**:
  - Set up a global variable or file-based approach to store the active `OpenIndexMap`.
  - Ensure that the newly created `OpenIndexMap` is automatically active.
  - Add error handling for when no OpenIndexMap is active.
- **Testing**:
  - Write tests to verify that after creating an OpenIndexMap, it becomes active.
  - Manually test that the active OpenIndexMap is correctly set.

## 4. Implement Adding Sheets with Inherited Defaults
- **Objective**: Implement the `add-sheet` command that adds a new sheet to the active OpenIndexMap.
- **Tasks**:
  - Develop the `add-sheet` command in `oimpycli.py`.
  - Ensure the `add-sheet` command uses the defaults from the active OpenIndexMap.
  - Allow sheet-specific overrides for defaults.
- **Testing**:
  - Write tests to verify that the `add-sheet` command correctly uses defaults and overrides.
  - Manually test via CLI by creating sheets with and without overrides.

  ```bash
  oimpy add-sheet --title "Sheet A" --sheet-number 1 --edition 2 --date 1921
  ```

## 5. Implement Manual Activation of OpenIndexMaps
- **Objective**: Allow the user to manually activate an OpenIndexMap.
- **Tasks**:
  - Implement the `activate-oim` command in `oimpycli.py`.
  - Ensure proper error handling if the specified OpenIndexMap doesn’t exist.
- **Testing**:
  - Write tests for manually activating OpenIndexMaps.
  - Manually test switching between active OpenIndexMaps.

  ```bash
  oimpy activate-oim --name "Map Collection X"
  ```

## 6. Implement Viewing the Active OpenIndexMap
- **Objective**: Allow users to view the currently active OpenIndexMap and its default values.
- **Tasks**:
  - Implement the `view-active` command in `oimpycli.py`.
  - Ensure the output displays the active OpenIndexMap’s name and default values.
- **Testing**:
  - Write tests to ensure that the active map is displayed correctly.
  - Manually test by switching OpenIndexMaps and using `view-active`.

  ```bash
  oimpy view-active
  ```

## 7. Write Unit Tests for Each Command
- **Objective**: Ensure your code is reliable and functions as expected.
- **Tasks**:
  - Implement unit tests for all CLI commands.
  - Test different edge cases (e.g., no active OpenIndexMap, overriding defaults, missing required fields).
  - Write tests for both successful and failure scenarios.
- **Tools**:
  - Use `pytest` for testing, and `Click`'s built-in testing utilities for CLI commands.

## 8. Integrate and Refactor Code
- **Objective**: Once all commands are implemented, clean up the code and ensure consistency.
- **Tasks**:
  - Refactor the code for readability, maintainability, and performance.
  - Ensure proper error handling throughout the codebase.
  - Review the use of global variables (like `active_oim`) and ensure they are handled safely.

## 9. Final Testing and Bug Fixing
- **Objective**: Test the CLI tool as a whole to identify and fix any remaining issues.
- **Tasks**:
  - Perform manual testing of all CLI commands together.
  - Test various edge cases, such as creating multiple OpenIndexMaps, switching between them, and adding sheets.
- **Goal**: Ensure the tool is functional and user-friendly.

## 10. Documentation
- **Objective**: Create user documentation for the CLI tool.
- **Tasks**:
  - Document how to use each CLI command (`oim`, `add-sheet`, `activate-oim`, `view-active`).
  - Provide examples for common workflows, such as creating an OpenIndexMap, adding sheets, and switching active maps.
  - Include information on setting up the environment, dependencies, and installation instructions.

## 11. Merge to Main Branch
- **Objective**: Merge the changes back into the main branch.
- **Tasks**:
  - Open a pull request, review the changes, and merge the new functionality into the main branch.
  - Ensure the documentation is updated on the repository.
  
  ```bash
  git checkout main
  git merge feature/cli-enhancements
  ```
