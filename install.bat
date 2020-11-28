rem Create python env
python -m venv venv
call venv\Scripts\activate

rem Install packages requirements
pip install -r requirements.txt

rem Build FortniteReplay .exe
cd src\FortniteReplay
dotnet publish
cd ..

rem Copy FortniteReplay .exe to root directory
copy FortniteReplay\bin\Debug\net5.0\win-x64\publish\FortniteReplay.exe .