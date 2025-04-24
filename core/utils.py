from pathlib import Path

def get_windows_default_log_dir():
    import os
    user = os.environ['USERPROFILE']
    default_path = Path(user) / 'Documents' / 'Paradox Interactive' / 'Crusader Kings III' / 'logs'
    if not default_path.exists():
        # If the default path doesn't exist, return the current directory
        return Path.cwd() / 'logs'
    return