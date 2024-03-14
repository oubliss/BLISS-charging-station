import paramiko
import json

class SkyCharge(object):
    
    def __init__(self) -> None:
        self.ssh_key = None
        self.hostname = None
        self.username = None
        
        self.ssh_cfg = {
            'pkey': self.ssh_key, 
            'hostname': self.hostname, 
            'username': self.username}
        
        self.connection = None
        
    def __init__(self, ssh_key, hostname, username) -> None:
        self.ssh_key = ssh_key
        self.hostname = hostname
        self.username = username
        
        self.ssh_cfg = {
            'pkey': self.ssh_key, 
            'hostname': self.hostname, 
            'username': self.username}
        
        self.connection = None
        
                
    def charging_state(self, timeout=None):
        rc, response = self.ssh_exec("skycharge-cli show-charging-state --json",
                                timeout=timeout)
        if rc:
            return rc, None

        return 0, json.loads(response)
    
    
    def connect(self) -> paramiko.SSHClient:
        
        ssh = paramiko.SSHClient()
        ssh._policy = paramiko.WarningPolicy()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if 'pkey' in self.ssh_cfg and self.ssh_cfg['pkey']:
            self.ssh_cfg['pkey'] = paramiko.RSAKey.from_private_key_file(self.ssh_cfg['pkey'])

        ssh.connect(**self.ssh_cfg)
        self.ssh = ssh
        
        return 0
    
    
    def disconnect(self):
        self.ssh.close()
    
    
    def start_scanning(self):
        rc, response = self.ssh_exec('skycharge-cli resume-scan')
        
    
    def stop_scanning(self): 
        rc, response = self.ssh_exec('skycharge-cli stop-scan')
        
        print(rc, response)
    
    
    def ssh_exec(self, cmd, input_data=None, timeout=None):
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
        if input_data:
            stdin.write(input_data)
        rc = stdout.channel.recv_exit_status()
        response = ''.join(stdout)
        error = ''.join(stderr)
        return rc, response
    
    
    def set_ssh_cfg(self, key, host, user):
        self.ssh_key = key
        self.hostname = host
        self.username = user
        
        self.ssh_cfg = {
            'pkey': self.ssh_key, 
            'hostname': self.hostname, 
            'username': self.username}
        
        return 0
        
        
    
