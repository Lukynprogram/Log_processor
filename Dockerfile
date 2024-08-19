# Use a minimal base image for security
FROM python:3.11-alpine

# Define the SSH port as an argument (default to 2222 if not specified)
ARG SSH_PORT=2222

# Install SSH and other essential tools
RUN apk add --no-cache openssh shadow \
    && echo "root:disabled" | chpasswd

# Configure SSHD
RUN ssh-keygen -A \
    && sed -i "s/#Port 22/Port $SSH_PORT/g" /etc/ssh/sshd_config \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/g' /etc/ssh/sshd_config \
    && sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config \
    && sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication no/g' /etc/ssh/sshd_config \
    && sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords no/g' /etc/ssh/sshd_config \
    && sed -i 's/#ChallengeResponseAuthentication no/ChallengeResponseAuthentication no/g' /etc/ssh/sshd_config \
    && sed -i 's/#UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config \
    && sed -i 's/#StrictModes yes/StrictModes no/g' /etc/ssh/sshd_config \
    && sed -i 's/#MaxAuthTries 6/MaxAuthTries 3/g' /etc/ssh/sshd_config \
    && echo "KexAlgorithms curve25519-sha256@libssh.org" >> /etc/ssh/sshd_config \
    && echo "Ciphers aes256-gcm@openssh.com" >> /etc/ssh/sshd_config \
    && echo "MACs hmac-sha2-512-etm@openssh.com" >> /etc/ssh/sshd_config

# Set up a non-root user for SSH and set the password
RUN adduser -D scpuser \
    && echo "scpuser:EPAM" | chpasswd

# Copy your Python package (assuming you've built the wheel)
COPY dist/log_analyzer-1.0.0-py3-none-any.whl /app/
RUN pip install /app/log_analyzer-1.0.0-py3-none-any.whl

# Expose the SSH port defined by the SSH_PORT argument
EXPOSE $SSH_PORT

# Start the SSH daemon and keep the container running
CMD ["/usr/sbin/sshd", "-D"]
