import os
import paramiko

# Define your SFTP connection details
sftp_host = "location"
sftp_port = 22
sftp_username = "uname"
sftp_password = "pwd"
sftp_remote_dir = "/support"
local_temp_dir = "D:\\Result_files"  # A temporary local directory to process files


# Connect to the SFTP server
def connect_sftp():
    transport = paramiko.Transport((sftp_host, sftp_port))
    transport.connect(username=sftp_username, password=sftp_password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp


# Check for new XML files
def check_new_files(sftp):
    new_files = []
    files = sftp.listdir(sftp_remote_dir)
    for file in files:
        if file.endswith(".xml"):
            new_files.append(file)
    return new_files


# Split a file into chunks of max 300 lines
def split_file(file_content):
    lines = file_content.splitlines()
    chunks = [lines[i:i + 300] for i in range(0, len(lines), 300)]
    return ["\n".join(chunk) for chunk in chunks]


# Process each new file
def process_file(sftp, file):
    remote_file_path = f"{sftp_remote_dir}/{file}"
    local_file_path = f"{local_temp_dir}/{file}"

    # Download the file
    sftp.get(remote_file_path, local_file_path)

    # Read the file content
    with open(local_file_path, 'r') as f:
        file_content = f.read()

    # Split the file into chunks of 300 lines max
    chunks = split_file(file_content)

    if len(chunks) > 1:
        base_name = file.rsplit('.', 1)[0]  # Remove extension

        for i, chunk in enumerate(chunks):
            chunk_name = f"{base_name}_{i + 1}.xml"
            chunk_path = f"{local_temp_dir}/{chunk_name}"

            # Write the chunk to a new file
            with open(chunk_path, 'w') as chunk_file:
                chunk_file.write(chunk)

            # Upload the chunked file back to the SFTP server
            sftp.put(chunk_path, f"{sftp_remote_dir}/{chunk_name}")

            # Clean up local temp files
            os.remove(chunk_path)

        # Optionally, remove the original file from the server
        sftp.remove(remote_file_path)

    # Clean up the original local temp file
    os.remove(local_file_path)


# Main function
def main():
    sftp = connect_sftp()
    new_files = check_new_files(sftp)
    for file in new_files:
        process_file(sftp, file)
    sftp.close()


if __name__ == "__main__":
    main()
