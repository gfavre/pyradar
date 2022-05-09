""" Main application entry point.

    python -m pyradar  ...

"""
import signal
from api.radar import run

def exit_gracefully(signum, frame):
    # restore the original signal handler as otherwise evil things will happen
    # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
    signal.signal(signal.SIGINT, signal.getsignal(signal.SIGINT))
    try:
        if input("\nReally quit? (y/n)> ").lower().startswith("y"):
            sys.exit(1)
    except KeyboardInterrupt:
        print("Ok, quitting")
        sys.exit(1)
    # restore the exit gracefully handler here
    signal.signal(signal.SIGINT, exit_gracefully)



def main():
    """ Execute the application.

    """
    signal.signal(signal.SIGINT, exit_gracefully)
    print(" [*] Waiting for events. To exit press CTRL+C")
    run()


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
