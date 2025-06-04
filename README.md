# QuietMap

QuietMap is a covert Python-based OSINT tool designed for automated network mapping, packet collection, and server information retrieval. It silently gathers critical data on a target system with minimal risk of detection. The tool supports **Nmap**-based scanning, with planned integrations for **Wireshark** (packet analysis) and the **Shodan API** (host intel).

---

## Features

- **Network Mapping (Nmap)**: Performs quiet port and service scans on target domains or IPs.
- **Flag-Driven Functionality**: Each function (e.g., discovery, scanning) can be toggled via CLI flags.
- **Stealth Operation**: Designed to operate with timing and behavior patterns that minimize detection.
- **Modular Output**: Stores results in categorized files for later analysis.
- **Planned Integrations**:
  - **Wireshark**: Passive packet capture
  - **Shodan API**: Server and exposure information lookup

---

## Requirements

- **Python 3.8+**
- **Nmap** (must be installed and accessible in your system PATH)
- [Optional, planned] Wireshark and Shodan API key

---

## Installation

### For Users (Standard Install)

Use this if you're only running the tool:

```bash
git clone https://github.com/AustinSAdams/QuietMap.git
cd QuietMap
pip install .
```

### For Developers (Editable Install)

Use this if you're modifying or extending the tool:

```bash
git clone https://github.com/AustinSAdams/QuietMap.git
cd QuietMap
pip install -e .
```

---

## Usage

QuietMap uses a command-line interface with distinct subcommands for different operations like reconnaissance and API key management.

```bash
quietmap <command> [options]
```

## Reconnaissance
The `recon` command is used to perform various domain-based reconnaissance modules. By default, if no flags are specified, it runs Network, Ports, and DNS modules.
```bash
quietmap recon <domain> [-n] [-p] [-d]
```
### Arguments
- `<domain>`: The target domain (e.g., `example.com`, `127.0.0.1`). This argument is required.
### Options
- `-n`, `--network`: Run only network discovery.
- `-p`, `--ports`: Run only port scanning.
- `-d`, `--dns`: Run only DNS resolution.

### Examples
Run all reconnaissance modules on a domain:
```bash
quietmap recon example.com
```

Run only port scanning on a domain:
```bash
quietmap recon -p example.com
```

Run port scanning and network discovery on a domain:
```bash
quietmap recon -p -n example.com
```

## API Key Management
QuietMap provides commands to manage API keys for various services, storing them locally.

### - `add_key`
Add or update an API key for a specific service.
```bash
quietmap add_key <service_name> <key_value>
```
**Arguments**
- `<service_name>`: The name of the API service (e.g., `'shodan'`, `'gemini'`).
- `<key_value>`: The actual API key string.
**Example**
Add or update a Shodan API key:
```bash
quietmap add_key shodan abc123
```

### - `list_keys`
List all stored API keys or display a specific one.
```bash
quietmap list_keys [service_name]
```
**Arguments**
- `<service_name>`: (optional): The specific API service name to display. If not provided, all stored keys will be listed.
**Examples**
List all stored API keys:
```bash
quietmap list_keys
```
Display the Shodan API key:
```bash
quietmap list_keys shodan
```

### - `remove_key`
Remove a specific API key or all stored API keys.
```bash
quietmap remove_key [service_name] [-a | --all]
```
**Arguments**
- `[service_name]` (optional): The specific name of the API service to remove.
**Options**
- `-a`, `--all`: A flag to remove ALL stored API keys. Use with caution; this action requires confirmation.
**Examples**
Remove the Shodan API key:
```bash
quietmap remove_key shodan
```
Remove all stored API keys (requires confirmation):
```bash
quietmap remove_key -a
```

---

## Output
Results are currently printed to the terminal. But, in the future, results will be stored in `output/` with subdirectories or files categorized by module (e.g., `scan-results/`, `dns-info.txt`).

---

## Future Features

- Wireshark integration for passive packet analysis
- Shodan API module for host information and service exposure
- Structured JSON reporting
- Timed/interval scanning automation

---

## Contributing

Issues, suggestions, and pull requests are welcome. Focus areas include stealth strategies, feature enhancements, and integrations.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
