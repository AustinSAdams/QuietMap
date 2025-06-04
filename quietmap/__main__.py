# Main
import argparse
from colorama import init, Fore
from quietmap import discover, scan, netresolve
from quietmap.dependencies import check_and_install_dependencies
from quietmap.utils import file

# API KEY FUNCTIONS
def add_key(args):
    file.add_or_update_api_key(args.service_name, args.key_value)
def list_keys(args):
    file.list_keys_logic(args.service_name)
def remove_key(args):
    if args.all and args.service_name:
        print(f"{Fore.RED}[ERROR] Cannot specify a service name and the --all flag simultaneously.")
        return
    elif args.all:
        confirm = input(f"{Fore.YELLOW}Are you sure you want to remove ALL API keys? (yes/no): ").lower()
        if confirm == 'yes':
            file.clear_all_api_keys()
        else:
            print(f"{Fore.CYAN}Operation cancelled.")
    elif args.service_name:
        file.delete_api_key(args.service_name)
    else:
        print(f"{Fore.RED}[ERROR] Please specify a service name to remove, or use the --all flag to remove all keys.")

# RECON FUNCTIONS
def run_reconnaissance(args):
    # If no flags are set, run all
    run_all = not (args.network or args.ports or args.dns)

    if args.network or run_all:
        discover.run(args.domain)

    if args.ports or run_all:
        scan_results = scan.run(args.domain)
        print(scan_results)

    if args.dns or run_all:
        netresolve.run(args.domain)

def main():
    # Ensure dependencies are installed
    check_and_install_dependencies()

    # Set color coding to reset after each print
    init(autoreset=True)

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=(
            "Quietmap – OSINT multitool for domain-based reconnaissance. "
            "By default, if no flags are specified, QuietMap will run all reconnaissance modules. "
            "Specify individual flags to only run certain modules. "
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands:")


    ## ----RECON FUNCTIONS---- ##
    parser_recon = subparsers.add_parser(
        "recon",
        help="Run domain-based reconnaissance modules.",
        description="By default, if no flags are specified, runs Network, Ports, and DNS modules."
    )
    parser_recon.add_argument(
        "domain",
        type=str,
        help="Target domain (e.g., example.com)"
    )
    parser_recon.add_argument(
        "-n", "--network",
        action="store_true",
        help="Run network discovery"
    )
    parser_recon.add_argument(
        "-p", "--ports",
        action="store_true",
        help="Run port scan"
    )
    parser_recon.add_argument(
        "-d", "--dns",
        action="store_true",
        help="Run DNS resolution"
    )
    parser_recon.set_defaults(func=run_reconnaissance)


    ## --add_key subcommand-- ##
    parser_add_key = subparsers.add_parser(
        "add_key",
        help="Add or update an API key for a specific service.",
        description="This command allows you to store or update an API key locally for a given service."
    )
    parser_add_key.add_argument(
        "service_name",
        type=str,
        help="The name of the API service (e.g., 'shodan', 'gemini')."
    )
    parser_add_key.add_argument(
        "key_value",
        type=str,
        help="The API key string."
    )
    parser_add_key.set_defaults(func=add_key)


    ## --list_keys subcommand-- ##
    parser_list_keys = subparsers.add_parser(
        "list_keys",
        help="Print an API key for a specific service.",
        description="This command allows you to view an API key for a given service."
    )
    parser_list_keys.add_argument(
        "service_name",
        type=str,
        nargs= '?',
        help="The specific API service name to display (optional). If not specified, all keys are listed."
    )
    parser_list_keys.set_defaults(func=list_keys)


    ## --remove_key subcommand-- ##
    parser_remove_key = subparsers.add_parser(
        "remove_key",
        help="Remove an API key for a specific service.",
        description="This command allows you to view an API key for a given service."
    )
    parser_remove_key.add_argument(
        "service_name",
        type=str,
        nargs= '?',
        help="The specific name of the API service to remove."
    )
    parser_remove_key.add_argument(
        "-a", "--all",
        action="store_true",
        help="Flag to remove ALL stored API keys."
    )
    parser_remove_key.set_defaults(func=remove_key)


    # Detailed explanation and examples for help menu
    parser.epilog = (
        "Examples:"
        "\n  Recon:"
        "\n    quietmap recon -h                  # Opens help menu"
        "\n    quietmap recon example.com         # Runs Network, Ports, and DNS"
        "\n    quietmap recon -n example.com      # Runs only Network Discovery"
        "\n    quietmap recon -p -n example.com   # Runs Port Scan and Network Discovery"
        "\n  API Management:"
        "\n    quietmap <command> -h              # Opens help menu"
        "\n    quietmap add_key shodan 123        # Adds or updates the Shodan API key"
        "\n    quietmap list_keys                 # Lists all present keys"
        "\n    quietmap list_keys shodan          # Displays shodan's API key"
        "\n    quietmap remove_key shodan         # Removes shodan's API key"
        "\n    quietmap remove_key -a             # Removes ALL API keys"
    )

    # Parse the flags from the CLI
    args = parser.parse_args()

    args.func(args)

if __name__ == "__main__":
    main()
