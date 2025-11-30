"""
Main entry point for the FeatureHero command-line application.
"""
import datetime
import sys
import importlib.metadata
import argparse
import subprocess
import os
import logging
import threading
from queue import Queue

from featurehero.worker.pip_worker import genetic_algorithm
from featurehero.core.job_manager import JobManager
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


def log_progress_from_queue(progress_queue: Queue, log_file: str):
    """Monitors a queue and logs progress updates to a file."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
    )
    while True:
        message = progress_queue.get()
        if message == "DONE":
            logging.info("Process completed.")
            break
        if isinstance(message, str) and message.startswith("[ERROR]"):
            logging.error(message)
            break
        if isinstance(message, int):
            logging.info("Progress: %d%%", message)


def run_worker(file_path: str, target_column: str):
    """Run the worker in terminal mode."""
    new_folder_path, new_file_name = prepare_work_space_file(
        file_path=file_path,
        target_column=target_column,
    )
    print(f"Processed file saved at: {new_folder_path}")
    progress_queue = Queue()

    progress_thread = threading.Thread(
        target=print_progress_from_queue,
        args=(progress_queue,),
        daemon=True
    )
    progress_thread.start()
    genetic_algorithm(
        progress_queue=progress_queue,
        selected_column=target_column,
        file_path=new_file_name,
        folder_file=new_folder_path,
    )


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


def create_parser() -> argparse.ArgumentParser:
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
    parser_run.add_argument(
        "--background",
        action="store_true",
        help="Run the process in the background and log to a file."
    )
    # Internal argument to run the process as a daemon
    parser_run.add_argument(
        "--run-as-daemon",
        action="store_true",
        help=argparse.SUPPRESS)
    # Internal argument to pass the log file path to the daemon
    parser_run.add_argument(
        "--log-file",
        dest="log_file",
        help=argparse.SUPPRESS)

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

    # Create the parser for the "jobs" command
    parser_jobs = subparsers.add_parser(
        "jobs", help="Manage background jobs")
    jobs_group = parser_jobs.add_mutually_exclusive_group(required=True)
    jobs_group.add_argument(
        "--list",
        action="store_true",
        help="List running background jobs"
    )
    jobs_group.add_argument(
        "--stop",
        dest="pid_to_stop",
        type=int,
        metavar="PID",
        help="Stop a running background job by its PID"
    )
    return parser


def handle_run_action(args: argparse.Namespace):
    """Handles the 'run' action."""
    if args.background and not args.run_as_daemon:
        # Create a unique, absolute path for the log file
        base_dir = os.path.dirname(os.path.abspath(args.file_path))
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"featurehero_{timestamp}.log"
        log_file = os.path.join(base_dir, log_filename)

        print(f"Running in background. Log will be saved to {log_file}")

        job_manager = JobManager()

        # Re-invoke the script with --run-as-daemon
        cmd = [
            sys.executable,
            "-m", "featurehero.main",
            "run",
            "--file", args.file_path,
            "--column", args.target_column,
            "--run-as-daemon",
            "--log-file", log_file
        ]

        try:
            # Detach the process from the current terminal
            popen_kwargs = {
                "stdout": subprocess.DEVNULL,
                "stderr": subprocess.DEVNULL,
            }
            if os.name == 'nt':  # Windows
                popen_kwargs['creationflags'] = subprocess.DETACHED_PROCESS
            else:  # POSIX
                popen_kwargs['start_new_session'] = True

            process = subprocess.Popen(cmd, **popen_kwargs)
            if process.pid:
                job_manager.register_job(
                    process.pid,
                    args.file_path,
                    args.target_column,
                    log_file
                )
        finally:
            # Exit the parent process, leaving the child to run
            sys.exit(0)
    elif args.run_as_daemon:
        # This is the daemon process, run the worker and log to file
        run_worker_background(args.file_path, args.target_column, args.log_file)
    else:
        # Run in foreground
        run_worker(args.file_path, args.target_column)


def handle_jobs_action(args: argparse.Namespace):
    """Handles the 'jobs' action."""
    job_manager = JobManager()
    if args.list:
        job_manager.list_jobs()
    elif args.pid_to_stop:
        job_manager.stop_job(args.pid_to_stop)


def main():
    """Parses arguments and dispatches the command."""
    parser = create_parser()
    args = parser.parse_args()

    if args.action == "run":
        handle_run_action(args)
    elif args.action == "version":
        print_version()
    elif args.action == "transform":
        run_transform(
            args.file_path,
            args.transform_type,
            args.columns,
            args.out_filename,
        )
    elif args.action == "help":
        parser.print_help()  # Should be unreachable, but good practice
    elif args.action == "jobs":
        handle_jobs_action(args)


def run_worker_background(file_path: str, target_column: str, log_file: str):
    """Run the worker in the background, logging to a file."""
    new_folder_path, new_file_name = prepare_work_space_file(
        file_path=file_path,
        target_column=target_column,
    )
    job_manager = JobManager()
    progress_queue = Queue()

    log_thread = threading.Thread(
        target=log_progress_from_queue,
        args=(progress_queue, log_file),
    )
    log_thread.daemon = True
    log_thread.start()

    pid = os.getpid()
    try:
        genetic_algorithm(
            progress_queue=progress_queue,
            selected_column=target_column,
            file_path=new_file_name,
            folder_file=new_folder_path,
        )
    finally:
        # Ensure the job is deregistered when it finishes or fails
        job_manager.deregister_job(pid)


if __name__ == "__main__":
    main()
