#include "iostream"
#include "raylib.h"

using namespace std;

int playerScore = 0;
int cpuScore = 0;

class Ball
{
public:
    float x, y;
    int speedX, speedY;
    int radius;

    void Draw()
    {
        DrawCircle(x, y, radius, WHITE);
    }

    void Update()
    {
        x += speedX;
        y += speedY;

        if (y + radius >= GetScreenHeight() || y - radius <= 0)
        {
            speedY *= -1;
        }

        if (x + radius >= GetScreenWidth())
        {
            cpuScore++;
            ResetBall();
        }

        if (x - radius <= 0)
        {
            playerScore++;
            ResetBall();
        }
    }

    void ResetBall()
    {
        x = GetScreenWidth() / 2;
        y = GetScreenHeight() / 2;

        int speedChoices[2] = {-1, 1};
        speedX *= speedChoices[GetRandomValue(0, 1)];
        speedY *= speedChoices[GetRandomValue(0, 1)];
    }
};

class Paddle
{
protected:
    void LimitMovement()
    {
        if (y <= 0)
        {
            y = 0;
        }

        if (y + height >= GetScreenHeight())
        {
            y = GetScreenHeight() - height;
        }
    }

public:
    float x, y;
    float width, height;
    int speed;

    void Draw()
    {
        DrawRectangle(x, y, width, height, WHITE);
    }

    void Update()
    {
        if (IsKeyDown(KEY_UP))
        {
            y = y - speed;
        }

        if (IsKeyDown(KEY_DOWN))
        {
            y = y + speed;
        }

        LimitMovement();
    }
};

class CPUPaddle : public Paddle
{
public:
    void Update(int ballY)
    {
        if (y + height / 2 > ballY)
        {
            y = y - speed;
        }

        if (y + height / 2 <= ballY)
        {
            y = y + speed;
        }

        LimitMovement();
    }
};

Ball ball;
Paddle player;
CPUPaddle cpu;

int main()
{
    cout << "Starting Pong..." << endl;

    const int width = 1280;
    const int height = 800;

    InitWindow(width, height, "PONG!");
    SetTargetFPS(60);

    ball.radius = 20;
    ball.x = width / 2;
    ball.y = height / 2;
    ball.speedX = 7;
    ball.speedY = 7;

    player.width = 25;
    player.height = 120;
    player.x = width - player.width - 10;
    player.y = (height / 2) - (player.height / 2);
    player.speed = 6;

    cpu.width = 25;
    cpu.height = 120;
    cpu.x = 10;
    cpu.y = height / 2 - cpu.height / 2;
    cpu.speed = 6;

    while (!WindowShouldClose())
    {
        BeginDrawing();

        ball.Update();
        player.Update();
        cpu.Update(ball.y);

        if (CheckCollisionCircleRec(Vector2{ball.x, ball.y}, ball.radius, Rectangle{player.x, player.y, player.width, player.height}))
        {
            ball.speedX *= -1;
        }

        if (CheckCollisionCircleRec(Vector2{ball.x, ball.y}, ball.radius, Rectangle{cpu.x, cpu.y, cpu.width, cpu.height}))
        {
            ball.speedX *= -1;
        }

        ClearBackground(BLACK);

        DrawLine(width / 2, 0, width / 2, height, WHITE);
        ball.Draw();
        cpu.Draw();
        player.Draw();
        DrawText(TextFormat("%i", cpuScore), width / 4 - 20, 20, 80, WHITE);
        DrawText(TextFormat("%i", playerScore), (3 * width / 4) - 20, 20, 80, WHITE);

        EndDrawing();
    }

    CloseWindow();
    return 0;
}