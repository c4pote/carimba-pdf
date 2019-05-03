pyinstaller --noconfirm --log-level=WARN ^
    --onefile --nowindow ^
    --add-data="settings.txt;." ^
    --add-data="carimbador.png;img" ^
    --icon=carimbador.ico ^
    main.spec

copy settings.txt dist
copy carimbador.png dist
