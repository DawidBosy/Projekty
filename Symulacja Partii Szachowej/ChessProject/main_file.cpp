/*
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#define TINYOBJLOADER_IMPLEMENTATION
#define GLM_FORCE_RADIANS

#include <windows.h>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <stdlib.h>
#include <stdio.h>
#include "lodepng.h"
#include "shaderprogram.h"
#include "tiny_obj_loader.h"
#include "loadOBJ.h"
#include "model.h"
#include "piece.h"
#include <algorithm>
#include <vector>
#include <iostream>
#include <PGNGameCollection.h> 
#include <PGNPosition.h> 

const float PI = 3.141592653589793f;

GLuint texBoard;
GLuint texWhite;
GLuint texBlack;

Model chessboard;
Piece pawn;
Piece rook;
Piece bishop;
Piece knight;
Piece queen;
Piece king;

bool CameraMoves = false;
bool firstMouse = true;
int movePassed = 0;
int GlobIterator = 0;
int actualPiece = 0;
int WDCount = 0;
int BDCount = 0;
int moves = 0;
float angle_x = 0; //declare variable for storing current rotation angle
float angle_y = 0; //declare variable for storing current rotation angle
float speed_x = 0;//[radians/s]
float speed_y = 0;//[radians/s]
float finalX = 0;
float finalZ = 0;
float finalY = 0;
float XDiff = 0;
float YDiff = 40;
float ZDiff = 0;
float fullDistance = 0;
float actualDistance = 0;
float cameraSpeed;// adjust accordingly
float deltaTime = 0.0f;	// Time between current frame and last frame
float lastFrame = 0.0f; // Time of last frame
float currentFrame;
float movementSpeed = 0.02f;
float yaw = -180.0f;
float pitch = -27.0f;
float lastX = 250;
float lastY = 250;
float fov = 45.0f;
float xoffset = 0;
float yoffset = 0;

std::vector<std::vector<glm::vec3>> MoveLists(500);
std::vector<std::vector<glm::vec3>> UpdatedMoves(500);
std::vector<std::vector<std::string>> MoveCharLists(500);

std::vector<glm::vec3> squares;
std::vector<glm::vec3> WDeletePos;
std::vector<glm::vec3> BDeletePos;
std::vector<glm::vec3> PiecesStartPos;
std::vector<glm::vec3> PiecesActualPos;
std::vector<glm::vec3> PiecesFinalPos;
std::vector<std::string> OccupiedPos;

glm::vec3 cameraPos = glm::vec3(30.0f, 20.0f, 0.0f);
glm::vec3 cameraFront = glm::vec3(-30.0f, -15.0f, 0.0f);
glm::vec3 cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);

int squareToInt(const char* pos) {
	return (pos[0] - 'a') * 8 + (pos[1] - '1');
}
int squareToInt(std::string pos) {
	return (char(pos[0]) - 'a') * 8 + (char(pos[1]) - '1');
}

void check(const char* text) {
	int code = glGetError();
	if (code != 0) {
		printf("Wykryto b³¹d z kodem b³êdu 0x%04X: %s\n", code, text);
	}
}

bool areEqual(glm::vec3 First, glm::vec3 Second) {
	if (First.x == Second.x && First.y == Second.y && First.z == Second.z)
		return 1;
	else return 0;
}

GLuint readTexture(const char* filename) {
	GLuint tex;
	glActiveTexture(GL_TEXTURE0);

	//Read the file into computers memory
	std::vector<unsigned char> image;   //Allocate a vector for storing the image
	unsigned width, height;   //Variables which will contain the image size
	//Read the image
	unsigned error = lodepng::decode(image, width, height, filename);

	//Import the image into graphics cards memory
	glGenTextures(1, &tex); //Initialize one handle
	glBindTexture(GL_TEXTURE_2D, tex); //Activate handle (bind it to the active texturing unit)
	//Import the image into the GC memory associated with the handle
	glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0,
		GL_RGBA, GL_UNSIGNED_BYTE, (unsigned char*)image.data());

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	return tex;
}

//Error processing callback procedure
void error_callback(int error, const char* description) {
	fputs(description, stderr);
}


void scroll_callback(GLFWwindow* window, double xoffset, double yoffset)
{
	fov -= (float)yoffset;
	if (fov < 1.0f)
		fov = 1.0f;
	if (fov > 45.0f)
		fov = 45.0f;
}

void windowResizeHandler(int windowWidth, int windowHeight) {
	const float aspectRatio = ((float)windowWidth) / windowHeight;
	float xSpan = 1; // Feel free to change this to any xSpan you need.
	float ySpan = 1; // Feel free to change this to any ySpan you need.

	if (aspectRatio > 1) {
		// Width > Height, so scale xSpan accordinly.
		xSpan *= aspectRatio;
	}
	else {
		// Height >= Width, so scale ySpan accordingly.
		ySpan = xSpan / aspectRatio;
	}

	glFrustum(-1 * xSpan, xSpan, -1 * ySpan, ySpan, -1, 1);

	// Use the entire window for rendering.
	glViewport(0, 0, windowWidth, windowHeight);
}

void mouse_callback(GLFWwindow* window, double xpos, double ypos)
{

	if (CameraMoves) {
		if (firstMouse)
		{
			lastX = xpos;
			lastY = ypos;
			firstMouse = false;
		}

		xoffset = xpos - lastX;
		yoffset = lastY - ypos;
		lastX = xpos;
		lastY = ypos;

		float sensitivity = 0.1f;
		xoffset *= sensitivity;
		yoffset *= sensitivity;

		yaw += xoffset;
		pitch += yoffset;

		if (pitch > 89.0f)
			pitch = 89.0f;
		if (pitch < -89.0f)
			pitch = -89.0f;

		glm::vec3 direction;
		direction.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
		direction.y = sin(glm::radians(pitch));
		direction.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
		cameraFront = glm::normalize(direction);
	}
}
void initSquares() {
	for (float i = -15.54f; i < 15.6f; i += 4.44f) {
		for (float j = 15.7f; j > -15.8f; j -= 4.45f) {
			squares.push_back(glm::vec3(i, 0.0f, j));
		}
	}
}

void processInput(GLFWwindow* window)
{
	cameraSpeed = 5.0f * deltaTime;
	if (glfwGetKey(window, GLFW_KEY_R) == GLFW_PRESS) {
		cameraPos = glm::vec3(30.0f, 20.0f, 0.0f); //reset kamery
		cameraFront = glm::vec3(-30.0f, -15.0f, 0.0f);
		cameraUp = glm::vec3(0.0f, 1.0f, 0.0f);
		yaw = -180.0f;
		pitch = -27.0f;
		fov = 45.0f;
	}
	if (glfwGetKey(window, GLFW_KEY_SPACE) == GLFW_PRESS)
		CameraMoves = true;
	else {
		CameraMoves = false;
		firstMouse = true;
	}
	if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
		cameraPos += cameraSpeed * glm::normalize(cameraFront);
	if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
		cameraPos -= cameraSpeed * glm::normalize(cameraFront);
	if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
		cameraPos -= glm::normalize(glm::cross(cameraFront, cameraUp)) * cameraSpeed;
	if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
		cameraPos += glm::normalize(glm::cross(cameraFront, cameraUp)) * cameraSpeed;
	if (glfwGetKey(window, GLFW_KEY_1) == GLFW_PRESS)
		movementSpeed = 0;
	if (glfwGetKey(window, GLFW_KEY_2) == GLFW_PRESS)
		movementSpeed = 0.02;
	if (glfwGetKey(window, GLFW_KEY_3) == GLFW_PRESS)
		movementSpeed = 0.04;
	if (glfwGetKey(window, GLFW_KEY_4) == GLFW_PRESS)
		movementSpeed = 0.1;
	if (glfwGetKey(window, GLFW_KEY_5) == GLFW_PRESS)
		movementSpeed = 0.2;
}

void initModels() {
	chessboard = Model("Models/chessboard.obj");
	pawn = Piece("Models/pawn.obj");
	rook = Piece("Models/rook.obj");
	knight = Piece("Models/knight.obj");
	bishop = Piece("Models/bishop.obj");
	queen = Piece("Models/queen.obj");
	king = Piece("Models/king.obj");
}

void ExpandMoves() {
	for (int it = 0;it < moves; it++) {
		if (find(OccupiedPos.begin(), OccupiedPos.end(), MoveCharLists[it][1]) != OccupiedPos.end()) { 
			UpdatedMoves[movePassed].push_back(MoveLists[it][1]);
			if (find(OccupiedPos.begin(), OccupiedPos.end(), MoveCharLists[it][1]) - OccupiedPos.begin() >= 16) 
				UpdatedMoves[movePassed].push_back(BDeletePos[BDCount++]);
			else	UpdatedMoves[movePassed].push_back(WDeletePos[WDCount++]);
			OccupiedPos[find(OccupiedPos.begin(), OccupiedPos.end(), MoveCharLists[it][1]) - OccupiedPos.begin()] = "00";
			movePassed++;
		}
		auto index = find(OccupiedPos.begin(), OccupiedPos.end(), MoveCharLists[it][0]);
		OccupiedPos[index - OccupiedPos.begin()] = MoveCharLists[it][1]; // update of occupiedPos, as the moves are going
		UpdatedMoves[movePassed].push_back(MoveLists[it][0]);
		UpdatedMoves[movePassed].push_back(MoveLists[it][1]);
		movePassed++;
	}
}

void initOpenGLProgram(GLFWwindow* window) {
	initShaders();
	glClearColor(0.25, 0.25, 0.25, 1); //Set color buffer clear color
	glEnable(GL_DEPTH_TEST); //Turn on pixel depth test based on depth buffer


	texBoard = readTexture("Textures/chessboard.png");
	texWhite = readTexture("Textures/white.png");
	texBlack = readTexture("Textures/black.png");

	initModels();
	glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
	glfwSetCursorPosCallback(window, mouse_callback);
	glfwSetScrollCallback(window, scroll_callback);

	//DECODE OF PIECES NUMERATION
	//Indexes: (when pair of figures, always starting from left from viewers perspective)
	//0-7 - white pawns
	//8 and 9 - white rooks
	//10 and 11 - white knights
	//12 and 13 - white bishops
	//14 - queen
	//15 - king
	//16 - 23 - black pawns
	//24 and 25 - white rooks
	//26 and 27 - white knights 
	//28 and 29 - white bishops
	//30 - queen
	//31 - king
	WDeletePos = { glm::vec3(-16.0f,0.0f,24.15f),glm::vec3(-12.0f,0.0f,24.15f),glm::vec3(-8.0f,0.0f,24.15f),glm::vec3(-4.0f,0.0f,24.15f),
	glm::vec3(-16.0f,0.0f,28.15f),glm::vec3(-12.0f,0.0f,28.15f),glm::vec3(-8.0f,0.0f,28.15f),glm::vec3(-4.0f,0.0f,28.15f) ,
	glm::vec3(-16.0f,0.0f,32.15f),glm::vec3(-12.0f,0.0f,32.15f),glm::vec3(-8.0f,0.0f,32.15f),glm::vec3(-4.0f,0.0f,32.15f) ,
	glm::vec3(-16.0f,0.0f,36.15f),glm::vec3(-12.0f,0.0f,36.15f),glm::vec3(-8.0f,0.0f,36.15f),glm::vec3(-4.0f,0.0f,36.15f) };

	BDeletePos = { glm::vec3(-16.0f,0.0f,-24.15f),glm::vec3(-12.0f,0.0f,-24.15f),glm::vec3(-8.0f,0.0f,-24.15f),glm::vec3(-4.0f,0.0f,-24.15f),
	glm::vec3(-16.0f,0.0f,-28.15f),glm::vec3(-12.0f,0.0f,-28.15f),glm::vec3(-8.0f,0.0f,-28.15f),glm::vec3(-4.0f,0.0f,-28.15f) ,
	glm::vec3(-16.0f,0.0f,-32.15f),glm::vec3(-12.0f,0.0f,-32.15f),glm::vec3(-8.0f,0.0f,-32.15f),glm::vec3(-4.0f,0.0f,-32.15f) ,
	glm::vec3(-16.0f,0.0f,-36.15f),glm::vec3(-12.0f,0.0f,-36.15f),glm::vec3(-8.0f,0.0f,-36.15f),glm::vec3(-4.0f,0.0f,-36.15f)};
	//WHITE
	PiecesStartPos = { squares[squareToInt("a2")],squares[squareToInt("b2")],squares[squareToInt("c2")],squares[squareToInt("d2")],squares[squareToInt("e2")],squares[squareToInt("f2")],squares[squareToInt("g2")],squares[squareToInt("h2")]
		,squares[squareToInt("a1")] ,squares[squareToInt("h1")] ,squares[squareToInt("b1")] ,squares[squareToInt("g1")] ,squares[squareToInt("c1")] ,squares[squareToInt("f1")] ,squares[squareToInt("d1")] ,squares[squareToInt("e1")]
		,squares[squareToInt("a7")] ,squares[squareToInt("b7")] ,squares[squareToInt("c7")] ,squares[squareToInt("d7")] ,squares[squareToInt("e7")] ,squares[squareToInt("f7")] ,squares[squareToInt("g7")] ,squares[squareToInt("h7")] 
		,squares[squareToInt("a8")] ,squares[squareToInt("h8")] ,squares[squareToInt("b8")] ,squares[squareToInt("g8")] ,squares[squareToInt("c8")] ,squares[squareToInt("f8")] ,squares[squareToInt("d8")] ,squares[squareToInt("e8")] };


	PiecesFinalPos = { squares[squareToInt("a2")],squares[squareToInt("b2")],squares[squareToInt("c2")],squares[squareToInt("d2")],squares[squareToInt("e2")],squares[squareToInt("f2")],squares[squareToInt("g2")],squares[squareToInt("h2")]
		,squares[squareToInt("a1")] ,squares[squareToInt("h1")] ,squares[squareToInt("b1")] ,squares[squareToInt("g1")] ,squares[squareToInt("c1")] ,squares[squareToInt("f1")] ,squares[squareToInt("d1")] ,squares[squareToInt("e1")]
		,squares[squareToInt("a7")] ,squares[squareToInt("b7")] ,squares[squareToInt("c7")] ,squares[squareToInt("d7")] ,squares[squareToInt("e7")] ,squares[squareToInt("f7")] ,squares[squareToInt("g7")] ,squares[squareToInt("h7")]
		,squares[squareToInt("a8")] ,squares[squareToInt("h8")] ,squares[squareToInt("b8")] ,squares[squareToInt("g8")] ,squares[squareToInt("c8")] ,squares[squareToInt("f8")] ,squares[squareToInt("d8")] ,squares[squareToInt("e8")] };
	

	PiecesActualPos = { squares[squareToInt("a2")],squares[squareToInt("b2")],squares[squareToInt("c2")],squares[squareToInt("d2")],squares[squareToInt("e2")],squares[squareToInt("f2")],squares[squareToInt("g2")],squares[squareToInt("h2")]
		,squares[squareToInt("a1")] ,squares[squareToInt("h1")] ,squares[squareToInt("b1")] ,squares[squareToInt("g1")] ,squares[squareToInt("c1")] ,squares[squareToInt("f1")] ,squares[squareToInt("d1")] ,squares[squareToInt("e1")]
		,squares[squareToInt("a7")] ,squares[squareToInt("b7")] ,squares[squareToInt("c7")] ,squares[squareToInt("d7")] ,squares[squareToInt("e7")] ,squares[squareToInt("f7")] ,squares[squareToInt("g7")] ,squares[squareToInt("h7")]
		,squares[squareToInt("a8")] ,squares[squareToInt("h8")] ,squares[squareToInt("b8")] ,squares[squareToInt("g8")] ,squares[squareToInt("c8")] ,squares[squareToInt("f8")] ,squares[squareToInt("d8")] ,squares[squareToInt("e8")] };

	

	for (int x = 0;x < 32;x++) { //Finding starting move
		if (areEqual(PiecesStartPos[x], MoveLists[GlobIterator][0])) {
			PiecesFinalPos[x] = MoveLists[GlobIterator][1];
			actualPiece = x;
			break;
		}
	}

	OccupiedPos = { "a2","b2","c2","d2","e2","f2","g2","h2","a1","h1","b1","g1","c1","f1","d1","e1",
				   "a7","b7","c7","d7","e7","f7","g7","h7","a8","h8","b8","g8","c8","f8","d8","e8" };


	ExpandMoves();
	
}

void freeOpenGLProgram(GLFWwindow* window) {
	freeShaders();
	glDeleteTextures(1, &texBoard);
	glDeleteTextures(1, &texWhite);
	glDeleteTextures(1, &texBlack);
}

bool startedMoving(int aPieceNumb) {
	//odleglosc euklidesowa
	fullDistance = pow(pow(PiecesFinalPos[aPieceNumb].x - PiecesStartPos[aPieceNumb].x, 2) 
				+ pow(PiecesFinalPos[aPieceNumb].z - PiecesStartPos[aPieceNumb].z, 2), 0.5);
	actualDistance = pow(pow(PiecesFinalPos[aPieceNumb].x - PiecesActualPos[aPieceNumb].x, 2)
		+ pow(PiecesFinalPos[aPieceNumb].z - PiecesActualPos[aPieceNumb].z, 2), 0.5);
	if (actualDistance < 0.9 * fullDistance)
		return true;
	else return false;
}

void MoveTo(int aPieceNumb) {
	XDiff = PiecesFinalPos[aPieceNumb].x - PiecesStartPos[aPieceNumb].x;
	ZDiff = PiecesFinalPos[aPieceNumb].z - PiecesStartPos[aPieceNumb].z;
	finalX = PiecesActualPos[aPieceNumb].x + movementSpeed * XDiff;
	finalY = PiecesActualPos[aPieceNumb].y + movementSpeed/2 * YDiff;
	finalZ = PiecesActualPos[aPieceNumb].z + movementSpeed * ZDiff;
	if (PiecesFinalPos[aPieceNumb].x != PiecesStartPos[aPieceNumb].x ||
		PiecesFinalPos[aPieceNumb].z != PiecesStartPos[aPieceNumb].z) {
		if (startedMoving(aPieceNumb))
			YDiff -= 2 * movementSpeed*50;
		else
			YDiff += 2 * movementSpeed*50;

		if (abs(PiecesFinalPos[aPieceNumb].x - finalX) < (movementSpeed*1.2)*abs(XDiff)) {
			finalX = PiecesFinalPos[aPieceNumb].x;
			XDiff = 0;
		}
		if (abs(PiecesFinalPos[aPieceNumb].y - finalY) < movementSpeed*30 && startedMoving(aPieceNumb)) {
			finalY = PiecesFinalPos[aPieceNumb].y;
			YDiff = 0;
		}
		if (abs(PiecesFinalPos[aPieceNumb].z - finalZ) < (movementSpeed*1.2)*abs(ZDiff)) {
			finalZ = PiecesFinalPos[aPieceNumb].z;
			ZDiff = 0;
		}
	}
	else
		finalY = 0;

	PiecesActualPos[aPieceNumb] = glm::vec3(finalX, finalY, finalZ);
}

bool MoveEnded(int PieceNumber, glm::vec3 expectedPosition) {
	if (areEqual(PiecesActualPos[PieceNumber],expectedPosition))
		return true;
	else return false;
}

void drawAllPieces(float angle_x, float angle_y) {
	if (MoveEnded(actualPiece, UpdatedMoves[GlobIterator][1])) {
		PiecesStartPos[actualPiece] = UpdatedMoves[GlobIterator][1];
		YDiff = 40;
		if (GlobIterator +1 < movePassed) //moves table not ended
			GlobIterator++; //move ended, jump to another;
		for (int x = 0;x < 32;x++) {
			if (areEqual(PiecesStartPos[x],UpdatedMoves[GlobIterator][0])) {
				PiecesFinalPos[x] = UpdatedMoves[GlobIterator][1];
				actualPiece = x;
				break;
			}
		}
	}

	// Draw white pieces
	for (int i = 0; i < 8; i++) {
		pawn.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[i], false);
	}

	rook.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[8], false);
	rook.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[9], false);

	knight.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[10], false);
	knight.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[11], false);

	bishop.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[12], false);
	bishop.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[13], false);

	queen.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[14], false);
	king.drawSolidAtPosition(texWhite, angle_x, angle_y, PiecesActualPos[15], false);


	// Draw black pieces
	for (int i = 0; i < 8; i++) {
		pawn.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[16+i], true);
	}


	rook.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[24], true);
	rook.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[25], true);

	knight.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[26], true);
	knight.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[27], true);

	bishop.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[28], true);
	bishop.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[29], true);

	queen.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[30], true);
	king.drawSolidAtPosition(texBlack, angle_x, angle_y, PiecesActualPos[31], true);
	
	for (int Piece = 0;Piece < 32;Piece++) {
		MoveTo(Piece);
	}
}


//Drawing procedure
void drawScene(GLFWwindow* window, float angle_x, float angle_y) {
	//************Place any code here that draws something inside the window******************l
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); //Clear color and depth buffers
	glm::mat4 P = glm::perspective(glm::radians(fov), 1.0f, 1.0f, 50.0f); //Compute projection matrix
	glm::mat4 V = glm::lookAt(cameraPos, cameraPos + cameraFront, cameraUp); //Compute view matrix
	spLambertTextured->use();
	glUniformMatrix4fv(spLambertTextured->u("P"), 1, false, glm::value_ptr(P));
	glUniformMatrix4fv(spLambertTextured->u("V"), 1, false, glm::value_ptr(V));
	glm::vec4 pointLightPositions[] = {
	 glm::vec4(0, 10, 0, 1),
	 glm::vec4( 30, 50, -30, 1),
	 glm::vec4(-30, 50, 30, 1),
	 glm::vec4(30, 50, 30, 1),
	 glm::vec4(-30, 50, -30, 1),
	};
	glUniform4fv(spLambertTextured->u("list"), 5, glm::value_ptr(pointLightPositions[0]));

	chessboard.drawSolid(texBoard, angle_x, angle_y);
	drawAllPieces(angle_x, angle_y);

	glfwSwapBuffers(window); //Copy back buffer to the front buffer
}
void game_header_printout(const pgn::Game& game)
{
	pgn::TagList tags = game.tags();

	std::string white_player = tags["White"].value();
	std::string black_player = tags["Black"].value();

	//std::cout << std::endl << std::endl << "------------- " << white_player << " - " << black_player << " -------------" << std::endl << std::endl;
}
void move_printout(const pgn::Ply& ply,bool isBlack)
{
	if (ply.isLongCastle()) {
		if (isBlack) {
			//31 i 24
			MoveCharLists[moves].push_back("e8"); //KING
			MoveCharLists[moves].push_back("c8");
			MoveLists[moves].push_back(squares[squareToInt("e8")]);
			MoveLists[moves++].push_back(squares[squareToInt("c8")]);

			MoveCharLists[moves].push_back("a8"); //ROOK
			MoveCharLists[moves].push_back("d8");
			MoveLists[moves].push_back(squares[squareToInt("a8")]);
			MoveLists[moves].push_back(squares[squareToInt("d8")]);
		}
		else {
			//15 i 8
			MoveCharLists[moves].push_back("e1"); //KING
			MoveCharLists[moves].push_back("c1");
			MoveLists[moves].push_back(squares[squareToInt("e1")]);
			MoveLists[moves++].push_back(squares[squareToInt("c1")]);

			MoveCharLists[moves].push_back("a1"); //ROOK
			MoveCharLists[moves].push_back("d1");
			MoveLists[moves].push_back(squares[squareToInt("a1")]);
			MoveLists[moves].push_back(squares[squareToInt("d1")]);
		}
	}
	else if (ply.isShortCastle()) {
		if (isBlack) {
			//15 i 9
			MoveCharLists[moves].push_back("e8"); //KING
			MoveCharLists[moves].push_back("g8");
			MoveLists[moves].push_back(squares[squareToInt("e8")]);
			MoveLists[moves++].push_back(squares[squareToInt("g8")]);

			MoveCharLists[moves].push_back("h8"); //ROOK
			MoveCharLists[moves].push_back("f8");
			MoveLists[moves].push_back(squares[squareToInt("h8")]);
			MoveLists[moves].push_back(squares[squareToInt("f8")]);
		}
		else {
			//31 i 25
			MoveCharLists[moves].push_back("e1"); //KING
			MoveCharLists[moves].push_back("g1");
			MoveLists[moves].push_back(squares[squareToInt("e1")]);
			MoveLists[moves++].push_back(squares[squareToInt("g1")]);

			MoveCharLists[moves].push_back("h1"); //ROOK
			MoveCharLists[moves].push_back("f1");
			MoveLists[moves].push_back(squares[squareToInt("h1")]);
			MoveLists[moves].push_back(squares[squareToInt("f1")]);
		}
		moves ++;
	}
	else {// manage normal moves conversion
		if (ply.fromSquare().str() != "" && ply.toSquare().str() != "") {
			MoveCharLists[moves].push_back(ply.fromSquare().str());
			MoveCharLists[moves].push_back(ply.toSquare().str());
			MoveLists[moves].push_back(squares[squareToInt(MoveCharLists[moves][0])]);
			MoveLists[moves].push_back(squares[squareToInt(MoveCharLists[moves][1])]);
			moves += 1;
		}
	}

}

void handleFile() {
	try
	{
		std::string fname = "sample2.pgn";
		std::ifstream pgnfile(fname.c_str());
		pgn::GameCollection games;
		pgnfile >> games;


		for (pgn::GameCollection::iterator game = games.begin(); game != games.end(); game++)
		{

			pgn::Game the_game = *game;
			game_header_printout(the_game);
			pgn::MoveList movelist = the_game.moves();
			pgn::Position p;

			for (pgn::MoveList::iterator itr = movelist.begin(); itr != movelist.end(); itr++)
			{
				pgn::Ply ply;
				ply = itr->white();
				p.update(ply);
				move_printout(ply, 0);

				ply = itr->black();
				if (!ply.valid()) break; 
				p.update(ply);
				move_printout(ply, 1);

			}
		}
	}
	catch (std::exception& e)
	{
		std::cerr << "exception: " << e.what() << std::endl;
	}
}

int main(void)
{

	GLFWwindow* window; //Pointer to object that represents the application window

	glfwSetErrorCallback(error_callback);//Register error processing callback procedure

	if (!glfwInit()) { //Initialize GLFW library
		fprintf(stderr, "Can't initialize GLFW.\n");
		exit(EXIT_FAILURE);
	}


	window = glfwCreateWindow(800, 800, "OpenGL", NULL, NULL);  //Create a window 500pxx500px titled "OpenGL" and an OpenGL context associated with it. 

	if (!window) //If no window is opened then close the program
	{
		glfwTerminate();
		exit(EXIT_FAILURE);
	}

	glfwMakeContextCurrent(window); //Since this moment OpenGL context corresponding to the window is active and all OpenGL calls will refer to this context.
	glfwSwapInterval(1); //During vsync wait for the first refresh

	GLenum err;
	if ((err = glewInit()) != GLEW_OK) { //Initialize GLEW library
		fprintf(stderr, "Can't initialize GLEW: %s\n", glewGetErrorString(err));
		exit(EXIT_FAILURE);
	}


	initSquares();
	handleFile();

	initOpenGLProgram(window); //Call initialization procedure
	
	int width, height;

	//Main application loop
	glfwSetTime(0); //clear internal timer 
	while (!glfwWindowShouldClose(window)) //As long as the window shouldnt be closed yet...
	{
		glfwGetWindowSize(window, &width, &height);
		windowResizeHandler(width, height);
		currentFrame = glfwGetTime();
		deltaTime = currentFrame - lastFrame;
		lastFrame = currentFrame;
		processInput(window);

		glClearColor(0.1f, 0.1f, 0.1f, 1.0f);

		drawScene(window, angle_x, angle_y); //Execute drawing procedure
		glfwPollEvents(); //Process callback procedures corresponding to the events that took place up to now
	}
	freeOpenGLProgram(window);

	glfwDestroyWindow(window); //Delete OpenGL context and the window.
	glfwTerminate(); //Free GLFW resources
	exit(EXIT_SUCCESS);
}
