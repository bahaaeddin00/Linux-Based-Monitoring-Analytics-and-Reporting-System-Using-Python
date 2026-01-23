import os
import time
import stat
import pwd
import grp
import csv
from datetime import datetime
from pathlib import Path

class DirectoryMonitor:
    def __init__(self, directory_path, log_file="directory_log.csv"):
        self.directory_path = directory_path
        self.log_file = log_file
        self.previous_state = {}
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "Event", "Filename", "File_Type", 
                    "Size_Bytes", "Permissions", "Owner", "Group", "Details"
                ])

    def get_file_metadata(self, filepath):
        """
        Extracts metadata for a single file using os.stat and pathlib.
        """
        try:
            path_obj = Path(filepath)
            file_stat = path_obj.stat()

            # 1. File Type
            if path_obj.is_symlink():
                f_type = "Symbolic Link"
            elif path_obj.is_dir():
                f_type = "Directory"
            else:
                f_type = "Regular File"

         
            perms = oct(stat.S_IMODE(file_stat.st_mode))

        
            try:
                owner = pwd.getpwuid(file_stat.st_uid).pw_name
                group = grp.getgrgid(file_stat.st_gid).gr_name
            except KeyError:
                owner = str(file_stat.st_uid)
                group = str(file_stat.st_gid)

         
            
            return {
                "filepath": filepath,
                "filename": path_obj.name,
                "type": f_type,
                "size": file_stat.st_size,
                "perms": perms,
                "owner": owner,
                "group": group,
                "mtime": file_stat.st_mtime, 
                "ctime": file_stat.st_ctime  
            }
        except FileNotFoundError:
            return None

    def scan_directory(self):
        """
        Scans the directory and returns a dictionary of current files and their metadata.
        """
        current_state = {}
        try:
           
            for entry in os.listdir(self.directory_path):
                full_path = os.path.join(self.directory_path, entry)
                metadata = self.get_file_metadata(full_path)
                if metadata:
                    current_state[entry] = metadata
        except FileNotFoundError:
            print(f"Error: Directory {self.directory_path} not found.")
        return current_state

    def log_event(self, event_type, metadata, details=""):
        """
        Writes the event to the CSV log file.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
      
        if metadata is None:
            row = [timestamp, event_type, "Unknown", "N/A", "0", "N/A", "N/A", "N/A", details]
        else:
            row = [
                timestamp, 
                event_type, 
                metadata['filename'], 
                metadata['type'], 
                metadata['size'], 
                metadata['perms'], 
                metadata['owner'], 
                metadata['group'], 
                details
            ]

        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
        print(f"[{timestamp}] {event_type}: {row[2]} - {details}")

    def monitor_step(self):
        """
        Performs one check cycle: compares current state vs previous state.
        """
        current_state = self.scan_directory()

        
        if not self.previous_state:
            self.previous_state = current_state
            return

      
        for filename in current_state:
            if filename not in self.previous_state:
                meta = current_state[filename]
                self.log_event("CREATED", meta, f"Created at {datetime.fromtimestamp(meta['ctime'])}")

       
        for filename in self.previous_state:
            if filename not in current_state:
                # We use previous metadata to log what was deleted
                meta = self.previous_state[filename]
                self.log_event("DELETED", meta, "File removed")

        
        for filename in current_state:
            if filename in self.previous_state:
                curr_meta = current_state[filename]
                prev_meta = self.previous_state[filename]

                changes = []
            
                if curr_meta['size'] != prev_meta['size']:
                    changes.append(f"Size: {prev_meta['size']}->{curr_meta['size']}")
                
           
                if curr_meta['perms'] != prev_meta['perms']:
                    changes.append(f"Perms: {prev_meta['perms']}->{curr_meta['perms']}")
                
               
                if curr_meta['mtime'] != prev_meta['mtime']:
                    changes.append("Content Modified")

                if changes:
                    details = "; ".join(changes)
                    self.log_event("MODIFIED", curr_meta, details)

      
        self.previous_state = current_state

if __name__ == "__main__":
  
    MONITOR_DIR = "./monitor_test"
    
   
    if not os.path.exists(MONITOR_DIR):
        os.makedirs(MONITOR_DIR)
        print(f"Created test directory: {MONITOR_DIR}")

    print(f"Starting Monitor on {MONITOR_DIR}...")
    print("Press Ctrl+C to stop.")

  
    monitor = DirectoryMonitor(MONITOR_DIR)

    
    try:
        while True:
            monitor.monitor_step()
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nStopping Monitor.")
