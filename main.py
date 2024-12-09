import argparse
import multiprocessing
import sys

from src.consumer_producer_service import consumer_producer_service
from src.producer_service import producer_service


def create_processes(producer_count, conprod_count):
    # Create producer processes
    for _ in range(producer_count):
        producer_process = multiprocessing.Process(target=producer_service)
        producer_process.start()

    # Create consumer-producer processes
    for _ in range(conprod_count):
        conprod_process = multiprocessing.Process(
            target=consumer_producer_service)
        conprod_process.start()


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description='Start producer and consumer-producer services.')

    # Define command-line arguments
    parser.add_argument('--producer', type=int, default=1,
                        help='Number of producer processes to start')
    parser.add_argument('--conprod', type=int, default=1,
                        help='Number of consumer-producer processes to start')

    # Parse the arguments
    args = parser.parse_args()

    # Get the number of processes from arguments, default to 1 if not specified
    producer_count = args.producer
    conprod_count = args.conprod

    # Validate input
    if producer_count < 1 or conprod_count < 1:
        print('Error: The number of processes must be at least 1.')
        sys.exit(1)

    print(
        f'Starting {producer_count} producer(s) and {conprod_count} '
        f'consumer-producer(s)'
    )

    # Create and start the processes
    create_processes(producer_count, conprod_count)


if __name__ == '__main__':
    main()
