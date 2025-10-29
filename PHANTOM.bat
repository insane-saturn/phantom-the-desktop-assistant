@echo off 
cd C:\Users\PC\Downloads 
python PHANTOM.py
if errorlevel 1 (
    echo.
    echo ==================
    echo ERROR OCCURRED!
    echo ==================
)
pause
```

Then run it and tell me **everything you see** - even if it's just one line.

---

**OR even better - let's see the error directly:**

1. Press `Windows Key + R`
2. Type: `cmd`
3. Press Enter
4. Type these commands:
```
   cd C:\Users\PC\Downloads
   python PHANTOM.py
