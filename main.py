import argparse
import multiprocessing
import sys

from src.consumer_producer_service import consumer_producer_service
from src.producer_service import producer_service


def main():
    """
    Main function to parse command-line arguments and create processes
    accordingly.
    """
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description='Start producer and consumer-producer services.')

    # Define command-line arguments
    parser.add_argument('--producer', type=int, default=None,
                        help='Number of producer processes to start')
    parser.add_argument('--conprod', type=int, default=None,
                        help='Number of consumer-producer processes to start')
    parser.add_argument('--same-domain-name', action='store_true',
                        help='Only process URLs from the same domain name')

    # Parse the arguments
    args = parser.parse_args()

    # Determine process counts based on arguments
    producer_count = args.producer
    conprod_count = args.conprod

    # Default behavior: one producer and one consumer-producer service if no arguments are provided
    if producer_count is None and conprod_count is None:
        producer_count = 1
        conprod_count = 1
    elif producer_count is None:
        producer_count = 0
    elif conprod_count is None:
        conprod_count = 0

    # Validate input
    if producer_count < 0 or conprod_count < 0:
        print('Error: The number of processes must be 0 or greater.')
        sys.exit(1)

    # Inform the user of the process configuration
    print(
        f'Starting {producer_count} producer(s) and {conprod_count} '
        f'consumer-producer(s) with same_domain_only={args.same_domain_name}'
    )

    # Create and start the processes
    create_processes(producer_count, conprod_count, args.same_domain_name)


def create_processes(producer_count, conprod_count, same_domain_only):
    """
    Create and start the specified number of producer and consumer-producer
    processes.

    Args:
        producer_count (int): Number of producer processes to create.
        conprod_count (int): Number of consumer-producer processes to create.
        same_domain_only (bool): Whether consumer-producer processes should limit
            processing to URLs from the same domain.
    """
    processes = []

    # Create producer processes
    for _ in range(producer_count):
        process = multiprocessing.Process(target=producer_service)
        process.start()
        processes.append(process)

    # Create consumer-producer processes, passing same_domain_only to each
    for _ in range(conprod_count):
        process = multiprocessing.Process(
            target=consumer_producer_service, args=(same_domain_only,))
        process.start()
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
