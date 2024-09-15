# Work Plans

* [CLI Implemenetation](#work-plan-for-cli-implementation)
* [SQLite Implementation](#work-plan-implementing-sqlite-as-primary-data-store-with-json-importexport-and-caching)

## Work Plan for CLI Implementation

### 1. Set up a Development Branch
- **Objective**: Create a separate branch for this new functionality.
- **Task**: 
  - Create a new branch, e.g., `feature/cli-enhancements`, to work on the new features.
  - Commit regularly to track progress.

  ```bash
  git checkout -b feature/cli-enhancements
  ```

### 2. Implement OpenIndexMap Creation with Defaults
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

### 3. Implement Active OpenIndexMap Handling
- **Objective**: Implement functionality to make an OpenIndexMap "active" after creation.
- **Tasks**:
  - Set up a global variable or file-based approach to store the active `OpenIndexMap`.
  - Ensure that the newly created `OpenIndexMap` is automatically active.
  - Add error handling for when no OpenIndexMap is active.
- **Testing**:
  - Write tests to verify that after creating an OpenIndexMap, it becomes active.
  - Manually test that the active OpenIndexMap is correctly set.

### 4. Implement Adding Sheets with Inherited Defaults
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

### 5. Implement Manual Activation of OpenIndexMaps
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

### 6. Implement Viewing the Active OpenIndexMap
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

### 7. Write Unit Tests for Each Command
- **Objective**: Ensure your code is reliable and functions as expected.
- **Tasks**:
  - Implement unit tests for all CLI commands.
  - Test different edge cases (e.g., no active OpenIndexMap, overriding defaults, missing required fields).
  - Write tests for both successful and failure scenarios.
- **Tools**:
  - Use `pytest` for testing, and `Click`'s built-in testing utilities for CLI commands.

### 8. Integrate and Refactor Code
- **Objective**: Once all commands are implemented, clean up the code and ensure consistency.
- **Tasks**:
  - Refactor the code for readability, maintainability, and performance.
  - Ensure proper error handling throughout the codebase.
  - Review the use of global variables (like `active_oim`) and ensure they are handled safely.

### 9. Final Testing and Bug Fixing
- **Objective**: Test the CLI tool as a whole to identify and fix any remaining issues.
- **Tasks**:
  - Perform manual testing of all CLI commands together.
  - Test various edge cases, such as creating multiple OpenIndexMaps, switching between them, and adding sheets.
- **Goal**: Ensure the tool is functional and user-friendly.

### 10. Documentation
- **Objective**: Create user documentation for the CLI tool.
- **Tasks**:
  - Document how to use each CLI command (`oim`, `add-sheet`, `activate-oim`, `view-active`).
  - Provide examples for common workflows, such as creating an OpenIndexMap, adding sheets, and switching active maps.
  - Include information on setting up the environment, dependencies, and installation instructions.

### 11. Merge to Main Branch
- **Objective**: Merge the changes back into the main branch.
- **Tasks**:
  - Open a pull request, review the changes, and merge the new functionality into the main branch.
  - Ensure the documentation is updated on the repository.
  
  ```bash
  git checkout main
  git merge feature/cli-enhancements
  ```


## Work Plan: Implementing SQLite as Primary Data Store with JSON Import/Export and Caching

### 1. **Conceptualize Backend Requirements**
   - **Objective**: Define what the backend needs to achieve, focusing on storing OpenIndexMaps and Sheets in SQLite, supporting JSON import/export, and caching data from remote repositories.
   - **Tasks**:
     - Identify key metadata fields for OpenIndexMaps and Sheets that will be stored in SQLite.
     - Decide how full JSON data will be handled (stored as blobs in SQLite or as flat JSON files).
     - Determine caching requirements for remote data (e.g., which fields/data need to be cached and how often they should sync with the remote repository).
   - **Output**: Clear understanding of what data needs to be stored, how it will be structured, and the interaction between SQLite and flat JSON files.

### 2. **Design SQLite Database Schema**
   - **Objective**: Create a schema to store OpenIndexMaps, Sheets, and any necessary relationships.
   - **Tasks**:
     - Define tables for `OpenIndexMaps` and `Sheets`, focusing on the core metadata fields.
     - Implement columns for JSON data (using `TEXT` or `BLOB` fields for storing complex data).
     - Add any foreign key relationships needed (e.g., linking Sheets to an OpenIndexMap).
   - **Output**: SQLite schema that is ready for implementation.

   **Example Schema**:
   ```sql
   CREATE TABLE openindexmaps (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT NOT NULL,
       scale TEXT,
       edition_no TEXT,
       date TEXT,
       publisher TEXT,
       json_data TEXT
   );

   CREATE TABLE sheets (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       openindexmap_id INTEGER,
       title TEXT NOT NULL,
       sheet_number INTEGER,
       json_data TEXT,
       FOREIGN KEY (openindexmap_id) REFERENCES openindexmaps(id)
   );
   ```

### 3. **Implement SQLite for Primary Data Storage**
   - **Objective**: Build functionality to use SQLite as the primary data store for OpenIndexMaps and Sheets.
   - **Tasks**:
     - Implement SQLite queries for creating, reading, updating, and deleting records.
     - Store core metadata in SQLite tables and full JSON structures as JSON blobs or in external JSON files.
     - Add methods to insert, update, and retrieve OpenIndexMaps and Sheets.
   - **Output**: SQLite functions integrated into the project as the main data store.

### 4. **JSON Import/Export Interfaces**
   - **Objective**: Build an interface for importing and exporting data to/from JSON, allowing easy interaction with the stored data.
   - **Tasks**:
     - Create functions to export SQLite data into flat JSON files (e.g., `openindexmap.json`, `sheet_1.json`).
     - Implement import functionality to take JSON files and populate SQLite tables.
   - **Output**: Simple export/import functionality, allowing users to work with JSON files and SQLite seamlessly.

   **Example:**
   ```python
   def export_openindexmap_to_json(map_id):
       data = get_openindexmap_data(map_id)  # Fetch from SQLite
       with open(f"openindexmap_{map_id}.json", 'w') as f:
           json.dump(data, f)

   def import_openindexmap_from_json(file_path):
       with open(file_path, 'r') as f:
           data = json.load(f)
       insert_openindexmap_data(data)  # Insert into SQLite
   ```

### 5. **Local Cache for Remote Data**
   - **Objective**: Implement caching using SQLite for remote data (e.g., data from GitHub repositories).
   - **Tasks**:
     - Identify which data from remote repositories needs to be cached (e.g., OpenIndexMaps or Sheets stored on GitHub).
     - Implement caching mechanism to store and periodically refresh this data locally in SQLite.
     - Create functions to sync data between the local cache and remote repositories.
   - **Output**: SQLite acts as a local cache for remote data, reducing the need to fetch remote data repeatedly.

   **Example**:
   ```python
   def cache_remote_data(map_id):
       data = fetch_data_from_github(map_id)
       store_in_sqlite_cache(map_id, data)

   def sync_cache_with_remote():
       # Periodically check for updates and refresh cache
       for map_id in get_cached_maps():
           if remote_version_updated(map_id):
               cache_remote_data(map_id)
   ```

### 6. **CLI Integration**
   - **Objective**: Integrate the SQLite backend and caching functionality into the CLI tool.
   - **Tasks**:
     - Modify the existing CLI to interact with the new SQLite backend.
     - Add commands for importing/exporting JSON data.
     - Add commands for caching and syncing remote data.
   - **Output**: A CLI that seamlessly interacts with SQLite, supports JSON import/export, and can cache remote data.

   **Example Commands**:
   ```bash
   oimpy create-map --name "Map Collection X" --scale "1:25000" --date "1975"
   oimpy export-map --map-id 1 --output-file "map_collection_x.json"
   oimpy import-map --input-file "map_collection_x.json"
   oimpy sync-cache
   ```

### 7. **Testing and Validation**
   - **Objective**: Ensure the system works correctly, with proper handling of SQLite data storage, JSON import/export, and caching.
   - **Tasks**:
     - Write unit tests for all major functions (SQLite queries, JSON handling, caching mechanisms).
     - Perform integration testing to ensure that the CLI interacts with the backend smoothly.
     - Test the caching functionality to ensure that remote data is synced correctly.
   - **Output**: Fully tested and validated SQLite-based backend with JSON import/export and caching.

### 8. **Documentation**
   - **Objective**: Document how the backend works, how to use the JSON interfaces, and how caching is implemented.
   - **Tasks**:
     - Write documentation for the SQLite schema, the JSON import/export process, and caching logic.
     - Include usage examples for the CLI commands.
   - **Output**: Clear documentation that explains how to use the SQLite backend and related functionality.
