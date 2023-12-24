#pragma once
#include <vector>
#include <map>
#include "position.h"
#include "colors.h"

class Tetrimino
{
public:
    Tetrimino();
    void Draw(int offsetX, int offsetY);
    void Move(int rows, int cols);
    void Rotate();
    void UndoRotation();

    std::vector<Position> GetCellPosition();
    int id;
    std::map<int, std::vector<Position>> cells;

private:
    int cellSize;
    int rotationState;
    std::vector<Color> colors;
    int rowOffset;
    int colOffset;
};