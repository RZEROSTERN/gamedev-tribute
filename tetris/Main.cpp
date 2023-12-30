#include <iostream>
#include "raylib.h"
#include "game.h"
#include "colors.h"

double lastUpdateTime = 0;

bool EventTriggered(double interval)
{
    double currentTime = GetTime();

    if (currentTime - lastUpdateTime >= interval)
    {
        lastUpdateTime = currentTime;
        return true;
    }

    return false;
}

int main()
{
    InitWindow(500, 620, "Tetris");
    SetTargetFPS(60);

    Font font = LoadFontEx("Font/fortress.ttf", 64, 0, 0);

    Game game = Game();

    while (WindowShouldClose() == false)
    {
        UpdateMusicStream(game.music);
        game.HandleInput();

        if (EventTriggered(0.2))
        {
            game.MoveTetriminoDown();
        }

        BeginDrawing();

        ClearBackground(darkBlue);

        DrawTextEx(font, "Score", {353, 16}, 36, 2, WHITE);
        DrawTextEx(font, "Next", {365, 160}, 36, 2, WHITE);

        if (game.gameOver)
        {
            DrawTextEx(font, "GAME OVER", {332, 450}, 24, 2, WHITE);
        }

        DrawRectangleRounded({320, 64, 170, 60}, 0.3, 6, lightBlue);

        char scoreText[10];
        sprintf(scoreText, "%d", game.score);
        Vector2 textSize = MeasureTextEx(font, scoreText, 38, 2);

        DrawTextEx(font, scoreText, {320 + (170 - textSize.x) / 2, 75}, 36, 2, WHITE);
        DrawRectangleRounded({320, 215, 170, 180}, 0.3, 6, lightBlue);

        game.Draw();

        EndDrawing();
    }

    CloseWindow();
}