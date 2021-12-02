
for /r %%i in (*.md) do (
     git log -p --author=Altti99 %%i 
     git blame <filename> | grep <authorname>

)

rem FOR /L %%A IN (*.md) DO (
rem   ECHO %%A
rem )