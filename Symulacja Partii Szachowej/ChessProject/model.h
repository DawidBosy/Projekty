#ifndef MODEL_H
#define MODEL_H

#include <GL/glew.h>
#include <vector>
#include <glm/glm.hpp>
#include <GLFW/glfw3.h>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "shaderprogram.h"
#include "loadOBJ.h"

class Model {
    public:
        int vertexCount;
        glm::vec3 point;
        glm::vec3 size;
        std::vector<float> vertices;
        std::vector<float> texCoords;
        std::vector<float> normals;
        Model();
        Model(const char *path);
        ~Model();
        virtual void drawSolid(GLuint &tex, float angleX, float angleY);
        void moveBy(glm::vec2 pos);
};

#endif