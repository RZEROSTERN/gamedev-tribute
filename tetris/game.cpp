#include "game.h"
#include <random>

Game::Game()
{
    grid = Grid();
    tetriminos = GetAllTetriminos();
    currentTetrimino = GetRandomTetrimino();
    nextTetrimino = GetRandomTetrimino();
    gameOver = false;
    score = 0;
    InitAudioDevice();
    music = LoadMusicStream("Sounds/bradinsky.mp3");
    PlayMusicStream(music);
    rotateSound = LoadSound("Sounds/rotate.mp3");
    clearSound = LoadSound("Sounds/clear.mp3");
}

Game::~Game()
{
    UnloadMusicStream(music);
    UnloadSound(rotateSound);
    UnloadSound(clearSound);
    CloseAudioDevice();
}

Tetrimino Game::GetRandomTetrimino()
{
    if (tetriminos.empty())
    {
        tetriminos = GetAllTetriminos();
    }

    int randomIndex = rand() % tetriminos.size();

    Tetrimino tetrimino = tetriminos[randomIndex];
    tetriminos.erase(tetriminos.begin() + randomIndex);

    return tetrimino;
}

std::vector<Tetrimino> Game::GetAllTetriminos()
{
    return {ITetrimino(), JTetrimino(), LTetrimino(), OTetrimino(), STetrimino(), TTetrimino(), ZTetrimino()};
}

void Game::Draw()
{
    grid.Draw();
    currentTetrimino.Draw(11, 11);

    switch (nextTetrimino.id)
    {
    case 3:
        nextTetrimino.Draw(255, 290);
        break;

    case 4:
        nextTetrimino.Draw(255, 280);
        break;
    default:
        nextTetrimino.Draw(270, 270);
        break;
    }
}

void Game::HandleInput()
{
    int keyPressed = GetKeyPressed();

    if (gameOver && keyPressed != 0)
    {
        gameOver = false;
        Reset();
    }

    switch (keyPressed)
    {
    case KEY_LEFT:
        MoveTetriminoLeft();
        break;
    case KEY_RIGHT:
        MoveTetriminoRight();
        break;
    case KEY_DOWN:
        MoveTetriminoDown();
        UpdateScore(0, 1);
        break;
    case KEY_UP:
        RotateTetrimino();
        break;
    }
}

void Game::MoveTetriminoLeft()
{
    if (!gameOver)
    {
        currentTetrimino.Move(0, -1);

        if (IsTetriminoOutside() || TetriminoFits() == false)
        {
            currentTetrimino.Move(0, 1);
        }
    }
}

void Game::MoveTetriminoRight()
{
    if (!gameOver)
    {
        currentTetrimino.Move(0, 1);

        if (IsTetriminoOutside() || TetriminoFits() == false)
        {
            currentTetrimino.Move(0, -1);
        }
    }
}

void Game::MoveTetriminoDown()
{
    if (!gameOver)
    {
        currentTetrimino.Move(1, 0);

        if (IsTetriminoOutside() || TetriminoFits() == false)
        {
            currentTetrimino.Move(-1, 0);
            LockTetrimino();
        }
    }
}

bool Game::IsTetriminoOutside()
{
    std::vector<Position> tiles = currentTetrimino.GetCellPosition();

    for (Position item : tiles)
    {
        if (grid.IsCellOutside(item.row, item.col))
        {
            return true;
        }
    }

    return false;
}

void Game::RotateTetrimino()
{
    if (!gameOver)
    {
        currentTetrimino.Rotate();
        if (IsTetriminoOutside())
        {
            currentTetrimino.UndoRotation();
        }
        else
        {
            PlaySound(rotateSound);
        }
    }
}

void Game::LockTetrimino()
{
    std::vector<Position> tiles = currentTetrimino.GetCellPosition();

    for (Position item : tiles)
    {
        grid.grid[item.row][item.col] = currentTetrimino.id;
    }

    currentTetrimino = nextTetrimino;

    if (TetriminoFits() == false)
    {
        gameOver = true;
    }

    nextTetrimino = GetRandomTetrimino();

    int rowsCleared = grid.ClearFullRows();

    if (rowsCleared > 0)
    {
        PlaySound(clearSound);
        UpdateScore(rowsCleared, 0);
    }
}

bool Game::TetriminoFits()
{
    std::vector<Position> tiles = currentTetrimino.GetCellPosition();

    for (Position item : tiles)
    {
        if (grid.IsCellEmpty(item.row, item.col) == false)
        {
            return false;
        }
    }

    return true;
}

void Game::Reset()
{
    grid.Initialize();
    tetriminos = GetAllTetriminos();
    currentTetrimino = GetRandomTetrimino();
    nextTetrimino = GetRandomTetrimino();
    score = 0;
}

void Game::UpdateScore(int linesCleared, int moveDownPoints)
{
    switch (linesCleared)
    {
    case 1:
        score += 250;
        break;
    case 2:
        score += 500;
        break;
    case 3:
        score += 750;
        break;
    case 4:
        score += 1000;
        break;
    default:
        break;
    }

    score += moveDownPoints;
}
