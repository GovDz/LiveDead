import concurrent.futures
import subprocess

def check_ssh(ip, port, user, password):
    try:
        subprocess.check_output(
            ['sshpass', '-p', password, 'ssh', '-o', 'StrictHostKeyChecking=no', '-p', port, f'{user}@{ip}', 'echo 2>&1'],
            timeout=5,
            stderr=subprocess.STDOUT,
        )
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

def check_ssh_entry(entry):
    ip, port, user, password = entry
    print(f'Checking {ip}|{port}|{user}')
    if check_ssh(ip, port, user, password):
        print(f'Success: {ip}|{port}|{user} is live')
        return f'{ip}|{port}|{user}|{password}'
    else:
        print(f'Failure: {ip}|{port}|{user} is dead')
        return None

def main(input_file):
    live_output_file = 'live_ssh.txt'
    dead_output_file = 'dead_ssh.txt'

    with open(input_file, 'r') as f:
        lines = f.readlines()

    ssh_entries = [line.strip().split('|') for line in lines if len(line.strip().split('|')) == 4]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(check_ssh_entry, ssh_entries))

    live_ssh_list = [result for result in results if result is not None]
    dead_ssh_list = [entry for entry, result in zip(ssh_entries, results) if result is None]

    with open(live_output_file, 'w') as live_file:
        live_file.write('\n'.join(live_ssh_list))

    with open(dead_output_file, 'w') as dead_file:
        dead_file.write('\n'.join('|'.join(entry) for entry in dead_ssh_list))

    print(f'SSH check complete. Results saved to {live_output_file} and {dead_output_file}')

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <ssh_list_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
