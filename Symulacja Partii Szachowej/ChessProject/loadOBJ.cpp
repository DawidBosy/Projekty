#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <iostream>
#include <limits>
#include <string>
#include <algorithm>
#include "loadOBJ.h"
#include "tiny_obj_loader.h"

bool loadOBJ(const char * path, std::vector < float > & vertices,
             std::vector < float > & uvs,
             std::vector < float > & normals,
             glm::vec3 &point,
             glm::vec3 &size,
             int &vertexCount
            ) {
    tinyobj::attrib_t attrib;
    std::vector<tinyobj::shape_t> shapes;
    std::vector<tinyobj::material_t> materials;

    std::vector<float> x, y, z;

    std::string warn;
    std::string err;

    bool ret = tinyobj::LoadObj(&attrib, &shapes, &materials, &warn, &err, path);

    if (!warn.empty()) {
        std::cout << warn << std::endl;
    }

    if (!err.empty()) {
        std::cerr << err << std::endl;
    }

    if (!ret) {
        exit(1);
    }

    vertexCount = 0;
    // Loop over shapes
    for (size_t s = 0; s < shapes.size(); s++) {
        // Loop over faces(polygon)
        size_t index_offset = 0;
        for (size_t f = 0; f < shapes[s].mesh.num_face_vertices.size(); f++) {
            size_t fv = size_t(shapes[s].mesh.num_face_vertices[f]);

            // Loop over vertices in the face.
            for (size_t v = 0; v < fv; v++) {
            // access to vertex
                tinyobj::index_t idx = shapes[s].mesh.indices[index_offset + v];

                float vx = attrib.vertices[3*size_t(idx.vertex_index)+0];
                float vy = attrib.vertices[3*size_t(idx.vertex_index)+1];
                float vz = attrib.vertices[3*size_t(idx.vertex_index)+2];

                vertexCount++;

                vertices.push_back(vx);
                vertices.push_back(vy);
                vertices.push_back(vz);
                vertices.push_back(1.0f);
                
                x.push_back(vx);
                y.push_back(vy);
                z.push_back(vz);

                // Check if `normal_index` is zero or positive. negative = no normal data
                if (idx.normal_index >= 0) {
                    float nx = attrib.normals[3*size_t(idx.normal_index)+0];
                    float ny = attrib.normals[3*size_t(idx.normal_index)+1];
                    float nz = attrib.normals[3*size_t(idx.normal_index)+2];

                    normals.push_back(nx);
                    normals.push_back(ny);
                    normals.push_back(nz);
                    normals.push_back(0.0f);
                }

                // Check if `texcoord_index` is zero or positive. negative = no texcoord data
                if (idx.texcoord_index >= 0) {
                    float tx = attrib.texcoords[2*size_t(idx.texcoord_index)+0];
                    float ty = attrib.texcoords[2*size_t(idx.texcoord_index)+1];

                    uvs.push_back(tx);
                    uvs.push_back(ty);
                }
                // Optional: vertex colors
                // tinyobj::real_t red   = attrib.colors[3*size_t(idx.vertex_index)+0];
                // tinyobj::real_t green = attrib.colors[3*size_t(idx.vertex_index)+1];
                // tinyobj::real_t blue  = attrib.colors[3*size_t(idx.vertex_index)+2];
            }
            index_offset += fv;

            // per-face material
            shapes[s].mesh.material_ids[f];
        }
    }

    float maxX = *std::max_element(x.begin(), x.end());
	float maxY = *std::max_element(y.begin(), y.end());
	float maxZ = *std::max_element(z.begin(), z.end());

    float minX = *std::min_element(x.begin(), x.end());
	float minY = *std::min_element(y.begin(), y.end());
	float minZ = *std::min_element(z.begin(), z.end());

    point = glm::vec3(-(maxX + minX) / 2.0f, -(maxY + minY) / 2.0f, -(maxZ + minZ) / 2.0f);
    size = glm::vec3(maxX - minX, maxY - minY, maxZ - minZ);

    return true;
}