$envName = ".venv"
$scriptName = "autojoin.py"

function Ensure-PythonInPath {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue

    if (-not $pythonCmd) {
        #Try adding WindowsApps manually (common Microsoft Store install path)
        $storePath = "$env:LOCALAPPDATA\Microsoft\WindowsApps"
        if (Test-Path "$storePath\python.exe") {
            Write-Host "Adding Microsoft Store Python path temporarily..."
            $env:Path += ";$storePath"
            $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
        }
    }

    return $pythonCmd
}

function Check-Python {
    $cmd = Ensure-PythonInPath
    if (-not $cmd) {
        Write-Host "Python command not found in PATH."
        return $false
    }

    try {
        $versionOutput = & python --version 2>&1
        if ($versionOutput -match "Python\s+[3-9]\.\d+") {
            Write-Host "Python detected: $versionOutput"
            return $true
        } else {
            Write-Host "Unexpected python version output: $versionOutput"
            return $false
        }
    } catch {
        Write-Host "Error checking Python version."
        return $false
    }
}

function Install-Python {
    Write-Host "Python not found or not working correctly."
    Write-Host "Opening Microsoft Store to install Python..."
    Start-Process "ms-windows-store://pdp/?ProductId=9PJPW5LDXLZ5"
    Write-Host "Please install Python manually, then re-run this script."
    exit 1
}

#Check Python
if (-not (Check-Python)) {
    Install-Python
}

#Create venv
if (-not (Test-Path $envName)) {
    Write-Host "Creating virtual environment..."
    python -m venv $envName
}

#Activate venv
$activateScript = ".\$envName\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "Virtual environment activation script not found." -ForegroundColor Red
    exit 1
}

Write-Host "Activating virtual environment..."
. $activateScript

#Install requirements
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies..."
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found!" -ForegroundColor Yellow
}

#Run
Write-Host "Launching $scriptName..."
python $scriptName