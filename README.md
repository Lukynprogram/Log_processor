# Log Processor Tool

This project provides a command-line tool to analyze Squid log files efficiently. The tool is packaged in a Docker container, making it easy to run without requiring a local Python setup.
This tool analyzes Squid log files to extract useful metrics such as the most frequent IP, least frequent IP, events per second, and total bytes exchanged.

## Prerequisites
Before you begin, ensure you have the following installed:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)

## Getting Started

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone -b master git@github.com:Lukynprogram/Log_processor.git
cd Log_processor
```
### 2. Build the Docker Container
Build the Docker container using the following command:
```bash
docker build -t minimal-python-scp .
```

### 3. Running the Docker Container
To run the Docker container, use the following command:

```bash
sudo docker run -d -p 2222:2222 --name python-scp minimal-python-scp
```

### 4. Accessing the Container via SSH
The default user is `scpuser`, and the password is `EPAM`. You can upload files to the container using `scp` (Secure Copy Protocol). For example:

```bash
scp -P 2222 access.log scpuser@{IP address of the container}:/home/scpuser/
```

### 5. Running the Log Analyzer
Once your files are uploaded to the container, you can run the log analyzer using the following commands:
- **Using Docker Exec:**
  ```bash
  sudo docker exec -it python-scp log-analyzer /home/scpuser/access.log --mfip --lfip --eps --bytes
    ```
- **Using shell (after SSH):**
  ```bash
  log-analyzer /home/scpuser/access.log --mfip --lfip --eps --bytes
    ```

### 6. Command-Line Options
The log analyzer supports the following command-line options:

```bash
usage: log-analyzer [-h] [--output OUTPUT] [--format {txt,json}] [--mfip] 
                    [--lfip] [--eps] [--bytes] [--ignore-local-ip] input [input ...]
```

#### Required Arguments:
- `input`: Path to one or more input files to be analyzed.

#### Optional Arguments:
- `-h, --help`: Show the help message and exit.
- `--output OUTPUT`: Specify the path to a file to save the output.
- `--format {txt,json}`: Choose the format of the output (either `txt` or `json`).
- `--mfip`: Display the most frequent IP address.
- `--lfip`: Display the least frequent IP addresses.
- `--eps`: Calculate and display events per second.
- `--bytes`: Display the total amount of bytes exchanged.
- `--ignore-local-ip`: Ignore local IP addresses in the analysis.

### 7. Conclusion
If you encounter any issues or have suggestions for improvements, feel free to contribute to the repository or contact the author.

### 8. PoC
![image](https://github.com/user-attachments/assets/e76a5f0d-a2d2-49c3-ac3e-a949e3a11343)
