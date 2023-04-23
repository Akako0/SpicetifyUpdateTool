@echo off

for /f "tokens=1,2 delims==" %%a in (update.conf) do set %%a=%%b

python update.py check_for_update

if %ERRORLEVEL% equ 1 (
    timeout /t 2 /nobreak >nul
    exit
)

if %ERRORLEVEL% equ 0 (
    echo Updating spicetify
    spicetify upgrade 
    spicetify restore backup apply
    if %UPDATE_MARKETPLACE% equ true (
        echo Updating marketplace
        spicetify upgrade -e
)
)

echo Spicetify Update completed
echo "  ______ __               __          ___                        _           "
echo " /_  __// /  ___ _ ___   / /__ ___   / _/___   ____  __ __ ___  (_)___  ___ _"
echo "  / /  / _ \/ _ `// _ \ /  '_/(_-<  / _// _ \ / __/ / // /(_-< / // _ \/ _ `/"
echo " /_/  /_//_/\_,_//_//_//_/\_\/___/ /_/  \___//_/    \_,_//___//_//_//_/\_, / "
echo "                                                                      /___/  "
echo "         ___     __           __             __                 __           "
echo "        /   |   / /__ ____ _ / /__ ____     / /_ ____   ____   / /_____      "
echo "       / /| |  / //_// __ `// //_// __ \   / __// __ \ / __ \ / // ___/      "
echo "      / ___ | / ,<  / /_/ // ,<  / /_/ /  / /_ / /_/ // /_/ // /(__  )       "
echo "     /_/  |_|/_/|_| \__,_//_/|_| \____/   \__/ \____/ \____//_//____/        "
timeout /t 5 /nobreak >nul