import subprocess


def _is_float_string(x: str) -> bool:
    try:
        float(x)
    except ValueError:
        return False
    return True


def _get_chrome_window_at_url(url: str, use_incognito: bool=True) -> None:
    command_list = [
        'google-chrome',
        '--new-window',
        url,
    ]

    if use_incognito:
        command_list = command_list[:-1] + ['--incognito'] + command_list[-1:]

    subprocess.call(command_list)


def get_cost_from_browser_and_manual_input(url: str, user_prompt: str) -> float:
    # First, generate webpage to allow user to access info
    _get_chrome_window_at_url(url)

    # Then collect user response
    response: str = input(user_prompt)

    if not _is_float_string(response):
        raise AssertionError('user did not provide a float string')

    return float(response)
