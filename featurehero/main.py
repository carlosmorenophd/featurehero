"""
Main entry point for the FeatureHero command-line application.
"""

import importlib.metadata
import argparse
import threading
from queue import Queue

from featurehero.worker.pip_worker import genetic_algorithm
from featurehero.core.files.work_space_file import prepare_work_space_file
from featurehero.core.files.transform_file import transform_data


def print_progress_from_queue(progress_queue: Queue):
    """
    Monitors a queue and prints progress updates to the console.
    """
    while True:
        message = progress_queue.get()
        if message == "DONE":
            print("\nProcess completed.")
            break
        if isinstance(message, str) and message.startswith("[ERROR]"):
            print(f"\n{message}")
            break
        if isinstance(message, int):
            print(f"\rProgress: {message}%", end="", flush=True)


def run_worker(file_path: str, target_column: str):
    """Run the worker in terminal mode."""
    new_folder_path, new_file_name = prepare_work_space_file(
        file_path=file_path,
        target_column=target_column,
    )
    print(f"Processed file saved at: {new_folder_path}")
    progress_queue = Queue()
    progress_thread = threading.Thread(
        target=print_progress_from_queue, args=(progress_queue,), daemon=True
    )
    progress_thread.start()
    genetic_algorithm(progress_queue=progress_queue,
                      selected_column=target_column,
                      file_path=new_file_name,
                      folder_file=new_folder_path)


def run_transform(file_path: str, transform_type: str, columns: list[str],
                  out_filename: str):
    """Run the data transformation worker."""
    try:
        transform_data(file_path, transform_type, columns, out_filename)
    except (FileNotFoundError, ValueError, KeyError, TypeError, OSError) as e:
        print(f"[ERROR] {e}")


def print_version():
    """Prints the current version of the application."""
    version = importlib.metadata.version("featurehero")
    print(f"FeatureHero Version: {version}")


def main():
    """Parses arguments and runs the application."""
    description = "FeatureHero - Genetic Orchestra for Predict and Selection"
    parser = argparse.ArgumentParser(
        description=description,
        epilog=("Use 'featurehero <action> --help' for more information on a "
                "specific action.")
    )
    subparsers = parser.add_subparsers(
        dest="action", help="Available actions", required=True)

    # Create the parser for the "run" command
    parser_run = subparsers.add_parser(
        "run", help="Run the genetic algorithm optimization")
    parser_run.add_argument(
        "--file",
        dest="file_path",
        required=True,
        help="Path to the input data file (.csv, .xlsx, .numbers).",
    )
    parser_run.add_argument(
        "--column",
        dest="target_column",
        required=True,
        help="Name of the target column for prediction."
    )

    # Create the parser for the "version" command
    subparsers.add_parser("version", help="Show the application version")

    # Create the parser for the "transform" command
    parser_transform = subparsers.add_parser(
        "transform", help="Transform data in a file")
    parser_transform.add_argument(
        "--file",
        dest="file_path",
        required=True,
        help="Path to the input data file.",
    )
    parser_transform.add_argument(
        "--type",
        dest="transform_type",
        required=True,
        choices=['date', 'category'],
        help="Type of transformation to apply.",
    )
    parser_transform.add_argument(
        "--columns",
        dest="columns",
        required=True,
        nargs='+',
        help="One or more column names to transform.",
    )
    parser_transform.add_argument(
        "--out",
        dest="out_filename",
        help="New name for the output file. (Optional)",
    )

    args = parser.parse_args()

    if args.action == "run":
        run_worker(args.file_path, args.target_column)
    elif args.action == "version":
        print_version()
    elif args.action == "transform":
        run_transform(
            args.file_path, args.transform_type, args.columns, args.out_filename
        )
    elif args.action == "help":
        parser.print_help()


if __name__ == "__main__":
    main()
