#include "piece.h"
#include <iostream>

Piece::Piece() : Model() {};

Piece::Piece(const char *path) : Model(path) {};

void Piece::drawSolidAtPosition(GLuint &tex, float angleX, float angleY, glm::vec3 pos, bool isBlack) {
    glm::mat4 M = glm::mat4(1.0f); //Initialize model matrix with abn identity matrix
	M = glm::scale(M, glm::vec3(0.5f, 0.5f, 0.5f));
	// M = glm::rotate(M, 90.0f, glm::vec3(1.0f, 0.0f, 1.0f));
	M = glm::rotate(M, angleY, glm::vec3(0.0f, 1.0f, 0.0f)); //Multiply model matrix by the rotation matrix around Y axis by angle_y degrees
	M = glm::rotate(M, angleX, glm::vec3(1.0f, 0.0f, 0.0f)); //Multiply model matrix by the rotation matrix around X axis by angle_x degrees


	// M = glm::translate(M, glm::vec3(2.22f, 0.0f, 2.35f));
	if (isBlack)
		M = glm::rotate(M, glm::radians(180.0f), glm::vec3(0.0f, 1.0f, 0.0f));

    M = glm::translate(M, glm::vec3(0.0f, 1.0f, 0.0f)); // Move on top of the board
    
	if (isBlack)
		M = glm::translate(M, glm::vec3(-pos.x,pos.y,-pos.z));
	else
		M = glm::translate(M, pos);
	 
	// M = glm::translate(M, pos);

	glUniformMatrix4fv(spLambertTextured->u("M"), 1, false, glm::value_ptr(M));
	glEnableVertexAttribArray(spLambertTextured->a("vertex"));
	glVertexAttribPointer(spLambertTextured->a("vertex"), 4, GL_FLOAT, false, 0, &(vertices[0]));
	glEnableVertexAttribArray(spLambertTextured->a("normal"));
	glVertexAttribPointer(spLambertTextured->a("normal"), 4, GL_FLOAT, false, 0, &(normals[0]));
	glEnableVertexAttribArray(spLambertTextured->a("texCoord"));
	glVertexAttribPointer(spLambertTextured->a("texCoord"), 2, GL_FLOAT, false, 0, &(texCoords[0]));
	
	glActiveTexture(GL_TEXTURE0); 
	glBindTexture(GL_TEXTURE_2D, tex); 
	glUniform1i(spLambertTextured->u("tex"),0);
	glDrawArrays(GL_TRIANGLES, 0, vertexCount);

	glDisableVertexAttribArray(spLambertTextured->a("vertex"));
	glDisableVertexAttribArray(spLambertTextured->a("normal"));
	glDisableVertexAttribArray(spLambertTextured->a("texCoord"));
}