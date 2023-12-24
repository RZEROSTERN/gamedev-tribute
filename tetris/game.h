#pragma once
#include "grid.h"
#include "tetriminos.cpp"

class Game
{
public:
    Game();
    ~Game();

    bool gameOver;
    int score;
    Music music;

    void Draw();
    void HandleInput();
    void MoveTetriminoDown();

private:
    Tetrimino GetRandomTetrimino();
    std::vector<Tetrimino> GetAllTetriminos();

    bool IsTetriminoOutside();
    void RotateTetrimino();
    void LockTetrimino();
    bool TetriminoFits();
    void Reset();
    void UpdateScore(int linesCleared, int moveDownPoints);
    void MoveTetriminoLeft();
    void MoveTetriminoRight();

    Grid grid;
    std::vector<Tetrimino> tetriminos;
    Tetrimino currentTetrimino;
    Tetrimino nextTetrimino;
    Sound rotateSound;
    Sound clearSound;
};