# PONG!

## Compile!
### For Windows
``` shell
g++ Main.cpp -o pong.exe -O1 -Wall -std=c++17 -Wno-missing-braces -I include/windows/ -L lib/windows/ -lraylib -lopengl32 -lgdi32 -lwinmm
```

### For MacOS (Linux to confirm)
Ensure you have installed raylib from brew.
``` shell
 g++ Main.cpp -o pong -O1 -Wall -std=c++17 -Wno-missing-braces -I /opt/homebrew/Cellar/raylib/5.0/include -L /opt/homebrew/Cellar/raylib/5.0/lib -lraylib
```

## References


Made in Mexico with <3 by RZEROSTERN