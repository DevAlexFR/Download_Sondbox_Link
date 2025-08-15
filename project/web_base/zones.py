import winreg
from time import sleep


def disable_protected_mode():
    """Desabilita o modo protegido do IE."""
    HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER

    def set_key_value(key_path, value_name, value):
        key = winreg.CreateKey(HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)

    def get_key_value(key_path, value_name):
        key = winreg.CreateKey(HKEY_CURRENT_USER, key_path)
        value = winreg.QueryValueEx(key, value_name)[0]
        winreg.CloseKey(key)
        return value

    # Disable protected mode for local intranet
    key_path = (
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\0'
    )
    value_name = '2500'
    value = 0
    set_key_value(key_path, value_name, value)

    # Disable protected mode for local intranet
    key_path = (
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\1'
    )
    value_name = '2500'
    value = 0
    set_key_value(key_path, value_name, value)

    # Disable protected mode for trusted pages
    key_path = (
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\2'
    )
    value_name = '2500'
    value = 0
    set_key_value(key_path, value_name, value)

    # Disable protected mode for internet
    key_path = (
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\3'
    )
    value_name = '2500'
    value = 0
    set_key_value(key_path, value_name, value)

    # Disable protected mode for restricted sites
    key_path = (
        r'Software\Microsoft\Windows\CurrentVersion\Internet Settings\Zones\4'
    )
    value_name = '2500'
    value = 0
    set_key_value(key_path, value_name, value)

    while get_key_value(key_path, value_name):
        sleep(0.5)


if __name__ == '__main__':
    disable_protected_mode()
