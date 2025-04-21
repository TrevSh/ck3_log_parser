def get_windows_default_log_dir(self):
    import os
    user = os.environ['USERPROFILE']
    return Path(user) / 'Documents' / 'Paradox Interactive' / 'Crusader Kings III' / 'logs'