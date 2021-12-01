#ifndef PIECE_H
#define PIECE_H

#include "model.h"

class Piece: public Model {
    public:
        Piece();
        Piece(const char* path);
        void drawSolidAtPosition(GLuint &tex, float angleX, float angleY, glm::vec3 pos, bool isWhite);
};

#endif