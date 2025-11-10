# -*- coding: utf-8 -*-
"""feathero package."""
__version__ = "2025.11.01"

# Make high-level functions available at the top-level of the package
from automations import process_file_dates


def run_interactive():
    """Starts an interactive session to use feathero's transformations."""
    print("--- Welcome to the feathero interactive interface ---")

    # Main menu
    main_option = input(
        "Select the operation type (e.g., 'transform'): ").strip().lower()

    if main_option == "transform":
        # Transformations submenu
        transform_type = (
            input("Select the transformation type ('date' or 'category'): ")
            .strip()
            .lower()
        )

        if transform_type == "date":
            print("\n--- Date Transformation ---")
            file_path = input(
                "Please enter the full path to the file (csv, xlsx, numbers): "
            ).strip()

            prefix_input = input(
                "Enter the prefix for the new file (leave blank to use '_transform_date'): "
            ).strip()

            try:
                print("Processing file...")
                if prefix_input:
                    new_file = process_file_dates(
                        file_path, prefix=prefix_input)
                else:
                    # Use the function's default prefix
                    new_file = process_file_dates(file_path)

                if new_file:
                    print(f"Success! Transformed file saved at: {new_file}")
            except FileNotFoundError:
                print(f"Error: Could not find the file at path '{file_path}'")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif transform_type == "category":
            print("\nSorry, the 'category' transformation is under construction.")
        else:
            print(
                f"Error: '{transform_type}' is not a valid transformation type.")
    else:
        print(f"Error: '{main_option}' is not a valid operation.")
