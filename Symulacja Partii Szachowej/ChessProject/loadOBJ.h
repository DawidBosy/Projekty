#ifndef LOADOBJ_H
#define LOADOBJ_H

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <stdlib.h>
#include <stdio.h>
#include <vector>

bool loadOBJ(const char * path,
             std::vector < float > &vertices,
             std::vector < float > &uvs,
             std::vector < float > &normals,
             glm::vec3 &point,
             glm::vec3 &size,
             int &vertexCount
            );

#endif